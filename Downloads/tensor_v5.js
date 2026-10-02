"use strict";

const fs = require('fs');

/*
  TENSOR V5 — aligned to latest state:
  - 41 particles: 12 base + 6 quark flavors + 6 neutrino variants + compact/dark + scalars + buses + derived
  - 3 routes: Oxford / Out of Oxford / Out of England
  - 3 states: RELEASE / STRESS_GROWTH / EXTREME_GROWTH
  - 84 circuit nodes from prose.txt
  - day/night graviton tracked via MC1R q/q_bar at 4:30 transitions
  - 41-particle color hex mapping with interference colors
  - Geomagnetic modulation (outer_core_convection coupling)
  - Creative 4-shapes (STRUCTURE, FLOW, CONTRAST, EMERGENCE)
  - Route-based 41-particle system (10 routes × 4 + axion_rebrancher)
  - 6-sphere toroidal circulation (Sun→Earth→Moon→CoMag→Barnard + Geomagnetic)
  - 16-window time phase (4 macro × 4 micro, fractal reverse)
  - Master equation Ψ(t, Obs, V, A, P) with structural constants
  - 3AM HYSTERESIS / Betti 12 phase bridge
  - 4:30PM ferric event (UV shield loss → GABA-A destruction)
  - 6 geometric nodes (bypass/funnel/separatrix/observer) + Darcy leakage

  T[profile, layer, route, state, time] -> {41 particle values} + graviton state + color + geomag + shapes
  + route vector + toroidal phase + window + master Ψ + hysteresis + ferric event + geometric node + Darcy
*/

const PARTICLES12 = ['proton','photon','electron','neutrino','muon','tau','gluon','w_boson','z_boson','higgs','axion','quark'];

// 41-particle system (from nm_body_particle_map_v3.md + color_hex_mapping.md)
const PARTICLES41 = [
  'proton','photon','electron','neutrino','muon','tau','gluon','w_boson','z_boson','higgs','em_field','graviton',
  'up_quark','down_quark','charm_quark','strange_quark','top_quark','bottom_quark',
  'electron_neutrino','electron_antineutrino','muon_neutrino','muon_antineutrino','tau_neutrino','tau_antineutrino',
  'neutron','neutron_star','dark_matter','dark_energy',
  'time','energy',
  'ego_d2','left_progesterone','right_testosterone','acetyl_coa',
  'spark','clathrate_buffer','axion_rebrancher','testosterone_sex','endorphin_imag','male_gaba_a_wk','pain_eliminate'
];

// 41-particle color hex mapping
const PARTICLE_COLORS = {
  proton:{base:'RED',hex:'#FF0000'}, photon:{base:'YELLOW',hex:'#FFFF00',alt:{observer:'#FFFFFF'}},
  electron:{base:'GREEN',hex:'#00FF00'}, neutrino:{base:'YELLOW',hex:'#FFFF00',alt:{observer:'#FFFFFF'}},
  muon:{base:'RED',hex:'#FF0000',alt:{lower_mantle:'#00FFFF'}}, tau:{base:'BLUE',hex:'#0000FF'},
  gluon:{base:'WHITE',hex:'#FFFFFF'}, w_boson:{base:'RED',hex:'#FF0000'},
  z_boson:{base:'YELLOW',hex:'#FFFF00',alt:{cytochrome_c_oxidase:'#00FF00'}},
  higgs:{base:'YELLOW',hex:'#FFFF00',alt:{observer:'#FFFFFF'}},
  em_field:{base:'WHITE',hex:'#FFFFFF'}, graviton:{base:'WHITE',hex:'#FFFFFF'},
  up_quark:{base:'RED',hex:'#FF0000'}, down_quark:{base:'RED',hex:'#FF0000',alt:{cytochrome_c_oxidase:'#00FF00'}},
  charm_quark:{base:'GREEN',hex:'#00FF00'}, strange_quark:{base:'RED',hex:'#FF0000'},
  top_quark:{base:'YELLOW',hex:'#FFFF00',alt:{dark_energy:'#000000'}}, bottom_quark:{base:'GREEN',hex:'#00FF00'},
  electron_neutrino:{base:'BLUE',hex:'#0000FF'}, electron_antineutrino:{base:'GREEN',hex:'#00FF00'},
  muon_neutrino:{base:'YELLOW',hex:'#FFFF00',alt:{succinate_dehydrogenase:'#0000FF'}}, muon_antineutrino:{base:'YELLOW',hex:'#FFFF00'},
  tau_neutrino:{base:'GREEN',hex:'#00FF00'}, tau_antineutrino:{base:'GREEN',hex:'#00FF00'},
  neutron:{base:'WHITE',hex:'#FFFFFF'}, neutron_star:{base:'YELLOW',hex:'#FFFF00',alt:{observer:'#FFFFFF'}},
  dark_matter:{base:'BLACK',hex:'#000000'}, dark_energy:{base:'BLACK',hex:'#000000'},
  time:{base:'RED',hex:'#FF0000'}, energy:{base:'RED',hex:'#FF0000'},
  ego_d2:{base:'RED',hex:'#FF0000'}, left_progesterone:{base:'BLUE',hex:'#0000FF'},
  right_testosterone:{base:'RED',hex:'#FF0000'}, acetyl_coa:{base:'RED',hex:'#FF0000'},
  spark:{base:'YELLOW',hex:'#FFFF00'}, clathrate_buffer:{base:'WHITE',hex:'#FFFFFF'},
  axion_rebrancher:{base:'WHITE',hex:'#FFFFFF'}, testosterone_sex:{base:'RED',hex:'#FF0000'},
  endorphin_imag:{base:'GREEN',hex:'#00FF00'}, male_gaba_a_wk:{base:'BLUE',hex:'#0000FF'}, pain_eliminate:{base:'GREEN',hex:'#00FF00'}
};

// Interference colors
const INTERFERENCE_COLORS = {
  'hind_insula:anterior_insula':{name:'LILAC',hex:'#C8A2C8'},
  'peonidine_a:oxidized_peonidine':{name:'CRIMSON',hex:'#DC143C'},
  'peonidine_b:aglycone_peonidine':{name:'MAROON',hex:'#800000'},
  'co2:o2':{name:'GRAY-BLUE',hex:'#6A7B9B'}
};
const SPARK_INTERFERENCE = {flash:'#FFFFFF', discharge:'#000000'};

// Geomag modulation
const GEOMAG_MODULATION = {
  source:'outer_core_convection',
  coupling:['ferritin','magnetite','oxidised_manganese','laterite'],
  dimEffects:{r:-0.02, g:0.03, gamma:0.02, s:-0.01}
};

// Creative 4-shapes
const CREATIVE_4SHAPES = {
  STRUCTURE:{dims:{g:0.35,p:0.30,nu:0.20,d:0.15}},
  FLOW:{dims:{r:0.35,h:0.25,gamma:0.25,s:0.15}},
  CONTRAST:{dims:{d:0.35,s:0.30,r:0.20,p:0.15}},
  EMERGENCE:{dims:{nu:0.30,gamma:0.25,h:0.25,g:0.20}}
};
const SHAPE_ORDER = ['STRUCTURE','FLOW','CONTRAST','EMERGENCE'];

// 41-particle dim weights — corrected per MBTI node mapping:
// SF=h=gluon, EJ=g=muon, NF=nu=w_boson, EP=gamma=photon,
// IJ=s=quark, IP=r=neutrino, NT=p=higgs, ST=d=tau/z_boson
const PARTICLE_DIM_WEIGHTS_41 = {
  proton:{r:1}, photon:{gamma:1}, electron:{s:1}, neutrino:{r:1},
  muon:{g:1}, tau:{d:1}, gluon:{h:1}, w_boson:{nu:1},
  z_boson:{d:1}, higgs:{p:1}, axion:{nu:1}, quark:{s:1},
  em_field:{gamma:0.5,s:0.5}, graviton:{g:0.5,nu:0.5},
  up_quark:{s:0.6,r:0.4}, down_quark:{s:0.5,h:0.5},
  charm_quark:{g:0.6,nu:0.4}, strange_quark:{d:0.6,s:0.4},
  top_quark:{g:0.7,d:0.3}, bottom_quark:{h:0.6,g:0.4},
  electron_neutrino:{r:0.6,s:0.4}, electron_antineutrino:{r:0.5,gamma:0.5},
  muon_neutrino:{r:0.5,g:0.5}, muon_antineutrino:{r:0.4,d:0.6},
  tau_neutrino:{r:0.5,d:0.5}, tau_antineutrino:{r:0.4,p:0.6},
  neutron:{nu:0.5,d:0.5}, neutron_star:{g:0.6,nu:0.4},
  dark_matter:{d:0.6,nu:0.4}, dark_energy:{gamma:0.6,d:0.4},
  time:{r:0.5,nu:0.5}, energy:{r:0.6,p:0.4},
  ego_d2:{p:0.6,s:0.4}, left_progesterone:{h:0.6,gamma:0.4},
  right_testosterone:{r:0.6,d:0.4}, acetyl_coa:{g:0.5,d:0.5},
  spark:{s:0.5,gamma:0.5}, clathrate_buffer:{g:0.5,nu:0.5},
  axion_rebrancher:{nu:0.6,gamma:0.4}, testosterone_sex:{r:0.5,d:0.5},
  endorphin_imag:{h:0.5,nu:0.5}, male_gaba_a_wk:{g:0.6,nu:0.4}, pain_eliminate:{d:0.7,g:0.3}
};

function getParticleColor(particle, context) {
  const entry = PARTICLE_COLORS[particle];
  if (!entry) return {base:'UNKNOWN', hex:'#888888'};
  if (context && entry.alt) {
    for (const [ctxKey, ctxHex] of Object.entries(entry.alt)) {
      if (context.includes(ctxKey)) return {base:entry.base, hex:ctxHex};
    }
  }
  return entry;
}

function applyGeomagModulation(dims, observerActive) {
  const mod = {...GEOMAG_MODULATION.dimEffects};
  if (!observerActive) { mod.r *= 2.0; mod.s *= 2.0; mod.g *= -0.5; }
  const result = {...dims};
  for (const [k,v] of Object.entries(mod)) {
    if (k in result) result[k] = Math.max(0, Math.min(1, result[k] + v));
  }
  return {dims: result, geomagStable: observerActive, modulations: mod};
}

function computeCreative4Shapes(dims) {
  const scores = {};
  for (const [shape, def] of Object.entries(CREATIVE_4SHAPES)) {
    let score = 0;
    for (const [dim, weight] of Object.entries(def.dims)) {
      score += (dims[dim] || 0.5) * weight;
    }
    scores[shape] = Math.max(0, Math.min(1, score));
  }
  const ranked = SHAPE_ORDER.sort((a,b) => scores[b] - scores[a]);
  return {scores, ranked, dominant: ranked[0], weakest: ranked[3]};
}
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

  // Geomag modulation
  const observerActive = !isNight || pVec.s > 0.5;
  const geomag = applyGeomagModulation(pVec, observerActive);
  for (const k of DIMS) pVec[k] = geomag.dims[k];

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

// Main tensor: 41-particle vector for (profile, layer, route, time)
function computeTensor(profile, layer, route, time) {
  const circ = computeCircadian(time, layer);
  const dim8 = compute8D(profile, layer, circ.state, time);

  // 41-particle values
  const values = {};
  for (const p of PARTICLES41) values[p] = 0.0;

  // Graviton pseudo-particle contribution: converts to higgs/em_field mix
  const gravitonAmp = circ.graviton ? 0.4 : 0.0;

  for (const node of circuit84) {
    if (!node.particle12) continue;
    let p = node.particle12;
    if (p === 'graviton') {
      p = circ.graviton ? 'em_field' : 'higgs';
    }
    if (p === 'axion') p = 'em_field'; // axion renamed to em_field in 41-particle system
    if (!PARTICLES41.includes(p)) continue;

    // Node route filter
    if (route === 'Oxford' && node.route !== 'Oxford') continue;
    if (route === 'Out_of_Oxford' && node.route !== 'Out_of_Oxford' && node.route !== 'Oxford') continue;

    // Node primary dim value
    const dim = node.dim || 'g';
    const dimValue = dim8[dim] || 0.5;

    // Base contribution
    let amp = dimValue * routeFactor(route) * stateFactor(circ.state) * (1/84);

    // Graviton q/q_bar boost on D-FF nodes at night
    if (circ.graviton && node.hasQbar) amp *= 1.5;
    // Day quark confinement boost
    if (circ.isDay && (p==='quark' || p==='proton' || p==='up_quark')) amp *= 1.2;

    values[p] += amp;
  }

  // Add graviton leakage to higgs (inertia) and em_field (dark/circadian)
  values.higgs += gravitonAmp * 0.05;
  values.em_field += gravitonAmp * 0.05;

  // 41-particle extended contributions from dim weights
  for (const [p, weights] of Object.entries(PARTICLE_DIM_WEIGHTS_41)) {
    if (PARTICLES12.includes(p)) continue; // already handled by circuit nodes
    let amp = 0;
    for (const [dim, w] of Object.entries(weights)) {
      amp += (dim8[dim] || 0.5) * w;
    }
    amp *= routeFactor(route) * stateFactor(circ.state) * 0.01;
    values[p] += amp;
  }

  // Normalize so vector sums to 1.0
  const sum = Object.values(values).reduce((a,b)=>a+b,0);
  if (sum > 0) for (const p of PARTICLES41) values[p] /= sum;

  // Color resolution for top particles
  const topParticles = PARTICLES41.filter(p => values[p] > 0.02);
  const colors = {};
  for (const p of topParticles) {
    colors[p] = getParticleColor(p, circ.graviton ? 'night' : 'observer');
  }

  // Creative 4-shapes
  const shapes = computeCreative4Shapes(dim8);

  // Route-based 41-particle system
  const isNight = circ.graviton;
  const activeRoute = getActiveRoute(t, isNight);
  const routeVec = computeRouteVector(activeRoute, dim8, t, isNight);
  const toroidalPhase = getToroidalPhase(t);

  // 16-window shift
  const { shifted: dim8Shifted, window: windowInfo } = applyWindowShift(dim8, t);

  // Master equation Ψ
  const observerActive = !isNight || (dim8.s > 0.5);
  const psi = computeMasterPsi(dim8Shifted, t, observerActive);

  // 3AM hysteresis + 4:30PM event
  const hyst3am = compute3amHysteresis(t, observerActive, dim8);
  const ferric430 = compute430pmEvent(t);

  // Geometric node + Darcy leakage
  const geoNode = getGeometricNode(profile.mbti, profile.gender, observerActive);
  const darcy = computeDarcyLeakage(dim8, observerActive);

  return { ...values, state: circ.state, graviton: circ.graviton, mc1rState: circ.mc1rState, dim8, colors, shapes,
           activeRoute, routeVec, toroidalPhase, windowInfo, psi, hyst3am, ferric430, geoNode, darcy };
}

// ---------- Route-based 41-particle system (from nm_body_particle_map_41.md) ----------
// 10 routes × (2 terminal + 1 gradient + 1 leakage) + 1 axion = 41

const ROUTES_41 = {
  music_creation:    { t_pos: 'proton_music',          t_neg: 'photon_music',           grad: 'gluon_music',           leak: 'em_music',
                       dims: { t_pos: ['r','p'], t_neg: ['gamma','s'], grad: ['h','r'], leak: ['gamma','s'] } },
  music_listening:   { t_pos: 'neutrino_listen',       t_neg: 'muon_listen',            grad: 'higgs_listen',          leak: 'acetylcholine_listen',
                       dims: { t_pos: ['r','gamma'], t_neg: ['g','s'], grad: ['p','s'], leak: ['p','s'] } },
  visual_1:          { t_pos: 'up_quark_v1',           t_neg: 'down_quark_v1',          grad: 'w_boson_v1',            leak: 'electron_v1',
                       dims: { t_pos: ['s','r'], t_neg: ['s','h'], grad: ['nu','d'], leak: ['s','gamma'] } },
  visual_2:          { t_pos: 'charm_quark_v2',        t_neg: 'strange_quark_v2',       grad: 'z_boson_v2',            leak: 'photon_v2',
                       dims: { t_pos: ['g','nu'], t_neg: ['d','s'], grad: ['d','g'], leak: ['gamma','s'] } },
  movement_1:        { t_pos: 'proton_move',           t_neg: 'gluon_move',             grad: 'w_boson_move',          leak: 'energy_move',
                       dims: { t_pos: ['r','p'], t_neg: ['h','r'], grad: ['nu','d'], leak: ['r','p'] } },
  movement_2:        { t_pos: 'top_quark_move',        t_neg: 'bottom_quark_move',      grad: 'tau_move',              leak: 'dark_matter_move',
                       dims: { t_pos: ['g','d'], t_neg: ['h','g'], grad: ['d','h'], leak: ['d','nu'] } },
  imagination_1:     { t_pos: 'higgs_imag',            t_neg: 'neutrino_imag',          grad: 'graviton_imag',         leak: 'dopamine_imag',
                       dims: { t_pos: ['p','s'], t_neg: ['r','gamma'], grad: ['g','nu'], leak: ['p','s'] } },
  imagination_2:     { t_pos: 'acetyl_coa_imag',       t_neg: 'electron_imag',          grad: 'axion_imag',            leak: 'endorphin_imag',
                       dims: { t_pos: ['g','d'], t_neg: ['s','gamma'], grad: ['nu','gamma'], leak: ['h','nu'] } },
  sexual:            { t_pos: 'testosterone_sex',      t_neg: 'progesterone_sex',       grad: 'oxytocin_sex',          leak: 'dopamine_sex',
                       dims: { t_pos: ['r','d'], t_neg: ['h','gamma'], grad: ['g','h'], leak: ['s','p'] } },
  weekend_optional:  { t_pos: 'serotonin_wk',          t_neg: 'cortisol_wk',            grad: 'epinephrine_wk',        leak: 'male_gaba_a_wk',
                       dims: { t_pos: ['g','h'], t_neg: ['g','gamma'], grad: ['r','s'], leak: ['g','nu'] } },
};

const AXION_REBRANCH_TABLE = {
  music_creation:   { default: 'music_listening',   night: 'imagination_1' },
  music_listening:  { default: 'visual_1',          night: 'weekend_optional' },
  visual_1:         { default: 'visual_2',          night: 'movement_1' },
  visual_2:         { default: 'music_creation',    night: 'imagination_2' },
  movement_1:       { default: 'movement_2',        night: 'sexual' },
  movement_2:       { default: 'sexual',            night: 'weekend_optional' },
  imagination_1:    { default: 'visual_2',          night: 'music_creation' },
  imagination_2:    { default: 'music_creation',    night: 'sexual' },
  sexual:           { default: 'music_listening',   night: 'movement_2' },
  weekend_optional: { default: 'weekend_optional',  night: 'weekend_optional' },
};

const ROUTE_PARTICLES_41 = [];
for (const r of Object.keys(ROUTES_41)) {
  ROUTE_PARTICLES_41.push(ROUTES_41[r].t_pos, ROUTES_41[r].t_neg, ROUTES_41[r].grad, ROUTES_41[r].leak);
}
ROUTE_PARTICLES_41.push('axion_rebrancher');

function getActiveRoute(hour, isNight) {
  let base;
  if (hour < 3) base = 'music_creation';
  else if (hour < 9) base = 'music_listening';
  else if (hour < 15) base = 'visual_1';
  else if (hour < 21) base = 'movement_2';
  else base = 'imagination_2';
  if (isNight && (hour >= 21 || hour < 3)) {
    const rb = AXION_REBRANCH_TABLE[base];
    return rb ? rb.night : base;
  }
  return base;
}

function computeRouteVector(routeName, dim8, hour, isNight) {
  const route = ROUTES_41[routeName];
  if (!route) return {};
  const vec = {};
  for (const p of ROUTE_PARTICLES_41) vec[p] = 0;
  for (const d of route.dims.t_pos) vec[route.t_pos] += (dim8[d] || 0.5) * 0.4;
  for (const d of route.dims.t_neg) vec[route.t_neg] += (dim8[d] || 0.5) * 0.3;
  for (const d of route.dims.grad)  vec[route.grad]  += (dim8[d] || 0.5) * 0.2;
  for (const d of route.dims.leak)  vec[route.leak]  += (dim8[d] || 0.5) * 0.1;
  if (isNight && (hour >= 21 || hour < 3)) vec.axion_rebrancher = 0.15 * (dim8.nu || 0.5);
  const sum = Object.values(vec).reduce((a,b)=>a+b, 0);
  if (sum > 0) for (const p of ROUTE_PARTICLES_41) vec[p] /= sum;
  return vec;
}

// ---------- 6-sphere toroidal circulation ----------
const SPHERE_CIRCULATION = [
  { phase:1, name:'Sun→Earth',       time:'0-3h',   blood:'AB', energy:'Proton→Photon',           dimTrans:'r→gamma',   slot:'RELEASE' },
  { phase:2, name:'Earth→Moon',      time:'3-9h',   blood:'A',  energy:'Photon→Z-boson',           dimTrans:'gamma→d',   slot:'STRESS_GROWTH' },
  { phase:3, name:'Moon→CoMag',      time:'9-15h',  blood:'O',  energy:'Z-boson→W-boson/Gluon',    dimTrans:'d→h',       slot:'PRESENT_MOMENT' },
  { phase:4, name:'CoMag→Barnard',   time:'15-21h', blood:'B',  energy:'W-boson/Gluon→Quark/Higgs', dimTrans:'h→g+d',    slot:'EXTREME_GROWTH' },
  { phase:5, name:'Barnard→Sun',     time:'21-3h',  blood:'AB', energy:'Quark/Higgs→Proton',       dimTrans:'g+d→r+s',   slot:'3AM_HYSTERESIS' },
];

function getToroidalPhase(hour) {
  for (const p of SPHERE_CIRCULATION) {
    const [s, e] = p.time.split('-');
    const sh = parseInt(s); const eh = parseInt(e);
    if (eh < sh) { if (hour >= sh || hour < eh) return p; }
    else if (sh <= hour && hour < eh) return p;
  }
  return SPHERE_CIRCULATION[0];
}

// ---------- 16-window time phase (4 macro × 4 micro, fractal reverse) ----------
const WINDOW_16 = [];
for (let macro = 0; macro < 4; macro++) {
  for (let micro = 0; micro < 4; micro++) {
    const win = macro * 4 + micro;
    const macroDims = ['r','p','s','d'];
    const microDims = ['nu','gamma','g','h'];
    WINDOW_16.push({
      window: win, startH: win * 1.5, endH: win * 1.5 + 1.5,
      macro, micro, macroDim: macroDims[macro], microDim: microDims[3 - micro],
      label: `W${win}(${win*1.5}-${win*1.5+1.5}h)`,
    });
  }
}

const WINDOW_SPECIAL = { 8: 'noon peak', 9: 'noradrenaline bridge', 10: 'lightning strike 3/32' };

function getWindow(hour) {
  const idx = Math.floor(hour / 1.5) % 16;
  return { ...WINDOW_16[idx], special: WINDOW_SPECIAL[idx] || '' };
}

function applyWindowShift(dim8, hour) {
  const w = getWindow(hour);
  const shifted = { ...dim8 };
  shifted[w.macroDim] = (shifted[w.macroDim] || 0.5) + 0.08;
  shifted[w.microDim] = (shifted[w.microDim] || 0.5) + 0.04;
  if (w.window === 10) shifted.d = (shifted.d || 0.5) + 0.15;
  if (w.window === 8)  shifted.s = (shifted.s || 0.5) + 0.10;
  for (const k of Object.keys(shifted)) shifted[k] = Math.max(0, Math.min(1, shifted[k]));
  return { shifted, window: w };
}

// ---------- Master equation Ψ(t, Obs, V, A, P) ----------
const BETA_0 = 0, BETA_6 = 6, BETA_7 = 7, BETA_12 = 12;
const KAPPA = 1/32, KAPPA_3_32 = 3/32, ONE_64 = 1/64, ONE_256 = 1/256;
const ALPHA_FS = 1/137.036, LAMBDA_6 = 6, X_L = 2, X_R = 14;
const W7 = 9 * Math.PI, H2 = 20;
const PHI = (1 + Math.sqrt(5)) / 2;
const SPARK_ANGLE_RAD = 138.88 * Math.PI / 180;

function computeMasterPsi(dim8, hour, observerActive) {
  const T = (W7 / H2) * (1 / Math.sqrt(2)) * ((BETA_12 + BETA_0) / (BETA_6 + BETA_7));
  const R = 10 * Math.pow(PHI, 3) + ALPHA_FS;
  const deltaKappa = (ONE_64 + ONE_256) / KAPPA;
  const sinTheta = Math.sin(SPARK_ANGLE_RAD);
  const phiB = (BETA_12 / BETA_7) + Math.pow(BETA_6 / BETA_7, 2) - ALPHA_FS / 2;
  const C = Math.sqrt(2) / 5;
  const nightHyst = 3 * C * Math.sqrt(1 - (ONE_64 + ONE_256));
  const obs = observerActive ? 1 : 0;
  const vDotA = Object.values(dim8).reduce((a,b)=>a+b, 0) * 4;
  const recognition = obs * vDotA / 128;
  const dB = (138.88 + 28) / 28;
  const darkGate = KAPPA_3_32 / KAPPA;
  const wavelengthNorm = LAMBDA_6 / (X_R - X_L);
  const psi = T * R * deltaKappa * sinTheta * phiB * nightHyst * recognition * dB * darkGate * wavelengthNorm;
  return { psi, T, R, deltaKappa, sinTheta, phiB, nightHyst, obs, vDotA, recognition, dB, darkGate, wavelengthNorm };
}

// ---------- 3AM HYSTERESIS / Betti 12 + 4:30PM ferric event ----------
function compute3amHysteresis(hour, observerActive, dim8) {
  const is3am = (hour >= 2 && hour <= 4) || hour >= 21;
  const observerBridge = observerActive ? 1 : 0;
  const betti12 = (11 + observerBridge) === 12;
  if (is3am && !observerActive) {
    return { active: true, betti12Complete: betti12, entropyZone: true,
             p: Math.random(), s: 0.5 + Math.random() * 0.5, nu: 0.9 + Math.random() * 0.1,
             label: '3AM_HYSTERESIS_ACTIVE' };
  }
  return { active: is3am, betti12Complete: betti12, entropyZone: false,
           p: dim8.p || 0.5, s: dim8.s || 0.5, nu: dim8.nu || 0.5,
           label: !is3am ? '3AM_HYSTERESIS_INACTIVE' : '3AM_OBSERVER_CLOSED' };
}

function compute430pmEvent(hour) {
  if (hour >= 16 && hour <= 17) {
    return { active: true, event: 'UV_shield_loss',
             cascade: 'magnetite Fe₃O₄ → Fe₂O₃', biological: 'ferroptosis' };
  }
  return { active: false, event: '', cascade: '', biological: '' };
}

// ---------- 6 geometric nodes + Darcy leakage ----------
const GEOMETRIC_NODES = {
  left_bypass:         { x: 2.0,  role: 'extrovert female bypass' },
  right_bypass:        { x: 14.0, role: 'extrovert male bypass' },
  center_funnel:       { x: 8.0,  role: 'introvert funnel / 3/32 spark' },
  separatrix_1:        { x: 5.0,  role: 'left boundary' },
  separatrix_2:        { x: 11.0, role: 'right boundary' },
  observer_singularity:{ x: null, role: 'observer = geomagnetic closure' },
};

const OBSERVER_CLOSURE_TENSION = (9 * Math.PI) / (20 * Math.sqrt(2));

function computeDarcyLeakage(dim8, observerActive) {
  const g = dim8.g || 0.5;
  const kappaEff = observerActive ? KAPPA : KAPPA * (1 + (1 - g) * 0.5);
  let state = 'stable';
  if (kappaEff < ONE_64) state = 'flatlined';
  else if (kappaEff > 1/16) state = 'chaos';
  return { kappa: kappaEff, state, darcyFlux: kappaEff * g, jensenGap: Math.abs(kappaEff - KAPPA) };
}

function getGeometricNode(mbti, gender, isObserver) {
  if (isObserver) return 'observer_singularity';
  const extrovert = mbti[0] === 'E';
  if (extrovert && gender === 'F') return 'left_bypass';
  if (extrovert && gender !== 'F') return 'right_bypass';
  return 'center_funnel';
}

// ---------- Field theory layer: interactions, evolution, conservation ----------

// 41x41 interaction matrix M[i][j]: directed influence of particle j on particle i
// Positive = source j feeds i; negative = j drains i.
const INTERACTION = (() => {
  const M = {};
  for (const a of PARTICLES41) { M[a] = {}; for (const b of PARTICLES41) M[a][b] = 0; }
  // Strong: quarks <-> gluon, proton
  M.up_quark.gluon = 0.8; M.down_quark.gluon = 0.7; M.charm_quark.gluon = 0.6;
  M.strange_quark.gluon = 0.5; M.top_quark.gluon = 0.4; M.bottom_quark.gluon = 0.5;
  M.gluon.up_quark = 0.6; M.gluon.down_quark = 0.5; M.gluon.charm_quark = 0.4;
  M.proton.up_quark = 0.5; M.proton.down_quark = 0.4; M.proton.gluon = 0.4;
  M.neutron.down_quark = 0.4; M.neutron.up_quark = 0.3;
  // EM: photon <-> electron, proton
  M.electron.photon = 0.5; M.photon.electron = 0.3; M.proton.photon = 0.2;
  M.em_field.photon = 0.6; M.photon.em_field = 0.4;
  // Weak: W <-> electron, muon, tau, neutrino; Z <-> neutrino
  M.electron.w_boson = 0.4; M.muon.w_boson = 0.3; M.tau.w_boson = 0.3;
  M.electron_neutrino.w_boson = 0.2; M.muon_neutrino.w_boson = 0.15; M.tau_neutrino.w_boson = 0.15;
  M.w_boson.electron = -0.2; M.w_boson.muon = -0.1; M.w_boson.tau = -0.1;
  M.electron_neutrino.z_boson = 0.3; M.z_boson.electron_neutrino = 0.2;
  M.muon_neutrino.z_boson = 0.2; M.tau_neutrino.z_boson = 0.2;
  // Antineutrino couplings
  M.electron_antineutrino.w_boson = 0.15; M.muon_antineutrino.w_boson = 0.1; M.tau_antineutrino.w_boson = 0.1;
  // Mass/Higgs: higgs feeds W/Z/quarks/leptons
  M.w_boson.higgs = 0.4; M.z_boson.higgs = 0.4; M.electron.higgs = 0.1;
  M.muon.higgs = 0.2; M.tau.higgs = 0.3; M.top_quark.higgs = 0.5; M.bottom_quark.higgs = 0.3;
  M.higgs.higgs = -0.1;
  // EM field / dark mixing: em_field <-> higgs, photon
  M.em_field.higgs = 0.2; M.higgs.em_field = 0.1; M.em_field.photon = 0.1;
  // Graviton <-> ferritin/magnetite (geomag coupling)
  M.graviton.em_field = 0.15; M.em_field.graviton = 0.1;
  M.graviton.higgs = 0.1; M.higgs.graviton = 0.05;
  // Lepton decays: muon, tau -> electron + neutrino
  M.electron.muon = 0.2; M.electron_neutrino.muon = 0.2; M.muon.muon = -0.4;
  M.electron.tau = 0.3; M.tau_neutrino.tau = 0.2; M.tau.tau = -0.5;
  // Neutron -> proton + electron + antineutrino (beta decay)
  M.proton.neutron = 0.3; M.electron.neutron = 0.2; M.electron_antineutrino.neutron = 0.2;
  M.neutron.neutron = -0.3;
  // Neutron star: dense, feeds graviton + dark
  M.graviton.neutron_star = 0.2; M.dark_matter.neutron_star = 0.15; M.neutron_star.neutron_star = -0.1;
  // Dark matter / dark energy: drain normal particles, feed nu/d
  M.dark_matter.electron = -0.05; M.dark_matter.photon = -0.03;
  M.dark_energy.time = 0.2; M.dark_energy.energy = 0.15; M.dark_energy.dark_energy = -0.05;
  // Time / energy scalars
  M.time.graviton = 0.1; M.energy.proton = 0.1; M.energy.electron = 0.05;
  // Hormone vectors
  M.ego_d2.electron = 0.2; M.ego_d2.proton = 0.1;
  M.left_progesterone.photon = 0.15; M.left_progesterone.electron = 0.1;
  M.right_testosterone.proton = 0.2; M.right_testosterone.higgs = 0.1;
  M.acetyl_coa.proton = 0.15; M.acetyl_coa.electron = 0.1;
  // Derived particles
  M.spark.em_field = 0.5; M.em_field.spark = 0.3; M.spark.photon = 0.2;
  M.clathrate_buffer.em_field = 0.2; M.clathrate_buffer.photon = 0.1;
  M.axion_rebrancher.em_field = 0.3; M.em_field.axion_rebrancher = 0.15;
  M.testosterone_sex.right_testosterone = 0.4; M.testosterone_sex.proton = 0.2;
  M.endorphin_imag.electron_antineutrino = 0.2; M.endorphin_imag.photon = 0.15;
  M.male_gaba_a_wk.electron = 0.2; M.male_gaba_a_wk.clathrate_buffer = 0.1;
  M.pain_eliminate.tau_antineutrino = 0.2; M.pain_eliminate.substance_p = 0.15;
  return M;
})();

// Particle "energy" weights (41 particles; higher = more massive/inertial)
const ENERGY = {
  photon: 0, gluon: 0, electron: 0.5, neutrino: 0.1, muon: 105, tau: 1777,
  w_boson: 80379, z_boson: 91188, higgs: 125000, em_field: 0, graviton: 0,
  up_quark: 2.2, down_quark: 4.7, charm_quark: 1275, strange_quark: 95,
  top_quark: 173000, bottom_quark: 4180,
  electron_neutrino: 0.1, electron_antineutrino: 0.1, muon_neutrino: 0.17,
  muon_antineutrino: 0.17, tau_neutrino: 18.2, tau_antineutrino: 18.2,
  neutron: 939, neutron_star: 1e9, dark_matter: 0, dark_energy: 0,
  time: 0, energy: 0, ego_d2: 0.01, left_progesterone: 0.01,
  right_testosterone: 0.01, acetyl_coa: 0.1,
  spark: 0, clathrate_buffer: 0, axion_rebrancher: 0,
  testosterone_sex: 0.01, endorphin_imag: 0.01, male_gaba_a_wk: 0.01, pain_eliminate: 0.01
};

// 6 attractor loops from prose, expressed as 41-particle conservation constraints
const ATTRACTORS = {
  energy: ['proton','gluon','w_boson','up_quark','down_quark','acetyl_coa','energy'],
  information: ['electron_neutrino','photon','z_boson','muon_neutrino','tau_neutrino','time'],
  repair: ['tau','gluon','w_boson','bottom_quark','strange_quark','pain_eliminate'],
  opioid: ['muon','electron','photon','endorphin_imag','electron_antineutrino'],
  gan_bulkhead: ['gluon','higgs','z_boson','top_quark','charm_quark','clathrate_buffer'],
  cox_retrograde: ['electron','electron_neutrino','photon','em_field','graviton','left_progesterone']
};

function attractorImbalance(vec) {
  const im = {};
  for (const [name, parts] of Object.entries(ATTRACTORS)) {
    im[name] = parts.reduce((s,p)=>s+(vec[p]||0),0) - (parts.length/PARTICLES41.length);
  }
  return im;
}

function fieldEnergy(vec) {
  return PARTICLES41.reduce((s,p)=>s+(vec[p]||0)*ENERGY[p],0);
}

// Time derivative dT/dt = interaction + route/state drift + graviton leakage
function dTensor_dt(vec, route, state, graviton) {
  const d = {};
  for (const p of PARTICLES41) d[p] = 0;

  // interaction term: i changes by influence from j weighted by both abundances
  for (const i of PARTICLES41) {
    for (const j of PARTICLES41) {
      d[i] += (INTERACTION[i][j] || 0) * (vec[j] || 0) * (vec[i] || 0);
    }
  }

  // route drift: outer routes increase em_field/neutrino (leakage) and deplete core
  const rf = routeFactor(route);
  d.em_field += (1 - rf) * 0.05 * (vec.higgs || 0);
  d.electron_neutrino += (1 - rf) * 0.03 * (vec.w_boson || 0);
  d.higgs -= (1 - rf) * 0.02 * (vec.higgs || 0);
  d.w_boson -= (1 - rf) * 0.02 * (vec.w_boson || 0);

  // state drift: EXTREME increases nu/em_field; STRESS increases d/g
  if (state === 'STRESS_GROWTH') { d.muon += 0.02; d.tau += 0.01; d.gluon += 0.01; d.dark_matter += 0.01; }
  if (state === 'EXTREME_GROWTH') { d.electron_neutrino += 0.03; d.em_field += 0.02; d.top_quark -= 0.01; d.dark_energy += 0.02; }

  // graviton leakage: night shifts higgs to em_field (q_bar dark state)
  if (graviton) {
    d.em_field += 0.02 * (vec.higgs || 0);
    d.higgs -= 0.02 * (vec.higgs || 0);
    d.graviton += 0.01 * (vec.neutron_star || 0);
  }

  return d;
}

// Evolve the tensor forward by dt using Euler, then renormalize
function evolveTensor(vec, route, state, graviton, dt, steps) {
  let current = { ...vec };
  const E0 = fieldEnergy(current);
  for (let k = 0; k < steps; k++) {
    const d = dTensor_dt(current, route, state, graviton);
    for (const p of PARTICLES41) current[p] = (current[p] || 0) + (d[p] || 0) * dt;
    for (const p of PARTICLES41) current[p] = Math.max(0, current[p]);
    const sum = PARTICLES41.reduce((s,p)=>s+current[p],0);
    if (sum > 0) for (const p of PARTICLES41) current[p] /= sum;
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

// Compute a single-node 41-particle vector at given state/time/route/scale.
function nodeVector({ particle12, dim, route = 'Oxford', scale = '1mm', time = 10.0 }) {
  const circ = computeCircadian(time, 'A');
  let p = particle12;
  if (p === 'graviton') p = circ.graviton ? 'em_field' : 'higgs';
  if (p === 'axion') p = 'em_field';
  if (!PARTICLES41.includes(p) && !PARTICLES12.includes(p)) return null;
  if (!PARTICLES41.includes(p)) p = 'em_field'; // map legacy 12-particle names
  const vec = {};
  for (const pt of PARTICLES41) vec[pt] = 0;
  const dim8 = { r: 0.5, h: 0.5, d: 0.5, p: 0.5, s: 0.5, gamma: 0.5, g: 0.5, nu: 0.5 };
  if (dim && DIMS.includes(dim)) dim8[dim] = 1.0;
  const dVal = dim8[dim] || 0.5;
  vec[p] = dVal * routeFactor(route) * scaleFactor(scale);
  const sum = PARTICLES41.reduce((s, pt) => s + vec[pt], 0);
  if (sum > 0) for (const pt of PARTICLES41) vec[pt] /= sum;
  return vec;
}

function vectorDistance(a, b) {
  return Math.sqrt(PARTICLES41.reduce((s, p) => s + Math.pow((a[p] || 0) - (b[p] || 0), 2), 0));
}

// Map any object to the closest 84-node reference(s) by 41-particle vector similarity.
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
  // Show top 10 particles by value
  const sorted = PARTICLES41.map(p => ({p, v: res[p] || 0})).sort((a,b) => b.v - a.v).slice(0, 10);
  console.log('top particles:', sorted.map(x => `${x.p}=${x.v.toFixed(4)}`).join(' | '));
  // Colors
  console.log('colors:', Object.entries(res.colors).slice(0, 5).map(([p,c]) => `${p}:${c.base}(${c.hex})`).join(' | '));
  // Creative shapes
  console.log(`shapes: dominant=${res.shapes.dominant} weakest=${res.shapes.weakest}`);
  console.log(`  scores: ${JSON.stringify(res.shapes.scores)}`);
  // New systems
  console.log(`active_route: ${res.activeRoute}`);
  const rvActive = Object.entries(res.routeVec).filter(([k,v]) => v > 0.01).map(([k,v]) => `${k}=${v.toFixed(4)}`).join(' | ');
  console.log(`route_vector (active): ${rvActive}`);
  console.log(`toroidal_phase: ${res.toroidalPhase.name} (${res.toroidalPhase.time}) dimTrans=${res.toroidalPhase.dimTrans}`);
  console.log(`window: ${res.windowInfo.label} macro=${res.windowInfo.macroDim} micro=${res.windowInfo.microDim} special=${res.windowInfo.special || 'none'}`);
  console.log(`master_psi: Ψ=${res.psi.psi.toFixed(4)} T=${res.psi.T.toFixed(6)} R=${res.psi.R.toFixed(4)} Φ_B=${res.psi.phiB.toFixed(4)} Λ=${res.psi.nightHyst.toFixed(4)}`);
  console.log(`3am_hysteresis: active=${res.hyst3am.active} betti12=${res.hyst3am.betti12Complete} entropy=${res.hyst3am.entropyZone} label=${res.hyst3am.label}`);
  if (res.ferric430.active) console.log(`430pm_event: ${res.ferric430.event} cascade=${res.ferric430.cascade}`);
  console.log(`geometric_node: ${res.geoNode}`);
  console.log(`darcy: kappa=${res.darcy.kappa.toFixed(6)} state=${res.darcy.state} flux=${res.darcy.darcyFlux.toFixed(6)}`);

  const ev = evolveTensor(res, route, res.state, res.graviton, 0.1, 10);
  console.log(`after dt=1.0: state=${res.state}, energy E0=${ev.E0.toFixed(2)} -> E1=${ev.E1.toFixed(2)}`);
  console.log('attractor imbalance:', JSON.stringify(ev.imbalance));
}

function printMap(target) {
  const m = mapToReference(target, 3);
  if (!m) { console.log(`MAP target: ${JSON.stringify(target)} — no match`); return; }
  console.log(`\nMAP target: ${JSON.stringify(target)}`);
  console.log('target vector (41):', PARTICLES41.filter(p => (m.targetVector[p] || 0) > 0.01).map(p => `${p}=${m.targetVector[p].toFixed(4)}`).join(' | '));
  console.log('top matches:');
  for (const x of m.matches) {
    console.log(`  #${x.num} ${x.name} (${x.particle12}, ${x.dim}, ${x.route}) distance=${x.distance.toFixed(4)}`);
  }
}

console.log('=== TENSOR V5 FIELD (41-particle) ===');
console.log('Particles (41):', PARTICLES41.join(' '));
console.log('Routes:', ROUTES.join(' '));
console.log('States:', STATES.join(' '));
console.log('Scales:', SCALES.join(' '));

printTensor(PROFILES[0], 'A', 'Oxford', 10.0);
printTensor(PROFILES[0], 'A', 'Oxford', 16.5);
printTensor(PROFILES[0], 'D', 'Out_of_England', 2.0);

printMap({ particle12: 'w_boson', dim: 'p', route: 'Oxford', scale: '1mm', coords: makeCoords('body', 0.1, 0.2, 0.3) });
printMap({ particle12: 'neutrino', dim: 'nu', route: 'Out_of_England', scale: '100mm', coords: makeCoords('geo', 37.5, 127.0, 0) });
printMap({ particle12: 'photon', dim: 's', route: 'Out_of_Oxford', scale: '1nm', coords: makeCoords('cosmic', 10.5, -45.2, 1e20) });
