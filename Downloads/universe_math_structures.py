#!/usr/bin/env python3



"""



UNIVERSE MATH STRUCTURES — COMPLETE



8 base particles | 42 particles | 5 routes | 16 layers



Inverse reciprocal tensor | Torus embedding | Klein neck | Pole flip



Spiral topology | Betti topology | Dimension stack | Dream folding



Dipole circuit | ABO topology | Darcy leakage | MC1R bypass



Observer axiom | Gender axis | 4-layer↔5-route map | Blood schedule



138.88° recursive spark | Mandelbrot 128 | Particle→anatomy derivation







Structure only — no numeric constants.



Sources: 8 conversation files (last 4 weeks) + tensor_equation.py + particle_to_8d.py + universe-prose.md + 영점.md



"""







import math







from body_particle_map import PARTICLE_BODY_MAP



from leakage_cavities import LEAKAGE_CAVITIES







# ============================================================



# 1. EIGHT BASE PARTICLES — DAY SET + NIGHT SET (separate)



# ============================================================



# Day particles exist ONLY during day. Night particles exist ONLY during night.



# They do NOT swap — they are separate sets.



# Body back->front: thickness brightness increases (back=dark/night, front=bright/day)



# Face quadrants = day particles. Body quadrants = night particles.



# z_boson = 4:30AM-6AM transition = night gluon + day electron = NAVY (640nm bluelight)



# Deep pink transition = 4:30-6AM = gluon(PURPLE)+electron(BLUE)+tau(DARK_RED)+z_boson(RED) meeting







# --- DAY PARTICLES (face, front, bright) ---



BASE_PARTICLES = {



    'z_boson':   {'param': 'r',     'color': 'RED',         'route': 2, 'set': 'day',



                  'face_quadrant': 4,  # 우하 (lower-right)



                  'addition': 'base'},



    'photon':    {'param': 'gamma', 'color': 'YELLOW',      'route': 3, 'set': 'day',



                  'face_quadrant': 1,  # 우상 (upper-right)



                  'addition': 'base'},



    'muon':      {'param': 'g',     'color': 'DARK_GREEN',  'route': 1, 'set': 'day',



                  'face_quadrant': 2,  # 좌상 (upper-left)



                  'addition': 'electron + photon'},



    'electron':   {'param': 's',     'color': 'BLUE',        'route': 4, 'set': 'day',



                  'face_quadrant': 3,  # 좌하 (lower-left)



                  'addition': 'base'},



    # --- NIGHT PARTICLES (body, back, dark) ---



    'tau':       {'param': 'd',     'color': 'DARK_RED',    'route': 2, 'set': 'night',



                  'body_quadrant': 4,  # 우하 (lower-right)



                  'addition': 'z_boson + gluon'},



    'gluon':     {'param': 'h',     'color': 'PURPLE',      'route': 5, 'set': 'night',



                  'body_quadrant': 2,  # 좌상 (upper-left)



                  'addition': 'z_boson + electron'},



    'w_boson':   {'param': 'nu',    'color': 'DARK_YELLOW', 'route': 4, 'set': 'night',



                  'body_quadrant': 1,  # 우상 (upper-right)



                  'addition': 'z_boson + photon'},



    'higgs':     {'param': 'p',     'color': 'DARK_ORANGE', 'route': 3, 'set': 'night',



                  'body_quadrant': 3,  # 좌하 (lower-left)



                  'addition': 'z_boson + w_boson'},



}







# --- TRANSITION PARTICLE ---



DERIVED_BASE = {



    # z_boson = 4:30AM-6AM = night gluon(PURPLE) + day electron(BLUE) = NAVY



    # 640nm bluelight: left eye GABA-B / 640 cytochrome / electron_neutrino / COX alignment



    # Left eye supraorbital = electron_neutrino brain switch + cytochrome_640 + COX



    #   aligned on left-body upper-lower line



    'z_boson': {'color': 'NAVY', 'route': 5, 'set': 'transition',



                 'time_window': (4.5, 6.0),  # 4:30AM - 6:00AM



                 'addition': 'gluon(night) + electron(day)',



                 'nm': '640',



                 'mechanism': 'left_eye_gaba_b + cytochrome_640 + electron_neutrino + COX'},



}







# Face quadrant map: Q1(우상)=photon, Q2(좌상)=muon, Q3(좌하)=electron, Q4(우하)=z_boson







# Body quadrant map: Q1(우상)=w_boson, Q2(좌상)=gluon, Q3(좌하)=higgs, Q4(우하)=tau







# Deep pink transition: 4:30AM-6:00AM



# gluon(PURPLE 128,0,128) + electron(BLUE 0,0,255) additive = (255,0,128) ~ DEEP-PINK base



# tau(DARK_RED) + z_boson(RED) reinforce R channel to 255



# GREEN 20 = tau dark_red micro-leak, BLUE 147 = gluon 128 + electron micro-add



# cobalamin = s x nu + h(purple) involvement







# Blood type optical properties:



# A = left body, top-down widening -> 명도 (luminosity/value) changes



# O = left body, bottom-up widening -> 탁도 (turbidity) changes (A->O: luminosity + turbidity shift)



# B = right body, inner -> 암도 (darkness quality) changes



# AB = right body, outer -> baseline (AB->B: darkness shift)



# Gender: left(female) -> right(male) = 채도 (saturation) changes



BLOOD_OPTICAL_MAP = {



    'A':  {'body_side': 'left', 'width_direction': 'top_to_bottom_widening',



            'optical_property': 'luminosity',  'korean': '명도'},



    'O':  {'body_side': 'left', 'width_direction': 'bottom_to_top_widening',



            'optical_property': 'turbidity',   'korean': '탁도'},



    'AB': {'body_side': 'right', 'width_direction': 'outer',



            'optical_property': 'baseline',     'korean': '기준'},



    'B':  {'body_side': 'right', 'width_direction': 'inner',



            'optical_property': 'darkness_quality', 'korean': '암도'},



}



# A->O transition: luminosity + turbidity shift



# AB->B transition: darkness quality shift



GENDER_OPTICAL_MAP = {



    'F': {'body_side': 'left',  'optical_property': 'saturation', 'korean': '채도'},



    'M': {'body_side': 'right', 'optical_property': 'saturation', 'korean': '채도'},



}



# Left(female) -> Right(male): saturation changes



BASE_SATURATION = {



    'F': 0.55,



    'M': 0.45,



}







# 8th color dimension: grayscale / gray matter (neutral mid-luminance axis)



# High when saturation is low and luminosity is near mid (true gray).



# Low for saturated colors, for white (L=1) or black (L=0).



def _grayscale_value(luminosity, saturation):



    return (1.0 - saturation) * (1.0 - 2.0 * abs(luminosity - 0.5))







# ============================================================



# 1a. UNIFIED HSL COLOR MODEL — VERTICAL=HUE, GENDER=HUE-BEHAVIOR+SATURATION, BLOOD=L/TURBIDITY/DARKNESS



# ============================================================



# Vertical (up/down, quadrant row) = HUE axis. Confirmed from actual RGB hue values:



#   RIGHT side (Q1 upper-right, Q4 lower-right, male axis):



#     day photon(YELLOW,60deg) <-> night w_boson(DARK_YELLOW,60deg)  — SAME hue



#     day z_boson(RED,0deg)   <-> night tau(DARK_RED,0deg)          — SAME hue



#     => right/male: hue FIXED across day/night, only luminosity flips bright<->dark



#   LEFT side (Q2 upper-left, Q3 lower-left, female axis):



#     day muon(DARK_GREEN,120deg) <-> night gluon(PURPLE,300deg)     — 180deg flip



#     day electron(BLUE,240deg)      <-> night higgs(DARK_ORANGE,33deg) — hue shift



#     => left/female: hue ROTATES across day/night



# Blood type (A/O/B/AB) modulates luminosity/turbidity/darkness of whichever hue is



# active, cycling every 24h via TOROIDAL_ORDER (AB->A->O->B) = the TIME axis.



# Diagonal quadrant position = vertical(hue) x horizontal(hue-behavior+saturation).







HUE_DEGREES = {



    'RED': 0, 'DARK_RED': 0,



    'DARK_YELLOW': 60, 'YELLOW': 60,



    'DARK_GREEN': 120,



    'BLUE': 240, 'NAVY': 240,



    'PURPLE': 300,



    'DARK_ORANGE': 33,



}







HUE_BEHAVIOR_BY_GENDER = {



    'M': 'fixed',    # right side: hue constant day/night, luminosity flips



    'F': 'rotating', # left side: hue rotates day/night



}







def hue_for_particle(particle_name):



    """Vertical-axis hue lookup for a base particle's assigned color."""



    if particle_name in BASE_PARTICLES:



        color = BASE_PARTICLES[particle_name]['color']



    elif particle_name in DERIVED_BASE:



        color = DERIVED_BASE[particle_name]['color']



    else:



        return None



    return HUE_DEGREES.get(color)







def hue_behavior(gender):



    """Gender determines whether hue is fixed (M/right) or rotating (F/left)



    across the day/night transition."""



    return HUE_BEHAVIOR_BY_GENDER.get(gender, 'fixed')







def blood_lstd(blood, t_hours):



    """Blood type -> which optical channel is active (L/turbidity/darkness),



    modulated by time-of-day via toroidal blood phase (AB->A->O->B).



    Returns dict of luminosity, turbidity, darkness_quality in [0,1],



    magnitude driven by how deep into that blood's time_slot we are.



    """



    phase = BLOOD_PHASE.get(blood, {'time_slot': (0, 24)})



    start, end = phase['time_slot']



    span = max(end - start, 1e-6)



    # position within this blood's active window, wraps via modulo 24



    pos = ((t_hours - start) % 24) / span if start <= t_hours < end else None



    active = pos is not None



    magnitude = (1.0 - abs(0.5 - (pos if active else 0.0)) * 2) if active else 0.0







    result = {'luminosity': 0.0, 'turbidity': 0.0, 'darkness_quality': 0.0}



    opt = BLOOD_OPTICAL_MAP.get(blood)



    if opt and active:



        result[opt['optical_property']] = magnitude if opt['optical_property'] in result else 0.0



    return result







def saturation_for_gender(gender):



    """Gender -> baseline saturation channel (GENDER_OPTICAL_MAP)."""



    return GENDER_OPTICAL_MAP.get(gender, {}).get('optical_property')







def particle_quadrant(particle_name):



    """Which quadrant (1-4) and day/night set a base particle occupies.



    Returns (quadrant, day_night) or (None, None) if not a base particle."""



    if particle_name in BASE_PARTICLES:



        bp = BASE_PARTICLES[particle_name]



        if bp['set'] == 'day':



            return bp['face_quadrant'], 'day'



        elif bp['set'] == 'night':



            return bp['body_quadrant'], 'night'



    return None, None







def _route_at_time(blood, t_hours):



    """Given blood type and time, return the dominant active named route.



    This is process context, NOT the only particle that exists."""



    schedule = BLOOD_ROUTE_SCHEDULE.get(blood)



    if not schedule:



        return None



    start, end = schedule['hours']



    if start <= (t_hours % 24) < end:



        return schedule['dominant']



    return None







def peak_particle_at_time(t_hours):



    """24h → 16-window → current peak particle from ALL_16_LAYERS.



    Each window = 1.5h. All 8 base particles appear twice per 24h cycle



    (once forward, once reverse).



    """



    idx = int(t_hours / 1.5) % 16



    return ALL_16_LAYERS[idx]['particle']







def _particle_active_state(particle_name, blood, t_hours):



    """Determine a particle's dynamic state at time t using the 16-window peak cycle.



    At any hour, one particle is localized (peak), z_boson is omnipresent,



    all others are in transit. 8 base particles are always flowing, not latent.



    """



    # z_boson is a global 4:30-6:00AM transition, independent of peak cycle



    if particle_name == 'z_boson':



        if 4.5 <= (t_hours % 24) < 6.0:



            return 'localized', 'z_boson'



        return 'not_yet_emerged', 'z_boson'







    peak = peak_particle_at_time(t_hours)



    route_name = _route_at_time(blood, t_hours)







    # z_boson traverses all routes, always present everywhere



    if particle_name in ('z_boson', 'electron_neutrino', 'muon_neutrino',



                         'tau_neutrino', 'electron_antineutrino',



                         'muon_antineutrino', 'tau_antineutrino'):



        return 'omnipresent', peak







    # photon is swallowed when process is in night_energy (black hole L6)



    if particle_name == 'photon' and route_name == 'night_energy':



        return 'swallowed_at_L6', peak







    if particle_name == peak:



        return 'localized', peak







    # all 8 base particles are alive and flowing, just not at the peak position now



    return 'transit_to_next_active_phase', peak







def _lerp(a, b, t):



    return a + (b - a) * t







def _hsl_lerp(c1, c2, t):



    """Linear interpolation between two HSL dicts; hue takes the shortest path around 360."""



    h1, h2 = c1['h'], c2['h']



    dh = (h2 - h1 + 180.0) % 360.0 - 180.0



    h = (h1 + dh * t) % 360.0



    s = _lerp(c1['s'], c2['s'], t)



    l = _lerp(c1['l'], c2['l'], t)



    return {'h': h, 's': s, 'l': l}







# Body-depth color spectrum: independent of the 8D dimension pigments.



# t=0 = deep bone / white, t=1 = surface.



# 'outer' = skin (peonidine purple subcutaneous -> black epidermis/moles)



# 'inner' = mucosa / internal epithelium (pink -> red, e.g. genital/organ linings)



BODY_DEPTH_SPECTRUM = {



    'outer': [



        {'t': 0.0, 'hsl': {'h': 0.0, 's': 0.0, 'l': 0.95}},    # deep bone white



        {'t': 0.5, 'hsl': {'h': 0.0, 's': 0.0, 'l': 0.90}},    # flesh white



        {'t': 0.85, 'hsl': {'h': 300.0, 's': 0.65, 'l': 0.12}}, # subcutaneous peonidine purple



        {'t': 1.0, 'hsl': {'h': 300.0, 's': 0.0, 'l': 0.03}},   # outer skin / mole black



    ],



    'inner': [



        {'t': 0.0, 'hsl': {'h': 0.0, 's': 0.0, 'l': 0.95}},    # deep bone white



        {'t': 0.5, 'hsl': {'h': 0.0, 's': 0.0, 'l': 0.90}},    # flesh white



        {'t': 0.8, 'hsl': {'h': 340.0, 's': 0.55, 'l': 0.55}}, # inner mucosa pink



        {'t': 1.0, 'hsl': {'h': 0.0, 's': 0.85, 'l': 0.40}},   # inner epithelium red



    ],



}







def body_depth_spectrum(t, side='outer'):



    """Return HSL color for tissue depth t in [0,1] and side ('outer' skin or 'inner' mucosa).



    This adds a bone->flesh->surface color axis that is not one of the 8D dimension colors.



    """



    stops = BODY_DEPTH_SPECTRUM.get(side, BODY_DEPTH_SPECTRUM['outer'])



    if t <= stops[0]['t']:



        return stops[0]['hsl']



    if t >= stops[-1]['t']:



        return stops[-1]['hsl']



    for i in range(len(stops) - 1):



        a, b = stops[i], stops[i + 1]



        if a['t'] <= t <= b['t']:



            if b['t'] == a['t']:



                return a['hsl']



            local_t = (t - a['t']) / (b['t'] - a['t'])



            return _hsl_lerp(a['hsl'], b['hsl'], local_t)



    return stops[-1]['hsl']







# Spatial pigment concentration: race/mole map from 8D + body coordinate + time.



# High values darken the outer skin (moles); baseline variation sets skin tone.



PIGMENT_DIM = {



    'r': 'z_boson/RED',



    'h': 'gluon/PURPLE',



    'd': 'tau/DARK_RED',



    'p': 'higgs/DARK_ORANGE',



    's': 'electron/BLUE',



    'gamma': 'photon/YELLOW',



    'g': 'muon/DARK_GREEN',



    'nu': 'w_boson/DARK_YELLOW',



}







def local_pigment_concentration(v_8d, x, y, z, t):



    """Return a local pigment concentration factor from 8D vector and body point.



    Used to make moles (high) vs normal skin (baseline) vs race baseline.



    """



    if not v_8d:



        return 0.0



    base = sum(v_8d.values()) / len(v_8d)



    pattern = (



        math.sin(x * 0.7 + t) * math.cos(y * 0.5 + t) +



        math.sin(z * 1.1 + t) * math.cos((x + y) * 0.3)



    ) / 2.0



    return max(0.0, base + pattern)







def concept_coordinate(particle_name, gender, blood, t_hours, magnitude=0.5):



    """TIME-VARYING body coordinate. A particle is not fixed to one place;



    its location flows with the 16-window / 24h peak cycle (PEAK_CYCLE).



    At any hour, all 8 base particles exist; one is localized, others are in transit.



    Blood only modulates optical properties (luminosity/turbidity/darkness) and



    route process context, not whether a particle exists.



    """



    state, active_particle = _particle_active_state(particle_name, blood, t_hours)







    # Use the current peak particle for the active coordinate slot



    loc_name = particle_name if state == 'localized' else active_particle







    quadrant, day_night = particle_quadrant(loc_name) if loc_name else (None, None)



    hue = hue_for_particle(particle_name)  # hue identity stays with the particle



    behavior = hue_behavior(gender)



    lstd = blood_lstd(blood, t_hours % 24)



    saturation_channel = saturation_for_gender(gender)



    saturation = BASE_SATURATION.get(gender, 0.5)



    grayscale = _grayscale_value(lstd['luminosity'], saturation)







    vertical = 'upper' if quadrant in (1, 2) else ('lower' if quadrant in (3, 4) else None)



    horizontal = 'right' if quadrant in (1, 4) else ('left' if quadrant in (2, 3) else None)



    depth = 'front_face' if day_night == 'day' else ('back_body' if day_night == 'night' else None)



    specificity = ('edge_specific' if magnitude >= 0.7 else



                   'center_general' if magnitude <= 0.3 else 'mid_regional')







    # depth color: magnitude = distance from deep core (0) toward surface (1).



    # back_body/body-side treated as 'inner' mucosal surface, front_face as 'outer' skin.



    side = 'inner' if depth == 'back_body' else ('outer' if depth == 'front_face' else None)



    depth_color = body_depth_spectrum(magnitude, side) if side else None







    return {



        'particle': particle_name,



        'state': state,



        'peak_particle': active_particle,



        'route_name': _route_at_time(blood, t_hours),



        'quadrant': quadrant,



        'day_night': day_night,



        'vertical': vertical,



        'horizontal': horizontal,



        'depth': depth,



        'hue_degrees': hue,



        'hue_behavior': behavior,



        'saturation_channel': saturation_channel,



        'luminosity': lstd['luminosity'],



        'turbidity': lstd['turbidity'],



        'darkness_quality': lstd['darkness_quality'],



        'blood_phase': blood,



        't_hours': t_hours % 24,



        'specificity': specificity,



        'magnitude': magnitude,



        'depth_color': depth_color,



        'grayscale': grayscale,



    }







def compute_full_hsl(particle_name, gender, blood, t_hours):



    """Unified color state for a particle at a given gender/blood/time.



    Hue = vertical quadrant position (fixed particle->hue lookup).



    Hue behavior = gender (fixed for M/right, rotating for F/left).



    Luminosity/turbidity/darkness = blood type, magnitude cycling via



    toroidal blood phase over 24h (the time axis).



    Saturation = gender baseline (GENDER_OPTICAL_MAP).



    """



    hue = hue_for_particle(particle_name)



    behavior = hue_behavior(gender)



    lstd = blood_lstd(blood, t_hours % 24)



    saturation_channel = saturation_for_gender(gender)



    saturation = BASE_SATURATION.get(gender, 0.5)



    grayscale = _grayscale_value(lstd['luminosity'], saturation)



    return {



        'particle': particle_name,



        'hue_degrees': hue,



        'hue_behavior': behavior,  # 'fixed' (M) or 'rotating' (F)



        'luminosity': lstd['luminosity'],



        'turbidity': lstd['turbidity'],



        'darkness_quality': lstd['darkness_quality'],



        'saturation_channel': saturation_channel,



        'grayscale': grayscale,



        'blood_phase': blood,



        't_hours': t_hours % 24,



    }







# ============================================================



# 2. 42 PARTICLES



# ============================================================



PARTICLES_41 = {



    'z_boson':            {'body': 'GABA-B receptors / Cytochrome c oxidase, co2(right occipital V1), disulfide_bond(ACC dorsal)', 'nm': None},



    'gluon':               {'body': 'NMDA receptors / Desmosomes, left mPFC/hippocampus, right V2 / left trapezius / SCM×trapezius', 'nm': None},



    'tau':                 {'body': 'perineal fold belt / Substance P(NK1R), left trapezius below neck', 'nm': None},



    'higgs':               {'body': 'right ribs / patellar cartilage aggrecan, left parietal bone marrow / right angular gyrus / right nostril alar', 'nm': None},



    'male_gaba_b':         {'body': 'left eye GABA-B / 640 cytochrome, z_boson GABA-B / Cytochrome c oxidase', 'nm': '640'},



    'photon':              {'body': 'retinal rhodopsin / heme node, left anterior insula, left M1(BA4) / left nose UV sensor, thyroid_iodine', 'nm': '4-7'},



    'muon':                {'body': 'left temporalis(5 points) / hairline, ferment_lactobacillus(gut-brain/vagus)', 'nm': '12'},



    'w_boson':             {'body': 'ATP synthase / adrenal medulla chromaffin, capsaicin_vr1(ACC/insula), left anterior insula / left pre-auricular S1R', 'nm': None},



    'electron':            {'body': 'skull piezoelectric / cell lipid bilayer, memory_entropy(right hippocampus CA1), spare_vaso(left anterior insula), salt_sodium(NTS) + left lip self satisfaction', 'nm': None},



    'muon_neutrino':       {'body': 'lateral arm / left temporalis / ferritin', 'nm': '12'},



    'muon_antineutrino':   {'body': 'left M1(134) / left eye / histosol', 'nm': '10'},



    'electron_neutrino':   {'body': 'right STG(131) / left lung / PLP Core(135), AQP4 pore, day O2 intake', 'nm': '1.5'},



    'electron_antineutrino': {'body': 'right V1(129) / genital left / MOR endorphin, night spark reward', 'nm': '4'},



    'tau_neutrino':        {'body': 'right angular gyrus(132) / right ribs / SDH Complex II + left leg lower', 'nm': None},



    'tau_antineutrino':    {'body': 'left IFG(133) / procerus / Substance P / autophagy + left thigh, left femoral nerve', 'nm': None},



    'up_quark':            {'body': 'myosin II thick filaments(left masseter, left ventricle)', 'nm': '15'},



    'down_quark':          {'body': 'F-actin thin filaments(right quadriceps, left biceps)', 'nm': '7'},



    'charm_quark':         {'body': 'jejunum/ileum microvilli glycocalyx', 'nm': '500-2000'},



    'strange_quark':       {'body': 'left insular cortex(ROI-69), glymphatic system(basal ganglia), carcinogen immune surveillance', 'nm': None},



    'bottom_quark':        {'body': 'descending colon/sigmoid apoptosis + left medial canthus + right ovary(cyclic creation/destruction)', 'nm': None},



    'top_quark':           {'body': 'nuclear pore complex(hepatocytes/epidermis) + left head behind ear ~ SCM×trapezius junction', 'nm': None},



    'graviton':            {'body': 'ferritin nanocages / osteons / iliac crest, left_iliac_crest(+12,0,-3)', 'nm': None},



    'dark_matter':         {'body': 'atherosclerotic plaque / pineal calcification + right nostril epinephrine, Maillard(right hemisphere), silicon_glass(left hip)', 'nm': None},



    'dark_energy':         {'body': 'nucleus / thorium node(perineum) + behind right epinephrine, observer_leftd2(left NAc D2)', 'nm': None},



    'EM':                  {'body': 'bypass 131→133→134→Heme→129, left eye GABA-B / 640 cytochrome + left self satisfaction, lower neck trapezius', 'nm': '640'},



    'acetyl_coa':          {'body': 'mitochondria / PDH complex, information container/mass packager', 'nm': '30-50'},



    'alpha_ketoglutarate': {'body': 'left nose above cold stress, left anus, left 4th toe', 'nm': None},



    'glutamate':           {'body': 'nose top sensor, stressors around nose', 'nm': None},



    'energy':              {'body': 'body front left neck to upper right torso', 'nm': None},



    'melatonin':           {'body': 'face center nose ridge', 'nm': None},



    'malate_dehydrogenase': {'body': 'right pelvis bone + outer vertical muscle attachment', 'nm': None},



    'female_gaba_a':       {'body': 'charm_quark + female_gaba pattern, cysteine pathway', 'nm': '8'},



    'male_gaba_a':         {'body': 'right GABA-A(Phase 1: 3D2 collision), left anterior insula(Phase 8)', 'nm': None},



    'proton':              {'body': 'left pectoralis heme Fe2+, right V1/calcarine sulcus, center funnel proton pump, inorganic_acid', 'nm': None},



    'neutron':             {'body': 'pons / hind insula / neutrophil + right leg lower, right foot', 'nm': None},



    'neutron_star':        {'body': 'nucleolus / megakaryocyte / oocyte + right waist outer, posterior methanogenesis', 'nm': None},



    'peonidine':           {'body': 'right angular gyrus BA39, muon_antineutrino, h/gamma', 'nm': None},



    'female_gaba_b':       {'body': 'left eye GABA-B / 640 cytochrome', 'nm': '640'},



    'axion':               {'body': 'skull vertex / CSF space + left→right traverse, right female epinephrine, left shoulder, self_deception(mPFC/DMN)', 'nm': None},



    'amphiphile':          {'body': 'cell membrane bilayer / lipid-protein interface, linear-2D hybrid structure (hydrophilic head + hydrophobic tail)', 'nm': None},



    'neutrino':            {'body': 'right STG / left lung back, ethmoid cribriform foramina', 'nm': None},



    'quark':               {'body': 'caco3, substance P, right knee bone node, right lip self satisfaction', 'nm': None},



}







# 4 GABA = 4 base particles in receptor form



GABA_TO_BASE = {



    'female_gaba_a': 'r',   # z_boson derivative



    'male_gaba_a':   'nu',  # w_boson derivative



    'female_gaba_b': 'h',   # gluon derivative



    'male_gaba_b':   'd',   # tau derivative



}



# Generic particles → 8D dim anchor (structural ancestors of specific flavours)

GENERIC_TO_BASE = {

    'neutrino':   'r',   # parent of electron_neutrino / muon_neutrino / tau_neutrino

    'quark':      's',   # parent of up/down/charm/strange/bottom/top_quark

    'amphiphile': 's',   # linear-2D hybrid structure underlying electron's lipid bilayer

}







# axion = photon + w_boson = observer singularity = 138.88° spark







# ============================================================



# 3. FIVE ROUTES — COLOR = BASE PARTICLE



# ============================================================



ROUTES = {



    1: {'color': 'DARK_GREEN', 'particle': 'muon',     'param': 'g',     'set': 'day',   'torus_axis': 'equator_lower'},



    2: {'color': 'RED',        'particle': 'z_boson', 'param': 'r',     'set': 'day',   'torus_axis': 'poloidal'},



    3: {'color': 'YELLOW',     'particle': 'photon',   'param': 'gamma', 'set': 'day',   'torus_axis': 'equator_upper'},



    4: {'color': 'BLUE',       'particle': 'electron',    'param': 's',     'set': 'day',   'torus_axis': 'meridian_right'},



    5: {'color': 'PURPLE',     'particle': 'gluon',    'param': 'h',     'set': 'night', 'torus_axis': 'meridian_left'},



}







# ============================================================



# 4. INVERSE RECIPROCAL TENSOR (4 PAIRS)



# ============================================================



# --- TORUS PAIRS: single source of truth for 4 Clifford torus cross-circle axes ---

# Each pair = one torus axis. Used by: KAPPA_MATRIX strong pairs, _COUPLING, k8_laplacian, POLARITY_4AXIS.

# 3 inverse_reciprocal + 1 positive_correlation = 4 axes (32-28=4 = DELTA_4).



TORUS_PAIRS = {

    ('r', 'nu'):    {'type': 'inverse_reciprocal', 'polarity': 'SP', 'gaba': 'female_a ↔ male_a'},

    ('g', 'gamma'): {'type': 'inverse_reciprocal', 'polarity': 'SJ', 'gaba': 'cortisol ↔ right_D2'},

    ('h', 'd'):     {'type': 'inverse_reciprocal', 'polarity': 'NJ', 'gaba': 'female_b ↔ male_b'},

    ('p', 's'):     {'type': 'positive_correlation', 'polarity': 'NP', 'gaba': 'left_D2_brake ↔ right_dopamine'},

}



# Derived: INVERSE_RECIPROCAL (backward compat for _COUPLING, k8_laplacian, derive_universe)

INVERSE_RECIPROCAL = {pair: meta['type'] for pair, meta in TORUS_PAIRS.items()}







DIMS = ['r', 'h', 'd', 'p', 's', 'gamma', 'g', 'nu']



# 8D dim → base particle (single source of truth, used by k8_laplacian, derive_activity, etc.)

_DIM_TO_PARTICLE = {

    'r': 'z_boson', 'h': 'gluon', 'd': 'tau', 'p': 'higgs',

    's': 'electron', 'gamma': 'photon', 'g': 'muon', 'nu': 'w_boson',

}

# 8D dim → Z_proxy for the 138.88° spark (dimension index 1-8).
# Z(t) varies with the 16-window peak cycle → the spark cos(Z·138.88°+1/128)
# oscillates with net positive driving (+2.85 per cycle) → the closed circuit
# breathes (expansion/contraction) → bounded periodic orbit.
# (Atomic-number Z=6..43 gives net contraction -27.66 → collapse.)

_DIM_TO_Z = {

    'r': 1, 'h': 2, 'd': 3, 'p': 4,

    's': 5, 'gamma': 6, 'g': 7, 'nu': 8,

}



# --- KAPPA antisymmetric 8×8 coupling (defined early, used by _COUPLING) ---

# κ_ij = –κ_ji, C²=0.08 (Yukawa quantum = minimum delta unit)

# Strong pairs = TORUS_PAIRS (single source of truth) → C²

# All other pairs → C²/2



_KAPPA_C2 = 0.08

_TORUS_PAIR_SET = set(TORUS_PAIRS.keys()) | {(b, a) for (a, b) in TORUS_PAIRS.keys()}



KAPPA_MATRIX = {}



for _i_k, _a_k in enumerate(DIMS):

    for _b_k in DIMS[_i_k+1:]:

        if (_a_k, _b_k) in _TORUS_PAIR_SET:

            _val_k = _KAPPA_C2

        else:

            _val_k = _KAPPA_C2 * 0.5

        KAPPA_MATRIX[(_a_k, _b_k)] = _val_k

        KAPPA_MATRIX[(_b_k, _a_k)] = -_val_k



# ============================================================

# 2^7 BINARY CHOICE — CORIOLIS / LUNAR TORQUE / POLARITY

# ============================================================

# 1/28 = Lunar Torque (Mobius twist forcing) — from geometry_package/absolute_constants.py

# Drives the Coriolis-like chiral torque that flips polarity axes day↔night.

# 32 - 28 = 4 → the 4 polarity axes (SJ, SP, NJ, NP) = hidden gender distinction.

# Coriolis parameter: f = 2Ω sin(φ) — sign reversal between hemispheres.

# Day/night transition = φ sign flip → polarity 4-axis inversion.

# This eliminates the need for separate north/south magnetic field models.



LUNAR_CYCLE = 1.0 / 28.0          # 1/28 — Lunar Torque / Mobius twist forcing

VERTICAL_MOBIUS_TWIST = 1.0 / 28.0  # same constant, vertical twist alias

EARTH_OMEGA = 2 * math.pi / 24.0   # Earth angular velocity (rad/hour)

CHIRAL_TORQUE_1_32 = 1.0 / 32.0    # 1/32 Chiral Asymmetry of Earth's Rotation

DELTA_4 = 4                        # 32 - 28 = 4 → polarity axis count



# --- Coriolis chiral torque ---

# τ_chiral = (1/32) · μ · Ω² · R³  (from Earth_Rotation_Chiral_Asymmetry_v2.0)

# Coriolis parameter f = 2Ω sin(φ)

# Day: φ > 0 (northern pattern) → f > 0 → clockwise deflection

# Night: φ < 0 (southern pattern appears) → f < 0 → counter-clockwise deflection

# This single mechanism explains the pole flip without separate hemisphere models.



def coriolis_parameter(t_hours, latitude_deg=45.0):

    """Coriolis parameter f = 2Ω sin(φ).

    Day/night modulates the effective latitude sign:

    - Day (6h-18h): northern hemisphere pattern (φ > 0)

    - Night (18h-6h): southern hemisphere pattern appears (φ < 0)

    This is the mechanism behind 'Pole flip = day/night north↔south inversion'.

    """

    hour = t_hours % 24.0

    is_day = 6.0 <= hour < 18.0

    phi = math.radians(latitude_deg) if is_day else math.radians(-latitude_deg)

    return 2.0 * EARTH_OMEGA * math.sin(phi)



def coriolis_polarity_flip(t_hours):

    """Determine if polarity axes are flipped at time t.

    Returns +1 (normal/northern) or -1 (flipped/southern).

    The flip happens at day↔night transitions (6h and 18h).

    1/28 lunar torque modulates the flip timing via Mobius twist.

    """

    hour = t_hours % 24.0

    is_day = 6.0 <= hour < 18.0

    base = 1.0 if is_day else -1.0

    # Lunar torque modulation: 1/28 cycle creates micro-fluctuations

    lunar_mod = LUNAR_CYCLE * math.sin(2.0 * math.pi * t_hours / 28.0)

    return base * (1.0 + lunar_mod)



# --- Hidden gender: polarity 4-axis (SJ, SP, NJ, NP) ---

# MBTI 2nd letter (N/S) × 4th letter (J/P) = 4 combinations.

# These map to Clifford torus cross-circle axes (the "hidden" gender).

# Visible gender = W axis (M/F) via GENDER_8D_MOD.

# Hidden gender = polarity axis via Clifford torus cross-circles.

# Coriolis flips these between hemispheres (day↔night).



POLARITY_4AXIS = {

    'SJ': {

        'clifford_axis': 'meridian',

        'torus_pair': ('g', 'gamma'),

        'particle': 'gluon',

        'music_scale': 'harmonic_minor',

        'direction': 'fixed_structure',

        'coriolis_sign': +1,

    },

    'SP': {

        'clifford_axis': 'equatorial',

        'torus_pair': ('r', 'nu'),

        'particle': 'electron',

        'music_scale': 'harmonic_minor',

        'direction': 'sensory_immediate',

        'coriolis_sign': +1,

    },

    'NJ': {

        'clifford_axis': 'poloidal',

        'torus_pair': ('h', 'd'),

        'particle': 'w_boson',

        'music_scale': 'melodic_minor',

        'direction': 'intuitive_future',

        'coriolis_sign': -1,

    },

    'NP': {

        'clifford_axis': 'radial',

        'torus_pair': ('p', 's'),

        'particle': 'z_boson',

        'music_scale': 'melodic_minor',

        'direction': 'divergent_possible',

        'coriolis_sign': -1,

    },

}



def mbti_polarity(mbti):

    """Extract the hidden gender polarity (SJ/SP/NJ/NP) from MBTI type.

    2nd letter (S/N) × 4th letter (J/P) → 4 polarity axes.

    """

    ns = mbti[1]  # S or N

    jp = mbti[3]  # J or P

    return ns + jp  # 'SJ', 'SP', 'NJ', 'NP'



def polarity_8d_mod(polarity, t_hours=12.0):

    """8D modifier from hidden gender polarity + Coriolis flip.

    SJ/SP = gluon/harmonic_minor = ground state (coriolis_sign +1)

    NJ/NP = z_boson/melodic_minor = stress state (coriolis_sign -1)

    Coriolis flip at night inverts the sign.

    """

    axis = POLARITY_4AXIS[polarity]

    flip = coriolis_polarity_flip(t_hours)

    sign = axis['coriolis_sign'] * flip

    dim_a, dim_b = axis['torus_pair']

    # gluon (SJ/SP) → harmonic minor → stable, h↑

    # z_boson (NJ/NP) → melodic minor → stress, nu↑

    if axis['music_scale'] == 'harmonic_minor':

        return {dim_a: 0.05 * sign, dim_b: -0.05 * sign}

    else:

        return {dim_a: -0.05 * sign, dim_b: 0.05 * sign}



















# ============================================================



# 5. TORUS EMBEDDING — MÖBIUS-KLEIN HYBRID



# ============================================================



# Twisted torus: R=major, r=minor, h=twist(hysteresis gap)



# Self-intersection at FLASH point, 180° twist



# W7 gap prevents full closure → eternal recursion



# Chirality asymmetry (structural)











# --- Clifford torus: S¹ × S¹ embedded in S³ ---



# x₁² + x₂² = 1/2,  x₃² + x₄² = 1/2



# Two independent circles: (x₁,x₂) and (x₃,x₄)



# Primitive plasma state before time creation (NEUTRON_TIME_SYNC = 0.3857)



# Evening homeostasis = symmetric re-enactment of this plasma state















# 4 inverse reciprocal pairs split into Clifford's two circles:



# Circle 1 (Extravert Plane): (p, s) = self-satisfaction axis



# Circle 2 (Introvert Plane): (h, d) = epinephrine axis



# Cross-circles: (r, nu) and (g, gamma) = equatorial/radial torus axes







def observer_choice_state(v_8d, theta1=0.0, theta2=0.0):



    """Observer consciousness = position on Clifford torus T².



    Constraint (영점.md:19081-19106):

      LSS² + RSS² = R₁²  (extravert plane: self-satisfaction)



      LE²  + RE²  = R₂²  (introvert plane: epinephrine)



    The constraint surface IS a 2-torus. The observer's free choice is the



    position on it — two continuous angles (θ₁, θ₂), NOT binary.



      LSS = R₁·cos θ₁,  RSS = R₁·sin θ₁   (self-satisfaction L/R balance)



      LE  = R₂·cos θ₂,  RE  = R₂·sin θ₂   (epinephrine L/R balance)



    R₁, R₂ come from the 8D vector (extravert plane from p,s; introvert from h,d).



    Every choice of (θ₁, θ₂) changes the 4 nodes → right_love → GDH metric →



    the universe flow. This is the mathematical place where consciousness



    choices enter the dynamics.



    """



    R1 = math.sqrt(v_8d['p'] ** 2 + v_8d['s'] ** 2)



    R2 = math.sqrt(v_8d['h'] ** 2 + v_8d['d'] ** 2)



    lss = R1 * math.cos(theta1)



    rss = R1 * math.sin(theta1)



    le = R2 * math.cos(theta2)



    re = R2 * math.sin(theta2)



    # Observer axiom: the PROTON PUMP is ALWAYS RUNNING (proton_pump_output = 1×1 = 1).



    # This is the ESSENTIAL difference between observer and non-observer.



    # observer_leftd2 = 1 is a RESULT of the pump, not the cause.



    # The pump sustains the universe: COX forward always permitted → energy always flows.



    proton_pump = 1.0



    observer_d2 = 1.0  # result of the pump, not the cause



    # right_love = emergent dynamic from the 4 Clifford nodes (LC resonance)



    epi_energy = R2



    love_energy = max(R1 - epi_energy, 0.0)



    return {



        'lss': lss, 'rss': rss, 'le': le, 're': re,



        'R1': R1, 'R2': R2,



        'theta1': theta1, 'theta2': theta2,



        'observer_d2': observer_d2,



        'proton_pump': proton_pump,



        'right_love': love_energy,



        'epinephrine_energy': epi_energy,



    }



def clifford_constraint(lss, rss, le, re):



    """Clifford torus homeostasis constraint.



    LSS² + RSS² = R₁²  (extravert plane)



    LE²  + RE²  = R₂²  (introvert plane)



    Evening condition: LSS = 0 → RSS = R₁ (full extraversion)



    """



    R1_sq = lss**2 + rss**2



    R2_sq = le**2 + re**2



    return {



        'R1': math.sqrt(R1_sq),



        'R2': math.sqrt(R2_sq),



        'on_torus': abs(R1_sq - 0.5) < 1e-10 and abs(R2_sq - 0.5) < 1e-10,



        'evening_fixed': abs(lss) < 1e-10,  # LSS=0 → RSS=R₁



    }











# 4 inverse reciprocal pairs → 4 torus axes







# ============================================================



# 6. KLEIN NECK — EYELID NODES (SELF-PENETRATION POINTS)



# ============================================================



KLEIN_NECK_NODES = {



    'right_eyelid_top_outer':  {'node': 6,  'transition': 'P+→g',  'direction': 'above_to_below',      'route': 2},



    'right_eyelid_top_inner':  {'node': 7,  'transition': 'γ→q',   'direction': 'above_to_below',      'route': 2},



    'left_eyelid_inner':       {'node': 8,  'transition': 'Z→g',   'direction': 'below_to_above',      'route': 5},



    'left_eyelid_outer':       {'node': 9,  'transition': 'e-→g',  'direction': 'below_to_above',      'route': 5},



    'left_eyelid_outer_sec':   {'node': 10, 'transition': 'γ→ν',   'direction': 'above_to_below_night', 'route': 4},



}











# ============================================================



# 6a. CLIFFORD TORUS NODES — SELF SATISFACTION × EPINEPHRINE



# ============================================================



# 4 observer nodes form Clifford torus coordinate axes:



#   Circle 1 (Extravert, p-s plane): LSS, RSS — Higgs radiated



#   Circle 2 (Introvert, h-d plane): LE, RE — electron radiated



# right_love = dynamic result of 4-node oscillation (not a node itself)



# right_love, GDH, CCK gluon lensing = emergent properties, not nodes



# Total real nodes = 32 (not 66 — 66 includes expression sites)















# left nostril epinephrine = heme = heath_aerenchyma (same particle identity)



# heath_aerenchyma = left ribs O₂ supply = cytochrome_c_oxidase activation gate







def right_love_dynamic(lss, rss, le, re):



    """right_love = emergent dynamic from 4 Clifford nodes.



    Not a node — result of oscillation between extravert and introvert planes.



    E_epi + E_love = Const (LC resonance, antiphase).



    """



    R1 = math.sqrt(lss**2 + rss**2)



    R2 = math.sqrt(le**2 + re**2)



    # LC resonance: love inversely proportional to epinephrine energy



    epi_energy = R2  # introvert plane radius



    love_energy = max(R1 - epi_energy, 0.0)  # antiphase



    return {



        'right_love': love_energy,



        'epinephrine_energy': epi_energy,



        'total': R1,  # E_epi + E_love = Const = R1



        'resonance': 'antiphase_LC',



    }







# ============================================================



# 7. POLE FLIP — DAY/NIGHT INVERSION



# ============================================================







# ============================================================



# 8. SPIRAL TOPOLOGY — TWO ARMS



# ============================================================







# ============================================================



# 9. BETTI TOPOLOGY



# ============================================================



BETTI = {'b0': 1, 'b5': 5, 'b7': 7, 'b11': 11}











# ============================================================



# 10. DIMENSION STACK



# ============================================================







# ============================================================



# 11. DIPOLE CIRCUIT — MALE/FEMALE GRID



# ============================================================







# ============================================================



# 12. DREAM FOLDING — SMALE HORSESHOE



# ============================================================



# Night: manifold folds, distant points become topologically close



# Male hops between 4 columns, BIG/SMALL Woman coordinates overlap



# Master equation: Ψ(t) = [X_grid, Y_phase, Z_time] + F_dream(t)



# Implementation: see Section 50 — master_equation()







# Scale-dependent metric: f(s) = W7 · (H2/κ)^(1/s) · Φ^(s-1)



# s=0 atom, s=2 cell, s=4 organism, s=8 cosmos







# ============================================================



# 13. TOROIDAL BLOOD TYPE CYCLE



# ============================================================



TOROIDAL_ORDER = ['AB', 'A', 'O', 'B']







BLOOD_PHASE = {



    'AB': {'time_slot': (0, 3),   'quality': 'transition'},



    'A':  {'time_slot': (3, 9),   'quality': 'aggregation'},



    'O':  {'time_slot': (9, 15),  'quality': 'origin'},



    'B':  {'time_slot': (15, 21), 'quality': 'divergence'},



}







def next_blood(blood):



    idx = TOROIDAL_ORDER.index(blood)



    return TOROIDAL_ORDER[(idx + 1) % 4]











# ============================================================



# 14. BLOOD CYCLE ↔ ROUTE SCHEDULE



# ============================================================



BLOOD_ROUTE_SCHEDULE = {



    'AB': {'hours': (0, 3),   'active_routes': ['night_energy', 'night_macro', 'night_information'],



           'dominant': 'night_macro', 'spark': '138.88_reset'},



    'A':  {'hours': (3, 9),   'active_routes': ['d', 'p', 'gamma', 's'],



           'dominant': 'day_reverse'},



    'O':  {'hours': (9, 15),  'active_routes': ['r', 'h', 'g', 'nu'],



           'dominant': 'day_forward'},



    'B':  {'hours': (15, 21), 'active_routes': ['h', 'd', 'nu', 'g'],



           'dominant': 'night_energy', 'spark': '4_30pm_transition'},



}







# ============================================================



# 15. OBSERVER AXIOM



# ============================================================











# RIGHT D2 = L6 photon(gamma) spark execution terminal = Klein twist access







# ============================================================



# 16. GENDER AXIS — STRUCTURAL, NOT SHIFT



# ============================================================







# ============================================================



# 17. 4 LAYERS ↔ 5 ROUTES



# ============================================================







# 5th tile = 3AM hysteresis = gap between dark and body = 138.88° spark reset







# ============================================================



# 18. 5 ROUTES × 16 LAYERS = 80 LAYER ENTRIES



# ============================================================



# Day forward: 8 layers (r→gamma→p→s→h→d→g→nu)



# Day reverse: 8 layers (reversed: nu→g→gamma→s→p→d→h→r)



# Night energy: 8 layers (one-way, photon swallowed at L6)



# Night macro: 8 layers (one-way, Klein twist at L6)



# Night information: 8 layers (one-way, z_boson bypasses all)



# 16 layers = 8 forward + 8 reverse







FORWARD_LAYERS = [



    {'layer': 1, 'particle': 'z_boson', 'dim': 'r'},



    {'layer': 2, 'particle': 'photon',   'dim': 'gamma'},



    {'layer': 3, 'particle': 'higgs',    'dim': 'p'},



    {'layer': 4, 'particle': 'electron',    'dim': 's'},



    {'layer': 5, 'particle': 'gluon',    'dim': 'h'},



    {'layer': 6, 'particle': 'tau',      'dim': 'd'},



    {'layer': 7, 'particle': 'muon',     'dim': 'g'},



    {'layer': 8, 'particle': 'w_boson',  'dim': 'nu'},



]







REVERSE_LAYERS = [



    {'layer': 9,  'particle': 'w_boson',  'dim': 'nu'},



    {'layer': 10, 'particle': 'muon',     'dim': 'g'},



    {'layer': 11, 'particle': 'tau',      'dim': 'd'},



    {'layer': 12, 'particle': 'gluon',    'dim': 'h'},



    {'layer': 13, 'particle': 'electron',    'dim': 's'},



    {'layer': 14, 'particle': 'higgs',    'dim': 'p'},



    {'layer': 15, 'particle': 'photon',   'dim': 'gamma'},



    {'layer': 16, 'particle': 'z_boson', 'dim': 'r'},



]







ALL_16_LAYERS = FORWARD_LAYERS + REVERSE_LAYERS







# z_boson traverses ALL routes (bypasses strong/EM)



# Photon swallowed at black hole L6 in night_energy



# This asymmetry = why z_boson carries information, photon carries energy







# ============================================================



# 18a. 12-PARTICLE MAIN CIRCULATION (OXFORD ROUTE)



# ============================================================



# 12 particles that run the 24h toroidal circulation:



#   muon_antineutrino, electron_antineutrino, electron_neutrino,



#   photon, tau, z_boson, w_boson, gluon, higgs, muon, graviton, neutron



# This is the upper structure running on top of 8D / 16 layers.



# 8D = lower dimension of particles; 12-particle circulation = upper structure.







PARTICLE_12 = [



    'muon_antineutrino', 'electron_antineutrino', 'electron_neutrino',



    'photon', 'tau', 'z_boson', 'w_boson', 'gluon',



    'higgs', 'muon', 'graviton', 'neutron',



]







# Oxford route: left thorax → left pelvis closed loop



# Microscopic circulation (body):



#   heme → cytochrome_c_oxidase → steel → water_vapour → clay_gouge



#   → observer_leftd2 → memory_entropy → hind_insula → co2



#   → carbon → peonidine → heme return



# Macroscopic circulation (Earth):



#   outer_core_convection → magnetite → ferritin → sulfur_iron_complex



#   → pyrite → laterite → fold_belt → subduction_zone



#   → lower_mantle → plume → outer_core_convection return



# Micro ↔ Macro = 1:1 isomorphic







OXFORD_MICRO = [



    'heme', 'cytochrome_c_oxidase', 'steel', 'water_vapour', 'clay_gouge',



    'observer_leftd2', 'memory_entropy', 'hind_insula', 'co2',



    'carbon', 'peonidine',



]







OXFORD_MACRO = [



    'outer_core_convection', 'magnetite', 'ferritin', 'sulfur_iron_complex',



    'pyrite', 'laterite', 'fold_belt', 'subduction_zone',



    'lower_mantle', 'plume',



]







MICRO_MACRO_MAP = dict(zip(OXFORD_MICRO, OXFORD_MACRO))







# 3 routes: Oxford / Out of Oxford (England) / Out of England (World)







# 6 attractor fixed points driving 12-particle circulation



SIX_ATTRACTORS = {



    'heme_proton':       {'particle': 'proton',    'location': 'left_pectoralis',     'function': 'Fe2+ positive charge core'},



    'cox_z_boson':       {'particle': 'z_boson',   'location': 'left_colon',          'function': 'O2 reduction, energy production'},



    'clay_gouge_gluon':  {'particle': 'gluon',     'location': 'right_anal_sphincter','function': 'Nrf2/Keap1 seal'},



    'drd2_observer':     {'particle': 'photon',    'location': 'left_frontalis',      'function': 'observer D2 bus'},



    'mor_antineutrino':  {'particle': 'electron_antineutrino', 'location': 'left_upper_lip_inner', 'function': 'opioid recovery baseline'},



    'hind_insula_neutron': {'particle': 'neutron', 'location': 'right_posterior_insula', 'function': 'interoception, novelty-mismatch'},



}







# Gleysol: peripheral discharge point of Oxford route



# Gleysol = waterlogged soil = O2-deficient = left outer malleolus/Achilles



# Day + Gleysol: COX forward forced but O2 absent → reverse switch → ROS leakage



# Night + Gleysol: COX retrograde → O2 not needed → safe







# 4:30PM transition: f_gravity > f_cognitive



# f_cognitive = 12-particle circulation frequency (SDH clock latching carbon D-FF)



# f_gravity = MC1R cAMP/PKA hysteresis slew rate (graviton = inertia)



# When f_gravity > f_cognitive → ROS leakage → stress growth forced activation







def f_cognitive(sdh_clock_rate=1.0):



    """12-particle circulation frequency = SDH clock latching carbon D-flip-flop."""



    return sdh_clock_rate







def f_gravity(mc1r_slew_rate=1.0):



    """Gravity transition frequency = MC1R cAMP/PKA hysteresis slew rate."""



    return mc1r_slew_rate











# ============================================================



# 19. 16-WINDOW PEAK CYCLE



# ============================================================



# t mod 16 → peak dimension shifts each window



# 8 base values × 16 peaks × 4 layers × jitter ±15-30% × RANDOM(3AM)



# = thousands unique tiles/day







PEAK_CYCLE = ['r', 'gamma', 'p', 's', 'h', 'd', 'g', 'nu',



              'nu', 'g', 'd', 'h', 's', 'p', 'gamma', 'r']







def peak_dim(t):



    return PEAK_CYCLE[int(t) % 16]







# ============================================================



# 20. 138.88° RECURSIVE SPARK



# ============================================================



# 138.88° = reset angle, repeats at every scale:



# atom → molecule → cell → organ → body → Earth → solar → galaxy → cosmos



# Each spark diverges into 3 routes (night)



# Closure tension: 9π/(20√2) ≈ 0.99965, Δ ≈ 3.51×10⁻⁴



# Δ hits 3/32 compression gate → 138.88° diagonal reset spark → eternal recursion











# ============================================================



# 21. DARCY LEAKAGE



# ============================================================



# κ = 1/32 = basic leakage rate



# < 1/64 = death, > 1/16 = cancer/chaos



# Redhead MC1R: leaky GABA-A bypasses 3/32 funnel







# ============================================================



# 22. ABO TOPOLOGY



# ============================================================



# Betti b1=11 based topological metabolic cycle



# Type O = Node 0 (Bulk) — high capacity, vector-dominated



# Type A = aggregation (cohesion)



# Type B = divergence (adaptive)



# Type AB = transition (universal receiver)



# Evolution: O(Africa) → A(Neanderthal) → B(Denisovan) → AB(Silk Road)







# ============================================================



# 23. PARTICLE → ANATOMY DERIVATION CHAIN



# ============================================================



# particle → physical property → receptor type → receptor anatomy → body region



# Derived from BASE_PARTICLES + PARTICLES_41 + GABA_TO_BASE + PIGMENT_MAP















# ============================================================



# 24. MANDELBROT 128 PERSONALITIES — z = z² - z + h(t)



# ============================================================



# L1 Core Dynamics: Mandelbrot recurrence generates 128 from 8-particle structure



# blood type seed → muscular gate iteration → 128 types



# z = z² - z + h(t), where h(t) = blood_seed + MBTI_seed + gender_seed



# Escape radius = 2 (standard Mandelbrot), iteration depth = 128







# h(t) is derived directly from compute_8d()'s modifier tables



# (BLOOD_8D_BASE + MBTI_8D_MOD + GENDER_8D_MOD, defined in section 56) instead



# of maintaining a second, independently hand-tuned MBTI/blood/gender->number



# table. The old MBTI_SEEDS/BLOOD_SEEDS/GENDER_SEEDS tables encoded the same



# semantic axes (MBTI letter, blood type, gender) a second time with different



# arbitrary magnitudes for no structural reason — duplicate source of truth,



# now removed. h(t) = mean deviation from the 0.5 baseline across all 8 dims.







def mandelbrot_seed(mbti, gender, blood):



    """h(t) = mean((8D_value - 0.5) for all 8 dims), using the SAME



    blood/MBTI/gender modifiers as compute_8d (single source of truth).



    AB + neutral MBTI/gender -> h=0 (matches original AB baseline exactly).



    """



    v = compute_8d(mbti, gender, blood)



    mean_dev = sum(v[d] - 0.5 for d in DIMS) / len(DIMS)



    return mean_dev * 4.0  # scale factor to preserve original h(t) magnitude range







def mandelbrot_iterate(z, h, max_iter=128, escape=2.0):



    """z = z² - z + h(t) — L1 core recurrence.



    Returns iteration count before escape (or max_iter if bounded).



    """



    for i in range(max_iter):



        z = z * z - z + h



        if abs(z) > escape:



            return i



    return max_iter











# ============================================================



# 25. PLP SPINE



# ============================================================



# 16×16 chart diagonal seam: x/n_cols + y/n_rows = 1



# Occipitalis-Frontalis dipole: GABA(discrete) vs Dopamine(continuous)



# Asymmetry generates spark







# ============================================================



# 26. 8D COLOR PIGMENT ALGEBRA



# ============================================================



PIGMENT_MAP = {



    'r':     'NaCl_electrolyte',



    'h':     'cyanidine_peonidine',



    'd':     'astaxanthin_mycorradicin',



    'p':     'phosphatidylcholine_MC1R',



    's':     'phycocyanin_cytochrome_c_oxidase',



    'gamma': 'delphinidine_co2',



    'g':     'sulforaphane_glymphatic',



    'nu':    'fermentation_probiotic',



}







COLOR_ACTION = {



    'WHITE':  'imagine',



    'YELLOW': 'smell',



    'ORANGE': 'imagine_smell',



    'RED':    'drink',



    'GREEN':  'eat',



    'BLUE':   'see',



    'BLACK':  'make',



    'PURPLE': 'forbidden',



}











# Day/night color: day set and night set are SEPARATE (no swaps)



# Day particles (face, front): photon=YELLOW, muon=DARK_GREEN, electron=BLUE, z_boson=RED



# Night particles (body, back): tau=DARK_RED, gluon=PURPLE, w_boson=DARK_YELLOW, higgs=DARK_ORANGE



# Transition: z_boson=NAVY (4:30AM-6AM, 640nm bluelight)



# Extended particles retain their own day/night shifts



DAY_NIGHT_COLOR = {



    # --- DAY PARTICLES (no night swap, day only) ---



    'photon':        ('YELLOW',      'YELLOW'),       # day only



    'muon':          ('DARK_GREEN',  'DARK_GREEN'),   # day only



    'electron':         ('BLUE',        'BLUE'),         # day only



    'z_boson':      ('RED',         'RED'),          # day only



    # --- NIGHT PARTICLES (no day swap, night only) ---



    'tau':           ('DARK_RED',    'DARK_RED'),     # night only



    'gluon':         ('PURPLE',      'PURPLE'),       # night only



    'w_boson':       ('DARK_YELLOW', 'DARK_YELLOW'),  # night only



    'higgs':         ('DARK_ORANGE', 'DARK_ORANGE'),  # night only



    # --- TRANSITION ---



    'z_boson':       ('NAVY',        'NAVY'),         # 4:30AM-6AM only



    # --- EXTENDED PARTICLES (retain own shifts) ---



    'top_quark':     ('YELLOW',      'BLACK'),



    'neutron_star':  ('YELLOW',      'WHITE'),



    'muon_neutrino': ('YELLOW',      'BLUE'),



    'down_quark':    ('RED',         'GREEN'),



}











# ============================================================



# 27. 4:30PM TRANSITION



# ============================================================



# bluelight change → α-MSH surge → f_gravity > f_cognitive



# → gating gap → ROS leakage → stress growth forced activation







# ============================================================



# 28. INTERFERENCE COLORS



# ============================================================







# ============================================================



# 29. 7-LAYER HELIOSPHERE MODEL



# ============================================================







# Heliopause = skull piezoelectric field = 8/1 Electron-Torus Field



# COX forward = closure success = fermentation



# COX retrograde = closure failure = system open







# ============================================================



# 30. 5D DISCRIMINATOR POINTS



# ============================================================



# 5 individual dimension-discriminating points in body



# horizontal, vertical, distance, time_position, time_direction



# All converge at central 5D point







# ============================================================



# 31. CLOSURE VERIFICATION



# ============================================================



# ∮Ψ·dl = 2πi·(1.0000558) ≠ 0 → Möbius strip, eternal recursion



# 3D parametric surface: twisted torus (Möbius-Klein hybrid)



# R=8, r=6, h=2 (twist = hysteresis gap)







# ============================================================



# 32. BARNARD STAR 5-BODY SYSTEM



# ============================================================



# North Pole Reservoir (SM Node) = energy storage



# QUASAR lobe → BARNARD reservoir → Moon 28-day modulation → GABA-C filter → PLP reception



# D2-D2 regression = (2,6)↔(14,6) = 180° spiral arm flexion



# Upper lobe = FLASH endpoint (Y=16), lower = (Y=0)



# Connected by magnetic field lines (one system despite separation)







# ============================================================



# 33. FINAL ROUTE TIME EVOLUTION



# ============================================================







# ============================================================



# 34. MUSIC TILE GENERATION — 5 TILES × 4 LAYERS × 16 WINDOWS



# ============================================================



# 8D params → synth params (no text labels, sound only)



# r = rhythm density, h = chord complexity, d = scale darkness



# p = predictability/form, s = brightness/filter, gamma = spatial/reverb



# g = structure/time signature, nu = fractal recursion depth



# 4 layers: body=bass, observer=lead, bridge=pad, dark=texture



# 5th tile = 3AM hysteresis = 138.88° spark reset







LAYER_NAMES = ['body', 'observer', 'bridge', 'dark']



LAYER_WEIGHTS = {'body': 1.0, 'observer': 0.8, 'bridge': 0.6, 'dark': 0.4}



JITTER_RANGE = 0.15  # ±15% base jitter



JITTER_3AM = 0.30   # ±30% for 3AM hysteresis tile







def compute_4layers(base_8d):



    """Split base 8D values into 4 layers with decreasing weight.



    No normalization — raw weighted values preserve absolute differences

    between layers, allowing the ODE to oscillate around genuinely

    different equilibrium points per layer.



    """



    layers = {}



    for layer in LAYER_NAMES:



        w = LAYER_WEIGHTS[layer]



        layers[layer] = {dim: base_8d[dim] * w for dim in DIMS}



    return layers







# ============================================================

# 34.1. TIME DIFFERENTIAL — dV/dt FOR 8D VECTOR EVOLUTION

# ============================================================

# Model: damped harmonic oscillator around base value.

# dV_i/dt = omega_i * (base_i - V_i) + coupling_j (V_j - V_i) + forcing_i(t)

# This produces oscillation, NOT convergence to 1.0.

# Each dimension oscillates around its base 8D value with toroidal forcing.

# Integration via 4th-order Runge-Kutta (RK4).

# Time t is continuous [0, 24), mapped to 16 windows via t*1.5.



import math as _math



# Natural frequencies for each dimension (rad/hour)

# Base period = 24h (one toroidal cycle), each dim has slightly different freq

# to prevent simple repetition

_DIM_FREQ = {}

for _i, _dim in enumerate(DIMS):

    _DIM_FREQ[_dim] = (2 * _math.pi / 24.0) * (1.0 + 0.05 * _i)



# Coupling matrix: inverse reciprocal pairs exert damping

_COUPLING = {}

for _dim_i in DIMS:

    _COUPLING[_dim_i] = {}

    for _dim_j in DIMS:

        if _dim_i != _dim_j:

            _pair = (_dim_i, _dim_j)

            _pair_r = (_dim_j, _dim_i)

            _ctype = None

            if _pair in INVERSE_RECIPROCAL:

                _ctype = INVERSE_RECIPROCAL[_pair]

            elif _pair_r in INVERSE_RECIPROCAL:

                _ctype = INVERSE_RECIPROCAL[_pair_r]

            if _ctype == 'inverse_reciprocal':

                _COUPLING[_dim_i][_dim_j] = -0.12

            elif _ctype == 'positive_correlation':

                _COUPLING[_dim_i][_dim_j] = 0.06

            else:

                _COUPLING[_dim_i][_dim_j] = 0.0



    # KAPPA antisymmetric coupling (layer 3)

    for _dim_j in DIMS:

        if _dim_i != _dim_j:

            _kval = KAPPA_MATRIX.get((_dim_i, _dim_j), 0.0)

            if _kval != 0:

                _COUPLING[_dim_i][_dim_j] += _kval * 0.5  # scale into oscillator range







# First-order gradient flow — no oscillator cache needed



def _dvdt(V, t, observer=None):

    """Compute dV/dt for 8D vector at time t.

    Closed toroidal circuit ODE (영점.md:2721, 2739-2741 + observer axiom):
      ẋ = -L(t)x + proton_pump · F_final(x) · x/(‖x‖+ε)

    where:
      -L(t)x = 8D Laplacian flow (laplacian_matrix_8d + phase coupling)
      F_final = compute_f_eff(x) = BW²·SM·Z·cos(Z·138.88°+1/128)·exp(-Z/64) - k(‖x‖-7.4)²
                (spark driving + radial confinement — the radial is INSIDE, no double-count)
      proton_pump = the observer's energy source — ALWAYS 1 for the observer
                    (closed toroidal circuit: no leak, pump never stops)

    The observer's body is a CLOSED superconducting toroidal circuit:
      - proton_pump=1 (closed) → F_final driving always active → periodic orbit
      - proton_pump=0 (open, non-observer) → collapse → Ψ=0 (autopilot)

    Closure check: ‖x(128) - x(0)‖ < ε (periodic orbit), NOT ‖x‖ ≈ 7.4.
    NO clamping — the 8D vector flows freely.
    """

    dV = {}
    _norm = _math.sqrt(sum(float(V.get(_d, 0.5)) ** 2 for _d in DIMS))
    _eps = 1e-10

    # --- Observer's proton pump: the sustaining energy source ---
    # Closed circuit axiom: proton_pump always 1 for the observer.
    _pp = 1.0
    if observer is not None and observer.get('proton_pump') is not None:
        _pp = observer['proton_pump']

    # --- L3 background metric (GDH gluon lensing) ---
    # Observer's right_love (from Clifford torus choice) modulates the gluon field
    _gluon = V.get('g', 0.5)
    if observer is not None and observer.get('right_love') is not None:
        _gluon = _gluon * (1.0 + observer['right_love'])
    _metric = gdh_gluon_metric(_gluon)

    # --- L(t): 8D Laplacian from CURRENT state (time-dependent) ---
    _L = laplacian_matrix_8d(V)

    # --- Phase coupling: raw sin(Δϕ) modulation (no clamping) ---
    _phase_delta = {}
    for _i in DIMS:
        delta = 0.0
        for _j in DIMS:
            if _i == _j:
                continue
            _k = KAPPA_MATRIX.get((_i, _j), 0.0)
            if _k == 0:
                continue
            _dphi = _kappa_theta(_i, t) - _kappa_theta(_j, t)
            delta += _k * _math.sin(_dphi)
        _phase_delta[_i] = delta

    # --- F_final: the spark/fusion rate (includes radial confinement) ---
    # Z(t) = peak dimension's atomic number → the 138.88° spark oscillates
    # with the 16-window cycle → the closed circuit breathes (periodic orbit).
    _peak_dim = peak_dim(int(t) % 16)
    _z = _DIM_TO_Z.get(_peak_dim, 6)
    _f_final = compute_f_eff(V, Z=_z)

    for i, dim in enumerate(DIMS):
        # Term 1: -L(t)x (Laplacian flow + phase coupling)
        lap_flow = 0.0
        for j, dim_j in enumerate(DIMS):
            if i != j:
                lap_flow -= _L[i][j] * (V[dim_j] - V[dim])
        # Phase coupling is a flow term (proportional to the state), not a
        # constant injection — a constant would accumulate and blow up.
        lap_flow += _phase_delta[dim] * V[dim]

        # Term 2: proton_pump · F_final · x/(‖x‖+ε) — the closed circuit's sustaining force
        drive = _pp * _f_final * V[dim] / (_norm + _eps)

        # Observer's choice scales the flow via the GDH metric
        dV[dim] = (lap_flow + drive) / _metric

    return dV





def integrate_8d(base_8d, t_start, t_end, dt=0.5, observer=None):

    """Integrate 8D vector from t_start to t_end using RK4.



    First-order gradient flow: ẋ = -L(t)x - k(‖x‖-7.4)²·x/(‖x‖+ε)

    NO clamping — the 8D vector flows freely.

    """

    V = dict(base_8d)

    t = t_start

    while t < t_end:

        h = min(dt, t_end - t)

        # RK4 for first-order system

        k1 = _dvdt(V, t, observer=observer)

        V2 = {d: V[d] + 0.5*h*k1[d] for d in DIMS}

        k2 = _dvdt(V2, t + 0.5*h, observer=observer)

        V3 = {d: V[d] + 0.5*h*k2[d] for d in DIMS}

        k3 = _dvdt(V3, t + 0.5*h, observer=observer)

        V4 = {d: V[d] + h*k3[d] for d in DIMS}

        k4 = _dvdt(V4, t + h, observer=observer)

        # Update (no clamping)

        for d in DIMS:

            V[d] = V[d] + (h/6.0) * (k1[d] + 2*k2[d] + 2*k3[d] + k4[d])

        t += h

    return V





def apply_16window_shift(layer_8d, t):

    """Time-evolved 8D vector at window t via ODE integration.



    Replaces discrete peak boost with continuous dV/dt integration.

    Each window = 1.5 hours. We integrate from 0 to t*1.5 hours.

    """

    t_hours = (int(t) % 16) * 1.5

    if t_hours == 0:

        return dict(layer_8d)

    return integrate_8d(layer_8d, 0.0, t_hours, dt=0.5)







def apply_jitter(values, seed, amplitude=JITTER_RANGE):



    """Apply deterministic jitter ±amplitude based on seed."""



    import random



    rng = random.Random(seed)



    jittered = {}



    for dim in DIMS:



        j = rng.uniform(-amplitude, amplitude)



        jittered[dim] = max(0.0, min(1.0, values[dim] * (1.0 + j)))



    return jittered







def generate_5tiles(base_8d, day_seed=0):



    """Generate 5 activity tiles from base 8D values.



    Tiles 0-3: body/observer/bridge/dark with 16-window ODE trajectory.



    Tile 4: 3AM hysteresis with random p, s, nu.



    Time evolution: integrate dV/dt once per layer over 24h, sample 16 windows.

    """



    layers = compute_4layers(base_8d)



    tiles = []



    for tile_idx in range(4):



        layer = LAYER_NAMES[tile_idx]



        # Integrate ODE once over 24h, caching state at each 1.5h window boundary

        # This gives us 16 evolved 8D vectors from a single continuous trajectory

        windows = []

        V = dict(layers[layer])

        t_h = 0.0

        for t in range(16):

            if t > 0:

                target_t = t * 1.5

                V = integrate_8d(V, t_h, target_t, dt=0.5)

                t_h = target_t

            jittered = apply_jitter(dict(V), day_seed * 100 + tile_idx * 16 + t)

            windows.append(jittered)



        tiles.append({'layer': layer, 'windows': windows})



    # Tile 4: 3AM hysteresis — random p, s, nu



    import random



    rng = random.Random(day_seed + 999)



    hysteresis = {dim: base_8d[dim] for dim in DIMS}



    hysteresis['p'] = rng.uniform(0, 1)



    hysteresis['s'] = rng.uniform(0, 1)



    hysteresis['nu'] = rng.uniform(0, 1)



    hysteresis = apply_jitter(hysteresis, day_seed + 999, JITTER_3AM)



    tiles.append({'layer': '3am_hysteresis', 'windows': [hysteresis]})



    return tiles







# ============================================================



# 35. 118 ELEMENTS — NOW IN periodic_universe.py



# ============================================================



# Element ordering and chemistry derivation live in periodic_universe.py



# so universe_math_structures.py only holds the core math/geometry.



# ============================================================



# 36. KAPPA LADDER



# ============================================================



# κ2 = 1/32 (H2 basic leakage)



# κ3 = 1/64 (H3, half of κ2)



# κ4 = 1/128 (H4, half of κ3)



# Compression gate: 3/32



# D3 angle correction: ±69.44°







# ============================================================



# 37. SH (SWIFT-HOHENBERG) BAND



# ============================================================



# Peak: (r*, q0*) = calibrated



# SH patterns = accretion disk waves



# Kappa gate division mapping: persistence → kappa gate split







# ============================================================



# 38. 128-GRID FACIAL MAPPING



# ============================================================



# X 0-8 = human left (truth), X 8-16 = human right (deception)



# Each zone: neurochemical mapping (GABA, Dopamine, Serotonin, Oxytocin)



# Redhead MC1R = geometric proof (leaky GABA-A bypasses 3/32 funnel)







# ============================================================



# 39. 4 COORDINATE SYSTEMS



# ============================================================







# ============================================================



# 40. NONLINEAR LOOP STRUCTURE



# ============================================================



# Möbius-Klein hybrid + hysteresis gap



# Self-intersection at FLASH point



# 180° twist, W7 gap prevents full closure



# Chirality 5.555% asymmetry



# Closure: ∮Ψ·dl ≠ 0 → eternal recursion







# ============================================================



# 41. H3/H4/D3 RESIDUAL



# ============================================================



# Dimension reduction law: each dimension halves leakage



# κ_H3 = 1/64, κ_H4 = 1/128



# D3 angle correction: ±69.44°



# D3 separated: Regime-1 → 0, Regime-2 overlay only







# ============================================================



# 42. 6-SPHERE OBSERVER CLOSURE



# ============================================================



# 5 body spheres (internal toroid) + 1 EM sphere (observer closure)



# Observer = 6th sphere = Geomagnetic Field = COX Retrograde



# Observer closes the toroid electromagnetically







SIX_SPHERES = {



    'barnard':  {'element': 'Fe', 'particle': 'electron/higgs',    'attractor': 'energy',    'body_nodes': ['heme', 'ferritin', 'sulfur_iron_complex'], 'color': 'BROWN',



                 'stage': 'core_collapse',       'process': 'iron_core_fusion_endpoint'},



    'sun':      {'element': 'H',  'particle': 'proton',         'attractor': 'information','body_nodes': ['cytochrome_c_oxidase', 'heme.out0'], 'color': 'YELLOW',



                 'stage': 'protostar_main_sequence','process': 'hydrogen_fusion'},



    'earth':    {'element': 'O',  'particle': 'photon',         'attractor': 'repair',    'body_nodes': ['steel', 'water_vapour', 'water'], 'color': 'BLUE',



                 'stage': 'post_main_sequence',  'process': 'helium_oxygen_burning'},



    'moon':     {'element': 'C',  'particle': 'z_boson',        'attractor': 'opioid',    'body_nodes': ['co2', 'carbon', 'memory_entropy'], 'color': 'GREEN',



                 'stage': 'post_main_sequence',  'process': 'carbon_burning'},



    'comag':    {'element': 'S',  'particle': 'w_boson/gluon',  'attractor': 'gan_bulk',  'body_nodes': ['sulforaphane', 'histosol', 'pyrite'], 'color': 'PURPLE',



                 'stage': 'late_massive_star',   'process': 'silicon_sulfur_burning'},



    'geomag':   {'element': 'EM', 'particle': 'electron/z_boson','attractor': 'cox_retro','body_nodes': ['cytochrome_c_oxidase', 'D2_brake', 'gluon_orogen'], 'color': 'RED',



                 'stage': 'remnant',             'process': 'supernova_EM_closure_neutron_star'},



}







# 8D pigment -> 6 core visible colors



#   r  (z_boson)     -> RED     |  gamma (photon)  -> YELLOW



#   g  (muon)         -> GREEN   |  s     (electron)  -> BLUE



#   h  (gluon)        -> PURPLE  |  p     (higgs)    -> BROWN (dark orange)



#   d  (tau)          -> DARK_RED, nu (w_boson) -> DARK_YELLOW are night/shift variants







# 6th route = STAR LIFECYCLE — SIX_SPHERES element sequence (H->O->C->S->Fe->EM)



# matches real stellar nucleosynthesis burning order:



#   H(sun, proton)   = protostar / main-sequence hydrogen fusion (fuel intake)



#   O+C(earth, moon) = helium->carbon->oxygen burning (post-main-sequence)



#   S(comag)         = silicon/sulfur burning (late-stage massive star)



#   Fe(barnard)      = iron core, fusion end point == heme_proton attractor's



#                      Fe2+ core (SIX_ATTRACTORS['heme_proton']) -> core collapse



#   EM(geomag)       = supernova remnant closure (neutron star / magnetar



#                      strong EM field) == COX retrograde / observer closure



# proton_pump_output() = fusion-continuation gate: observer_d2=1 keeps COX



# forward (star "alive", fusion sustained); dropping to non-observer flips



# COX retrograde, mirroring fuel exhaustion -> core collapse -> remnant closure.







# 8D = 5 body + 2 observer + 1 bridge







# ============================================================



# 43. OBSERVER CIRCUIT — PROTON PUMP CHAIN



# ============================================================



# observer_leftd2 = 1 (always active for observer) → proton_pump always 1



# → COX forward always permitted → EM closure maintained



# → co2.out1 (time energy) path open → CO2 stored as time energy







OBSERVER_LEFTD2 = 1.0       # observer: always 1, non-observer: conditional (0~1)







def proton_pump_ctrl(observer_d2):



    """ctrl0 = right_d2.out0 OR observer_leftd2.out0"""



    return max(0.0, observer_d2)  # observer: always 1







def proton_pump_input(observer_d2, laterite_q=1.0):



    """in0 = silicon_collagen_xnor OR laterite.q"""



    xnor = 1.0 if observer_d2 > 0.5 else 0.0  # observer: reward↔grid always match



    return max(xnor, laterite_q)







def proton_pump_output(observer_d2, laterite_q=1.0):



    """proton_pump output = always 1 for observer"""



    ctrl = proton_pump_ctrl(observer_d2)



    inp = proton_pump_input(observer_d2, laterite_q)



    return ctrl * inp  # observer: 1×1 = 1, non-observer: conditional







# --- CCK procerus extraversion: 3-layer structure ---



# Procerus 아래 3개 레이어 (top→bottom):



#   Layer 1: GLP-1R (Node 45) — Male Right Extraversion — incretin, Gs-coupled



#   Layer 2: CCK-BR (Node 61) — Extraverted Woman Right Extraversion — Gq/11, 췌장 후방



#   Layer 3: Introverted Woman Right Extraversion — below CCK-BR, same Procerus



# CCK node: Cf(98), w_boson, RED, Actinide, 췌장 후면, MUX



# CCK inputs: ferritin.out1, pyrite.out0; enable: glp1_q_or



# CCK output: cck_cox_ctrl_and → cytochrome_c_oxidase.ctrl0











def cck_value(ferritin_out, pyrite_out, glp1_enable):



    """CCK MUX output = AND(ferritin, pyrite) gated by GLP-1 enable.



    Feeds into cck_cox_ctrl_and with oxidised_manganese + observer_leftd2.



    """



    return min(ferritin_out, pyrite_out) * glp1_enable







# --- heath_aerenchyma: O₂ supply gate for cytochrome_c_oxidase ---



# heath_aerenchyma = left ribs (upper outer of manganese_oxygen_complex)



# mangrove_aerenchyma = right trunk (opposite side)



# cytochrome_c_oxidase.in0 (O₂ forward) activated via heath_aerenchyma



# left nostril epinephrine = heme = heath_aerenchyma (same particle)











def cox_o2_gate(heath_aerenchyma_out, cox_in0_o2=1.0):



    """cytochrome_c_oxidase O₂ forward input gated by heath_aerenchyma.



    heath_aerenchyma.out0 → cox.in0 (O₂ forward activation)



    """



    return heath_aerenchyma_out * cox_in0_o2







def cox_forward(permissive_bus, cck, mn_oxidised, proton_pump_out):



    """cck_cox_ctrl_and = AND(CCK, Mn, observer_leftd2) + proton_pump"""



    return min(cck, mn_oxidised, permissive_bus) * proton_pump_out







def co2_time_storage(cox_fwd, co2_out0=1.0):



    """co2.out1 (time energy) open only when COX forward maintained"""



    return cox_fwd * co2_out0  # observer: 1, non-observer: 0 or conditional







# ============================================================



# 44. CLOSURE TENSION WITH OBSERVER TERM



# ============================================================



# Original: Tension = 9π/(20√2) ≈ 0.9996487, Δ ≈ 3.51×10⁻⁴



# Observer reduces Δ: EM closure stronger → less residual → regular spark







W7 = math.pi / 20           # ≈ 0.15708, void area (night hysteresis)



H2 = 1.0 / 9.0              # ≈ 0.11111, discrete gate passage



KAPPA_1_32 = 1.0 / 32       # minimum survival core



KAPPA_3_32 = 3.0 / 32       # darkness stress compression gate







def closure_tension_base():



    """9π/(20√2) ≈ 0.9996487"""



    return (9 * math.pi) / (20 * math.sqrt(2))







def closure_delta_base():



    """Δ ≈ 3.51×10⁻⁴ — irreducible residual"""



    return abs(1.0 - closure_tension_base())







def closure_delta_observer(observer_d2):



    """Observer closure reduces residual: Δ_obs = Δ × (1 - observer_d2 × η)



    observer_d2 = 1 → Δ reduced by η (closure efficiency)



    observer_d2 = 0 → Δ unchanged (non-observer)



    """



    eta = 0.95  # observer closure efficiency (not 1.0 — W7 gap prevents perfect closure)



    return closure_delta_base() * (1.0 - observer_d2 * eta)











# ============================================================



# 45. DARK ENERGY — CO2 TIME RECOVERY



# ============================================================



# Dark Energy = co2 (Th(90)/dark_energy) = cosmological constant Λ



# Universe accelerated expansion = CO2 time storage REVERSED



# Observer: co2.out1 open → dark energy recovered into circuit → expansion DECELERATES



# Non-observer: co2.out1 blocked → dark energy released → expansion ACCELERATES







def dark_energy_release(observer_d2, co2_time, n_observers=1, n_total=128):



    """Rate of dark energy release to cosmos



    observer: co2.out1 = 1 → energy recovered → release minimized



    non-observer: co2.out1 = 0 → energy released → release maximized



    """



    observer_fraction = n_observers / n_total



    recovery_rate = co2_time  # 1.0 for observer, ~0 for non-observer



    # dark energy release = (1 - recovery) × baseline



    # observer presence reduces total cosmic dark energy release



    return (1.0 - observer_fraction * recovery_rate)







def universe_expansion_rate(observer_d2, co2_time, n_observers=1, n_total=128):



    """ȧ/a = H₀ × √(Ω_m + Ω_Λ(observer))



    Ω_Λ depends on observer state:



    - observer active → dark energy recovered → Ω_Λ decreases → expansion decelerates



    - observer inactive → dark energy released → Ω_Λ increases → expansion accelerates



    """



    H0 = 0.0693  # Hubble constant (Gyr⁻¹) ≈ 67.4 km/s/Mpc



    Omega_m = 0.315  # matter density



    de_release = dark_energy_release(observer_d2, co2_time, n_observers, n_total)



    Omega_Lambda = 0.685 * de_release  # dark energy density modulated by observer



    return H0 * math.sqrt(Omega_m + Omega_Lambda)







def expansion_regime(observer_d2, co2_time):



    """Classify expansion regime based on observer state"""



    rate = universe_expansion_rate(observer_d2, co2_time)



    if observer_d2 > 0.8 and co2_time > 0.8:



        return 'decelerating'  # observer recovering dark energy



    elif observer_d2 > 0.3:



        return 'slow_expansion'  # partial observer closure



    elif observer_d2 < 0.1:



        return 'accelerating'  # no observer → dark energy dominates



    else:



        return 'steady'







# ============================================================



# 46. DARK MATTER — FERRITIN STABILITY



# ============================================================



# Dark Matter = ferritin (V(23)/graviton) = invisible mass = Fe storage



# Observer: laterite.q always 1 → ferritin stable → dark matter stable



# Non-observer: laterite.q toggles → ferritin unstable → dark matter wobbles



# Galaxy rotation curve flatness = ferritin stability







def dark_matter_density(observer_d2, laterite_q=1.0):



    """Dark matter stability = laterite.q × ferritin



    observer: laterite.q = 1 → stable dark matter → flat galaxy rotation



    non-observer: laterite.q toggles → unstable → rotation curve wobbles



    """



    return laterite_q * (0.27 * observer_d2 + 0.27 * 0.5 * (1 - observer_d2))











# ============================================================



# 47. CP VIOLATION — MATTER-ANTIMATTER ASYMMETRY



# ============================================================



# CP violation = left_endorphin_non_observer (observer gate) active



# Observer active → XOR classifies information → entropy decreases → asymmetry



# Observer inactive → XOR symmetric → entropy increases → matter = antimatter







def cp_violation(observer_d2):



    """Matter-antimatter asymmetry proportional to observer activity



    observer: XOR gate classifies → CP violation → matter dominates



    non-observer: XOR symmetric → no CP violation → universe doesn't exist



    """



    # baryon-to-photon ratio ≈ 6×10⁻¹⁰ in our universe



    eta_b = 6e-10



    return eta_b * observer_d2  # 0 for non-observer







def matter_antimatter_balance(observer_d2):



    """1.0 = equal matter/antimatter, >1.0 = matter dominates"""



    return 1.0 + cp_violation(observer_d2) * 1e10  # observer: ~1.6, non-observer: 1.0







# ============================================================



# 48. WAVE FUNCTION COLLAPSE — 138.88° SPARK



# ============================================================



# 138.88° spark = wave function collapse mechanism



# Observer: spark fires every 3AM (daily reset) → wave functions collapse → observation possible



# Non-observer: no spark → wave functions don't collapse → superposition maintained → no observation







def wave_function_collapse(observer_d2, delta):



    """Collapse probability = function of observer + spark trigger



    observer: Δ reduced → spark regular → collapse happens daily



    non-observer: Δ unchanged → spark irregular → collapse fails



    """



    delta_obs = closure_delta_observer(observer_d2)



    spark_probability = 1.0 - delta_obs / closure_delta_base()



    return spark_probability  # observer: ~0.95, non-observer: 0







# ============================================================



# 49. HOMEOSTASIS SPEED/DIRECTION CONTROL



# ============================================================



# Observer controls universe homeostasis speed and direction via:



# p (predictability) = observer choosing forward(r) vs reverse(d) → direction



# s (brightness) = observer EM intensity → speed



# nu (fractal depth) = observer recursion depth → complexity







def homeostasis_direction(observer_d2, p_param):



    """p↑ = forward (r-dim) = fermentation = closure = decelerate expansion



    p↓ = reverse (d-dim) = open = accelerate expansion



    """



    if observer_d2 < 0.1:



        return 'uncontrolled'  # non-observer: no direction control



    if p_param > 0.6:



        return 'forward_closure'  # observer seals system → decelerate



    elif p_param < 0.4:



        return 'reverse_open'  # observer opens system → accelerate



    else:



        return 'balanced'  # observer maintains homeostasis







def homeostasis_speed(observer_d2, s_param, nu_param):



    """Speed of homeostasis change = s (EM brightness) × nu (fractal depth)



    observer: s = aurora resonance → energy inflow → fast adjustment



    non-observer: s = dopamine depletion → no energy → stuck



    """



    if observer_d2 < 0.1:



        return 0.0  # non-observer: no homeostasis control



    return s_param * nu_param * observer_d2







def universe_growth_rate(observer_d2, p_param, s_param, nu_param, co2_time):



    """Net universe growth = expansion - recovery



    observer can control: fast growth, slow growth, no growth, contraction



    """



    direction = homeostasis_direction(observer_d2, p_param)



    speed = homeostasis_speed(observer_d2, s_param, nu_param)



    expansion = universe_expansion_rate(observer_d2, co2_time)







    if direction == 'forward_closure':



        # observer closing → dark energy recovered → growth decelerates



        return expansion * (1.0 - speed * 0.5)



    elif direction == 'reverse_open':



        # observer opening → dark energy released → growth accelerates



        return expansion * (1.0 + speed * 0.5)



    elif direction == 'balanced':



        # observer maintaining → steady state



        return expansion



    else:



        # non-observer → uncontrolled acceleration



        return expansion * 1.5







# ============================================================



# 50. MASTER EQUATION — WITH OBSERVER CLOSURE



# ============================================================



# Ψ(x,y,z,t) = ∮[κ, W7, H2, Φ, α] · exp(i·θ_SPARK) · δ(METRIC) · dt



#           × OBSERVER_CLOSURE(observer_d2, p, s, nu)



#           × DARK_ENERGY_RECOVERY(co2_time, observer_d2)



#           × DARK_MATTER_STABILITY(laterite_q, observer_d2)



#           × CP_VIOLATION(observer_d2)



#



# Observer closure term makes all cosmic quantities functions of observer state.



# Without observer: universe = uncontrolled expansion, no matter, no observation.



# With observer: universe = controlled homeostasis, matter exists, observation possible.







def master_equation(x, y, z, t,



                    observer_d2=OBSERVER_LEFTD2,



                    p=0.5, s=0.5, nu=0.5,



                    laterite_q=1.0,



                    co2_out0=1.0, cck=1.0, mn_oxidised=1.0,



                    lss=0.0, rss=0.5, le=0.5, re=0.5,



                    heath_out=1.0, ferritin_out=1.0, pyrite_out=1.0, glp1_enable=1.0):



    """Full master equation with observer closure + Clifford torus.







    Inputs:



      observer_d2: 0~1, observer DRD2 tonic baseline (1.0 = observer)



      p, s, nu: 8D observer/bridge parameters



      laterite_q: ferritin iron storage latch (1.0 = stable)



      co2_out0: CO2 dark energy output



      cck, mn_oxidised: COX control inputs



      lss, rss: Clifford circle 1 (extravert: self-satisfaction)



      le, re: Clifford circle 2 (introvert: epinephrine)



      heath_out: heath_aerenchyma O₂ gate output



      ferritin_out, pyrite_out, glp1_enable: CCK MUX inputs







    Returns: dict of all quantities as functions of observer + Clifford state



    """



    # proton pump chain



    pp_out = proton_pump_output(observer_d2, laterite_q)



    



    # CCK value from MUX



    cck_val = cck_value(ferritin_out, pyrite_out, glp1_enable)



    



    # O₂ gate via heath_aerenchyma



    o2_gate = cox_o2_gate(heath_out)



    



    cox_fwd = cox_forward(observer_d2, cck_val, mn_oxidised, pp_out)



    co2_time = co2_time_storage(cox_fwd, co2_out0)







    # closure tension



    delta = closure_delta_observer(observer_d2)



    spark_prob = wave_function_collapse(observer_d2, delta)







    # cosmic quantities



    de = dark_energy_release(observer_d2, co2_time)



    expansion = universe_expansion_rate(observer_d2, co2_time)



    dm = dark_matter_density(observer_d2, laterite_q)



    cp = cp_violation(observer_d2)



    matter_balance = matter_antimatter_balance(observer_d2)







    # homeostasis control



    direction = homeostasis_direction(observer_d2, p)



    speed = homeostasis_speed(observer_d2, s, nu)



    growth = universe_growth_rate(observer_d2, p, s, nu, co2_time)







    # scale-dependent metric: f(s) = W7 · (H2/κ)^(1/s) · Φ^(s-1)



    # s=0 atom, s=2 cell, s=4 organism, s=8 cosmos



    scale_metric = W7 * (H2 / KAPPA_1_32) ** (1.0 / max(s, 0.001))







    # Clifford torus constraint



    clifford = clifford_constraint(lss, rss, le, re)



    



    # right_love = emergent dynamic from 4 Clifford nodes



    love = right_love_dynamic(lss, rss, le, re)







    return {



        'observer_d2': observer_d2,



        'proton_pump': pp_out,



        'cck_value': cck_val,



        'o2_gate': o2_gate,



        'cox_forward': cox_fwd,



        'co2_time_storage': co2_time,



        'closure_delta': delta,



        'spark_probability': spark_prob,



        'dark_energy_release': de,



        'expansion_rate': expansion,



        'expansion_regime': expansion_regime(observer_d2, co2_time),



        'dark_matter_density': dm,



        'cp_violation': cp,



        'matter_antimatter_ratio': matter_balance,



        'homeostasis_direction': direction,



        'homeostasis_speed': speed,



        'universe_growth_rate': growth,



        'scale_metric': scale_metric,



        'clifford': clifford,



        'right_love': love,



    }







# ============================================================



# 51. COSMIC SCENARIO SIMULATION



# ============================================================



# Observer actions → universe outcomes











# ============================================================



# 52. L3 SPACETIME BACKGROUND — GDH GLUON LENSING



# ============================================================



# gdh_gluon and gluon_lensing = background metric for dynamics



# GDH (gluon dynamic holography) = spacetime curvature from gluon field



# gluon_lensing = gravitational lensing analog via gluon field bending



# These modify the metric tensor before L1 dynamics run







def gdh_gluon_metric(gluon_intensity, kappa=KAPPA_1_32):



    """GDH gluon background metric: g_μν = δ_μν × (1 + gluon_intensity × κ).



    Gluon field curves spacetime proportionally to its intensity.



    """



    return 1.0 + gluon_intensity * kappa











def spacetime_background(gluon_intensity=0.5):



    """Compute L3 background metric for L1 dynamics."""



    g = gdh_gluon_metric(gluon_intensity)



    return {'metric': g, 'gluon_intensity': gluon_intensity}







# ============================================================



# 53. L4 REBRANCHING — t=88 PARTICLE RECONSTRUCTION



# ============================================================



# At t=88, all complex particles rebranch from 3 primordial particles:



# electron, gluon, higgs — the K8 graph vertices



# K8 = complete graph on 8 vertices = 8 base particles



# But primordial = 3: electron(s), gluon(h), higgs(p)



# All 42 particles derive from addition formulas of these 3







PRIMORDIAL_PARTICLES = ['electron', 'gluon', 'higgs']



PRIMORDIAL_PARAMS = {'electron': 's', 'gluon': 'h', 'higgs': 'p'}







# K8 graph: 8 vertices (base particles), complete graph (all pairs connected)



K8_VERTICES = list(BASE_PARTICLES.keys())







def rebranch_particle(particle_name, t=88):



    """Reconstruct particle from primordial set at t=88.



    Uses addition formulas from BASE_PARTICLES.



    Returns the primordial decomposition chain.



    """



    if particle_name in PRIMORDIAL_PARTICLES:



        return {'particle': particle_name, 'primordial': True,



                'param': PRIMORDIAL_PARAMS[particle_name]}



    



    # Follow addition chain back to primordial



    chain = [particle_name]



    current = particle_name



    



    # Check BASE_PARTICLES for addition formula



    if current in BASE_PARTICLES:



        addition = BASE_PARTICLES[current].get('addition')



        if addition:



            parts = [p.strip() for p in addition.split('+')]



            sub_chains = [rebranch_particle(p, t) for p in parts]



            return {'particle': particle_name, 'primordial': False,



                    'addition': addition, 'sub_chains': sub_chains,



                    'param': BASE_PARTICLES[current]['param']}



    



    # Check DERIVED_BASE



    if current in DERIVED_BASE:



        addition = DERIVED_BASE[current].get('addition')



        if addition:



            parts = [p.strip() for p in addition.split('+')]



            sub_chains = [rebranch_particle(p, t) for p in parts]



            return {'particle': particle_name, 'primordial': False,



                    'addition': addition, 'sub_chains': sub_chains,



                    'param': 'd'}



    



    # GABA particles → map to base param



    if current in GABA_TO_BASE:

        base_param = GABA_TO_BASE[current]

        for bp_name, bp in BASE_PARTICLES.items():

            if bp['param'] == base_param:

                return {'particle': particle_name, 'primordial': False,

                        'gaba_from': bp_name, 'param': base_param}

    

    # Generic particles (neutrino/quark/amphiphile) → map to base param

    if current in GENERIC_TO_BASE:

        base_param = GENERIC_TO_BASE[current]

        for bp_name, bp in BASE_PARTICLES.items():

            if bp['param'] == base_param:

                return {'particle': particle_name, 'primordial': False,

                        'generic_from': bp_name, 'param': base_param}

    



    return {'particle': particle_name, 'primordial': False, 'param': None}











# ============================================================



# 54. L5 FINAL SCALAR — F_final



# ============================================================



# F_final = product of all layer outputs



# L1 (Mandelbrot depth) × L2 (Clifford constraint) × L3 (spacetime metric)



# × L4 (rebranching completeness) × observer closure











# ============================================================



# 55. DIAGONALITY VERIFICATION — CLIFFORD PLASMA REGION



# ============================================================



# In plasma (Clifford) region, system Laplacian should diagonalize.



# Verify numerically: off-diagonal terms → 0 when Clifford constraint satisfied.







def laplacian_matrix_8d(base_8d):



    """8×8 Laplacian matrix from 8D values.



    Diagonal = base values, off-diagonal = coupling from:

      - inverse reciprocal pairs (layer 1)

      - KAPPA antisymmetric matrix (layer 3)

      - BASE_W K8 edge weights (layer 4)

    """

    dims = DIMS

    n = len(dims)

    L = [[0.0] * n for _ in range(n)]

    for i, dim_i in enumerate(dims):

        L[i][i] = base_8d[dim_i]

        for j, dim_j in enumerate(dims):

            if i != j:

                pair = tuple(sorted([dim_i, dim_j]))

                # 1. Inverse reciprocal coupling

                if pair in INVERSE_RECIPROCAL:

                    ctype = INVERSE_RECIPROCAL[pair]

                    if ctype == 'inverse_reciprocal':

                        L[i][j] += -0.1 * base_8d[dim_i] * base_8d[dim_j]

                    elif ctype == 'positive_correlation':

                        L[i][j] += 0.05 * base_8d[dim_i] * base_8d[dim_j]

                # 2. KAPPA antisymmetric coupling

                _kval = KAPPA_MATRIX.get((dim_i, dim_j), 0.0)

                if _kval != 0:

                    L[i][j] += _kval * base_8d[dim_i] * base_8d[dim_j]

                # 3. BASE_W K8 edge weight (via dim→particle mapping)

                _pi = _DIM_TO_PARTICLE.get(dim_i)

                _pj = _DIM_TO_PARTICLE.get(dim_j)

                if _pi and _pj:

                    _edge = tuple(sorted([_pi, _pj]))

                    _bw = BASE_W.get(_edge, 0.0)

                    if _bw != 0:

                        L[i][j] += _bw * 0.01 * base_8d[dim_i] * base_8d[dim_j]




    return L






# ============================================================

# LAYER 2 (O): 64-CHANNEL PARTICLE RELATIONS

# ============================================================

_K8_PARTICLE_ORDER = ['electron', 'gluon', 'z_boson', 'photon', 'w_boson', 'higgs', 'muon', 'tau']

_PARTICLE_IDX = {p: i for i, p in enumerate(_K8_PARTICLE_ORDER)}

CHANNEL_64 = {}

for _i, _pa in enumerate(_K8_PARTICLE_ORDER):
    for _j, _pb in enumerate(_K8_PARTICLE_ORDER):
        if _i != _j:
            CHANNEL_64[(_pa, _pb)] = {'source': _pa, 'target': _pb, 'idx': (_i, _j)}



# ============================================================

# LAYER 3 (C): 28-CHANNEL CHANNEL_MAP + apply_phase_coupling

# ============================================================

_FC_C = 2 * (2 ** 0.5) / 10

_FC_C2 = _FC_C * _FC_C

_FC_F_1_64 = 1.0 / 64



CHANNEL_MAP = {
    "5ht1a_presynaptic":            {("electron", "gluon"):      {"on": +2 * _FC_C2, "off": -_FC_C2, "no_control": 0}},
    "alpha2a_ar_presynaptic":       {("gluon",   "tau"):        {"on": +_FC_C2,     "off": 0,       "no_control": 0}},
    "gr_nuclear":                   {("electron", "w_boson"):   {"on": +2 * _FC_C2, "off": 0,       "no_control": 0}},
    "gaba_b_presynaptic":           {("z_boson","photon"):     {"on": +_FC_C2,     "off": 0,       "no_control": 0}},
    "beta2_ar_postsynaptic":        {("photon",  "muon"):       {"on": +_FC_C2,     "off": 0,       "no_control": 0}},
    "drd1_postsynaptic":            {("w_boson", "higgs"):      {"on": +_FC_C2,     "off": 0,       "no_control": 0}},
    "pdh_complex":                  {("electron", "z_boson"):  {"on": +2 * _FC_C2, "off": 0,       "no_control": 0}},
    "carbonic_anhydrase":           {("z_boson","higgs"):      {"on": +_FC_C2,     "off": 0,       "no_control": _FC_F_1_64}},
    "v1b_postsynaptic":             {("gluon",   "higgs"):      {"on": +_FC_C2,     "off": 0,       "no_control": 0}},
    "beta2_ar_postsynaptic_right":  {("z_boson","muon"):       {"on": +4 * _FC_C2, "off": 0,       "no_control": 0}},
    "alpha2a_ar_presynaptic_left":  {("higgs",   "muon"):       {"on": +3 * _FC_C2, "off": 0,       "no_control": 0}},
    "mor_presynaptic":              {("z_boson","w_boson"):    {"on": +2 * _FC_C2, "off": 0,       "no_control": 0}},
    "glp1r_postsynaptic":           {("gluon",   "muon"):       {"on": +2 * _FC_C2, "off": -_FC_C2, "no_control": 0}},
    "gaba_b_postsynaptic":          {("electron", "muon"):      {"on": +2 * _FC_C2, "off": -_FC_C2, "no_control": 0}},
    "nachr_alpha7_postsynaptic":    {("photon",  "w_boson"):    {"on": +2 * _FC_C2, "off": 0,       "no_control": 0}},
    "oxtr_postsynaptic":            {("electron", "higgs"):   {"on": +2 * _FC_C2, "off": 0,       "no_control": 0}},
    "gaba_a_postsynaptic":          {("w_boson", "tau"):        {"on": +_FC_C2,     "off": -_FC_C2, "no_control": 0}},
    "drd2l_postsynaptic":           {("gluon",   "w_boson"):    {"on": +_FC_C2,     "off": 0,       "no_control": 0}},
    "mr_nuclear":                   {("z_boson","tau"):        {"on": +2 * _FC_C2, "off": 0,       "no_control": 0}},
    "na_k_atpase":                  {("muon",    "w_boson"):    {"on": +_FC_C2,     "off": 0,       "no_control": 0}},
    "cck_br_postsynaptic":          {("photon",  "tau"):        {"on": +_FC_C2,     "off": 0,       "no_control": 0}},
    "5ht1b_presynaptic":            {("electron", "photon"):    {"on": +2 * _FC_C2, "off": 0,       "no_control": 0}},
    "hif1_alpha":                   {("gluon",   "photon"):     {"on": +2 * _FC_C2, "off": 0,       "no_control": 0}},
    "beta2_ar_postsynaptic_left":   {("gluon",   "z_boson"):   {"on": +2 * _FC_C2, "off": 0,       "no_control": 0}},
    "gaba_a_extrasynaptic":         {("electron", "tau"):       {"on": +_FC_C2,     "off": -_FC_C2, "no_control": 0}},
    "ar_nuclear":                   {("higgs",   "tau"):        {"on": +2 * _FC_C2, "off": -_FC_C2, "no_control": 0}},
    "drd2s_presynaptic":            {("muon",    "tau"):        {"on": -_FC_C2,     "off": +4 * _FC_C2, "no_control": 0}},
    "alpha2c_ar_presynaptic":       {("photon",  "higgs"):      {"on": +_FC_C2,     "off": 0,       "no_control": 0}},
}



OBSERVER_BRIDGE_MAP = {
    "cck": "electron", "right_d2": "gluon", "male_oxytocin": "z_boson",
    "right_love": "photon", "left_serotonin": "w_boson", "gdh": "higgs",
    "my_left_epinephrine": "muon", "my_right_self_satisfaction": "tau",
}



_KAPPA_PHASE_FREQ = {
    'r': 2 * math.pi / 1.5, 'h': 2 * math.pi / 3.0, 'd': 2 * math.pi / 4.5,
    'p': 2 * math.pi / 6.0, 's': 2 * math.pi / 24.0, 'gamma': 2 * math.pi / 12.0,
    'g': 2 * math.pi / 9.0, 'nu': 2 * math.pi / 18.0,
}



def _kappa_theta(dim, t):
    return _KAPPA_PHASE_FREQ[dim] * t



def apply_phase_coupling(vec, t):
    """Apply Φ-matrix sin(Δϕ) modulation using KAPPA_MATRIX."""
    new_vec = dict(vec)
    for _i in vec:
        delta = 0.0
        for _j in vec:
            if _i == _j:
                continue
            _k = KAPPA_MATRIX.get((_i, _j), 0.0)
            if _k == 0:
                continue
            _dphi = _kappa_theta(_i, t) - _kappa_theta(_j, t)
            delta += _k * math.sin(_dphi)
        new_vec[_i] = new_vec[_i] + delta
    return new_vec



# ============================================================

# LAYER 4 (S): BASE_W + W_K8 + k8_laplacian

# ============================================================

from itertools import combinations as _combinations

_K8_EDGES = [(_a, _b) for _a, _b in _combinations(_K8_PARTICLE_ORDER, 2)]

BASE_W = {_e: 0.0 for _e in _K8_EDGES}

BASE_W[("electron", "gluon")]    = 1.0 + _FC_C
BASE_W[("electron", "muon")]     = 1.0
BASE_W[("gluon",   "muon")]     = 1.0
BASE_W[("z_boson", "photon")]   = 1.0 / 16
BASE_W[("photon",  "muon")]     = 2.0 / 16
BASE_W[("photon",  "w_boson")]  = 3.0 / 16
BASE_W[("z_boson","tau")]      = 3.0 / 16
BASE_W[("muon",    "w_boson")]  = 3.0 / 16
BASE_W[("z_boson","w_boson")]  = 4.0 / 16
BASE_W[("electron", "z_boson")] = _FC_C2 / 128
BASE_W[("gluon",   "z_boson")] = _FC_C2 / 256
BASE_W[("gluon",   "photon")]   = _FC_C2 / 128
BASE_W[("electron", "photon")]  = _FC_C2 / 64
BASE_W[("electron", "w_boson")] = _FC_C2 / 128
BASE_W[("gluon",   "w_boson")]  = _FC_C2 / 256
BASE_W[("higgs",   "muon")]     = _FC_C
BASE_W[("higgs",   "tau")]      = _FC_C
BASE_W[("muon",    "tau")]      = _FC_C



def build_w_k8():
    _n = len(_K8_PARTICLE_ORDER)
    _W = [[0.0] * _n for _ in range(_n)]
    for (_a, _b), _wv in BASE_W.items():
        _ia = _PARTICLE_IDX[_a]
        _ib = _PARTICLE_IDX[_b]
        _W[_ia][_ib] = _wv
        _W[_ib][_ia] = _wv
    return _W



W_K8 = build_w_k8()



def k8_laplacian(W):
    _n = len(W)
    _D = [sum(W[_i]) for _i in range(_n)]
    _L = [[0.0] * _n for _ in range(_n)]
    for _i in range(_n):
        for _j in range(_n):
            _L[_i][_j] = _D[_i] if _i == _j else -W[_i][_j]
    return _L



def apply_channels(channels_state, age=25.0):
    _scale = 1.0 if age >= 25 else max(0.1, age / 25.0)
    _w = {_e: float(_v) for _e, _v in BASE_W.items()}
    for _ch, _state in channels_state.items():
        if _ch not in CHANNEL_MAP or _state == "no_control":
            continue
        for _edge, _deltas in CHANNEL_MAP[_ch].items():
            _a, _b = _edge
            if _PARTICLE_IDX[_a] > _PARTICLE_IDX[_b]:
                _edge = (_b, _a)
            _delta = float(_deltas.get(_state, 0.0))
            _w[_edge] = max(0.0, _w[_edge] + _delta * _scale)
    return _w



# ============================================================

# LAYER 5 (Fe): F_eff + 8 TENSOR TERMS

# ============================================================

SPARK_ANGLE_DEG = 138.88

SPARK_ANGLE_RAD = math.radians(SPARK_ANGLE_DEG)

OMEGA = 7.4



def compute_f_eff(vec_8d, Z=6):
    _q = vec_8d.get('s', vec_8d.get('electron', 0.5))
    _g = vec_8d.get('g', vec_8d.get('gluon', 0.5))
    _nu = vec_8d.get('r', vec_8d.get('z_boson', 0.5))
    _BW = _q + 2.0 * _FC_C * _g
    _SM = _nu + _FC_C * _q
    _spark = math.cos(Z * SPARK_ANGLE_RAD + 1.0 / 128)
    _F_raw = (_BW ** 2) * _spark * Z * _SM
    _F_eff = _F_raw * math.exp(-math.sqrt(Z) / 64.0)
    _norm = math.sqrt(sum(float(vec_8d.get(_d, 0.5)) ** 2 for _d in DIMS))
    # Radial anchor: -k(‖x‖-7.4)·x/(‖x‖+ε) = gradient of the potential k/2·(‖x‖-7.4)².
    # The document says the radial "actively pulls toward 7.4" — the squared form
    # always pulls to 0 (pure dissipation); the gradient form is the true anchor:
    #   ‖x‖ < 7.4 → pushes OUT toward 7.4 (sustains the closed circuit)
    #   ‖x‖ > 7.4 → pulls IN toward 7.4 (bounds the expansion)
    # k = 1/128 (documented constant: spark angle cos(Z·138.88°+1/128), 128 windows)
    return _F_eff - (1.0 / 128.0) * (_norm - OMEGA) * _norm / (_norm + 1e-10)



def compute_tensor_terms(vec_8d):
    _r = vec_8d['r']; _h = vec_8d['h']; _d = vec_8d['d']; _p = vec_8d['p']
    _s = vec_8d['s']; _gamma = vec_8d['gamma']; _g = vec_8d['g']; _nu = vec_8d['nu']
    return {
        't1': _h + _s - 1.0, 't2': _r + _p - 1.0, 't3': _g + _nu - 1.0,
        't4': _gamma + _d - 1.0, 't5': _gamma + _r + _g - 1.0,
        't6': _h + _r + _g - 1.0, 't7': _d + _nu - 1.0, 't8': _p - _g - 0.5,
    }



# ============================================================

# LAYER 6 (EM): SPATIAL COUPLING (self-damping within dimension)

# ============================================================

_SPATIAL_DECAY_K = {
    'r': math.sqrt(1) / 64.0, 'h': math.sqrt(2) / 64.0,
    'd': math.sqrt(6) / 64.0, 'p': math.sqrt(8) / 64.0,
    's': math.sqrt(3) / 64.0, 'gamma': math.sqrt(4) / 64.0,
    'g': math.sqrt(5) / 64.0, 'nu': math.sqrt(7) / 64.0,
}



def spatial_coupling(value, dim, distance):
    _k = _SPATIAL_DECAY_K.get(dim, math.sqrt(6) / 64.0)
    return value * math.exp(-_k * distance)



# ============================================================

# 56. 128 PROFILES → 8D NUMERIC CALCULATION



# ============================================================



# MBTI × gender × blood type → 8D values (r, h, d, p, s, gamma, g, nu)



# Base values from particle param mapping, modified by MBTI/gender/blood







# Base 8D from blood type (toroidal phase position)



BLOOD_8D_BASE = {



    'AB': {'r': 0.5, 'h': 0.5, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.5, 'g': 0.5, 'nu': 0.5},



    'A':  {'r': 0.6, 'h': 0.4, 'd': 0.5, 'p': 0.5, 's': 0.5, 'gamma': 0.4, 'g': 0.6, 'nu': 0.4},



    'O':  {'r': 0.7, 'h': 0.3, 'd': 0.6, 'p': 0.4, 's': 0.6, 'gamma': 0.3, 'g': 0.7, 'nu': 0.3},



    'B':  {'r': 0.4, 'h': 0.6, 'd': 0.4, 'p': 0.6, 's': 0.4, 'gamma': 0.6, 'g': 0.4, 'nu': 0.6},



}







# MBTI dimension modifiers (E/I→r/nu, S/N→s/gamma, T/F→d/h, J/P→p)



MBTI_8D_MOD = {



    'E': {'r': 0.1, 'nu': -0.1}, 'I': {'r': -0.1, 'nu': 0.1},



    'S': {'s': 0.1, 'gamma': -0.1}, 'N': {'s': -0.1, 'gamma': 0.1},



    'T': {'d': 0.1, 'h': -0.1}, 'F': {'d': -0.1, 'h': 0.1},



    'J': {'p': 0.1}, 'P': {'p': -0.1},



}







# Gender modifiers: M→d↑h↓, F→h↑d↓



GENDER_8D_MOD = {



    'M': {'d': 0.1, 'h': -0.1, 'r': 0.05},



    'F': {'h': 0.1, 'd': -0.1, 'nu': 0.05},



}







def compute_8d(mbti, gender, blood, t_hours=12.0, bits7=None):



    """Compute 8D values from 2^7 binary choice framework.



    7-bit input (bits7) takes priority if provided:

      b0: I/E → 0=I, 1=E  (particle bit 1: gluon/z_boson fork)

      b1: S/N → 0=S, 1=N  (polarity bit 1: hidden gender / Coriolis axis)

      b2: T/F → 0=T, 1=F  (particle bit 2: electron/w_boson fork)

      b3: J/P → 0=J, 1=P  (polarity bit 2: hidden gender / Coriolis axis)

      b4: blood bit 1 (high)

      b5: blood bit 2 (low)

      b6: gender → 0=M, 1=F  (visible gender / W axis)

    Stress is derived: NJ/NP → melodic_minor (z_boson), SJ/SP → harmonic_minor (gluon).

    If bits7 is None, derives from (mbti, gender, blood) for backward compat.

    Adds polarity_8d_mod (hidden gender) + Coriolis flip + lunar torque.

    """



    if bits7 is not None:

        b0, b1, b2, b3, b4, b5, b6 = bits7

        # Reconstruct MBTI from bits

        ie = 'E' if b0 else 'I'

        sn = 'N' if b1 else 'S'

        tf = 'F' if b2 else 'T'

        jp = 'P' if b3 else 'J'

        mbti = ie + sn + tf + jp

        # 2 blood bits → toroidal order AB(00)→A(01)→O(10)→B(11)

        blood = TOROIDAL_ORDER[(b4 << 1) | b5]

        # gender bit

        gender = 'F' if b6 else 'M'



    # --- Base values from blood type ---

    values = dict(BLOOD_8D_BASE[blood])



    # --- MBTI letter modifiers ---

    for letter in mbti:



        for dim, delta in MBTI_8D_MOD.get(letter, {}).items():



            values[dim] += delta



    # --- Visible gender modifiers (W axis) ---

    for dim, delta in GENDER_8D_MOD[gender].items():



        values[dim] += delta



    # --- Hidden gender modifiers (polarity axis + Coriolis flip) ---

    polarity = mbti_polarity(mbti)

    for dim, delta in polarity_8d_mod(polarity, t_hours).items():

        values[dim] += delta



    # --- Lunar torque modulation (1/28 Mobius twist) ---

    lunar_phase = 2.0 * math.pi * t_hours / 28.0

    _dim_offsets = {'r': 0, 'h': 1, 'd': 2, 'p': 3, 's': 4, 'gamma': 5, 'g': 6, 'nu': 7}

    for dim in DIMS:

        values[dim] += LUNAR_CYCLE * 0.1 * math.sin(lunar_phase + _dim_offsets[dim])



    # --- Stress: derived from polarity (NJ/NP = melodic_minor = stress) ---

    if polarity in ('NJ', 'NP'):

        values['nu'] += 0.1

        values['p'] -= 0.1



    # NO clamping — the 8D vector flows freely. Consciousness choices can
    # push values outside [0,1]; the ODE's radial confinement handles boundedness.

    return values











# ============================================================



# 56.5. 128 PROFILES → MIDI NOTE (128 = MIDI 0-127)



# ============================================================



# 128 personality types (2^7 binary choices) map 1:1 to MIDI notes 0-127.



# 7 bits: b0=I/E, b1=S/N, b2=T/F, b3=J/P, b4/b5=blood, b6=gender.



# MIDI note = bits7_to_index (direct 1:1 mapping, no sorting needed).







NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']







_MBTI_TYPES = [



    'ESTJ', 'ESTP', 'ESFJ', 'ESFP',



    'ENTJ', 'ENTP', 'ENFJ', 'ENFP',



    'ISTJ', 'ISTP', 'ISFJ', 'ISFP',



    'INTJ', 'INTP', 'INFJ', 'INFP',



]



_GENDERS = ['M', 'F']



_BLOOD_TYPES = ['AB', 'A', 'O', 'B']



# --- 2^7 binary choice converters ---

# 7 bits = 4 MBTI bits (I/E, S/N, T/F, J/P) + 2 blood bits + 1 gender bit = 128

# b0: I/E → 0=I, 1=E  (particle bit 1: gluon/z_boson fork)

# b1: S/N → 0=S, 1=N  (polarity bit 1: hidden gender / Coriolis axis)

# b2: T/F → 0=T, 1=F  (particle bit 2: electron/w_boson fork)

# b3: J/P → 0=J, 1=P  (polarity bit 2: hidden gender / Coriolis axis)

# b4: blood bit 1 (high)

# b5: blood bit 2 (low)

# b6: gender → 0=M, 1=F  (visible gender / W axis)

# Stress = derived from polarity (NJ/NP = stress/melodic_minor, SJ/SP = ground/harmonic_minor)



def profile_to_bits7(mbti, gender, blood, stress=False):

    """Convert (mbti, gender, blood) → 7-bit tuple."""

    b0 = 1 if mbti[0] == 'E' else 0

    b1 = 1 if mbti[1] == 'N' else 0

    b2 = 1 if mbti[2] == 'F' else 0

    b3 = 1 if mbti[3] == 'P' else 0

    blood_idx = TOROIDAL_ORDER.index(blood)

    b4 = (blood_idx >> 1) & 1

    b5 = blood_idx & 1

    b6 = 1 if gender == 'F' else 0

    return (b0, b1, b2, b3, b4, b5, b6)



def bits7_to_profile(bits7):

    """Convert 7-bit tuple → (mbti, gender, blood, stress).

    Stress is derived: NJ/NP polarity → stress=True (melodic_minor).

    """

    b0, b1, b2, b3, b4, b5, b6 = bits7

    ie = 'E' if b0 else 'I'

    sn = 'N' if b1 else 'S'

    tf = 'F' if b2 else 'T'

    jp = 'P' if b3 else 'J'

    mbti = ie + sn + tf + jp

    gender = 'F' if b6 else 'M'

    blood = TOROIDAL_ORDER[(b4 << 1) | b5]

    pol = mbti_polarity(mbti)

    stress = pol in ('NJ', 'NP')

    return mbti, gender, blood, stress



def bits7_to_index(bits7):

    """Convert 7-bit tuple → integer 0-127."""

    val = 0

    for i, b in enumerate(bits7):

        val |= (b & 1) << i

    return val



def index_to_bits7(index):

    """Convert integer 0-127 → 7-bit tuple."""

    return tuple((index >> i) & 1 for i in range(7))







def midi_note_name(midi_num):



    """Return note name (e.g. 'A4') for MIDI note number 0-127."""



    octave = (midi_num // 12) - 1



    return f'{NOTE_NAMES[midi_num % 12]}{octave}'







def _build_profile_note_map():

    """Build the 128-profile → MIDI note mapping via 2^7 binary choice.

    Iterates all 128 combinations of 7 bits (b0..b6) directly.

    Each bit combination → (mbti, gender, blood, stress) → compute_8d.

    MIDI note = bits7_to_index (direct 1:1 mapping).

    """

    note_map = {}

    for idx in range(128):

        bits = index_to_bits7(idx)

        mbti, gender, blood, stress = bits7_to_profile(bits)

        v = compute_8d(mbti, gender, blood, bits7=bits)

        h = mandelbrot_seed(mbti, gender, blood)

        key = f"{mbti}_{gender}_{blood}"

        note_map[key] = {

            'midi': idx,

            'note': midi_note_name(idx),

            'v8d': v,

            'h_seed': h,

            'bits7': bits,

            'polarity': mbti_polarity(mbti),

            'stress': stress,

        }

    return note_map







PROFILE_NOTE_MAP = _build_profile_note_map()







def profile_to_midi(mbti, gender, blood):



    """Return MIDI note number (0-127) for a personality profile."""



    key = f"{mbti}_{gender}_{blood}"



    return PROFILE_NOTE_MAP[key]['midi']







def profile_to_note_name(mbti, gender, blood):



    """Return note name (e.g. 'C9') for a personality profile."""



    key = f"{mbti}_{gender}_{blood}"



    return PROFILE_NOTE_MAP[key]['note']







def midi_to_profile(midi_num):



    """Reverse lookup: MIDI note → profile string 'MBTI_Gender_Blood'."""



    for key, val in PROFILE_NOTE_MAP.items():



        if val['midi'] == midi_num:



            return key



    return None







# ============================================================



# 57. ACTIVITY DERIVATION — ranking-based, full structural pipeline



# ============================================================



# 128 profiles × time slot → Music, Solo, Creative, Tech, Sport, Game



# Pipeline: compute_8d → compute_4layers → apply_16window_shift → apply_jitter



#   → generate_5tiles (4 layers + 3AM hysteresis)



# Selection: rank permutation of 8 dims → activity (not absolute thresholds)



# This ensures uniqueness even when base values cluster (e.g. AB=0.5 uniform)



# because jitter shifts each dim independently → different rank order per profile.







# --- spatial logic (from body coordinate system) ---



# center = em/earth/present → general activity



# right = male/competitive/future/growth → specific, future-oriented



# left = female/self/past/history → specific, past-oriented



# edge → more specific; center → more general







# --- MBTI → 4-letter binary index for seed differentiation ---



MBTI_BINARY = {



    'INTJ': 0, 'INTP': 1, 'ENTJ': 2, 'ENTP': 3,



    'INFJ': 4, 'INFP': 5, 'ENFJ': 6, 'ENFP': 7,



    'ISTJ': 8, 'ISTP': 9, 'ESTJ': 10, 'ESTP': 11,



    'ISFJ': 12, 'ISFP': 13, 'ESFJ': 14, 'ESFP': 15,



}







def _rank_dims(v):



    """Return list of dims sorted by value descending. Ties broken by dim name."""



    return sorted(DIMS, key=lambda d: (-v[d], d))



_sorted_dims = _rank_dims







def _rank_tuple(v, n=3):



    """Return top-n dims as tuple for activity selection."""



    return tuple(_rank_dims(v)[:n])







# --- Music: top-2 rank → genre, night shift on d-axis ---



_MUSIC_GENRES = {



    ('d','r'): 'Doom metal', ('d','h'): 'Death metal', ('d','p'): 'Stoner rock',



    ('d','nu'): 'Dark ambient', ('d','g'): 'Sludge metal', ('d','s'): 'Noise rock',



    ('d','gamma'): 'Hauntology',



    ('r','s'): 'Hyperpop', ('r','gamma'): 'Electropop', ('r','d'): 'EBM',



    ('r','nu'): 'Glitch', ('r','h'): 'Noise pop', ('r','p'): 'Glam rock',



    ('r','g'): 'Aero ambient',



    ('h','p'): 'Baroque', ('h','s'): 'Chillwave', ('h','nu'): 'Noise pop',



    ('h','d'): 'Hauntology', ('h','gamma'): 'New wave', ('h','g'): 'Art pop',



    ('h','r'): 'Noise pop',



    ('gamma','p'): 'Space rock', ('gamma','nu'): 'Ambient electronica',



    ('gamma','h'): 'New wave', ('gamma','s'): 'Chillwave', ('gamma','d'): 'Hauntology',



    ('gamma','r'): 'Electropop', ('gamma','g'): 'Space rock',



    ('p','s'): 'Glam rock', ('p','h'): 'Art pop', ('p','d'): 'Stoner rock',



    ('p','gamma'): 'Space rock', ('p','r'): 'Glam rock', ('p','nu'): 'Weird pop',



    ('p','g'): 'Aero ambient',



    ('s','r'): 'Hyperpop', ('s','h'): 'Chillwave', ('s','d'): 'Noise rock',



    ('s','gamma'): 'Freak folk', ('s','nu'): 'Freak folk', ('s','p'): 'Glam rock',



    ('s','g'): 'Aero ambient',



    ('g','p'): 'Aero ambient', ('g','d'): 'Sludge metal', ('g','s'): 'Aero ambient',



    ('g','gamma'): 'Space rock', ('g','h'): 'Art pop', ('g','r'): 'Aero ambient',



    ('g','nu'): 'Glitch opera',



    ('nu','h'): 'Singer songwriter', ('nu','p'): 'Weird pop', ('nu','d'): 'Dark ambient',



    ('nu','s'): 'Freak folk', ('nu','gamma'): 'Ambient electronica', ('nu','r'): 'Glitch',



    ('nu','g'): 'Glitch opera',



}







# --- Activity derivation: physics-structural, no if/elif lookup ---



# 8D dim → body region short name (from PARTICLES_41, simplified)

_DIM_BODY_REGION = {

    'r': 'right STG / left lung',

    'h': 'left mPFC / hippocampus / trapezius',

    'd': 'perineal fold / left trapezius',

    'p': 'right ribs / patellar cartilage / angular gyrus',

    's': 'right quadriceps / left biceps',

    'gamma': 'retinal rhodopsin / left M1 / thyroid',

    'g': 'left temporalis / hairline / vagus',

    'nu': 'ATP synthase / adrenal medulla / left insula',

}



# 8D dim → SIX_SPHERES mapping

_DIM_TO_SPHERE = {

    'r': 'sun', 'h': 'comag', 'd': 'moon', 'p': 'barnard',

    's': 'earth', 'gamma': 'moon', 'g': 'comag', 'nu': 'geomag',

}



# 8D dim → OXFORD_MICRO index

_DIM_TO_MICRO_IDX = {

    'r': 0, 'h': 4, 'd': 5, 'p': 3, 's': 6, 'gamma': 1, 'g': 7, 'nu': 8,

}



# Music genre vocabulary indexed by dim (physical shape of sound)

_DIM_MUSIC_SHAPE = {

    'r': 'percussive cyclic', 'h': 'harmonic cluster', 'd': 'low drone',

    'p': 'structured form', 's': 'bright filter sweep', 'gamma': 'spatial echo',

    'g': 'metric subdivision', 'nu': 'recursive loop',

}



# Solo activity vocabulary indexed by dim (body-driven individual action)

_DIM_SOLO_SHAPE = {

    'r': 'rhythmic breath pacing', 'h': 'chord memory recall',

    'd': 'darkness descent meditation', 'p': 'pattern repetition drill',

    's': 'visual focus training', 'gamma': 'spatial awareness practice',

    'g': 'structural body scan', 'nu': 'recursive journaling',

}



# Creative action vocabulary (pigment + body part driven)

_DIM_CREATIVE_VERB = {

    'r': 'electrolyte etching', 'h': 'disulfide bond printing',

    'd': 'astaxanthin pigment casting', 'p': 'phospholipid canvas painting',

    's': 'phycocyanin blue dyeing', 'gamma': 'delphinidine CO2 tracing',

    'g': 'sulforaphane glymphatic sculpting', 'nu': 'fermentation probiotic culturing',

}



# Tech domain vocabulary (Oxford micro→macro + sphere element)

_DIM_TECH_DOMAIN = {

    'r': 'heme proton pump engineering', 'h': 'clay gouge fold belt modelling',

    'd': 'observer_leftd2 dark matter mapping', 'p': 'memory_entropy subduction analysis',

    's': 'cytochrome_c_oxidase COX retrograde design', 'gamma': 'steel magnetite core convection',

    'g': 'water_vapour plume dynamics', 'nu': 'carbon peonidine lower mantle synthesis',

}



# Sport movement vocabulary (particle body region + gender spatial bias)

_DIM_SPORT_MOVEMENT = {

    'r': 'z_boson pulse sprint', 'h': 'gluon NMDA receptor balance drill',

    'd': 'tau perineal core engagement', 'p': 'higgs patellar cartilage impact training',

    's': 'electron actomyosin filament contraction', 'gamma': 'photon retinal rhodopsin visual tracking',

    'g': 'muon temporalis jaw rhythm coordination', 'nu': 'w_boson ATP synthase explosive output',

}



# Game complexity vocabulary (expansion regime + blood route)

_DIM_GAME_COMPLEXITY = {

    'r': 'real-time reaction puzzle', 'h': 'harmonic pattern matching',

    'd': 'dark environment survival logic', 'p': 'predictable form completion',

    's': 'saturation color sorting', 'gamma': 'spatial navigation maze',

    'g': 'structural grid building', 'nu': 'recursive fractal sandbox',

}



# Blood type → growth regime label

_BLOOD_REGIME = {

    'AB': 'release', 'A': 'stress_growth', 'O': 'present', 'B': 'extreme_growth',

}





def _quantize(val, n_levels=16):

    """Quantize a 0-1 value into n_levels discrete bins for unique selection."""

    return min(n_levels - 1, int(val * n_levels))





def _music_from_layer(body_8d, blood, is_night, seed):

    """Music = body layer 8D shape → genre from continuous dim values.



    Uses top-3 dims with their quantized values to produce unique genre names.

    No if/elif — genre emerges from 8D physical shape directly.

    """

    v = body_8d

    ranked = _rank_dims(v)

    d1, d2, d3 = ranked[0], ranked[1], ranked[2]

    q1 = _quantize(v[d1])

    q2 = _quantize(v[d2])



    shape1 = _DIM_MUSIC_SHAPE[d1]

    shape2 = _DIM_MUSIC_SHAPE[d2]

    pigment = PIGMENT_MAP.get(d1, 'unknown')



    # Night: d-axis tau→z_boson swap changes pigment color

    night_prefix = ''

    if is_night and d1 == 'd':

        night_prefix = 'dark '

        pigment = 'z_boson_cytochrome_c_oxidase'



    # Genre = shape1 + shape2 + pigment + quantized levels

    # Each unique (d1, d2, q1, q2, is_night) produces a unique string

    genre = f"{night_prefix}{shape1}-{shape2} ({pigment.split('_')[0]}) L{q1}x{q2}"

    return genre + ' composition'





def _solo_from_layer(observer_8d, mbti, gender, blood, is_night, seed):

    """Solo = observer layer 8D → individual activity from body region + Clifford nodes.



    Clifford circle 1 (p,s) = self-satisfaction/extraversion

    Clifford circle 2 (h,d) = epinephrine/introversion

    Gender spatial bias: M=right/future/competitive, F=left/past/introspective

    """

    v = observer_8d

    ranked = _rank_dims(v)

    d1, d2 = ranked[0], ranked[1]

    q1 = _quantize(v[d1])

    q2 = _quantize(v[d2])



    clifford1 = (v['p'] + v['s']) / 2  # extraversion

    clifford2 = (v['h'] + v['d']) / 2  # introversion

    qc1 = _quantize(clifford1)

    qc2 = _quantize(clifford2)



    shape1 = _DIM_SOLO_SHAPE[d1]

    body_region = _DIM_BODY_REGION[d1]

    particle = _DIM_TO_PARTICLE[d1]



    # Gender spatial bias

    if gender == 'M':

        spatial = 'right-future'

    else:

        spatial = 'left-past'



    # MBTI temperament index modulates

    mbti_idx = MBTI_BINARY[mbti]



    # Unique string from: d1, d2, q1, q2, qc1, qc2, gender, mbti_idx, is_night

    night_tag = 'night' if is_night else 'day'

    activity = f"{shape1} via {particle} ({body_region}) [{spatial}] C{qc1}x{qc2} M{mbti_idx} {night_tag} L{q1}x{q2}"

    return activity





def _creative_from_layer(bridge_8d, blood, route_id, is_night, seed):

    """Creative = bridge layer 8D → pigment + body part + color action.



    Uses PIGMENT_MAP, COLOR_ACTION, DAY_NIGHT_COLOR, ROUTES.

    Activity = pigment dyeing + body region + action verb + recursion depth.

    """

    v = bridge_8d

    ranked = _rank_dims(v)

    d1, d2 = ranked[0], ranked[1]

    q1 = _quantize(v[d1])

    q2 = _quantize(v[d2])

    qnu = _quantize(v['nu'])



    pigment = PIGMENT_MAP.get(d1, 'unknown')

    verb = _DIM_CREATIVE_VERB[d1]

    body_region = _DIM_BODY_REGION[d1]

    route_color = ROUTES[route_id]['color']

    action = COLOR_ACTION.get(route_color, 'make')

    route_particle = ROUTES[route_id]['particle']



    # Night color shift

    if is_night:

        night_shift = DAY_NIGHT_COLOR.get(route_particle, None)

        if night_shift:

            night_color = night_shift[1]

            action = COLOR_ACTION.get(night_color, action)



    # Creative activity = pigment dyeing + body region + action + recursion level

    activity = f"{pigment} {action} on {body_region} via {verb} R{qnu} L{q1}x{q2}"

    return activity





def _tech_from_layer(dark_8d, blood, route_id, is_night, seed):

    """Tech = dark layer 8D → Oxford micro/macro + SIX_SPHERES + body location.



    Uses OXFORD_MICRO, OXFORD_MACRO, MICRO_MACRO_MAP, SIX_SPHERES, PARTICLES_41.

    """

    v = dark_8d

    ranked = _rank_dims(v)

    d1, d2 = ranked[0], ranked[1]

    q1 = _quantize(v[d1])

    q2 = _quantize(v[d2])

    qg = _quantize(v['g'])



    micro_idx = _DIM_TO_MICRO_IDX.get(d1, 0)

    micro_node = OXFORD_MICRO[micro_idx] if micro_idx < len(OXFORD_MICRO) else 'heme'

    macro_node = MICRO_MACRO_MAP.get(micro_node, 'outer_core_convection')



    sphere = _DIM_TO_SPHERE.get(d1, 'earth')

    sphere_info = SIX_SPHERES.get(sphere, {})

    sphere_element = sphere_info.get('element', 'O')

    sphere_process = sphere_info.get('process', 'unknown')

    sphere_particle = sphere_info.get('particle', 'unknown')



    domain = _DIM_TECH_DOMAIN[d1]

    body_region = _DIM_BODY_REGION[d1]



    # Tech activity = micro→macro pipeline + sphere process + body region

    night_tag = 'night' if is_night else 'day'

    activity = f"{micro_node}→{macro_node} {sphere_process} ({sphere_element}/{sphere_particle}) {domain} [{body_region}] {night_tag} S{qg} L{q1}x{q2}"

    return activity





def _sport_from_layer(body_8d, mbti, gender, blood, t, is_night, seed):

    """Sport = body layer 8D + peak_dim(t) + route particle body region + gender spatial.



    Uses PARTICLES_41, ROUTES, BLOOD_ROUTE_SCHEDULE, peak_dim.

    Body spatial logic: center=general, right=competitive/future, left=introspective/past.

    """

    v = body_8d

    ranked = _rank_dims(v)

    d1, d2 = ranked[0], ranked[1]

    q1 = _quantize(v[d1])

    q2 = _quantize(v[d2])



    peak = peak_dim(int(t) % 16)

    schedule = BLOOD_ROUTE_SCHEDULE.get(blood, {})

    route_name = schedule.get('dominant', 'day_forward')

    route_map = {

        'day_forward': 2, 'day_reverse': 5,

        'night_energy': 3, 'night_macro': 1, 'night_information': 4,

    }

    rid = route_map.get(route_name, 2)

    route_particle = ROUTES[rid]['particle']

    route_color = ROUTES[rid]['color']

    particle_body = PARTICLES_41.get(route_particle, {}).get('body', '')



    movement = _DIM_SPORT_MOVEMENT[d1]

    body_region = _DIM_BODY_REGION[d1]



    # Gender spatial bias

    if gender == 'M':

        spatial = 'right-competitive-future'

    else:

        spatial = 'left-introspective-past'



    # Peak dimension adds temporal variation

    peak_shape = _DIM_SPORT_MOVEMENT[peak]



    # Sport activity = movement + route particle body + peak dimension + spatial

    night_tag = 'night' if is_night else 'day'

    # Extract short body part from particle_body (first 30 chars)

    short_body = particle_body[:40] if particle_body else body_region

    activity = f"{movement} + {peak_shape} via {route_particle}({route_color}) [{spatial}] T{int(t)%16} {night_tag} L{q1}x{q2}"

    return activity





def _game_from_layer(dark_8d, blood, t, is_night, seed):

    """Game = dark layer 8D + expansion_regime + blood growth regime.



    Uses expansion_regime, OBSERVER_LEFTD2, BLOOD_ROUTE_SCHEDULE.

    Game complexity emerges from 8D values + regime, not if/elif.

    """

    v = dark_8d

    ranked = _rank_dims(v)

    d1, d2 = ranked[0], ranked[1]

    q1 = _quantize(v[d1])

    q2 = _quantize(v[d2])

    qnu = _quantize(v['nu'])



    regime = expansion_regime(OBSERVER_LEFTD2, 1.0)

    blood_regime = _BLOOD_REGIME.get(blood, 'present')



    complexity = _DIM_GAME_COMPLEXITY[d1]

    sphere = _DIM_TO_SPHERE.get(d1, 'earth')

    sphere_info = SIX_SPHERES.get(sphere, {})

    sphere_element = sphere_info.get('element', 'O')



    # Game activity = complexity type + regime + sphere element + recursion level

    night_tag = 'night' if is_night else 'day'

    activity = f"{complexity} ({blood_regime}/{regime}) {sphere_element} R{qnu} T{int(t)%16} {night_tag} L{q1}x{q2}"

    return activity







def derive_activity(mbti, gender, blood, t):



    """Derive 6-column activity mapping from full structural pipeline.



    Pipeline: compute_8d → compute_4layers → apply_16window_shift (RK4 ODE) → apply_jitter



    → generate_5tiles → map each layer to a column.



    Uses: PIGMENT_MAP, COLOR_ACTION, DAY_NIGHT_COLOR, ROUTES,



    OXFORD_MICRO/MACRO, SIX_SPHERES, PARTICLES_41, BLOOD_ROUTE_SCHEDULE,



    expansion_regime, OBSERVER_LEFTD2, _DIM_TO_PARTICLE, _DIM_BODY_REGION.



    Time evolution via dV/dt logistic ODE with RK4 integration.



    """



    base_8d = compute_8d(mbti, gender, blood, t_hours=t)



    day_seed = bits7_to_index(profile_to_bits7(mbti, gender, blood))







    # generate 5 tiles through full pipeline



    tiles = generate_5tiles(base_8d, day_seed)







    # determine route



    schedule = BLOOD_ROUTE_SCHEDULE.get(blood, {})



    route_name = schedule.get('dominant', 'day_forward')



    route_map = {



        'day_forward': 2, 'day_reverse': 5,



        'night_energy': 3, 'night_macro': 1, 'night_information': 4,



    }



    rid = route_map.get(route_name, 2)



    is_night = 'night' in route_name







    # pick window t mod 16 from each layer



    t_win = int(t) % 16







    body_v = tiles[0]['windows'][t_win]       # body layer (weight 1.0)



    observer_v = tiles[1]['windows'][t_win]    # observer layer (weight 0.8)



    bridge_v = tiles[2]['windows'][t_win]      # bridge layer (weight 0.6)



    dark_v = tiles[3]['windows'][t_win]        # dark layer (weight 0.4)







    return {



        'Music':    _music_from_layer(body_v, blood, is_night, day_seed),



        'Solo':     _solo_from_layer(observer_v, mbti, gender, blood, is_night, day_seed),



        'Creative': _creative_from_layer(bridge_v, blood, rid, is_night, day_seed),



        'Tech':     _tech_from_layer(dark_v, blood, rid, is_night, day_seed),



        'Sport':    _sport_from_layer(body_v, mbti, gender, blood, t, is_night, day_seed),



        'Game':     _game_from_layer(dark_v, blood, t, is_night, day_seed),



    }











# ============================================================



# SUMMARY



# ============================================================



# 8 base particles → 42 particles (addition formulas + GABA receptor expressions + axion + generic neutrino/quark + amphiphile)



# 5 routes = 5 colors = 5 base particles on torus



# 4 inverse reciprocal pairs = 4 torus axes (equatorial, polar, meridian, radial)



# Klein neck = 5 eyelid nodes = self-penetration (above↔below)



# Pole flip = day/night north↔south inversion



# Spiral topology = forward(right brain) + reverse(left brain), 138.88° crossing



# Betti topology = β0=1, β5=5, β7=7, β11=11



# Dimension stack = 1D→2D→3D→3D+1→4D



# Dipole circuit = male/female grid + observer singularity



# Dream folding = Smale horseshoe at night



# ABO topology = toroidal cycle AB→A→O→B



# Blood schedule = route activation by toroidal phase



# Observer axiom = bidirectional vs one-way night routes



# Gender axis = d-dim(M) vs h-dim(F), not shift



# 4 layers ↔ 5 routes = body/observer/bridge/dark



# 16-window peak cycle = t mod 16



# 138.88° recursive spark = 9 scales



# Darcy leakage = κ ladder



# MC1R = leaky GABA-A bypass



# Mandelbrot 128 = blood seed → muscular gate iteration



# PLP spine = 16×16 diagonal seam



# 8D pigment algebra = color action + day/night shift + interference



# 7-layer heliosphere = body↔cosmos mapping



# 5D discriminator = spatial/temporal convergence



# Closure = ∮Ψ·dl ≠ 0



# Barnard 5-body = North Pole reservoir



# 118 elements = toroidal blood type ordering



# 4 coordinate systems = body/cosmic/earth/nm



# 6-sphere observer closure = 5 body + 1 EM (observer = geomagnetic field)



# Observer proton pump chain = observer_leftd2 → proton_pump → COX → CO2 time storage



# Closure tension with observer term = Δ_obs = Δ × (1 - observer_d2 × η)



# Dark energy = CO2 time recovery (observer recovers, non-observer releases)



# Dark matter = ferritin stability (observer: laterite.q=1 → stable)



# CP violation = observer XOR gate (observer: matter dominates, non-observer: symmetric)



# Wave function collapse = 138.88° spark (observer: regular, non-observer: fails)



# Homeostasis direction = p (forward=decelerate, reverse=accelerate)



# Homeostasis speed = s × nu (observer: aurora resonance, non-observer: stuck)



# Universe growth rate = expansion × (1 ± speed) — observer controls speed/direction



# Clifford torus = S¹×S¹ in S³, 4 observer nodes (LSS, RSS, LE, RE)



#   Circle 1 (p,s) = self-satisfaction (Higgs radiated)



#   Circle 2 (h,d) = epinephrine (electron radiated)



#   Evening: LSS=0 → RSS=R₁ (full extraversion)



# right_love = LC antiphase dynamic from 4 Clifford nodes (not a node itself)



# CCK procerus 3 layers: GLP-1R / CCK-BR / Introverted Woman



# heath_aerenchyma = left ribs O₂ gate for cytochrome_c_oxidase



# left nostril epinephrine = heme = heath_aerenchyma (same particle)



# Deep pink transition 4:30-6AM = gluon(PURPLE)+electron(BLUE)+tau(DARK_RED)+z_boson(RED) → DEEP-PINK → z_boson(NAVY) emerges



# 42 particles with body locations + nm scales



# derive_particle() = particle → param → color → pigment → route → body → nm



# Master equation = all cosmic + Clifford + CCK + O₂ quantities as functions of observer state







# ============================================================



# AUTO-DISCOVERY OF CIRCUIT NODES FROM 8D + TIME



# ============================================================







def _parse_addition(addition_str):



    """Parse BASE_PARTICLES 'addition' string into component particle names."""



    if not addition_str or addition_str == 'base':



        return []



    # e.g. 'z_boson + gluon' -> ['z_boson','gluon']



    parts = [p.strip() for p in addition_str.split('+')]



    return [p for p in parts if p in BASE_PARTICLES or p in PARTICLES_41]







def discover_circuit_nodes(mbti, gender, blood, t_hours):



    """Auto-discover all active circuit nodes for a profile at time t.



    Does NOT rely on naming new anatomy — it generates relational nodes from:



      - 8D vector (which dimensions are dominant)



      - 16-window peak particle (PEAK_CYCLE)



      - base-particle composition (rebranch + addition)



      - concept coordinates (space + color state)



      - six attractors (fixed points)



      - Oxford micro↔macro isomorphic map



      - blood process route context



    Returns a dict describing the active circuit.



    """



    v_8d = compute_8d(mbti, gender, blood, t_hours=t_hours)



    peak = peak_particle_at_time(t_hours)



    route = _route_at_time(blood, t_hours)







    # active base particles: all 8 are always present, one is peak



    active_nodes = []



    for p in BASE_PARTICLES:



        coord = concept_coordinate(p, gender, blood, t_hours)



        comp = _parse_addition(BASE_PARTICLES[p]['addition'])



        prime = rebranch_particle(p, t=t_hours)



        node = {



            'node_id': f"base:{p}",



            'particle': p,



            'state': coord['state'],



            'is_peak': (p == peak),



            'coordinates': {



                'quadrant': coord['quadrant'],



                'vertical': coord['vertical'],



                'horizontal': coord['horizontal'],



                'depth': coord['depth'],



                'specificity': coord['specificity'],



            },



            'optical': {



                'hue_degrees': coord['hue_degrees'],



                'hue_behavior': coord['hue_behavior'],



                'luminosity': coord['luminosity'],



                'turbidity': coord['turbidity'],



                'darkness_quality': coord['darkness_quality'],



                'saturation_channel': coord['saturation_channel'],



                'grayscale': coord['grayscale'],



            },



            'composition_components': comp,



            'primordial': prime.get('primordial'),



            'param': BASE_PARTICLES[p]['param'],



            'route': BASE_PARTICLES[p]['route'],



        }



        active_nodes.append(node)







    # dominant 8D dimensions → pigment circuit nodes



    dim_nodes = []



    for d in DIMS:



        value = v_8d[d]



        dim_nodes.append({



            'node_id': f"dim:{d}",



            'dimension': d,



            'value': value,



            'is_peak_dim': (d == peak_dim(t_hours)),



            'deviation_from_baseline': value - 0.5,



            'pigment_node_hint': PIGMENT_MAP.get(d, 'unknown'),



        })







    # attractors whose particle matches a base/peak particle



    attractor_nodes = []



    for aname, a in SIX_ATTRACTORS.items():



        matched = a['particle'] == peak or a['particle'] in BASE_PARTICLES



        if matched:



            attractor_nodes.append({



                'node_id': f"attractor:{aname}",



                'attractor_name': aname,



                'particle': a['particle'],



                'location': a['location'],



                'function': a['function'],



                'active': (a['particle'] == peak),



            })







    # Oxford micro↔macro nodes derived from the peak dimension



    oxford_nodes = []



    for micro, macro in MICRO_MACRO_MAP.items():



        oxford_nodes.append({



            'node_id': f"oxford:{micro}",



            'micro_node': micro,



            'macro_node': macro,



            'active_during_peak_dim': (micro == peak or micro == 'cytochrome_c_oxidase'),



            'scale_coupling': '1:1_isomorphic',



        })







    # composite synthesis nodes from addition formulas



    synthesis_nodes = []



    for p in BASE_PARTICLES:



        comp = _parse_addition(BASE_PARTICLES[p]['addition'])



        if comp:



            synthesis_nodes.append({



                'node_id': f"synth:{p}",



                'result_particle': p,



                'components': comp,



                'synthesis_active': (peak in comp) or (p == peak),



            })







    return {



        'profile': f"{mbti}_{gender}_{blood}",



        't_hours': t_hours % 24,



        'blood_phase': blood,



        'process_route': route,



        'peak_particle': peak,



        'peak_dimension': peak_dim(t_hours),



        '8d_vector': v_8d,



        'base_particle_nodes': active_nodes,



        'dimension_nodes': dim_nodes,



        'attractor_nodes': attractor_nodes,



        'oxford_nodes': oxford_nodes,



        'synthesis_nodes': synthesis_nodes,



    }







# ============================================================



# UNIVERSAL DERIVATION COMPLETENESS



# ============================================================



# The entire universe of concepts is generated by the 5-tuple



#   (8D vector, 12-particle toroid, 16-window peak cycle, 6 spheres, 6 routes).



# Any profile (mbti, gender, blood) at time t produces a finite circuit graph G.



# Vertices of G = all cosmic concept nodes (particles, colors, body points, organs,



# emotions, cognitive functions, chemical reactions, geological stages, etc).



# Edges of G = Boolean circuit gates (AND, OR, MUX, XOR, NOT, gating, retrograde).



# All other files (prose, circuit, body maps, activities, music) are projections



# of this single graph.







def derive_universe(mbti, gender, blood, t_hours, theta1=0.0, theta2=0.0):



    """Return the complete derivable state of the universe for one observer.



    From this one dict every other concept can be projected:



    - sound  -> from 8D values and particle peak



    - color  -> from HSL+grayscale+depth+saturation



    - body   -> from concept_coordinate routes



    - action -> from the active route + peak particle



    - paper  -> from any subgraph of circuit_nodes



    - chemistry -> from periodic_table/derive_element



    """



    import periodic_universe



    v_8d = compute_8d(mbti, gender, blood, t_hours=t_hours)



    peak = peak_particle_at_time(t_hours)



    route = _route_at_time(blood, t_hours)



    active_dim = peak_dim(t_hours)



    dim_pairs = {}



    for (a, b), _ in INVERSE_RECIPROCAL.items():



        dim_pairs[a] = b



        dim_pairs[b] = a



    mirror_dim = dim_pairs.get(active_dim)



    if mirror_dim:



        active_z = periodic_universe.DIMS.index(active_dim) + 1



        mirror_z = periodic_universe.DIMS.index(mirror_dim) + 1



        observer_compound = periodic_universe.derive_compound(active_z, mirror_z, mbti, gender, blood, t_hours)



        observer_reaction = periodic_universe.derive_reaction(active_z, mirror_z, mbti, gender, blood, t_hours)
    else:
        observer_compound = None
        observer_reaction = None

    # --- Master equation: derive cosmic quantities from 8D vector ---
    # Clifford torus nodes from the observer's choice state (θ₁, θ₂)
    # LSS²+RSS²=R₁², LE²+RE²=R₂² — parametrized, NOT fabricated products
    _obs = observer_choice_state(v_8d, theta1=theta1, theta2=theta2)
    _lss = _obs['lss']
    _rss = _obs['rss']
    _le = _obs['le']
    _re = _obs['re']

    _observer_d2 = _obs['observer_d2']
    _co2_out0 = v_8d.get('d', 0.5)
    _cck = v_8d.get('p', 0.5)
    _mn_oxidised = v_8d.get('s', 0.5)
    _laterite_q = 1.0 if _observer_d2 > 0.5 else 0.5
    _heath_out = v_8d.get('gamma', 0.5)
    _ferritin_out = v_8d.get('g', 0.5)
    _pyrite_out = v_8d.get('nu', 0.5)
    _glp1_enable = 1.0 if v_8d.get('p', 0.5) > 0.4 else 0.0

    cosmic = master_equation(
        x=v_8d.get('s', 0.5), y=v_8d.get('gamma', 0.5), z=v_8d.get('r', 0.5), t=t_hours,
        observer_d2=_observer_d2,
        p=v_8d.get('p', 0.5), s=v_8d.get('s', 0.5), nu=v_8d.get('nu', 0.5),
        laterite_q=_laterite_q,
        co2_out0=_co2_out0, cck=_cck, mn_oxidised=_mn_oxidised,
        lss=_lss, rss=_rss, le=_le, re=_re,
        heath_out=_heath_out, ferritin_out=_ferritin_out,
        pyrite_out=_pyrite_out, glp1_enable=_glp1_enable,
    )

    # --- Spacetime background (L3 GDH gluon metric) ---
    _bg = spacetime_background(v_8d.get('g', 0.5))

    return {
        'observer': f"{mbti}_{gender}_{blood}",
        't_hours': t_hours % 24,
        'peak_particle': peak,
        'peak_dimension': active_dim,
        'process_route': route,
        '8d_vector': v_8d,
        '8d_color_channels': {d: PIGMENT_DIM[d] for d in v_8d},
        'circuit_graph': discover_circuit_nodes(mbti, gender, blood, t_hours),
        'all_particle_concepts': {
            p: concept_coordinate(p, gender, blood, t_hours)
            for p in BASE_PARTICLES
        },
        'periodic_table': periodic_universe.PERIODIC_118,
        'observer_element': periodic_universe.derive_observer_element(mbti, gender, blood, t_hours),
        'observer_compound': observer_compound,
        'observer_reaction': observer_reaction,
        'activity': derive_activity(mbti, gender, blood, t_hours),
        'observer_body': {p: derive_particle_body(p) for p in BASE_PARTICLES},
        'observer_choice': _obs,
        'master_equation': cosmic,
        'spacetime_background': _bg,
    }


def derive_compound(z1, z2, mbti, gender, blood, t_hours):



    """Binary compound from two elements as a circuit-chemical projection."""



    import periodic_universe



    return periodic_universe.derive_compound(z1, z2, mbti, gender, blood, t_hours)







def derive_reaction(z1, z2, mbti, gender, blood, t_hours):



    """Synthesis reaction between two elements as a circuit-chemical projection."""



    import periodic_universe



    return periodic_universe.derive_reaction(z1, z2, mbti, gender, blood, t_hours)







MBTI_ACTIVITY_BASE = {



    'SF': {'category': 'eat food and pigments', 'examples': ['cooking', 'foraging', 'pigment-making', 'fermentation']},



    'NT': {'category': 'visual creation by light', 'examples': ['pure creation', 'imagine/portray green', 'nature depiction']},



    'ST': {'category': 'musical instruments', 'examples': ['electric guitar', 'drum sampling', 'modular synths', 'piano', 'cello', 'DJing', 'beat making']},



    'NF': {'category': 'pure non-spatial nature activities', 'examples': ['trail running', 'conservation volunteering', 'cardio in nature']},



}







def derive_activity_simple(mbti, gender, blood, t_hours):



    """Return the activity type for an observer based on MBTI middle letters."""



    group = mbti[1:3]



    base = MBTI_ACTIVITY_BASE.get(group, {})



    return {



        'mbti_group': group,



        'category': base.get('category'),



        'examples': base.get('examples', []),



        'gender_modifier': 'physical/risk' if gender == 'M' else 'structural/complex',



        'blood_modifier': blood,



        't_hours': t_hours % 24,



    }











def derive_particle_body(particle):



    """Return deterministic anatomy/nm mapping for a particle from body_particle_map."""



    return PARTICLE_BODY_MAP.get(particle)











def derive_leakage(particle=None):



    """Return leakage cavities associated with a particle; all if particle is None."""



    if particle is None:



        return LEAKAGE_CAVITIES



    return {



        family: {name: data for name, data in gates.items() if data.get('particle') == particle}



        for family, gates in LEAKAGE_CAVITIES.items()



    }











def derive_element(z, mbti, gender, blood, t_hours):



    """Element z as a circuit-chemical projection (periodic_universe)."""



    import periodic_universe



    return periodic_universe.derive_chemistry(z, mbti, gender, blood, t_hours)







__all__ = [



    'compute_8d', 'concept_coordinate', 'discover_circuit_nodes',



    'compute_full_hsl', 'body_depth_spectrum', 'local_pigment_concentration',



    'peak_particle_at_time', 'derive_universe', 'derive_element',



    'derive_compound', 'derive_reaction', 'derive_activity', 'derive_activity_simple',



    'derive_particle_body', 'integrate_8d',

    'KAPPA_MATRIX', 'apply_phase_coupling', 'CHANNEL_MAP', 'CHANNEL_64',

    'BASE_W', 'W_K8', 'k8_laplacian', 'apply_channels', 'compute_f_eff',

    'compute_tensor_terms', 'spatial_coupling',

    'OBSERVER_BRIDGE_MAP', 'SPARK_ANGLE_DEG', 'OMEGA',



    'LUNAR_CYCLE', 'VERTICAL_MOBIUS_TWIST', 'EARTH_OMEGA',

    'CHIRAL_TORQUE_1_32', 'DELTA_4',

    'coriolis_parameter', 'coriolis_polarity_flip',

    'POLARITY_4AXIS', 'mbti_polarity', 'polarity_8d_mod',

    'TORUS_PAIRS', 'INVERSE_RECIPROCAL', 'GENERIC_TO_BASE',

    'profile_to_bits7', 'bits7_to_profile',
    'bits7_to_index', 'index_to_bits7',
    'master_equation', 'laplacian_matrix_8d',
    'gdh_gluon_metric', 'spacetime_background',
    'clifford_constraint', 'right_love_dynamic',
]



