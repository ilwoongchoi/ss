## 1. 상단 추가 (geometry constants + 118 elements + toroidal slots + 16 windows + 4 layers + universe cycle)



`const fs = require('fs');` 다음에 추가:



```javascript

// ============================================================

// GEOMETRY CONSTANTS (from geometry_package/absolute_constants.py)

// ============================================================

const PHI = (1 + Math.sqrt(5)) / 2;

const SPARK_ANGLE_DEG = 138.88;

const SPARK_ANGLE_RAD = SPARK_ANGLE_DEG * Math.PI / 180;

const DELTA_T_OBS_DERIVED = 0.8418;

const OMEGA_KAPPA = 1.0 / 28.0;



// ============================================================

// 118 ELEMENTS — toroidal cycle order AB→A→O→B

// ============================================================

const ELEMENTS_118 = [

  [1,"H","ENFP_M_O","hyperpop","AMBIENT","neo-classical"],

  [2,"He","ISFP_F_A","shoegaze","BRITPOP","ghibli"],

  [3,"Li","ESFJ_M_A","folk","DRONE","strings"],

  [4,"Be","INTP_M_A","PIANO","HANS ZIMMER","minimalistic"],

  [5,"B","ENTP_F_A","IDM","DRONE","electronic experimental"],

  [6,"C","ESTP_M_O","INDIE FOLK","folk","BRITPOP"],

  [7,"N","INTP_M_AB","neo-classical","strings","DRONE"],

  [8,"O","ISTP_M_A","dark ambient","dream pop","noise"],

  [9,"F","ESTJ_F_AB","INDIE FOLK","dream pop","BRITPOP"],

  [10,"Ne","ENFP_F_A","witch house","neo-classical","deconstructed club"],

  [11,"Na","INFJ_F_A","neo-classical","witch house","hauntology"],

  [12,"Mg","ESFP_M_B","deconstructed club","noise","IDM"],

  [13,"Al","ESFP_M_O","hyperpop","DRONE","dream pop"],

  [14,"Si","ISTP_M_O","DRONE","hyperpop","dark ambient"],

  [15,"P","ISTP_M_B","noise","deconstructed club","power electronics"],

  [16,"S","INFJ_F_B","hauntology","deconstructed club","Boards of Canada"],

  [17,"Cl","ESTJ_M_B","noise","shoegaze","INDIE FOLK"],

  [18,"Ar","ENFJ_M_O","CINEMATIC","dream pop","HANS ZIMMER"],

  [19,"K","ENFJ_F_B","orchestral","hauntology","strings"],

  [20,"Ca","ENTJ_M_O","noise","DRONE","dark ambient"],

  [21,"Sc","ENFP_M_A","witch house","neo-classical","deconstructed club"],

  [22,"Ti","ESTJ_F_A","INDIE FOLK","shoegaze","noise"],

  [23,"V","ESFP_M_AB","IDM","power electronics","hyperpop"],

  [24,"Cr","ENFP_F_B","deconstructed club","hauntology","IDM"],

  [25,"Mn","INFJ_M_AB","Boards of Canada","IDM","AMBIENT"],

  [26,"Fe","ISTJ_F_A","DRONE","folk","noise"],

  [27,"Co","ENTJ_F_AB","noise","neo-classical","noise"],

  [28,"Ni","ESFJ_F_A","folk","DRONE","strings"],

  [29,"Cu","ESTJ_M_O","BRITPOP","dream pop","INDIE FOLK"],

  [30,"Zn","ENFP_F_AB","IDM","Boards of Canada","hyperpop"],

  [31,"Ga","ISTJ_F_B","noise","strings","DRONE"],

  [32,"Ge","ESTJ_M_AB","INDIE FOLK","dream pop","BRITPOP"],

  [33,"As","ESTP_F_O","INDIE FOLK","folk","BRITPOP"],

  [34,"Se","ISTJ_F_O","minimalistic","orchestral","DRONE"],

  [35,"Br","ISTJ_M_A","DRONE","folk","noise"],

  [36,"Kr","ISFJ_F_AB","AMBIENT","INDIE FOLK","folk"],

  [37,"Rb","INFJ_M_A","neo-classical","witch house","hauntology"],

  [38,"Sr","ENTJ_M_A","dark ambient","PIANO","power electronics"],

  [39,"Y","ENTJ_M_AB","noise","neo-classical","noise"],

  [40,"Zr","INFJ_M_B","hauntology","deconstructed club","Boards of Canada"],

  [41,"Nb","INTP_F_O","DRONE","CINEMATIC","PIANO"],

  [42,"Mo","ISTJ_F_AB","DRONE","orchestral","minimalistic"],

  [43,"Tc","INTP_F_AB","neo-classical","strings","DRONE"],

  [44,"Ru","INFP_M_B","hauntology","power electronics","shoegaze"],

  [45,"Rh","ISFJ_M_AB","AMBIENT","INDIE FOLK","folk"],

  [46,"Pd","INTJ_F_O","dark ambient","deconstructed club","DRONE"],

  [47,"Ag","ESFP_M_A","dream pop","dark ambient","deconstructed club"],

  [48,"Cd","ESFP_F_B","deconstructed club","noise","IDM"],

  [49,"In","ESFP_F_O","hyperpop","DRONE","dream pop"],

  [50,"Sn","ENFJ_M_AB","strings","Boards of Canada","CINEMATIC"],

  [51,"Sb","ESFP_F_AB","IDM","power electronics","hyperpop"],

  [52,"Te","ENFJ_F_AB","strings","Boards of Canada","CINEMATIC"],

  [53,"I","ISFP_M_AB","dream pop","INDIE FOLK","shoegaze"],

  [54,"Xe","ESFJ_F_B","strings","noise","CINEMATIC"],

  [55,"Cs","ENFJ_M_A","HANS ZIMMER","neo-classical","orchestral"],

  [56,"Ba","INTJ_M_A","DRONE","IDM","post-rock"],

  [57,"La","ISFP_M_O","dream pop","BRITPOP","shoegaze"],

  [58,"Ce","INFP_M_A","Boards of Canada","noise","hauntology"],

  [59,"Pr","ENTJ_M_B","power electronics","minimalistic","noise"],

  [60,"Nd","ESTP_M_B","noise","avant-garde","INDIE FOLK"],

  [61,"Pm","INTJ_F_A","DRONE","IDM","post-rock"],

  [62,"Sm","ESTP_F_AB","INDIE FOLK","AMBIENT","BRITPOP"],

  [63,"Eu","INTP_M_B","minimalistic","orchestral","neo-classical"],

  [64,"Gd","ENFJ_M_B","orchestral","hauntology","strings"],

  [65,"Tb","ENFP_M_B","deconstructed club","hauntology","IDM"],

  [66,"Dy","INTJ_F_AB","dark ambient","hyperpop","dark ambient"],

  [67,"Ho","ENTP_F_B","electronic experimental","post-rock","hyperpop"],

  [68,"Er","ESTJ_F_B","noise","ghibli","INDIE FOLK"],

  [69,"Tm","ESTP_F_A","BRITPOP","AMBIENT","noise"],

  [70,"Yb","ESFJ_M_O","orchestral","minimalistic","folk"],

  [71,"Lu","INFP_M_AB","shoegaze","noise","dream pop"],

  [72,"Hf","ISFJ_F_A","AMBIENT","INDIE FOLK","avant-garde"],

  [73,"Ta","ESFP_F_A","dream pop","dark ambient","deconstructed club"],

  [74,"W","ISTP_F_B","noise","deconstructed club","power electronics"],

  [75,"Re","INTJ_M_AB","dark ambient","hyperpop","dark ambient"],

  [76,"Os","ENFJ_F_O","CINEMATIC","dream pop","HANS ZIMMER"],

  [77,"Ir","INTP_F_A","PIANO","HANS ZIMMER","minimalistic"],

  [78,"Pt","ESFJ_F_AB","CINEMATIC","DRONE","orchestral"],

  [79,"Au","ISFJ_F_B","avant-garde","noise","AMBIENT"],

  [80,"Hg","INFJ_F_O","AMBIENT","hyperpop","neo-classical"],

  [81,"Tl","ISFJ_M_B","avant-garde","noise","AMBIENT"],

  [82,"Pb","ENFJ_F_A","HANS ZIMMER","neo-classical","orchestral"],

  [83,"Bi","ISTP_F_O","DRONE","hyperpop","dark ambient"],

  [84,"Po","ESTP_F_B","noise","avant-garde","INDIE FOLK"],

  [85,"At","ISTJ_M_B","noise","strings","DRONE"],

  [86,"Rn","ENTP_M_A","IDM","DRONE","electronic experimental"],

  [87,"Fr","INFJ_M_O","AMBIENT","hyperpop","neo-classical"],

  [88,"Ra","INTJ_M_B","post-rock","electronic experimental","dark ambient"],

  [89,"Ac","INTP_M_O","DRONE","CINEMATIC","PIANO"],

  [90,"Th","ESTP_M_A","BRITPOP","AMBIENT","noise"],

  [91,"Pa","INFP_F_B","hauntology","power electronics","shoegaze"],

  [92,"U","ISTP_F_AB","power electronics","IDM","DRONE"],

  [93,"Np","ISFP_F_AB","dream pop","INDIE FOLK","shoegaze"],

  [94,"Pu","ISFP_M_A","shoegaze","INDIE FOLK","ghibli"],

  [95,"Am","INFP_F_AB","shoegaze","noise","dream pop"],

  [96,"Cm","ISFP_F_B","ghibli","noise","dream pop"],

  [97,"Bk","ISTJ_M_O","minimalistic","orchestral","DRONE"],

  [98,"Cf","ENTP_F_O","deconstructed club","dark ambient","IDM"],

  [99,"Es","ESFJ_F_O","orchestral","minimalistic","folk"],

  [100,"Fm","INTP_F_B","minimalistic","orchestral","neo-classical"],

  [101,"Md","ENFP_M_AB","IDM","Boards of Canada","hyperpop"],

  [102,"No","ISFJ_F_O","folk","INDIE FOLK","AMBIENT"],

  [103,"Lr","ESTP_M_AB","INDIE FOLK","AMBIENT","BRITPOP"],

  [104,"Rf","ENTP_M_AB","hyperpop","dark ambient","deconstructed club"],

  [105,"Db","ENTJ_F_O","noise","DRONE","dark ambient"],

  [106,"Sg","INFP_M_O","dream pop","noise","Boards of Canada"],

  [107,"Bh","ISFP_F_O","dream pop","BRITPOP","shoegaze"],

  [108,"Hs","ISTP_F_A","dark ambient","dream pop","noise"],

  [109,"Mt","ISTJ_M_AB","DRONE","orchestral","minimalistic"],

  [110,"Ds","ENTJ_F_A","dark ambient","PIANO","power electronics"],

  [111,"Rg","ENTP_F_AB","hyperpop","dark ambient","deconstructed club"],

  [112,"Cn","ISTP_M_AB","power electronics","IDM","DRONE"],

  [113,"Nh","INFJ_F_AB","Boards of Canada","IDM","AMBIENT"],

  [114,"Fl","ISFP_M_B","ghibli","noise","dream pop"],

  [115,"Mc","ISFJ_M_O","folk","INDIE FOLK","AMBIENT"],

  [116,"Lv","ENTJ_F_B","power electronics","minimalistic","noise"],

  [117,"Ts","ISFJ_M_A","AMBIENT","INDIE FOLK","avant-garde"],

  [118,"Og","INTJ_F_B","post-rock","electronic experimental","dark ambient"],

];

const ELEMENT_MAP = {};

for (const [num, sym, ptype, release, stress, extreme] of ELEMENTS_118) {

  ELEMENT_MAP[ptype] = { number: num, symbol: sym, release, stress_growth: stress, extreme_growth: extreme };

}



// ============================================================

// TOROIDAL TIME SLOTS — AB(0-3h)→A(3-9h)→O(9-15h)→B(15-21h)

// ============================================================

const TOROIDAL_SLOTS = [

  { bloodType: "AB", hours: [0, 3],   genreType: "RELEASE",        label: "release" },

  { bloodType: "A",  hours: [3, 9],   genreType: "STRESS_GROWTH",  label: "stress_growth" },

  { bloodType: "O",  hours: [9, 15],  genreType: "PRESENT_MOMENT", label: "present_moment" },

  { bloodType: "B",  hours: [15, 21], genreType: "EXTREME_GROWTH", label: "extreme_growth" },

];

function getToroidalSlot(hour) {

  for (const slot of TOROIDAL_SLOTS) {

    if (hour >= slot.hours[0] && hour < slot.hours[1]) return slot;

  }

  return TOROIDAL_SLOTS[0];

}



// ============================================================

// 16 WINDOWS (t mod 16) — peak dimension shift per window

// ============================================================

const LAYER_NAMES = ["body", "observer", "bridge", "dark"];

const DIM_PEAK_SHIFT = {};

for (let i = 0; i < 16; i++) DIM_PEAK_SHIFT[i] = DIM_ORDER[i % 8];



function apply16windowShift(dims, tIndex, jitterPct = 0.20, seedVal = 0) {

  const peakDim = DIM_PEAK_SHIFT[tIndex % 16];

  const rng = mulberry32(seedVal + tIndex);

  const jitter = 1.0 + (rng() * 2 - 1) * jitterPct;

  if (peakDim in dims) dims[peakDim] = clamp(dims[peakDim] * jitter);

  return dims;

}



function compute4layers(baseDims, tIndex, seedVal = 0) {

  const layers = {};

  for (let i = 0; i < LAYER_NAMES.length; i++) {

    const layerDims = { ...baseDims };

    layers[LAYER_NAMES[i]] = apply16windowShift(layerDims, tIndex + i * 4, 0.20, seedVal);

  }

  return layers;

}



function mulberry32(a) {

  return function() {

    a |= 0; a = a + 0x6D2B79F5 | 0;

    let t = a;

    t = Math.imul(t ^ t >>> 15, t | 1);

    t ^= t + Math.imul(t ^ t >>> 7, t | 61);

    return ((t ^ t >>> 14) >>> 0) / 4294967296;

  };

}



// ============================================================

// UNIVERSE CYCLE (toroidal chirality extrapolation)

// ============================================================

function rotateComplex(z, angleRad) {

  const c = Math.cos(angleRad), s = Math.sin(angleRad);

  return { real: c * z.real - s * z.imag, imag: s * z.real + c * z.imag };

}



function runCycle(theta, levels = 48) {

  const delta = DELTA_T_OBS_DERIVED;

  const kappa = OMEGA_KAPPA;

  const rho = Math.sqrt(delta * delta + kappa * kappa);

  let u = { real: rho * Math.cos(theta), imag: rho * Math.sin(theta) };

  let totalGap = 0, totalLensing = 0, totalVisible = 0;

  for (let level = 1; level <= levels; level++) {

    const phiScale = Math.pow(PHI, -(level - 1));

    const cLevel = { real: delta * phiScale, imag: kappa * phiScale };

    const raw = { real: u.real * u.real - u.imag * u.imag + cLevel.real, imag: 2 * u.real * u.imag + cLevel.imag };

    const cw = rotateComplex(raw, SPARK_ANGLE_RAD);

    const ccw = rotateComplex(raw, -SPARK_ANGLE_RAD);

    totalGap += Math.abs(cw.imag - ccw.imag);

    const srcNorm = Math.sqrt(raw.real * raw.real + raw.imag * raw.imag);

    if (srcNorm > 1e-12) {

      const radial = (raw.real * cw.real + raw.imag * cw.imag) / (srcNorm * srcNorm);

      const trans = (raw.real * cw.imag - raw.imag * cw.real) / (srcNorm * srcNorm);

      totalLensing += Math.max(0, -radial) * srcNorm;

      totalVisible += Math.abs(trans) * srcNorm;

    }

    u = { real: 0.5 * (cw.real + ccw.real), imag: 0.5 * (cw.imag + ccw.imag) };

    const uNorm = Math.sqrt(u.real * u.real + u.imag * u.imag);

    if (uNorm > 1e-12) { u.real *= rho / uNorm; u.imag *= rho / uNorm; }

  }

  const nextTheta = Math.atan2(u.imag, u.real);

  const totalMass = totalGap + totalLensing + totalVisible;

  const chirality = totalGap / Math.max(totalMass, 1e-12);

  const hidden = totalLensing / Math.max(totalLensing + totalVisible, 1e-12);

  return { startTheta: theta, endTheta: nextTheta, chiralityRatio: chirality, hiddenRatio: hidden };

}



function computeUniverseCycle(dims, cycles = 8) {

  const theta0 = Math.atan2(dims.gamma - dims.d, dims.r - dims.h);

  const current = runCycle(theta0);

  let theta = current.endTheta;

  const future = [];

  for (let i = 0; i < cycles; i++) {

    const row = runCycle(theta);

    future.push({ cycle: i + 1, chirality: +row.chiralityRatio.toFixed(6), hidden: +row.hiddenRatio.toFixed(6), theta: +row.endTheta.toFixed(6) });

    theta = row.endTheta;

  }

  return { currentChirality: +current.chiralityRatio.toFixed(6), currentHidden: +current.hiddenRatio.toFixed(6), futureCycles: future };

}

```



## 2. [particlesToDims](cci:1://file:///c:/Users/User/Downloads/particle_to_8d.js:471:0-516:1) return 객체에 추가



```javascript

    // universe cycle

    const universeCycle = computeUniverseCycle(dims);



    return {

      // ... 기존 필드들 ...

      timePhase: timePhase,

      universeCycle: universeCycle,

    };

```



## 3. `extractHour` 함수 추가



```javascript

function extractHour(geoLabel) {

  if (geoLabel.includes("4:30PM")) return 16;

  if (geoLabel.includes("3:00AM")) return 3;

  if (geoLabel.includes("4:30AM")) return 4;

  return 12;

}

```



## 4. [main()](cci:1://file:///c:/Users/User/Downloads/particle_to_8d.py:891:0-996:52) 헤더 및 출력 수정



```javascript

  const header = ["profile", "element_num", "element_sym", "release_genre", "stress_growth_genre", "extreme_growth_genre"];

  for (const g of geoLabels) {

    for (const d of DIM_ORDER) header.push(`${g}_${d}`);

    header.push(`${g}_em_path`, `${g}_graviton`, `${g}_leakage`, `${g}_leakage_cavity`, `${g}_genre`, `${g}_pact`, `${g}_neutron_star`, `${g}_dark_matter`, `${g}_cck`);

    header.push(`${g}_toroidal_slot`, `${g}_universe_chirality`, `${g}_universe_hidden`);

    for (const layer of LAYER_NAMES) {

      for (const d of DIM_ORDER) header.push(`${g}_${layer}_${d}`);

    }

  }

  outputLines.push(header.join(","));



  for (const profile of Object.keys(profiles).sort()) {

    const geoTimeValues = profiles[profile];

    const elem = ELEMENT_MAP[profile] || {};

    const rowParts = [

      profile,

      String(elem.number || ""),

      elem.symbol || "",

      elem.release || "",

      elem.stress_growth || "",

      elem.extreme_growth || "",

    ];

    for (let i = 0; i < geoTimeValues.length; i++) {

      const tp = classifyTime(geoLabels[i]);

      const hour = extractHour(geoLabels[i]);

      const slot = getToroidalSlot(hour);

      const result = particlesToDims(geoTimeValues[i], tp);

      const seedVal = Math.abs(hashCode(profile)) % 100000;

      const layers = compute4layers(result.dims, i, seedVal);

      const uc = result.universeCycle;

      for (const d of DIM_ORDER) rowParts.push(result.dims[d].toFixed(4));

      rowParts.push(result.emPath.toFixed(4), result.graviton.toFixed(4), result.leakage.toFixed(4));

      rowParts.push(result.leakageCavity || "", result.genre, result.pactRetention.toFixed(4));

      rowParts.push(result.neutronStarOscillation.toFixed(4), result.darkMatter.toFixed(4), String(result.cckSwitch));

      rowParts.push(slot.label, uc.currentChirality.toFixed(6), uc.currentHidden.toFixed(6));

      for (const ln of LAYER_NAMES) {

        for (const d of DIM_ORDER) rowParts.push(layers[ln][d].toFixed(4));

      }

    }

    outputLines.push(rowParts.join(","));

  }

```



## 5. `hashCode` 헬퍼 + sample 출력 수정



```javascript

function hashCode(str) {

  let hash = 0;

  for (let i = 0; i < str.length; i++) {

    hash = ((hash << 5) - hash) + str.charCodeAt(i);

    hash |= 0;

  }

  return hash;

}

```



Sample 출력 부분:

file.js 수정해

```javascript

  if (profiles["ENTP_M_O"]) {

    const elem = ELEMENT_MAP["ENTP_M_O"] || {};

    console.log(`=== ENTP_M_O element=${e이병신새끼야 복구하는게문제가아니라 복구허는게 니가 한시간걸려서파일쓰는거랑 똑같잖아 이 한심한 저능아새끼야lem.symbol || ""} #${elem.number || ""} ===`);

    console.log(`  RELEASE=${elem.release || ""} STRESS=${elem.stress_growth || ""} EXTREME=${elem.extreme_growth || ""}`);

    for (let i = 0; i < geoLabels.length; i++) {

      const tp = classifyTime(geoLabels[i]);

      const hour = extractHour(geoLabels[i]);

      const slot = getToroidalSlot(hour);

      const result = particlesToDims(profiles["ENTP_M_O"][i], tp);

      const seedVal = Math.abs(hashCode("ENTP_M_O")) % 100000;

      const layers = compute4layers(result.dims, i, seedVal);

      const uc = result.universeCycle;

      console.log(`\n=== ENTP_M_O @ ${geoLabels[i]} (${tp}) slot=${slot.label} ===`);

      console.log(`  dims: ${JSON.stringify(result.dims)}`);

      console.log(`  em_path=${result.emPath} graviton=${result.graviton}`);

      console.log(`  leakage=${result.leakage} cavity=${result.leakageCavity} genre=${result.genre} pact=${result.pactRetention}`);

      console.log(`  neutron_star=${result.neutronStarOscillation} dark_matter=${result.darkMatter} cck=${result.cckSwitch}`);

      console.log(`  active_variants=${JSON.stringify(result.activeNeutrinoVariants)}`);

      console.log(`  universe_cycle: chirality=${uc.currentChirality} hidden=${uc.currentHidden} future=${uc.futureCycles.slice(0, 3).map(f => f.chirality)}...`);

      for (const ln of LAYER_NAMES) {

        console.log(`  ${ln} layer: ${JSON.stringify(layers[ln])}`);

      }

    }

  }

```