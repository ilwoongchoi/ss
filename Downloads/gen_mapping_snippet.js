"use strict";
const fs = require('fs');

const text = fs.readFileSync('prose.txt','utf8');
const circuit84 = JSON.parse(fs.readFileSync('circuit84_extracted.json','utf8'));

// Known real-ish coordinates for cosmic and geographic landmarks.
// Unknowns get null/0; the user can override.
const GEO = {
  'Australia': {lat:-25.27, lon:133.77, alt:0},
  'Pilbara, Australia': {lat:-21.5, lon:119.0, alt:0},
  'Ring of Fire': {lat:0, lon:180, alt:0},
  'Andean subduction arc magma chambers': {lat:-20, lon:-70, alt:-20000},
  'Lower Mantle D"" layer / 660-km discontinuity': {lat:0, lon:0, alt:-660000},
  'Earth’s outer core': {lat:0, lon:0, alt:-3000000},
  'Clarion-Clipperton Zone': {lat:13.5, lon:-128.0, alt:-5000},
  'Amazon basin': {lat:-5.0, lon:-60.0, alt:0},
  'Amazon Rainforest': {lat:-3.0, lon:-60.0, alt:0},
  'Mariana Trench': {lat:11.3, lon:142.2, alt:-11000},
  'Kuroko-type massive sulfide deposits, Japan': {lat:39.0, lon:140.0, alt:0},
  'Siberian Yedoma permafrost': {lat:65.0, lon:100.0, alt:0},
  'Andean altiplano': {lat:-16.0, lon:-69.0, alt:3800},
  'Iceland': {lat:65.0, lon:-19.0, alt:0},
  'Local Void': {lat:0, lon:0, alt:0},
  'Himalayas': {lat:27.9, lon:86.5, alt:5000},
  'Amazon basin — single largest tropical carbon sink/source toggle': {lat:-5.0, lon:-60.0, alt:0},
  'Ouachita fold belt': {lat:34.5, lon:-94.5, alt:0},
  'Bathurst massive-sulfide district, New Brunswick': {lat:47.6, lon:-65.6, alt:0},
  'Peru upwelling oxygen minimum zone': {lat:-15.0, lon:-75.0, alt:0},
  'Salar de Uyuni': {lat:-20.2, lon:-67.5, alt:3653},
  'Gaema Plateau uranium mine, Korean Peninsula': {lat:38.0, lon:128.0, alt:1000},
  'Hulun Lake, Manchuria': {lat:48.5, lon:117.5, alt:600},
  'Shatt al-Arab confluence': {lat:30.4, lon:47.8, alt:0},
  'Amazon-Andes atmospheric river': {lat:-5.0, lon:-70.0, alt:4000},
  'San Andreas fault gouge': {lat:35.0, lon:-120.0, alt:0},
  'Yellowstone Grand Prismatic hot spring': {lat:44.5, lon:-110.8, alt:0},
  'Arctic auroral zone': {lat:70, lon:0, alt:100},
  'Dead Sea': {lat:31.5, lon:35.5, alt:-430},
  'Amazon basin — single largest mycorrhizal symbiotic carbon-exchange forest': {lat:-5.0, lon:-60.0, alt:0},
  'Congo Basin': {lat:0, lon:20.0, alt:0},
  'Hawaiian Islands': {lat:19.5, lon:-155.5, alt:0},
  'Pampas chernozem': {lat:-36.0, lon:-62.0, alt:0},
  'Siberian boreal podzol belt': {lat:60.0, lon:100.0, alt:0},
  'Ganges foreland basin': {lat:27.0, lon:85.0, alt:0},
  'Panama Isthmus': {lat:9.0, lon:-80.0, alt:0},
  'Great Barrier Reef': {lat:-18.2, lon:147.7, alt:0},
  'New England temperate forest': {lat:43.0, lon:-71.0, alt:0},
  'Bab-el-Mandeb': {lat:12.6, lon:43.4, alt:0},
  'Indo-Gangetic Plain': {lat:27.0, lon:80.0, alt:0},
  'Brazilian Shield': {lat:-15.0, lon:-55.0, alt:0},
  'Yucatán Peninsula C4/C3 mixed photosynthesis belt': {lat:20.0, lon:-89.0, alt:0},
  'Chuquicamata, Chile': {lat:-22.3, lon:-68.9, alt:2800},
  'Salar de Atacama': {lat:-23.3, lon:-68.2, alt:2300},
  'Fynbos, Western Cape': {lat:-34.0, lon:18.5, alt:0},
  'Hawaii (Big Island)': {lat:19.5, lon:-155.5, alt:0},
  'Parkfield, San Andreas fault': {lat:35.9, lon:-120.4, alt:0},
  'Lake Taihu': {lat:31.2, lon:120.4, alt:0},
  'Lake Tanganyika': {lat:-6.0, lon:30.0, alt:773},
  'Himalayas — active continental collision orogen': {lat:27.9, lon:86.5, alt:5000},
  'Suez Canal': {lat:30.0, lon:32.5, alt:0},
  'Lago di Bolsena': {lat:42.6, lon:11.9, alt:0},
  'Krakatoa': {lat:-6.1, lon:105.4, alt:0},
  'Singapore Strait': {lat:1.2, lon:103.8, alt:0},
  'Nile delta': {lat:30.8, lon:31.0, alt:0},
  'Mecca': {lat:21.4, lon:39.8, alt:0},
  'Rust Belt': {lat:41.5, lon:-83.0, alt:0},
  'Bosphorus': {lat:41.0, lon:29.0, alt:0},
  'Amazon river mouth': {lat:-0.5, lon:-50.0, alt:0},
  'Daintree Rainforest': {lat:-16.2, lon:145.3, alt:0},
  'Greenwich': {lat:51.4, lon:0.0, alt:0},
  'Trans-Siberian railway': {lat:55.0, lon:90.0, alt:0},
  'Panama Canal locks': {lat:9.0, lon:-79.6, alt:0},
  'Himalayas — thorax/abdomen boundary of Asia/India': {lat:27.9, lon:86.5, alt:5000},
  'Sundarbans — Bengal delta mangrove': {lat:22.0, lon:89.5, alt:0},
  'Desert varnish, Mojave Desert': {lat:35.0, lon:-115.0, alt:0},
  'Transvaal Basin — single O₂-producing cyanobacterial mat province': {lat:-25.0, lon:27.0, alt:0},
  'Río Tinto, Spain': {lat:37.6, lon:-6.5, alt:0},
  'Ruhr industrial region': {lat:51.5, lon:7.3, alt:0},
  'West Siberian peat bog': {lat:60.0, lon:80.0, alt:0},
  'Strait of Gibraltar': {lat:36.0, lon:-5.5, alt:0},
  'Tibetan Plateau': {lat:32.0, lon:86.0, alt:4500},
  'Capsaicin highlands': {lat:17.0, lon:-92.0, alt:1500},
  'Great Barrier Reef — single largest living carbonate pH-buffer structure': {lat:-18.2, lon:147.7, alt:0},
  'Sahara': {lat:23.0, lon:0.0, alt:0},
  'Athabasca oil sands': {lat:57.0, lon:-111.5, alt:0},
  'Borneo — Southeast Asian palm-oil/fat-rich tropical landmass': {lat:1.0, lon:114.0, alt:0},
  'Oxford': {lat:51.75, lon:-1.25, alt:0},
  'Seoul': {lat:37.55, lon:126.99, alt:0},
  'Korean Peninsula': {lat:36.0, lon:128.0, alt:0},
  'Ganges': {lat:25.3, lon:83.0, alt:0},
  'Caribbean': {lat:15.0, lon:-75.0, alt:0},
};
const COSMIC = {
  'Antares': {ra:248.1, dec:-26.4, dist:550},
  'Horsehead Nebula': {ra:85.3, dec:-2.5, dist:1500},
  'Black Eye Galaxy': {ra:194.2, dec:21.7, dist:1.7e7},
  'Neutron star crust — degenerate matter, fractional crystallization, liquid→solid phases': {ra:0, dec:0, dist:0},
  'Rocky exoplanet mantle — silicate magma ocean; post-perovskite-like': {ra:0, dec:0, dist:0},
  'Magnetic cataclysmic variables — accreting white dwarfs with liquid-metal dynamos': {ra:0, dec:0, dist:0},
  'Planetesimal accretion bodies — concentric metal-silicate differentiation': {ra:0, dec:0, dist:0},
  'Enceladus — active subsurface ocean; evaporation/condensation/precipitation cycle; single ocean world': {ra:40.4, dec:-0.7, dist:8.5},
  'Lagoon Nebula — N-bearing H II region, molecular cloud with N emission': {ra:271.0, dec:-24.4, dist:4100},
  'Antennae Galaxies — major merger, streams, tidal tails': {ra:180.5, dec:-18.9, dist:4.5e7},
  'V Sge — interacting white dwarf binary with metal-rich accretion; CO emission, mass transfer': {ra:301.6, dec:33.5, dist:4400},
  'Gliese 229B — first CH₄ brown dwarf; gas collapse, H₂/He/CH₄ atmosphere; mass threshold': {ra:91.6, dec:-21.9, dist:18.8},
  'Pleiades — compact open cluster; young, UV-stressed stars; radiating / binding': {ra:56.6, dec:24.1, dist:445},
  'Large Magellanic Cloud — massive S-rich gas bridge, thicker paired cloud': {ra:80.9, dec:-69.8, dist:1.6e5},
  'Small Magellanic Cloud — metal-poor, thin, low-mass dwarf; peripheral': {ra:15.7, dec:-73.2, dist:2.0e5},
  'Andromeda Galaxy — massive spiral, edge-on observer, neutral matter': {ra:10.7, dec:41.3, dist:2.5e6},
  'Epoch of reionization — C II/O I phase transition in early universe; single global state toggle': {ra:0, dec:0, dist:1.3e10},
  'Tidal tail streams from galaxy merger — elongated suture of stars and gas': {ra:0, dec:0, dist:0},
  'Chi Cygni — S-type AGB star with carbon/sulfur transfer in circumstellar envelope': {ra:300.5, dec:32.4, dist:345},
  'Castor — sextuple hierarchical triple system; three-body branching around common center': {ra:113.6, dec:31.9, dist:51},
  'Meridiani Planum halite evaporite — single named Martian salt threshold/crystallization region': {ra:0, dec:0, dist:1.5e8},
  'HE 1523-0901 — old, metal-poor halo star with thorium/uranium actinide clock': {ra:231.0, dec:-9.3, dist:9.0e3},
  'GW170817 kilonova ejecta — r-process REE/Th/Pb-rich remnant (afterglow)': {ra:197.4, dec:-23.0, dist:1.3e8},
  'Vela Pulsar — rapidly rotating, multi-beam central engine; pulsar/quasar-like broadcast': {ra:128.8, dec:-45.2, dist:1000},
  'TW Hydrae protoplanetary disk — water-ice snow line; REE/radial sorting in single disk': {ra:165.4, dec:-34.7, dist:176},
  'Saturn\'s rings — flat, aligned dust/ice platelets in equatorial plane': {ra:0, dec:0, dist:8.8e8},
  'Supernova 1987A — neutrino burst; non-interactive, passed through matter; triggered deep recovery': {ra:83.8, dec:-69.3, dist:1.6e5},
  'Crab Nebula (M1) — supernova remnant with high-energy particle bursts; radiative stress front': {ra:83.6, dec:22.0, dist:6500},
  'Aurora on Jupiter — polar EM-field excitation; charged-particle spiral': {ra:0, dec:0, dist:4.2e8},
  'Fermi Bubbles — Milky Way outflow/fountain; gas leaving disk, returning later': {ra:0, dec:0, dist:0},
  'Sirius A — A-type star with sharp sodium-D doublet absorption': {ra:101.3, dec:-16.7, dist:8.6},
  'Algol (β Persei) — classic eclipsing binary; mass transfer via Roche-lobe overflow': {ra:49.1, dec:40.9, dist:92.8},
  'SS Cygni — accreting cataclysmic variable; disk eats donor, recycles matter': {ra:325.7, dec:43.6, dist:550},
  'Volcanic surface of Io — fresh basaltic ash, sulfur/Mn-rich': {ra:0, dec:0, dist:4.2e8},
  'Lunar highlands regolith — early space weathering, micro-meteorite spark': {ra:0, dec:0, dist:3.8e5},
  'Jupiter bands; layered cloud deck with pale upper / dark lower': {ra:0, dec:0, dist:4.2e8},
  'Galaxy cluster gravitational well — matter sinking into deep potential': {ra:0, dec:0, dist:0},
  'GW170817 — neutron-star merger / kilonova coalescence; final burst releasing jets and tidal ejecta': {ra:197.4, dec:-23.0, dist:1.3e8},
  'BPM 37093 (Lucy) — crystallized carbon-oxygen white dwarf; diamond core under pressure; pH/carbonate buffer': {ra:163.0, dec:-28.0, dist:53},
  'R Coronae Borealis — variable red/blue carbon star; dust-driven color changes': {ra:239.5, dec:37.9, dist:6000},
  'Crab Pulsar (PSR B0531+21) — rapid millisecond beams, glitching, precise timing': {ra:83.6, dec:22.0, dist:6500},
  'Magellanic Stream falling onto the Milky Way\'s dark-matter halo — mass accretion after infall': {ra:60, dec:-70, dist:1.6e5},
  'Ancient Martian duricrust / oxidized Fe-Al hardpan — planetary weathering cap': {ra:0, dec:0, dist:1.5e8},
  'Sun — CNO/pp-chain branching; carbon-skeleton/energy shunt in solar core': {ra:0, dec:0, dist:1.5e8},
  'Tycho\'s supernova remnant (SN 1572) — mixed Fe/Ni/Co/Cu ejecta; rapid nucleosynthesis': {ra:0.0, dec:63.9, dist:10000},
  '67P/Churyumov–Gerasimenko — chlorine-bearing comet, ion tail driven by solar wind': {ra:0, dec:0, dist:0},
  'Ganymede — subsurface ocean; water-laden, O₂-poor, layered ice shell with air-like inclusions': {ra:0, dec:0, dist:5.1e8},
  'M87 (Virgo A) — giant elliptical galaxy with kiloparsec-scale jet upwelling from deep core': {ra:187.7, dec:12.4, dist:5.4e7},
  'Crab Pulsar glitch/spin-up — discrete angular-momentum ratchet; stick-slip': {ra:83.6, dec:22.0, dist:6500},
  'Sagittarius B2 — CH₃OH maser / CH₃-rich ices; one-carbon methylation chemistry': {ra:266.4, dec:-28.9, dist:26000},
  'Hulse-Taylor binary (PSR B1913+16) — tight neutron-star pair spiraling together; gravitational bonding': {ra:288.8, dec:35.0, dist:21000},
  'Sloan Great Wall — large-scale structure wall; gravity-bound, folded matter': {ra:149.2, dec:2.3, dist:1.0e9},
  'Mira (Omicron Ceti) — AGB star with H/He/CNO burning shells; variable, O₂-cycle-like layers': {ra:34.8, dec:-2.9, dist:420},
  'WR 104 — Wolf-Rayet star with Fe-S wind; pinwheel spiral': {ra:264.0, dec:-43.8, dist:4600},
  'Tharsis — planetary-scale flood basalt province, Mars; single largest shield': {ra:0, dec:0, dist:1.5e8},
  'Galactic bulge — old, metal-rich, dynamically hot stellar population': {ra:266.4, dec:-29.0, dist:27000},
  'Canadian Shield — stable, exposed Precambrian cratonic platform; solid lithospheric base': {lat:55, lon:-100}, // placeholder mixed
  'Antarctic Ice Sheet — stable, high-mass, ground-contacting ice plateau': {lat:-85, lon:0, alt:2000},
  'Egg Nebula (CRL 2688) — post-AGB star ejecting fat-rich bipolar lobes; late-stage mass ejection': {ra:315.0, dec:42.4, dist:3000},
  'Europa — tidally stressed, salt-rich subsurface ocean; channel-like ice-shell cracks': {ra:0, dec:0, dist:4.2e8},
  'Meridiani Planum blueberries — Martian Mn⁴⁺ oxide concretions; single redox toggle': {ra:0, dec:0, dist:1.5e8},
  'Earth — the single known oxygen-rich, water-splitting planetary atmosphere': {ra:0, dec:0, dist:0},
  'Io\'s Pele volcano — active sulfur plume; volcanic haze; acid-iron cloud buffer': {ra:0, dec:0, dist:4.2e8},
  'Iron meteorites — Widmanstätten pattern; Fe-Ni alloy phase boundary': {ra:0, dec:0, dist:0},
  'Titan organic haze / tholins — reduced carbon-sulfur accumulation': {ra:0, dec:0, dist:8.9e8},
  'Cosmic filament / bridge between two clusters — baryonic bridge': {ra:0, dec:0, dist:0},
  'Boötes void — vast empty region; no observer, transparent, low interaction': {ra:219.5, dec:26.4, dist:7.0e8},
  'Pistol Star — massive, young, UV-bright; drives circumstellar dust shield/pigmentation': {ra:256.5, dec:-40.8, dist:26000},
  'SGR 1806-20 magnetar giant flare — fast, intense, high-energy pain-like burst': {ra:272.0, dec:-20.4, dist:50000},
  'Pinwheel Galaxy (M101) — coiled spiral-arm scaffold': {ra:210.8, dec:54.3, dist:2.1e7},
  'Mars seasonal CO₂ polar cap — frost/sublimation/adsorbed tristate; slow reversible dry cycle': {ra:0, dec:0, dist:1.5e8},
  'Veil Nebula — shock-excited filaments, ionized gas; π-like delocalization': {ra:311.4, dec:31.4, dist:2400},
  'Sunspot active region AR12192 — largest sunspot group of solar cycle 24; aligned fields trigger multiple X-class flares': {ra:0, dec:0, dist:1.5e8},
  'T Tauri (prototype in Taurus) — young, eruptive variable star; emotional instability': {ra:65.4, dec:19.8, dist:420},
  'Galactic center — dense star-forming hub; everything passes through': {ra:266.4, dec:-29.0, dist:26000},
  'TRAPPIST-1 planetary system — compact, tightly tuned habitable zone; multiple temperate orbits': {ra:346.6, dec:-5.0, dist:39},
  'Sagittarius A* — small, massive, controls galactic metabolism': {ra:266.4, dec:-29.0, dist:26000},
  'Perseus molecular cloud — dark, dense, star-formation reward broadcast': {ra:52.3, dec:31.3, dist:1000},
  'Magellanic Bridge — baryonic bridge connecting LMC and SMC': {ra:55, dec:-66, dist:1.6e5},
  'Heliosphere — Sun\'s continuous, low-interaction life-supporting plasma outflow': {ra:0, dec:0, dist:0},
  'Orion Nebula — fractal tree-like structure; coordinated star formation': {ra:83.8, dec:-5.4, dist:1344},
  'Crab Pulsar — sharp, precise repeated output': {ra:83.6, dec:22.0, dist:6500},
  'Cygnus A (3C 405) — powerful polar jet; fast collimated vertical outflow': {ra:299.9, dec:40.7, dist:7.6e8},
  'HH 1/2 (Orion) — prototype collimated one-sided bipolar jet; rhythmic outflow': {ra:83.8, dec:-5.4, dist:1300},
  'Milky Way disk-halo boundary — separating bulge/halo of a named galaxy': {ra:0, dec:0, dist:0},
  'Jupiter\'s main auroral oval — one-way Birkeland current tubes along polar field lines': {ra:0, dec:0, dist:4.2e8},
  'Venus — sulfuric acid cloud layer; global acid reservoir/chemical reactor': {ra:0, dec:0, dist:6.8e7},
};

function parseBodyCoord(s) {
  const m = s.match(/\(([\-\+\d\.]+)\s*,?\s*([\-\+\d\.]+)\s*,?\s*([\-\+\d\.]+)\)/);
  if (!m) return null;
  return { x: parseFloat(m[1]), y: parseFloat(m[2]), z: parseFloat(m[3]) };
}

function extractTable() {
  const re = /\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*)\s*\|/g;
  const rows = [];
  let m;
  const mapText = text.match(/# Loop-Vector Body–Cosmic–Earth Mapping[\s\S]*?## Branch-loop dictionary/)[0];
  while ((m = re.exec(mapText)) !== null) {
    const num = parseInt(m[1].trim());
    if (num >= 1 && num <= 84) {
      rows.push({
        num,
        bodyNode: m[2].trim(),
        bodyCoordRaw: m[3].trim(),
        loop: m[4].trim(),
        vectorShape: m[5].trim(),
        cosmic: m[6].trim(),
        geo: m[7].trim(),
        notes: m[8].trim()
      });
    }
  }
  return rows;
}

const rows = extractTable();

// Enrich with circuit84 data and coordinates
const mapping = rows.map(r => {
  const c = circuit84.find(n => n.num === r.num) || {};
  return {
    num: r.num,
    body: { name: r.bodyNode, coord: parseBodyCoord(r.bodyCoordRaw) || {x:0, y:0, z:0}, description: r.loop },
    cosmic: { name: r.cosmic, coord: COSMIC[r.cosmic] || {ra:0, dec:0, dist:0} },
    geo: { name: r.geo, coord: GEO[r.geo] || {lat:0, lon:0, alt:0} },
    route: c.route || 'Oxford',
    scale: '1mm', // default scale; user can override
    particle12: c.particle12 || '',
    dim: c.dim || 'g',
    notes: r.notes
  };
});

// Sort by num
mapping.sort((a,b)=>a.num-b.num);

fs.writeFileSync('body_cosmic_geo_map.json', JSON.stringify(mapping, null, 2));
console.log('Total mapped rows:', mapping.length);
console.log('First 3:', JSON.stringify(mapping.slice(0,3), null, 2));
