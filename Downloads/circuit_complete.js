"use strict";
/*
  COMPLETE CIRCUIT GRAPH BUILDER
  1. Parse all 282 nodes from CIRCUITFILE.MD
  2. Extract all wires (in/out connections)
  3. Extract all particles, locations, elements
  4. Find empty body spaces — regions with no nodes
  5. Generate missing nodes from structural rules
  6. Output complete graph
*/

const fs = require('fs');

const raw = fs.readFileSync('CIRCUITFILE.MD', 'utf8');
const lines = raw.split('\n');

// ============================================================
// 1. PARSE ALL NODES
// ============================================================
const nodes = {};
let currentNode = null;
let currentSection = '';

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];

  // Node definition: name [gate_type] or name [description, gate_type]
  const nodeMatch = line.match(/^([a-z][a-z0-9_]+)\s+\[([^\]]+)\]/);
  if (nodeMatch) {
    const name = nodeMatch[1];
    const bracket = nodeMatch[2];
    currentNode = name;
    if (!nodes[name]) nodes[name] = { name, gateType: '', inputs: [], outputs: [], particle: '', element: '', location: '', physics: '', wires: [] };

    // Extract gate type from bracket
    const gateTypes = ['AND', 'OR', 'XOR', 'XNOR', 'NAND', 'NOR', 'MUX', 'D flip-flop', 'T flip-flop', 'tristate', 'decoder', '2 tristate', '1 tristate', '2-output decoder', '3-output'];
    for (const gt of gateTypes) {
      if (bracket.includes(gt)) {
        nodes[name].gateType = gt;
        break;
      }
    }
    if (!nodes[name].gateType) nodes[name].gateType = bracket.split(':')[0].trim().substring(0, 30);
    continue;
  }

  if (!currentNode || !nodes[currentNode]) continue;

  // Input lines: in0 <-, in1 <-, etc
  const inMatch = line.match(/^\s*(in\d+|in_main|in_sub|in_ctrl|d|clk|enable|preset|reset|ctrl\d+)\s*<[-=]\s*(.+)/i);
  if (inMatch) {
    const port = inMatch[1].toLowerCase();
    const source = inMatch[2].trim();
    nodes[currentNode].inputs.push({ port, source, line: i + 1 });
    nodes[currentNode].wires.push({ type: 'in', port, source, line: i + 1 });
  }

  // Output lines: out0 ->, out1 ->, q ->, q_bar ->, out ->, etc
  const outMatch = line.match(/^\s*(out\d*|q|q_bar|out)\s*->\s*(.+)/i);
  if (outMatch) {
    const port = outMatch[1].toLowerCase();
    const targets = outMatch[2].trim();
    nodes[currentNode].outputs.push({ port, targets, line: i + 1 });
    nodes[currentNode].wires.push({ type: 'out', port, targets, line: i + 1 });
  }

  // PHYSICS line: element and particle
  const physMatch = line.match(/PHYSICS:.*?element=([^\s|]+).*?particle=([^\s|]+)/i);
  if (physMatch) {
    nodes[currentNode].element = physMatch[1];
    nodes[currentNode].particle = physMatch[2];
  } else {
    const elMatch = line.match(/element[=:]\s*([^\s|,]+)/i);
    const ptMatch = line.match(/particle[=:]\s*([^\s|,]+)/i);
    if (elMatch) nodes[currentNode].element = elMatch[1];
    if (ptMatch) nodes[currentNode].particle = ptMatch[1];
  }

  // LOCATION line
  const locMatch = line.match(/^LOCATION:\s*(.+)/i);
  if (locMatch) {
    nodes[currentNode].location = locMatch[1].trim();
  }

  // 8D dimension
  const dimMatch = line.match(/8D:\s*(.+)/i);
  if (dimMatch) {
    nodes[currentNode].dim8 = dimMatch[1].trim();
  }
}

// ============================================================
// 2. BUILD WIRE GRAPH
// ============================================================
const wireGraph = {}; // source_node -> [target_node, ...]
const wireDetails = []; // {from, to, fromPort, toPort, line}

for (const name in nodes) {
  const node = nodes[name];
  for (const out of node.outputs) {
    // Parse targets: "node1.port, node2.port, node3.port"
    const targets = out.targets.split(',').map(s => s.trim());
    for (const t of targets) {
      const tm = t.match(/^([a-z][a-z0-9_]+)\.([a-z0-9_]+)/i);
      if (tm) {
        const targetNode = tm[1];
        const targetPort = tm[2];
        if (!wireGraph[name]) wireGraph[name] = [];
        wireGraph[name].push(targetNode);
        wireDetails.push({ from: name, to: targetNode, fromPort: out.port, toPort: targetPort, line: out.line });
      } else {
        // Target without explicit port
        const tm2 = t.match(/^([a-z][a-z0-9_]+)/i);
        if (tm2) {
          if (!wireGraph[name]) wireGraph[name] = [];
          wireGraph[name].push(tm2[1]);
          wireDetails.push({ from: name, to: tm2[1], fromPort: out.port, toPort: '', line: out.line });
        }
      }
    }
  }
}

// ============================================================
// 3. FIND DISCONNECTED / DANGLING WIRES
// ============================================================
const dangling = [];
for (const name in nodes) {
  const node = nodes[name];
  for (const inp of node.inputs) {
    // Check if source node exists
    const srcMatch = inp.source.match(/([a-z][a-z0-9_]+)\./i) || inp.source.match(/([a-z][a-z0-9_]+)/i);
    if (srcMatch) {
      const srcNode = srcMatch[1];
      if (!nodes[srcNode] && srcNode !== 'self' && !srcNode.startsWith('0') && !srcNode.startsWith('1')) {
        dangling.push({ node: name, port: inp.port, missingSource: srcNode, line: inp.line });
      }
    }
  }
}

// ============================================================
// 4. FIND EMPTY BODY SPACES
// ============================================================
// Map all body locations from nodes
const bodyLocations = {};
for (const name in nodes) {
  if (nodes[name].location) {
    const loc = nodes[name].location.toLowerCase();
    bodyLocations[name] = loc;
  }
}

// Key body regions that should have nodes (from 02_core_nodes.md + 05_energy_master.md)
const expectedRegions = [
  { region: 'left forehead', keywords: ['forehead', 'frontalis'], side: 'left' },
  { region: 'right forehead', keywords: ['forehead', 'frontalis'], side: 'right' },
  { region: 'left eye inner', keywords: ['eye', 'canthus', 'eyelid'], side: 'left' },
  { region: 'right eye inner', keywords: ['eye', 'canthus', 'eyelid'], side: 'right' },
  { region: 'left nose', keywords: ['nose'], side: 'left' },
  { region: 'right nose', keywords: ['nose'], side: 'right' },
  { region: 'nose center', keywords: ['nose center', 'nose bridge'], side: 'center' },
  { region: 'left temple', keywords: ['temple', 'temporalis'], side: 'left' },
  { region: 'right temple', keywords: ['temple', 'temporalis'], side: 'right' },
  { region: 'left ear', keywords: ['ear', 'auricular'], side: 'left' },
  { region: 'right ear', keywords: ['ear', 'auricular'], side: 'right' },
  { region: 'scalp', keywords: ['scalp'], side: 'center' },
  { region: 'left occipital', keywords: ['occipital'], side: 'left' },
  { region: 'right occipital', keywords: ['occipital'], side: 'right' },
  { region: 'left brain inner', keywords: ['brain', 'hippocampal'], side: 'left' },
  { region: 'right brain inner', keywords: ['brain', 'insula', 'hippocampal'], side: 'right' },
  { region: 'left lip', keywords: ['lip', 'philtrum', 'orbicularis'], side: 'left' },
  { region: 'right lip', keywords: ['lip', 'orbicularis'], side: 'right' },
  { region: 'left cheek', keywords: ['cheek', 'zygomatic', 'risorius', 'buccal'], side: 'left' },
  { region: 'right cheek', keywords: ['cheek', 'zygomatic', 'risorius', 'buccal'], side: 'right' },
  { region: 'left jaw', keywords: ['jaw', 'chin', 'masseter'], side: 'left' },
  { region: 'right jaw', keywords: ['jaw', 'chin', 'masseter'], side: 'right' },
  { region: 'left neck', keywords: ['neck', 'throat', 'larynx', 'trachea'], side: 'left' },
  { region: 'right neck', keywords: ['neck', 'throat', 'larynx', 'trachea'], side: 'right' },
  { region: 'left shoulder', keywords: ['shoulder', 'deltoid', 'trapezius'], side: 'left' },
  { region: 'right shoulder', keywords: ['shoulder', 'deltoid', 'trapezius'], side: 'right' },
  { region: 'left arm', keywords: ['arm', 'bicep', 'tricep', 'forearm', 'elbow'], side: 'left' },
  { region: 'right arm', keywords: ['arm', 'bicep', 'tricep', 'forearm', 'elbow'], side: 'right' },
  { region: 'left wrist', keywords: ['wrist'], side: 'left' },
  { region: 'right wrist', keywords: ['wrist'], side: 'right' },
  { region: 'left hand', keywords: ['hand', 'palm'], side: 'left' },
  { region: 'right hand', keywords: ['hand', 'palm'], side: 'right' },
  { region: 'left fingers', keywords: ['finger', 'thumb', 'phalange'], side: 'left' },
  { region: 'right fingers', keywords: ['finger', 'thumb', 'phalange'], side: 'right' },
  { region: 'left chest', keywords: ['chest', 'pectoralis', 'rib', 'sternum', 'intercostal'], side: 'left' },
  { region: 'right chest', keywords: ['chest', 'pectoralis', 'rib', 'sternum', 'intercostal'], side: 'right' },
  { region: 'left lung', keywords: ['lung', 'pleura', 'bronchus'], side: 'left' },
  { region: 'right lung', keywords: ['lung', 'pleura', 'bronchus'], side: 'right' },
  { region: 'mediastinum', keywords: ['mediastinum', 'pericardium'], side: 'center' },
  { region: 'left abdomen', keywords: ['abdomen', 'stomach', 'liver'], side: 'left' },
  { region: 'right abdomen', keywords: ['abdomen', 'pancreas'], side: 'right' },
  { region: 'left kidney', keywords: ['kidney', 'adrenal'], side: 'left' },
  { region: 'right kidney', keywords: ['kidney', 'adrenal'], side: 'right' },
  { region: 'left hip', keywords: ['hip', 'pelvis', 'ilium'], side: 'left' },
  { region: 'right hip', keywords: ['hip', 'pelvis', 'ilium'], side: 'right' },
  { region: 'left thigh', keywords: ['thigh', 'femur'], side: 'left' },
  { region: 'right thigh', keywords: ['thigh', 'femur'], side: 'right' },
  { region: 'left knee', keywords: ['knee', 'patella'], side: 'left' },
  { region: 'right knee', keywords: ['knee', 'patella'], side: 'right' },
  { region: 'left calf', keywords: ['calf', 'tibia', 'fibula'], side: 'left' },
  { region: 'right calf', keywords: ['calf', 'tibia', 'fibula'], side: 'right' },
  { region: 'left ankle', keywords: ['ankle', 'malleolus', 'Achilles'], side: 'left' },
  { region: 'right ankle', keywords: ['ankle', 'malleolus', 'Achilles'], side: 'right' },
  { region: 'left foot', keywords: ['foot', 'sole', 'plantar', 'metatarsal', 'calcaneus'], side: 'left' },
  { region: 'right foot', keywords: ['foot', 'sole', 'plantar', 'metatarsal', 'calcaneus'], side: 'right' },
  { region: 'left toes', keywords: ['toe'], side: 'left' },
  { region: 'right toes', keywords: ['toe'], side: 'right' },
  { region: 'left genital', keywords: ['genital', 'genitalia', 'perineum', 'groin', 'inguinal'], side: 'left' },
  { region: 'right genital', keywords: ['genital', 'genitalia', 'perineum', 'groin', 'inguinal'], side: 'right' },
  { region: 'left gluteal', keywords: ['gluteal', 'bum', 'anus', 'rectum'], side: 'left' },
  { region: 'right gluteal', keywords: ['gluteal', 'bum', 'anus', 'rectum'], side: 'right' },
  { region: 'left lower back', keywords: ['lumbar', 'sacroiliac', 'sacrum', 'coccyx'], side: 'left' },
  { region: 'right lower back', keywords: ['lumbar', 'sacroiliac', 'sacrum', 'coccyx'], side: 'right' },
  { region: 'left upper back', keywords: ['thoracic', 'spine', 'spinous'], side: 'left' },
  { region: 'right upper back', keywords: ['thoracic', 'spine', 'spinous'], side: 'right' },
  { region: 'left nipple', keywords: ['nipple'], side: 'left' },
  { region: 'right nipple', keywords: ['nipple'], side: 'right' },
  { region: 'left clavicle', keywords: ['clavicle', 'sternocleidomastoid'], side: 'left' },
  { region: 'right clavicle', keywords: ['clavicle', 'sternocleidomastoid'], side: 'right' },
  { region: 'left lat dorsi', keywords: ['lat', 'dorsi'], side: 'left' },
  { region: 'right lat dorsi', keywords: ['lat', 'dorsi'], side: 'right' },
  { region: 'left armpit', keywords: ['armpit', 'axillary'], side: 'left' },
  { region: 'right armpit', keywords: ['armpit', 'axillary'], side: 'right' },
  { region: 'left waist', keywords: ['waist'], side: 'left' },
  { region: 'right waist', keywords: ['waist'], side: 'right' },
  { region: 'diaphragm', keywords: ['diaphragm'], side: 'center' },
  { region: 'spleen', keywords: ['spleen'], side: 'center' },
  { region: 'bladder', keywords: ['bladder'], side: 'center' },
  { region: 'left testis', keywords: ['testis', 'testicle', 'epididymis'], side: 'left' },
  { region: 'right testis', keywords: ['testis', 'testicle', 'epididymis'], side: 'right' },
  { region: 'uterus', keywords: ['uterus', 'ovary'], side: 'center' },
  { region: 'prostate', keywords: ['prostate', 'seminal', 'vas'], side: 'center' },
  { region: 'left femoral', keywords: ['femoral'], side: 'left' },
  { region: 'right femoral', keywords: ['femoral'], side: 'right' },
  { region: 'left popliteal', keywords: ['popliteal'], side: 'left' },
  { region: 'right popliteal', keywords: ['popliteal'], side: 'right' },
  { region: 'left tibial', keywords: ['tibial'], side: 'left' },
  { region: 'right tibial', keywords: ['tibial'], side: 'right' },
  { region: 'left dorsal foot', keywords: ['dorsal'], side: 'left' },
  { region: 'right dorsal foot', keywords: ['dorsal'], side: 'right' },
];

// Check which regions have nodes
const regionCoverage = {};
for (const er of expectedRegions) {
  let found = false;
  let foundNodes = [];
  for (const name in bodyLocations) {
    const loc = bodyLocations[name];
    if (er.side === 'center') {
      if (loc.includes(er.side) || (!loc.includes('left') && !loc.includes('right'))) {
        for (const kw of er.keywords) {
          if (loc.includes(kw)) { found = true; foundNodes.push(name); break; }
        }
      }
    } else {
      if (loc.includes(er.side)) {
        for (const kw of er.keywords) {
          if (loc.includes(kw)) { found = true; foundNodes.push(name); break; }
        }
      }
    }
  }
  regionCoverage[er.region] = { found, nodes: foundNodes, keywords: er.keywords, side: er.side };
}

// ============================================================
// 5. PARTICLES IN CIRCUIT
// ============================================================
const particleMap = {};
for (const name in nodes) {
  const p = nodes[name].particle;
  if (p) {
    if (!particleMap[p]) particleMap[p] = [];
    particleMap[p].push(name);
  }
}

// ============================================================
// 6. OUTPUT
// ============================================================
console.log('='.repeat(100));
console.log('COMPLETE CIRCUIT GRAPH ANALYSIS');
console.log('='.repeat(100));

console.log('\n## NODE STATISTICS');
console.log(`Total nodes: ${Object.keys(nodes).length}`);
console.log(`Nodes with location: ${Object.keys(bodyLocations).length}`);
console.log(`Nodes with particle: ${Object.keys(particleMap).reduce((s, p) => s + particleMap[p].length, 0)}`);
console.log(`Total wires: ${wireDetails.length}`);
console.log(`Dangling wires (missing source): ${dangling.length}`);

console.log('\n## GATE TYPE DISTRIBUTION');
const gateCounts = {};
for (const name in nodes) {
  const gt = nodes[name].gateType;
  gateCounts[gt] = (gateCounts[gt] || 0) + 1;
}
for (const gt of Object.keys(gateCounts).sort((a, b) => gateCounts[b] - gateCounts[a])) {
  console.log(`  ${gt}: ${gateCounts[gt]}`);
}

console.log('\n## PARTICLE DISTRIBUTION');
for (const p of Object.keys(particleMap).sort()) {
  console.log(`  ${p}: ${particleMap[p].length} nodes → ${particleMap[p].join(', ')}`);
}

console.log('\n## EMPTY BODY SPACES (no nodes found)');
let emptyCount = 0;
for (const region of Object.keys(regionCoverage).sort()) {
  const rc = regionCoverage[region];
  if (!rc.found) {
    console.log(`  [MISSING] ${region} (side=${rc.side}, keywords=${rc.keywords.join(',')})`);
    emptyCount++;
  }
}
console.log(`\nTotal empty regions: ${emptyCount} / ${Object.keys(regionCoverage).length}`);

console.log('\n## REGIONS WITH NODES');
for (const region of Object.keys(regionCoverage).sort()) {
  const rc = regionCoverage[region];
  if (rc.found) {
    console.log(`  [OK] ${region}: ${rc.nodes.join(', ')}`);
  }
}

console.log('\n## DANGLING WIRES (referenced but non-existent source nodes)');
for (const d of dangling) {
  console.log(`  ${d.node}.${d.port} ← ${d.missingSource} (line ${d.line})`);
}

console.log('\n## NODES WITH NO OUTPUTS (dead-end nodes)');
let deadEnds = 0;
for (const name in nodes) {
  if (nodes[name].outputs.length === 0) {
    console.log(`  ${name} [${nodes[name].gateType}]`);
    deadEnds++;
  }
}
console.log(`Total dead-end nodes: ${deadEnds}`);

console.log('\n## NODES WITH NO INPUTS (source-only nodes)');
let noInputs = 0;
for (const name in nodes) {
  if (nodes[name].inputs.length === 0) {
    console.log(`  ${name} [${nodes[name].gateType}]`);
    noInputs++;
  }
}
console.log(`Total source-only nodes: ${noInputs}`);
