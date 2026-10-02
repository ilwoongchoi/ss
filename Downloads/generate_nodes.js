"use strict";
/*
  GENERATE MISSING CIRCUIT NODES FOR EMPTY BODY SPACES
  Based on structural rules from prose files:
  - Each body region maps to a circuit node via cognitive function → 8D dim
  - Toroidal symmetry: left/right pairs exist
  - 6 domains per node: physicochemical, cosmological, geological, biological, neuroscience, haplogenetics
  - Each node gets: gate type, element, particle, 8D dim, location
  - Particles assigned from the 12-particle framework + circuit-specific particles
  - Gate types follow the existing distribution pattern

  Rules for node generation:
  1. If right side exists but left doesn't → mirror with inverted polarity
  2. If neither exists → create from 8D dimension mapping for that body region
  3. Internal organs get biological gate types (tristate, MUX)
  4. Surface points get AND/OR gates (sensory/motor)
  5. Brain regions get D flip-flops (memory/state)
*/

const fs = require('fs');

// Existing nodes with locations (from analysis)
const existingNodes = JSON.parse(fs.readFileSync('existing_nodes.json', 'utf8'));

// Empty regions from analysis
const emptyRegions = [
  'bladder', 'diaphragm', 'left ankle', 'left arm', 'left cheek', 'left clavicle',
  'left dorsal foot', 'left eye inner', 'left fingers', 'left hand', 'left jaw',
  'left kidney', 'left lung', 'left nose', 'left popliteal', 'left shoulder',
  'left temple', 'left testis', 'left tibial', 'left upper back', 'left wrist',
  'nose center', 'prostate', 'right abdomen', 'right ankle', 'right calf',
  'right cheek', 'right clavicle', 'right dorsal foot', 'right femoral',
  'right forehead', 'right genital', 'right jaw', 'right kidney', 'right knee',
  'right lung', 'right neck', 'right nipple', 'right nose', 'right popliteal',
  'right shoulder', 'right testis', 'right tibial', 'right upper back',
  'right waist', 'spleen', 'uterus'
];

// 8D dimension → body region mapping (from 03_ferric_compression.md 16-window structure)
const dimBodyMap = {
  r: ['left forehead', 'right forehead', 'left calf', 'right calf', 'left foot', 'right foot'],
  h: ['left temple', 'right temple', 'left chest', 'right chest', 'left lung', 'right lung'],
  d: ['left nose', 'right nose', 'nose center', 'left gluteal', 'right gluteal', 'left genital', 'right genital'],
  p: ['left brain inner', 'right brain inner', 'left occipital', 'right occipital', 'scalp'],
  s: ['left eye inner', 'right eye inner', 'left ear', 'right ear', 'left cheek', 'right cheek'],
  gamma: ['left shoulder', 'right shoulder', 'left upper back', 'right upper back', 'left lat dorsi', 'right lat dorsi'],
  g: ['left hand', 'right hand', 'left fingers', 'right fingers', 'left wrist', 'right wrist', 'left arm', 'right arm'],
  nu: ['left hip', 'right hip', 'left waist', 'right waist', 'left lower back', 'right lower back'],
};

// Particle assignments by body region type
const regionParticles = {
  'left eye inner': 'photon', 'right eye inner': 'photon',
  'left nose': 'quark', 'right nose': 'quark', 'nose center': 'graviton',
  'left temple': 'muon', 'right temple': 'muon',
  'left cheek': 'electron', 'right cheek': 'electron',
  'left jaw': 'tau', 'right jaw': 'tau',
  'left shoulder': 'w_boson', 'right shoulder': 'w_boson',
  'left arm': 'gluon', 'right arm': 'gluon',
  'left wrist': 'neutrino', 'right wrist': 'neutrino',
  'left hand': 'proton', 'right hand': 'proton',
  'left fingers': 'photon', 'right fingers': 'photon',
  'left ankle': 'z_boson', 'right ankle': 'z_boson',
  'left popliteal': 'neutrino', 'right popliteal': 'neutrino',
  'left tibial': 'muon', 'right tibial': 'muon',
  'left dorsal foot': 'electron', 'right dorsal foot': 'electron',
  'left kidney': 'higgs', 'right kidney': 'higgs',
  'left lung': 'photon', 'right lung': 'photon',
  'left upper back': 'w_boson', 'right upper back': 'w_boson',
  'left clavicle': 'proton', 'right clavicle': 'proton',
  'left testis': 'z_boson', 'right testis': 'z_boson',
  'right forehead': 'electron',
  'right genital': 'proton',
  'right neck': 'muon',
  'right nipple': 'gluon',
  'right abdomen': 'higgs',
  'right calf': 'tau',
  'right knee': 'graviton',
  'right waist': 'neutrino',
  'bladder': 'neutrino',
  'diaphragm': 'photon',
  'prostate': 'z_boson',
  'spleen': 'strange_quark',
  'uterus': 'higgs',
};

// Element assignment: continue from 118+ (new elements for missing nodes)
// Use atomic numbers 119-128 for the 10 missing profiles, then extend
const regionElements = {
  'left eye inner': 'Cu(29)', 'right eye inner': 'Cu(29)',
  'left nose': 'Si(14)', 'right nose': 'Si(14)', 'nose center': 'Ca(20)',
  'left temple': 'Mn(25)', 'right temple': 'Mn(25)',
  'left cheek': 'K(19)', 'right cheek': 'K(19)',
  'left jaw': 'Ti(22)', 'right jaw': 'Ti(22)',
  'left shoulder': 'Zn(30)', 'right shoulder': 'Zn(30)',
  'left arm': 'Ga(31)', 'right arm': 'Ga(31)',
  'left wrist': 'Ge(32)', 'right wrist': 'Ge(32)',
  'left hand': 'As(33)', 'right hand': 'As(33)',
  'left fingers': 'Se(34)', 'right fingers': 'Se(34)',
  'left ankle': 'Br(35)', 'right ankle': 'Br(35)',
  'left popliteal': 'Kr(36)', 'right popliteal': 'Kr(36)',
  'left tibial': 'Rb(37)', 'right tibial': 'Rb(37)',
  'left dorsal foot': 'Sr(38)', 'right dorsal foot': 'Sr(38)',
  'left kidney': 'Y(39)', 'right kidney': 'Y(39)',
  'left lung': 'Zr(40)', 'right lung': 'Zr(40)',
  'left upper back': 'Nb(41)', 'right upper back': 'Nb(41)',
  'left clavicle': 'Mo(42)', 'right clavicle': 'Mo(42)',
  'left testis': 'Tc(43)', 'right testis': 'Tc(43)',
  'right forehead': 'Ru(44)',
  'right genital': 'Rh(45)',
  'right neck': 'Pd(46)',
  'right nipple': 'Ag(47)',
  'right abdomen': 'Cd(48)',
  'right calf': 'In(49)',
  'right knee': 'Sn(50)',
  'right waist': 'Sb(51)',
  'bladder': 'Te(52)',
  'diaphragm': 'I(53)',
  'prostate': 'Xe(54)',
  'spleen': 'Cs(55)',
  'uterus': 'Ba(56)',
};

// Gate type by region type
function getGateType(region) {
  if (region.includes('brain') || region.includes('occipital') || region.includes('scalp')) return 'D flip-flop';
  if (region.includes('kidney') || region.includes('lung') || region.includes('spleen') || region.includes('uterus') || region.includes('bladder') || region.includes('diaphragm') || region.includes('prostate')) return 'tristate';
  if (region.includes('eye') || region.includes('ear') || region.includes('nose') || region.includes('cheek') || region.includes('temple')) return 'MUX';
  if (region.includes('jaw') || region.includes('shoulder') || region.includes('arm') || region.includes('wrist') || region.includes('hand') || region.includes('finger') || region.includes('ankle') || region.includes('calf') || region.includes('knee') || region.includes('clavicle') || region.includes('neck') || region.includes('back') || region.includes('waist') || region.includes('forehead') || region.includes('genital') || region.includes('testis') || region.includes('abdomen') || region.includes('nipple') || region.includes('dorsal') || region.includes('popliteal') || region.includes('tibial')) return 'AND';
  return 'OR';
}

// 8D dimension for region
function getDim8(region) {
  for (const dim in dimBodyMap) {
    if (dimBodyMap[dim].includes(region)) return dim;
  }
  // Default by region type
  if (region.includes('eye')) return 's';
  if (region.includes('nose')) return 'd';
  if (region.includes('temple') || region.includes('lung') || region.includes('chest')) return 'h';
  if (region.includes('shoulder') || region.includes('back')) return 'gamma';
  if (region.includes('hand') || region.includes('finger') || region.includes('arm') || region.includes('wrist')) return 'g';
  if (region.includes('hip') || region.includes('waist') || region.includes('lower back')) return 'nu';
  if (region.includes('forehead') || region.includes('calf') || region.includes('foot')) return 'r';
  if (region.includes('brain') || region.includes('occipital')) return 'p';
  return 'r';
}

// Generate node name from region
function nodeName(region) {
  return region.replace(/\s+/g, '_').replace(/left_/g, 'left_').replace(/right_/g, 'right_');
}

// ============================================================
// GENERATE MISSING NODES
// ============================================================
const newNodes = [];
let newId = 283;

for (const region of emptyRegions) {
  const name = nodeName(region);
  const particle = regionParticles[region] || 'proton';
  const element = regionElements[region] || 'Fe(26)';
  const gateType = getGateType(region);
  const dim8 = getDim8(region);
  const side = region.startsWith('left') ? 'left' : (region.startsWith('right') ? 'right' : 'center');

  // Find mirror node (if right exists, create left mirror and vice versa)
  const mirrorRegion = side === 'left' ? 'right' + region.substring(4) :
                       side === 'right' ? 'left' + region.substring(5) : null;
  const mirrorExists = mirrorRegion && !emptyRegions.includes(mirrorRegion);

  newNodes.push({
    id: newId++,
    name: name,
    gateType: gateType,
    particle: particle,
    element: element,
    location: `LOCATION: ${region}`,
    dim8: `8D: ${dim8}-dim`,
    side: side,
    mirror: mirrorRegion,
    mirrorExists: mirrorExists,
    domain: 'biological',
    cosmicMapping: '', // to be filled from 05_energy_master.md mirror table
    earthMapping: '',  // to be filled from geo_mirror table
  });
}

// ============================================================
// OUTPUT
// ============================================================
console.log('='.repeat(100));
console.log(`GENERATED ${newNodes.length} MISSING CIRCUIT NODES`);
console.log('='.repeat(100));

console.log('\n## NEW NODES\n');
console.log('ID  | Node Name                        | Gate         | Particle       | Element    | 8D | Location           | Mirror');
console.log('-'.repeat(120));

for (const n of newNodes) {
  console.log(
    `${String(n.id).padEnd(4)}| ${n.name.padEnd(32)}| ${n.gateType.padEnd(12)}| ${n.particle.padEnd(14)}| ${n.element.padEnd(10)}| ${n.dim8.padEnd(3)}| ${n.name.padEnd(18)}| ${n.mirror || '-'}`
  );
}

// Group by particle
console.log('\n## NEW NODES BY PARTICLE\n');
const byParticle = {};
for (const n of newNodes) {
  if (!byParticle[n.particle]) byParticle[n.particle] = [];
  byParticle[n.particle].push(n.name);
}
for (const p of Object.keys(byParticle).sort()) {
  console.log(`  ${p}: ${byParticle[p].length} → ${byParticle[p].join(', ')}`);
}

// Group by 8D dim
console.log('\n## NEW NODES BY 8D DIMENSION\n');
const byDim = {};
for (const n of newNodes) {
  const dim = n.dim8.split(':')[1].trim().split('-')[0];
  if (!byDim[dim]) byDim[dim] = [];
  byDim[dim].push(n.name);
}
for (const d of Object.keys(byDim).sort()) {
  console.log(`  ${d}: ${byDim[d].length} → ${byDim[d].join(', ')}`);
}

// Group by gate type
console.log('\n## NEW NODES BY GATE TYPE\n');
const byGate = {};
for (const n of newNodes) {
  if (!byGate[n.gateType]) byGate[n.gateType] = [];
  byGate[n.gateType].push(n.name);
}
for (const g of Object.keys(byGate).sort()) {
  console.log(`  ${g}: ${byGate[g].length} → ${byGate[g].join(', ')}`);
}

// Mirror pairs analysis
console.log('\n## MIRROR PAIR ANALYSIS\n');
for (const n of newNodes) {
  if (n.side === 'left' && n.mirror && !n.mirrorExists) {
    console.log(`  [BOTH MISSING] ${n.name} ↔ ${n.mirror.replace(/\s+/g, '_')} (both sides empty)`);
  } else if (n.side === 'left' && n.mirror && n.mirrorExists) {
    console.log(`  [MIRROR EXISTS] ${n.name} ↔ ${n.mirror} (right side has node)`);
  } else if (n.side === 'right' && n.mirror && !n.mirrorExists) {
    // already covered by left side
  } else if (n.side === 'center') {
    console.log(`  [CENTER] ${n.name} (no mirror)`);
  }
}

// Wiring suggestions
console.log('\n## SUGGESTED WIRING FOR NEW NODES\n');
for (const n of newNodes) {
  const dim = n.dim8.split(':')[1].trim().split('-')[0];
  // Connect to observer_leftd2 bus (master permissive)
  // Connect to existing nodes in same 8D dim
  const sameDimNodes = existingNodes.filter(en => en.dim8 && en.dim8.includes(dim));
  const suggestedInputs = sameDimNodes.slice(0, 2).map(en => en.name);
  console.log(`  ${n.name} [${n.gateType}]:`);
  console.log(`    in0 ← ${suggestedInputs[0] || 'observer_leftd2.out0'}`);
  console.log(`    in1 ← ${suggestedInputs[1] || 'observer_leftd2.out0'}`);
  console.log(`    out → (connect to downstream nodes in ${dim}-dim pathway)`);
  console.log(`    PHYSICS: element=${n.element}, particle=${n.particle}`);
  console.log(`    ${n.location}`);
  console.log(`    ${n.dim8}`);
  console.log('');
}

// Summary
console.log('='.repeat(100));
console.log('SUMMARY');
console.log('='.repeat(100));
console.log(`Original nodes: 282`);
console.log(`New nodes generated: ${newNodes.length}`);
console.log(`Total nodes: ${282 + newNodes.length}`);
console.log(`Empty regions filled: ${emptyRegions.length}`);
console.log(`Particles covered: ${Object.keys(byParticle).length}`);
console.log(`8D dimensions covered: ${Object.keys(byDim).length}`);
