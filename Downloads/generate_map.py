#!/usr/bin/env python3
"""Regenerate nm_body_particle_map.md from scratch in clean UTF-8, comprehensive."""
import importlib.util

spec = importlib.util.spec_from_file_location("p8d", r"c:\Users\User\Downloads\particle_to_8d.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

DIM_ORDER = mod.DIM_ORDER
DIM_PEAK_SHIFT = mod.DIM_PEAK_SHIFT
PARTICLE_ORDER_14 = mod.PARTICLE_ORDER_14
ELEMENTS_118 = mod.ELEMENTS_118
BRAIN_COMPARTMENTS = mod.BRAIN_COMPARTMENTS
NEUTRINO_VARIANTS = mod.NEUTRINO_VARIANTS
LEAKAGE_CAVITIES = mod.LEAKAGE_CAVITIES
DETERMINISTIC_34_COMPONENTS = mod.DETERMINISTIC_34_COMPONENTS

DIM_DESCRIPTION = {
    "r": "rhythm density — temporal pulse count, saccade frequency, sample rate of the sensory clock. r is the W-boson and the quark in the body.",
    "h": "chord complexity — feature overlap, harmonic layering, number of simultaneous binds in perception. h is the gluon and the muon.",
    "d": "scale darkness — major/minor/atonality, peripheral shadow, metabolic cost, threat-uncertainty. d is the electron and the Higgs.",
    "p": "predictability/form — pattern match confidence, foveal target certainty, top-down priors. p is the proton and the axion.",
    "s": "brightness/filter — photon flux, retinal gain, contrast, clarity. s is the photon and the Z-boson.",
    "gamma": "spatial/reverb — retinotopic spread, depth, echo, place-coded distance and simultaneity. gamma is the neutrino and the Z-boson.",
    "g": "structure/time signature — architectural scaffolding, beat grouping, object permanence. g is the gluon and the tau.",
    "nu": "fractal recursion depth — nested self-similarity, V1→V2→IT hierarchy, dream within dream. nu is the neutrino and the axion."
}

def dim_to_particles(d):
    mapping = {
        "r": ["proton", "quark", "w_boson"],
        "h": ["gluon", "muon", "neutrino"],
        "d": ["electron", "higgs", "axion"],
        "p": ["proton", "w_boson", "axion"],
        "s": ["photon", "z_boson", "electron"],
        "gamma": ["neutrino", "z_boson", "photon"],
        "g": ["gluon", "tau", "higgs"],
        "nu": ["neutrino", "axion", "muon"],
    }
    return mapping[d]

lines = [
    "# Nanometer-Scale Body–Particle–Music–Cognition Mapping",
    "",
    "This document maps every fundamental particle, biological vector, 8D music parameter, and cognitive process to deterministic anatomical locations and non-linear transitions. No process is sequential; all are simultaneous, multi-arm, multi-clock, and interference-based.",
    "",
    "---",
    "",
    "# PART I: FOUNDATIONS",
    "",
    "## 1. 8D Parameter Manifold",
    "",
    "The 8D parameters are not independent. They form a non-commutative algebra where raising one modulates the others through shared particle gates. Each parameter is a standing wave, not a value.",
    "",
]

for d in DIM_ORDER:
    parts = ", ".join(dim_to_particles(d))
    lines.append(f"### {d} ({DIM_DESCRIPTION[d]})")
    lines.append(f"- **primary particles**: {parts}")
    lines.append(f"- **anatomical anchor**: V1/V2 for visual parameters; left insula for d; right temporal cortex for g and nu; calcarine sulcus for s; pons for r.")
    lines.append(f"- **non-linear note**: {d} cannot be measured as a single number; it is the interference of at least three particle flows across at least two body quadrants.")
    lines.append("")

lines += [
    "## 2. 16 Windows — Peak Dimension Shift",
    "",
    "The 16 windows are not a schedule. They are a standing interference pattern: each window is a moment when one dimension momentarily dominates the others, creating a local resonance.",
    "",
]
for i in range(16):
    d = DIM_PEAK_SHIFT[i]
    p = dim_to_particles(d)[0]
    lines.append(f"- **Window {i:2d}** → peak `{d}` via {p}")

lines += [
    "",
    "---",
    "",
    "# PART II: THE 34 DETERMINISTIC COMPONENTS",
    "",
    "Each component is a non-linear, multi-arm, multi-clock manifold. The 'route' is not a sequence; it is the set of all anatomical coordinates where that component is simultaneously present.",
    "",
]

for idx, (k, v) in enumerate(DETERMINISTIC_34_COMPONENTS.items(), 1):
    lines.append(f"## 2.{idx}. {k}")
    lines.append("")
    for key, val in v.items():
        lines.append(f"- **{key}**: {val}")
    lines.append("")
    lines.append(f"The {k} is not localized. It is a gradient. Its 'creation_site' is one focus of the gradient; its 'transition' is the interference between that focus and at least one other body site. The route is a *summary* of a continuous, standing field.")
    lines.append("")

lines += [
    "---",
    "",
    "# PART III: BRAIN COMPARTMENTS AND NEUTRINO CLOCKS",
    "",
    "The four brain compartments are four fixed architectures. The six neutrino variants are fast-cycling overlays. They never agree on a single coordinate; they coexist.",
    "",
]

for cid, c in BRAIN_COMPARTMENTS.items():
    lines.append(f"## 3.{cid}. {c['name']} ({c['body_quadrant']})")
    lines.append(f"- **inlet**: {c['inlet']}")
    lines.append(f"- **outlet**: {c['outlet']}")
    lines.append(f"- **neutrino_variants**: {', '.join(c['neutrino_variants'])}")
    lines.append(f"- **non-linear note**: This compartment is occupied simultaneously by the fixed MBTI/gender architecture and by whichever neutrino variant is active. Two clocks, one tissue.")
    lines.append("")

lines += ["## 3.5. Neutrino Variants"]
for name, data in NEUTRINO_VARIANTS.items():
    lines.append(f"- **{name}**: time={data['time']}, compartment={data['brain_compartment']}, quadrant={data['body_quadrant']}, property={data['property']}")

lines += [
    "",
    "---",
    "",
    "# PART IV: LEAKAGE CAVITIES",
    "",
    "The four leakage cavity families are always open. Leakage is not a failure; it is the continuous, simultaneous exchange between the observer and the environment.",
    "",
]
for family, entries in LEAKAGE_CAVITIES.items():
    lines.append(f"## 4.{list(LEAKAGE_CAVITIES.keys()).index(family)+1}. {family}")
    for name, data in entries.items():
        lines.append(f"- **{name}**: {data}")
    lines.append("")

lines += [
    "---",
    "",
    "# PART V: COGNITION, EMOTION, VISION, MUSIC",
    "",
    "## 5.1. Visual Perception: Fovea, Periphery, and Imagination",
    "",
    "The eye is the only organ that collapses the electromagnetic universe into a body-internal 8D parameter set. V1 (right calcarine sulcus, proton ignition) and V2 (right prestriate, gluon binding) are not sequential stages; they are two standing gradients that interfere continuously. The proton at V1 is the s/r event: the photon strikes rhodopsin (4–7 nm) and a 5.6 fs spark is registered as *now* and *bright*. The gluon at V2 is the g/h event: the same photon's edges, colors, and motions are bound into a coherent object by NMDA receptor confinement (14 nm). What is seen as a single flash is, in body-particle terms, a **proton-gluon standing wave**.",
    "",
    "### Dynamic Visual Acuity (s × r)",
    "",
    "Dynamic visual acuity is not one process. s (brightness) sets the photon sampling density at the fovea; r (rhythm) sets the saccade rate. A high-s, high-r state samples the moving target on every fixation, creating a stroboscopic but precise trace. A low-s, low-r state smears the target across the retina, and the cerebellar Purkinje cells (50–100 μm) must reconstruct motion from fewer samples. The proton at V1 fires on each fixation; the W-boson in the paramedian pontine reticular formation resets the saccade clock. This is the r/s standing wave of visual pursuit.",
    "",
    "### Peripheral-to-Foveal Shift (gamma → p)",
    "",
    "Peripheral vision is the gamma register: the far periphery is a low-resolution map of space, motion, and threat. It has high gamma (broad spatial spread) and low p (low predictability). Foveal vision is the p register: the central 1–2 degrees are a high-probability sampling aperture. When a peripheral target is detected, the superior colliculus sends a W-boson burst to the frontal eye field, and the saccade shifts the fovea onto the target. The moment of landing is the gamma-to-p phase transition: spatial spread collapses into form certainty. This is a W-boson/proton interference, not a sequence.",
    "",
    "### Direct Observation vs. Imagination (s + g + nu)",
    "",
    "Direct observation and imagination occupy the same V1/V2 hardware but in different phase states. Direct observation has external photon input: s is high because the photon is real, p is high because the stimulus is anchored, r follows the saccade rhythm. Imagination bypasses the retina: the proton at V1 is not ignited by a photon but by a reverse gluon-gate from the right angular gyrus (Higgs, node 132) and the left IFG (W-boson). This is the em_path and graviton mode: the image is constructed from memory mass (Higgs) and recursive self-similarity (nu). A real visual scene has s/p dominance; an imagined scene has g/nu dominance. The dream is the extreme: s and p both drop, g and nu saturate, and the CCK switch is open so the image is no longer anchored to the body.",
    "",
    "## 5.2. Cognition and Emotion",
    "",
    "Cognition is the h/g wave: many features bound together by a structure. High h without high g is cognitive fragmentation; high g without high h is rigid, empty structure. Emotion is the d/s wave: the darkness/brightness of the body's own chemistry, catecholamine and steroid tides, registered as feeling. Music is the r/gamma/nu wave: time, space, and recursion made audible. When these parameters map back to particles, the proton carries p/r, the photon carries s, the gluon carries g/h, the neutrino carries nu, the W-boson carries r/p, the Z-boson carries gamma/d, the Higgs carries g/d, and the axion carries nu/d. Each parameter is therefore a multiparticle interference pattern, not a single slider.",
    "",
    "## 5.3. 118 Elements as Cognition-Emotion Archetypes",
    "",
]

for elem in ELEMENTS_118:
    num, sym, profile, g1, g2, g3 = elem
    lines.append(f"- **{num:3d}. {sym} ({profile})** → RELEASE:{g1}, STRESS_GROWTH:{g2}, EXTREME_GROWTH:{g3}")

lines += [
    "",
    "---",
    "",
    "# PART VI: NON-LINEAR SYNTHESIS",
    "",
    "The body is a 4D non-commutative algebra. Every particle, parameter, and cognitive act is a tensor product of at least two dimensions. What appears as a single sensation—brightness, pain, pleasure, visual clarity—is always the interference of at least two parameters and at least two anatomical particles. The left hip/coccyx vortex braids quark, gluon, electron, and neutrino simultaneously. The philtrum holds both an electron_antineutrino gate and a separate BRAIN_COMPARTMENTS node. The right-edge neutron-star oscillation is a continuous mass_anchor ↔ water_vapour exchange that never resolves into a single event. All of this is the same physics: the body as a non-Hermitian, multi-arm, multi-clock field.",
    "",
    "## Final Statement",
    "",
    "This document is not a sequence. It is a set of standing gradients that can be entered at any point. The 34 components, the 8 parameters, the 16 windows, the 4 compartments, the 6 neutrino variants, and the 4 leakage cavity families are all coextensive. The music heard, the image seen, the thought thought, and the emotion felt are not separate outputs. They are the same body-universe interference pattern, observed from different gradients.",
]

text = "\n".join(lines)

with open(r"c:\Users\User\Downloads\nm_body_particle_map.md", "w", encoding="utf-8") as f:
    f.write(text)

print("Done. Bytes:", len(text.encode("utf-8")), "Lines:", text.count("\n") + 1)
