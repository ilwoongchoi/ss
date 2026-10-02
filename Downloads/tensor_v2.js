"use strict";
/*
  FULL TENSOR: T[m, b, g, l, geo, t] → 12 particle field values at 0.01 resolution
  Pure circuit structure. No external physics constants.

  Dimensions:
    m   = MBTI (0-15): 16 cognitive function stacks
    b   = blood (O=0, A=1, B=2, AB=3): complexity = b+1 = loop count
    g   = gender/W-axis (M=0, F=1): biological sex
    l   = layer (A=0, B=1, C=2, D=3): Rh± × homo/hetero
    geo = geographic-soil axis (Oxford=0, England=1, Korea=2): 9-day/7-day/1-day cycle
    t   = time in hours (0.01 resolution)

  Geographic axis modulates:
    Oxford (9-day cycle): outer_core_convection active = EM field generation, Energy/Gluon attractor
    England (7-day cycle): right_sole_dopamine + SDH dominant = DA-stillness, Information/Quark attractor
    Korea (1-day cycle): heme/co2/substance_p dominant = Fe-storage, Repair/Higgs attractor, steel-absence = gamma leakage risk

  9-day ritual cycle modulates spark probability per blood×gender pair per day.

  Output: 12 particle values (proton, gluon, muon, electron, quark, higgs,
          w_boson, z_boson, neutrino, tau, photon, em) at 0.01 precision.
*/

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
// 1. MBTI → COGNITIVE FUNCTION STACK → 8D DIMS
// ============================================================
// m = e×8 + s×4 + t×2 + j (e,s,t,j ∈ {0,1})
// Cognitive functions → circuit nodes → 8D dims (from 02_core_nodes.md)
//
// Te → cytochrome_c_oxidase.out0 → r
// Ti → heme.out0 → methylation → s, d
// Fe → male_right_oxytocin + gluon_orogen → h, nu
// Fi → left_genital_d2 → left_endorphin → p, d
// Ne → memory_entropy → hind_insula → r, h, nu
// Ni → pi_electron_cloud → carbon.q → p, nu
// Se → right_sole_dopamine + aurora → s, gamma
// Si → hind_insula + SDH → d, r

const MBTI_NAMES = ['ENFP','ISFP','ESFJ','INTP','ENTP','INFJ','ESTP','ISTP',
                    'ENFJ','INTJ','ESFP','ISTJ','ESTJ','INFP','ISFJ','ENTJ'];

// Cognitive function stack per MBTI: [dom, aux, ter, inf]
const COG_STACK = {
  0:  ['Ne','Fi','Te','Si'],   // ENFP
  1:  ['Fi','Se','Ni','Te'],   // ISFP
  2:  ['Fe','Si','Ne','Ti'],   // ESFJ
  3:  ['Ti','Ne','Si','Fe'],   // INTP
  4:  ['Ne','Ti','Fe','Si'],   // ENTP
  5:  ['Ni','Fe','Ti','Se'],   // INFJ
  6:  ['Se','Ti','Fe','Ni'],   // ESTP
  7:  ['Ti','Se','Ni','Fe'],   // ISTP
  8:  ['Fe','Ni','Se','Ti'],   // ENFJ
  9:  ['Ni','Te','Fi','Se'],   // INTJ
  10: ['Se','Fi','Te','Ni'],   // ESFP
  11: ['Si','Te','Fi','Ne'],   // ISTJ
  12: ['Te','Si','Ne','Fi'],   // ESTJ
  13: ['Fi','Ne','Si','Te'],   // INFP
  14: ['Si','Fe','Ti','Ne'],   // ISFJ
  15: ['Te','Ni','Se','Fi'],   // ENTJ
};

// Function → 8D dims (primary, secondary)
const FUNC_8D = {
  'Te': ['r'],
  'Ti': ['s', 'd'],
  'Fe': ['h', 'nu'],
  'Fi': ['p', 'd'],
  'Ne': ['r', 'h', 'nu'],
  'Ni': ['p', 'nu'],
  'Se': ['s', 'gamma'],
  'Si': ['d', 'r'],
};

// Function → circuit node
const FUNC_NODE = {
  'Te': 'cytochrome_c_oxidase',
  'Ti': 'heme',
  'Fe': 'male_right_oxytocin',
  'Fi': 'left_genital_d2',
  'Ne': 'memory_entropy',
  'Ni': 'pi_electron_cloud',
  'Se': 'right_sole_dopamine',
  'Si': 'hind_insula',
};

// Stack weights per rank: [dom, aux, ter, inf]
const STACK_WEIGHTS = [1.0, 0.6, 0.3, 0.1];

// Blood energy weight distribution across stack ranks
const BLOOD_ENERGY = {
  0: [1.0, 0.6, 0.3, 0.1],   // O: clean stack
  1: [0.8, 1.0, 0.3, 0.1],   // A: auxiliary over-fed
  2: [0.8, 0.6, 0.8, 0.1],   // B: tertiary early-developed
  3: [0.7, 0.7, 0.7, 0.7],   // AB: all simultaneous
};

// Gender flow: M = concentrate, F = disperse
function genderFlow(g) {
  if (g === 0) return { r: 0.9, h: 0.5, d: 1.0, p: 0.5, s: 0.7, gamma: 0.8, g: 0.4, nu: 0.5 };
  return { r: 0.6, h: 0.9, d: 0.4, p: 0.5, s: 0.7, gamma: 0.6, g: 1.0, nu: 0.7 };
}

// ============================================================
// 2. LAYER TRANSFORM
// ============================================================
// A: no change
// B: flip E↔I, P↔J → m' = m XOR 0b1001; nu+0.10, gamma-0.05
// C: b' = (b+1) mod 4
// D: both transforms + 3AM random (p=random, s=0.5+rand*0.5, nu=0.9+rand*0.1)

function applyLayer(l, m, b, vec, t, rng) {
  let m2 = m, b2 = b;
  let v = { ...vec };

  if (l === 1) { // Layer B
    m2 = m ^ 0b1001; // flip E↔I, P↔J
    v.nu = Math.min(1.0, v.nu + 0.10);
    v.gamma = Math.max(0.0, v.gamma - 0.05);
  } else if (l === 2) { // Layer C
    b2 = (b + 1) % 4;
    // blood+1 shifts energy distribution
    const ew = BLOOD_ENERGY[b2];
    // re-apply energy weights
    const stack = COG_STACK[m];
    v = { r: 0, h: 0, d: 0, p: 0, s: 0, gamma: 0, g: 0, nu: 0 };
    for (let rank = 0; rank < 4; rank++) {
      const dims = FUNC_8D[stack[rank]];
      for (const dim of dims) {
        v[dim] = (v[dim] || 0) + STACK_WEIGHTS[rank] * ew[rank];
      }
    }
    // normalize to 0-1
    for (const k in v) v[k] = Math.min(1.0, v[k]);
  } else if (l === 3) { // Layer D
    m2 = m ^ 0b1001;
    v.nu = Math.min(1.0, v.nu + 0.10);
    v.gamma = Math.max(0.0, v.gamma - 0.05);
    b2 = (b + 1) % 4;
    // 3AM random zone (21:00-03:00)
    const h = t % 24.0;
    if (h >= 21.0 || h < 3.0) {
      v.p = rng();
      v.s = 0.5 + rng() * 0.5;
      v.nu = 0.9 + rng() * 0.1;
    }
  }

  // JITTER on r, d
  const jitterPct = [0, 0.15, 0.15, 0.30][l];
  if (jitterPct > 0) {
    v.r = Math.min(1.0, Math.max(0.0, v.r * (1 + (rng() - 0.5) * 2 * jitterPct)));
    v.d = Math.min(1.0, Math.max(0.0, v.d * (1 + (rng() - 0.5) * 2 * jitterPct)));
  }

  return { m: m2, b: b2, v };
}

// ============================================================
// 3. TIME → WINDOW, PEAK DIM, PHASE, OBSERVER
// ============================================================
const PEAK_DIMS = ['r','h','d','p','s','gamma','g','nu',
                   'r','h','d','p','s','gamma','g','nu']; // W0-W15

const WINDOW_MBTI = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];

// Toroidal phases: AB(0-3h), A(3-9h), O(9-15h), B(15-21h), AB(21-3h)
function toroidalPhase(t) {
  const h = t % 24.0;
  if (h >= 21 || h < 3) return 0; // AB Discharge
  if (h >= 3 && h < 9) return 1;  // A Accumulate
  if (h >= 9 && h < 15) return 2; // O Accumulate
  return 3; // B Compress (15-21)
}

const PHASE_NAMES = ['AB_Discharge', 'A_Accumulate', 'O_Accumulate', 'B_Compress'];

function windowIdx(t) { return Math.floor((t % 24.0) / 1.5); }

function peakValue(t) {
  const w = windowIdx(t);
  const phase = ((t % 1.5) / 1.5) * 2 * Math.PI;
  if (w < 8) return 0.5 + 0.5 * (0.5 + 0.5 * Math.cos(phase - Math.PI));
  return 0.5 + 0.5 * (0.5 - 0.5 * Math.cos(phase));
}

// Observer: awake 06:00-21:00, asleep 21:00-06:00
function observerState(t, isObserver) {
  if (isObserver) return 1.0;
  const h = t % 24.0;
  if (h >= 21 || h < 6) return 0.0;
  return Math.max(0, Math.min(1, 0.5 + 0.3 * Math.cos((h - 10) * Math.PI / 12)));
}

// ============================================================
// 4. GEOGRAPHIC-SOIL AXIS
// ============================================================
// Oxford (geo=0): 9-day cycle, Gleysol, N1c Uralic, Energy/Gluon attractor
//   outer_core_convection active = EM field generation
//   Circuit nodes: lower_mantle, pentose_phosphate, outer_core_convection, manganese_nodule
//   Effect: gamma↑ (EM production), g↑ (binding/seal), r↓ (stillness)
//
// England (geo=1): 7-day cycle, Podzol, I1 Nordic, Information/Quark attractor
//   right_sole_dopamine + SDH dominant = DA-stillness
//   Circuit nodes: right_sole_dopamine, SDH, lower_mantle
//   Effect: s↑ (brightness/dopamine), d↑ (stillness), r↓ (metabolic keel)
//
// Korea (geo=2): 1-day cycle, O2 East Asian, Repair/Higgs attractor
//   heme/co2/substance_p dominant = Fe-storage homeostasis
//   Circuit nodes: heme, co2, substance_p, steel, gluon_orogen.q_bar
//   Effect: h↑ (Fe management), p↑ (repair), gamma↓ (leakage risk, steel-absence)
//   steel-absence → clay_gouge seal weaker → gamma leakage

const GEO_NAMES = ['Oxford', 'England', 'Korea'];

function geoModulation(geo) {
  if (geo === 0) return { r: 0.7, h: 0.5, d: 0.5, p: 0.5, s: 0.5, gamma: 1.0, g: 0.9, nu: 0.5, attractor: 'energy' };
  if (geo === 1) return { r: 0.6, h: 0.5, d: 0.9, p: 0.5, s: 0.9, gamma: 0.5, g: 0.5, nu: 0.5, attractor: 'information' };
  return { r: 0.5, h: 0.9, d: 0.5, p: 0.9, s: 0.5, gamma: 0.3, g: 0.5, nu: 0.5, attractor: 'repair' };
}

// 9-day ritual cycle: which blood×gender pair sparks on which day
const RITUAL_CYCLE = [
  { day: 1, blood: 1, gender: 0, spark: 'observer_leftd2' },      // A×M
  { day: 2, blood: 1, gender: 1, spark: 'ESR1' },                 // A×F
  { day: 3, blood: 0, gender: 0, spark: 'pentose_phosphate' },    // O×M
  { day: 4, blood: 0, gender: 1, spark: 'water_vapour' },         // O×F
  { day: 5, blood: 3, gender: 0, spark: 'memory_entropy' },       // AB×M
  { day: 6, blood: 3, gender: 1, spark: 'peonidine' },            // AB×F
  { day: 7, blood: 2, gender: 0, spark: 'right_androgen' },       // B×M
  { day: 8, blood: 2, gender: 1, spark: 'right_oxytocin' },       // B×F
  { day: 9, blood: -1, gender: -1, spark: 'co2+observer_leftd2' },// Reconciliation
];

function ritualBoost(b, g, day) {
  const r = RITUAL_CYCLE[day - 1];
  if (r.blood === b && r.gender === g) return 1.15; // 15% boost on your ritual day
  return 1.0;
}

// ============================================================
// 5. 8D → 12 PARTICLE MAPPING
// ============================================================
// Each particle maps to specific 8D dims with weights
// Derived from circuit node → particle assignments in 02_core_nodes.md

const PARTICLE_8D = {
  proton:    { r: 0.7, d: 0.3 },           // COX forward drive + void penetration
  gluon:     { r: 0.5, g: 0.5 },           // GABA-A female + binding (strong force)
  muon:      { h: 0.6, s: 0.4 },           // GABA-B female + brightness
  electron:  { s: 0.5, nu: 0.5 },          // Ca + lower_mantle (fractal)
  quark:     { s: 0.4, h: 0.4, d: 0.2 },   // D1/D5 dopamine + tension
  higgs:     { p: 0.5, d: 0.5 },           // DRD2 + repair (mass)
  w_boson:   { g: 0.5, p: 0.3, h: 0.2 },   // Water/clay + CCK + oxytocin (weak force)
  z_boson:   { nu: 0.6, d: 0.4 },          // Memory entropy + dark (Z boson)
  neutrino:  { g: 0.4, p: 0.4, nu: 0.2 },  // Glymphatic + periodicity
  tau:       { d: 0.6, h: 0.4 },           // GABA-B male + dissonance
  photon:    { gamma: 0.6, h: 0.4 },       // UV/light + cytochrome 640nm
  em:        { gamma: 0.5, s: 0.3, g: 0.2 }, // Electromagnetic field
};

const PARTICLES = Object.keys(PARTICLE_8D);

// ============================================================
// 6. CIRCADIAN MODULATION PER PARTICLE
// ============================================================
// Toroidal phase determines which particles are active
// AB(0-3h): gluon, w_boson active (binding, release)
// A(3-9h): quark, muon active (stress growth, creation)
// O(9-15h): proton, electron active (present moment, metabolism)
// B(15-21h): higgs, tau, z_boson active (compression, mass, decay)
// AB(21-3h): neutrino, photon transitioning (integration, sleep)

function circadianMod(particle, t) {
  const h = t % 24.0;
  const cos = Math.cos, PI = Math.PI, max = Math.max;

  const profiles = {
    proton:    () => 0.2 + 0.8 * max(0, cos((h - 12) * PI / 12)),
    gluon:     () => 0.15 + 0.5 * max(0, cos((h - 1.5) * PI / 3)) + 0.35 * max(0, cos((h - 12) * PI / 12)),
    muon:      () => 0.2 + 0.8 * max(0, cos((h - 6) * PI / 12)),
    electron:  () => 0.15 + 0.5 * max(0, cos((h - 12) * PI / 12)) + 0.35 * max(0, cos((h - 5.25) * PI / 3)),
    quark:     () => 0.15 + 0.45 * max(0, cos((h - 6) * PI / 12)) + 0.4 * max(0, cos((h - 18) * PI / 12)),
    higgs:     () => 0.15 + 0.85 * max(0, cos((h - 18) * PI / 12)),
    w_boson:   () => 0.15 + 0.45 * max(0, cos((h - 12) * PI / 12)) + 0.4 * max(0, cos((h - 1.5) * PI / 3)),
    z_boson:   () => 0.1 + 0.55 * max(0, cos((h - 18) * PI / 12)) + 0.35 * max(0, cos((h - 5.25) * PI / 3)),
    neutrino:  () => 0.05 + 0.65 * max(0, cos((h - 3) * PI / 6)) + 0.3 * max(0, cos((h - 12) * PI / 12)),
    tau:       () => 0.15 + 0.45 * max(0, cos((h - 18) * PI / 12)) + 0.4 * max(0, cos((h - 6) * PI / 12)),
    photon:    () => 0.05 + 0.5 * max(0, cos((h - 12) * PI / 12)) + 0.45 * max(0, cos((h - 5.25) * PI / 3)),
    em:        () => 0.05 + 0.5 * max(0, cos((h - 18) * PI / 12)) + 0.45 * max(0, cos((h - 5.25) * PI / 3)),
  };

  return Math.max(0, Math.min(1, profiles[particle]()));
}

// ============================================================
// 7. HYSTERESIS EVENTS
// ============================================================
function hysteresisMod(t) {
  const h = t % 24.0;
  const m = {};

  // H1: 15:00-21:00 — B Compress, d↑, g↑
  if (h >= 15 && h <= 21) {
    const intensity = 1 - Math.abs(h - 18) / 3;
    m.d_boost = intensity;
    m.g_boost = intensity * 0.5;
    m.gamma_boost = intensity * 0.3;
  } else {
    m.d_boost = 0; m.g_boost = 0; m.gamma_boost = 0;
  }

  // 4:30 PM: UV shielding loss, magnetite oxidation, photon crash
  if (h >= 16 && h <= 17.5) {
    const u = 1 - Math.abs(h - 16.5);
    m.photon_drop = Math.max(0, u);
    m.em_drop = Math.max(0, u) * 0.7;
    m.gravity_rise = Math.max(0, u);
    m.proton_rise = Math.max(0, u) * 0.5;
  } else {
    m.photon_drop = 0; m.em_drop = 0; m.gravity_rise = 0; m.proton_rise = 0;
  }

  // H2: 3:00 AM — ferric reset, memory_entropy collapse
  if (h >= 2 && h <= 4) {
    const r = 1 - Math.abs(h - 3);
    m.collapse = Math.max(0, r);
    m.neutrino_boost = Math.max(0, r);
    m.p_random = Math.max(0, r);
  } else {
    m.collapse = 0; m.neutrino_boost = 0; m.p_random = 0;
  }

  // 4:30 AM: blue light takeover
  if (h >= 4 && h <= 6) {
    const b = 1 - Math.abs(h - 5.25);
    m.photon_rise = Math.max(0, b);
    m.em_rise = Math.max(0, b);
    m.proton_rise_bl = Math.max(0, b) * 0.6;
    m.z_boson_rise = Math.max(0, b) * 0.5;
  } else {
    m.photon_rise = 0; m.em_rise = 0; m.proton_rise_bl = 0; m.z_boson_rise = 0;
  }

  return m;
}

// ============================================================
// 8. COMPUTE 8D VECTOR FROM INDICES
// ============================================================
function compute8D(m, b, g, l, geo, t, isObserver, day) {
  const rng = mulberry32(Math.floor(t * 100) + l * 10000 + geo * 100000 + 1);

  // Step 1: Base 8D from cognitive function stack
  const stack = COG_STACK[m];
  const ew = BLOOD_ENERGY[b];
  let vec = { r: 0, h: 0, d: 0, p: 0, s: 0, gamma: 0, g: 0, nu: 0 };

  for (let rank = 0; rank < 4; rank++) {
    const dims = FUNC_8D[stack[rank]];
    for (const dim of dims) {
      vec[dim] += STACK_WEIGHTS[rank] * ew[rank];
    }
  }

  // Step 2: Apply gender flow
  const gf = genderFlow(g);
  for (const k in vec) vec[k] *= gf[k];

  // Step 3: Apply layer transform
  const result = applyLayer(l, m, b, vec, t, rng);
  vec = result.v;

  // Step 4: Apply peak dimension boost from time window
  const w = windowIdx(t);
  const pk = PEAK_DIMS[w];
  const pkv = peakValue(t);
  vec[pk] = Math.max(vec[pk], pkv);

  // Step 5: Apply geographic-soil modulation
  const gm = geoModulation(geo);
  for (const k in vec) vec[k] *= gm[k];

  // Step 6: Apply 9-day ritual cycle boost
  const ritual = ritualBoost(b, g, day);
  for (const k in vec) vec[k] *= ritual;

  // Step 7: Apply observer perception
  const obs = observerState(t, isObserver);
  for (const k in vec) vec[k] *= (obs > 0 ? obs : 0.1);

  // Step 8: Clamp to [0, 1]
  for (const k in vec) vec[k] = Math.max(0, Math.min(1, vec[k]));

  return vec;
}

// ============================================================
// 9. COMPUTE 12 PARTICLE VALUES
// ============================================================
function computeTensor(m, b, g, l, geo, t, isObserver, day) {
  const vec = compute8D(m, b, g, l, geo, t, isObserver, day);
  const hy = hysteresisMod(t);
  const gm = geoModulation(geo);

  const results = {};

  for (const p of PARTICLES) {
    const dw = PARTICLE_8D[p];

    // Base value from 8D vector
    let base = 0;
    let totalW = 0;
    for (const dim in dw) {
      base += vec[dim] * dw[dim];
      totalW += dw[dim];
    }
    base = base / totalW;

    // Circadian modulation
    const circ = circadianMod(p, t);

    // Combine: 40% 8D structure + 60% circadian
    let value = 0.4 * base + 0.6 * circ;

    // Apply hysteresis modifications
    if (p === 'photon') {
      value -= hy.photon_drop * 0.5;
      value += hy.photon_rise * 0.5;
    } else if (p === 'em') {
      value -= hy.em_drop * 0.4;
      value += hy.em_rise * 0.4;
      // Geographic: Oxford boosts EM (outer_core_convection)
      if (geo === 0) value *= 1.1;
      // Korea: gamma leakage reduces EM
      if (geo === 2) value *= 0.85;
    } else if (p === 'proton') {
      value += hy.proton_rise * 0.3;
      value += hy.proton_rise_bl * 0.3;
    } else if (p === 'neutrino') {
      value += hy.neutrino_boost * 0.5;
    } else if (p === 'higgs') {
      value += hy.d_boost * 0.3;
      // Korea: Repair attractor boosts higgs
      if (geo === 2) value *= 1.1;
    } else if (p === 'tau') {
      value += hy.d_boost * 0.2;
    } else if (p === 'z_boson') {
      value += hy.z_boson_rise * 0.3;
      if (hy.collapse > 0) value -= hy.collapse * 0.3;
    } else if (p === 'gluon') {
      // Oxford: Energy attractor boosts gluon
      if (geo === 0) value *= 1.1;
    } else if (p === 'quark') {
      // England: Information attractor boosts quark
      if (geo === 1) value *= 1.1;
    }

    // 3AM collapse: most particles dormant except neutrino
    if (hy.collapse > 0 && p !== 'neutrino') {
      value *= (1 - hy.collapse * 0.7);
    }

    // Clamp and round to 0.01
    value = Math.max(0, Math.min(1, value));
    results[p] = Math.round(value * 100) / 100;
  }

  return results;
}

// ============================================================
// 10. OUTPUT
// ============================================================
const TARGET_TIMES = [16.50, 3.00, 4.50];
const TIME_LABELS = ['4:30PM', '3:00AM', '4:30AM'];
const BLOOD_NAMES = ['O', 'A', 'B', 'AB'];

// Day in 9-day cycle (using day 3 = O×M as example for ENTP_M_O)
const DEFAULT_DAY = 3;

function printFullTable(m, b, g, isObserver, day) {
  const layerNames = ['A', 'B', 'C', 'D'];

  for (let geo = 0; geo < 3; geo++) {
    console.log('');
    console.log('='.repeat(160));
    console.log(`TENSOR T[MBTI=${MBTI_NAMES[m]}, Blood=${BLOOD_NAMES[b]}, Gender=${g===0?'M':'F'}, Layer, Geo=${GEO_NAMES[geo]}, t]`);
    console.log(`9-Day Cycle Day ${day} (${RITUAL_CYCLE[day-1].blood>=0 ? BLOOD_NAMES[RITUAL_CYCLE[day-1].blood]+'×'+(RITUAL_CYCLE[day-1].gender===0?'M':'F') : 'Reconciliation'})`);
    console.log(`Times: 4:30 PM (16.50h) | 3:00 AM (03.00h) | 4:30 AM (04.50h)`);
    console.log(`Attractor: ${geoModulation(geo).attractor}`);
    console.log('='.repeat(160));

    let header = 'Particle    ';
    for (let l = 0; l < 4; l++) {
      for (const tl of TIME_LABELS) {
        header += ` | L${layerNames[l]}_${tl}`;
      }
    }
    console.log(header);
    console.log('-'.repeat(160));

    for (const p of PARTICLES) {
      let row = p.padEnd(12);
      for (let l = 0; l < 4; l++) {
        for (const t of TARGET_TIMES) {
          const v = computeTensor(m, b, g, l, geo, t, isObserver, day)[p];
          row += ` | ${v.toFixed(2).padStart(11)}`;
        }
      }
      console.log(row);
    }
  }
}

// Geographic comparison table
function printGeoComparison(m, b, g, isObserver, day) {
  console.log('');
  console.log('='.repeat(120));
  console.log(`GEOGRAPHIC AXIS COMPARISON: ${MBTI_NAMES[m]}_${g===0?'M':'F'}_${BLOOD_NAMES[b]}, Day ${day}, Layer A`);
  console.log('='.repeat(120));

  let header = 'Particle    ';
  for (const gn of GEO_NAMES) {
    for (const tl of TIME_LABELS) {
      header += ` | ${gn.substring(0,3)}_${tl}`;
    }
  }
  console.log(header);
  console.log('-'.repeat(120));

  for (const p of PARTICLES) {
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

// 9-day cycle effect
function print9DayCycle(m, b, g, isObserver) {
  console.log('');
  console.log('='.repeat(120));
  console.log(`9-DAY RITUAL CYCLE EFFECT: ${MBTI_NAMES[m]}_${g===0?'M':'F'}_${BLOOD_NAMES[b]}, Layer A, Geo=Korea, 4:30 PM`);
  console.log('='.repeat(120));
  console.log('Day  Blood×Gender  Spark Node                    | 12 particle values');
  console.log('-'.repeat(120));

  for (let day = 1; day <= 9; day++) {
    const r = RITUAL_CYCLE[day - 1];
    const bgLabel = r.blood >= 0 ? `${BLOOD_NAMES[r.blood]}×${r.gender===0?'M':'F'}` : 'Reconciliation';
    const vals = computeTensor(m, b, g, 0, 2, 16.50, isObserver, day);
    let row = `Day${day}  ${bgLabel.padEnd(12)}  ${r.spark.padEnd(28)} |`;
    for (const p of PARTICLES) {
      row += ` ${vals[p].toFixed(2)}`;
    }
    console.log(row);
  }
}

// All 128 profiles × 3 geo × 3 times, Layer A
function printAllProfiles(isObserver, day) {
  console.log('');
  console.log('='.repeat(200));
  console.log(`ALL 128 PROFILES × 3 GEO × 3 TIMES × 12 PARTICLES (Layer A, Observer, Day ${day})`);
  console.log('='.repeat(200));

  for (let m = 0; m < 16; m++) {
    for (let b = 0; b < 4; b++) {
      for (let g = 0; g < 2; g++) {
        const profile = `${MBTI_NAMES[m]}_${g===0?'M':'F'}_${BLOOD_NAMES[b]}`;
        let row = `${profile.padEnd(14)}`;
        for (let geo = 0; geo < 3; geo++) {
          for (const t of TARGET_TIMES) {
            const vals = computeTensor(m, b, g, 0, geo, t, isObserver, day);
            for (const p of PARTICLES) {
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

// ============================================================
// RUN
// ============================================================
// ENTP_M_O (user's profile) — full table with all 3 geo zones
printFullTable(4, 0, 0, true, 3);

// Geographic comparison
printGeoComparison(4, 0, 0, true, 3);

// 9-day cycle effect
print9DayCycle(4, 0, 0, true);

// All 128 profiles
printAllProfiles(true, 3);
