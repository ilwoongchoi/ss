#!/usr/bin/env node
"use strict";
/*
TENSOR EQUATION T[m,b,g,l,t] → 12 PARTICLE FIELD VALUES AT 0.01 RESOLUTION
V_k = impedance(m) × energy_weight(b) × flow(g) × peak_dim(t mod 16) × layer_transform(l) × Obs(t)
*/

// Deterministic PRNG (mulberry32)
function mulberry32(seed) {
  return function() {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

const PEAK_DIMS = ['r','h','d','p','s','gamma','g','nu','r','h','d','p','s','gamma','g','nu'];

function windowIdx(t) { return Math.floor((t % 24.0) / 1.5); }

function peakValue(t) {
  const w = windowIdx(t);
  const phase = ((t % 1.5) / 1.5) * 2 * Math.PI;
  if (w < 8) return 0.5 + 0.5 * (0.5 + 0.5 * Math.cos(phase - Math.PI));
  return 0.5 + 0.5 * (0.5 - 0.5 * Math.cos(phase));
}

const MBTI_8D = {
  0:  ['r',1.0,'s',0.6,'nu',0.3],
  1:  ['h',1.0,'gamma',0.6,'nu',0.3],
  2:  ['d',1.0,'h',0.6,'g',0.3],
  3:  ['p',1.0,'nu',0.6,'h',0.3],
  4:  ['s',1.0,'r',0.6,'nu',0.3],
  5:  ['gamma',1.0,'h',0.6,'p',0.3],
  6:  ['g',1.0,'s',0.6,'r',0.3],
  7:  ['nu',1.0,'p',0.6,'d',0.3],
  8:  ['r',0.8,'h',0.8,'gamma',0.4],
  9:  ['h',1.0,'p',0.6,'nu',0.3],
  10: ['s',1.0,'gamma',0.6,'r',0.3],
  11: ['d',1.0,'g',0.6,'p',0.3],
  12: ['g',1.0,'d',0.6,'p',0.3],
  13: ['h',1.0,'gamma',0.6,'nu',0.3],
  14: ['g',1.0,'gamma',0.6,'h',0.3],
  15: ['d',1.0,'gamma',0.6,'g',0.3],
};

function impedanceVector(m) {
  const vec = {r:0.5,h:0.5,d:0.5,p:0.5,s:0.5,gamma:0.5,g:0.5,nu:0.5};
  const [dom,dv,sec,sv,tert,tv] = MBTI_8D[m];
  vec[dom]=dv; vec[sec]=sv; vec[tert]=tv;
  return vec;
}

const BLOOD_WEIGHT = {0:1.0, 1:0.75, 2:0.60, 3:0.50};

function flow(g) {
  return g===0
    ? {r:0.8,h:0.5,d:1.0,p:0.5,s:0.6,gamma:0.9,g:0.4,nu:0.5}
    : {r:0.6,h:0.9,d:0.4,p:0.5,s:0.7,gamma:0.5,g:1.0,nu:0.6};
}

function layerTransform(l, vec, t, rng) {
  let v = {...vec};
  if (l===1) { v.nu=Math.min(1,v.nu+0.10); v.gamma=Math.max(0,v.gamma-0.05); }
  else if (l===2) { for(let k in v) v[k]=Math.min(1,Math.max(0,v[k]+0.05)); }
  else if (l===3) {
    v.nu=Math.min(1,v.nu+0.10); v.gamma=Math.max(0,v.gamma-0.05);
    for(let k in v) v[k]=Math.min(1,Math.max(0,v[k]+0.05));
    const h=t%24;
    if (h>=21||h<3) { v.p=rng(); v.s=0.5+rng()*0.5; v.nu=0.9+rng()*0.1; }
  }
  return v;
}

function obs(t, isObs) {
  if (isObs) return 1.0;
  const h=t%24;
  if (h>=21||h<6) return 0.0;
  return Math.max(0,Math.min(1, 0.5+0.3*Math.cos((h-10)*Math.PI/12)));
}

function jitter(l, vec, rng) {
  const pct = [0,0.15,0.15,0.30][l];
  if (!pct) return vec;
  let v={...vec};
  v.r=Math.min(1,Math.max(0, v.r*(1+(rng()-0.5)*2*pct)));
  v.d=Math.min(1,Math.max(0, v.d*(1+(rng()-0.5)*2*pct)));
  return v;
}

// Corrected per MBTI node mapping:
// SF=h=gluon, EJ=g=muon, NF=nu=w_boson, EP=gamma=photon,
// IJ=s=quark, IP=r=neutrino, NT=p=higgs, ST=d=tau/z_boson
const PARTICLE_WEIGHTS = {
  proton:   {r:0.7,p:0.3},
  gluon:    {h:0.6,r:0.4},
  muon:     {g:0.7,s:0.3},
  electron: {s:0.5,gamma:0.5},
  quark:    {s:0.6,h:0.4},
  higgs:    {p:0.6,s:0.4},
  w_boson:  {nu:0.6,d:0.4},
  z_boson:  {d:0.7,g:0.3},
  neutrino: {r:0.6,gamma:0.4},
  tau:      {d:0.7,h:0.3},
  photon:   {gamma:0.7,s:0.3},
  em:       {gamma:0.6,s:0.4},
};

const PARTICLES = Object.keys(PARTICLE_WEIGHTS);

function circ(p, t) {
  const h=t%24;
  const cos=Math.cos, PI=Math.PI, max=Math.max;
  const profiles = {
    proton:   () => 0.3+0.7*max(0,cos((h-12)*PI/12)),
    gluon:    () => 0.2+0.4*max(0,cos((h-1.5)*PI/3))+0.4*max(0,cos((h-12)*PI/12)),
    muon:     () => 0.3+0.7*max(0,cos((h-6)*PI/12)),
    electron: () => 0.2+0.5*max(0,cos((h-12)*PI/12))+0.3*max(0,cos((h-5.25)*PI/3)),
    quark:    () => 0.2+0.4*max(0,cos((h-6)*PI/12))+0.4*max(0,cos((h-18)*PI/12)),
    higgs:    () => 0.2+0.8*max(0,cos((h-18)*PI/12)),
    w_boson:  () => 0.2+0.4*max(0,cos((h-12)*PI/12))+0.4*max(0,cos((h-1.5)*PI/3)),
    z_boson:  () => 0.1+0.5*max(0,cos((h-18)*PI/12))+0.4*max(0,cos((h-5.25)*PI/3)),
    neutrino: () => 0.1+0.6*max(0,cos((h-3)*PI/6))+0.3*max(0,cos((h-12)*PI/12)),
    tau:      () => 0.2+0.4*max(0,cos((h-18)*PI/12))+0.4*max(0,cos((h-6)*PI/12)),
    photon:   () => 0.1+0.5*max(0,cos((h-12)*PI/12))+0.4*max(0,cos((h-5.25)*PI/3)),
    em:       () => 0.1+0.5*max(0,cos((h-18)*PI/12))+0.4*max(0,cos((h-5.25)*PI/3)),
  };
  return Math.max(0,Math.min(1, profiles[p]()));
}

function hyst(t) {
  const h=t%24; let m={};
  m.d_boost = (h>=15&&h<=21) ? 1-Math.abs(h-18)/3 : 0;
  m.g_boost = m.d_boost*0.5; m.gamma_boost=m.d_boost*0.3;
  if (h>=16&&h<=17.5) { const u=1-Math.abs(h-16.5)/1; m.photon_drop=u; m.em_drop=u*0.7; m.gravity_rise=u; m.proton_rise=u*0.5; }
  else { m.photon_drop=0;m.em_drop=0;m.gravity_rise=0;m.proton_rise=0; }
  if (h>=2&&h<=4) { const r=1-Math.abs(h-3)/1; m.collapse=r; m.neutrino_boost=r; m.caco3_reverse=r; m.p_random=r; }
  else { m.collapse=0;m.neutrino_boost=0;m.caco3_reverse=0;m.p_random=0; }
  if (h>=4&&h<=6) { const b=1-Math.abs(h-5.25)/1; m.photon_rise=b; m.em_rise=b; m.proton_rise_bl=b*0.6; m.z_boson_rise=b*0.5; }
  else { m.photon_rise=0;m.em_rise=0;m.proton_rise_bl=0;m.z_boson_rise=0; }
  return m;
}

function computeTensor(m,b,g,l,t,isObs=false) {
  const rng = mulberry32(Math.floor(t*100)+l*10000+1);
  let vec = impedanceVector(m);
  const pk = PEAK_DIMS[windowIdx(t)];
  vec[pk] = Math.max(vec[pk], peakValue(t));
  const ew = BLOOD_WEIGHT[b];
  for (let k in vec) vec[k]*=ew;
  const fv = flow(g);
  for (let k in vec) vec[k]*=fv[k];
  vec = layerTransform(l, vec, t, rng);
  vec = jitter(l, vec, rng);
  const ov = obs(t, isObs);
  for (let k in vec) vec[k] *= (ov>0?ov:0.1);
  const hy = hyst(t);
  const results = {};
  for (const p of PARTICLES) {
    const dw = PARTICLE_WEIGHTS[p];
    let base=0; for (let d in dw) base += vec[d]*dw[d];
    const circVal = circ(p, t);
    let value = 0.4*base + 0.6*circVal;
    if (p==='photon') { value -= hy.photon_drop*0.5; value += hy.photon_rise*0.5; }
    else if (p==='em') { value -= hy.em_drop*0.4; value += hy.em_rise*0.4; }
    else if (p==='proton') { value += hy.proton_rise*0.3; value += hy.proton_rise_bl*0.3; }
    else if (p==='neutrino') { value += hy.neutrino_boost*0.5; }
    else if (p==='higgs') { value += hy.d_boost*0.3; }
    else if (p==='tau') { value += hy.d_boost*0.2; }
    else if (p==='z_boson') { value += hy.z_boson_rise*0.3; if (hy.collapse>0) value -= hy.collapse*0.3; }
    if (hy.collapse>0 && p!=='neutrino') value *= (1 - hy.collapse*0.7);
    results[p] = Math.round(Math.max(0,Math.min(1,value))*100)/100;
  }
  return results;
}

// ============================================================
// OUTPUT
// ============================================================
const TARGET_TIMES = [16.50, 3.00, 4.50];
const TIME_LABELS = ['4:30PM', '3:00AM', '4:30AM'];

function fullTable(m,b,g,isObs=false) {
  const ln=['A','B','C','D'];
  console.log(`\n${'='.repeat(140)}`);
  console.log(`COMPLETE TENSOR: T[MBTI=${m}, Blood=${b}, Gender=${g}] → 12 particles × 3 times × 4 layers`);
  console.log(`Times: 4:30 PM (16.50h) | 3:00 AM (03.00h) | 4:30 AM (04.50h)`);
  console.log(`${'='.repeat(140)}`);
  let header = 'Particle    ';
  for (let l=0;l<4;l++) for (let tl of TIME_LABELS) header += ` | L${ln[l]}_${tl}`;
  console.log(header);
  console.log('-'.repeat(140));
  for (const p of PARTICLES) {
    let row = p.padEnd(12);
    for (let l=0;l<4;l++) for (let t of TARGET_TIMES) {
      const v = computeTensor(m,b,g,l,t,isObs)[p];
      row += ` | ${v.toFixed(2).padStart(11)}`;
    }
    console.log(row);
  }
}

// Run for ENTP_M_O (user's likely profile)
fullTable(4, 0, 0, true);

// Also run for all 16 MBTI × 4 blood × 2 gender = 128 profiles at 3 times, Layer A
console.log(`\n${'='.repeat(100)}`);
console.log("ALL 128 PROFILES × 3 TIMES × 12 PARTICLES (Layer A, Observer)");
console.log(`${'='.repeat(100)}`);

const MBTI_NAMES = ['ENFP','ISFP','ESFJ','INTP','ENTP','INFJ','ESTP','ISTP',
                    'ENFJ','INTJ','ESFP','ISTJ','ESTJ','INFP','ISFJ','ENTJ'];
const BLOOD_NAMES = ['O','A','B','AB'];

for (let m=0;m<16;m++) {
  for (let b=0;b<4;b++) {
    for (let g=0;g<2;g++) {
      const profile = `${MBTI_NAMES[m]}_${g===0?'M':'F'}_${BLOOD_NAMES[b]}`;
      let row = `${profile.padEnd(14)}`;
      for (let t of TARGET_TIMES) {
        const vals = computeTensor(m,b,g,0,t,true);
        // Print compact: 12 values separated by spaces
        for (const p of PARTICLES) row += ` ${vals[p].toFixed(2)}`;
        row += ' |';
      }
      console.log(row);
    }
  }
}

// Continuous sweep at 0.01 resolution for ENTP_M_O_LayerA
console.log(`\n${'='.repeat(180)}`);
console.log("CONTINUOUS SWEEP: ENTP_M_O_LayerA, all 12 particles, 0.15h steps (0.01h resolution available)");
console.log(`${'='.repeat(180)}`);
let h2 = 'Time     ';
for (const p of PARTICLES) h2 += ` | ${p.padStart(8)}`;
console.log(h2);
console.log('-'.repeat(180));
for (let ti=0; ti<=2400; ti+=15) {
  const t = ti/100.0;
  const vals = computeTensor(4,0,0,0,t,true);
  let row = `${t.toFixed(2).padStart(8)}`;
  for (const p of PARTICLES) row += ` | ${vals[p].toFixed(2).padStart(8)}`;
  console.log(row);
}
