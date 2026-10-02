"use strict";
/*
  TENSOR V4 — COMPLETE: 329 nodes, all 47 missing nodes wired by scientific reasoning
  T[m, b, g, l, geo, t] → 12 particle field values at 0.01 resolution

  Each missing node wired by:
  1. Biological structure at that body location
  2. Particle assignment from physics isomorphism
  3. Circuit connection to existing nodes via functional pathway
  4. Mirror cross-connection (left/right symmetry)
  5. Observer bus (observer_leftd2 as master permissive)
  6. Gate type from biological function (tristate for organs, AND for convergence, MUX for sensory)
*/

const fs = require('fs');

// ============================================================
// PRNG
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
// 1. LOAD EXISTING 282 NODES
// ============================================================
const existingNodes = JSON.parse(fs.readFileSync('existing_nodes.json', 'utf8'));

// ============================================================
// 2. 47 NEW NODES — FULL DEFINITION WITH WIRING
// ============================================================
// Each node: name, gate, particle, element, dim, location, side, inputs[], outputs[]
// Inputs reference existing circuit nodes by functional pathway
// Outputs connect to downstream nodes in same 8D dim or mirror pair

const newNodes = [
  // --- CENTER ORGANS ---
  { name:'bladder', gate:'tristate', particle:'neutrino', element:'Te(52)', dim:'r',
    location:'urinary bladder (pelvic floor)', side:'center',
    inputs:['water.out0','observer_leftd2.out0'],
    outputs:['water_vapour.in0'],
    bio:'ADH/vasopressin-regulated urinary storage. Fluid balance endpoint. Connects to water (fluid regulation) and observer bus.' },

  { name:'diaphragm', gate:'tristate', particle:'photon', element:'I(53)', dim:'r',
    location:'diaphragm (thoracoabdominal boundary)', side:'center',
    inputs:['cytochrome_c_oxidase.out0','co2.out0'],
    outputs:['heme.in0'],
    bio:'Primary respiratory muscle. Drives O2/CO2 exchange. Connects to COX (O2 consumption) and co2 (CO2 regulation). Output feeds heme (oxygenation).' },

  { name:'nose_center', gate:'MUX', particle:'graviton', element:'Ca(20)', dim:'d',
    location:'nasal bridge / septum / vomeronasal organ', side:'center',
    inputs:['carbon.q','pi_electron_cloud.q_bar'],
    outputs:['memory_entropy.in_main'],
    bio:'Olfactory midline structure. Vomeronasal organ for pheromone detection. Connects to carbon (structural) and pi_electron_cloud (electron routing). Output feeds memory_entropy (novelty detection).' },

  { name:'prostate', gate:'tristate', particle:'z_boson', element:'Xe(54)', dim:'r',
    location:'prostate gland (pelvic floor)', side:'center',
    inputs:['left_genital_d2.out0','craton.out1'],
    outputs:['water.in1'],
    bio:'Prostatic smooth muscle and fluid production. D2 brake controls emission. Connects to left_genital_d2 (reward brake) and craton (structural stress). Output feeds water (fluid regulation).' },

  { name:'spleen', gate:'tristate', particle:'strange_quark', element:'Cs(55)', dim:'r',
    location:'spleen (left upper quadrant)', side:'center',
    inputs:['heme.out1','ferritin.in0'],
    outputs:['heme.in1'],
    bio:'RBC recycling and immune filtration. Red pulp recycles heme iron. Connects to heme (RBC breakdown) and ferritin (iron storage). Output feeds back to heme (iron recirculation).' },

  { name:'uterus', gate:'tristate', particle:'higgs', element:'Ba(56)', dim:'r',
    location:'uterus (pelvic cavity)', side:'center',
    inputs:['heme.out0','observer_leftd2.out0'],
    outputs:['ferritin.in1'],
    bio:'Endometrial cycling, myometrial growth. Estrogen-driven mass accumulation. Connects to heme (blood supply) and observer bus. Output feeds ferritin (iron storage for cycle).' },

  // --- LEFT SIDE ---
  { name:'left_ankle', gate:'AND', particle:'z_boson', element:'Br(35)', dim:'r',
    location:'left ankle (talocrural joint)', side:'left',
    inputs:['right_sole_dopamine.q','aurora.out0'],
    outputs:['histosol.in0'],
    bio:'Proprioceptive balance joint. Lymphatic drainage. Connects to right_sole_dopamine (motor dopamine) and aurora (Na+ threshold). Output feeds histosol (soil/ground connection). Mirror: right_ankle.' },

  { name:'left_arm', gate:'AND', particle:'gluon', element:'Ga(31)', dim:'g',
    location:'left arm (brachial plexus)', side:'left',
    inputs:['actomyosin.out0','observer_leftd2.out0'],
    outputs:['adapter_protein.d'],
    bio:'Brachial plexus motor/sensory pathway. Strong force binding (gluon). Connects to actomyosin (muscle contraction) and observer bus. Output clocks adapter_protein (somatic adapter). Mirror: right arm (substance_p).' },

  { name:'left_cheek', gate:'MUX', particle:'electron', element:'K(19)', dim:'s',
    location:'left cheek (buccinator / CN VII)', side:'left',
    inputs:['right_acetylcholine.out0','hind_insula.out0'],
    outputs:['memory_entropy.in_hind_insula'],
    bio:'Facial nerve motor + trigeminal sensory. Electron = neural signal. Connects to right_acetylcholine (cholinergic) and hind_insula (interoception). Output feeds memory_entropy (novelty mismatch). Mirror: right_cheek.' },

  { name:'left_clavicle', gate:'AND', particle:'proton', element:'Mo(42)', dim:'r',
    location:'left clavicle (sternocleidomastoid origin)', side:'left',
    inputs:['heme.out0','observer_leftd2.out0'],
    outputs:['pi_electron_cloud.in0'],
    bio:'Subclavian vessels, SCM attachment. Proton = vascular flow. Connects to heme (blood) and observer bus. Output feeds pi_electron_cloud (electron routing). Mirror: right_clavicle.' },

  { name:'left_dorsal_foot', gate:'AND', particle:'electron', element:'Sr(38)', dim:'r',
    location:'left dorsal foot (dorsalis pedis)', side:'left',
    inputs:['right_sole_dopamine.q','histosol.out0'],
    outputs:['pyrite.in0'],
    bio:'Dorsalis pedis artery, extensor tendons. Electron = peripheral neural. Connects to right_sole_dopamine (dopamine) and histosol (soil). Output feeds pyrite (framboidal iron). Mirror: right_dorsal_foot.' },

  { name:'left_eye_inner', gate:'MUX', particle:'photon', element:'Cu(29)', dim:'s',
    location:'left medial canthus / lacrimal caruncle', side:'left',
    inputs:['aurora.out0','water_vapour.out0'],
    outputs:['pentose_phosphate.in0'],
    bio:'Medial canthus, nasolacrimal duct. Photon = light/lacrimal. Connects to aurora (EM field) and water_vapour (tears). Output feeds pentose_phosphate (PPP antioxidant). Mirror: right_eye_inner (pentose_phosphate).' },

  { name:'left_fingers', gate:'AND', particle:'photon', element:'Se(34)', dim:'g',
    location:'left fingers (digital arteries / flexor tendons)', side:'left',
    inputs:['adapter_protein.q','actomyosin.out0'],
    outputs:['adapter_protein.d'],
    bio:'Fine motor precision, digital circulation. Photon = precision/light touch. Connects to adapter_protein (somatic adapter) and actomyosin (motor). Output clocks adapter_protein. Mirror: right_fingers (adapter_protein, actomyosin).' },

  { name:'left_hand', gate:'AND', particle:'proton', element:'As(33)', dim:'g',
    location:'left hand (thenar / median nerve)', side:'left',
    inputs:['actomyosin.out0','observer_leftd2.out0'],
    outputs:['chlorine_ion_pump.in0'],
    bio:'Thenar/hypothenar, median/ulnar nerve. Proton = motor drive. Connects to actomyosin (contraction) and observer bus. Output feeds chlorine_ion_pump (ion transport). Mirror: right_hand (chlorine_ion_pump).' },

  { name:'left_jaw', gate:'AND', particle:'tau', element:'Ti(22)', dim:'r',
    location:'left jaw (masseter / TMJ / V3)', side:'left',
    inputs:['right_acetylcholine.out0','collagen.out0'],
    outputs:['collagen.in1'],
    bio:'Masseter, TMJ, trigeminal V3. Tau = heavy force. Connects to right_acetylcholine (cholinergic motor) and collagen (connective tissue). Output feeds collagen (matrix tension). Mirror: right_jaw.' },

  { name:'left_kidney', gate:'tristate', particle:'higgs', element:'Y(39)', dim:'r',
    location:'left kidney (renal cortex)', side:'left',
    inputs:['heme.out1','ferritin.in0'],
    outputs:['heme.in1'],
    bio:'Renal filtration, RAAS, EPO production. Higgs = mass/filtration. Connects to heme (iron/EPO) and ferritin (iron storage). Output feeds heme (iron recirculation). Mirror: right_kidney.' },

  { name:'left_lung', gate:'tristate', particle:'photon', element:'Zr(40)', dim:'h',
    location:'left lung (pulmonary circulation)', side:'left',
    inputs:['cytochrome_c_oxidase.out0','co2.out0'],
    outputs:['cytochrome_c_oxidase.in0'],
    bio:'Pulmonary gas exchange. Photon = O2/light. Connects to COX (O2 consumption) and co2 (CO2). Output feeds COX (oxygen supply). Mirror: right_lung.' },

  { name:'left_nose', gate:'MUX', particle:'quark', element:'Si(14)', dim:'d',
    location:'left nasal cavity / olfactory epithelium', side:'left',
    inputs:['memory_entropy.out_hind_insula','hind_insula.out0'],
    outputs:['carbon.in0'],
    bio:'Olfactory epithelium, nasal mucosa. Quark = sensory creation. Connects to memory_entropy (novelty) and hind_insula (interoception). Output feeds carbon (structural latch). Mirror: right_nose.' },

  { name:'left_popliteal', gate:'AND', particle:'neutrino', element:'Kr(36)', dim:'r',
    location:'left popliteal fossa (popliteal artery/vein)', side:'left',
    inputs:['water.out0','observer_leftd2.out0'],
    outputs:['histosol.in1'],
    bio:'Popliteal vessels, tibial nerve. Neutrino = passive flow. Connects to water (fluid) and observer bus. Output feeds histosol (soil drainage). Mirror: right_popliteal.' },

  { name:'left_shoulder', gate:'AND', particle:'w_boson', element:'Zn(30)', dim:'gamma',
    location:'left shoulder (deltoid / rotator cuff)', side:'left',
    inputs:['aurora.out0','actomyosin.out0'],
    outputs:['fold_belt.in0'],
    bio:'Deltoid, rotator cuff, brachial plexus. W_boson = weak force/mobility. Connects to aurora (Na+ threshold) and actomyosin (motor). Output feeds fold_belt (structural tension). Mirror: right_shoulder.' },

  { name:'left_temple', gate:'MUX', particle:'muon', element:'Mn(25)', dim:'h',
    location:'left temple (temporalis / temporal artery)', side:'left',
    inputs:['memory_entropy.out_hind_insula','hind_insula.out0'],
    outputs:['mc1r.in0'],
    bio:'Temporalis muscle, temporal artery, MCA. Muon = neural. Connects to memory_entropy (hippocampal) and hind_insula (insula). Output feeds mc1r (MC1R receptor switch). Mirror: right_temple (right_acetylcholine).' },

  { name:'left_testis', gate:'AND', particle:'z_boson', element:'Tc(43)', dim:'r',
    location:'left testis (Leydig cells / spermatogenesis)', side:'left',
    inputs:['right_androgen.out0','craton.out1'],
    outputs:['left_genital_d2.in2'],
    bio:'Spermatogenesis, Leydig testosterone. Z_boson = reproductive weak force. Connects to right_androgen (androgen) and craton (structural). Output feeds left_genital_d2 (D2 brake). Mirror: right_testis.' },

  { name:'left_tibial', gate:'AND', particle:'muon', element:'Rb(37)', dim:'r',
    location:'left posterior tibial (artery / nerve)', side:'left',
    inputs:['right_sole_dopamine.q','observer_leftd2.out0'],
    outputs:['magnetite.in0'],
    bio:'Posterior tibial artery/nerve. Muon = neural. Connects to right_sole_dopamine (dopamine) and observer bus. Output feeds magnetite (magnetic sensing). Mirror: right_tibial.' },

  { name:'left_upper_back', gate:'AND', particle:'w_boson', element:'Nb(41)', dim:'gamma',
    location:'left upper back (trapezius / rhomboids)', side:'left',
    inputs:['aurora.out0','observer_leftd2.out0'],
    outputs:['subduction_zone.in0'],
    bio:'Trapezius, rhomboids, scapular stabilizers. W_boson = postural. Connects to aurora (EM) and observer bus. Output feeds subduction_zone (structural gate). Mirror: right_upper_back.' },

  { name:'left_wrist', gate:'AND', particle:'neutrino', element:'Ge(32)', dim:'g',
    location:'left wrist (carpal tunnel / median nerve)', side:'left',
    inputs:['chlorine_ion_pump.out0','adapter_protein.q'],
    outputs:['adapter_protein.d'],
    bio:'Carpal tunnel, flexor retinaculum. Neutrino = fine flow. Connects to chlorine_ion_pump (ion transport) and adapter_protein (somatic adapter). Output clocks adapter_protein. Mirror: right_wrist (chlorine_ion_pump).' },

  // --- RIGHT SIDE ---
  { name:'right_abdomen', gate:'AND', particle:'higgs', element:'Cd(48)', dim:'r',
    location:'right abdomen (liver / gallbladder region)', side:'right',
    inputs:['heme.out1','methanogenesis.out0'],
    outputs:['ferritin.in1'],
    bio:'Hepatic flexure, gallbladder, liver right lobe. Higgs = mass/metabolism. Connects to heme (heme breakdown) and methanogenesis (gut). Output feeds ferritin (iron storage). Mirror: left abdomen (methylation).' },

  { name:'right_ankle', gate:'AND', particle:'z_boson', element:'Br(35)', dim:'r',
    location:'right ankle (talocrural joint)', side:'right',
    inputs:['right_sole_dopamine.q','aurora.out0'],
    outputs:['histosol.in0'],
    bio:'Mirror of left_ankle. Proprioceptive balance. Connects to right_sole_dopamine and aurora. Output feeds histosol.' },

  { name:'right_calf', gate:'AND', particle:'tau', element:'In(49)', dim:'r',
    location:'right calf (gastrocnemius / soleus / Achilles)', side:'right',
    inputs:['actomyosin.out0','observer_leftd2.out0'],
    outputs:['pyrite.in0'],
    bio:'Gastrocnemius/soleus, venous pump. Tau = force. Connects to actomyosin (contraction) and observer bus. Output feeds pyrite (iron-sulfur). Mirror: left calf (caco3_final_and, laterite).' },

  { name:'right_cheek', gate:'MUX', particle:'electron', element:'K(19)', dim:'s',
    location:'right cheek (buccinator / CN VII)', side:'right',
    inputs:['right_acetylcholine.out0','hind_insula.out0'],
    outputs:['memory_entropy.in_hind_insula'],
    bio:'Mirror of left_cheek. Facial nerve + trigeminal. Connects to right_acetylcholine and hind_insula.' },

  { name:'right_clavicle', gate:'AND', particle:'proton', element:'Mo(42)', dim:'r',
    location:'right clavicle (SCM / subclavian)', side:'right',
    inputs:['heme.out0','observer_leftd2.out0'],
    outputs:['pi_electron_cloud.in0'],
    bio:'Mirror of left_clavicle. Subclavian vessels. Connects to heme and observer bus.' },

  { name:'right_dorsal_foot', gate:'AND', particle:'electron', element:'Sr(38)', dim:'r',
    location:'right dorsal foot (dorsalis pedis artery)', side:'right',
    inputs:['right_sole_dopamine.q','histosol.out0'],
    outputs:['pyrite.in0'],
    bio:'Mirror of left_dorsal_foot. Dorsalis pedis. Connects to right_sole_dopamine and histosol.' },

  { name:'right_femoral', gate:'OR', particle:'proton', element:'Fe(26)', dim:'r',
    location:'right femoral triangle (femoral artery/nerve)', side:'right',
    inputs:['heme.out0','water.out0'],
    outputs:['actomyosin.in0'],
    bio:'Femoral artery/nerve, iliopsoas. Proton = vascular. OR gate = alternative flow path. Connects to heme (blood) and water (fluid). Output feeds actomyosin (contraction). Mirror: left femoral (caco3_final_and).' },

  { name:'right_forehead', gate:'AND', particle:'electron', element:'Ru(44)', dim:'r',
    location:'right forehead (frontalis / supraorbital nerve)', side:'right',
    inputs:['observer_leftd2.out0','electric_grid_and.out0'],
    outputs:['pi_electron_cloud.in0'],
    bio:'Frontalis muscle, supraorbital nerve. Electron = neural. Connects to observer_leftd2 (same region) and electric_grid_and (bio-electric grid). Output feeds pi_electron_cloud. Mirror: left forehead (observer_leftd2, nonobserver_left_d2).' },

  { name:'right_genital', gate:'AND', particle:'proton', element:'Rh(45)', dim:'d',
    location:'right genital (genitofemoral nerve / cremaster)', side:'right',
    inputs:['aurora_2.out','left_genital_d2.out0'],
    outputs:['water.in1'],
    bio:'Genitofemoral nerve, cremaster, right genital vasopressin pathway. Proton = motor/vascular. Connects to aurora_2 (stress XOR Na+) and left_genital_d2 (D2 brake). Output feeds water (fluid regulation). THIS IS THE UNWIRED AURORA→RIGHT_GENITAL CONNECTION. Mirror: left_genital (left_genital_d2).' },

  { name:'right_jaw', gate:'AND', particle:'tau', element:'Ti(22)', dim:'r',
    location:'right jaw (masseter / TMJ)', side:'right',
    inputs:['right_acetylcholine.out0','collagen.out0'],
    outputs:['collagen.in1'],
    bio:'Mirror of left_jaw. Masseter, TMJ. Connects to right_acetylcholine and collagen.' },

  { name:'right_kidney', gate:'tristate', particle:'higgs', element:'Y(39)', dim:'r',
    location:'right kidney (renal cortex)', side:'right',
    inputs:['heme.out1','ferritin.in0'],
    outputs:['heme.in1'],
    bio:'Mirror of left_kidney. Renal filtration, EPO. Connects to heme and ferritin.' },

  { name:'right_knee', gate:'AND', particle:'graviton', element:'Sn(50)', dim:'r',
    location:'right knee (patellofemoral / meniscus / cruciate)', side:'right',
    inputs:['actomyosin.out0','magnetite.out0'],
    outputs:['magnetite.in0'],
    bio:'Patellofemoral joint, meniscus. Graviton = structural weight. Connects to actomyosin (motor) and magnetite (magnetic sensing). Output feeds magnetite. Mirror: left_knee (caco3_final_and, magnetite).' },

  { name:'right_lung', gate:'tristate', particle:'photon', element:'Zr(40)', dim:'h',
    location:'right lung (pulmonary circulation)', side:'right',
    inputs:['cytochrome_c_oxidase.out0','co2.out0'],
    outputs:['cytochrome_c_oxidase.in0'],
    bio:'Mirror of left_lung. Pulmonary gas exchange. Connects to COX and co2.' },

  { name:'right_neck', gate:'AND', particle:'muon', element:'Pd(46)', dim:'r',
    location:'right neck (SCM / carotid sheath / vagus)', side:'right',
    inputs:['right_acetylcholine.out0','pi_electron_cloud.q_bar'],
    outputs:['right_acetylcholine.in0'],
    bio:'SCM, carotid sheath, vagus nerve. Muon = neural. Connects to right_acetylcholine (cholinergic) and pi_electron_cloud (electron routing). Output feeds right_acetylcholine. Mirror: left_neck (pi_electron_cloud).' },

  { name:'right_nipple', gate:'AND', particle:'gluon', element:'Ag(47)', dim:'r',
    location:'right nipple (areolar smooth muscle / sympathetic)', side:'right',
    inputs:['observer_leftd2.out0','male_right_oxytocin.q'],
    outputs:['bioenergetic_drive_and.in0'],
    bio:'Areolar smooth muscle, sympathetic innervation. Gluon = binding. Connects to observer bus and male_right_oxytocin (oxytocin). Output feeds bioenergetic_drive_and (metabolic drive). Mirror: left_nipple (heme).' },

  { name:'right_nose', gate:'MUX', particle:'quark', element:'Si(14)', dim:'d',
    location:'right nasal cavity / olfactory epithelium', side:'right',
    inputs:['memory_entropy.out_hind_insula','hind_insula.out0'],
    outputs:['carbon.in0'],
    bio:'Mirror of left_nose. Olfactory epithelium. Connects to memory_entropy and hind_insula.' },

  { name:'right_popliteal', gate:'AND', particle:'neutrino', element:'Kr(36)', dim:'r',
    location:'right popliteal fossa', side:'right',
    inputs:['water.out0','observer_leftd2.out0'],
    outputs:['histosol.in1'],
    bio:'Mirror of left_popliteal. Popliteal vessels. Connects to water and observer bus.' },

  { name:'right_shoulder', gate:'AND', particle:'w_boson', element:'Zn(30)', dim:'gamma',
    location:'right shoulder (deltoid / rotator cuff)', side:'right',
    inputs:['aurora.out0','actomyosin.out0'],
    outputs:['fold_belt.in0'],
    bio:'Mirror of left_shoulder. Deltoid, rotator cuff. Connects to aurora and actomyosin.' },

  { name:'right_testis', gate:'AND', particle:'z_boson', element:'Tc(43)', dim:'r',
    location:'right testis (Leydig cells)', side:'right',
    inputs:['right_androgen.out0','craton.out1'],
    outputs:['drd2_mpoa.in2'],
    bio:'Mirror of left_testis. Spermatogenesis. Connects to right_androgen and craton. Output feeds drd2_mpoa (D2 brake).' },

  { name:'right_tibial', gate:'AND', particle:'muon', element:'Rb(37)', dim:'r',
    location:'right posterior tibial', side:'right',
    inputs:['right_sole_dopamine.q','observer_leftd2.out0'],
    outputs:['magnetite.in0'],
    bio:'Mirror of left_tibial. Posterior tibial. Connects to right_sole_dopamine and observer bus.' },

  { name:'right_upper_back', gate:'AND', particle:'w_boson', element:'Nb(41)', dim:'gamma',
    location:'right upper back (trapezius / rhomboids)', side:'right',
    inputs:['aurora.out0','observer_leftd2.out0'],
    outputs:['subduction_zone.in0'],
    bio:'Mirror of left_upper_back. Trapezius, rhomboids. Connects to aurora and observer bus.' },

  { name:'right_waist', gate:'AND', particle:'neutrino', element:'Sb(51)', dim:'nu',
    location:'right waist (quadratus lumborum / lat insertion)', side:'right',
    inputs:['basin.q','mc1r.q'],
    outputs:['basin.d'],
    bio:'Quadratus lumborum, latissimus insertion. Neutrino = passive structural. Connects to basin (metabolic sink) and mc1r (MC1R switch). Output clocks basin. Mirror: left_waist (mc1r, basin).' },
];

// ============================================================
// 3. BUILD COMPLETE NODE MAP
// ============================================================
const nodeParticleMap = {};
const nodeDimMap = {};

for (const n of existingNodes) {
  if (n.particle) nodeParticleMap[n.name] = n.particle;
  if (n.dim8) {
    const m = n.dim8.match(/([rhdp]|gamma|g|nu)/i);
    if (m) nodeDimMap[n.name] = m[1].toLowerCase();
  }
}
for (const n of newNodes) {
  nodeParticleMap[n.name] = n.particle;
  nodeDimMap[n.name] = n.dim;
}

// ============================================================
// 4. PARTICLE NORMALIZATION
// ============================================================
function normalizeParticle(raw) {
  if (!raw) return null;
  const p = raw.trim();
  const lower = p.toLowerCase();

  if (lower === 'proton' || lower === 'spark' || lower.includes('proton')) return 'proton';
  if (lower === 'gluon' || lower === 'gaba-a') return 'gluon';
  if (lower === 'muon' || lower === 'gaba-b' || lower === 'gaba-b_2') return 'muon';
  if (lower === 'electron' || lower === 'electron') return 'electron';
  if (lower.includes('quark') || lower === 'up' || lower === 'down' || lower === 'strange' || lower === 'charm') return 'quark';
  if (lower === 'higgs' || lower === 'ego' || lower === 'neutron_star') return 'higgs';
  if (lower === 'w_boson' || lower === 'w' || lower.includes('w boson') || lower === 'vasopressin' || lower === 'right_testosterone') return 'w_boson';
  if (lower === 'z_boson' || lower === 'z' || lower === 'z boson' || lower === 'axion' || lower === 'dark' || lower === 'dark energy' || lower === 'time' || lower === 'gkyib') return 'z_boson';
  if (lower.includes('neutrino') || lower === 'neutron') return 'neutrino';
  if (lower === 'tau') return 'tau';
  if (lower === 'photon' || lower === 'observer' || lower === 'expression') return 'photon';
  if (lower.includes('electromagnetic') || lower === 'em') return 'em';
  if (lower === 'graviton') return 'higgs';
  if (lower === 'dopamine' || lower === 'noradrenaline') return 'electron';
  if (lower === 'cortisol' || lower === 'satisfaction') return 'higgs';
  if (lower === 'tca' || lower === 'energy' || lower === 'precursor') return 'proton';
  if (lower === 'serotonin_1a' || lower === 'serotonin_1b') return 'neutrino';

  return null;
}

const PARTICLES12 = ['proton','gluon','muon','electron','quark','higgs','w_boson','z_boson','neutrino','tau','photon','em'];

// Count nodes per particle
const particleCounts = {};
for (const p of PARTICLES12) particleCounts[p] = 0;
for (const name in nodeParticleMap) {
  const np = normalizeParticle(nodeParticleMap[name]);
  if (np && particleCounts[np] !== undefined) particleCounts[np]++;
}

// ============================================================
// 5. CIRCUIT STATE COMPUTATION
// ============================================================
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
const RITUAL = [
  {b:1,g:0},{b:1,g:1},{b:0,g:0},{b:0,g:1},{b:3,g:0},{b:3,g:1},{b:2,g:0},{b:2,g:1},{b:-1,g:-1}
];

function compute8D(m, b, g, l, geo, t, isObserver, day) {
  const rng = mulberry32(Math.floor(t * 100) + l * 10000 + geo * 100000 + m * 1000000 + 1);
  const h = t % 24.0;

  // Observer
  const obs = isObserver ? 1.0 : (h >= 21 || h < 6 ? 0.0 : Math.max(0, Math.min(1, 0.5 + 0.3 * Math.cos((h - 10) * Math.PI / 12))));

  // Window + peak
  const w = Math.floor(h / 1.5);
  const peakDim = ['r','h','d','p','s','gamma','g','nu','r','h','d','p','s','gamma','g','nu'][w % 16];
  const peakVal = 0.5 + 0.5 * Math.abs(Math.cos((h % 1.5) / 1.5 * Math.PI));

  // Layer transform
  let m2 = m, b2 = b;
  if (l === 1) m2 = m ^ 0b1001;
  if (l === 2) b2 = (b + 1) % 4;
  if (l === 3) { m2 = m ^ 0b1001; b2 = (b + 1) % 4; }

  // Base 8D from cognitive stack
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

  // Layer B/D transforms
  if (l === 1 || l === 3) {
    vec.nu = Math.min(1.0, vec.nu + 0.10);
    vec.gamma = Math.max(0.0, vec.gamma - 0.05);
  }
  if (l === 3 && (h >= 21 || h < 3)) {
    vec.p = rng();
    vec.s = 0.5 + rng() * 0.5;
    vec.nu = 0.9 + rng() * 0.1;
  }

  // Jitter
  const jitter = [0, 0.15, 0.15, 0.30][l];
  if (jitter > 0) {
    vec.r = Math.max(0, Math.min(1, vec.r * (1 + (rng() - 0.5) * 2 * jitter)));
    vec.d = Math.max(0, Math.min(1, vec.d * (1 + (rng() - 0.5) * 2 * jitter)));
  }

  // Peak boost
  vec[peakDim] = Math.max(vec[peakDim], peakVal);

  // Geographic modulation
  const geoMod = {
    0: {r:0.7, h:0.5, d:0.5, p:0.5, s:0.5, gamma:1.0, g:0.9, nu:0.5},
    1: {r:0.6, h:0.5, d:0.9, p:0.5, s:0.9, gamma:0.5, g:0.5, nu:0.5},
    2: {r:0.5, h:0.9, d:0.5, p:0.9, s:0.5, gamma:0.3, g:0.5, nu:0.5},
  }[geo];
  for (const k in vec) vec[k] *= geoMod[k];

  // 9-day ritual
  const r = RITUAL[(day - 1) % 9];
  const ritualBoost = (r.b === b && r.g === g) ? 1.15 : 1.0;
  for (const k in vec) vec[k] *= ritualBoost;

  // Observer
  for (const k in vec) vec[k] *= (obs > 0 ? obs : 0.1);

  // Clamp
  for (const k in vec) vec[k] = Math.max(0, Math.min(1, vec[k]));

  return { vec, obs, peakDim, h, rng };
}

function hysteresis(h) {
  const hy = {};
  if (h >= 15 && h <= 21) { const i = 1 - Math.abs(h - 18) / 3; hy.d_boost = Math.max(0, i); hy.gamma_boost = Math.max(0, i) * 0.3; }
  else { hy.d_boost = 0; hy.gamma_boost = 0; }
  if (h >= 16 && h <= 17.5) { const u = 1 - Math.abs(h - 16.5); hy.photon_drop = Math.max(0, u); hy.em_drop = Math.max(0, u) * 0.7; hy.proton_rise = Math.max(0, u) * 0.5; }
  else { hy.photon_drop = 0; hy.em_drop = 0; hy.proton_rise = 0; }
  if (h >= 2 && h <= 4) { const c = 1 - Math.abs(h - 3); hy.collapse = Math.max(0, c); hy.neutrino_boost = Math.max(0, c); }
  else { hy.collapse = 0; hy.neutrino_boost = 0; }
  if (h >= 4 && h <= 6) { const b = 1 - Math.abs(h - 5.25); hy.photon_rise = Math.max(0, b); hy.em_rise = Math.max(0, b); hy.z_boson_rise = Math.max(0, b) * 0.5; }
  else { hy.photon_rise = 0; hy.em_rise = 0; hy.z_boson_rise = 0; }
  return hy;
}

// ============================================================
// 6. COMPUTE TENSOR — ALL 329 NODES
// ============================================================
function computeTensor(m, b, g, l, geo, t, isObserver, day) {
  const { vec, h } = compute8D(m, b, g, l, geo, t, isObserver, day);
  const hy = hysteresis(h);

  // Aggregate all 329 nodes by normalized particle
  const sums = {};
  const counts = {};
  for (const p of PARTICLES12) { sums[p] = 0; counts[p] = 0; }

  // Process existing 282 nodes
  for (const n of existingNodes) {
    const dim = nodeDimMap[n.name];
    let val = dim ? vec[dim] : 0.5;
    const rawP = nodeParticleMap[n.name] || '';
    const np = normalizeParticle(rawP);
    if (!np) continue;

    // Hysteresis
    if (np === 'photon') { val -= hy.photon_drop * 0.5; val += hy.photon_rise * 0.5; }
    if (np === 'em') { val -= hy.em_drop * 0.4; val += hy.em_rise * 0.4; if (geo === 0) val *= 1.1; if (geo === 2) val *= 0.85; }
    if (np === 'proton') val += hy.proton_rise * 0.3;
    if (np === 'neutrino') val += hy.neutrino_boost * 0.5;
    if (np === 'higgs') { val += hy.d_boost * 0.3; if (geo === 2) val *= 1.1; }
    if (np === 'gluon' && geo === 0) val *= 1.1;
    if (np === 'quark' && geo === 1) val *= 1.1;
    if (np === 'w_boson') val += hy.gamma_boost * 0.2;
    if (hy.collapse > 0 && np !== 'neutrino') val *= (1 - hy.collapse * 0.7);

    // Gate type modulation
    const gt = (n.gateType || '').toLowerCase();
    if (gt.includes('and')) val *= 0.9;
    if (gt.includes('xor')) val *= 0.8;
    if (gt.includes('flip-flop')) val = val * 0.7 + 0.3 * (val > 0.5 ? 1 : 0);
    if (gt.includes('tristate')) val *= 0.85;

    val = Math.max(0, Math.min(1, val));
    sums[np] += val;
    counts[np]++;
  }

  // Process 47 new nodes
  for (const n of newNodes) {
    const dim = n.dim;
    let val = vec[dim] || 0.5;
    const np = n.particle === 'strange_quark' ? 'quark' : n.particle;

    // Hysteresis
    if (np === 'photon') { val -= hy.photon_drop * 0.5; val += hy.photon_rise * 0.5; }
    if (np === 'z_boson') { val += hy.z_boson_rise * 0.3; if (hy.collapse > 0) val -= hy.collapse * 0.3; }
    if (np === 'neutrino') val += hy.neutrino_boost * 0.5;
    if (np === 'higgs') { val += hy.d_boost * 0.3; if (geo === 2) val *= 1.1; }
    if (np === 'gluon' && geo === 0) val *= 1.1;
    if (np === 'quark' && geo === 1) val *= 1.1;
    if (np === 'w_boson') val += hy.gamma_boost * 0.2;
    if (np === 'em') { val -= hy.em_drop * 0.4; val += hy.em_rise * 0.4; if (geo === 0) val *= 1.1; if (geo === 2) val *= 0.85; }
    if (hy.collapse > 0 && np !== 'neutrino') val *= (1 - hy.collapse * 0.7);

    // Gate type
    if (n.gate === 'AND') val *= 0.9;
    if (n.gate === 'MUX') val *= 0.95;
    if (n.gate === 'tristate') val *= 0.85;
    if (n.gate === 'OR') val *= 1.0;

    val = Math.max(0, Math.min(1, val));
    sums[np] += val;
    counts[np]++;
  }

  // Average per particle
  const results = {};
  for (const p of PARTICLES12) {
    results[p] = counts[p] > 0 ? Math.round((sums[p] / counts[p]) * 100) / 100 : 0;
  }
  return results;
}

// ============================================================
// 7. OUTPUT
// ============================================================
const TARGET_TIMES = [16.50, 3.00, 4.50];
const TIME_LABELS = ['4:30PM', '3:00AM', '4:30AM'];
const BLOOD_NAMES = ['O','A','B','AB'];
const MBTI_NAMES = ['ENFP','ISFP','ESFJ','INTP','ENTP','INFJ','ESTP','ISTP','ENFJ','INTJ','ESFP','ISTJ','ESTJ','INFP','ISFJ','ENTJ'];
const GEO_NAMES = ['Oxford','England','Korea'];
const LAYER_NAMES = ['A','B','C','D'];

// Stats
console.log('='.repeat(100));
console.log('TENSOR V4 — COMPLETE CIRCUIT (329 NODES, ALL WIRED)');
console.log('='.repeat(100));
console.log(`Original: 282 | Generated: 47 | Total: 329`);
console.log(`New wires: ${newNodes.length * 2} (inputs + outputs per node)`);
console.log('');
console.log('Particle distribution (all 329 nodes):');
for (const p of PARTICLES12) {
  console.log(`  ${p.padEnd(12)}: ${particleCounts[p]} nodes`);
}

// Full table for ENTP_M_O
for (let geo = 0; geo < 3; geo++) {
  console.log('');
  console.log('='.repeat(160));
  console.log(`T[ENTP_M_O, Layer, Geo=${GEO_NAMES[geo]}, t] — 329 nodes, Day 3`);
  console.log('='.repeat(160));
  let header = 'Particle    ';
  for (let l = 0; l < 4; l++) for (const tl of TIME_LABELS) header += ` | L${LAYER_NAMES[l]}_${tl}`;
  console.log(header);
  console.log('-'.repeat(160));
  for (const p of PARTICLES12) {
    let row = p.padEnd(12);
    for (let l = 0; l < 4; l++) {
      for (const t of TARGET_TIMES) {
        row += ` | ${computeTensor(4, 0, 0, l, geo, t, true, 3)[p].toFixed(2).padStart(11)}`;
      }
    }
    console.log(row);
  }
}

// Geographic comparison
console.log('');
console.log('='.repeat(130));
console.log('GEOGRAPHIC COMPARISON: ENTP_M_O, Layer A, Day 3, 329 nodes');
console.log('='.repeat(130));
let header = 'Particle    ';
for (const gn of GEO_NAMES) for (const tl of TIME_LABELS) header += ` | ${gn.substring(0,3)}_${tl}`;
console.log(header);
console.log('-'.repeat(130));
for (const p of PARTICLES12) {
  let row = p.padEnd(12);
  for (let geo = 0; geo < 3; geo++) {
    for (const t of TARGET_TIMES) {
      row += ` | ${computeTensor(4, 0, 0, 0, geo, t, true, 3)[p].toFixed(2).padStart(8)}`;
    }
  }
  console.log(row);
}

// All 128 profiles
console.log('');
console.log('='.repeat(200));
console.log('ALL 128 PROFILES × 3 GEO × 3 TIMES × 12 PARTICLES (Layer A, Observer, Day 3, 329 nodes)');
console.log('='.repeat(200));
for (let m = 0; m < 16; m++) {
  for (let b = 0; b < 4; b++) {
    for (let g = 0; g < 2; g++) {
      let row = `${MBTI_NAMES[m]}_${g===0?'M':'F'}_${BLOOD_NAMES[b]}`.padEnd(14);
      for (let geo = 0; geo < 3; geo++) {
        for (const t of TARGET_TIMES) {
          const vals = computeTensor(m, b, g, 0, geo, t, true, 3);
          for (const p of PARTICLES12) row += ` ${vals[p].toFixed(2)}`;
          row += ' |';
        }
      }
      console.log(row);
    }
  }
}
