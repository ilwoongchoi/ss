#!/usr/bin/env python3
"""
_activity_41.py — 8D × 41 particles × 10 routes, 128-slot deterministic activity map.

- 41 particles = 10 routes × (2 terminal + 1 gradient + 1 leakage) + 1 axion rebrancher
- 128 profiles: 16 MBTI × 2 gender × 4 blood × + element layer.
- 128 time slots (~11 min) over 24h, each emits top 5 routes -> activities.
"""
import math, json, hashlib, random, csv

DIMS = ['r', 'h', 'd', 'p', 's', 'gamma', 'g', 'nu']

# ============================================================
# 41 PARTICLES
# ============================================================
PARTICLES_41 = [
    # music_creation
    'proton_music','photon_music','gluon_music','em_music',
    # music_listening
    'neutrino_listen','muon_listen','higgs_listen','acetylcholine_listen',
    # visual_1
    'up_quark_v1','down_quark_v1','w_boson_v1','electron_v1',
    # visual_2
    'charm_quark_v2','strange_quark_v2','z_boson_v2','photon_v2',
    # movement_1
    'proton_move','gluon_move','w_boson_move','energy_move',
    # movement_2
    'top_quark_move','bottom_quark_move','tau_move','dark_matter_move',
    # imagination_1
    'higgs_imag','neutrino_imag','graviton_imag','dopamine_imag',
    # imagination_2
    'acetyl_coa_imag','electron_imag','axion_imag','endorphin_imag',
    # sexual
    'testosterone_sex','progesterone_sex','oxytocin_sex','dopamine_sex',
    # weekend_optional
    'serotonin_wk','cortisol_wk','epinephrine_wk','male_gaba_a_wk',
    # 41st
    'axion_rebrancher'
]

# ============================================================
# 10 ROUTES: each route = 2 terminal + 1 gradient + 1 leakage
# ============================================================
ROUTES_10 = {
    'music_creation':     {'terminal': ['proton_music','photon_music'], 'gradient':'gluon_music',    'leakage':'em_music'},
    'music_listening':    {'terminal': ['neutrino_listen','muon_listen'], 'gradient':'higgs_listen',   'leakage':'acetylcholine_listen'},
    'visual_1':           {'terminal': ['up_quark_v1','down_quark_v1'],   'gradient':'w_boson_v1',     'leakage':'electron_v1'},
    'visual_2':           {'terminal': ['charm_quark_v2','strange_quark_v2'], 'gradient':'z_boson_v2', 'leakage':'photon_v2'},
    'movement_1':         {'terminal': ['proton_move','gluon_move'],      'gradient':'w_boson_move',   'leakage':'energy_move'},
    'movement_2':         {'terminal': ['top_quark_move','bottom_quark_move'], 'gradient':'tau_move',   'leakage':'dark_matter_move'},
    'imagination_1':      {'terminal': ['higgs_imag','neutrino_imag'],    'gradient':'graviton_imag',  'leakage':'dopamine_imag'},
    'imagination_2':      {'terminal': ['acetyl_coa_imag','electron_imag'], 'gradient':'axion_imag',    'leakage':'endorphin_imag'},
    'sexual':             {'terminal': ['testosterone_sex','progesterone_sex'], 'gradient':'oxytocin_sex', 'leakage':'dopamine_sex'},
    'weekend_optional':   {'terminal': ['serotonin_wk','cortisol_wk'],    'gradient':'epinephrine_wk',  'leakage':'male_gaba_a_wk'},
}

# 8D weights for the 40 route particles (each named after base physical particle + role suffix)
PARTICLE_WEIGHTS = {
    'proton_music':        {'r':0.8,'p':0.5},
    'photon_music':        {'gamma':0.8,'s':0.3},
    'gluon_music':         {'h':0.8,'r':0.5},
    'em_music':            {'gamma':0.7,'s':0.5},
    'neutrino_listen':     {'r':0.8,'gamma':0.4},
    'muon_listen':         {'g':0.7,'s':0.3},
    'higgs_listen':        {'p':0.6,'s':0.3},
    'acetylcholine_listen':{'p':0.7,'s':0.4},
    'up_quark_v1':         {'s':0.7,'r':0.4},
    'down_quark_v1':       {'s':0.6,'h':0.4},
    'w_boson_v1':          {'nu':0.7,'d':0.5},
    'electron_v1':         {'s':0.6,'gamma':0.5},
    'charm_quark_v2':      {'g':0.7,'nu':0.4},
    'strange_quark_v2':    {'d':0.7,'s':0.5},
    'z_boson_v2':          {'d':0.7,'g':0.5},
    'photon_v2':           {'gamma':0.8,'s':0.4},
    'proton_move':         {'r':0.9,'p':0.3},
    'gluon_move':          {'h':0.7,'r':0.4},
    'w_boson_move':        {'nu':0.6,'d':0.3},
    'energy_move':         {'r':0.7,'p':0.3},
    'top_quark_move':      {'g':0.8,'d':0.4},
    'bottom_quark_move':   {'h':0.7,'g':0.3},
    'tau_move':            {'d':0.8,'h':0.5},
    'dark_matter_move':    {'d':0.7,'nu':0.4},
    'higgs_imag':          {'p':0.7,'s':0.4},
    'neutrino_imag':       {'r':0.8,'gamma':0.3},
    'graviton_imag':       {'g':0.7,'nu':0.4},
    'dopamine_imag':       {'p':0.7,'s':0.4},
    'acetyl_coa_imag':     {'g':0.6,'d':0.4},
    'electron_imag':       {'s':0.6,'gamma':0.5},
    'axion_imag':          {'nu':0.8,'gamma':0.4},
    'endorphin_imag':      {'h':0.7,'nu':0.3},
    'testosterone_sex':    {'r':0.8,'d':0.5},
    'progesterone_sex':    {'h':0.8,'gamma':0.5},
    'oxytocin_sex':        {'g':0.7,'h':0.5},
    'dopamine_sex':        {'s':0.7,'p':0.4},
    'serotonin_wk':        {'g':0.7,'h':0.4},
    'cortisol_wk':         {'g':0.8,'gamma':0.5},
    'epinephrine_wk':      {'r':0.8,'s':0.4},
    'male_gaba_a_wk':      {'g':0.8,'nu':0.5},
    'axion_rebrancher':    {'nu':0.5,'gamma':0.5},
}

# ============================================================
# PROFILES
# ============================================================
MBTI_LIST = ['ENFP','ISFP','ESFJ','INTP','ENTP','INFJ','ESTP','ISTP',
             'ENFJ','INTJ','ESFP','ISTJ','ESTJ','INFP','ISFJ','ENTJ']
BLOOD_TYPES = ['O','A','B','AB']
GENDERS = ['M','F']

MBTI_8D = {
    'ENFP':('r',1.0,'s',0.6,'nu',0.3),
    'ISFP':('h',1.0,'gamma',0.6,'nu',0.3),
    'ESFJ':('d',1.0,'h',0.6,'g',0.3),
    'INTP':('p',1.0,'nu',0.6,'h',0.3),
    'ENTP':('s',1.0,'r',0.6,'nu',0.3),
    'INFJ':('gamma',1.0,'h',0.6,'p',0.3),
    'ESTP':('g',1.0,'s',0.6,'r',0.3),
    'ISTP':('nu',1.0,'p',0.6,'d',0.3),
    'ENFJ':('r',0.8,'h',0.8,'gamma',0.4),
    'INTJ':('h',1.0,'p',0.6,'nu',0.3),
    'ESFP':('s',1.0,'gamma',0.6,'r',0.3),
    'ISTJ':('d',1.0,'g',0.6,'p',0.3),
    'ESTJ':('g',1.0,'d',0.6,'p',0.3),
    'INFP':('h',1.0,'gamma',0.6,'nu',0.3),
    'ISFJ':('g',1.0,'gamma',0.6,'h',0.3),
    'ENTJ':('d',1.0,'gamma',0.6,'g',0.3),
}

BLOOD_WEIGHT = {'O':1.0,'A':0.75,'B':0.60,'AB':0.50}

def flow(g):
    if g == 'M':
        return {'r':0.8,'h':0.5,'d':1.0,'p':0.5,'s':0.6,'gamma':0.9,'g':0.4,'nu':0.5}
    return {'r':0.6,'h':0.9,'d':0.4,'p':0.5,'s':0.7,'gamma':0.5,'g':1.0,'nu':0.6}

def impedance_vector(mbti, blood, gender):
    dom,dv,sec,sv,tert,tv = MBTI_8D[mbti]
    v = {d:0.5 for d in DIMS}
    v[dom]=dv; v[sec]=sv; v[tert]=tv
    for d in v: v[d]*=BLOOD_WEIGHT[blood]*flow(gender)[d]
    for d in v: v[d]=max(0.0,min(1.0,v[d]))
    return v

# ============================================================
# CIRCADIAN 128-SLOT
# ============================================================
def circadian_128(slot_i):
    h = slot_i * 24.0 / 128.0
    boosts = {}
    # 4 phases: 0-3h AB, 3-9h A, 9-15h O, 15-21h B, 21-24h AB
    if 0<=h<3 or h>=21:
        boosts = {'gamma':0.3,'nu':0.3,'d':0.2}
    elif 3<=h<9:
        boosts = {'h':0.3,'g':0.2,'r':0.1}
    elif 9<=h<15:
        boosts = {'s':0.3,'r':0.2,'p':0.1}
    else:
        boosts = {'d':0.3,'g':0.2,'gamma':0.1}
    return h, boosts

# ============================================================
# ACTIVITY VOCABULARY per route (40 options each)
# ============================================================
ACTIVITY_BANK = {
    'music_creation':     ['PIANO COMPOSITION','STRING QUARTET ARRANGEMENT','COUNTERPOINT EXERCISE','MICROTONAL COMPOSITION','SPECTRAL MUSIC ANALYSIS','CONSTRAINT-BASED COMPOSITION','JAZZ PIANO VOICINGS','ORCHESTRATION','AMBIENT DRONE COMPOSITION','SHOEGAZE GUITAR LAYERING','NOISE TEXTURE GENERATION','MODULAR SYNTH PATCH','TAPE MUSIC COMPOSITION','CONCRETE MUSIC','HYPERPOP PRODUCTION','WITCH HOUSE COMPOSITION','DECONSTRUCTED CLUB MIX','GLITCH POP ARRANGEMENT','VAPORWAVE SAMPLING','SPECTRAL FREEZING','BITCRUSH PROCESSING','ULTRASONIC EXPLORATION','ALGORITHMIC COMPOSITION','GENERATIVE MUSIC CODING','L-SYSTEM GENERATION','FRACTAL RENDERING AUDIO','SHADER PROGRAMMING SOUND','REACTION-DIFFUSION AUDIO','WAVE FUNCTION COLLAPSE SOUND','RHYTHMIC GYMNASTICS','DANCE IMPROVISATION','CAPOEIRA','BREAKDANCING','TANGO','HIP-HOP DANCE','STEP AEROBICS','TRAMPOLINE','SKIPPING ROPE VARIATIONS','PARKOUR FREE RUNNING','TRAIL RUNNING','BEACH SPRINTS'],
    'music_listening':    ['DEEP LISTENING SESSION','ACOUSTIC ECOLOGY WALK','BINAURAL SOUND BATH','SPATIAL AUDIO MIX REVIEW','ALBUM DECONSTRUCTION','FIELD RECORDING LISTENING','HARMONIC RESONANCE TUNING','SLOW MOTION REMIX STUDY','HISTORICAL RECORDING ANALYSIS','LIVE CONCERT IMMERSION','OPERA BROADCAST','JAZZ SET DEEP LISTEN','ELECTRONIC SET IMMERSION','NOISE WALL LISTENING','DRONE MEDITATION','AMBIENT WORK MUSIC','CLASSICAL FOCUS MUSIC','FOLK MUSIC LISTENING','WORLD MUSIC EXPLORATION','SOUNDTRACK ANALYSIS','PODCAST SCORE REVIEW','RADIO DRAMA LISTEN','MUSICAL THEATRE CAST RECORDING','CHANTING PRACTICE','OVERTONE SINGING LISTEN','BINAURAL BEATS FOCUS','ISOCHRONIC TONES','SOLFEGGIO FREQUENCIES','8D AUDIO EXPERIENCE','DOLBY ATMOS DEMO','SPATIAL MUSIC INSTALLATION','SOUND ART GALLERY','LIVE ACOUSTIC SET','VINYL ANALYTICAL LISTEN','CASSETTE TAPE STUDY','REEL-TO-REEL PLAYBACK','SCHNELLER WALK LISTEN','URBAN SOUND MAP','RURAL SOUNDSCAPE','NIGHT SOUNDS LISTEN','WILDLIFE ACOUSTICS'],
    'visual_1':           ['DIGITAL PAINTING','COLOR THEORY STUDY','PHOTO EDITING','LIGHTING DESIGN','STUDIO PHOTOGRAPHY','COLOR GRADING','VISUAL EFFECTS','3D RENDERING','MOTION GRAPHICS','BRIGHTFIELD MICROSCOPY','WILDLIFE PHOTOGRAPHY','LANDSCAPE PAINTING','BOTANICAL ILLUSTRATION','PLEIN AIR PAINTING','WATERCOLOR','PASTEL DRAWING','STAINED GLASS DESIGN','CALLIGRAPHY','ILLUMINATION','GOLD LEAF GILDING','3D MODELING','ARCHITECTURAL DRAWING','CNC MACHINING','3D PRINTING','CAD DESIGN','TOPOGRAPHIC MAPPING','SPATIAL PLANNING','INTERIOR DESIGN RENDER','URBAN DESIGN','LANDSCAPE ARCHITECTURE','VIRTUAL REALITY EXPLORATION','AUGMENTED REALITY DESIGN','GAME ENVIRONMENT DESIGN','LEVEL DESIGN','TERRAIN GENERATION','FLIGHT SIMULATOR','SATELLITE IMAGERY ANALYSIS','GIS MAPPING','CARTOGRAPHY','TOPOGRAPHIC SURVEY','CINEMATIC COMPOSITION'],
    'visual_2':           ['GENERATIVE ART CODING','CELLULAR AUTOMATON','L-SYSTEM GENERATION','FRACTAL RENDERING','MANDELBROT EXPLORATION','PERLIN NOISE SCULPTING','SHADER PROGRAMMING','PROCEDURAL TERRAIN','WAVE FUNCTION COLLAPSE','REACTION-DIFFUSION SIMULATION','BLACK INK DRAWING','VOID MEDITATION','NEGATIVE SPACE PAINTING','MONOCHROME COMPOSITION','DECONSTRUCTION ANALYSIS','DARKROOM PHOTOGRAPHY','ABSTRACT PAINTING','SENSORY WALK','IMPROVISATIONAL MUSIC','FREE JAZZ IMPROVISATION','AVANT-GARDE COMPOSITION','NOISE MUSIC PERFORMANCE','POWER ELECTRONICS','DARK AMBIENT DRONE','INDUSTRIAL SOUND DESIGN','GLITCH COMPOSITION','DRONE METAL','HARSH NOISE WALL','SPECTRAL DISRUPTION','PHILOSOPHY READING','PHENOMENOLOGY JOURNAL','EXISTENTIAL WRITING','ZEN KOAN STUDY','DREAM ANALYSIS','SYMBOLIC INTERPRETATION','JOURNALING','FANTASY WORLD BUILDING','CREATIVE NONFICTION','POETRY WRITING','FEATURE FILM SCREENWRITER','DYNAMIC DIORAMA'],
    'movement_1':         ['SPRINT INTERVALS','JUMP ROPE','ROWING ERGOMETER','CYCLING TIME TRIAL','SWIMMING SPRINTS','BOXING COMBINATION DRILLS','KETTLEBELL CIRCUIT','BURPEE INTERVALS','STAIR CLIMBING','BATTLE ROPES','DANCE IMPROVISATION','CAPOEIRA','BREAKDANCING','TANGO','HIP-HOP DANCE','STEP AEROBICS','TRAMPOLINE','JUMPING JACKS CIRCUIT','SKIPPING ROPE VARIATIONS','RHYTHMIC GYMNASTICS','TRAIL RUNNING','CROSS-COUNTRY SKIING','ORIENTEERING','NORDIC WALKING','BEACH SPRINTS','HILL REPEATS','SANDBAG CARRY','OBSTACLE COURSE RUNNING','PARKOUR','FREE RUNNING','WEIGHTLIFTING','RESISTANCE TRAINING','COMBAT SPORTS','YOGA','PILATES','DANCE FLOW','MARTIAL ARTS SPARRING','IMPROVISED NAVIGATION','ENGINEERING PROJECT','MECHANICAL REPAIR','CIRCUIT DESIGN'],
    'movement_2':         ['EXTREME SPORTS','MARTIAL ARTS SPARRING','IMPROVISED NAVIGATION','FREE RUNNING','PARKOUR ADVANCED','ROCK CLIMBING','BOULDERING','ICE CLIMBING','ALPINE SKIING','MOUNTAINEERING','BMX AERIAL','INLINE AERIAL','SKATEBOARD TRICKS','TRAMPOLINE FLIPS','FLOORBALL','LACROSSE ATTACK','KABADDI','KORFBALL','SEPAKTAKRAW','ULTIMATE FRIS','ICE HOCKEY WING','TENNIS BASELINE STRATEGY','POGOSTICK','ABSEILING','GEOCACHING','FLOWBOARDING','WATER SPORTS','SURFING','KITESURFING','WAKEBOARDING','SCUBA DIVING','FREEDIVING','SKYDIVING','PARAGLIDING','HANG GLIDING','BASE JUMPING','CANYONING','CAVING','EXPEDITION RACING','ULTRAMARATHON','TRIATHLON'],
    'imagination_1':      ['FRACTAL GENERATION','RECURSIVE ALGORITHM DESIGN','MANDELBROT SET EXPLORATION','JULIA SET RENDERING','IFS GENERATION','L-SYSTEM TREE GENERATION','KOCH SNOWFLAKE STUDY','SIERPINSKI TRIANGLE','DRAGON CURVE','H-FRACTAL','ORIGAMI','WET FOLDING ORIGAMI','MODULAR ORIGAMI','TESSELLATION FOLDING','KIRIGAMI','PAPER CUTTING ART','POP-UP BOOK DESIGN','FOLDING GEOMETRY STUDY','RIGID ORIGAMI','CREASE PATTERN DESIGN','DEEP MEDITATION','VIPASSANA','ZAZEN','CONTEMPLATIVE PRAYER','LUCID DREAMING PRACTICE','SENSORY DEPRIVATION','FLOATING TANK','BREATHWORK','YOGA NIDRA','TRANCE INDUCTION','ALGORITHMIC COMPOSITION','GENERATIVE ART CODING','CELLULAR AUTOMATON','L-SYSTEM GENERATION','FRACTAL RENDERING','MANDELBROT EXPLORATION','PERLIN NOISE SCULPTING','SHADER PROGRAMMING','PROCEDURAL TERRAIN','WAVE FUNCTION COLLAPSE','REACTION-DIFFUSION SIMULATION'],
    'imagination_2':      ['POETRY WRITING','FANTASY WORLD BUILDING','CREATIVE NONFICTION','JOURNALING','SYMBOLIC INTERPRETATION','DREAM ANALYSIS','ZEN KOAN STUDY','PHENOMENOLOGY JOURNAL','EXISTENTIAL WRITING','PHILOSOPHY READING','STORYBOARDING','SCENARIO PLANNING','FUTURE CASTING','SCIENCE FICTION WRITING','MYTHOLOGY STUDY','ARCHETYPAL ANALYSIS','TAROT INTERPRETATION','ASTROLOGY MAPPING','I CHING CONSULTATION','DIVINATION PRACTICE','LUCID DREAMING','ASTRAL PROJECTION','SENSORY IMAGINATION','MENTAL REHEARSAL','VISUALIZATION TRAINING','MEMORY PALACE','MNEMONIC JOURNEY','COGNITIVE MAPPING','CONCEPT MAP DRAWING','MIND MAP EXPLORATION','BRAINSTORMING SESSION','LATERAL THINKING PUZZLES','STARTUP IDEATION','DEBATE PRACTICE','NEGOTIATION SIMULATION','STRATEGIC PLANNING','LONG-TERM FORECASTING','SYSTEM OPTIMIZATION','BUSINESS STRATEGY','EXECUTIVE DECISION SIMULATION','POLICY DESIGN'],
    'sexual':             ['SENSUAL MASSAGE PRACTICE','INTIMATE DANCE','TANTRIC BREATHWORK','PARTNER YOGA','COUPLES PILATES','SENSORY FOCUS EXERCISE','BODY AWARENESS MEDITATION','SELF-PLEASURE RITUAL','EROTIC WRITING','INTIMACY JOURNALING','RELATIONSHIP MAPPING','ATTACHMENT STYLE STUDY','LOVE LANGUAGE ANALYSIS','BOUNDARY PRACTICE','CONSENT COMMUNICATION','DESIRE EXPLORATION','FANTASY DISCUSSION','SENSORY DEPRIVATION TOGETHER','TRUST EXERCISE','EYE GAZING PRACTICE','CUDDLE THERAPY','SKIN-TO-SKIN REST','AROMATHERAPY INTIMACY','BATH RITUAL','SHARED BREATHWORK','HEART COHERENCE PRACTICE','ENERGY EXCHANGE MEDITATION','TANTRIC SOUNDING','PLEASURE MAPPING','EROGENOUS ZONES STUDY','LIBIDO TRACKING','HORMONAL CYCLE MAPPING','FERTILITY AWARENESS','PROSTATE/PELVIC FLOOR WORK','PC MUSCLE TRAINING','KEGEL ROUTINE','HIP OPENING YOGA','SACRAL CHAKRA MEDITATION','SHADOW WORK INTIMACY','REPAIR CONVERSATION','AFTERCARE RITUAL'],
    'weekend_optional':   ['OUTDOOR SURVIVAL','DIRECT ACTION','PHYSICAL CHALLENGE','WILDLIFE DOCUMENTARY','OUTDOOR SURVIVAL','DETAILED CRAFTSMANSHIP','METHODICAL STUDY','GRADUAL MASTERY','CREATIVE ADAPTATION','IMPROVISED SOLUTION','FLEXIBLE APPROACH','INTERDISCIPLINARY SYNTHESIS','PARADOX INTEGRATION','MULTI-DOMAIN BRIDGING','COMMUNITY ORGANIZING','EVENT PLANNING','GROUP FACILITATION','PUBLIC SPEAKING','WORKSHOP FACILITATION','COMMUNITY THEATRE','GARDENING','CAREGIVING','HISTORICAL RESEARCH','ARCHIVAL RESEARCH','DATA AUDIT','COMPLIANCE REVIEW','PROJECT MANAGEMENT','OPERATIONS PLANNING','LOGISTICS OPTIMIZATION','CONSERVATION ARCHITECTURE','RESTORATION','HERITAGE MASONRY','LIME MORTAR WORK','THATCHING','DRY STONE WALLING','HEDGELAYING','HEDGE LAYERING','COB BUILDING','EARTH BAG CONSTRUCTION','BOOKBINDING','LEATHERWORK'],
}

# ============================================================
# MUSCLE SUB-COMPARTMENTS (nm-level decomposition)
# ============================================================
MUSCLE_COMPARTMENTS = {
    'frontalis_L_outer_top':    ['proton_music','neutrino_listen','up_quark_v1','proton_move'],
    'frontalis_L_outer_bottom': ['dopamine_imag','acetylcholine_listen','electron_v1','dopamine_sex'],
    'frontalis_L_inner_top':    ['higgs_imag','acetyl_coa_imag','higgs_listen','testosterone_sex'],
    'frontalis_L_inner_bottom': ['electron_imag','dopamine_sex','cortisol_wk','serotonin_wk'],
    'frontalis_R_outer_top':    ['photon_music','muon_listen','down_quark_v1','gluon_move'],
    'frontalis_R_outer_bottom': ['proton_music','w_boson_v1','w_boson_move','epinephrine_wk'],
    'frontalis_R_inner_top':    ['neutrino_imag','graviton_imag','photon_v2','progesterone_sex'],
    'frontalis_R_inner_bottom': ['proton_music','photon_music','proton_move','dopamine_sex'],
    'occipitalis_L_outer_top':  ['male_gaba_a_wk','strange_quark_v2','dark_matter_move','endorphin_imag'],
    'occipitalis_L_outer_bottom':['left_occipitalis_estrogen?','cortisol_wk','acetylcholine_listen','male_gaba_a_wk'],
    'occipitalis_L_inner_top':  ['gluon_music','gluon_move','energy_move','bottom_quark_move'],
    'occipitalis_L_inner_bottom':['photon_v2','top_quark_move','graviton_imag','male_gaba_a_wk'],
    'occipitalis_R_outer_top':  ['testosterone_sex','oxytocin_sex','cortisol_wk','epinephrine_wk'],
    'occipitalis_R_outer_bottom':['serotonin_wk','electron_imag','electron_v1','dark_matter_move'],
    'occipitalis_R_inner_top':  ['female_gaba?','gluon_music','w_boson_v1','neutrino_imag'],
    'occipitalis_R_inner_bottom':['em_music','charm_quark_v2','z_boson_v2','photon_v2'],
    'temporalis_L_outer':       ['charm_quark_v2','higgs_listen','endorphin_imag','dopamine_imag'],
    'temporalis_L_inner':       ['5HT1A?','neutrino_listen','acetylcholine_listen','serotonin_wk'],
    'temporalis_R_outer':       ['5HT1B?','tau_move','male_gaba_a_wk','cortisol_wk'],
    'temporalis_R_inner':       ['acetylcholine_listen','higgs_imag','dopamine_sex','progesterone_sex'],
}

# ============================================================
# DETERMINISTIC GENERATOR
# ============================================================
def hash_choice(seed, choices):
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return choices[h % len(choices)]

def slot_time(i):
    m = i * 11
    hh, mm = divmod(m, 60)
    return f"{hh}:{mm:02d}"

def generate_128_csv():
    # 128 slot → profile determined by rotating through 16 MBTI × 2 gender × 4 blood = 128
    profiles = [f"{m}_{g}_{b}" for m in MBTI_LIST for g in GENDERS for b in BLOOD_TYPES]
    rows = []
    for i in range(128):
        prof = profiles[i]
        mbti, gender, blood = prof.split('_')
        vec = impedance_vector(mbti, blood, gender)
        h, boosts = circadian_128(i)
        for d, b in boosts.items(): vec[d] = min(1.0, vec[d] + b)

        # compute each route score
        route_scores = {}
        for route, parts in ROUTES_10.items():
            score = 0.0
            for p in parts['terminal']:
                for dim, w in PARTICLE_WEIGHTS[p].items():
                    score += vec.get(dim,0.5) * w * 1.5
            for p in [parts['gradient'], parts['leakage']]:
                for dim, w in PARTICLE_WEIGHTS[p].items():
                    score += vec.get(dim,0.5) * w
            # add time-of-day mod
            score += 0.05 * math.sin((h/24.0 + hash(route)%100/1000) * 6.28318)
            route_scores[route] = score

        # top 5 routes
        top5 = sorted(route_scores, key=route_scores.get, reverse=True)[:5]
        acts = []
        for j, route in enumerate(top5):
            seed = f"{prof}_{i}_{route}"
            acts.append(hash_choice(seed, ACTIVITY_BANK[route]))

        # rebrancher: axion may override slot 3 (random time position)
        axion_pos = int(hash_choice(f"{prof}_{i}_axion", [str(x) for x in range(5)])) if 0<=h<3 or h>=21 else None
        if axion_pos is not None and 0<=axion_pos<5:
            acts[axion_pos] = hash_choice(f"{prof}_{i}_axion_override", ACTIVITY_BANK['weekend_optional'])

        rows.append([slot_time(i), prof] + acts)

    with open('activity_128_41.csv','w',newline='',encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['time','profile','A1','A2','A3','A4','A5'])
        w.writerows(rows)
    print('Wrote activity_128_41.csv')
    return rows

if __name__ == '__main__':
    generate_128_csv()
