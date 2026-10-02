const fs = require('fs');
const text = fs.readFileSync('prose.txt','utf8');

// Split into detailed node blocks by line-start pattern "N. name —"
const detailBlocks = [];
const lines = text.split('\n');
let current = null;
lines.forEach(line => {
  const m = line.match(/^(\d{1,2})\.\s+([\w_]+)\s+—/);
  if (m) {
    if (current) detailBlocks.push(current);
    current = { num: parseInt(m[1]), name: m[2], lines: [] };
  }
  if (current) current.lines.push(line);
});
if (current) detailBlocks.push(current);

function normParticle(raw) {
  if (!raw) return '';
  const p = raw.toLowerCase().trim();
  if (p.includes('proton')) return 'proton';
  if (p.includes('photon')) return 'photon';
  if (p.includes('electron_antineutrino') || p.includes('electron_neutrino') || p.includes('muon_neutrino') || p.includes('tau_neutrino') || p.includes('tau_antineutrino') || p.includes('antineutrino') || p.includes('neutrino')) return 'neutrino';
  if (p.includes('muon')) return 'muon';
  if (p.includes('tau')) return 'tau';
  if (p.includes('gluon')) return 'gluon';
  if (p.includes('w_boson') || p.includes('w boson') || p.includes('w-boson')) return 'w_boson';
  if (p.includes('z_boson') || p.includes('z boson') || p.includes('z-boson')) return 'z_boson';
  if (p.includes('higgs')) return 'higgs';
  if (p.includes('axion')) return 'axion';
  if (p.includes('quark') || p.includes('up') || p.includes('down') || p.includes('strange') || p.includes('charm')) return 'quark';
  if (p.includes('graviton')) return 'graviton';
  if (p.includes('electron')) return 'electron';
  if (p.includes('dark_energy') || p.includes('time')) return 'z_boson';
  if (p.includes('dark_matter') || p.includes('neutron_star')) return 'higgs';
  if (p.includes('energy')) return 'photon';
  if (p.includes('spark')) return 'photon';
  if (p.includes('testosterone') || p.includes('progesterone')) return 'w_boson';
  if (p.includes('neutron')) return 'neutrino'; // not in 12, map to closest
  return '';
}

// Explicit route sets from prose.txt 3-route definition
const oxfordCore = new Set(['observer_leftd2','heme','steel','clay_gouge','quark_orogen_magma','observer_left_endorphin_electron_antineutrino','nonobserver_left_d2','carbon']);
const englandSet = new Set(['methanogenesis','histosol','sulforaphane','aurora','glymphatic_system','cysteine','memory_entropy','hind_insula','fold_belt','substance_p']);
const koreaSet = new Set(['ferritin','peat','sodium','anoxia','actinium_trigger','adapter_protein','mycorradicin','andosol']);

const nodes = {};

detailBlocks.forEach(blk => {
  const block = blk.lines.join('\n');
  const elMatch = block.match(/원소=([^\n\/,]+)/);
  const pMatches = [...block.matchAll(/입자=([^\n\/,]+)/g)];
  const rawParticle = pMatches.length ? pMatches[0][1].trim() : '';
  const dimMatch = block.match(/음악 차원:\s*([rhdp]|gamma|g|nu)/i);
  let route = 'Oxford';
  if (koreaSet.has(blk.name) || /외부|external|world|Korea|retina|cochlea|EMF|피부/i.test(block)) route = 'Out_of_England';
  else if (englandSet.has(blk.name)) route = 'Out_of_Oxford';
  else if (oxfordCore.has(blk.name)) route = 'Oxford';
  else if (/histosol|sulforaphane|glymphatic|cysteine|memory_entropy|hind_insula|fold_belt|substance_p|methanogenesis|aurora/i.test(block)) route = 'Out_of_Oxford';
  const isDFF = /D flip-flop|래치/i.test(block);
  const hasQbar = isDFF && /q_bar/i.test(block);
  const graviton = /graviton/i.test(block) && hasQbar;
  const p12 = normParticle(rawParticle);
  const flag = p12 === 'neutron' ? 'NOT_IN_12' : '';
  nodes[blk.num] = { num: blk.num, name: blk.name, element: elMatch ? elMatch[1].trim() : '', rawParticle, particle12: p12==='neutron'?'':p12, dim: dimMatch ? dimMatch[1].toLowerCase() : '', route, isDFF, hasQbar, graviton, flag, source:'detail' };
});

// Nodes 1 and 9 have alternate heading formats; hardcode them
const detailExtra = {
  1: { name:'observer_leftd2', element:'Na(11)', rawParticle:'w_boson', particle12:'w_boson', dim:'p', route:'Oxford', isDFF:false, hasQbar:false, graviton:false, flag:'HEADING_EXTRA' },
  9: { name:'nonobserver_left_d2', element:'', rawParticle:'w_boson', particle12:'w_boson', dim:'g', route:'Oxford', isDFF:false, hasQbar:false, graviton:false, flag:'HEADING_EXTRA' }
};
for (const [num, info] of Object.entries(detailExtra)) {
  if (!nodes[num]) {
    nodes[num] = { num: parseInt(num), ...info, source:'detail' };
  }
}

// Manual mapping for nodes 71-84 from the Loop-Vector mapping table notes
const tableExtra = {
  71: { name:'left_amygdala', particle12:'electron', dim:'r', route:'Out_of_England' },
  72: { name:'left_thalamus', particle12:'photon', dim:'s', route:'Out_of_England' },
  73: { name:'left_hypothalamus', particle12:'w_boson', dim:'p', route:'Out_of_England' },
  74: { name:'pituitary', particle12:'higgs', dim:'g', route:'Out_of_England' },
  75: { name:'midbrain', particle12:'photon', dim:'s', route:'Out_of_England' },
  76: { name:'pons', particle12:'neutrino', dim:'nu', route:'Out_of_England' },
  77: { name:'medulla', particle12:'neutrino', dim:'g', route:'Out_of_England' },
  78: { name:'cerebellum', particle12:'quark', dim:'nu', route:'Out_of_England' },
  79: { name:'cerebellar_dentate', particle12:'w_boson', dim:'r', route:'Out_of_England' },
  80: { name:'spinal_cord_cervical', particle12:'photon', dim:'g', route:'Out_of_England' },
  81: { name:'right_phrenic_nerve', particle12:'w_boson', dim:'r', route:'Out_of_England' },
  82: { name:'diaphragm', particle12:'proton', dim:'r', route:'Out_of_England' },
  83: { name:'esophagus', particle12:'gluon', dim:'g', route:'Out_of_England' },
  84: { name:'stomach', particle12:'w_boson', dim:'r', route:'Out_of_England' },
};

// Also correct missing dims for known nodes from prose
const dimFix = {
  heme:'s', steel:'s', observer_left_endorphin_electron_antineutrino:'p', carbon:'p',
  aurora:'s', methanogenesis:'g', male_right_oxytocin:'h', glp1:'s', laterite:'s',
  manganese_nodule:'nu', nitrogenase:'g', water:'g', oxidised_manganese:'g',
  ferritin:'s', plume:'nu', cck:'r', mangrove_aerenchyma:'g'
};

for (const [num, info] of Object.entries(tableExtra)) {
  if (!nodes[num]) {
    nodes[num] = { num: parseInt(num), name: info.name, element:'', rawParticle:'', particle12: info.particle12, dim: info.dim, route: info.route, isDFF:false, hasQbar:false, graviton: info.particle12==='graviton', flag:'TABLE_EXTRA', source:'table' };
  }
}

// Hardcode missing particles from prose/table for detail nodes
const particleFix = {
  mc1r:'higgs',
  andosol:'higgs',
  mycorradicin:'gluon',
  autophagy:'tau',
  heath_aerenchyma:'neutrino',
  adapter_protein:'neutrino',
  left_genital_d2:'w_boson',
  lactate_dehydrogenase:'gluon',
  monazite:'z_boson',
  actomyosin_ctrl:'w_boson',
  gluon_orogen:'gluon'
};

for (const [k, particle] of Object.entries(particleFix)) {
  const n = Object.values(nodes).find(x=>x.name===k);
  if (n && !n.particle12) { n.particle12 = particle; n.rawParticle = particle; }
  if (n && n.name==='mc1r') { n.graviton = true; n.isDFF = true; n.hasQbar = true; }
}

for (const [k, info] of Object.entries(dimFix)) {
  const n = Object.values(nodes).find(x=>x.name===k);
  if (n && !n.dim) n.dim = info;
}

// Fallback dims by particle if still missing
const dimByParticle = {
  proton:'r', photon:'s', electron:'r', neutrino:'nu', muon:'d', tau:'d', gluon:'g',
  w_boson:'r', z_boson:'p', higgs:'g', axion:'nu', quark:'h', graviton:'p'
};
for (const k of Object.keys(nodes)) {
  const n = nodes[k];
  if (!n.dim && n.particle12) n.dim = dimByParticle[n.particle12] || 'g';
}

// Cleanup: remove non-node entries (single-letter dims) and renumber if needed
for (const k of Object.keys(nodes)) {
  const n = nodes[k];
  if (!n.name || n.name.length < 2 || /^(r|h|d|p|s|g|nu|gamma)$/.test(n.name)) {
    delete nodes[k];
  }
}

const list = Object.keys(nodes).sort((a,b)=>parseInt(a)-parseInt(b)).map(k=>nodes[k]);
console.log('Total:', list.length);
list.forEach(n=>console.log(`${String(n.num).padStart(2)} ${n.name.padEnd(28)} | ${(n.particle12||'').padEnd(10)} | ${(n.dim||'').padEnd(6)} | ${n.route} ${n.flag||''}`));

fs.writeFileSync('circuit84_extracted.json', JSON.stringify(list, null, 2));
