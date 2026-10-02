// ============================================
// TOROIDAL MUSIC PROGRAM — No labels, sound only
// 4 calibration rounds × 8 tiles, pick 1 per round
// ============================================

// --- 8D base vectors per MBTI (internal, never shown) ---
const MBTI_VECTORS = {
  ENFJ:{r:0.3,h:0.8,d:0.2,p:0.5,s:0.3,gamma:0.7,g:0.8,nu:0.3},
  INFJ:{r:0.2,h:0.8,d:0.2,p:0.7,s:0.2,gamma:0.5,g:0.4,nu:0.7},
  INFP:{r:0.4,h:0.7,d:0.2,p:0.4,s:0.3,gamma:0.6,g:0.3,nu:0.6},
  INTJ:{r:0.2,h:0.7,d:0.4,p:0.7,s:0.2,gamma:0.4,g:0.4,nu:0.6},
  ENFP:{r:0.8,h:0.4,d:0.2,p:0.4,s:0.8,gamma:0.4,g:0.2,nu:0.6},
  ESFP:{r:0.8,h:0.3,d:0.2,p:0.3,s:0.8,gamma:0.7,g:0.5,nu:0.3},
  ESTP:{r:0.8,h:0.2,d:0.7,p:0.3,s:0.7,gamma:0.5,g:0.3,nu:0.2},
  ENTJ:{r:0.4,h:0.2,d:0.7,p:0.4,s:0.3,gamma:0.6,g:0.7,nu:0.2},
  ESTJ:{r:0.4,h:0.2,d:0.7,p:0.7,s:0.3,gamma:0.4,g:0.8,nu:0.2},
  ENTP:{r:0.7,h:0.2,d:0.4,p:0.4,s:0.7,gamma:0.4,g:0.2,nu:0.5},
  INTP:{r:0.2,h:0.6,d:0.2,p:0.8,s:0.2,gamma:0.3,g:0.4,nu:0.8},
  ISTP:{r:0.2,h:0.2,d:0.7,p:0.7,s:0.2,gamma:0.3,g:0.3,nu:0.6},
  ISFP:{r:0.4,h:0.7,d:0.2,p:0.3,s:0.5,gamma:0.7,g:0.2,nu:0.5},
  ISFJ:{r:0.2,h:0.5,d:0.2,p:0.7,s:0.3,gamma:0.6,g:0.6,nu:0.3},
  ISTJ:{r:0.3,h:0.2,d:0.6,p:0.8,s:0.2,gamma:0.3,g:0.7,nu:0.2},
  ESFJ:{r:0.4,h:0.6,d:0.2,p:0.4,s:0.3,gamma:0.6,g:0.7,nu:0.3}
};

const MBTI_OPPOSITE = {
  ENFJ:'ISFP',INFJ:'ENFP',INFP:'ENFJ',INTJ:'ENTP',ENFP:'INFJ',ESFP:'ISFJ',
  ESTP:'ESFJ',ENTJ:'INTP',ESTJ:'ISFP',ENTP:'INTJ',INTP:'ENTJ',ISTP:'ESFP',
  ISFP:'ESTJ',ISFJ:'ESFP',ISTJ:'ESFJ',ESFJ:'ISTJ'
};

// --- Web Audio API + Soundfont ---
let audioCtx = null;
let masterGain = null;
let reverbNode = null;
let reverbGain = null;
let activeInstruments = {};
let instrumentsLoaded = false;
let instrumentLoadPromise = null;
let activePlayers = [];
let activeNodes = [];
let reverbBuffer = null;

// Instrument sets selected by 8D parameters
// Each set = { chord, bass, lead, counter, percussion }
const INSTRUMENT_SETS = {
  // Bright + spacious (high s, high gamma) — cinematic/orchestral
  cinematic: {
    chord: 'string_ensemble_1',
    bass: 'contrabass',
    lead: 'flute',
    counter: 'violin',
    bright: 'tubular_bells'
  },
  // Bright + rhythmic (high s, high r) — pop/EDM
  pop: {
    chord: 'electric_piano_1',
    bass: 'electric_bass_finger',
    lead: 'lead_2_sawtooth',
    counter: 'synth_brass_1',
    bright: 'glockenspiel'
  },
  // Dark + spacious (low s, high gamma) — ambient/neo-classical
  ambient: {
    chord: 'pad_2_warm',
    bass: 'acoustic_bass',
    lead: 'cello',
    counter: 'oboe',
    bright: 'music_box'
  },
  // Dark + rhythmic (low s, high r) — rock/garage
  rock: {
    chord: 'overdriven_guitar',
    bass: 'electric_bass_pick',
    lead: 'distortion_guitar',
    counter: 'electric_guitar_muted',
    bright: 'steel_drums'
  },
  // Mid everything — jazz/soul
  jazz: {
    chord: 'acoustic_grand_piano',
    bass: 'acoustic_bass',
    lead: 'soprano_sax',
    counter: 'trumpet',
    bright: 'vibraphone'
  },
  // Very dark (high d) — dark ambient/experimental
  dark: {
    chord: 'pad_4_choir',
    bass: 'synth_bass_1',
    lead: 'bassoon',
    counter: 'french_horn',
    bright: 'fx_3_crystal'
  },
  // Very bright + extreme (very high s) — hyperpop/hyperactive
  hyper: {
    chord: 'lead_1_square',
    bass: 'synth_bass_2',
    lead: 'lead_6_voice',
    counter: 'synth_brass_2',
    bright: 'tinkle_bell'
  },
  // Acoustic/folk (mid s, mid gamma, low r) — folk/acoustic
  folk: {
    chord: 'acoustic_guitar_nylon',
    bass: 'acoustic_bass',
    lead: 'acoustic_guitar_steel',
    counter: 'viola',
    bright: 'kalimba'
  }
};

// All instruments we need to load
const ALL_INSTRUMENTS = new Set();
Object.values(INSTRUMENT_SETS).forEach(set => {
  Object.values(set).forEach(name => ALL_INSTRUMENTS.add(name));
});
// Add drums separately — we'll use synth drums for now since soundfont drums are kit-based

function initAudio() {
  if (audioCtx) {
    if (audioCtx.state === 'suspended') audioCtx.resume();
    return;
  }
  audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  masterGain = audioCtx.createGain();
  masterGain.gain.value = 0.7;
  masterGain.connect(audioCtx.destination);

  // Reverb
  reverbBuffer = makeReverbBuffer(audioCtx, 2.5, 2.0);
  reverbNode = audioCtx.createConvolver();
  reverbNode.buffer = reverbBuffer;
  reverbGain = audioCtx.createGain();
  reverbGain.gain.value = 0.3;
  reverbNode.connect(reverbGain);
  reverbGain.connect(masterGain);

  // Start loading instruments
  loadInstruments();
}

function loadInstruments() {
  if (instrumentLoadPromise) return instrumentLoadPromise;
  instrumentLoadPromise = Promise.resolve();
  return instrumentLoadPromise;
}

// Lazy-load a single instrument by name
function loadInstrument(name) {
  if (activeInstruments[name]) return Promise.resolve(activeInstruments[name]);
  if (typeof Soundfont === 'undefined') return Promise.reject('no Soundfont');

  return Soundfont.instrument(audioCtx, name, { soundfont: 'MusyngKite' }).then(player => {
    activeInstruments[name] = player;
    return player;
  });
}

// Load all instruments for a given instrument set
function loadInstrumentSet(instSet) {
  const names = Object.values(instSet);
  return Promise.all(names.map(n => loadInstrument(n).catch(() => null)));
}

function makeReverbBuffer(ctx, seconds, decay) {
  const rate = ctx.sampleRate;
  const len = rate * seconds;
  const buf = ctx.createBuffer(2, len, rate);
  for (let ch = 0; ch < 2; ch++) {
    const data = buf.getChannelData(ch);
    for (let i = 0; i < len; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, decay);
    }
  }
  return buf;
}

function stopAllSound() {
  // Stop all soundfont players
  activePlayers.forEach(p => {
    try { p.stop(); } catch(e) {}
  });
  activePlayers = [];

  // Stop any synth nodes (drums etc)
  activeNodes.forEach(n => {
    try { n.stop(); } catch(e) {}
    try { n.disconnect(); } catch(e) {}
  });
  activeNodes = [];
}

// --- Select instrument set from 8D parameters ---
function pickInstrumentSet(v) {
  // Very dark
  if (v.d > 0.78) return INSTRUMENT_SETS.dark;
  // Very bright + extreme
  if (v.s > 0.8 && v.r > 0.6) return INSTRUMENT_SETS.hyper;
  // Bright + spacious
  if (v.s > 0.6 && v.gamma > 0.5) return INSTRUMENT_SETS.cinematic;
  // Bright + rhythmic
  if (v.s > 0.6 && v.r > 0.5) return INSTRUMENT_SETS.pop;
  // Dark + spacious
  if (v.s < 0.4 && v.gamma > 0.4) return INSTRUMENT_SETS.ambient;
  // Dark + rhythmic
  if (v.s < 0.4 && v.r > 0.4) return INSTRUMENT_SETS.rock;
  // Acoustic/folk (mid, low energy)
  if (v.r < 0.4 && v.s > 0.3 && v.s < 0.6) return INSTRUMENT_SETS.folk;
  // Default: jazz/soul (mid everything)
  return INSTRUMENT_SETS.jazz;
}

// --- Play a soundfont note ---
function playNote(midi, time, dur, gain, instrumentName, reverbAmount) {
  if (!activeInstruments[instrumentName]) return;
  const player = activeInstruments[instrumentName];
  const opts = {
    gain: gain,
    duration: dur,
    attack: 0.01,
    release: 0.1
  };
  const node = player.start(midi, time, opts);
  if (node) {
    activePlayers.push(player);
    // Send to reverb
    if (reverbAmount > 0.05 && reverbNode) {
      try {
        const sendGain = audioCtx.createGain();
        sendGain.gain.value = reverbAmount;
        node.connect(sendGain);
        sendGain.connect(reverbNode);
        activeNodes.push(sendGain);
      } catch(e) {}
    }
  }
}

// --- Play chord (multiple notes at once) ---
function playChord(midiNotes, time, dur, gain, instrumentName, reverbAmount) {
  midiNotes.forEach(midi => {
    playNote(midi, time, dur, gain, instrumentName, reverbAmount);
  });
}

// --- Modes (brightness spectrum: Lydian→Locrian = toroidal cycle) ---
const MODES = {
  lydian:      [0, 2, 4, 6, 7, 9, 11],   // brightest — AB Discharge
  ionian:      [0, 2, 4, 5, 7, 9, 11],   // major — A Accumulate
  mixolydian:  [0, 2, 4, 5, 7, 9, 10],   // b7 — A→O transition
  dorian:      [0, 2, 3, 5, 7, 9, 10],   // minor hopeful — O Accumulate
  aeolian:     [0, 2, 3, 5, 7, 8, 10],   // natural minor — B Compress
  phrygian:    [0, 1, 3, 5, 7, 8, 10],   // dark exotic — B→AB transition
  locrian:     [0, 1, 3, 5, 6, 8, 10],   // darkest — AB Integrate
  harmonicMin: [0, 2, 3, 5, 7, 8, 11],   // tension — cadential minor
  chromatic:   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  // entropy — 3AM RANDOM
};

// d → mode selection (toroidal phase position)
function pickMode(d) {
  if (d < 0.12) return MODES.lydian;
  if (d < 0.25) return MODES.ionian;
  if (d < 0.40) return MODES.mixolydian;
  if (d < 0.55) return MODES.dorian;
  if (d < 0.70) return MODES.aeolian;
  if (d < 0.83) return MODES.phrygian;
  if (d < 0.93) return MODES.locrian;
  return MODES.chromatic;
}

// --- Chord types by harmony complexity (h = leakage rate) ---
function pickChordType(h) {
  if (h < 0.20) return [0, 7];                    // power chord — AB ignition
  if (h < 0.35) return [0, 4, 7];                 // major/minor triad — A structure
  if (h < 0.50) return [0, 4, 7, 9];              // 6th chord — A→O color
  if (h < 0.65) return [0, 4, 7, 10];             // 7th chord — O richness
  if (h < 0.78) return [0, 4, 7, 10, 14];         // 9th chord — B density
  if (h < 0.90) return [0, 4, 7, 10, 14, 17];     // 11th chord — B→AB
  return [0, 2, 4, 7, 10, 14, 17];                // cluster — AB entropy
}

// --- Chord progressions (toroidal cycle mappings) ---
// Each progression = a toroidal energy path
const PROGRESSIONS = {
  // I-IV-V-I = complete toroidal cycle (AB→A→B→AB)
  cycle:       [0, 3, 4, 0],
  // I-V-vi-IV = asymmetric loop (never resolves = pop anthem)
  popAnthem:   [0, 4, 5, 3],
  // I-vi-IV-V = circle of fifths segment (A→O→A→B)
  circleFifths:[0, 5, 3, 4],
  // i-iv-V-i = minor cycle (B Compress version)
  minorCycle:  [0, 3, 4, 0],
  // I-♭VII-♭VI-V = phrygian/dorian descent (B→AB compression)
  descending:  [0, 6, 5, 4],
  // i-♭VI-♭VII-i = aeolian loop (B Compress hold)
  aeolianLoop: [0, 5, 6, 0],
  // I-II-vi-IV = lydian/mixolydian brightness (AB Discharge)
  bright:      [0, 1, 5, 3],
  // random degrees for p↓ (free improv / Layer D)
  free:        null
};

function pickProgression(p, g) {
  if (p < 0.2) return PROGRESSIONS.free;        // free improv
  if (p < 0.4) return PROGRESSIONS.descending;  // semi-structured
  if (p < 0.6) return PROGRESSIONS.popAnthem;   // pop
  if (p < 0.75) return PROGRESSIONS.circleFifths;
  if (p < 0.9) return PROGRESSIONS.cycle;       // classical
  return PROGRESSIONS.cycle;                     // strict
}

// --- Cadence types (phase transitions) ---
// Perfect (V→I) = B→AB full discharge
// Plagal (IV→I) = A→AB gentle return
// Deceptive (V→vi) = B→O bilirubin bypass
// Half (→V) = arrive at B, hold tension
function getCadence(barIdx, totalBars, prog, p) {
  const isLastBar = (barIdx === totalBars - 1);
  if (!isLastBar) return null;
  
  // High p = perfect cadence (strict resolution)
  // Medium p = plagal (gentle)
  // Low p = deceptive or half (unresolved)
  if (p > 0.7) return { type: 'perfect', from: 4, to: 0 };
  if (p > 0.4) return { type: 'plagal', from: 3, to: 0 };
  if (p > 0.2) return { type: 'deceptive', from: 4, to: 5 };
  return { type: 'half', from: prog[barIdx % prog.length], to: 4 };
}

// --- Voice leading: minimize movement between chords ---
function voiceLead(prevChord, newChordRoot, chordIntervals, scale, octave) {
  if (!prevChord || prevChord.length === 0) {
    // First chord — root position
    return chordIntervals.map(iv => newChordRoot + iv + octave * 12);
  }
  
  // Find closest inversion by minimizing total semitone movement
  const inversions = [
    chordIntervals.map(iv => newChordRoot + iv + octave * 12),           // root position
    chordIntervals.map((iv, i) => newChordRoot + iv + (i >= chordIntervals.length - 1 ? -12 : 0) + octave * 12), // 1st inv
    chordIntervals.map((iv, i) => newChordRoot + iv + (i >= chordIntervals.length - 2 ? -12 : 0) + octave * 12), // 2nd inv
  ];
  
  let best = inversions[0];
  let bestDist = Infinity;
  for (const inv of inversions) {
    let dist = 0;
    for (let i = 0; i < Math.min(inv.length, prevChord.length); i++) {
      dist += Math.abs(inv[i] - prevChord[i]);
    }
    if (dist < bestDist) { bestDist = dist; best = inv; }
  }
  return best;
}

// --- Melodic motif generation (fractal self-similarity) ---
function generateMotif(scale, rootMidi, length, nu, p) {
  const motif = [];
  const scaleLen = scale.length;
  
  // Base motif = stepwise + occasional leap
  let prevDegree = 0;
  for (let i = 0; i < length; i++) {
    const useVariation = Math.random() > p;
    let degree;
    if (useVariation) {
      // Random walk with small steps
      const step = Math.floor((Math.random() - 0.5) * 4);
      degree = (prevDegree + step + scaleLen * 3) % scaleLen;
    } else {
      // Pattern: ascending then descending (arch shape = toroidal cycle)
      const phase = i / length;
      degree = Math.floor(Math.sin(phase * Math.PI) * (scaleLen / 2)) % scaleLen;
      if (degree < 0) degree += scaleLen;
    }
    motif.push(rootMidi + scale[degree]);
    prevDegree = degree;
  }
  
  // Fractal recursion: nu↑ = add ornamentation (passing tones, neighbor tones)
  if (nu > 0.5) {
    const ornamented = [];
    for (let i = 0; i < motif.length; i++) {
      ornamented.push(motif[i]);
      if (i < motif.length - 1 && Math.random() < nu * 0.5) {
        // Passing tone between motif notes
        const mid = (motif[i] + motif[i + 1]) / 2;
        ornamented.push(Math.round(mid));
      }
    }
    return ornamented;
  }
  
  return motif;
}

// --- Note frequency ---
function noteFreq(midi) {
  return 440 * Math.pow(2, (midi - 69) / 12);
}

// --- Drum synthesis ---
function makeKick(ctx, time, gain) {
  const osc = ctx.createOscillator();
  const g = ctx.createGain();
  osc.frequency.setValueAtTime(150, time);
  osc.frequency.exponentialRampToValueAtTime(40, time + 0.1);
  g.gain.setValueAtTime(gain, time);
  g.gain.exponentialRampToValueAtTime(0.001, time + 0.15);
  osc.connect(g);
  g.connect(masterGain);
  osc.start(time);
  osc.stop(time + 0.2);
  activeNodes.push(osc, g);
}

function makeSnare(ctx, time, gain, brightness) {
  const noiseBuf = ctx.createBuffer(1, ctx.sampleRate * 0.15, ctx.sampleRate);
  const data = noiseBuf.getChannelData(0);
  for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
  const noise = ctx.createBufferSource();
  noise.buffer = noiseBuf;
  const filter = ctx.createBiquadFilter();
  filter.type = 'highpass';
  filter.frequency.value = 1000 + brightness * 3000;
  const g = ctx.createGain();
  g.gain.setValueAtTime(gain, time);
  g.gain.exponentialRampToValueAtTime(0.001, time + 0.12);
  noise.connect(filter);
  filter.connect(g);
  g.connect(masterGain);
  noise.start(time);
  noise.stop(time + 0.15);
  activeNodes.push(noise, filter, g);
}

function makeHat(ctx, time, gain, brightness) {
  const noiseBuf = ctx.createBuffer(1, ctx.sampleRate * 0.05, ctx.sampleRate);
  const data = noiseBuf.getChannelData(0);
  for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
  const noise = ctx.createBufferSource();
  noise.buffer = noiseBuf;
  const filter = ctx.createBiquadFilter();
  filter.type = 'highpass';
  filter.frequency.value = 5000 + brightness * 5000;
  const g = ctx.createGain();
  g.gain.setValueAtTime(gain, time);
  g.gain.exponentialRampToValueAtTime(0.001, time + 0.04);
  noise.connect(filter);
  filter.connect(g);
  g.connect(masterGain);
  noise.start(time);
  noise.stop(time + 0.06);
  activeNodes.push(noise, filter, g);
}

// --- FM Bell synth (for high s / bright tiles) ---
function makeFMBell(ctx, freq, time, dur, gain, brightness, reverbSend, panner) {
  const carrier = ctx.createOscillator();
  carrier.type = 'sine';
  carrier.frequency.value = freq;
  const modulator = ctx.createOscillator();
  modulator.type = 'sine';
  modulator.frequency.value = freq * (2 + brightness * 4); // ratio 2:1 to 6:1
  const modGain = ctx.createGain();
  modGain.gain.setValueAtTime(freq * (1 + brightness * 3), time);
  modGain.gain.exponentialRampToValueAtTime(0.01, time + dur * 0.5);
  modulator.connect(modGain);
  modGain.connect(carrier.frequency);

  const g = ctx.createGain();
  g.gain.setValueAtTime(0, time);
  g.gain.linearRampToValueAtTime(gain, time + 0.005);
  g.gain.exponentialRampToValueAtTime(0.001, time + dur);

  const pan = ctx.createStereoPanner();
  pan.pan.value = panner;
  carrier.connect(g);
  g.connect(pan);
  pan.connect(masterGain);

  if (reverbSend > 0.1) {
    const rn = ctx.createConvolver();
    rn.buffer = reverbBuffer;
    const rg = ctx.createGain();
    rg.gain.value = reverbSend * 0.5;
    pan.connect(rn);
    rn.connect(rg);
    rg.connect(masterGain);
    activeNodes.push(rn, rg);
  }

  carrier.start(time);
  modulator.start(time);
  carrier.stop(time + dur + 0.1);
  modulator.stop(time + dur + 0.1);
  activeNodes.push(carrier, modulator, modGain, g, pan);
}

// --- Pluck synth (for melodic lines, guitar-like) ---
function makePluck(ctx, freq, time, dur, gain, brightness, reverbSend, panner) {
  const osc = ctx.createOscillator();
  osc.type = 'triangle';
  osc.frequency.value = freq;
  const osc2 = ctx.createOscillator();
  osc2.type = 'sawtooth';
  osc2.frequency.value = freq;
  osc2.detune.value = -5;

  const filter = ctx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.setValueAtTime(3000 + brightness * 4000, time);
  filter.frequency.exponentialRampToValueAtTime(200 + brightness * 300, time + dur);
  filter.Q.value = 3;

  const g = ctx.createGain();
  g.gain.setValueAtTime(0, time);
  g.gain.linearRampToValueAtTime(gain, time + 0.002);
  g.gain.exponentialRampToValueAtTime(0.001, time + dur);

  const pan = ctx.createStereoPanner();
  pan.pan.value = panner;
  osc.connect(filter);
  osc2.connect(filter);
  filter.connect(g);
  g.connect(pan);
  pan.connect(masterGain);

  if (reverbSend > 0.1) {
    const rn = ctx.createConvolver();
    rn.buffer = reverbBuffer;
    const rg = ctx.createGain();
    rg.gain.value = reverbSend * 0.3;
    pan.connect(rn);
    rn.connect(rg);
    rg.connect(masterGain);
    activeNodes.push(rn, rg);
  }

  osc.start(time);
  osc2.start(time);
  osc.stop(time + dur + 0.1);
  osc2.stop(time + dur + 0.1);
  activeNodes.push(osc, osc2, filter, g, pan);
}

// --- Warm pad with slow filter sweep ---
function makeWarmPad(ctx, freqs, time, dur, gain, brightness, reverbSend, panner) {
  const padGain = ctx.createGain();
  const filter = ctx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.setValueAtTime(400 + brightness * 2000, time);
  filter.frequency.linearRampToValueAtTime(800 + brightness * 5000, time + dur * 0.3);
  filter.frequency.linearRampToValueAtTime(400 + brightness * 2000, time + dur);
  filter.Q.value = 0.5;

  let reverbNode = null;
  if (reverbSend > 0.1) {
    reverbNode = ctx.createConvolver();
    reverbNode.buffer = reverbBuffer;
    const reverbGain = ctx.createGain();
    reverbGain.gain.value = reverbSend * 0.5;
    filter.connect(reverbNode);
    reverbNode.connect(reverbGain);
    reverbGain.connect(masterGain);
    activeNodes.push(reverbNode, reverbGain);
  }

  const pan = ctx.createStereoPanner();
  pan.pan.value = panner;
  padGain.connect(filter);
  filter.connect(pan);
  pan.connect(masterGain);

  const attack = 0.4 + (1 - brightness) * 0.3;
  const release = 0.6;
  padGain.gain.setValueAtTime(0, time);
  padGain.gain.linearRampToValueAtTime(gain, time + attack);
  padGain.gain.setValueAtTime(gain, time + dur - release);
  padGain.gain.linearRampToValueAtTime(0, time + dur);

  freqs.forEach((f, i) => {
    [-7, 7].forEach(detune => {
      const osc = ctx.createOscillator();
      osc.type = i === 0 ? 'sawtooth' : 'triangle';
      osc.frequency.value = f;
      osc.detune.value = detune;
      const og = ctx.createGain();
      og.gain.value = 0.5 / freqs.length;
      osc.connect(og);
      og.connect(padGain);
      osc.start(time);
      osc.stop(time + dur + 0.1);
      activeNodes.push(osc, og);
    });
  });
  activeNodes.push(padGain, filter, pan);
}

// --- Pad synth (chord) ---
function makePad(ctx, freqs, time, dur, gain, brightness, reverbSend, panner) {
  const padGain = ctx.createGain();
  const filter = ctx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.value = 800 + brightness * 5000;
  filter.Q.value = 0.7;

  // Reverb send
  let reverbNode = null;
  if (reverbSend > 0.1) {
    reverbNode = ctx.createConvolver();
    reverbNode.buffer = reverbBuffer;
    const reverbGain = ctx.createGain();
    reverbGain.gain.value = reverbSend * 0.5;
    filter.connect(reverbNode);
    reverbNode.connect(reverbGain);
    reverbGain.connect(masterGain);
    activeNodes.push(reverbNode, reverbGain);
  }

  // Stereo panner
  const pan = ctx.createStereoPanner();
  pan.pan.value = panner;

  padGain.connect(filter);
  filter.connect(pan);
  pan.connect(masterGain);

  // ADSR for pad
  const attack = 0.3;
  const release = 0.5;
  padGain.gain.setValueAtTime(0, time);
  padGain.gain.linearRampToValueAtTime(gain, time + attack);
  padGain.gain.setValueAtTime(gain, time + dur - release);
  padGain.gain.linearRampToValueAtTime(0, time + dur);

  freqs.forEach((f, i) => {
    // Two oscillators per note with detune for warmth
    [-7, 7].forEach(detune => {
      const osc = ctx.createOscillator();
      osc.type = i === 0 ? 'sawtooth' : 'triangle';
      osc.frequency.value = f;
      osc.detune.value = detune;
      const og = ctx.createGain();
      og.gain.value = 0.5 / freqs.length;
      osc.connect(og);
      og.connect(padGain);
      osc.start(time);
      osc.stop(time + dur + 0.1);
      activeNodes.push(osc, og);
    });
  });
  activeNodes.push(padGain, filter, pan);
}

// --- Bass synth ---
function makeBass(ctx, freq, time, dur, gain, brightness) {
  const osc = ctx.createOscillator();
  osc.type = 'sawtooth';
  osc.frequency.value = freq;
  const sub = ctx.createOscillator();
  sub.type = 'sine';
  sub.frequency.value = freq * 0.5;

  const filter = ctx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.value = 200 + brightness * 800;
  filter.Q.value = 3;

  const g = ctx.createGain();
  g.gain.setValueAtTime(0, time);
  g.gain.linearRampToValueAtTime(gain, time + 0.01);
  g.gain.setValueAtTime(gain, time + dur * 0.7);
  g.gain.exponentialRampToValueAtTime(0.001, time + dur);

  osc.connect(filter);
  sub.connect(filter);
  filter.connect(g);
  g.connect(masterGain);
  osc.start(time);
  sub.start(time);
  osc.stop(time + dur + 0.1);
  sub.stop(time + dur + 0.1);
  activeNodes.push(osc, sub, filter, g);
}

// --- Lead/arp synth ---
function makeLead(ctx, freq, time, dur, gain, brightness, reverbSend, panner, waveType) {
  const osc = ctx.createOscillator();
  osc.type = waveType;
  osc.frequency.value = freq;

  // Slight detune layer
  const osc2 = ctx.createOscillator();
  osc2.type = waveType;
  osc2.frequency.value = freq;
  osc2.detune.value = 12;

  const filter = ctx.createBiquadFilter();
  filter.type = 'lowpass';
  filter.frequency.value = 2000 + brightness * 6000;
  filter.Q.value = 2;

  const g = ctx.createGain();
  g.gain.setValueAtTime(0, time);
  g.gain.linearRampToValueAtTime(gain, time + 0.005);
  g.gain.exponentialRampToValueAtTime(0.001, time + dur);

  const pan = ctx.createStereoPanner();
  pan.pan.value = panner;

  osc.connect(filter);
  osc2.connect(filter);
  filter.connect(g);
  g.connect(pan);
  pan.connect(masterGain);

  // Reverb send
  if (reverbSend > 0.1) {
    const reverbNode = ctx.createConvolver();
    reverbNode.buffer = reverbBuffer;
    const rg = ctx.createGain();
    rg.gain.value = reverbSend * 0.4;
    pan.connect(reverbNode);
    reverbNode.connect(rg);
    rg.connect(masterGain);
    activeNodes.push(reverbNode, rg);
  }

  osc.start(time);
  osc2.start(time);
  osc.stop(time + dur + 0.1);
  osc2.stop(time + dur + 0.1);
  activeNodes.push(osc, osc2, filter, g, pan);
}

// --- 8D → 9 INTENT VARIABLES (Composition Engine) ---
// From 09_musical_state_spec.md
function computeIntentVariables(v) {
  // v = { r, h, d, p, s, gamma, g, nu }
  const closure = (v.g * 0.5) + (v.p * 0.3) + 0.2; // NAND_LOW assumed 0.2 baseline
  const tension = (v.d * 0.5) + ((1 - v.p) * 0.3) + (v.h * 0.2);
  const motion = (v.r * 0.6) + (v.p * 0.4);
  const brightness = (v.s * 0.7) + (v.gamma * 0.3);
  const space = (v.gamma * 0.7) + ((1 - v.g) * 0.3);
  const recurrence = (v.nu * 0.6) + (v.p * 0.4);
  const density = (v.g * 0.7) + (v.r * 0.3);
  const direction = ((v.h - v.d) * 0.7); // +1 = ascending, -1 = descending
  const cadenceEligibility = (closure * 0.5) + ((1 - tension) * 0.3) + (recurrence * 0.2);

  return { closure, tension, motion, brightness, space, recurrence, density, direction, cadenceEligibility };
}

// --- FORM / CADENCE AUTOMATON ---
let cadenceHysteresis = 0; // q state
const THETA_CADENCE = 0.6;
const THETA_RESOLVE = 0.7;
const THETA_SUSPEND = 0.5;

function computeRole(intent) {
  const { closure, tension, motion, brightness, space, recurrence, density, direction, cadenceEligibility } = intent;

  // Cadence Index
  const C = (closure * 0.5) + ((1 - tension) * 0.3) + (recurrence * 0.2);

  // Cadence Latch (hysteresis)
  if (C > THETA_CADENCE) cadenceHysteresis = Math.min(1, cadenceHysteresis + 0.1);
  else cadenceHysteresis = Math.max(0, cadenceHysteresis - 0.1);

  // Suspend Trigger (simplified: high brightness + high space)
  const S = (brightness > 0.6 && space > 0.6) ? 1 : 0;

  // Priority
  if (S > THETA_SUSPEND) return 'suspend';
  if (cadenceHysteresis > THETA_RESOLVE) return 'resolve';

  // Role scores
  const scores = {
    establish: (1 - tension) * 0.8 + closure * 0.2,
    expand: motion * 0.6 + brightness * 0.4,
    stress: tension * 0.7 + motion * 0.3,
    fracture: tension * 0.5 + (1 - closure) * 0.5,
    suspend: space * 0.7 + (1 - motion) * 0.3,
    discharge: motion * 0.8 + tension * 0.2,
    resolve: closure * 0.8 + (1 - tension) * 0.2
  };

  return Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b);
}

// --- ROLE → COMPOSITION PLAN ---
function getCompositionPlan(role, intent, v) {
  const { closure, tension, motion, brightness, space, recurrence, density, direction } = intent;

  switch (role) {
    case 'establish':
      return {
        chords: [0], // I only
        bass: 'root_pedal',
        melody: 'tonic_arpeggio',
        rhythm: 'quarter_pulse',
        arrangement: { pad: false, lead: 'single_voice' }
      };
    case 'expand':
      return {
        chords: [0, 3], // I→IV
        bass: 'step_ascent',
        melody: 'motif_sequence',
        rhythm: 'eighth_sync',
        arrangement: { pad: true, bass: 'active' }
      };
    case 'stress':
      return {
        chords: [3, 4], // IV→V
        bass: 'rise_to_V',
        melody: 'tension_notes',
        rhythm: 'syncopated_eighth',
        arrangement: { extraLayer: true, snareFill: true }
      };
    case 'fracture':
      return {
        chords: [4, 5], // V→vi deceptive
        bass: 'abrupt_drop',
        melody: 'leaps_rests',
        rhythm: 'broken_hits',
        arrangement: { pad: false, glitch: true }
      };
    case 'suspend':
      return {
        chords: [0, 5, 7], // sus4+add9
        bass: 'pedal',
        melody: 'slow_wide_arpeggio',
        rhythm: 'sparse_long',
        arrangement: { maxReverb: true, hiSynth: true }
      };
    case 'discharge':
      return {
        chords: [4, 0], // V→I fast
        bass: 'V_I_descent',
        melody: 'descending_run',
        rhythm: 'dense_eighth_sixteenth',
        arrangement: { percussiveBoost: true }
      };
    case 'resolve':
      return {
        chords: [4, 0], // V→I cadence
        bass: 'V_I_cadence',
        melody: 'landing_tonic',
        rhythm: 'slowdown',
        arrangement: { fadeLayers: true, sustainPad: true }
      };
    default:
      return getCompositionPlan('establish', intent, v);
  }
}

// --- COMPOSITION PLAN → AUDIO ---
function playComposition(v, duration = 8.0) {
  initAudio();
  stopAllSound();

  const intent = computeIntentVariables(v);
  const role = computeRole(intent);
  const plan = getCompositionPlan(role, intent, v);

  console.log('Role:', role, 'Plan:', plan);

  _renderComposition(plan, intent, v, duration);
}

function _renderComposition(plan, intent, v, duration) {
  const ctx = audioCtx;
  if (!ctx) return;
  const now = ctx.currentTime + 0.05;

  // Get mode and scale from d
  const mode = pickMode(v.d);
  const rootMidi = 60; // C4

  // Render chords
  const chordType = pickChordType(v.h);
  const barDuration = duration / plan.chords.length;

  let prevChord = null;
  plan.chords.forEach((degree, i) => {
    const chordRoot = rootMidi + mode[degree % mode.length];
    const chordNotes = chordType.map(iv => chordRoot + iv);
    const chordMidi = voiceLead(prevChord, chordRoot, chordType, mode, 4);
    prevChord = chordMidi;

    const chordStart = now + i * barDuration;
    const instSet = pickInstrumentSet(v);

    // Chord pad
    if (plan.arrangement.pad !== false) {
      makePad(ctx, chordMidi.map(n => noteFreq(n)), chordStart, barDuration * 0.9, 0.15, v.s, v.gamma, 0);
    }

    // Bass
    const bassFreq = noteFreq(chordRoot - 12);
    makeBass(ctx, bassFreq, chordStart, barDuration * 0.8, 0.2, v.s);

    // Melody based on plan
    const motifLength = 8;
    const motif = generateMotif(mode, rootMidi + 12, motifLength, v.nu, v.p);
    motif.forEach((midi, j) => {
      const noteTime = chordStart + (j / motifLength) * barDuration;
      const noteDur = barDuration / motifLength * 0.8;
      makeLead(ctx, noteFreq(midi), noteTime, noteDur, 0.1, v.s, v.gamma, (j % 2 === 0 ? -0.3 : 0.3), 'sine');
    });
  });

  // Drums based on rhythm type
  if (plan.rhythm === 'quarter_pulse' || plan.rhythm === 'eighth_sync') {
    const numBeats = Math.floor(duration * 2);
    for (let i = 0; i < numBeats; i++) {
      const beatTime = now + i * 0.5;
      makeKick(ctx, beatTime, 0.3);
      if (i % 2 === 1) makeSnare(ctx, beatTime, 0.15, v.s);
      makeHat(ctx, beatTime + 0.25, 0.05, v.s);
    }
  }
}

// --- 8D → ABSTRACT TEXTURE SYNTHESIS (fallback) ---
// No genre, no chords, no drums, no motifs.
// Each 8D parameter maps directly to a sonic quality.
// The user hears abstract blobs and chooses by preference,
// not by genre bias. The parameters speak for themselves.

function playTile8D(v, duration = 8.0) {
  initAudio();
  stopAllSound();
  console.log('playTile8D called, v=', v);
  // Use composition engine instead of texture
  playComposition(v, duration);
}

function _playTexture(v, duration) {
  try {
    const ctx = audioCtx;
    if (!ctx) { console.error('No audioCtx'); return; }
    if (!masterGain) { console.error('No masterGain'); return; }
    if (ctx.state === 'suspended') ctx.resume();
    const now = ctx.currentTime + 0.05;
    stopAllSound();

    const baseFreq = 440 * Math.pow(2, (0.5 - v.d) * 2);
    const numOscs = 2 + Math.floor(v.h * 6);
    const pulseRate = 0.5 + v.r * 5;
    const pulseDur = 1 / pulseRate;
    const cutoff = 200 + v.s * 6000;
    const reverbAmount = v.gamma;
    const lfoRate = 0.1 + v.g * 2;
    const lfoDepth = 0.1 + v.g * 0.4;
    const numLayers = 1 + Math.floor(v.nu * 5);
    const variation = (1 - v.p) * 0.3;

    if (!reverbBuffer) reverbBuffer = makeReverbBuffer(ctx, 3, 3);

    const textureGain = ctx.createGain();
    textureGain.gain.value = 0.3;
    textureGain.connect(masterGain);

    const reverbSend = ctx.createGain();
    reverbSend.gain.value = reverbAmount * 0.6;
    textureGain.connect(reverbSend);
    if (reverbGain) reverbSend.connect(reverbGain);

    const lfo = ctx.createOscillator();
    lfo.frequency.value = lfoRate;
    const lfoGain = ctx.createGain();
    lfoGain.gain.value = lfoDepth;
    lfo.connect(lfoGain);
    lfo.start(now);
    lfo.stop(now + duration + 0.5);
    activeNodes.push(lfo, lfoGain);

    for (let layer = 0; layer < numLayers; layer++) {
      const layerFreq = baseFreq * Math.pow(2, layer * 0.5);
      const layerGain = 0.15 / numLayers;

      const layerFilter = ctx.createBiquadFilter();
      layerFilter.type = 'lowpass';
      layerFilter.frequency.value = cutoff * (1 - layer * 0.1);
      layerFilter.Q.value = 1 + v.h * 3;

      const layerGainNode = ctx.createGain();
      layerGainNode.gain.value = layerGain;

      lfoGain.connect(layerFilter.frequency);

      for (let o = 0; o < numOscs; o++) {
        const osc = ctx.createOscillator();
        const detuneRatio = Math.pow(2, v.h * 2);
        const oscFreq = layerFreq * (1 + (o - numOscs/2) * 0.01 * detuneRatio);
        const waveTypes = ['sine', 'triangle', 'sawtooth', 'square'];
        osc.type = waveTypes[Math.floor(v.d * 3.99)];
        const freqJitter = 1 + (Math.random() - 0.5) * variation;
        osc.frequency.value = oscFreq * freqJitter;
        osc.connect(layerFilter);
        osc.start(now);
        osc.stop(now + duration + 0.5);
        activeNodes.push(osc);
      }

      layerFilter.connect(layerGainNode);
      layerGainNode.connect(textureGain);
      activeNodes.push(layerFilter, layerGainNode);

      if (v.r > 0.2) {
        const pulseGain = ctx.createGain();
        pulseGain.gain.value = 0;
        layerGainNode.disconnect();
        layerGainNode.connect(pulseGain);
        pulseGain.connect(textureGain);
        activeNodes.push(pulseGain);

        const numPulses = Math.floor(duration * pulseRate);
        for (let p = 0; p < numPulses; p++) {
          const pulseTime = now + p * pulseDur;
          const jitter = (Math.random() - 0.5) * variation * pulseDur;
          pulseGain.gain.setValueAtTime(0, pulseTime + jitter);
          pulseGain.gain.linearRampToValueAtTime(layerGain * 2, pulseTime + jitter + 0.02);
          pulseGain.gain.exponentialRampToValueAtTime(0.001, pulseTime + jitter + pulseDur * 0.8);
        }
      }

      if (v.nu > 0.4 && layer < numLayers - 1) {
        const subLayerGain = ctx.createGain();
        subLayerGain.gain.value = layerGain * 0.5 * v.nu;
        const subFilter = ctx.createBiquadFilter();
        subFilter.type = 'bandpass';
        subFilter.frequency.value = layerFreq * 2;
        subFilter.Q.value = 5;
        const subOsc = ctx.createOscillator();
        subOsc.type = 'sine';
        subOsc.frequency.value = layerFreq * (1.5 + Math.random() * 0.5);
        subOsc.connect(subFilter);
        subFilter.connect(subLayerGain);
        subLayerGain.connect(textureGain);
        subOsc.start(now + 0.1 * layer);
        subOsc.stop(now + duration + 0.5);
        activeNodes.push(subOsc, subFilter, subLayerGain);
      }
    }

    if (v.d > 0.4) {
      const noiseAmount = (v.d - 0.4) * 0.15;
      const noiseBuf = ctx.createBuffer(1, ctx.sampleRate * duration, ctx.sampleRate);
      const data = noiseBuf.getChannelData(0);
      for (let i = 0; i < data.length; i++) {
        data[i] = (Math.random() * 2 - 1) * noiseAmount;
      }
      const noise = ctx.createBufferSource();
      noise.buffer = noiseBuf;
      const nFilter = ctx.createBiquadFilter();
      nFilter.type = 'bandpass';
      nFilter.frequency.value = 400 + v.d * 1500;
      nFilter.Q.value = 0.8;
      const nGain = ctx.createGain();
      nGain.gain.value = 0.08;
      noise.connect(nFilter);
      nFilter.connect(nGain);
      nGain.connect(textureGain);
      noise.start(now);
      noise.stop(now + duration);
      activeNodes.push(noise, nFilter, nGain);
    }

    if (v.s > 0.5) {
      const shimmerFreq = 2000 + v.s * 4000;
      const shimmer = ctx.createOscillator();
      shimmer.type = 'sine';
      shimmer.frequency.value = shimmerFreq;
      const shimmerGain = ctx.createGain();
      shimmerGain.gain.value = 0;
      shimmer.connect(shimmerGain);
      shimmerGain.connect(textureGain);
      shimmerGain.gain.setValueAtTime(0, now);
      shimmerGain.gain.linearRampToValueAtTime((v.s - 0.5) * 0.08, now + 1);
      shimmerGain.gain.linearRampToValueAtTime(0, now + duration);
      shimmer.start(now);
      shimmer.stop(now + duration + 0.5);
      activeNodes.push(shimmer, shimmerGain);
    }

    if (v.gamma > 0.4) {
      const panner = ctx.createStereoPanner();
      const panLfo = ctx.createOscillator();
      panLfo.frequency.value = 0.1 + v.gamma * 0.5;
      const panLfoGain = ctx.createGain();
      panLfoGain.gain.value = v.gamma * 0.8;
      panLfo.connect(panLfoGain);
      panLfoGain.connect(panner.pan);
      textureGain.disconnect();
      textureGain.connect(panner);
      panner.connect(masterGain);
      panner.connect(reverbSend);
      panLfo.start(now);
      panLfo.stop(now + duration + 0.5);
      activeNodes.push(panner, panLfo, panLfoGain);
    }

    setTimeout(() => { stopAllSound(); }, duration * 1000 + 1500);
  } catch(err) { console.error('TEXTURE ERROR:', err); }
}

// --- Calibration rounds ---
// O-phase present-moment anchor: the transparent white buoyancy point
const O_ANCHOR = { r:0.45, h:0.70, d:0.50, p:0.70, s:0.60, gamma:0.65, g:0.55, nu:0.55 };

const ROUNDS = [
  { param: 'r', label: null, values: [0.30, 0.36, 0.40, 0.45, 0.50, 0.55, 0.62, 0.70] },
  { param: 'nu', label: null, values: [0.30, 0.38, 0.45, 0.50, 0.55, 0.62, 0.68, 0.75] },
  { param: 'mix', label: null, values: null },
  { param: 's_gamma', label: null, values: null }
];

const ROUND3_TILES = [
  { h:0.72, d:0.15, g:0.60, p:0.72, s:0.65, gamma:0.68, r:0.40, nu:0.50 },
  { h:0.68, d:0.22, g:0.58, p:0.68, s:0.62, gamma:0.55, r:0.48, nu:0.52 },
  { h:0.70, d:0.35, g:0.55, p:0.65, s:0.58, gamma:0.50, r:0.50, nu:0.55 },
  { h:0.70, d:0.50, g:0.55, p:0.70, s:0.60, gamma:0.65, r:0.45, nu:0.55 },
  { h:0.72, d:0.62, g:0.52, p:0.68, s:0.55, gamma:0.62, r:0.42, nu:0.58 },
  { h:0.68, d:0.72, g:0.50, p:0.65, s:0.50, gamma:0.55, r:0.48, nu:0.60 },
  { h:0.74, d:0.80, g:0.48, p:0.62, s:0.52, gamma:0.60, r:0.40, nu:0.62 },
  { h:0.72, d:0.88, g:0.50, p:0.60, s:0.58, gamma:0.58, r:0.45, nu:0.65 },
];

const ROUND4_TILES = [
  { s:0.45, gamma:0.45, r:0.45, d:0.50, h:0.70, p:0.68, g:0.55, nu:0.52 },
  { s:0.52, gamma:0.52, r:0.42, d:0.45, h:0.70, p:0.70, g:0.55, nu:0.50 },
  { s:0.58, gamma:0.58, r:0.46, d:0.50, h:0.70, p:0.70, g:0.55, nu:0.55 },
  { s:0.60, gamma:0.65, r:0.45, d:0.50, h:0.70, p:0.70, g:0.55, nu:0.55 },
  { s:0.65, gamma:0.68, r:0.48, d:0.45, h:0.72, p:0.68, g:0.58, nu:0.58 },
  { s:0.70, gamma:0.72, r:0.50, d:0.40, h:0.72, p:0.65, g:0.55, nu:0.60 },
  { s:0.75, gamma:0.75, r:0.52, d:0.35, h:0.72, p:0.62, g:0.52, nu:0.62 },
  { s:0.80, gamma:0.80, r:0.40, d:0.30, h:0.74, p:0.65, g:0.55, nu:0.55 },
];

let currentRound = 0;
let roundSelections = [];
let userProfile = null;

function init() {
  renderRoundDots();
  renderCalibrationRound();
}

function renderRoundDots() {
  const container = document.getElementById('round-dots');
  container.innerHTML = '';
  for (let i = 0; i < 4; i++) {
    const dot = document.createElement('div');
    dot.className = 'round-dot';
    if (i < currentRound) dot.classList.add('done');
    if (i === currentRound) dot.classList.add('current');
    container.appendChild(dot);
  }
}

function renderCalibrationRound() {
  const grid = document.getElementById('tile-grid');
  grid.innerHTML = '';

  for (let i = 0; i < 8; i++) {
    const tile = document.createElement('div');
    tile.className = 'tile';
    tile.dataset.index = i;

    // Small play/stop toggle button inside tile
    const playBtn = document.createElement('div');
    playBtn.className = 'tile-play-btn';
    const playIcon = document.createElement('div');
    playIcon.className = 'play-icon';
    playBtn.appendChild(playIcon);
    tile.appendChild(playBtn);

    let isPlaying = false;
    let playTimeout = null;

    // Play/stop button click
    playBtn.addEventListener('click', (e) => {
      e.stopPropagation();

      if (isPlaying) {
        // Stop
        stopAllSound();
        isPlaying = false;
        tile.classList.remove('playing');
        playBtn.classList.remove('playing');
        if (playTimeout) { clearTimeout(playTimeout); playTimeout = null; }
      } else {
        // Stop any other playing tile
        document.querySelectorAll('.tile').forEach(t => {
          t.classList.remove('playing');
          const pb = t.querySelector('.tile-play-btn');
          if (pb) pb.classList.remove('playing');
        });
        // Play this tile
        isPlaying = true;
        tile.classList.add('playing');
        playBtn.classList.add('playing');
        const v = getRoundVector(currentRound, i);
        playTile8D(v, 4.0);

        playTimeout = setTimeout(() => {
          isPlaying = false;
          tile.classList.remove('playing');
          playBtn.classList.remove('playing');
          playTimeout = null;
        }, 4500);
      }
    });

    // Tile body click = select this tile
    tile.addEventListener('click', (e) => {
      if (e.target === playBtn || playBtn.contains(e.target)) return;

      stopAllSound();
      isPlaying = false;
      if (playTimeout) { clearTimeout(playTimeout); playTimeout = null; }

      document.querySelectorAll('.tile').forEach(t => {
        t.classList.remove('playing', 'selected');
        const pb = t.querySelector('.tile-play-btn');
        if (pb) pb.classList.remove('playing');
      });
      tile.classList.add('selected');

      roundSelections[currentRound] = i;

      setTimeout(() => {
        currentRound++;
        if (currentRound < 4) {
          renderRoundDots();
          renderCalibrationRound();
        } else {
          determineProfile();
        }
      }, 600);
    });

    grid.appendChild(tile);
  }
}

function getRoundVector(round, tileIdx) {
  // Start from O-anchor (present-moment transparent white buoyancy)
  const base = Object.assign({}, O_ANCHOR);

  if (round === 0) {
    // Vary r around O-anchor (0.45) — all tiles stay near present-moment tempo
    base.r = ROUNDS[0].values[tileIdx];  // 0.30-0.70
    base.h = 0.68 + (tileIdx % 3) * 0.02;  // 0.68-0.72 = 9th chord anchor
    base.d = 0.35 + tileIdx * 0.04;  // 0.35-0.63 = modes near Dorian
    base.p = 0.68;  // strict loop tendency
    base.s = 0.55 + tileIdx * 0.01;  // near white light
    base.gamma = 0.60 + tileIdx * 0.01;  // near buoyant space
    base.g = 0.55;
    base.nu = 0.50 + (tileIdx % 3) * 0.03;  // near polyphonic loop
  } else if (round === 1) {
    // Vary nu around O-anchor (0.55) — all tiles stay near present-moment texture
    base.nu = ROUNDS[1].values[tileIdx];  // 0.30-0.75
    base.r = 0.42 + tileIdx * 0.01;  // near time-stopped
    base.h = 0.68 + base.nu * 0.04;  // 0.69-0.71 = 9th chord
    base.d = 0.40 + tileIdx * 0.03;  // modes near Dorian
    base.p = 0.60 + base.nu * 0.10;  // loop tightens with texture
    base.s = 0.58;
    base.gamma = 0.58 + base.nu * 0.08;  // space expands with texture
    base.g = 0.55;
  } else if (round === 2) {
    // 8 worlds orbiting O-anchor
    const t = ROUND3_TILES[tileIdx];
    Object.assign(base, t);
  } else if (round === 3) {
    // 8 timbral worlds orbiting O-anchor
    const t = ROUND4_TILES[tileIdx];
    Object.assign(base, t);
  }

  return base;
}

// --- Profile determination from 4 round selections ---
// Round 0 (r): low r = I, high r = E; also M vs F tendency
// Round 1 (nu): low nu = S, high nu = N; also M vs F tendency
// Round 2 (h/d/g/p): determines T/F and J/P
// Round 3 (s/gamma): determines blood type O/A/B/AB

function determineProfile() {
  const r0 = roundSelections[0]; // 0-7
  const r1 = roundSelections[1]; // 0-7
  const r2 = roundSelections[2]; // 0-7
  const r3 = roundSelections[3]; // 0-7

  // E/I from round 0 (r selection)
  const isE = r0 >= 4;
  const ei = isE ? 'E' : 'I';

  // S/N from round 1 (nu selection)
  const isN = r1 >= 4;
  const sn = isN ? 'N' : 'S';

  // T/F from round 2: tiles 0,1,6 = F (high h), tiles 2,3,7 = T (high d), tiles 4,5 = neutral
  const tfTiles = [2,3,7]; // T-leaning
  const isT = tfTiles.includes(r2);
  const tf = isT ? 'T' : 'F';

  // J/P from round 2: tiles with high g = J, low g = P
  const jTiles = [0,2,5,7]; // high g
  const isJ = jTiles.includes(r2);
  const jp = isJ ? 'J' : 'P';

  // Gender from rounds 0+1 combined
  // M tends toward high r AND high nu (mass + fractal)
  // F tends toward high r OR high nu but not both, or moderate
  const rScore = r0 / 7;
  const nuScore = r1 / 7;
  const mScore = (rScore + nuScore) / 2;
  const fScore = 1 - Math.abs(rScore - nuScore);
  const gender = mScore > fScore ? 'M' : 'F';

  // Blood from round 3 (s/gamma = complexity)
  // 0-1: O (complexity 1), 2-3: A (complexity 2), 4-5: B (complexity 3), 6-7: AB (complexity 4)
  let blood;
  if (r3 <= 1) blood = 'O';
  else if (r3 <= 3) blood = 'A';
  else if (r3 <= 5) blood = 'B';
  else blood = 'AB';

  const mbti = ei + sn + tf + jp;
  userProfile = { mbti, gender, blood, profile: `${mbti}_${gender}_${blood}` };

  enterProgram();
}

// --- Program stage ---
function enterProgram() {
  document.getElementById('calibration').classList.remove('active');
  document.getElementById('program').classList.add('active');
  renderProgramTiles();
}

function renderProgramTiles() {
  const grid = document.getElementById('prog-tile-grid');
  grid.innerHTML = '';

  for (let i = 0; i < 8; i++) {
    const tile = document.createElement('div');
    tile.className = 'tile';

    const playBtn = document.createElement('div');
    playBtn.className = 'tile-play-btn';
    const playIcon = document.createElement('div');
    playIcon.className = 'play-icon';
    playBtn.appendChild(playIcon);
    tile.appendChild(playBtn);

    let isPlaying = false;
    let playTimeout = null;

    playBtn.addEventListener('click', (e) => {
      e.stopPropagation();

      if (isPlaying) {
        stopAllSound();
        isPlaying = false;
        tile.classList.remove('playing');
        playBtn.classList.remove('playing');
        if (playTimeout) { clearTimeout(playTimeout); playTimeout = null; }
      } else {
        document.querySelectorAll('#prog-tile-grid .tile').forEach(t => {
          t.classList.remove('playing');
          const pb = t.querySelector('.tile-play-btn');
          if (pb) pb.classList.remove('playing');
        });
        isPlaying = true;
        tile.classList.add('playing');
        playBtn.classList.add('playing');
        const v = generateProgramVector(i);
        playTile8D(v, 6.0);

        playTimeout = setTimeout(() => {
          isPlaying = false;
          tile.classList.remove('playing');
          playBtn.classList.remove('playing');
          playTimeout = null;
        }, 6500);
      }
    });

    grid.appendChild(tile);
  }

  // Refresh tiles every 30 seconds (time windows shift)
  setInterval(() => {
    // Tiles auto-regenerate on next click; no visual change needed
  }, 30000);
}

function generateProgramVector(tileIdx) {
  const now = new Date();
  const h = now.getHours();
  const t = h;

  // Base vector from profile
  const base = { ...(MBTI_VECTORS[userProfile.mbti] || {}) };

  // W axis
  if (userProfile.gender === 'M') {
    base.nu = Math.min(1, (base.nu || 0.5) + 0.1);
    base.d = Math.min(1, (base.d || 0.5) + 0.1);
  } else {
    base.r = Math.min(1, (base.r || 0.5) + 0.1);
    base.g = Math.min(1, (base.g || 0.5) + 0.1);
  }

  // Determine active slot from time
  let jitter = 0;
  let useRandom = false;
  let useOpposite = false;

  if (h >= 0 && h < 3) { jitter = 0; } // AB
  else if (h >= 3 && h < 9) { jitter = 0.15; useOpposite = true; } // A - stress growth
  else if (h >= 9 && h < 15) { jitter = 0.15; } // O - present
  else if (h >= 15 && h < 21) { jitter = 0.30; useOpposite = true; } // B - extreme growth
  else { jitter = 0.30; useRandom = (h >= 21 || h < 3); } // AB integrate

  // Apply temperament opposite for stress/extreme
  if (useOpposite) {
    const opp = MBTI_VECTORS[MBTI_OPPOSITE[userProfile.mbti]] || {};
    Object.assign(base, opp);
    if (h >= 3 && h < 9) { // A slot
      base.nu = Math.min(1, (base.nu || 0.5) + 0.10);
      base.gamma = Math.max(0, (base.gamma || 0.5) - 0.05);
    }
  }

  // 3AM random
  if (useRandom) {
    base.p = Math.random();
    base.s = 0.5 + Math.random() * 0.5;
    base.nu = 0.9 + Math.random() * 0.1;
  }

  // JITTER on r, d
  if (jitter > 0) {
    base.r = Math.max(0, Math.min(1, base.r * (1 + (Math.random() * 2 - 1) * jitter)));
    base.d = Math.max(0, Math.min(1, base.d * (1 + (Math.random() * 2 - 1) * jitter)));
  }

  // Peak dimension per tile (tileIdx maps to one of 8 dims)
  const peakKey = ['r','h','d','p','s','gamma','g','nu'][tileIdx];
  base[peakKey] = Math.min(1, (base[peakKey] || 0.5) + 0.15);

  // Also shift by time window (t mod 8)
  const timePeak = ['r','h','d','p','s','gamma','g','nu'][t % 8];
  base[timePeak] = Math.min(1, (base[timePeak] || 0.5) + 0.10);

  return base;
}

// --- Save / Load state (via Electron menu) ---
if (window.api) {
  window.api.onRequestSaveState(() => {
    const isProgramStage = document.getElementById('program').classList.contains('active');
    const data = {
      currentRound,
      roundSelections,
      userProfile,
      isProgramStage
    };
    window.api.sendSaveStateData(data);
  });

  window.api.onLoadStateData((data) => {
    if (!data) return;
    currentRound = data.currentRound || 0;
    roundSelections = data.roundSelections || [];
    userProfile = data.userProfile || null;

    if (data.isProgramStage && userProfile) {
      enterProgram();
    } else {
      renderRoundDots();
      renderCalibrationRound();
    }
  });
}

// --- Start ---
init();
