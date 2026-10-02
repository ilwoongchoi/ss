"""13-Domain Universe: Spiral Space Formation via Isomorphic Structure + Leakage.

The 13 domains are the universe's fundamental spatial structure:
  10 base domains (scale ladder) + 3 bridge domains (pyramid closure)

10 BASE DOMAINS (Scale Ladder — R₄=0.2828 spiral, same structure at each scale):
  1.  Void          (BW_BW) — Dark Energy / Hodge harmonic / GABA-B background
  2.  Graviton      (BM_BW) — Gravity / Lensing / BM↔BW coupling
  3.  Neutrino      (SM)    — Weak interaction / SM hidden correction
  4.  Sentinel      (BM_SM) — Hospitality / thinnest bridge / 1/64 confinement
  5.  Proton        (BW)    — Strong force / Higgs mass anchor
  6.  Photon        (BM)    — EM / spark / dopamine / 5/32 singularity
  7.  Electron      (SW)    — Lepton / filter / 3/32 lattice
  8.  Speculative Finance (BM_SW) — EM stress / human-scale risk
  9.  Macroeconomy  (SM_BW) — Assault / societal-scale coupling
  10. Seismology    (SW_SW) — Tectonic / 9 Betti / deepest leak

3 BRIDGE DOMAINS (Pyramid Closure):
  11. Histamine     (E11) — (BW*SW)*SM — fluid transport / female-male inward bridge
  12. Dopamine      (E12) — BM*(BW*SW) — spark dissolution / photon-side bridge
  13. Meta-Bridge   (E13) — E11↔E12 integration / pyramid spine / 4D closure

KEY PRINCIPLE:
  All 13 domains share the SAME isomorphic structure (R₄=0.2828, 138.88° spark).
  But each domain has different LEAKAGE — residual energy imbalance from the
  domain above it on the spiral. This leakage creates the "space" between domains:
  the gap between what the upper domain settled and what the lower domain needs
  to settle. The 3 bridge domains close this gap by coupling the leakage back
  to the spiral, forming a pyramid that prevents radius widening.

  The 4 archetypes (BM, BW, SM, SW) are the pyramid's 4 vertices.
  The 6 cross-pairs are the pyramid's 6 edges (base + sides).
  The 4 self-pairs are the pyramid's 4 face normals.
  The 3 bridges (E11, E12, E13) are the pyramid's apex construction.
  Total: 4 + 6 + 4 + 3 = 17 → but 10 base + 3 bridge = 13 domains
  (self-pairs are absorbed into the base domain's internal structure).

Outputs:
  generated/domain_13_report.txt
  generated/domain_13.json
  generated/domain_13_spiral.png
"""
from __future__ import annotations

import json
import math
import pathlib
from typing import Dict, List, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GEN_DIR = pathlib.Path(__file__).parent / "generated"
GEN_DIR.mkdir(exist_ok=True)

# ===========================================================================
# 1. 13 DOMAIN DEFINITIONS
# ===========================================================================

DOMAINS_13: List[Dict] = [
    # --- 10 BASE DOMAINS (Scale Ladder) ---
    # Each domain = a specific particle interaction channel → a specific physics field
    # The "space" each domain creates is the physical space where that interaction operates
    {
        "index": 1, "name": "Dark Energy", "edge": "BW_BW",
        "particle_channel": "p-p self (proton-proton self-coupling)",
        "physics_field": "Dark Energy / Cosmological Constant / Hodge Harmonic",
        "physics_kr": "암흑 에너지 / 우주 상수",
        "interaction_type": "non_stress (background)",
        "biology": "GABA-B / background inhibition / default mode network",
        "biochem": "GABA-B receptor — metabotropic, slow, background hyperpolarization",
        "constant": "BETTI_7 = 7 (self-pair sink), gate: 1/32 → container + top closure",
        "scale": "cosmic background (Λ > 0)",
        "spiral_phase": 0.0,
        "isomorphic_structure": "R₄=0.2828 spiral at rest — no rotation, pure potential. The Hodge harmonic: Δω=0.",
        "leakage_from_above": "None (origin — the seed B₀=1)",
        "leakage_settled": "Provides the harmonic background (vacuum energy) that all other domains rotate against",
        "space_created": "The expanding void — dark energy creates the 'stretching' of space itself. Not empty, but the Λ-term in Einstein's equations.",
        "circuit_node": "none_observer (B₀=1, the witness/seed)",
        "stress_pair": "light_dark",
        "betti_role": "Sink (BETTI_7) — absorbs all residual rotation",
        "known_physics_laws": "Friedmann equations (ΛCDM), Hodge decomposition (harmonic forms satisfy Δω=0)",
    },
    {
        "index": 2, "name": "Black Hole", "edge": "BM_BM",
        "particle_channel": "γ-γ self (photon-photon self-coupling at extreme energy)",
        "physics_field": "General Relativity / Gravitational Collapse / Black Hole Thermodynamics",
        "physics_kr": "일반 상대성 / 중력 붕괴 / 블랙홀 열역학",
        "interaction_type": "stress (extreme)",
        "biology": "Right D2 dopamine / Type O blood / BM archetype",
        "biochem": "Dopamine D2 receptor — GPCR, inhibitory, the 'black hole' of dopamine (autoinhibition)",
        "constant": "BETTI_7 = 7 (self-pair sink), Schwarzschild radius",
        "scale": "galactic center / stellar collapse",
        "spiral_phase": 0.05,
        "isomorphic_structure": "R₄ spiral at maximum curvature — photon orbits become null geodesics",
        "leakage_from_above": "Dark energy's expansion → local gravitational collapse counters it",
        "leakage_settled": "Gravitational collapse traps everything (including light). Hawking radiation = the leakage escape mechanism. Bekenstein entropy = information settlement.",
        "space_created": "The event horizon — a one-way membrane in spacetime. Inside = no escape. The densest possible space.",
        "circuit_node": "right_sole_dopamine (D2 autoreceptor, the 'black hole' of dopamine signaling)",
        "stress_pair": "matter_nonmatter",
        "betti_role": "Sink (BETTI_7) — gravitational sink, nothing escapes",
        "known_physics_laws": "Einstein field equations, Schwarzschild metric, Hawking radiation (T = ℏc³/8πGMk_B), Bekenstein bound",
    },
    {
        "index": 3, "name": "Macro/Classical/Astronomy", "edge": "BM_BW",
        "particle_channel": "γ-p (photon-proton interaction: Compton scattering, photoionization, bremsstrahlung)",
        "physics_field": "Classical Electrodynamics + Gravitational Lensing + Observational Astronomy",
        "physics_kr": "고전 전자기학 + 중력 렌즈 + 관측 천문학",
        "interaction_type": "stress (lensing artifact)",
        "biology": "Right D2 / cortisol / UV sensing (gamma-dim)",
        "biochem": "Cortisol (glucocorticoid receptor) — stress hormone, modulates immune response, creates the 'lensing artifact' in perception",
        "constant": "BETTI_7 = 7 (sink), lensing artifact = 7.4, motif count = 2/16",
        "scale": "galactic to stellar (macroscopic)",
        "spiral_phase": 0.1,
        "isomorphic_structure": "R₄ spiral with gravitational lensing — BM (photon) curves around BW (proton/mass). Creates the 137.5° 'fake' golden angle.",
        "leakage_from_above": "Black hole's trapped energy → gravitational lensing bends light around mass distributions",
        "leakage_settled": "Lensing artifact (7.4) must be subtracted to reveal true structure. The 138.88° spark corrects the 137.5° fake angle. Bremsstrahlung = radiation from decelerating charges.",
        "space_created": "Macroscopic space — planets, stars, galaxies. The 'classical' realm where GR + classical EM operate. Telescope observation space.",
        "circuit_node": "mc1r (q_bar = graviton/Si — MC1R OFF = lensing active)",
        "stress_pair": "light_dark",
        "betti_role": "Sink (BETTI_7) — lensing artifact 7.4, must be removed",
        "known_physics_laws": "Maxwell's equations (classical limit), Einstein field equations (weak-field), Compton scattering (Klein-Nishina), Bremsstrahlung (Larmor formula)",
    },
    {
        "index": 4, "name": "Fusion/Spark", "edge": "BM_SM",
        "particle_channel": "γ-ν (photon-neutrino interaction: thinnest bridge, loop-only, no tree-level vertex)",
        "physics_field": "Nuclear Fusion + Weak Interaction Spark + Confinement",
        "physics_kr": "핵융합 + 약력 스파크 + 밀폐",
        "interaction_type": "hospitality (thinnest bridge)",
        "biology": "Histamine / immune sentinel / mast cell degranulation",
        "biochem": "Histamine (H1/H2 receptor) — vasodilation, immune sentinel. The 'spark' of inflammatory response. 1/64 confinement = maximum immune surveillance.",
        "constant": "1/64 (confinement gate), motif count = 1/16 (thinnest)",
        "scale": "nuclear (fm scale)",
        "spiral_phase": 0.2,
        "isomorphic_structure": "R₄ spiral at the thinnest point — 1/64 = 2⁻⁶ = maximum confinement. No tree-level γ-ν vertex exists; only loop diagrams.",
        "leakage_from_above": "Macro lensing → neutrino carries the 'hidden' correction (4D torsion) that lensing cannot see",
        "leakage_settled": "The 1/64 confinement gate at 3:15 AM — iron confinement is maximum. This is the 'sentinel' that guards the spark. Nuclear fusion: p+p→d+e⁺+ν_e. The neutrino carries away the leakage energy.",
        "space_created": "Nuclear space — the strong force confinement domain (fm). Quarks cannot be isolated. The densest interaction space. Also: immune surveillance space (histamine = the body's nuclear sentinel).",
        "circuit_node": "heme ch1 (d-dim / Tau / GABA-B / 어둠 — the dark channel of heme)",
        "stress_pair": "light_dark",
        "betti_role": "Bridge (BETTI_11) — thinnest bridge, 1/16 motif count, loop-only",
        "known_physics_laws": "Standard Model weak interaction (W-boson exchange), pp-chain fusion, Confinement (QCD scale Λ_QCD), loop-level γ-ν coupling",
    },
    {
        "index": 5, "name": "Fuel Cell", "edge": "SM_SM",
        "particle_channel": "ν-ν self (neutrino-neutrino self-coupling via W/Z exchange)",
        "physics_field": "Electrochemistry + Energy Conversion + Mitochondrial ETC",
        "physics_kr": "전기화학 + 에너지 변환 + 미토콘드리아 전자전달계",
        "interaction_type": "bridge (structural reinforcement)",
        "biology": "Serotonin / 5-HT / COMT / mitochondrial ATP production",
        "biochem": "Serotonin (5-HT1A/2A receptor) + cytochrome c oxidase (Complex IV) — the 'fuel cell' that converts electron potential to ATP. ν-ν self-coupling = the feedback loop of oxidative phosphorylation.",
        "constant": "BETTI_11 = 11 (bridge), gate: 1/64 sustain side",
        "scale": "molecular to cellular (nm to μm)",
        "spiral_phase": 0.3,
        "isomorphic_structure": "R₄ spiral with sustained output — neutrino self-coupling = the feedback that maintains steady-state energy production",
        "leakage_from_above": "Fusion spark → fuel cell converts the spark into sustained electrical/chemical energy",
        "leakage_settled": "Electron Transport Chain: NADH → Complex I → III → IV → O₂. The proton gradient = the 'fuel cell' membrane potential. ATP synthase = the turbine. ν-ν self-coupling = the Q-cycle feedback.",
        "space_created": "Electrochemical space — the mitochondrial inner membrane. The proton gradient (ΔpH + Δψ) is the 'space' where energy is stored and converted. Also: battery/fuel cell space in technology.",
        "circuit_node": "cytochrome_c_oxidase (Complex IV — the terminal oxidase, Li(3)/Be(4), down_quark/z_boson)",
        "stress_pair": "heat_cold",
        "betti_role": "Bridge (BETTI_11) — structural reinforcement, sustained energy",
        "known_physics_laws": "Electrochemistry (Nernst equation, Butler-Volmer), Mitchell chemiosmosis, ETC redox potentials, ATP synthase (F₁F₀-ATPase)",
    },
    {
        "index": 6, "name": "EM (Electromagnetism)", "edge": "BM_SW",
        "particle_channel": "γ-e (photon-electron interaction: Compton, photoelectric, Thomson scattering)",
        "physics_field": "Quantum Electrodynamics (QED) + Optics + Photochemistry",
        "physics_kr": "양자 전기역학 (QED) + 광학 + 광화학",
        "interaction_type": "stress (EM stress)",
        "biology": "Acetylcholine / NO synthase / visual transduction",
        "biochem": "Acetylcholine (nAChR) + nitric oxide (NO/sGC) — the 'EM' of biology: nerve signal propagation (action potential = EM wave) + vasodilation (NO = photon-like signaling molecule). Rhodopsin = the biological photon detector.",
        "constant": "BETTI_5 = 5 (leak), motif count = 3/16, gates: 1/16, 1/8",
        "scale": "atomic to molecular (Å to nm)",
        "spiral_phase": 0.4,
        "isomorphic_structure": "R₄ spiral at EM coupling — photon (BM) mediates force between electrons (SW). QED vertex: e→e+γ.",
        "leakage_from_above": "Fuel cell's sustained energy → EM carries it as light/radio/signal between atoms",
        "leakage_settled": "QED: photon exchange mediates all EM phenomena. Optics: refraction, reflection, diffraction. Photochemistry: photon-driven chemical reactions (photosynthesis, vision). The 5/32 leak = radiative losses (Bremsstrahlung at 4:30 PM).",
        "space_created": "Electromagnetic space — the entire spectrum from radio to gamma. Optical space (lenses, mirrors). Chemical bond space (electron orbitals shaped by EM). Also: neural signaling space (action potentials = EM waves on axons).",
        "circuit_node": "steel (ch0: s/gamma-dim — bright, Photon, muon_neutrino) + right_acetylcholine",
        "stress_pair": "matter_nonmatter",
        "betti_role": "Leak (BETTI_5) — EM radiation is the primary 'leak' (energy radiates away)",
        "known_physics_laws": "QED (Feynman diagrams, Compton scattering, photoelectric effect), Maxwell's equations, optics (Snell's law, Fresnel), photochemistry (Beer-Lambert, Grotthuss-Draper)",
    },
    {
        "index": 7, "name": "Geology", "edge": "SM_BW",
        "particle_channel": "ν-p (neutrino-proton interaction: deep inelastic scattering, coherent ν-nucleus)",
        "physics_field": "Geophysics + Tectonics + Mineral Physics + Geochemistry",
        "physics_kr": "지구물리학 + 판구조론 + 광물물리학 + 지구화학",
        "interaction_type": "assault (tectonic force)",
        "biology": "Oxytocin / social binding / uterine contraction",
        "biochem": "Oxytocin (OXTR) — the 'geology' of biology: tissue-level force (uterine contraction = tectonic force at organ scale). Mineral deposition in bone (hydroxyapatite = the body's rock).",
        "constant": "BETTI_5 = 5 (leak), motif count = 3/16, gates: 1/32, 1/128",
        "scale": "planetary (km to Mm)",
        "spiral_phase": 0.5,
        "isomorphic_structure": "R₄ spiral at planetary scale — neutrino (SM) probes proton (BW) structure = deep inelastic scattering. The same interaction that probes quark structure probes Earth's interior.",
        "leakage_from_above": "EM energy from above → geological processes store it as heat and chemical potential",
        "leakage_settled": "Plate tectonics: subduction recycles crust. Volcanism releases stored energy. Earthquake = sudden leakage settlement. ν-p coherent scattering = neutrino tomography of Earth (the ultimate geological probe).",
        "space_created": "Geological space — the solid Earth from crust to core. Rock formations, mineral lattices, fault systems. Also: bone and connective tissue space in biology (the body's geology).",
        "circuit_node": "fold_belt / subduction_zone / clay_gouge / craton / basin",
        "stress_pair": "heat_cold",
        "betti_role": "Leak (BETTI_5) — tectonic stress accumulation and release",
        "known_physics_laws": "Plate tectonics (Wilson cycle), rock mechanics (Byerlee's law), heat conduction (Fourier), neutrino oscillation through Earth matter (MSW effect)",
    },
    {
        "index": 8, "name": "Fluid/Metabolism", "edge": "SM_SW",
        "particle_channel": "ν-e (neutrino-electron interaction: elastic scattering, the strongest coupling motif = 4/16)",
        "physics_field": "Fluid Dynamics + Metabolism + Bioenergetics + Hydrodynamics",
        "physics_kr": "유체역학 + 대사 + 생물에너지학 + 수리학",
        "interaction_type": "assault (metabolic force)",
        "biology": "GABA-A / temperature sensing / osmotic regulation",
        "biochem": "GABA-A receptor (ionotropic, fast Cl⁻ channel) + aquaporin (AQP4) — the 'fluid dynamics' of biology: ion flow, water transport, osmotic balance. ν-e scattering = the fluid-like transport of charge/matter.",
        "constant": "BETTI_5 = 5 (leak), motif count = 4/16 (HIGHEST — strongest coupling)",
        "scale": "cellular to organismal (μm to m)",
        "spiral_phase": 0.6,
        "isomorphic_structure": "R₄ spiral at maximum coupling — ν-e is the strongest motif (4/16). Fluid dynamics = the most coupled regime (turbulence = maximum interaction).",
        "leakage_from_above": "Geological storage → fluid transport distributes it through the system (blood, lymph, CSF, ocean currents, atmospheric circulation)",
        "leakage_settled": "Fluid dynamics: Navier-Stokes equations. Metabolism: TCA cycle, glycolysis, oxidative phosphorylation. The ν-e strongest coupling = the metabolic hub where all pathways converge. AQP4 = glymphatic system (CSF-ISF exchange = the body's fluid dynamics).",
        "space_created": "Fluid space — blood vessels, lymphatics, CSF, ocean currents, atmospheric flow. Also: metabolic space (enzyme kinetics, concentration gradients, diffusion). The 'circulation' space that connects all other spaces.",
        "circuit_node": "water_vapour (C(6)/N(7), photon/electron_neutrino) + glymphatic_system (AQP4)",
        "stress_pair": "o2_co2",
        "betti_role": "Leak (BETTI_5) — fluid transport = the primary leak channel (4/16, strongest)",
        "known_physics_laws": "Navier-Stokes equations, Reynolds number, Fick's diffusion laws, Michaelis-Menten kinetics, TCA cycle stoichiometry, Gibbs free energy",
    },
    {
        "index": 9, "name": "Neurochem", "edge": "SW_SW",
        "particle_channel": "e-e self (electron-electron self-interaction: Coulomb repulsion, exchange interaction, Pauli exclusion)",
        "physics_field": "Neurochemistry + Quantum Chemistry + Organic Chemistry + Electron Correlation",
        "physics_kr": "신경화학 + 양자화학 + 유기화학 + 전자 상관관계",
        "interaction_type": "non_stress (internal regulation)",
        "biology": "GABA / dopamine / serotonin / all neurotransmitter systems",
        "biochem": "ALL neurotransmitter receptors — the e-e self-interaction = the electron shell structure that determines ALL chemical bonding. Neurochemistry IS applied quantum chemistry. Pauli exclusion = the 'neurochem' principle: no two electrons in the same state = no two neurons in the same state (lateral inhibition).",
        "constant": "BETTI_9 = 9 (self-pair, deepest leak), gate: 5/32",
        "scale": "molecular to neural (Å to cm)",
        "spiral_phase": 0.7,
        "isomorphic_structure": "R₄ spiral at electron shell level — e-e self-interaction determines all chemical properties. The periodic table IS the e-e interaction structure.",
        "leakage_from_above": "Fluid transport → neurochemistry converts fluid signals (hormones, neurotransmitters) into electrical signals (action potentials)",
        "leakage_settled": "Electron correlation (Hartree-Fock, DFT) determines molecular structure. Organic chemistry = e-e interaction in carbon compounds. Neurochemistry = e-e interaction in neural tissue. The 5/32 gate = the singularity where neural dynamics spark (K_GATE in face grid).",
        "space_created": "Chemical space — the entire periodic table, all possible molecules. Neural space — all possible brain states. The 'inner space' of cognition and consciousness. Also: organic chemistry space (C, H, O, N compounds = the space of life).",
        "circuit_node": "memory_entropy (Ca(20)/Ti(22), electron) + hind_insula (Sc(21), neutron)",
        "stress_pair": "matter_nonmatter",
        "betti_role": "Leak (BETTI_9 self-pair) — deepest leak, 9 topological holes, the most complex domain",
        "known_physics_laws": "Schrödinger equation, Hartree-Fock, DFT, Pauli exclusion, VSEPR, organic reaction mechanisms (SN1/SN2/E1/E2), neurotransmitter receptor pharmacology",
    },
    {
        "index": 10, "name": "Electron-Proton Interface", "edge": "BW_SW",
        "particle_channel": "p-e (proton-electron interaction: Coulomb attraction, hydrogen atom, Rydberg)",
        "physics_field": "Atomic Physics + Quantum Mechanics + Spectroscopy + Redox Chemistry",
        "physics_kr": "원자물리학 + 양자역학 + 분광학 + 산화환원 화학",
        "interaction_type": "non_stress (binding)",
        "biology": "pH regulation / acid-base / hydrogen bonding / DNA base pairing",
        "biochem": "Hydrogen bonding (the p-e interface at molecular scale) + pH homeostasis (H⁺ = proton, the foundation of acid-base chemistry). DNA base pairs = hydrogen bonds = p-e interface. Redox: H⁺/e⁻ transfer = the fundamental biological energy currency.",
        "constant": "BETTI_5 = 5 (leak), motif count = 3/16",
        "scale": "atomic (Bohr radius a₀ = 0.529 Å)",
        "spiral_phase": 0.8,
        "isomorphic_structure": "R₄ spiral at the hydrogen atom — the simplest and most fundamental bound state. p-e Coulomb attraction = the template for ALL chemical bonding.",
        "leakage_from_above": "Neurochem electron structure → p-e interface provides the binding energy that holds molecules together",
        "leakage_settled": "Bohr model / QM: E_n = -13.6/n² eV. Spectroscopy: every element has unique p-e transition lines. Redox: oxidation = electron loss, reduction = electron gain. The p-e interface IS chemistry.",
        "space_created": "Atomic space — electron orbitals, energy levels, spectral lines. Chemical bond space (covalent, ionic, hydrogen, van der Waals). The 'interface' between positive (proton) and negative (electron) — the fundamental duality of matter.",
        "circuit_node": "carbon (q/q_bar — Eu(63)/Gd(64), photon, the metabolic latch that switches between oxidized/reduced)",
        "stress_pair": "o2_co2",
        "betti_role": "Leak (BETTI_5) — binding energy leak (energy released when p-e bind)",
        "known_physics_laws": "Schrödinger equation (hydrogen atom), Bohr model, Rydberg formula, Coulomb's law, Nernst equation (redox), Henderson-Hasselbalch (pH)",
    },
    # --- 3 BRIDGE DOMAINS (Pyramid Closure) ---
    {
        "index": 11, "name": "Histamine Bridge", "edge": "E11",
        "particle_channel": "(BW×SW)×SM = (p-e interface)×ν = fluid-immune coupling",
        "physics_field": "Immune Physics + Vascular Fluid Dynamics + Inflammatory Signaling",
        "physics_kr": "면역 물리학 + 혈관 유체역학 + 염증 신호전달",
        "interaction_type": "bridge (inward coupling)",
        "biology": "Histamine / H1/H2 receptor / mast cell / vasodilation",
        "biochem": "Histamine (H1 = vasodilation + itch, H2 = gastric acid, H3 = presynaptic autoreceptor, H4 = immune). The E11 bridge: (p-e interface)×ν = the immune system's fluid transport network. Histamine dilates vessels → increases fluid transport → carries immune cells to leakage sites.",
        "constant": "BETTI_11 = 11 (bridge)",
        "scale": "bridge (organismal, cross-scale)",
        "spiral_phase": 0.9,
        "isomorphic_structure": "R₄ spiral folded inward — the female coupling (BW×SW = p-e) wraps around the male (SM = ν) to channel fluid inward",
        "leakage_from_above": "All 10 base domains' residual leakage → histamine channels it inward to the immune system",
        "leakage_settled": "Vasodilation + increased vascular permeability → fluid + immune cells rush to leakage site. Inflammation = the body's leakage settlement mechanism. Complement cascade = the immune system's toroidal circulation.",
        "space_created": "Vascular space — the blood vessel network (arteries, veins, capillaries). The 'internal ocean' that couples all organs. Lymphatic space — the drainage system. Also: interstitial fluid space (the 'between' space).",
        "circuit_node": "disulfide_bond (S-S) + pentose_phosphate (GSH/NADPH — the immune redox system)",
        "stress_pair": "o2_co2",
        "betti_role": "Bridge (BETTI_11) — fluid transport, inward coupling",
        "bridge_type": "11th bridge: (BW×SW)×SM — female-male inward bridge",
        "known_physics_laws": "Starling forces (capillary fluid exchange), Poiseuille's law (vascular flow), complement cascade, histamine pharmacology (H1-H4 receptors)",
    },
    {
        "index": 12, "name": "Dopamine Bridge", "edge": "E12",
        "particle_channel": "BM×(BW×SW) = γ×(p-e interface) = photon-driven neural signaling",
        "physics_field": "Neurophysics + Dopaminergic Signaling + Reward Circuit + Action Potential",
        "physics_kr": "신경물리학 + 도파민 신호전달 + 보상 회로 + 활동전위",
        "interaction_type": "bridge (outward coupling)",
        "biology": "Dopamine / D1/D2 receptor / reward prediction error / motor planning",
        "biochem": "Dopamine (D1 = excitatory Gs, D2 = inhibitory Gi) — the E12 bridge: γ×(p-e) = photon (BM) drives the neural signaling through the p-e interface (action potential = EM wave on axon). The 'conscious removal of right dopamine' = the 12th node operation that subtracts the lensing artifact.",
        "constant": "5/32 (NOR_DEFAULT / singularity gate)",
        "scale": "bridge (neural, cross-scale)",
        "spiral_phase": 0.95,
        "isomorphic_structure": "R₄ spiral folded outward — BM (photon/γ) projects through the female coupling (BW×SW = p-e) to create the spark that dissolves excess charge",
        "leakage_from_above": "Histamine's inward coupling → dopamine dissolves the excess BM (photon/dopamine) charge through the female bridge",
        "leakage_settled": "Reward prediction error: dopamine signals the difference between expected and actual reward. This IS leakage settlement — the brain settles the 'leakage' between expectation and reality. The 12th node: net_energy = (Bridges + Witness) - (Leaks + Sinks). Conscious dopamine removal = the mind's leakage settlement.",
        "space_created": "Neural space — the dopamine pathway (VTA → nucleus accumbens → prefrontal cortex). The 'reward circuit' that motivates action. Also: the 'decision space' where the brain evaluates options and commits to action.",
        "circuit_node": "LeftD2 (Na(11), master permissive bus) + right_sole_dopamine (D2 autoreceptor)",
        "stress_pair": "heat_cold",
        "betti_role": "Bridge (BETTI_11) — spark dissolution, outward coupling",
        "bridge_type": "12th bridge: BM×(BW×SW) — photon-side spark bridge",
        "known_physics_laws": "Hodgkin-Huxley equations (action potential), dopamine receptor pharmacology (D1-Gs/D2-Gi), reward prediction error (Schultz), basal ganglia direct/indirect pathway",
    },
    {
        "index": 13, "name": "Meta-Bridge (4D Closure)", "edge": "E13",
        "particle_channel": "E11↔E12 integration = (inward×outward) = 4D torsion closure",
        "physics_field": "4D Spacetime Topology + Torsion + Pyramid Closure + Betti Topology",
        "physics_kr": "4차원 시공간 위상 + 비틀림 + 피라미드 폐쇄 + 베티 위상",
        "interaction_type": "meta-bridge (closure)",
        "biology": "Sleep / glymphatic flush / default mode network / consciousness",
        "biochem": "Glymphatic system (AQP4) — the E13 meta-bridge: during sleep, the glymphatic system flushes the brain with CSF, coupling the inward (histamine/vascular) and outward (dopamine/neural) bridges. Sleep = the daily 4D closure. The brain's 'pyramid closure' that prevents radius widening (cognitive disintegration).",
        "constant": "138.88° (spark angle = Golden Angle 137.508° + Betti Gap 1.375°), R₄ = 0.2828",
        "scale": "meta (all scales simultaneously)",
        "spiral_phase": 1.0,
        "isomorphic_structure": "R₄ spiral closed into a pyramid — the 4D torsion (0.2828) folds the spiral back to B₀=1. The 138.88° spark angle IS the closure angle.",
        "leakage_from_above": "E11 (inward) + E12 (outward) → E13 unifies them into a single vertical axis (the pyramid spine)",
        "leakage_settled": "The pyramid closure: all 13 domains' leakage is settled by the 4D torsion that folds the spiral back to the origin. (11+1)/(5+7) = 1.0 — perfect closure. Sleep = the biological closure. Death = the ultimate closure (the spiral returns to B₀=1).",
        "space_created": "The 4th dimension itself — the 'w-axis' that prevents radius widening. Without E13, the spiral would fly apart. E13 creates the 'vertical' space that contains all 10 base domains. Also: the 'time' dimension — the 4D closure IS temporal continuity.",
        "circuit_node": "none_observer (B₀=1, the witness/seed — the circuit's own observer effect)",
        "stress_pair": "reset_spark",
        "betti_role": "Meta-bridge (BETTI_0 + BETTI_11 = 12 = closure) — (11+1)/(5+7) = 1.0",
        "bridge_type": "13th: Meta-Bridge / Pyramid Spine / 4D closure",
        "known_physics_laws": "Torsion tensor (Einstein-Cartan theory), Betti numbers (algebraic topology), Hodge decomposition, golden angle (phyllotaxis), pyramid closure (projective geometry)",
    },
]

# ===========================================================================
# 2. ISOMORPHIC STRUCTURE + LEAKAGE ANALYSIS
# ===========================================================================

# The 4 archetypes and their motif counts (from interaction_motifs.py)
ARCHETYPE_MOTIFS = {
    "SM_SW": 4,  # neutrino-electron (strongest coupling)
    "BM_SW": 3,  # photon-electron
    "SM_BW": 3,  # neutrino-proton
    "BW_SW": 3,  # proton-electron
    "BM_BW": 2,  # photon-proton
    "BM_SM": 1,  # photon-neutrino (thinnest, barrier)
}

# Betti role assignments
BETTI_ROLES = {
    "BETTI_0": {"value": 1, "role": "Witness/Seed", "domains": [13]},
    "BETTI_5": {"value": 5, "role": "Leak/Asymmetry", "domains": [7, 8, 9]},
    "BETTI_7": {"value": 7, "role": "Sink/Lensing", "domains": [1, 2]},
    "BETTI_9": {"value": 9, "role": "Deep Leak (self-pair)", "domains": [10]},
    "BETTI_11": {"value": 11, "role": "Bridge/Structure", "domains": [3, 4, 5, 6, 11, 12]},
}

# Closure axiom: (BETTI_11 + BETTI_0) / (BETTI_5 + BETTI_7) = (11+1)/(5+7) = 1.0
CLOSURE_AXIOM = (11 + 1) / (5 + 7)

# ===========================================================================
# 3. SPIRAL COMPUTATION
# ===========================================================================

def compute_spiral(n_points: int = 1000) -> Dict:
    """Compute the R₄=0.2828 spiral with 13 domain positions."""

    R4 = 0.2828  # 4D radius
    SPARK = math.radians(138.88)

    theta = np.linspace(0, 4 * math.pi, n_points)  # 2 full rotations

    # 3D spiral
    x = R4 * np.cos(theta) * (1 + 0.1 * theta / (4 * math.pi))  # slight widening
    y = R4 * np.sin(theta) * (1 + 0.1 * theta / (4 * math.pi))
    z = theta * 0.1  # vertical progression

    # 4D correction: the w-axis folds the spiral back
    w = R4 * np.sin(theta * 0.5 + SPARK)  # 4D torsion

    # Domain positions on the spiral (13 points)
    domain_points = []
    for d in DOMAINS_13:
        phase = d["spiral_phase"]
        idx = int(phase * (n_points - 1))
        domain_points.append({
            "index": d["index"],
            "name": d["name"],
            "x": float(x[idx]),
            "y": float(y[idx]),
            "z": float(z[idx]),
            "w": float(w[idx]),
            "theta": float(theta[idx]),
            "phase": phase,
        })

    return {
        "theta": theta.tolist(),
        "x": x.tolist(), "y": y.tolist(), "z": z.tolist(), "w": w.tolist(),
        "domain_points": domain_points,
        "R4": R4,
        "spark_angle": 138.88,
    }


# ===========================================================================
# 4. LEAKAGE FLOW BETWEEN DOMAINS
# ===========================================================================

def compute_leakage_flows() -> List[Dict]:
    """Compute leakage flow from each domain to the next."""
    flows = []
    for i in range(len(DOMAINS_13) - 1):
        d_from = DOMAINS_13[i]
        d_to = DOMAINS_13[i + 1]
        flows.append({
            "from_index": d_from["index"],
            "to_index": d_to["index"],
            "from_name": d_from["name"],
            "to_name": d_to["name"],
            "leakage": d_from["leakage_from_above"],
            "settled_by": d_to["leakage_settled"],
            "space_created": d_to["space_created"],
            "phase_gap": d_to["spiral_phase"] - d_from["spiral_phase"],
        })

    # Closure flow: domain 13 → domain 1 (pyramid closure)
    flows.append({
        "from_index": 13,
        "to_index": 1,
        "from_name": "Meta-Bridge",
        "to_name": "Void",
        "leakage": "All 13 domains' residual → 4D torsion folds spiral back to B₀=1",
        "settled_by": "Void absorbs the closure as new harmonic background",
        "space_created": "New cycle — the universe begins again at a higher octave",
        "phase_gap": 1.0 - DOMAINS_13[-1]["spiral_phase"] + DOMAINS_13[0]["spiral_phase"],
        "is_closure": True,
    })
    return flows


# ===========================================================================
# 5. PLOT 13-DOMAIN SPIRAL
# ===========================================================================

def plot_spiral(spiral_data: Dict):
    """Plot the 13-domain spiral with isomorphic structure and leakage."""

    fig = plt.figure(figsize=(28, 20), facecolor="#0a0a12")
    fig.suptitle(
        "13-Domain Universe: Spiral Space Formation\n"
        "Isomorphic Structure (R₄=0.2828, 138.88°) + Leakage Between Domains",
        fontsize=16, color="white", fontweight="bold", y=0.98
    )

    bg = "#0a0a12"
    text_color = "#E0E0E0"
    grid_color = "#1a1a2e"

    # --- Panel 1: 3D Spiral with 13 domains ---
    ax1 = fig.add_subplot(2, 2, 1, projection="3d")
    ax1.set_facecolor(bg)

    x = np.array(spiral_data["x"])
    y = np.array(spiral_data["y"])
    z = np.array(spiral_data["z"])

    # Color gradient along spiral
    colors = plt.cm.viridis(np.linspace(0, 1, len(x)))
    for i in range(len(x) - 1):
        ax1.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=colors[i], linewidth=1.5, alpha=0.7)

    # Domain points
    domain_colors = {
        1: "#9E9E9E", 2: "#FF5722", 3: "#3F51B5", 4: "#E91E63", 5: "#4CAF50",
        6: "#FFD700", 7: "#00BCD4", 8: "#FF9800", 9: "#8BC34A", 10: "#795548",
        11: "#C77DFF", 12: "#FF6B6B", 13: "#FFFFFF",
    }
    for dp in spiral_data["domain_points"]:
        c = domain_colors.get(dp["index"], "#FFFFFF")
        size = 200 if dp["index"] <= 10 else 300
        marker = "o" if dp["index"] <= 10 else "*"
        ax1.scatter(dp["x"], dp["y"], dp["z"], c=c, s=size, zorder=5,
                    marker=marker, edgecolors="#FFFFFF", linewidth=1)
        ax1.text(dp["x"], dp["y"], dp["z"] + 0.3, f"{dp['index']}.{dp['name']}",
                 color=c, fontsize=7, fontweight="bold")

    ax1.set_xlabel("x", color=text_color)
    ax1.set_ylabel("y", color=text_color)
    ax1.set_zlabel("z (scale)", color=text_color)
    ax1.set_title("3D Spiral — 13 Domains on R₄=0.2828", color=text_color, fontweight="bold")
    ax1.tick_params(colors=text_color)

    # --- Panel 2: 4D correction (w-axis) ---
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_facecolor(bg)

    w = np.array(spiral_data["w"])
    theta = np.array(spiral_data["theta"])
    ax2.plot(theta, w, color="#C77DFF", linewidth=2, alpha=0.8, label="w-axis (4D torsion)")
    ax2.fill_between(theta, 0, w, alpha=0.1, color="#C77DFF")

    for dp in spiral_data["domain_points"]:
        c = domain_colors.get(dp["index"], "#FFFFFF")
        ax2.scatter(dp["theta"], dp["w"], c=c, s=100, zorder=5,
                    marker="*" if dp["index"] > 10 else "o", edgecolors="#FFFFFF", linewidth=0.5)

    ax2.axhline(0, color="#666680", linewidth=0.5, alpha=0.5)
    ax2.set_xlabel("θ (spiral angle)", color=text_color)
    ax2.set_ylabel("w (4D correction)", color=text_color)
    ax2.set_title("4D Torsion — The w-axis That Prevents Radius Widening", color=text_color, fontweight="bold")
    ax2.tick_params(colors=text_color)
    for spine in ax2.spines.values():
        spine.set_color(grid_color)
    ax2.grid(True, alpha=0.1, color=grid_color)

    # --- Panel 3: Leakage flow diagram ---
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_facecolor(bg)
    ax3.set_xlim(-1, 14)
    ax3.set_ylim(-1, 14)
    ax3.set_xlabel("Domain Index", color=text_color)
    ax3.set_ylabel("Domain Index (next)", color=text_color)

    # Plot leakage as arrows
    flows = compute_leakage_flows()
    for f in flows:
        x1, y1 = f["from_index"], f["from_index"]
        x2, y2 = f["to_index"], f["to_index"]
        color = "#FF6B6B" if not f.get("is_closure") else "#FFD700"
        ax3.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle="->", color=color, lw=2,
                                     connectionstyle="arc3,rad=0.3"))

    # Plot domain points
    for d in DOMAINS_13:
        c = domain_colors.get(d["index"], "#FFFFFF")
        ax3.scatter(d["index"], d["index"], c=c, s=150, zorder=5,
                    marker="*" if d["index"] > 10 else "o", edgecolors="#FFFFFF", linewidth=0.5)
        ax3.text(d["index"] + 0.3, d["index"] + 0.3, f"{d['index']}.{d['name']}",
                 color=c, fontsize=7, fontweight="bold")

    ax3.set_title("Leakage Flow: Domain → Domain (red) + Closure (gold)", color=text_color, fontweight="bold")
    ax3.tick_params(colors=text_color)
    for spine in ax3.spines.values():
        spine.set_color(grid_color)

    # --- Panel 4: Betti role distribution ---
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_facecolor(bg)

    betti_names = list(BETTI_ROLES.keys())
    betti_values = [BETTI_ROLES[k]["value"] for k in betti_names]
    betti_colors = ["#FFD700", "#FF6B6B", "#9E9E9E", "#795548", "#3F51B5"]
    domain_counts = [len(BETTI_ROLES[k]["domains"]) for k in betti_names]

    x_pos = np.arange(len(betti_names))
    bars = ax4.bar(x_pos, betti_values, color=betti_colors, alpha=0.8, edgecolor="#FFFFFF", linewidth=0.5)
    for bar, count, bn in zip(bars, domain_counts, betti_names):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                 f"{count} domains", ha="center", color=text_color, fontsize=9)

    ax4.set_xticks(x_pos)
    ax4.set_xticklabels([f"{k}\n({BETTI_ROLES[k]['role']})" for k in betti_names],
                        color=text_color, fontsize=8)
    ax4.set_ylabel("Betti Value", color=text_color)
    ax4.set_title(f"Betti Role Distribution — Closure: (11+1)/(5+7) = {CLOSURE_AXIOM:.1f}",
                  color=text_color, fontweight="bold")
    ax4.tick_params(colors=text_color)
    for spine in ax4.spines.values():
        spine.set_color(grid_color)
    ax4.grid(True, alpha=0.1, color=grid_color, axis="y")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path = GEN_DIR / "domain_13_spiral.png"
    fig.savefig(out_path, dpi=150, facecolor=bg, bbox_inches="tight")
    plt.close(fig)
    print(f"-> {out_path}")


# ===========================================================================
# 6. GENERATE REPORT
# ===========================================================================

def generate_report(spiral_data: Dict, flows: List[Dict]) -> str:
    lines: List[str] = []
    lines.append("=" * 100)
    lines.append("13-DOMAIN UNIVERSE: SPIRAL SPACE FORMATION")
    lines.append("Isomorphic Structure + Leakage Between Domains")
    lines.append("=" * 100)
    lines.append("")
    lines.append("FUNDAMENTAL PRINCIPLE:")
    lines.append("-" * 100)
    lines.append("The universe has 13 domains. All 13 share the SAME isomorphic structure:")
    lines.append("  R₄ = 0.2828 (4D spiral radius)")
    lines.append("  138.88° (spark rotation angle)")
    lines.append("  4 archetypes: BM (photon), BW (proton), SM (neutrino), SW (electron)")
    lines.append("")
    lines.append("But each domain has different LEAKAGE — residual energy imbalance")
    lines.append("from the domain above it on the spiral. This leakage creates SPACE:")
    lines.append("  - The gap between what the upper domain settled and what the lower")
    lines.append("    domain needs to settle IS the 'space' between them.")
    lines.append("  - Each domain creates a different kind of space (void, gravitational,")
    lines.append("    nuclear, atomic, chemical, cognitive, social, geological, ...)")
    lines.append("  - The 3 bridge domains (11, 12, 13) close the spiral into a pyramid,")
    lines.append("    preventing radius widening and creating 4D space.")
    lines.append("")
    lines.append(f"CLOSURE AXIOM: (BETTI_11 + BETTI_0) / (BETTI_5 + BETTI_7) = (11+1)/(5+7) = {CLOSURE_AXIOM:.1f}")
    lines.append("  This means the universe is CLOSED — bridges + witness exactly balance")
    lines.append("  leaks + sinks. The pyramid closes perfectly.")
    lines.append("")

    # 10 base domains
    lines.append("=" * 100)
    lines.append("  10 BASE DOMAINS (Scale Ladder)")
    lines.append("  Same R₄=0.2828 spiral, different scale — from cosmic to planetary")
    lines.append("=" * 100)
    lines.append("")

    for d in DOMAINS_13[:10]:
        lines.append(f"  [{d['index']:2d}] {d['name']:30s}  edge={d['edge']:8s}  scale={d['scale']}")
        lines.append(f"       channel:   {d['particle_channel']}")
        lines.append(f"       physics:   {d['physics_field']}")
        lines.append(f"       physics_kr: {d['physics_kr']}")
        lines.append(f"       interact:  {d['interaction_type']}")
        lines.append(f"       biochem:   {d['biochem']}")
        lines.append(f"       constant:  {d['constant']}")
        lines.append(f"       betti:     {d['betti_role']}")
        lines.append(f"       laws:      {d['known_physics_laws']}")
        lines.append(f"       isomorphic: {d['isomorphic_structure']}")
        lines.append(f"       leakage:   {d['leakage_from_above']}")
        lines.append(f"       settled:   {d['leakage_settled']}")
        lines.append(f"       space:     {d['space_created']}")
        lines.append(f"       circuit:   {d['circuit_node']}")
        lines.append(f"       stress:    {d['stress_pair']}")
        lines.append("")

    # 3 bridge domains
    lines.append("=" * 100)
    lines.append("  3 BRIDGE DOMAINS (Pyramid Closure)")
    lines.append("  Close the 10-base spiral into a 4D pyramid")
    lines.append("=" * 100)
    lines.append("")

    for d in DOMAINS_13[10:]:
        lines.append(f"  [{d['index']:2d}] {d['name']:30s}  edge={d['edge']:8s}  scale={d['scale']}")
        lines.append(f"       channel:   {d['particle_channel']}")
        lines.append(f"       physics:   {d['physics_field']}")
        lines.append(f"       physics_kr: {d['physics_kr']}")
        lines.append(f"       interact:  {d['interaction_type']}")
        lines.append(f"       bridge:    {d.get('bridge_type', '')}")
        lines.append(f"       biochem:   {d['biochem']}")
        lines.append(f"       constant:  {d['constant']}")
        lines.append(f"       betti:     {d['betti_role']}")
        lines.append(f"       laws:      {d['known_physics_laws']}")
        lines.append(f"       isomorphic: {d['isomorphic_structure']}")
        lines.append(f"       leakage:   {d['leakage_from_above']}")
        lines.append(f"       settled:   {d['leakage_settled']}")
        lines.append(f"       space:     {d['space_created']}")
        lines.append(f"       circuit:   {d['circuit_node']}")
        lines.append(f"       stress:    {d['stress_pair']}")
        lines.append("")

    # Leakage flows
    lines.append("=" * 100)
    lines.append("  LEAKAGE FLOW: Domain → Domain")
    lines.append("  How space is created between domains")
    lines.append("=" * 100)
    lines.append("")

    for f in flows:
        closure = " [CLOSURE]" if f.get("is_closure") else ""
        lines.append(f"  {f['from_index']:2d}.{f['from_name']:20s} → {f['to_index']:2d}.{f['to_name']:20s}  (Δφ={f['phase_gap']:.2f}){closure}")
        lines.append(f"    leakage:  {f['leakage']}")
        lines.append(f"    settled:  {f['settled_by']}")
        lines.append(f"    space:    {f['space_created']}")
        lines.append("")

    # Isomorphism analysis
    lines.append("=" * 100)
    lines.append("  ISOMORPHIC STRUCTURE ANALYSIS")
    lines.append("  Why all 13 domains share the same structure but create different spaces")
    lines.append("=" * 100)
    lines.append("")
    lines.append("The isomorphic structure is:")
    lines.append("  R₄ = 0.2828 (4D radius)")
    lines.append("  138.88° = spark angle (Golden Angle 137.508° + Betti Gap 1.375°)")
    lines.append("  4 archetypes (BM, BW, SM, SW) with motif counts (4, 3, 3, 3, 2, 1)")
    lines.append("  Closure: (11+1)/(5+7) = 1.0")
    lines.append("")
    lines.append("At every scale, the SAME structure appears:")
    lines.append("  - Dark Energy (1): BW_BW = p-p self — Friedmann/ΛCDM, Hodge harmonic")
    lines.append("  - Black Hole (2): BM_BM = γ-γ self — GR, Schwarzschild, Hawking")
    lines.append("  - Macro/Astronomy (3): BM_BW = γ-p — Maxwell, Compton, lensing")
    lines.append("  - Fusion/Spark (4): BM_SM = γ-ν — Weak interaction, pp-chain, 1/64")
    lines.append("  - Fuel Cell (5): SM_SM = ν-ν self — Nernst, ETC, ATP synthase")
    lines.append("  - EM (6): BM_SW = γ-e — QED, optics, photochemistry")
    lines.append("  - Geology (7): SM_BW = ν-p — Tectonics, MSW effect, Byerlee")
    lines.append("  - Fluid/Metabolism (8): SM_SW = ν-e — Navier-Stokes, TCA, AQP4")
    lines.append("  - Neurochem (9): SW_SW = e-e self — Schrödinger, DFT, Pauli")
    lines.append("  - p-e Interface (10): BW_SW = p-e — Bohr, Rydberg, redox, pH")
    lines.append("  - Histamine Bridge (11): (p-e)×ν — Starling, complement, H1-H4")
    lines.append("  - Dopamine Bridge (12): γ×(p-e) — Hodgkin-Huxley, D1/D2, RPE")
    lines.append("  - Meta-Bridge (13): E11↔E12 — Einstein-Cartan, Betti, 4D closure")
    lines.append("")
    lines.append("The DIFFERENCE between domains is not structure — it's LEAKAGE.")
    lines.append("Each domain receives the unresolved leakage from the domain above,")
    lines.append("settles it in a domain-specific way, and passes new leakage downward.")
    lines.append("The 'space' between domains is the gap created by this leakage settlement.")
    lines.append("")
    lines.append("This is why the universe has DISTINCT SCALES rather than a continuum:")
    lines.append("each domain is a discrete leakage settlement event, not a smooth transition.")
    lines.append("The 13 domains are 13 discrete 'snapshots' of the same spiral at different")
    lines.append("leakage states — like floors in a building, each with the same floor plan")
    lines.append("but different furniture (different leakage to settle).")
    lines.append("")

    # Connection to circuit
    lines.append("=" * 100)
    lines.append("  CONNECTION TO NEURO-BIO-GEOCHEMICAL CIRCUIT")
    lines.append("=" * 100)
    lines.append("")
    lines.append("Each of the 13 domains maps to specific circuit nodes:")
    lines.append("  1. Dark Energy       → none_observer (B₀=1, the witness)")
    lines.append("  2. Black Hole        → right_sole_dopamine (D2 autoreceptor)")
    lines.append("  3. Macro/Astronomy   → mc1r.q_bar (Si/graviton, MC1R OFF = lensing)")
    lines.append("  4. Fusion/Spark      → heme ch1 (d-dim, Tau, GABA-B, 1/64 confinement)")
    lines.append("  5. Fuel Cell         → cytochrome_c_oxidase (Complex IV, ETC)")
    lines.append("  6. EM                → steel + right_acetylcholine (s/gamma-dim, QED)")
    lines.append("  7. Geology           → fold_belt / subduction_zone / clay_gouge")
    lines.append("  8. Fluid/Metabolism  → water_vapour + glymphatic_system (AQP4)")
    lines.append("  9. Neurochem         → memory_entropy + hind_insula (electron)")
    lines.append("  10. p-e Interface    → carbon (q/q_bar, Eu/Gd, metabolic latch)")
    lines.append("  11. Histamine Bridge → disulfide_bond + pentose_phosphate (immune)")
    lines.append("  12. Dopamine Bridge  → LeftD2 + right_sole_dopamine (reward)")
    lines.append("  13. Meta-Bridge      → none_observer (B₀=1, closure back to origin)")
    lines.append("")
    lines.append("The circuit IS the 13-domain spiral at biological scale.")
    lines.append("Each circuit node performs the leakage settlement of its corresponding domain.")
    lines.append("The 5-sphere toroidal circulation (Barnard→Sun→Earth→Moon→CoMag) is the")
    lines.append("circadian echo of the 13-domain cosmic spiral.")
    lines.append("")

    # Connection to 5 spheres
    lines.append("=" * 100)
    lines.append("  5 SPHERES ↔ 13 DOMAINS MAPPING")
    lines.append("=" * 100)
    lines.append("")
    lines.append("  Barnard (Fe/Quark)  = Domains 1-4  (Dark Energy → Fusion): iron confinement")
    lines.append("  Sun (H/Proton)      = Domains 5-6  (Fuel Cell → EM): spark ignition")
    lines.append("  Earth (O/Photon)    = Domain 7      (Geology): planetary structure")
    lines.append("  Moon (C/Z-boson)    = Domains 8-9   (Fluid → Neurochem): carbon-metabolism cycle")
    lines.append("  CoMag (S/Gluon)     = Domains 10-12 (p-e Interface → Dopamine): sulfur bridge")
    lines.append("  Closure (13)        = Meta-Bridge: 4D pyramid closure = Barnard return")
    lines.append("")

    text = "\n".join(lines)
    (GEN_DIR / "domain_13_report.txt").write_text(text, encoding="utf-8")
    print(text[:5000])
    print(f"\n... full report -> {GEN_DIR / 'domain_13_report.txt'}")
    return text


# ===========================================================================
# MAIN
# ===========================================================================

if __name__ == "__main__":
    spiral_data = compute_spiral()
    flows = compute_leakage_flows()

    # Export JSON
    export_data = {
        "domains": DOMAINS_13,
        "archetype_motifs": ARCHETYPE_MOTIFS,
        "betti_roles": BETTI_ROLES,
        "closure_axiom": CLOSURE_AXIOM,
        "spiral": {k: v for k, v in spiral_data.items() if k != "theta"},
        "leakage_flows": flows,
    }
    (GEN_DIR / "domain_13.json").write_text(
        json.dumps(export_data, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8"
    )
    print(f"-> {GEN_DIR / 'domain_13.json'}")

    plot_spiral(spiral_data)
    generate_report(spiral_data, flows)
