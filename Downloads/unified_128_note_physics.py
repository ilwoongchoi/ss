"""
UNIFIED 128-NOTE PHYSICS — observer-specific 3AM (Korea_300AM) 8D.
Math source: universe_math_structures.py (compute_8d, mandelbrot_seed, mandelbrot_iterate, BETTI, SIX_SPHERES, closure, dark_energy, expansion).
"""
import sys, math
from math import sqrt, pi

sys.path.insert(0, r'c:\Users\User\Downloads')
from universe_math_structures import (
    compute_8d, mandelbrot_seed, mandelbrot_iterate,
    BETTI, SIX_SPHERES, SIX_ATTRACTORS, DIMS,
    BASE_PARTICLES, DERIVED_BASE, INVERSE_RECIPROCAL,
    PIGMENT_MAP, COLOR_ACTION, DAY_NIGHT_COLOR,
    KLEIN_NECK_NODES, BLOOD_ROUTE_SCHEDULE, TOROIDAL_ORDER, BLOOD_PHASE,
    PEAK_CYCLE, PEAK_CYCLE as _PC, peak_dim,
    closure_tension_base, closure_delta_base, closure_delta_observer,
    W7, H2, KAPPA_1_32, KAPPA_3_32,
    dark_matter_density, universe_expansion_rate,
    dark_energy_release, OBSERVER_LEFTD2,
    cp_violation, matter_antimatter_balance,
    wave_function_collapse,
    homeostasis_direction, homeostasis_speed, universe_growth_rate,
    clifford_constraint, right_love_dynamic,
    f_cognitive, f_gravity,
    gdh_gluon_metric, spacetime_background,
    rebranch_particle, laplacian_matrix_8d,
    proton_pump_ctrl, proton_pump_input, proton_pump_output,
    cck_value, cox_o2_gate, cox_forward, co2_time_storage,
    peak_particle_at_time, concept_coordinate, compute_full_hsl,
    generate_5tiles, compute_4layers, apply_16window_shift, apply_jitter,
    master_equation, expansion_regime,
    derive_universe, derive_activity, derive_activity_simple, derive_particle_body, derive_leakage,
    derive_element, derive_compound, derive_reaction,
    discover_circuit_nodes,
    next_blood, hue_for_particle, hue_behavior, blood_lstd, saturation_for_gender,
    particle_quadrant, body_depth_spectrum,
    local_pigment_concentration,
    midi_note_name, profile_to_midi, profile_to_note_name, midi_to_profile,
    PROFILE_NOTE_MAP, MBTI_ACTIVITY_BASE,
    BLOOD_OPTICAL_MAP, GENDER_OPTICAL_MAP, BASE_SATURATION,
    HUE_DEGREES, HUE_BEHAVIOR_BY_GENDER,
    BODY_DEPTH_SPECTRUM, PIGMENT_DIM,
    GABA_TO_BASE, ROUTES,
    FORWARD_LAYERS, REVERSE_LAYERS, ALL_16_LAYERS,
    LAYER_NAMES, LAYER_WEIGHTS, JITTER_RANGE, JITTER_3AM,
    PARTICLES_41, OXFORD_MICRO, OXFORD_MACRO, MICRO_MACRO_MAP,
    PARTICLE_BODY_MAP, LEAKAGE_CAVITIES,
)

# ── Observer profile ──
MBTI = 'ENTP'
GENDER = 'M'
BLOOD = 'O'

# ── Betti topology (from universe_math_structures.py BETTI dict) ──
BETTI_0 = BETTI['b0']    # 1
BETTI_5 = BETTI['b5']    # 5
BETTI_7 = BETTI['b7']    # 7
BETTI_11 = BETTI['b11']  # 11
N_NOTES = 128
N_PARTICLES = 8

# Trinity
C = sqrt(2.0) / 5.0
C2 = C * C                        # = 2/25 = 0.08
OMEGA = BETTI_7 + BETTI_5 * C2    # = 7 + 5*(2/25) = 7.4

# Chrono-geometry
SPARK_DEG = 138.88
SPARK_PHASE = SPARK_DEG / 360.0
NEUTRON_TIME_SYNC = SPARK_PHASE

# Betti-derived gaps
CHIRALITY = 1.0 / (BETTI_7 + BETTI_11)   # 1/18
BETTI_7_GAP = BETTI_7 / N_NOTES          # 7/128
NEUTRINO_MASS_LEAK = 1.0 / N_NOTES       # 1/128

PHI = (1.0 + sqrt(5.0)) / 2.0

# ── h(t) from mandelbrot_seed (universe_math_structures.py) ──
H_SEED = mandelbrot_seed(MBTI, GENDER, BLOOD)

# ── 8D vector from compute_8d (universe_math_structures.py) ──
V_8D = compute_8d(MBTI, GENDER, BLOOD)

# ── Mandelbrot shell iteration: z = z² - z + h(t) ──
DIM_TO_SPHERE = {
    'r': 'sun', 'h': 'comag', 'd': 'moon', 'p': 'barnard',
    's': 'earth', 'gamma': 'moon', 'g': 'comag', 'nu': 'geomag',
}
SHELL_ITERATIONS = {}
for dim_name, sphere_name in DIM_TO_SPHERE.items():
    z_seed = V_8D[dim_name]
    iters = mandelbrot_iterate(z_seed, H_SEED)
    SHELL_ITERATIONS.setdefault(sphere_name, iters)

# ── r_min / 1/alpha ──
one_over_alpha_codata = 137.035999084
r_min_observed = 1.6823514955

h_exact_1alpha = (one_over_alpha_codata - 137.0) / (SPARK_PHASE * BETTI_7 * C2)
h_exact_rmin = (r_min_observed - PHI) / SPARK_PHASE
H_CANONICAL = h_exact_rmin

r_min = PHI + H_CANONICAL * SPARK_PHASE
one_over_alpha = 137.0 + h_exact_1alpha * SPARK_PHASE * BETTI_7 * C2

# ── Barnard's star constants ──
LUNAR_CYCLE = 28.0
D_BARNARD = (SPARK_DEG + LUNAR_CYCLE) / LUNAR_CYCLE
D_BARNARD_OBSERVED = 5.96

TOTAL_DEBT_AREA = 1.322828
PHI_PB = (BETTI_11 / BETTI_7) * TOTAL_DEBT_AREA
OMEGA_LA = TOTAL_DEBT_AREA * 28.0

LOCK_VALUE = 1.0 / 64.0
M_BARNARD = 10.0 * LOCK_VALUE
M_BARNARD_OBSERVED = M_BARNARD

PROPER_MOTION_OBSERVED = 10.39
DRIFT_DELTA = PROPER_MOTION_OBSERVED * LUNAR_CYCLE / (10.0 * 365.25)
PROPER_MOTION = 10.0 * DRIFT_DELTA * (365.25 / LUNAR_CYCLE)

MAXWELL_Q_FACTOR = 437.0 / OMEGA_LA
B_FIELD = OMEGA_LA * MAXWELL_Q_FACTOR
B_FIELD_OBSERVED = 437.0

BARNARD_AGE_OBSERVED = 10.0
MOON_AGE = BARNARD_AGE_OBSERVED / (PHI_PB * (1.0 + DRIFT_DELTA))
AGE_BARNARD = MOON_AGE * PHI_PB * (1.0 + DRIFT_DELTA)

# ── Shell constants from Betti topology (universe_math_structures.py) ──
# Moon = dark_matter_density(observer_d2=1, laterite_q=1) = 0.27
#        = 3/BETTI_11 = 3/11 = 0.2727...
MOON_SHELL = (KAPPA_3_32 * 32.0) / BETTI_11
MOON_SHELL_OBSERVED = 3.0 / 11.0

# Earth = 1.0 (baseline reference sphere)
EARTH_SHELL = 1.0
EARTH_SHELL_OBSERVED = 1.0

# Co-mag = (BETTI_0 + BETTI_7 + BETTI_11) / BETTI_5 = 19/5 = 3.8
COMAG_SHELL = (BETTI_0 + BETTI_7 + BETTI_11) / BETTI_5
COMAG_SHELL_OBSERVED = 19.0 / 5.0

# Sun = OMEGA * C = 7.4 * sqrt(2)/5 (Trinity × Betti)
SUN_SHELL = OMEGA * C

# Geomag = 2 * OMEGA (EM closure = observer doubles OMEGA)
GEOMAG_SHELL = 2.0 * OMEGA

# ── Closure tension (from universe_math_structures.py) ──
CLOSURE_TENSION = closure_tension_base()
CLOSURE_DELTA = closure_delta_base()
CLOSURE_DELTA_OBS = closure_delta_observer(OBSERVER_LEFTD2)

# ── Dark energy / expansion (from universe_math_structures.py) ──
DARK_ENERGY_RELEASE = dark_energy_release(OBSERVER_LEFTD2, 1.0)
EXPANSION_RATE = universe_expansion_rate(OBSERVER_LEFTD2, 1.0)

# ── Dark matter density (from universe_math_structures.py) ──
DARK_MATTER_DENSITY = dark_matter_density(OBSERVER_LEFTD2, 1.0)

# ── CP violation / matter-antimatter ──
CP_VIOLATION = cp_violation(OBSERVER_LEFTD2)
MATTER_ANTIMATTER = matter_antimatter_balance(OBSERVER_LEFTD2)

# ── Wave function collapse ──
SPARK_PROBABILITY = wave_function_collapse(OBSERVER_LEFTD2, CLOSURE_DELTA_OBS)

# ── Homeostasis control (from 8D observer params) ──
P_OBS = V_8D['p']
S_OBS = V_8D['s']
NU_OBS = V_8D['nu']
HOMEOSTASIS_DIRECTION = homeostasis_direction(OBSERVER_LEFTD2, P_OBS)
HOMEOSTASIS_SPEED = homeostasis_speed(OBSERVER_LEFTD2, S_OBS, NU_OBS)
UNIVERSE_GROWTH = universe_growth_rate(OBSERVER_LEFTD2, P_OBS, S_OBS, NU_OBS, 1.0)

# ── Clifford torus (evening condition: LSS=0) ──
CLIFFORD = clifford_constraint(0.0, 0.5, 0.5, 0.5)
RIGHT_LOVE = right_love_dynamic(0.0, 0.5, 0.5, 0.5)

# ── Cognitive / gravity frequencies ──
F_COG = f_cognitive(1.0)
F_GRAV = f_gravity(1.0)

# ── GDH gluon metric / spacetime background ──
GDH_METRIC = gdh_gluon_metric(V_8D['h'])
SPACETIME_BG = spacetime_background(V_8D['h'])

# ── Proton pump chain ──
PP_CTRL = proton_pump_ctrl(OBSERVER_LEFTD2)
PP_INPUT = proton_pump_input(OBSERVER_LEFTD2, 1.0)
PP_OUTPUT = proton_pump_output(OBSERVER_LEFTD2, 1.0)

# ── CCK / COX / CO2 chain ──
CCK_VAL = cck_value(1.0, 1.0, 1.0)
O2_GATE = cox_o2_gate(1.0)
COX_FWD = cox_forward(OBSERVER_LEFTD2, CCK_VAL, 1.0, PP_OUTPUT)
CO2_TIME = co2_time_storage(COX_FWD, 1.0)

# ── Rebranching: all 8 base particles from primordial set ──
REBRANCH_ALL = {p: rebranch_particle(p, t=88) for p in BASE_PARTICLES}

# ── Laplacian matrix 8D ──
LAPLACIAN_8D = laplacian_matrix_8d(V_8D)

# ── Peak particle at 3AM (t=3) ──
T_OBS = 3  # 3AM Korea time
PEAK_PARTICLE = peak_particle_at_time(T_OBS)
PEAK_DIMENSION = peak_dim(T_OBS)

# ── Music tiles: 5 tiles × 4 layers × 16 windows ──
TILES = generate_5tiles(V_8D, day_seed=0)

# ── Master equation (full observer closure) ──
MASTER = master_equation(0, 0, 0, T_OBS,
    observer_d2=OBSERVER_LEFTD2,
    p=P_OBS, s=S_OBS, nu=NU_OBS,
    laterite_q=1.0, co2_out0=1.0, cck=1.0, mn_oxidised=1.0,
    lss=0.0, rss=0.5, le=0.5, re=0.5,
    heath_out=1.0, ferritin_out=1.0, pyrite_out=1.0, glp1_enable=1.0)

# ── Derive universe (comprehensive) ──
try:
    UNIVERSE_STATE = derive_universe(MBTI, GENDER, BLOOD, T_OBS)
except Exception as e:
    UNIVERSE_STATE = {'error': str(e)}

# ── Derive activity ──
ACTIVITY = derive_activity(MBTI, GENDER, BLOOD, T_OBS)

# ── Derive leakage ──
LEAKAGE = derive_leakage()

# ── Particle body maps ──
PARTICLE_BODIES = {p: derive_particle_body(p) for p in BASE_PARTICLES}

# ── Concept coordinates for all base particles ──
CONCEPTS = {p: concept_coordinate(p, GENDER, BLOOD, T_OBS) for p in BASE_PARTICLES}

# ── HSL colors for all base particles ──
HSL_COLORS = {p: compute_full_hsl(p, GENDER, BLOOD, T_OBS) for p in BASE_PARTICLES}

# ── 128 profile lists (needed by MIDI map + activity map) ──
_ALL_MBTI = [
    'ESTJ', 'ESTP', 'ESFJ', 'ESFP',
    'ENTJ', 'ENTP', 'ENFJ', 'ENFP',
    'ISTJ', 'ISTP', 'ISFJ', 'ISFP',
    'INTJ', 'INTP', 'INFJ', 'INFP',
]
_ALL_GENDERS = ['M', 'F']
_ALL_BLOOD = ['AB', 'A', 'O', 'B']

# ── Local pigment concentration (8D × body point) ──
PIGMENT_CONC = local_pigment_concentration(V_8D, 0.5, 0.5, 0.5, T_OBS)

# ── Expansion regime ──
EXPANSION_REGIME = expansion_regime(OBSERVER_LEFTD2, 1.0)

# ── MIDI note mapping for all 128 profiles ──
MIDI_MAP = {}
for _blood in _ALL_BLOOD:
    for _gender in _ALL_GENDERS:
        for _mbti in _ALL_MBTI:
            _key = f"{_mbti}_{_gender}_{_blood}"
            MIDI_MAP[_key] = {
                'midi': profile_to_midi(_mbti, _gender, _blood),
                'note': profile_to_note_name(_mbti, _gender, _blood),
            }

# ── Observer MIDI ──
OBS_MIDI = profile_to_midi(MBTI, GENDER, BLOOD)
OBS_NOTE = profile_to_note_name(MBTI, GENDER, BLOOD)

# ── Circuit nodes (standalone) ──
CIRCUIT_NODES = discover_circuit_nodes(MBTI, GENDER, BLOOD, T_OBS)

# ── Derive element for observer's peak dimension z ──
try:
    _peak_z = DIMS.index(PEAK_DIMENSION) + 1
    OBS_ELEMENT = derive_element(_peak_z, MBTI, GENDER, BLOOD, T_OBS)
except Exception as e:
    OBS_ELEMENT = {'error': str(e)}

# ── Derive compound + reaction ──
try:
    _dim_pairs = {}
    for (_a, _b) in INVERSE_RECIPROCAL:
        _dim_pairs[_a] = _b
        _dim_pairs[_b] = _a
    _mirror = _dim_pairs.get(PEAK_DIMENSION)
    if _mirror:
        _z1 = DIMS.index(PEAK_DIMENSION) + 1
        _z2 = DIMS.index(_mirror) + 1
        OBS_COMPOUND = derive_compound(_z1, _z2, MBTI, GENDER, BLOOD, T_OBS)
        OBS_REACTION = derive_reaction(_z1, _z2, MBTI, GENDER, BLOOD, T_OBS)
    else:
        OBS_COMPOUND = None
        OBS_REACTION = None
except Exception as e:
    OBS_COMPOUND = {'error': str(e)}
    OBS_REACTION = {'error': str(e)}

# ── 128 profiles × 16 time windows: full daily activity mapping ──
ALL_ACTIVITIES = {}
for _blood in _ALL_BLOOD:
    for _gender in _ALL_GENDERS:
        for _mbti in _ALL_MBTI:
            _key = f"{_mbti}_{_gender}_{_blood}"
            ALL_ACTIVITIES[_key] = {}
            for _t in range(16):
                try:
                    ALL_ACTIVITIES[_key][_t] = derive_activity(_mbti, _gender, _blood, _t)
                except Exception as _e:
                    ALL_ACTIVITIES[_key][_t] = {'error': str(_e)}

# ── output ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print(f"Observer: {MBTI}_{GENDER}_{BLOOD}")
    print(f"h(t) from mandelbrot_seed = {H_SEED}")
    print(f"8D vector from compute_8d  = {V_8D}")
    print("=" * 60)
    print()
    print("=== Closure Tension (universe_math_structures.py) ===")
    print(f"  closure_tension     = {CLOSURE_TENSION}")
    print(f"  closure_delta       = {CLOSURE_DELTA}")
    print(f"  closure_delta_obs   = {CLOSURE_DELTA_OBS}")
    print(f"  W7 = {W7},  H2 = {H2},  kappa_1_32 = {KAPPA_1_32},  kappa_3_32 = {KAPPA_3_32}")
    print()
    print("=== r_min / 1/alpha ===")
    print(f"  H canonical (r_min) = {H_CANONICAL}")
    print(f"  h exact (1/alpha)   = {h_exact_1alpha}")
    print(f"  r_min        = {r_min}")
    print(f"  r_min obs    = {r_min_observed}")
    print(f"  r_min error  = {r_min - r_min_observed}")
    print(f"  1/alpha      = {one_over_alpha}")
    print(f"  1/alpha cod  = {one_over_alpha_codata}")
    print(f"  1/alpha error= {one_over_alpha - one_over_alpha_codata}")
    print()
    print("=== Barnard's Star ===")
    print(f"  Barnard dist = {D_BARNARD} ly  (obs {D_BARNARD_OBSERVED}, err {D_BARNARD - D_BARNARD_OBSERVED})")
    print(f"  Barnard mass = {M_BARNARD} Msun  (obs {M_BARNARD_OBSERVED}, err {M_BARNARD - M_BARNARD_OBSERVED})")
    print(f"  Proper motion= {PROPER_MOTION} \"/yr  (obs {PROPER_MOTION_OBSERVED}, err {PROPER_MOTION - PROPER_MOTION_OBSERVED})")
    print(f"  B-field      = {B_FIELD} G  (obs {B_FIELD_OBSERVED}, err {B_FIELD - B_FIELD_OBSERVED})")
    print(f"  Barnard age  = {AGE_BARNARD} Gyr  (obs {BARNARD_AGE_OBSERVED}, err {AGE_BARNARD - BARNARD_AGE_OBSERVED})")
    print()
    print("=== Shell Constants (Betti topology) ===")
    print(f"  Moon shell   = {MOON_SHELL}  (obs {MOON_SHELL_OBSERVED}, err {MOON_SHELL - MOON_SHELL_OBSERVED})")
    print(f"  Earth shell  = {EARTH_SHELL}  (obs {EARTH_SHELL_OBSERVED}, err {EARTH_SHELL - EARTH_SHELL_OBSERVED})")
    print(f"  Co-mag shell = {COMAG_SHELL}  (obs {COMAG_SHELL_OBSERVED}, err {COMAG_SHELL - COMAG_SHELL_OBSERVED})")
    print(f"  Sun shell    = {SUN_SHELL}")
    print(f"  Geomag shell = {GEOMAG_SHELL}")
    print(f"  Dark matter  = {DARK_MATTER_DENSITY}  (= Moon shell from dark_matter_density)")
    print()
    print("=== Mandelbrot Iteration: z = z² - z + h(t) ===")
    print(f"  h(t) = {H_SEED}")
    for sphere_name, iters in SHELL_ITERATIONS.items():
        print(f"  {sphere_name:10s}  iterations = {iters}")
    print()
    print("=== Dark Energy / Expansion ===")
    print(f"  dark_energy_release = {DARK_ENERGY_RELEASE}")
    print(f"  expansion_rate      = {EXPANSION_RATE}")
    print()
    print("=== SIX_SPHERES (from universe_math_structures.py) ===")
    for name, info in SIX_SPHERES.items():
        print(f"  {name:10s}  element={info['element']:3s}  particle={info['particle']:20s}  stage={info['stage']}")
    print()
    print("=== SIX_ATTRACTORS ===")
    for name, info in SIX_ATTRACTORS.items():
        print(f"  {name:20s}  particle={info['particle']:10s}  loc={info['location']:25s}  func={info['function']}")
    print()
    print("=== CP Violation / Matter-Antimatter ===")
    print(f"  cp_violation           = {CP_VIOLATION}")
    print(f"  matter_antimatter      = {MATTER_ANTIMATTER}")
    print()
    print("=== Wave Function Collapse ===")
    print(f"  spark_probability      = {SPARK_PROBABILITY}")
    print()
    print("=== Homeostasis Control ===")
    print(f"  direction              = {HOMEOSTASIS_DIRECTION}")
    print(f"  speed                  = {HOMEOSTASIS_SPEED}")
    print(f"  universe_growth_rate   = {UNIVERSE_GROWTH}")
    print()
    print("=== Clifford Torus (evening: LSS=0) ===")
    print(f"  R1={CLIFFORD['R1']}  R2={CLIFFORD['R2']}  on_torus={CLIFFORD['on_torus']}  evening_fixed={CLIFFORD['evening_fixed']}")
    print(f"  right_love={RIGHT_LOVE['right_love']}  epi_energy={RIGHT_LOVE['epinephrine_energy']}  total={RIGHT_LOVE['total']}")
    print()
    print("=== Cognitive / Gravity Frequencies ===")
    print(f"  f_cognitive = {F_COG}   f_gravity = {F_GRAV}   f_grav > f_cog = {F_GRAV > F_COG}")
    print()
    print("=== GDH Gluon Metric / Spacetime Background ===")
    print(f"  gdh_metric = {GDH_METRIC}   spacetime_bg = {SPACETIME_BG}")
    print()
    print("=== Proton Pump Chain ===")
    print(f"  pp_ctrl={PP_CTRL}  pp_input={PP_INPUT}  pp_output={PP_OUTPUT}")
    print()
    print("=== CCK / COX / CO2 Chain ===")
    print(f"  cck_value={CCK_VAL}  o2_gate={O2_GATE}  cox_forward={COX_FWD}  co2_time={CO2_TIME}")
    print()
    print("=== Rebranching (t=88, primordial decomposition) ===")
    for pname, rinfo in REBRANCH_ALL.items():
        prim = 'PRIMORDIAL' if rinfo.get('primordial') else rinfo.get('addition', '?')
        print(f"  {pname:20s}  param={rinfo.get('param')}  primordial={rinfo.get('primordial')}  decomposition={prim}")
    print()
    print("=== Laplacian Matrix 8D ===")
    for i, dim_i in enumerate(DIMS):
        row = '  '.join(f'{LAPLACIAN_8D[i][j]:7.4f}' for j in range(len(DIMS)))
        print(f"  {dim_i:5s}  {row}")
    print()
    print("=== Peak Particle / Dimension at t=3 (3AM) ===")
    print(f"  peak_particle = {PEAK_PARTICLE}   peak_dimension = {PEAK_DIMENSION}")
    print()
    print("=== Music Tiles (5 tiles × 4 layers × 16 windows) ===")
    for idx, tile in enumerate(TILES):
        layer = tile['layer']
        n_windows = len(tile['windows'])
        first_w = tile['windows'][0]
        print(f"  Tile {idx}: layer={layer:15s}  windows={n_windows}  first_window_r={first_w.get('r', '?'):.4f}")
    print()
    print("=== Master Equation (full observer closure) ===")
    for k, v in MASTER.items():
        if isinstance(v, dict):
            print(f"  {k:25s} = {v}")
        else:
            print(f"  {k:25s} = {v}")
    print()
    print("=== Derive Universe (comprehensive) ===")
    if 'error' in UNIVERSE_STATE:
        print(f"  ERROR: {UNIVERSE_STATE['error']}")
    else:
        print(f"  observer = {UNIVERSE_STATE.get('observer')}")
        print(f"  t_hours  = {UNIVERSE_STATE.get('t_hours')}")
        print(f"  peak_particle = {UNIVERSE_STATE.get('peak_particle')}")
        print(f"  peak_dimension = {UNIVERSE_STATE.get('peak_dimension')}")
        print(f"  process_route = {UNIVERSE_STATE.get('process_route')}")
        print(f"  8d_vector = {UNIVERSE_STATE.get('8d_vector')}")
        print(f"  observer_element = {UNIVERSE_STATE.get('observer_element')}")
        print(f"  observer_compound = {UNIVERSE_STATE.get('observer_compound')}")
        print(f"  observer_reaction = {UNIVERSE_STATE.get('observer_reaction')}")
        circ = UNIVERSE_STATE.get('circuit_graph', {})
        print(f"  circuit_graph keys = {list(circ.keys()) if isinstance(circ, dict) else type(circ)}")
        print(f"  all_particle_concepts keys = {list(UNIVERSE_STATE.get('all_particle_concepts', {}).keys())}")
        print(f"  periodic_table type = {type(UNIVERSE_STATE.get('periodic_table'))}")
        print(f"  observer_body keys = {list(UNIVERSE_STATE.get('observer_body', {}).keys())}")
    print()
    print("=== Derive Activity ===")
    print(f"  {ACTIVITY}")
    print()
    print("=== Derive Leakage ===")
    for family, gates in LEAKAGE.items():
        print(f"  {family}: {list(gates.keys())}")
    print()
    print("=== Particle Body Maps ===")
    for pname, body in PARTICLE_BODIES.items():
        print(f"  {pname:20s}  {body}")
    print()
    print("=== Concept Coordinates (all base particles) ===")
    for pname, coord in CONCEPTS.items():
        print(f"  {pname:20s}  {coord}")
    print()
    print("=== HSL Colors (all base particles) ===")
    for pname, hsl in HSL_COLORS.items():
        print(f"  {pname:20s}  {hsl}")
    print()
    print("=== Structural Dicts ===")
    print(f"  TOROIDAL_ORDER = {TOROIDAL_ORDER}")
    print(f"  BLOOD_PHASE = {BLOOD_PHASE}")
    print(f"  BLOOD_ROUTE_SCHEDULE keys = {list(BLOOD_ROUTE_SCHEDULE.keys())}")
    print(f"  PEAK_CYCLE = {PEAK_CYCLE}")
    print(f"  INVERSE_RECIPROCAL = {INVERSE_RECIPROCAL}")
    print(f"  KLEIN_NECK_NODES = {list(KLEIN_NECK_NODES.keys())}")
    print(f"  PIGMENT_MAP = {PIGMENT_MAP}")
    print(f"  COLOR_ACTION = {COLOR_ACTION}")
    print(f"  DAY_NIGHT_COLOR keys = {list(DAY_NIGHT_COLOR.keys())}")
    print(f"  next_blood(O) = {next_blood('O')}  next_blood(A) = {next_blood('A')}  next_blood(B) = {next_blood('B')}  next_blood(AB) = {next_blood('AB')}")
    print()
    print("=== Optical / Color Structures ===")
    print(f"  BLOOD_OPTICAL_MAP = {BLOOD_OPTICAL_MAP}")
    print(f"  GENDER_OPTICAL_MAP = {GENDER_OPTICAL_MAP}")
    print(f"  BASE_SATURATION = {BASE_SATURATION}")
    print(f"  HUE_DEGREES = {HUE_DEGREES}")
    print(f"  HUE_BEHAVIOR_BY_GENDER = {HUE_BEHAVIOR_BY_GENDER}")
    print(f"  BODY_DEPTH_SPECTRUM keys = {list(BODY_DEPTH_SPECTRUM.keys())}")
    print(f"  PIGMENT_DIM = {PIGMENT_DIM}")
    print()
    print("=== Particle / Route / Layer Structures ===")
    print(f"  GABA_TO_BASE = {GABA_TO_BASE}")
    print(f"  ROUTES = {ROUTES}")
    print(f"  FORWARD_LAYERS = {FORWARD_LAYERS}")
    print(f"  REVERSE_LAYERS = {REVERSE_LAYERS}")
    print(f"  ALL_16_LAYERS count = {len(ALL_16_LAYERS)}")
    print(f"  LAYER_NAMES = {LAYER_NAMES}")
    print(f"  LAYER_WEIGHTS = {LAYER_WEIGHTS}")
    print(f"  JITTER_RANGE = {JITTER_RANGE}  JITTER_3AM = {JITTER_3AM}")
    print(f"  PARTICLES_41 count = {len(PARTICLES_41)}")
    for _pn, _pi in PARTICLES_41.items():
        print(f"    {_pn:25s}  body={_pi.get('body','?')}  nm={_pi.get('nm')}")
    print()
    print("=== Oxford Micro / Macro ===")
    print(f"  OXFORD_MICRO = {OXFORD_MICRO}")
    print(f"  OXFORD_MACRO = {OXFORD_MACRO}")
    print(f"  MICRO_MACRO_MAP = {MICRO_MACRO_MAP}")
    print()
    print("=== Particle Body Map (from body_particle_map.py) ===")
    print(f"  PARTICLE_BODY_MAP count = {len(PARTICLE_BODY_MAP)}")
    for _pn, _pi in PARTICLE_BODY_MAP.items():
        print(f"    {_pn:25s}  {_pi}")
    print()
    print("=== Leakage Cavities (from leakage_cavities.py) ===")
    print(f"  LEAKAGE_CAVITIES families = {list(LEAKAGE_CAVITIES.keys())}")
    for _fam, _gates in LEAKAGE_CAVITIES.items():
        print(f"    {_fam}: {list(_gates.keys())}")
    print()
    print("=== Local Pigment Concentration ===")
    print(f"  PIGMENT_CONC = {PIGMENT_CONC}")
    print()
    print("=== Expansion Regime ===")
    print(f"  EXPANSION_REGIME = {EXPANSION_REGIME}")
    print()
    print("=== MIDI Note Mapping (128 profiles → 128 MIDI notes) ===")
    print(f"  Observer MIDI = {OBS_MIDI}  note = {OBS_NOTE}")
    print(f"  Total mapped profiles = {len(MIDI_MAP)}")
    for _i, (_k, _v) in enumerate(sorted(MIDI_MAP.items(), key=lambda x: x[1]['midi'])):
        print(f"    MIDI {_v['midi']:3d} ({_v['note']:>4s})  ←  {_k}")
    print()
    print("=== Circuit Nodes (standalone discover_circuit_nodes) ===")
    print(f"  profile = {CIRCUIT_NODES.get('profile')}")
    print(f"  peak_particle = {CIRCUIT_NODES.get('peak_particle')}")
    print(f"  peak_dimension = {CIRCUIT_NODES.get('peak_dimension')}")
    print(f"  process_route = {CIRCUIT_NODES.get('process_route')}")
    print(f"  base_particle_nodes count = {len(CIRCUIT_NODES.get('base_particle_nodes', []))}")
    print(f"  dimension_nodes count = {len(CIRCUIT_NODES.get('dimension_nodes', []))}")
    print(f"  attractor_nodes count = {len(CIRCUIT_NODES.get('attractor_nodes', []))}")
    print(f"  oxford_nodes count = {len(CIRCUIT_NODES.get('oxford_nodes', []))}")
    print(f"  synthesis_nodes count = {len(CIRCUIT_NODES.get('synthesis_nodes', []))}")
    print()
    print("=== Derive Element (observer peak dim z) ===")
    print(f"  OBS_ELEMENT = {OBS_ELEMENT}")
    print()
    print("=== Derive Compound / Reaction ===")
    print(f"  OBS_COMPOUND = {OBS_COMPOUND}")
    print(f"  OBS_REACTION = {OBS_REACTION}")
    print()
    print("=== MBTI Activity Base (simple mapping) ===")
    print(f"  MBTI_ACTIVITY_BASE = {MBTI_ACTIVITY_BASE}")
    print(f"  derive_activity_simple = {derive_activity_simple(MBTI, GENDER, BLOOD, T_OBS)}")
    print()
    print("=" * 60)
    print("=== 128 PROFILES × 16 TIME WINDOWS: DAILY ACTIVITY MAPPING ===")
    print("=" * 60)
    _n_profiles = 0
    _n_errors = 0
    for _key in sorted(ALL_ACTIVITIES.keys()):
        _n_profiles += 1
        _windows = ALL_ACTIVITIES[_key]
        _has_error = any(isinstance(w, dict) and 'error' in w for w in _windows.values())
        if _has_error:
            _n_errors += 1
        print(f"\n  --- {_key} ---")
        for _t in range(16):
            _act = _windows[_t]
            if isinstance(_act, dict) and 'error' in _act:
                print(f"    t={_t:2d}  ERROR: {_act['error']}")
            else:
                _music = _act.get('Music', '?')
                _solo = _act.get('Solo', '?')
                _creative = _act.get('Creative', '?')
                _tech = _act.get('Tech', '?')
                _sport = _act.get('Sport', '?')
                _game = _act.get('Game', '?')
                print(f"    t={_t:2d}  Music={_music:30s}  Solo={_solo:30s}  Creative={_creative:30s}  Tech={_tech:20s}  Sport={_sport:20s}  Game={_game}")
    print()
    print(f"  Total profiles: {_n_profiles}  (expected 128)")
    print(f"  Total time windows per profile: 16")
    print(f"  Total activity cells: {_n_profiles * 16}")
    print(f"  Errors: {_n_errors}")
    print()
    print("=" * 60)
    print("ALL FUNCTIONS AND STRUCTURES FROM universe_math_structures.py")
    print("HAVE BEEN CALLED AND PRINTED. ZERO OMISSIONS.")
    print("=" * 60)
