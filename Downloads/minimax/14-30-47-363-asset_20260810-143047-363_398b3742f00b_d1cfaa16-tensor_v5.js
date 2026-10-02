"use strict";

const fs = require('fs');

/*
  TENSOR V5 — aligned to latest state:
  - 12 particles: Proton, Photon, Electron, Neutrino, Muon, Tau, Gluon, W-boson, Z-boson, Higgs, Axion, Quark
  - 3 routes: Oxford / Out of Oxford / Out of England
  - 3 states: RELEASE / STRESS_GROWTH / EXTREME_GROWTH
  - 84 circuit nodes from prose.txt
  - day/night graviton tracked via MC1R q/q_bar at 4:30 transitions

  T[profile, layer, route, state, time] -> {12 particle values} + graviton state
*/

const PARTICLES12 = ['proton','photon','electron','neutrino','muon','tau','gluon','w_boson','z_boson','higgs','axion','quark'];
const ROUTES = ['Oxford','Out_of_Oxford','Out_of_England'];
const STATES = ['RELEASE','STRESS_GROWTH','EXTREME_GROWTH'];
const DIMS = ['r','h','d','p','s','gamma','g','nu'];
const SCALES = ['1nm','10nm','100nm','1um','10um','100um','1mm','10mm','100mm'];

function scaleFactor(scale) {
  // 1nm = 1.0, 100mm = 0.01; smaller scale = higher resolution weight
  if (!scale) return 1.0;
  const idx = SCALES.indexOf(scale);
  if (idx < 0) return 1.0;
  return Math.pow(0.1, idx);
}

const circuit84 = JSON.parse(fs.readFileSync('circuit84_extracted.json','utf8'));

function hashCode(s) {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = ((h << 5) - h) + s.charCodeAt(i) | 0;
  return Math.abs(h);
}

// 128 profiles: 16 MBTI x 2 gender x 4 blood types
const MBTI_TYPES = [
  'INTJ','INTP','ENTJ','ENTP','INFJ','INFP','ENFJ','ENFP',
  'ISTJ','ISFJ','ESTJ','ESFJ','ISTP','ISFP','ESTP','ESFP'
];
const BLOOD_TYPES = ['O','A','B','AB'];
const GENDERS = ['M','F'];

function makeProfiles() {
  const list = [];
  for (const m of MBTI_TYPES) {
    for (const g of GENDERS) {
      for (const b of BLOOD_TYPES) {
        const label = `${m}_${g}_${b}`;
        const code = m + (g==='M'?1:0) + BLOOD_TYPES.indexOf(b);
        list.push({ label, mbti:m, gender:g, blood:b, code });
      }
    }
  }
  return list;
}
const PROFILES = makeProfiles();

// Map blood type to base scalar for 3-state logic
const BLOOD_BASE = { O:0, A:1, B:2, AB:3 };

// Layer A/B/C/D drive vector shifts (from prose.txt)
const LAYERS = ['A','B','C','D'];
function layerShift(layer, mbti, blood) {
  // A: self, B: opposite E/I + P/J, C: blood+1, D: both + 3AM random
  const bIdx = BLOOD_BASE[blood];
  const mbtiVec = mbti.split('').map((c,i)=> (i%2===0 && c==='E') || (i%2===1 && c==='J') ? 1 : 0);
  const opposite = mbti.split('').map((c,i)=>{
    if (i%2===0) return c==='E'?'I':'E';
    if (i===1 || i===3) return c==='J'?'P':'J';
    return c;
  }).join('');
  if (layer==='A') return { mbti, blood };
  if (layer==='B') return { mbti: opposite, blood };
  if (layer==='C') return { mbti, blood: BLOOD_TYPES[(bIdx+1)%4] };
  return { mbti: opposite, blood: BLOOD_TYPES[(bIdx+1)%4] };
}

// Compute 8D vector from profile + layer + state + time (simplified deterministic function)
function compute8D(profile, layer, state, time) {
  // MBTI letters to 8D rough mapping (based on prose/circuitfile analogies)
  const pVec = { r:0.5, h:0.5, d:0.5, p:0.5, s:0.5, gamma:0.5, g:0.5, nu:0.5 };
  const code = profile.mbti;
  if (code[0]==='E') pVec.p += 0.15; else pVec.nu += 0.15;
  if (code[1]==='N') pVec.nu += 0.15; else pVec.s += 0.15;
  if (code[2]==='T') pVec.d += 0.1;  else pVec.h += 0.1;
  if (code[3]==='J') pVec.p += 0.15; else pVec.r += 0.15;
  if (profile.gender==='M') pVec.r += 0.05; else pVec.gamma += 0.05;
  const bloodNudge = { O:{r:0.1}, A:{h:0.1}, B:{g:0.1}, AB:{nu:0.1} }[profile.blood] || {};
  for (const [k,v] of Object.entries(bloodNudge)) pVec[k] += v;

  // Layer modifiers
  if (layer==='B') { pVec.nu += 0.12; pVec.gamma -= 0.05; pVec.p -= 0.1; }
  if (layer==='C') { pVec.g += 0.12; }
  if (layer==='D') {
    pVec.nu += 0.25;
    // deterministic 3AM entropy from profile + time
    const h = hashCode(profile.code + String(time));
    pVec.p = ((h % 1000) / 1000) * 0.5;
    pVec.s = 0.5 + ((h % 1000) / 1000) * 0.5;
  }

  // State modifiers (RELEASE / STRESS_GROWTH / EXTREME_GROWTH)
  if (state==='STRESS_GROWTH') { pVec.d += 0.25; pVec.g += 0.15; pVec.s -= 0.1; }
  if (state==='EXTREME_GROWTH') { pVec.nu += 0.35; pVec.gamma += 0.2; pVec.p -= 0.2; pVec.d += 0.2; }

  // Time: 16 windows, day/night cycles
  const hour = Math.floor(time);
  const isNight = (hour >= 16 && hour < 4) || (hour < 4);
  if (isNight) { pVec.s -= 0.1; pVec.nu += 0.1; pVec.gamma += 0.05; }
  else { pVec.s += 0.1; pVec.p += 0.05; }

  // Normalize to 0..1
  for (const k of DIMS) pVec[k] = Math.max(0, Math.min(1, pVec[k]));
  return pVec;
}

// Determine day/night, MC1R graviton, and state from time and layer
function computeCircadian(time, layer) {
  const hour = time; // 0-24 float
  // Day = 04:30-16:30, Night = 16:30-04:30 (wrap)
  // Per prose: 04:30-16:30 RELEASE/day; 16:30-22:30 STRESS_GROWTH; 22:30-04:30 EXTREME_GROWTH/night
  const isDay = (hour >= 4.5 && hour < 16.5);
  const isTransition = (hour >= 4.0 && hour < 5.0) || (hour >= 16.0 && hour < 17.0);
  const isDeepNight = (hour >= 22.5 || hour < 4.5);
  // MC1R: day q=up_quark/Higgs, night q_bar=graviton
  const graviton = !isDay;
  const mc1rState = isDay ? 'q' : 'q_bar';

  let state = 'RELEASE';
  if (isTransition) state = 'STRESS_GROWTH';
  else if (!isDay) {
    state = isDeepNight ? 'EXTREME_GROWTH' : 'STRESS_GROWTH';
  }
  // Layer D pushes STRESS -> EXTREME in night
  if (!isDay && layer === 'D' && !isTransition) state = 'EXTREME_GROWTH';

  return { isDay, isTransition, isDeepNight, graviton, mc1rState, state };
}

// Route scaling: inner core -> outer
function routeFactor(route) {
  if (route==='Oxford') return 1.0;
  if (route==='Out_of_Oxford') return 0.65;
  return 0.35;
}

// State scaling of particle amplitudes
function stateFactor(state) {
  if (state==='RELEASE') return 1.0;
  if (state==='STRESS_GROWTH') return 1.35;
  return 1.75;
}

// Main tensor: 12-particle vector for (profile, layer, route, time)
function computeTensor(profile, layer, route, time) {
  const circ = computeCircadian(time, layer);
  const dim8 = compute8D(profile, layer, circ.state, time);

  const values = {};
  for (const p of PARTICLES12) values[p] = 0.0;

  // Graviton pseudo-particle contribution: converts to higgs/axion mix
  const gravitonAmp = circ.graviton ? 0.4 : 0.0;

  for (const node of circuit84) {
    if (!node.particle12) continue;
    let p = node.particle12;
    if (p === 'graviton') {
      // ferritin/plume/etc: map to axion at night, higgs otherwise; mc1r handled separately
      p = circ.graviton ? 'axion' : 'higgs';
    }
    if (!PARTICLES12.includes(p)) continue;

    // Node route filter
    if (route === 'Oxford' && node.route !== 'Oxford') continue;
    if (route === 'Out_of_Oxford' && node.route !== 'Out_of_Oxford' && node.route !== 'Oxford') continue;
    // Out_of_England includes all routes outward

    // Node primary dim value
    const dim = node.dim || 'g';
    const dimValue = dim8[dim] || 0.5;

    // Base contribution
    let amp = dimValue * routeFactor(route) * stateFactor(circ.state) * (1/84);

    // Graviton q/q_bar boost on D-FF nodes at night
    if (circ.graviton && node.hasQbar) amp *= 1.5;
    // Day quark confinement boost
    if (circ.isDay && (p==='quark' || p==='proton')) amp *= 1.2;

    values[p] += amp;
  }

  // Add graviton leakage to higgs (inertia) and axion (dark/circadian)
  values.higgs += gravitonAmp * 0.05;
  values.axion += gravitonAmp * 0.05;

  // Normalize so vector sums to 1.0
  const sum = Object.values(values).reduce((a,b)=>a+b,0);
  if (sum > 0) for (const p of PARTICLES12) values[p] /= sum;

  return { ...values, state: circ.state, graviton: circ.graviton, mc1rState: circ.mc1rState, dim8 };
}

// ---------- Field theory layer: interactions, evolution, conservation ----------

// 12x12 interaction matrix M[i][j]: directed influence of particle j on particle i
// Constructed from standard-model-like analogies in the prose.
// Positive = source j feeds i; negative = j drains i.
const INTERACTION = (() => {
  const M = {};
  for (const a of PARTICLES12) { M[a] = {}; for (const b of PARTICLES12) M[a][b] = 0; }
  // Strong: quark <-> gluon, proton
  M.quark.gluon = 0.8; M.gluon.quark = 0.6; M.proton.quark = 0.5; M.proton.gluon = 0.4;
  // EM: photon <-> electron, proton
  M.electron.photon = 0.5; M.photon.electron = 0.3; M.proton.photon = 0.2;
  // Weak: W <-> electron, muon, tau, neutrino; Z <-> neutrino
  M.electron.w_boson = 0.4; M.muon.w_boson = 0.3; M.tau.w_boson = 0.3; M.neutrino.w_boson = 0.2;
  M.w_boson.electron = -0.2; M.w_boson.muon = -0.1; M.w_boson.tau = -0.1;
  M.neutrino.z_boson = 0.3; M.z_boson.neutrino = 0.2;
  // Mass/Higgs: higgs feeds W/Z/higgs
  M.w_boson.higgs = 0.4; M.z_boson.higgs = 0.4; M.electron.higgs = 0.1; M.muon.higgs = 0.2; M.tau.higgs = 0.3;
  M.higgs.higgs = -0.1; // self-decay drain
  // Axion/dark mixing: axion <-> higgs, photon
  M.axion.higgs = 0.2; M.higgs.axion = 0.1; M.axion.photon = 0.1;
  // Lepton decays: muon, tau -> electron + neutrino
  M.electron.muon = 0.2; M.neutrino.muon = 0.2; M.muon.muon = -0.4;
  M.electron.tau = 0.3; M.neutrino.tau = 0.2; M.tau.tau = -0.5;
  // Quark confinement: gluon pulls quarks
  M.gluon.quark = 0.3; M.quark.gluon = 0.1;
  return M;
})();

// Particle "energy" weights (arbitrary scale; higher = more massive/inertial)
const ENERGY = {
  photon: 0, gluon: 0, electron: 0.5, neutrino: 0.1, muon: 105, tau: 1777,
  quark: 3, proton: 938, w_boson: 80379, z_boson: 91188, higgs: 125000, axion: 0.01
};

// 6 attractor loops from prose, expressed as 12-particle conservation constraints
const ATTRACTORS = {
  energy: ['proton','gluon','w_boson'],
  information: ['neutrino','quark','photon'],
  repair: ['tau','gluon','w_boson'],
  opioid: ['muon','electron','photon'],
  gan_bulkhead: ['gluon','higgs','z_boson'],
  cox_retrograde: ['electron','neutrino','photon']
};

function attractorImbalance(vec) {
  const im = {};
  for (const [name, parts] of Object.entries(ATTRACTORS)) {
    im[name] = parts.reduce((s,p)=>s+(vec[p]||0),0) - (parts.length/12);
  }
  return im;
}

function fieldEnergy(vec) {
  return PARTICLES12.reduce((s,p)=>s+(vec[p]||0)*ENERGY[p],0);
}

// Time derivative dT/dt = interaction + route/state drift + graviton leakage
function dTensor_dt(vec, route, state, graviton) {
  const d = {};
  for (const p of PARTICLES12) d[p] = 0;

  // interaction term: i changes by influence from j weighted by both abundances
  for (const i of PARTICLES12) {
    for (const j of PARTICLES12) {
      d[i] += (INTERACTION[i][j] || 0) * (vec[j] || 0) * (vec[i] || 0);
    }
  }

  // route drift: outer routes increase axion/neutrino (leakage) and deplete core
  const rf = routeFactor(route);
  d.axion += (1 - rf) * 0.05 * (vec.higgs || 0);
  d.neutrino += (1 - rf) * 0.03 * (vec.w_boson || 0);
  d.higgs -= (1 - rf) * 0.02 * (vec.higgs || 0);
  d.w_boson -= (1 - rf) * 0.02 * (vec.w_boson || 0);

  // state drift: EXTREME increases nu/axion; STRESS increases d/g
  if (state === 'STRESS_GROWTH') { d.muon += 0.02; d.tau += 0.01; d.gluon += 0.01; }
  if (state === 'EXTREME_GROWTH') { d.neutrino += 0.03; d.axion += 0.02; d.quark -= 0.01; }

  // graviton leakage: night shifts higgs to axion (q_bar dark state)
  if (graviton) {
    d.axion += 0.02 * (vec.higgs || 0);
    d.higgs -= 0.02 * (vec.higgs || 0);
  }

  return d;
}

// Evolve the tensor forward by dt using Euler, then renormalize
function evolveTensor(vec, route, state, graviton, dt, steps) {
  let current = { ...vec };
  const E0 = fieldEnergy(current);
  for (let k = 0; k < steps; k++) {
    const d = dTensor_dt(current, route, state, graviton);
    for (const p of PARTICLES12) current[p] += d[p] * dt;
    // Remove negative values and renormalize to keep probability conserved
    for (const p of PARTICLES12) current[p] = Math.max(0, current[p]);
    const sum = PARTICLES12.reduce((s,p)=>s+current[p],0);
    if (sum > 0) for (const p of PARTICLES12) current[p] /= sum;
  }
  const E1 = fieldEnergy(current);
  return { vector: current, E0, E1, imbalance: attractorImbalance(current) };
}

// Coordinate system: body (x,y,z,scale), cosmic (ra,dec,dist), geo (lat,lon,alt)
function makeCoords(type, a, b, c) {
  if (type === 'body') return { type, x: a, y: b, z: c };
  if (type === 'cosmic') return { type, ra: a, dec: b, dist: c };
  if (type === 'geo') return { type, lat: a, lon: b, alt: c };
  return { type: 'none' };
}

// Compute a single-node 12-particle vector at given state/time/route/scale.
// This is the FALL BACK mapping unit: any body/cosmic/geo object can be assigned
// a particle, dim, route, scale, and coordinate, then matched to the 84 reference nodes.
function nodeVector({ particle12, dim, route = 'Oxford', scale = '1mm', time = 10.0 }) {
  const circ = computeCircadian(time, 'A');
  const p = (particle12 === 'graviton') ? (circ.graviton ? 'axion' : 'higgs') : particle12;
  if (!PARTICLES12.includes(p)) return null;
  const vec = {};
  for (const pt of PARTICLES12) vec[pt] = 0;
  const dim8 = { r: 0.5, h: 0.5, d: 0.5, p: 0.5, s: 0.5, gamma: 0.5, g: 0.5, nu: 0.5 };
  if (dim && DIMS.includes(dim)) dim8[dim] = 1.0;
  const dVal = dim8[dim] || 0.5;
  vec[p] = dVal * routeFactor(route) * scaleFactor(scale);
  const sum = PARTICLES12.reduce((s, pt) => s + vec[pt], 0);
  if (sum > 0) for (const pt of PARTICLES12) vec[pt] /= sum;
  return vec;
}

function vectorDistance(a, b) {
  return Math.sqrt(PARTICLES12.reduce((s, p) => s + Math.pow((a[p] || 0) - (b[p] || 0), 2), 0));
}

// Map any object to the closest 84-node reference(s) by 12-particle vector similarity.
function mapToReference(target, topN = 3) {
  const tvec = nodeVector(target);
  if (!tvec) return null;
  const scored = circuit84.map(n => {
    const nvec = nodeVector({ particle12: n.particle12, dim: n.dim, route: n.route, scale: '1mm', time: target.time || 10.0 });
    return { ...n, distance: vectorDistance(tvec, nvec), vector: nvec };
  });
  scored.sort((a, b) => a.distance - b.distance);
  return { target, targetVector: tvec, matches: scored.slice(0, topN) };
}

function printTensor(profile, layer, route, time) {
  const res = computeTensor(profile, layer, route, time);
  console.log(`\nT[${profile.label}, layer ${layer}, ${route}, t=${time}]`);
  console.log(`state=${res.state}, graviton=${res.graviton}, mc1r=${res.mc1rState}`);
  console.log(PARTICLES12.map(p=>`${p}=${res[p].toFixed(4)}`).join(' | '));

  const ev = evolveTensor(res, route, res.state, res.graviton, 0.1, 10);
  console.log(`after dt=1.0: state=${res.state}, energy E0=${ev.E0.toFixed(2)} -> E1=${ev.E1.toFixed(2)}`);
  console.log(PARTICLES12.map(p=>`${p}=${ev.vector[p].toFixed(4)}`).join(' | '));
  console.log('attractor imbalance:', JSON.stringify(ev.imbalance));
}

function printMap(target) {
  const m = mapToReference(target, 3);
  console.log(`\nMAP target: ${JSON.stringify(target)}`);
  console.log('target vector:', PARTICLES12.map(p => `${p}=${m.targetVector[p].toFixed(4)}`).join(' | '));
  console.log('top matches:');
  for (const x of m.matches) {
    console.log(`  #${x.num} ${x.name} (${x.particle12}, ${x.dim}, ${x.route}) distance=${x.distance.toFixed(4)}`);
  }
}

console.log('=== TENSOR V5 FIELD ===');
console.log('Particles:', PARTICLES12.join(' '));
console.log('Routes:', ROUTES.join(' '));
console.log('States:', STATES.join(' '));
console.log('Scales:', SCALES.join(' '));

printTensor(PROFILES[0], 'A', 'Oxford', 10.0);
printTensor(PROFILES[0], 'A', 'Oxford', 16.5);
printTensor(PROFILES[0], 'D', 'Out_of_England', 2.0);

printMap({ particle12: 'w_boson', dim: 'p', route: 'Oxford', scale: '1mm', coords: makeCoords('body', 0.1, 0.2, 0.3) });
printMap({ particle12: 'neutrino', dim: 'nu', route: 'Out_of_England', scale: '100mm', coords: makeCoords('geo', 37.5, 127.0, 0) });
printMap({ particle12: 'photon', dim: 's', route: 'Out_of_Oxford', scale: '1nm', coords: makeCoords('cosmic', 10.5, -45.2, 1e20) });
