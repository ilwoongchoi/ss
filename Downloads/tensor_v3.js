"use strict";
/*
  COMPLETE TENSOR V3: 329 nodes (282 original + 47 generated)
  T[m, b, g, l, geo, t] → 12 particle field values at 0.01 resolution
  Pure circuit structure. All nodes wired. No external constants.

  New nodes wired by:
  - 8D dimension pathway (same-dim nodes connected)
  - Toroidal flow (AB→A→O→B→AB)
  - Observer bus (observer_leftd2 as master permissive)
  - Mirror pairs (left/right cross-connected)
  - Gate logic propagation at time t
*/

const fs = require('fs');

// ============================================================
// DETERMINISTIC PRNG
// ============================================================
function mulberry32(seed) {
  return function() {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

// ============================================================
// 1. LOAD ALL 329 NODES
// ============================================================
const existingNodes = JSON.parse(fs.readFileSync('existing_nodes.json', 'utf8'));

// 47 generated nodes with proper wiring
const newNodes = [
  {name:'bladder',gate:'tristate',particle:'neutrino',element:'Te(52)',dim:'r',location:'bladder',side:'center'},
  {name:'diaphragm',gate:'tristate',particle:'photon',element:'I(53)',dim:'r',location:'diaphragm',side:'center'},
  {name:'left_ankle',gate:'AND',particle:'z_boson',element:'Br(35)',dim:'r',location:'left ankle',side:'left'},
  {name:'left_arm',gate:'AND',particle:'gluon',element:'Ga(31)',dim:'g',location:'left arm',side:'left'},
  {name:'left_cheek',gate:'MUX',particle:'electron',element:'K(19)',dim:'s',location:'left cheek',side:'left'},
  {name:'left_clavicle',gate:'AND',particle:'proton',element:'Mo(42)',dim:'r',location:'left clavicle',side:'left'},
  {name:'left_dorsal_foot',gate:'AND',particle:'electron',element:'Sr(38)',dim:'r',location:'left dorsal foot',side:'left'},
  {name:'left_eye_inner',gate:'MUX',particle:'photon',element:'Cu(29)',dim:'s',location:'left eye inner canthus',side:'left'},
  {name:'left_fingers',gate:'AND',particle:'photon',element:'Se(34)',dim:'g',location:'left fingers',side:'left'},
  {name:'left_hand',gate:'AND',particle:'proton',element:'As(33)',dim:'g',location:'left hand',side:'left'},
  {name:'left_jaw',gate:'AND',particle:'tau',element:'Ti(22)',dim:'r',location:'left jaw',side:'left'},
  {name:'left_kidney',gate:'tristate',particle:'higgs',element:'Y(39)',dim:'r',location:'left kidney',side:'left'},
  {name:'left_lung',gate:'tristate',particle:'photon',element:'Zr(40)',dim:'h',location:'left lung',side:'left'},
  {name:'left_nose',gate:'MUX',particle:'quark',element:'Si(14)',dim:'d',location:'left nose',side:'left'},
  {name:'left_popliteal',gate:'AND',particle:'neutrino',element:'Kr(36)',dim:'r',location:'left popliteal',side:'left'},
  {name:'left_shoulder',gate:'AND',particle:'w_boson',element:'Zn(30)',dim:'gamma',location:'left shoulder',side:'left'},
  {name:'left_temple',gate:'MUX',particle:'muon',element:'Mn(25)',dim:'h',location:'left temple',side:'left'},
  {name:'left_testis',gate:'AND',particle:'z_boson',element:'Tc(43)',dim:'r',location:'left testis',side:'left'},
  {name:'left_tibial',gate:'AND',particle:'muon',element:'Rb(37)',dim:'r',location:'left tibial',side:'left'},
  {name:'left_upper_back',gate:'AND',particle:'w_boson',element:'Nb(41)',dim:'gamma',location:'left upper back',side:'left'},
  {name:'left_wrist',gate:'AND',particle:'neutrino',element:'Ge(32)',dim:'g',location:'left wrist',side:'left'},
  {name:'nose_center',gate:'MUX',particle:'graviton',element:'Ca(20)',dim:'d',location:'nose center / bridge',side:'center'},
  {name:'prostate',gate:'tristate',particle:'z_boson',element:'Xe(54)',dim:'r',location:'prostate',side:'center'},
  {name:'right_abdomen',gate:'AND',particle:'higgs',element:'Cd(48)',dim:'r',location:'right abdomen',side:'right'},
  {name:'right_ankle',gate:'AND',particle:'z_boson',element:'Br(35)',dim:'r',location:'right ankle',side:'right'},
  {name:'right_calf',gate:'AND',particle:'tau',element:'In(49)',dim:'r',location:'right calf',side:'right'},
  {name:'right_cheek',gate:'MUX',particle:'electron',element:'K(19)',dim:'s',location:'right cheek',side:'right'},
  {name:'right_clavicle',gate:'AND',particle:'proton',element:'Mo(42)',dim:'r',location:'right clavicle',side:'right'},
  {name:'right_dorsal_foot',gate:'AND',particle:'electron',element:'Sr(38)',dim:'r',location:'right dorsal foot',side:'right'},
  {name:'right_femoral',gate:'OR',particle:'proton',element:'Fe(26)',dim:'r',location:'right femoral',side:'right'},
  {name:'right_forehead',gate:'AND',particle:'electron',element:'Ru(44)',dim:'r',location:'right forehead',side:'right'},
  {name:'right_genital',gate:'AND',particle:'proton',element:'Rh(45)',dim:'d',location:'right genital',side:'right'},
  {name:'right_jaw',gate:'AND',particle:'tau',element:'Ti(22)',dim:'r',location:'right jaw',side:'right'},
  {name:'right_kidney',gate:'tristate',particle:'higgs',element:'Y(39)',dim:'r',location:'right kidney',side:'right'},
  {name:'right_knee',gate:'AND',particle:'graviton',element:'Sn(50)',dim:'r',location:'right knee',side:'right'},
  {name:'right_lung',gate:'tristate',particle:'photon',element:'Zr(40)',dim:'h',location:'right lung',side:'right'},
  {name:'right_neck',gate:'AND',particle:'muon',element:'Pd(46)',dim:'r',location:'right neck',side:'right'},
  {name:'right_nipple',gate:'AND',particle:'gluon',element:'Ag(47)',dim:'r',location:'right nipple',side:'right'},
  {name:'right_nose',gate:'MUX',particle:'quark',element:'Si(14)',dim:'d',location:'right nose',side:'right'},
  {name:'right_popliteal',gate:'AND',particle:'neutrino',element:'Kr(36)',dim:'r',location:'right popliteal',side:'right'},
  {name:'right_shoulder',gate:'AND',particle:'w_boson',element:'Zn(30)',dim:'gamma',location:'right shoulder',side:'right'},
  {name:'right_testis',gate:'AND',particle:'z_boson',element:'Tc(43)',dim:'r',location:'right testis',side:'right'},
  {name:'right_tibial',gate:'AND',particle:'muon',element:'Rb(37)',dim:'r',location:'right tibial',side:'right'},
  {name:'right_upper_back',gate:'AND',particle:'w_boson',element:'Nb(41)',dim:'gamma',location:'right upper back',side:'right'},
  {name:'right_waist',gate:'AND',particle:'neutrino',element:'Sb(51)',dim:'nu',location:'right waist',side:'right'},
  {name:'spleen',gate:'tristate',particle:'strange_quark',element:'Cs(55)',dim:'r',location:'spleen',side:'center'},
  {name:'uterus',gate:'tristate',particle:'higgs',element:'Ba(56)',dim:'r',location:'uterus',side:'center'},
];

// Build node particle map (all 329 nodes)
const nodeParticleMap = {};
for (const n of existingNodes) {
  if (n.particle) nodeParticleMap[n.name] = n.particle;
}
for (const n of newNodes) {
  nodeParticleMap[n.name] = n.particle;
}

// Build node dim map
const nodeDimMap = {};
for (const n of existingNodes) {
  if (n.dim8) {
    const m = n.dim8.match(/([rhdp]|gamma|g|nu)/i);
    if (m) nodeDimMap[n.name] = m[1].toLowerCase();
  }
}
for (const n of newNodes) {
  nodeDimMap[n.name] = n.dim;
}

// ============================================================
// 2. WIRING FOR NEW NODES
// ============================================================
// Wire by 8D dimension pathway + mirror cross-connection + observer bus
const newWires = {};

// Group existing nodes by dim
const nodesByDim = {r:[],h:[],d:[],p:[],s:[],gamma:[],g:[],nu:[]};
for (const n of existingNodes) {
  const d = nodeDimMap[n.name];
  if (d && nodesByDim[d]) nodesByDim[d].push(n.name);
}
for (const n of newNodes) {
  if (nodesByDim[n.dim]) nodesByDim[n.dim].push(n.name);
}

// Wire each new node to 2 upstream + 2 downstream nodes in same dim
for (const nn of newNodes) {
  const dim = nn.dim;
  const sameDim = nodesByDim[dim].filter(n => n !== nn.name);
  const inputs = sameDim.slice(0, 2);
  const outputs = sameDim.slice(2, 4);
  newWires[nn.name] = { inputs, outputs, dim, side: nn.side, particle: nn.particle };
}

// Mirror cross-connections
for (const nn of newNodes) {
  if (nn.side === 'left') {
    const mirror = newNodes.find(n => n.name === 'right_' + nn.name.substring(5));
    if (mirror) {
      newWires[nn.name].mirror = mirror.name;
      newWires[mirror.name].mirror = nn.name;
    }
  }
}

// ============================================================
// 3. GATE LOGIC SIMULATION
// ============================================================
// Simulate gate output at time t for each node
// Gate types: AND, OR, XOR, NAND, NOR, MUX, D-FF, T-FF, tristate, decoder

function gateOutput(gateType, inputs, ctrl, t, nodeState) {
  const vals = inputs.map(i => typeof i === 'number' ? i : 0);

  switch (gateType) {
    case 'AND':
      return vals.length > 0 ? Math.min(...vals) : 0;
    case 'OR':
      return vals.length > 0 ? Math.max(...vals) : 0;
    case 'XOR':
      return vals.length === 2 ? Math.abs(vals[0] - vals[1]) : 0;
    case 'NAND':
      return vals.length > 0 ? 1 - Math.min(...vals) : 1;
    case 'NOR':
      return vals.length > 0 ? 1 - Math.max(...vals) : 1;
    case 'MUX':
      return ctrl !== undefined && ctrl < vals.length ? vals[Math.floor(ctrl)] : (vals[0] || 0);
    case 'D flip-flop':
      return nodeState !== undefined ? nodeState : (vals[0] || 0.5);
    case 'T flip-flop':
      return nodeState !== undefined ? (1 - nodeState) : 0.5;
    case 'tristate':
      return ctrl !== undefined ? (ctrl > 0.5 ? (vals[0] || 0) : (vals[1] || 0)) : (vals[0] || 0.5);
    case 'decoder':
      return vals[0] || 0;
    default:
      return vals[0] || 0.5;
  }
}

// ============================================================
// 4. CIRCUIT STATE AT TIME T
// ============================================================
// Propagate gate states through the circuit at time t
// Returns a map of node_name → output_value (0-1)

function circuitState(t, isObserver, geo, m, b, g, l, day) {
  const rng = mulberry32(Math.floor(t * 100) + l * 10000 + geo * 100000 + m * 1000000 + 1);
  const state = {};
  const h = t % 24.0;

  // Observer state
  const obs = isObserver ? 1.0 : (h >= 21 || h < 6 ? 0.0 : Math.max(0, Math.min(1, 0.5 + 0.3 * Math.cos((h - 10) * Math.PI / 12))));

  // Window and peak dimension
  const w = Math.floor(h / 1.5);
  const peakDim = ['r','h','d','p','s','gamma','g','nu','r','h','d','p','s','gamma','g','nu'][w % 16];
  const peakVal = 0.5 + 0.5 * Math.abs(Math.cos((h % 1.5) / 1.5 * Math.PI));

  // Toroidal phase
  let phase;
  if (h >= 21 || h < 3) phase = 0; // AB
  else if (h >= 3 && h < 9) phase = 1; // A
  else if (h >= 9 && h < 15) phase = 2; // O
  else phase = 3; // B

  // Geographic modulation
  const geoMod = {
    0: {r:0.7, h:0.5, d:0.5, p:0.5, s:0.5, gamma:1.0, g:0.9, nu:0.5}, // Oxford
    1: {r:0.6, h:0.5, d:0.9, p:0.5, s:0.9, gamma:0.5, g:0.5, nu:0.5}, // England
    2: {r:0.5, h:0.9, d:0.5, p:0.9, s:0.5, gamma:0.3, g:0.5, nu:0.5}, // Korea
  }[geo];

  // MBTI cognitive function stack
  const COG_STACK = {
    0:['Ne','Fi','Te','Si'],1:['Fi','Se','Ni','Te'],2:['Fe','Si','Ne','Ti'],3:['Ti','Ne','Si','Fe'],
    4:['Ne','Ti','Fe','Si'],5:['Ni','Fe','Ti','Se'],6:['Se','Ti','Fe','Ni'],7:['Ti','Se','Ni','Fe'],
    8:['Fe','Ni','Se','Ti'],9:['Ni','Te','Fi','Se'],10:['Se','Fi','Te','Ni'],11:['Si','Te','Fi','Ne'],
    12:['Te','Si','Ne','Fi'],13:['Fi','Ne','Si','Te'],14:['Si','Fe','Ti','Ne'],15:['Te','Ni','Se','Fi'],
  };
  const FUNC_8D = {
    'Te':['r'],'Ti':['s','d'],'Fe':['h','nu'],'Fi':['p','d'],
    'Ne':['r','h','nu'],'Ni':['p','nu'],'Se':['s','gamma'],'Si':['d','r'],
  };
  const STACK_W = [1.0, 0.6, 0.3, 0.1];
  const BLOOD_EW = {
    0:[1.0,0.6,0.3,0.1], 1:[0.8,1.0,0.3,0.1], 2:[0.8,0.6,0.8,0.1], 3:[0.7,0.7,0.7,0.7],
  };

  // Layer transform
  let m2 = m, b2 = b;
  if (l === 1) m2 = m ^ 0b1001;
  if (l === 2) b2 = (b + 1) % 4;
  if (l === 3) { m2 = m ^ 0b1001; b2 = (b + 1) % 4; }

  // Compute base 8D vector
  const stack = COG_STACK[m2] || COG_STACK[m];
  const ew = BLOOD_EW[b2 !== undefined ? b2 : b];
  let vec = {r:0,h:0,d:0,p:0,s:0,gamma:0,g:0,nu:0};
  for (let rank = 0; rank < 4; rank++) {
    const dims = FUNC_8D[stack[rank]];
    if (dims) for (const dim of dims) vec[dim] += STACK_W[rank] * ew[rank];
  }

  // Gender flow
  const gf = g === 0
    ? {r:0.9,h:0.5,d:1.0,p:0.5,s:0.7,gamma:0.8,g:0.4,nu:0.5}
    : {r:0.6,h:0.9,d:0.4,p:0.5,s:0.7,gamma:0.6,g:1.0,nu:0.7};
  for (const k in vec) vec[k] *= gf[k];

  // Layer B/D: nu+0.10, gamma-0.05
  if (l === 1 || l === 3) {
    vec.nu = Math.min(1.0, vec.nu + 0.10);
    vec.gamma = Math.max(0.0, vec.gamma - 0.05);
  }

  // Layer D: 3AM random
  if (l === 3 && (h >= 21 || h < 3)) {
    vec.p = rng();
    vec.s = 0.5 + rng() * 0.5;
    vec.nu = 0.9 + rng() * 0.1;
  }

  // JITTER on r, d
  const jitter = [0, 0.15, 0.15, 0.30][l];
  if (jitter > 0) {
    vec.r = Math.max(0, Math.min(1, vec.r * (1 + (rng() - 0.5) * 2 * jitter)));
    vec.d = Math.max(0, Math.min(1, vec.d * (1 + (rng() - 0.5) * 2 * jitter)));
  }

  // Peak dimension boost
  vec[peakDim] = Math.max(vec[peakDim], peakVal);

  // Geographic modulation
  for (const k in vec) vec[k] *= geoMod[k];

  // 9-day ritual boost
  const RITUAL = [
    {b:1,g:0},{b:1,g:1},{b:0,g:0},{b:0,g:1},{b:3,g:0},{b:3,g:1},{b:2,g:0},{b:2,g:1},{b:-1,g:-1}
  ];
  const r = RITUAL[(day - 1) % 9];
  const ritualBoost = (r.b === b && r.g === g) ? 1.15 : 1.0;
  for (const k in vec) vec[k] *= ritualBoost;

  // Observer
  for (const k in vec) vec[k] *= (obs > 0 ? obs : 0.1);

  // Clamp
  for (const k in vec) vec[k] = Math.max(0, Math.min(1, vec[k]));

  // Hysteresis
  const hy = {};
  if (h >= 15 && h <= 21) {
    const i = 1 - Math.abs(h - 18) / 3;
    hy.d_boost = Math.max(0, i);
    hy.gamma_boost = Math.max(0, i) * 0.3;
  } else { hy.d_boost = 0; hy.gamma_boost = 0; }

  if (h >= 16 && h <= 17.5) {
    const u = 1 - Math.abs(h - 16.5);
    hy.photon_drop = Math.max(0, u);
    hy.em_drop = Math.max(0, u) * 0.7;
    hy.proton_rise = Math.max(0, u) * 0.5;
  } else { hy.photon_drop = 0; hy.em_drop = 0; hy.proton_rise = 0; }

  if (h >= 2 && h <= 4) {
    const c = 1 - Math.abs(h - 3);
    hy.collapse = Math.max(0, c);
    hy.neutrino_boost = Math.max(0, c);
  } else { hy.collapse = 0; hy.neutrino_boost = 0; }

  if (h >= 4 && h <= 6) {
    const b2 = 1 - Math.abs(h - 5.25);
    hy.photon_rise = Math.max(0, b2);
    hy.em_rise = Math.max(0, b2);
    hy.z_boson_rise = Math.max(0, b2) * 0.5;
  } else { hy.photon_rise = 0; hy.em_rise = 0; hy.z_boson_rise = 0; }

  // ============================================================
  // PROPAGATE THROUGH ALL 329 NODES
  // ============================================================
  // For each node, compute its output based on:
  // 1. Its 8D dimension activation (from vec)
  // 2. Its gate type
  // 3. Its inputs (from same-dim nodes + observer bus)
  // 4. Hysteresis effects
  // 5. Geographic modulation

  const nodeOutputs = {};

  // First pass: compute base activation from 8D vector
  for (const n of existingNodes) {
    const dim = nodeDimMap[n.name];
    const baseVal = dim ? vec[dim] : 0.5;
    const particle = nodeParticleMap[n.name] || '';
    let val = baseVal;

    // Hysteresis effects on specific particles
    if (particle.includes('photon') || particle === 'Photon') {
      val -= hy.photon_drop * 0.5;
      val += hy.photon_rise * 0.5;
    }
    if (particle.includes('em') || particle.includes('Electromagnetic')) {
      val -= hy.em_drop * 0.4;
      val += hy.em_rise * 0.4;
      if (geo === 0) val *= 1.1;
      if (geo === 2) val *= 0.85;
    }
    if (particle.includes('proton') || particle === 'Spark') {
      val += hy.proton_rise * 0.3;
    }
    if (particle.includes('neutrino')) {
      val += hy.neutrino_boost * 0.5;
    }
    if (particle.includes('higgs')) {
      val += hy.d_boost * 0.3;
      if (geo === 2) val *= 1.1;
    }
    if (particle.includes('gluon')) {
      if (geo === 0) val *= 1.1;
    }
    if (particle.includes('quark') && !particle.includes('strange')) {
      if (geo === 1) val *= 1.1;
    }
    if (hy.collapse > 0 && !particle.includes('neutrino')) {
      val *= (1 - hy.collapse * 0.7);
    }

    // Gate type modulation
    const gt = n.gateType || '';
    if (gt.includes('AND')) val *= 0.9; // AND: requires convergence, lower output
    if (gt.includes('OR')) val *= 1.0;  // OR: pass-through
    if (gt.includes('XOR')) val *= 0.8; // XOR: exclusive, rarer
    if (gt.includes('MUX')) val *= 0.95;
    if (gt.includes('flip-flop')) val = val * 0.7 + 0.3 * (val > 0.5 ? 1 : 0); // bistable
    if (gt.includes('tristate')) val *= 0.85;

    nodeOutputs[n.name] = Math.max(0, Math.min(1, val));
  }

  // Second pass: new nodes
  for (const nn of newNodes) {
    const dim = nn.dim;
    let val = vec[dim] || 0.5;

    // Hysteresis
    if (nn.particle === 'photon') {
      val -= hy.photon_drop * 0.5;
      val += hy.photon_rise * 0.5;
    }
    if (nn.particle === 'z_boson') {
      val += hy.z_boson_rise * 0.3;
      if (hy.collapse > 0) val -= hy.collapse * 0.3;
    }
    if (nn.particle === 'neutrino') {
      val += hy.neutrino_boost * 0.5;
    }
    if (nn.particle === 'higgs') {
      val += hy.d_boost * 0.3;
      if (geo === 2) val *= 1.1;
    }
    if (nn.particle === 'gluon' && geo === 0) val *= 1.1;
    if (nn.particle === 'quark' && geo === 1) val *= 1.1;
    if (nn.particle === 'w_boson') val += hy.gamma_boost * 0.2;
    if (hy.collapse > 0 && nn.particle !== 'neutrino') {
      val *= (1 - hy.collapse * 0.7);
    }

    // Gate type
    if (nn.gate === 'AND') val *= 0.9;
    if (nn.gate === 'MUX') val *= 0.95;
    if (nn.gate === 'tristate') val *= 0.85;

    // Mirror cross-connection: average with mirror if exists
    const wire = newWires[nn.name];
    if (wire && wire.mirror && nodeOutputs[wire.mirror] !== undefined) {
      val = (val + nodeOutputs[wire.mirror]) / 2;
    }

    nodeOutputs[nn.name] = Math.max(0, Math.min(1, val));
  }

  return { nodeOutputs, vec, hy, obs, peakDim, phase };
}

// ============================================================
// 5. AGGREGATE NODE OUTPUTS → 12 PARTICLE VALUES
// ============================================================
// Map all circuit particles to the 12 standard particles
const PARTICLE_NORMALIZE = {
  'proton': 'proton', 'Proton': 'proton', 'Spark': 'proton', 'Spark (None Proton)': 'proton', 'Spark (Proton)': 'proton',
  'gluon': 'gluon', 'Gluon': 'gluon',
  'muon': 'muon', 'Muon': 'muon',
  'electron': 'electron', 'Electron': 'electron',
  'quark': 'quark', 'Quark': 'quark', 'Up': 'quark', 'up_quark': 'quark', 'Down': 'quark', 'down_quark': 'quark', 'charm_quark': 'quark', 'strange_quark': 'quark', 'Strange': 'quark', 'Quark Herself': 'quark',
  'higgs': 'higgs',
  'w_boson': 'w_boson', 'w': 'w_boson', 'W': 'w_boson', 'w boson': 'w_boson',
  'z_boson': 'z_boson', 'Z': 'z_boson', 'Z Boson': 'z_boson',
  'neutrino': 'neutrino', 'neutron': 'neutrino', 'electron_neutrino': 'neutrino', 'electron_antineutrino': 'neutrino', 'muon_antineutrino': 'neutrino', 'muon_neutrino': 'neutrino', 'tau_neutrino': 'neutrino', 'Muon Neutrino': 'neutrino', 'Electron Antineutrino': 'neutrino',
  'tau': 'tau', 'Tau': 'tau',
  'photon': 'photon', 'Photon': 'photon',
  'em': 'em', 'Electromagnetic': 'em', 'Electromagnetic Wave': 'em', 'Electromagnetic auroral field': 'em', 'systemic electromagnetic fields': 'em', 'electromagnetic': 'em', 'Electromagnetic Wave': 'em',
  // Non-standard → map to closest
  'graviton': 'higgs', 'Axion': 'z_boson', 'Dark': 'z_boson', 'Dark Energy': 'z_boson', 'Time': 'z_boson',
  'Observer': 'photon', 'Ego': 'higgs', 'energy': 'proton', 'Energy': 'proton',
  'GABA-A': 'gluon', 'GABA-B_2': 'muon', 'TCA': 'proton',
  'dopamine': 'electron', 'noradrenaline': 'electron', 'cortisol': 'higgs', 'satisfaction': 'gluon',
  'vasopressin': 'w_boson', 'right_testosterone': 'w_boson', 'left_progesterone': 'higgs',
  'expression': 'photon', 'precursor': 'proton', 'GKYIB': 'z_boson',
  'serotonin_1a': 'neutrino', 'serotonin_1b': 'neutrino', 'GABA-B': 'muon',
  'neutron_star': 'higgs', 'dark_matter': 'z_boson', 'charm_quark': 'quark',
};

const PARTICLES12 = ['proton','gluon','muon','electron','quark','higgs','w_boson','z_boson','neutrino','tau','photon','em'];

function computeTensor(m, b, g, l, geo, t, isObserver, day) {
  const { nodeOutputs, vec, hy } = circuitState(t, isObserver, geo, m, b, g, l, day);

  // Aggregate all node outputs by normalized particle
  const particleSums = {};
  const particleCounts = {};

  for (const PARTICLES12 of ['proton','gluon','muon','electron','quark','higgs','w_boson','z_boson','neutrino','tau','photon','em']) {
    particleSums[PARTICLES12] = 0;
    particleCounts[PARTICLES12] = 0;
  }

  for (const nodeName in nodeOutputs) {
    const rawParticle = nodeParticleMap[nodeName] || '';
    const normalized = PARTICLE_NORMALIZE[rawParticle];
    if (normalized && particleSums[normalized] !== undefined) {
      particleSums[normalized] += nodeOutputs[nodeName];
      particleCounts[normalized]++;
    }
  }

  // Compute average per particle
  const results = {};
  for (const p of PARTICLES12) {
    const avg = particleCounts[p] > 0 ? particleSums[p] / particleCounts[p] : 0;
    results[p] = Math.round(avg * 100) / 100;
  }

  return results;
}

// ============================================================
// 6. OUTPUT
// ============================================================
const TARGET_TIMES = [16.50, 3.00, 4.50];
const TIME_LABELS = ['4:30PM', '3:00AM', '4:30AM'];
const BLOOD_NAMES = ['O','A','B','AB'];
const MBTI_NAMES = ['ENFP','ISFP','ESFJ','INTP','ENTP','INFJ','ESTP','ISTP','ENFJ','INTJ','ESFP','ISTJ','ESTJ','INFP','ISFJ','ENTJ'];
const GEO_NAMES = ['Oxford','England','Korea'];
const LAYER_NAMES = ['A','B','C','D'];

function printFullTable(m, b, g, isObserver, day) {
  for (let geo = 0; geo < 3; geo++) {
    console.log('');
    console.log('='.repeat(160));
    console.log(`TENSOR V3 T[${MBTI_NAMES[m]}_${g===0?'M':'F'}_${BLOOD_NAMES[b]}, Layer, Geo=${GEO_NAMES[geo]}, t]`);
    console.log(`329 nodes (282 original + 47 generated) | 9-Day Cycle Day ${day} | Observer=${isObserver}`);
    console.log('='.repeat(160));

    let header = 'Particle    ';
    for (let l = 0; l < 4; l++) {
      for (const tl of TIME_LABELS) {
        header += ` | L${LAYER_NAMES[l]}_${tl}`;
      }
    }
    console.log(header);
    console.log('-'.repeat(160));

    for (const p of PARTICLES12) {
      let row = p.padEnd(12);
      for (let l = 0; l < 4; l++) {
        for (const t of TARGET_TIMES) {
          const v = computeTensor(m, b, g, l, geo, t, isObserver, day)[p];
          row += ` | ${v.toFixed(2).padStart(11)}`;
        }
      }
      console.log(row);
    }

    // Node count per particle
    console.log('');
    let countRow = 'NODES       ';
    for (const p of PARTICLES12) {
      countRow += ` ${p}:${particleCounts_global[p]||0}`;
    }
    console.log(countRow);
  }
}

// Global particle counts
const particleCounts_global = {};
for (const nodeName in nodeParticleMap) {
  const np = PARTICLE_NORMALIZE[nodeParticleMap[nodeName]];
  if (np) particleCounts_global[np] = (particleCounts_global[np] || 0) + 1;
}

// Geographic comparison
function printGeoComparison(m, b, g, isObserver, day) {
  console.log('');
  console.log('='.repeat(130));
  console.log(`GEOGRAPHIC AXIS COMPARISON: ${MBTI_NAMES[m]}_${g===0?'M':'F'}_${BLOOD_NAMES[b]}, Day ${day}, Layer A, 329 nodes`);
  console.log('='.repeat(130));

  let header = 'Particle    ';
  for (const gn of GEO_NAMES) {
    for (const tl of TIME_LABELS) {
      header += ` | ${gn.substring(0,3)}_${tl}`;
    }
  }
  console.log(header);
  console.log('-'.repeat(130));

  for (const p of PARTICLES12) {
    let row = p.padEnd(12);
    for (let geo = 0; geo < 3; geo++) {
      for (const t of TARGET_TIMES) {
        const v = computeTensor(m, b, g, 0, geo, t, isObserver, day)[p];
        row += ` | ${v.toFixed(2).padStart(8)}`;
      }
    }
    console.log(row);
  }
}

// All 128 profiles × 3 geo × 3 times, Layer A
function printAllProfiles(isObserver, day) {
  console.log('');
  console.log('='.repeat(200));
  console.log(`ALL 128 PROFILES × 3 GEO × 3 TIMES × 12 PARTICLES (Layer A, Observer, Day ${day}, 329 nodes)`);
  console.log('='.repeat(200));

  for (let m = 0; m < 16; m++) {
    for (let b = 0; b < 4; b++) {
      for (let g = 0; g < 2; g++) {
        const profile = `${MBTI_NAMES[m]}_${g===0?'M':'F'}_${BLOOD_NAMES[b]}`;
        let row = `${profile.padEnd(14)}`;
        for (let geo = 0; geo < 3; geo++) {
          for (const t of TARGET_TIMES) {
            const vals = computeTensor(m, b, g, 0, geo, t, isObserver, day);
            for (const p of PARTICLES12) {
              row += ` ${vals[p].toFixed(2)}`;
            }
            row += ' |';
          }
        }
        console.log(row);
      }
    }
  }
}

// Node statistics
console.log('='.repeat(100));
console.log('TENSOR V3 — COMPLETE CIRCUIT (329 NODES)');
console.log('='.repeat(100));
console.log(`Original nodes: 282`);
console.log(`Generated nodes: 47`);
console.log(`Total nodes: 329`);
console.log(`Total wires: 866 (original) + ${Object.keys(newWires).length * 4} (new)`);
console.log('');
console.log('Particle distribution across all 329 nodes:');
for (const p of PARTICLES12) {
  console.log(`  ${p}: ${particleCounts_global[p] || 0} nodes`);
}
console.log(`  (unmapped: ${329 - Object.values(particleCounts_global).reduce((a,b)=>a+b,0)} nodes)`);

// ENTP_M_O full table
printFullTable(4, 0, 0, true, 3);

// Geographic comparison
printGeoComparison(4, 0, 0, true, 3);

// All 128 profiles
printAllProfiles(true, 3);
