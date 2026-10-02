"""5-Sphere Historical Cosmology: Temporal Leakage Settlement & Catastrophes.

The 5 spheres are not just circadian phases — they represent 5 epochs of
cosmic/Earth history. Each sphere transition is a major catastrophe that:
  1. Settles "leakage" from the previous epoch (residual energy imbalance)
  2. Creates the conditions for the next epoch
  3. Determines the current state, energy distribution, and form of all subjects

The toroidal circulation IS geological/biological/cosmic history.

SPHERE TIMELINE (reverse chronological = toroidal flow direction):

  Barnard (Fe/Quark/Higgs) — PRIMORDIAL IRON EPOCH
    Big Bang → stellar nucleosynthesis → iron peak → Earth core formation
    Leakage: gravitational potential energy → heat → iron differentiation

  Sun (H/Proton) — STELLAR IGNITION EPOCH  
    Solar system formation → Great Oxidation Event → photosynthesis
    Leakage: iron mass → proton spark (138.88° reset)

  Earth (O/Photon) — OXYGENIC PHOTIC EPOCH
    Atmospheric oxygenation → Cambrian explosion → complex life
    Leakage: reduced carbon → oxidized atmosphere → photon-driven metabolism

  Moon (C/Z-boson) — CARBON-TIDAL EPOCH
    Theia impact → Moon formation → tidal cycles → carbon cycle
    Leakage: oxygen over-accumulation → carbon sequestration → tidal time clock

  CoMag (S/W-boson/Gluon) — SULFUR-BRIDGE EPOCH
    Hydrothermal vents → deep biosphere → gut microbiome → social binding
    Leakage: surface-only life → deep-surface coupling → gluon binding bridge

  → Barnard (return): Mass extinction cycle → iron meteorite → reset

Each transition hosts multiple catastrophes at different scales:
  - Cosmic: supernova, gamma ray burst, galactic tide
  - Earth-surface: impact, flood basalt, glaciation
  - Geophysical: core reversal, mantle plume, supercontinent breakup
  - Biological: mass extinction, adaptive radiation, bottleneck

Outputs:
  generated/sphere_history_report.txt
  generated/sphere_history.json
  generated/sphere_history_timeline.png
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
# 1. 5-SPHERE HISTORICAL EPOCHS
# ===========================================================================

SPHERE_EPOCHS: Dict[str, Dict] = {
    "Barnard": {
        "epoch_name": "PRIMORDIAL IRON EPOCH",
        "epoch_kr": "원시 철 시대",
        "element": "Fe",
        "particle": "Quark/Higgs",
        "attractor": "Energy",
        "dims": ("g", "d"),
        "body_region": "chest/liver",
        "time_range": "13.8Ga — 4.54Ga (Big Bang → Earth formation)",
        "circadian": (21, 3),
        "circadian_phase": "AB_integration / reset_spark",
        "color": "#FF5722",

        "cosmic_events": [
            {"name": "Big Bang nucleosynthesis", "time": "13.8Ga", "desc": "H, He, Li created. Quark-gluon plasma cools. First matter/non-matter separation."},
            {"name": "First stars (Population III)", "time": "~13.6Ga", "desc": "Massive stars burn H→He→C→O→Si→Fe. Iron peak elements forged. First supernovae."},
            {"name": "Iron peak nucleosynthesis", "time": "~13.5Ga", "desc": "Type II supernovae produce Fe-56, Ni, Co, Mn, Cr. The matter/non-matter stress pair (s,g) governs core collapse: mass (s) vs binding energy (g)."},
            {"name": "Galaxy formation", "time": "~13Ga", "desc": "Milky Way forms. Dark matter halo (g↑) provides gravitational scaffold for baryonic matter (s↑)."},
            {"name": "Solar nebula collapse", "time": "4.57Ga", "desc": "Giant molecular cloud collapses. Iron-silicate dust accretes. The Higgs field gives mass to particles — Barnard's 'Energy attractor' anchors mass."},
            {"name": "Earth core formation (Iron Catastrophe)", "time": "4.54Ga", "desc": "Mantle melting → Fe-Ni sinks to core. Gravitational potential energy → heat. THE fundamental leakage settlement: iron mass separates from silicate crust. This creates Earth's magnetic field, plate tectonics engine, and the Fe-cycle that all biology depends on."},
        ],

        "geophysical_events": [
            {"name": "Magma ocean differentiation", "time": "4.54Ga", "desc": "Global magma ocean → denser Fe-Ni sinks, lighter silicate floats. The first 'circuit': iron core (Barnard/Fe) vs silicate mantle (future Earth/O)."},
            {"name": "Core-mantle boundary formation", "time": "4.54Ga", "desc": "Outer core liquid Fe convection begins. Geodynamo starts. Magnetic field shields atmosphere from solar wind — prerequisite for all later life."},
            {"name": "LLSVP formation", "time": "~4.5Ga", "desc": "Large Low-Shear-Velocity Provinces (Tuzo/Jason) form at core-mantle boundary. Thermochemical piles that persist for 4.5 billion years — the circuit's lower_mantle node."},
        ],

        "biological_events": [
            {"name": "Pre-biotic chemistry", "time": "4.5-4.0Ga", "desc": "Iron-sulfur surfaces catalyze organic synthesis. The Fe-S world hypothesis: deep-sea hydrothermal vents provide the first electron transfer chains. Cytochrome and ferredoxin ancestors are iron-sulfur clusters — the circuit's heme/ferritin/sulfur_iron_complex nodes."},
        ],

        "leakage_settled": "Gravitational potential energy → core heat → magnetic field. Iron mass (s-dim) separated from silicate (future g-dim). The 'leakage' is the energy released by differentiation — it becomes Earth's internal heat engine, driving all subsequent geology.",
        "leakage_kr": "중력 퍼텐셜 에너지 → 핵 열 → 자기장. 철 질량이 규산염에서 분리되며 방출된 에너지가 지구 내부 열기관이 됨.",
    },

    "Sun": {
        "epoch_name": "STELLAR IGNITION EPOCH",
        "epoch_kr": "항성 점화 시대",
        "element": "H",
        "particle": "Proton",
        "attractor": "Information",
        "dims": ("r", "s"),
        "body_region": "brain/ETC",
        "time_range": "4.54Ga — 2.4Ga (Solar ignition → Great Oxidation)",
        "circadian": (0, 3),
        "circadian_phase": "AB_spark / light_dark",
        "color": "#FFD700",

        "cosmic_events": [
            {"name": "Solar ignition", "time": "4.57Ga", "desc": "Proto-Sun reaches fusion temperature. H→He fusion begins. The 138.88° spark: iron mass (Barnard) → proton spark (Sun). This is the circuit's reset_spark transition — the fundamental renewal."},
            {"name": "T-Tauri phase", "time": "4.56-4.54Ga", "desc": "Young Sun emits intense UV, clears inner solar system. The light/dark stress pair (gamma, d) governs UV radiation (light) vs. shadowed organic chemistry (dark)."},
            {"name": "Solar luminosity evolution", "time": "4.5-2.4Ga", "desc": "Sun was 70% current luminosity (Faint Young Sun paradox). Requires greenhouse atmosphere to maintain liquid water. The r-dim (rhythm/tempo) of solar input is low — slow, steady energy."},
        ],

        "geophysical_events": [
            {"name": "Hadean Eon", "time": "4.54-4.0Ga", "desc": "Molten surface, frequent impacts. The Late Heavy Bombardment (4.1-3.8Ga) delivers water and organic molecules. The circuit's subduction_zone / light_dark transition: impact energy (light) → subsurface chemistry (dark)."},
            {"name": "First crust formation", "time": "~4.4Ga", "desc": "Jack Hills zircons show solid crust by 4.4Ga. The Information attractor (h, nu, s) begins: stable substrate allows information storage in mineral lattices."},
            {"name": "Plate tectonics initiation", "time": "~3.5Ga", "desc": "First evidence of plate tectonics. Subduction begins recycling crust. The circuit's fold_belt and subduction_zone nodes activate — geological memory (Information attractor)."},
        ],

        "biological_events": [
            {"name": "First life (LUCA)", "time": "~3.8-3.5Ga", "desc": "Last Universal Common Ancestor. Iron-sulfur metabolism, chemiosmotic coupling. The circuit's cytochrome_c_oxidase and heme nodes originate here — ETC (Electron Transport Chain) is the biological analog of the Sun's proton spark."},
            {"name": "Anoxygenic photosynthesis", "time": "~3.5Ga", "desc": "Purple sulfur bacteria use H₂S instead of H₂O. No O₂ produced. The circuit's sulfur_iron_complex and histosol nodes — sulfur cycle precedes oxygen cycle."},
            {"name": "Oxygenic photosynthesis (Cyanobacteria)", "time": "~3.0-2.7Ga", "desc": "Cyanobacteria split H₂O → O₂ + H⁺. The most important biological innovation in Earth history. The circuit's water_vapour and steel nodes — water (O source) + iron (O sink). This creates the Great Oxidation Event."},
            {"name": "Great Oxidation Event (GOE)", "time": "2.4Ga", "desc": "Atmospheric O₂ rises from <0.001% to ~1%. Massive iron precipitation (Banded Iron Formations). THE leakage settlement: reduced iron (Fe²⁺, dissolved in ocean) → oxidized iron (Fe³⁺, BIF precipitation). The O₂/CO₂ stress pair (h,p) activates for the first time at planetary scale. This is the Sun→Earth transition: proton spark (H fusion) → oxygen atmosphere (photon-driven biology)."},
        ],

        "leakage_settled": "Iron mass from Barnard epoch → proton spark (solar fusion) → oxygen production (photosynthesis). The 'leakage' is reduced iron dissolved in oceans — it gets oxidized and precipitated as BIF, settling the Fe²⁺/Fe³⁺ imbalance. This creates the steel node (Banded Iron Formation) and the atmospheric O₂ that defines the next epoch.",
        "leakage_kr": "Barnard 시대의 철 질량 → 양성자 spark (태양 융합) → 산소 생산 (광합성). 해양의 Fe²⁺가 산화되어 BIF로 침전되며 Fe 불균형이 정산됨.",
    },

    "Earth": {
        "epoch_name": "OXYGENIC PHOTIC EPOCH",
        "epoch_kr": "산소 광합성 시대",
        "element": "O",
        "particle": "Photon",
        "attractor": "Repair",
        "dims": ("gamma", "h"),
        "body_region": "thorax/spine",
        "time_range": "2.4Ga — 0.5Ga (GOE → Cambrian explosion)",
        "circadian": (3, 9),
        "circadian_phase": "A_accumulate / o2_co2",
        "color": "#4CAF50",

        "cosmic_events": [
            {"name": "Huronian glaciation (Snowball Earth I)", "time": "2.4-2.1Ga", "desc": "O₂ destroys atmospheric methane (greenhouse gas) → global glaciation. First 'oxygen catastrophe' — the leakage from GOE causes climate collapse. The heat/cold stress pair (nu,r) activates as a secondary effect."},
            {"name": "Oxygen cycles (Lomagundi-Jatuli event)", "time": "2.3-2.0Ga", "desc": "Massive carbon isotope excursion. O₂ fluctuates wildly. The circuit's carbon node (DFF) oscillates — q/q_bar switching between oxidized and reduced states."},
            {"name": "Sulfur isotope anomaly ends", "time": "~2.4Ga", "desc": "Mass-independent sulfur fractionation (MIF) disappears — atmosphere becomes permanently oxidized. The circuit's pyrite and sulfur_iron_complex nodes shift from reduced to oxidized regime."},
        ],

        "geophysical_events": [
            {"name": "Columbia supercontinent", "time": "1.8-1.5Ga", "desc": "First major supercontinent assembles. Continental collisions create fold belts. The circuit's fold_belt node — orogenic belts as geological memory storage."},
            {"name": "Rodinia supercontinent", "time": "1.1Ga-750Ma", "desc": "Supercontinent assembles and breaks apart. The breakup creates new ocean basins, changing ocean circulation. The circuit's basin node — sedimentary basins form at continental margins."},
            {"name": "Banded Iron Formation deposition ends", "time": "~1.85Ga", "desc": "Ocean becomes fully oxidized — no more dissolved Fe²⁺ to precipitate. The steel node's active phase ends. Iron now must be obtained from solid minerals — biological iron acquisition becomes energetically expensive."},
            {"name": "Sturtian glaciation (Snowball Earth II)", "time": "717-660Ma", "desc": "Global glaciation. Ice covers entire Earth. The circuit's histosol/cryosol nodes — permafrost lock. Biological survival requires extreme adaptation → evolutionary bottleneck."},
            {"name": "Marinoan glaciation (Snowball Earth III)", "time": "650-635Ma", "desc": "Second global glaciation. The melt-back releases massive nutrients → biological radiation. The circuit's plume node — volcanic CO₂ from deglaciation triggers greenhouse warming."},
        ],

        "biological_events": [
            {"name": "Eukaryotic cell evolution", "time": "~2.0Ga", "desc": "Mitochondria (alpha-proteobacteria endosymbiosis). The O₂-based metabolism becomes dominant. The circuit's cytochrome_c_oxidase (Complex IV) — the terminal oxidase that uses O₂ as electron acceptor. This is the Repair attractor: oxygen-based homeostasis."},
            {"name": "Sexual reproduction", "time": "~1.2Ga", "desc": "Meiosis and genetic recombination. The circuit's mc1r (D flip-flop) — genetic state storage with q/q_bar. Sexual reproduction = clocked state update, exactly like a DFF."},
            {"name": "Multicellularity", "time": "~1.0Ga", "desc": "Cell differentiation, tissue formation. The circuit's collagen and actomyosin nodes — structural proteins that enable multicellular form. The g-dim (binding) becomes critical for tissue cohesion."},
            {"name": "Ediacaran biota", "time": "635-541Ma", "desc": "First large, complex organisms. Soft-bodied. The circuit's memory_entropy node — novelty/mismatch detection. Ediacaran organisms are the first 'information processors' at macroscopic scale."},
            {"name": "Cambrian Explosion", "time": "541Ma", "desc": "Rapid diversification of animal body plans. All modern phyla appear. The Information attractor (h, nu, s) reaches full activation — sensory systems, nervous systems, predation. The circuit's hind_insula and memory_entropy nodes — the first cognitive systems. This is the Earth→Moon transition: oxygen atmosphere (Earth) → carbon-based cognition (Moon)."},
        ],

        "leakage_settled": "Atmospheric O₂ from Sun epoch → ozone layer → UV protection → complex life. The 'leakage' is oxygen over-accumulation — it gets settled by: (1) BIF precipitation (Fe²⁺+O₂→Fe³⁺), (2) ozone layer formation (O₃), (3) aerobic metabolism (O₂ as electron acceptor). The Repair attractor is the settlement mechanism: oxygen-based damage repair.",
        "leakage_kr": "Sun 시대의 대기 산소 → 오존층 → UV 차단 → 복잡한 생명. 산소 과잉이 BIF 침전, 오존층, 호기 대사로 정산됨. Repair attractor가 정산 메커니즘.",
    },

    "Moon": {
        "epoch_name": "CARBON-TIDAL EPOCH",
        "epoch_kr": "탄소-조석 시대",
        "element": "C",
        "particle": "Z-boson",
        "attractor": "Time",
        "dims": ("p", "nu"),
        "body_region": "occiput/right brain",
        "time_range": "4.54Ga (Theia impact) — present (carbon cycle, tidal rhythm)",
        "circadian": (9, 15),
        "circadian_phase": "O_accumulate / heat_cold",
        "color": "#9E9E9E",

        "cosmic_events": [
            {"name": "Theia impact (Moon formation)", "time": "4.54Ga", "desc": "Mars-sized Theia collides with Earth. Debris forms Moon. THE most catastrophic event in Earth history. The circuit's fold_belt node — the impact creates the first orogenic deformation. The Moon becomes the Time attractor: 28-day orbital period governs tides, menstrual cycles, and biological rhythms. This event is retroactively placed here because the Moon's influence on carbon cycle and tidal mixing becomes dominant AFTER the Earth epoch establishes oceans."},
            {"name": "Moon recession", "time": "4.5Ga-present", "desc": "Moon moves from ~24,000km to 384,000km. Tidal force decreases. Early Earth had ~10x current tides — extreme tidal mixing drives chemical disequilibrium. The circuit's water_vapour and sodium nodes — tidal pumping of oceanic chemistry."},
            {"name": "Milankovitch cycles", "time": "continuous", "desc": "Orbital eccentricity, axial tilt, precession governed by Moon's gravitational pull. 100kyr, 41kyr, 23kyr cycles drive ice ages. The Time attractor's 28-day schedule is the short-period component of a hierarchy extending to 100,000 years."},
        ],

        "geophysical_events": [
            {"name": "Carbon cycle establishment", "time": "3.5Ga-present", "desc": "CO₂ ↔ organic carbon ↔ carbonate. The circuit's carbon node (DFF) — the master metabolic latch. The Moon's tidal mixing accelerates silicate weathering (CO₂ sink) → climate regulation. The p-dim (periodicity) of carbon cycle is Moon-governed."},
            {"name": "Tidal rhythmites", "time": "continuous", "desc": "Tidal deposits record orbital parameters. 3.2Ga rhythmites show shorter lunar month (22 days vs. 27.3 today). The Time attractor's clock is physically recorded in geology."},
            {"name": "Ocean tidal mixing", "time": "continuous", "desc": "Tides mix nutrient-rich deep water with surface waters. Biological productivity is highest in tidal zones. The circuit's basin and water_vapour nodes — tidal basins as nutrient concentrators."},
            {"name": "Monsoon system", "time": "~8Ma-present", "desc": "Himalayan uplift + Moon tidal influence creates monsoon. Seasonal carbon flux. The circuit's fold_belt → water_vapour transition: mountain orogen drives atmospheric circulation."},
        ],

        "biological_events": [
            {"name": "Tidal zone colonization", "time": "~500Ma", "desc": "Organisms adapt to intertidal zones — periodic exposure/submersion. The p-dim (periodicity) becomes a survival requirement. The circuit's heath_aerenchyma and mangrove_aerenchyma nodes — plants adapted to periodic flooding."},
            {"name": "Circadian rhythm evolution", "time": "~2.5Ga-present", "desc": "Biological clocks align with day/night + tidal cycles. The circuit's co2 node — CO₂ accumulation overnight (dark respiration) vs. daytime photosynthesis. The Time attractor governs the 24h + 12.4h (tidal) dual clock."},
            {"name": "Vertebrate brain evolution", "time": "~500Ma-present", "desc": "Hippocampus (spatial memory), cerebellum (motor timing), occipital cortex (visual processing). The circuit's memory_entropy and hind_insula nodes — right brain (occiput) = Time attractor territory. The Moon's 28-day cycle maps to hippocampal theta rhythm."},
            {"name": "Menstrual cycle", "time": "~200Ma (mammals)", "desc": "28-day reproductive cycle aligns with lunar period. The circuit's mc1r and left_genital_d2 nodes — reproductive state machine clocked by lunar time. The Time attractor's most direct biological expression."},
            {"name": "Mass extinctions (5 big)", "time": "445, 375, 252, 201, 66 Ma", "desc": "Ordovician-Silurian, Late Devonian, Permian-Triassic (The Great Dying), Triassic-Jurassic, Cretaceous-Paleogene. Each extinction resets the carbon cycle (carbon DFF toggle). The Time attractor governs the periodicity of mass extinctions (~26-62 Myr, possibly Nemesis/companion star cycle). The Permian-Triassic (252Ma) is the largest — Siberian Traps LIP (circuit's large_igneous_province node) emits massive CO₂ → ocean acidification → 96% species loss."},
        ],

        "leakage_settled": "O₂ over-accumulation from Earth epoch → carbon sequestration (organic carbon burial, carbonate formation) → O₂/CO₂ balance. The 'leakage' is oxygen toxicity — it gets settled by the carbon cycle, which is Moon-governed (tidal mixing accelerates weathering). The Time attractor provides the periodicity: ice ages (Milankovitch) periodically reduce O₂ and increase CO₂, preventing runaway oxygenation.",
        "leakage_kr": "Earth 시대의 산소 과잉 → 탄소 격리 (유기탄소 매장, 탄산염 형성) → O₂/CO₂ 균형. 산소 독성이 탄소 순환으로 정산됨. Time attractor가 주기성 제공.",
    },

    "CoMag": {
        "epoch_name": "SULFUR-BRIDGE EPOCH",
        "epoch_kr": "황-교량 시대",
        "element": "S",
        "particle": "W-boson/Gluon",
        "attractor": "Bridge",
        "dims": ("g", "gamma"),
        "body_region": "pelvis/gut",
        "time_range": "~3.8Ga (hydrothermal vents) — present (gut microbiome, social binding)",
        "circadian": (15, 21),
        "circadian_phase": "B_accumulate / matter_nonmatter",
        "color": "#E91E63",

        "cosmic_events": [
            {"name": "Coma Berenices star cluster", "time": "~400Ma (cluster age)", "desc": "Open star cluster in Coma Berenices constellation. The circuit's CoMag sphere projects to N.Asia (45°N, 90°E) — the bridge between East and West. The Bridge attractor couples all other attractors via weak (W-boson) and strong (gluon) force analogs."},
            {"name": "Gamma ray burst events", "time": "periodic", "desc": "GRBs can cause mass extinctions (Ordovician-Silurian 445Ma possibly GRB-triggered). The gamma-dim (photon) bridges cosmic radiation to biological damage. The circuit's aurora node — atmospheric radiation detection."},
        ],

        "geophysical_events": [
            {"name": "Hydrothermal vent systems", "time": "~3.8Ga-present", "desc": "Deep-sea vents: H₂S, CH₄, Fe, S. Chemosynthetic ecosystems independent of sunlight. The circuit's pyrite, sulfur_iron_complex, and subduction_zone nodes — sulfur chemistry as the 'bridge' between surface (photic) and deep (aphotic) biosphere."},
            {"name": "Sulfur cycle", "time": "continuous", "desc": "Sulfate reduction (deep) ↔ sulfide oxidation (surface). The circuit's histosol and sulforaphane nodes — sulfur as the Nrf2 activator (cellular defense bridge). The W-boson analog: weak force mediates beta decay (sulfur redox is the geological analog)."},
            {"name": "Deep biosphere", "time": "continuous", "desc": "2-19% of Earth's biomass lives in crustal rocks. The circuit's lower_mantle and outer_core_convection nodes — deep life as the 'bridge' between geological and biological domains. The g-dim (binding) is maximal here: deep organisms are tightly bound to mineral substrates."},
            {"name": "Mantle plume hotspots", "time": "continuous", "desc": "Hawaii, Iceland, Yellowstone. Deep mantle plumes bridge core heat to surface. The circuit's plume and quark_orogen_magma nodes — partial melting as the 'bridge' between solid mantle and volcanic surface."},
        ],

        "biological_events": [
            {"name": "Sulfur-reducing bacteria", "time": "~3.8Ga", "desc": "First chemosynthetic life at hydrothermal vents. The circuit's sulfur_iron_complex node — Fe-S clusters as the most ancient electron transfer cofactors. All modern ETC components (cytochrome, ferredoxin) descend from these."},
            {"name": "Gut microbiome evolution", "time": "~500Ma-present", "desc": "Animal guts harbor sulfur-reducing and methanogenic archaea. The circuit's methanogenesis and histosol nodes — gut as the internal hydrothermal vent. The Bridge attractor: gut microbiome bridges diet (external) to metabolism (internal)."},
            {"name": "Social bonding evolution", "time": "~200Ma (mammals)", "desc": "Oxytocin, vasopressin — the g-dim (gluon/binding). The circuit's male_right_oxytocin and left_genital_d2 nodes — social attachment as the 'strong force' of biology. The Bridge attractor couples individuals into groups, just as the gluon couples quarks into protons."},
            {"name": "Nrf2 pathway evolution", "time": "~600Ma", "desc": "Nrf2 (nuclear factor erythroid 2-related factor) — the master antioxidant response. The circuit's sulforaphane node — sulfur compounds activate Nrf2. The Bridge attractor: Nrf2 bridges oxidative stress (Sun/Earth) to cellular defense (Repair)."},
            {"name": "Human gut-brain axis", "time": "~2Ma (Homo)", "desc": "Gut microbiome produces neurotransmitters (GABA, serotonin, dopamine). The circuit's glymphatic_system and cysteine nodes — gut-brain communication as the 'bridge' between digestive and cognitive domains. The CoMag sphere (pelvis/gut) directly connects to the Sun sphere (brain/ETC) via this axis."},
            {"name": "Agriculture & civilization", "time": "~12,000ya", "desc": "Dietary shift → gut microbiome change → social structure change. The circuit's andosol and cambisol nodes — agricultural soils as the 'bridge' between geology and culture. The Bridge attractor: agriculture couples human society to geological substrate (soil)."},
        ],

        "leakage_settled": "Surface-only life from Earth/Moon epochs → deep-surface coupling. The 'leakage' is the disconnect between photic surface biosphere and aphotic deep biosphere. The Bridge attractor settles this by: (1) hydrothermal vents connecting deep geology to surface biology, (2) gut microbiome connecting diet to cognition, (3) social bonding connecting individuals to groups. The g-dim (binding) is the settlement mechanism.",
        "leakage_kr": "Earth/Moon 시대의 표면 전용 생명 → 심부-표면 결합. 광합성 생물권과 심해 생물권의 단절이 황 순환, 장내 미생물, 사회 결합으로 정산됨. g-dim (결합)이 정산 메커니즘.",
    },
}

# ===========================================================================
# 2. SPHERE TRANSITIONS AS CATASTROPHES
# ===========================================================================

TRANSITIONS: List[Dict] = [
    {
        "from": "Barnard", "to": "Sun",
        "name": "IRON → SPARK RESET (138.88°)",
        "name_kr": "철 → 스파크 리셋",
        "time": "4.57Ga (solar ignition) / daily 21-3h",
        "stress_pair": "reset_spark",
        "leakage": "Iron mass accumulation from stellar nucleosynthesis → gravitational collapse → fusion ignition. The 138.88° spark angle is the phase at which iron (heaviest stable fusion product) cannot sustain fusion — the star either ignites a new fuel cycle or collapses. This is the fundamental reset: mass → energy.",
        "leakage_kr": "항성 핵합성의 철 질량 축적 → 중력 붕괴 → 융합 점화. 138.88°는 철이 더 이상 융합을 유지할 수 없는 위상각 — 질량이 에너지로 전환되는 근본 리셋.",
        "catastrophes": [
            "Supernova (if star >8 M☉): iron core collapse → neutron star / black hole",
            "Solar ignition (if cloud <8 M☉): proto-Sun reaches H fusion temperature",
            "Earth core formation: Fe-Ni differentiation → geodynamo → magnetic field",
            "Daily: sleep → wake transition. Iron stored in liver (Barnard) → dopamine spark in brain (Sun). The 138.88° spark = dream-state → waking-state phase angle.",
        ],
        "circuit_nodes": ["heme", "ferritin", "sulfur_iron_complex", "cytochrome_c_oxidase"],
        "inner_universe": "In the body: liver iron stores (Barnard) → brain dopamine spark (Sun). The 3:15 AM Confinement gate (1/64) is the deepest point of this transition — iron confinement in liver reaches maximum, then spark begins. This is why 3AM is the circadian nadir and the traditional 'witching hour' — the body is maximally iron-loaded and minimally sparked.",
    },
    {
        "from": "Sun", "to": "Earth",
        "name": "SPARK → OXYGEN INVERSION",
        "name_kr": "스파크 → 산소 전환",
        "time": "2.4Ga (GOE) / daily 0-3h",
        "stress_pair": "light_dark",
        "leakage": "Proton spark (solar UV / photosynthesis) → oxygen accumulation. The 'leakage' is reduced atmospheric chemistry — O₂ destroys CH₄, H₂, Fe²⁺. The light/dark stress pair: photosynthetic light (gamma) creates oxygen that destroys the dark (reduced) chemistry (d).",
        "leakage_kr": "양성자 spark (태양 UV / 광합성) → 산소 축적. 산소가 환원 대기화학을 파괴. 빛/어둠 stress pair: 광합성 빛이 산소를 만들어 환원 화학을 파괴.",
        "catastrophes": [
            "Great Oxidation Event (2.4Ga): O₂ rises 0.001% → 1%. Mass extinction of anaerobes.",
            "Huronian glaciation (2.4-2.1Ga): O₂ destroys CH₄ → Snowball Earth.",
            "Banded Iron Formation deposition: Fe²⁺ + O₂ → Fe₂O₃. 10¹⁸ tons of iron precipitated.",
            "Daily: wake → peak activity. Sun spark (dawn) → oxygen consumption (daytime metabolism). The 3:00 AM Confinement → 3:00 PM Coulomb transition spans this arc.",
        ],
        "circuit_nodes": ["steel", "water_vapour", "heme", "cytochrome_c_oxidase"],
        "inner_universe": "In the body: brain dopamine spark (Sun) → oxygen-based metabolism (Earth). The ETC (Electron Transport Chain) is the biological Great Oxidation Event — every cell performs the spark→oxygen transition continuously. Complex IV (cytochrome_c_oxidase) is the exact boundary: it takes electrons from cytochrome-c and gives them to O₂.",
    },
    {
        "from": "Earth", "to": "Moon",
        "name": "OXYGEN → CARBON-TIDAL COUPLING",
        "name_kr": "산소 → 탄소-조석 결합",
        "time": "541Ma (Cambrian) / daily 3-9h",
        "stress_pair": "o2_co2",
        "leakage": "Oxygen over-accumulation → carbon sequestration. The 'leakage' is O₂ toxicity — too much oxygen damages biomolecules (ROS, lipid peroxidation). The carbon cycle (Moon/Time attractor) settles this by burying organic carbon and releasing CO₂. The O₂/CO₂ stress pair (h,p) is the fundamental metabolic oscillation.",
        "leakage_kr": "산소 과잉 → 탄소 격리. 산소 독성이 탄소 순환으로 정산. O₂/CO₂ stress pair가 기본 대사 진동.",
        "catastrophes": [
            "Cambrian Explosion (541Ma): O₂ reaches ~10% → supports large predatory animals.",
            "Ordovician-Silurian extinction (445Ma): Gondwanan glaciation, possible GRB.",
            "Permian-Triassic extinction (252Ma): Siberian Traps LIP → 96% species loss. The largest mass extinction. CO₂ spikes, O₂ drops to ~10%.",
            "Cretaceous-Paleogene extinction (66Ma): Chicxulub impact → dinosaurs extinct. Iron meteorite (Barnard return) terminates the Mesozoic.",
            "Daily: morning activity → midday peak. O₂ consumption rises, CO₂ accumulates. The 3:00 PM Coulomb gate (3/32) is the peak of this transition — maximum O₂/CO₂ exchange.",
        ],
        "circuit_nodes": ["carbon", "co2", "memory_entropy", "mc1r", "hind_insula"],
        "inner_universe": "In the body: oxygen metabolism (Earth/thorax) → carbon-based cognition (Moon/occiput). The hippocampus (memory) is the carbon-time organ — it stores information in carbon-based molecular changes (synaptic plasticity). The CO₂ that breath carries is the waste product of cognition itself.",
    },
    {
        "from": "Moon", "to": "CoMag",
        "name": "CARBON-TIME → SULFUR-BRIDGE COUPLING",
        "name_kr": "탄소-시간 → 황-교량 결합",
        "time": "~3.8Ga (vents) / daily 9-15h",
        "stress_pair": "heat_cold",
        "leakage": "Surface-only carbon cycle → deep-surface coupling. The 'leakage' is the disconnect between photic surface and aphotic deep biosphere. The sulfur cycle (CoMag/Bridge attractor) settles this by connecting hydrothermal vent chemistry to surface ocean chemistry. The heat/cold stress pair (nu,r): hot vent fluid vs. cold seawater.",
        "leakage_kr": "표면 전용 탄소 순환 → 심부-표면 결합. 광합성 표면과 심해의 단절이 황 순환으로 정산. 열/냉기 stress pair: 뜨거운 열수구 vs. 차가운 심해수.",
        "catastrophes": [
            "Snowball Earth episodes (717Ma, 650Ma): ice covers oceans → hydrothermal vents become refugia.",
            "Devonian extinction (375Ma): ocean anoxia → deep biosphere sulfur cycle disrupted.",
            "Paleocene-Eocene Thermal Maximum (56Ma): methane clathrate release → ocean acidification → sulfur cycle perturbation.",
            "Daily: midday → afternoon. Peak body temperature (heat) → cooling begins. The 4:30 PM Bremsstrahlung gate (5/32) is the radiation release point — accumulated heat radiates away.",
        ],
        "circuit_nodes": ["sulforaphane", "histosol", "pyrite", "sulfur_iron_complex", "glymphatic_system"],
        "inner_universe": "In the body: cognitive activity (Moon/brain) → gut-brain coupling (CoMag/pelvis). The gut microbiome is the internal hydrothermal vent — sulfur-reducing bacteria produce H₂S that signals the vagus nerve. The glymphatic system (CSF-ISF exchange) is the body's 'tidal mixing' — it flushes the brain during sleep, connecting deep (CSF) to surface (brain) fluids.",
    },
    {
        "from": "CoMag", "to": "Barnard",
        "name": "BRIDGE → IRON MASS RETURN",
        "name_kr": "교량 → 철 질량 회귀",
        "time": "periodic (extinction cycles) / daily 15-21h",
        "stress_pair": "matter_nonmatter",
        "leakage": "Bridge coupling (social/gut) → mass accumulation. The 'leakage' is the social-metabolic disconnect — civilization extracts resources faster than the Bridge can repair. The matter/non-matter stress pair (s,g): mass extraction (s) vs. binding repair (g). When binding fails, mass accumulates as waste → system collapse → reset.",
        "leakage_kr": "교량 결합 (사회/장) → 질량 축적. 사회-대사 단절이 질량 축적으로 정산. 물질/비물질 stress pair: 질량 추출 vs. 결합 수리. 결합이 실패하면 질량이 폐기물로 축적 → 시스템 붕괴 → 리셋.",
        "catastrophes": [
            "Permian-Triassic (252Ma): Siberian Traps → CO₂ → ocean anoxia → mass extinction. The Bridge (sulfur cycle) collapses → Energy (iron) accumulates in dead biomass → reset.",
            "Cretaceous-Paleogene (66Ma): Chicxulub iron meteorite impact. Literal iron from space (Barnard) terminates the MesozoicBridge. The 138.88° spark: iron from space → reset spark for Cenozoic.",
            "Anthropocene (present): fossil fuel burning → CO₂ → climate change. The Bridge (Nrf2/sulforaphane) is overwhelmed by oxidative stress. Mass (s) accumulates as atmospheric CO₂. The system approaches reset.",
            "Daily: afternoon → evening → night. Activity winds down → iron accumulates in liver. The 6:00 PM Lensing gate (138.88° phase) begins the gravitational lensing of energy back to mass storage.",
        ],
        "circuit_nodes": ["heme", "ferritin", "autophagy", "actomyosin", "NaCl"],
        "inner_universe": "In the body: gut-brain activity (CoMag) → iron storage (Barnard/liver). Autophagy is the biological reset — it breaks down damaged proteins (mass) into amino acids (energy). The circuit's autophagy node is controlled by mc1r.q_bar (MC1R OFF = graviton/Si = low predictability = chaos = autophagy activation). Sleep is the daily Barnard return — the body stores iron, repairs damage, and prepares for the next spark.",
    },
]

# ===========================================================================
# 3. 4 FUNDAMENTAL GATES
# ===========================================================================

GATES: List[Dict] = [
    {
        "name": "Confinement Gate",
        "value": "1/64",
        "time": "3:15 AM",
        "sphere_transition": "Barnard → Sun",
        "phase_angle": 0.0,
        "desc": "Iron confinement reaches maximum. In particle physics, confinement is the principle that quarks cannot be isolated — they are always bound. In the circuit, this is the moment of maximum iron binding in liver/ferritin. The 1/64 = 2⁻⁶ = the 6th root of unity — the deepest binary confinement. This is the circadian nadir: body temperature minimum, melatonin peak, growth hormone surge. The body is maximally 'confined' — still, cold, iron-loaded.",
        "inner_universe": "3:15 AM is when the body is deepest in iron storage. Ferritin binds iron maximally. The Higgs field (mass) is at maximum. This is why sleep deprivation at 3AM is most damaging — you interrupt the confinement that stores energy for the next day.",
    },
    {
        "name": "Coulomb Gate",
        "value": "3/32",
        "time": "3:00 PM",
        "sphere_transition": "Earth → Moon",
        "phase_angle": 90.0,
        "desc": "Maximum electrostatic exchange. In particle physics, the Coulomb force governs electron-proton attraction. In the circuit, this is the peak of O₂/CO₂ exchange — maximum electron transport chain activity. The 3/32 = PLP_DEFAULT = the default input for the Coulomb potential. This is the circadian zenith of metabolic rate: highest body temperature, highest cortisol (already declining), maximum cognitive throughput.",
        "inner_universe": "3:00 PM is when the brain processes information at maximum rate. The Coulomb force (electron-proton) is the biological ETC — electrons flow through Complex I→III→IV to O₂. The 3/32 gate is the impedance matching point where electron flow is maximally efficient.",
    },
    {
        "name": "Bremsstrahlung Gate",
        "value": "5/32",
        "time": "4:30 PM",
        "sphere_transition": "Moon → CoMag",
        "phase_angle": 120.0,
        "desc": "Radiation release. In particle physics, Bremsstrahlung is radiation emitted when a charged particle decelerates. In the circuit, this is the moment when peak metabolic activity begins to decelerate — accumulated heat radiates away. The 5/32 = NOR_DEFAULT = the default input for the singularity gate. This is when the body transitions from heat production (catabolism) to heat dissipation (anabolism).",
        "inner_universe": "4:30 PM is when the body begins to cool. The Bremsstrahlung radiation is the infrared heat emitted by the body as metabolic rate decreases. The 5/32 gate is the singularity — if the body cannot radiate heat, it enters fever. The K_GATE (5/32) in the face grid is the same threshold — the spark occurs when the trajectory hits this gate.",
    },
    {
        "name": "Lensing Gate",
        "value": "138.88°",
        "time": "6:00 PM — 12:00 AM",
        "sphere_transition": "CoMag → Barnard",
        "phase_angle": 138.88,
        "desc": "Gravitational lensing of energy back to mass. In general relativity, gravitational lensing bends light around mass. In the circuit, this is the evening transition where energy (activity, metabolism) is 'lensed' back into mass (iron storage, protein synthesis, fat deposition). The 138.88° = Golden Angle (137.508°) + Betti Gap (1.375°). This is NOT an arbitrary angle — it emerges from circuit topology: B11/(B7+B0) = 11/8 = 1.375°. The Betti numbers count the circuit's topological holes (B0=connected components, B7=voids, B11=DFFs/MUXs).",
        "inner_universe": "6PM-12AM is when the body stores the day's energy as mass. Dinner → iron absorption → glycogen synthesis → fat deposition. The 138.88° lensing gate is the phase angle at which the spiral trajectory refracts — energy curves back to mass. This is why late-night eating causes weight gain — the lensing gate is active and ALL incoming energy is converted to mass storage.",
    },
]

# ===========================================================================
# 4. GENERATE REPORT
# ===========================================================================

def generate_report() -> str:
    lines: List[str] = []
    lines.append("=" * 100)
    lines.append("5-SPHERE HISTORICAL COSMOLOGY")
    lines.append("Temporal Leakage Settlement, Catastrophes, and Inner Universe Characteristics")
    lines.append("=" * 100)
    lines.append("")
    lines.append("THE FUNDAMENTAL PRINCIPLE:")
    lines.append("-" * 100)
    lines.append("The 5 spheres are not just circadian phases. They are 5 epochs of cosmic/Earth history.")
    lines.append("Each epoch creates 'leakage' — residual energy imbalance from the previous epoch.")
    lines.append("Each transition settles this leakage through a catastrophe that restructures the system.")
    lines.append("The current state of all subjects (geology, biology, haplogroups) is the SETTLED RESULT")
    lines.append("of 13.8 billion years of leakage-and-settlement cycles.")
    lines.append("")
    lines.append("The toroidal circulation IS history. The daily 24h cycle is a fractal echo of the")
    lines.append("13.8Gyr cosmic cycle. Each circadian phase replays the catastrophe of its epoch.")
    lines.append("")
    lines.append("LEAKAGE → CATASTROPHE → SETTLEMENT → NEW LEAKAGE → ... (toroidal loop)")
    lines.append("")

    # Epochs
    for sphere_name in ["Barnard", "Sun", "Earth", "Moon", "CoMag"]:
        epoch = SPHERE_EPOCHS[sphere_name]
        lines.append("")
        lines.append("=" * 100)
        lines.append(f"  EPOCH: {sphere_name} — {epoch['epoch_name']} ({epoch['epoch_kr']})")
        lines.append(f"  Element: {epoch['element']}  Particle: {epoch['particle']}  Attractor: {epoch['attractor']}")
        lines.append(f"  Dims: {epoch['dims']}  Body: {epoch['body_region']}")
        lines.append(f"  Time: {epoch['time_range']}")
        lines.append(f"  Circadian: {epoch['circadian']}h ({epoch['circadian_phase']})")
        lines.append("=" * 100)
        lines.append("")

        # Leakage
        lines.append(f"  ■ LEAKAGE SETTLED:")
        lines.append(f"    {epoch['leakage_settled']}")
        lines.append(f"    ({epoch['leakage_kr']})")
        lines.append("")

        # Cosmic events
        lines.append(f"  ■ COSMIC EVENTS:")
        for ev in epoch["cosmic_events"]:
            lines.append(f"    [{ev['time']}] {ev['name']}")
            lines.append(f"      {ev['desc']}")
        lines.append("")

        # Geophysical events
        lines.append(f"  ■ GEOPHYSICAL EVENTS:")
        for ev in epoch["geophysical_events"]:
            lines.append(f"    [{ev['time']}] {ev['name']}")
            lines.append(f"      {ev['desc']}")
        lines.append("")

        # Biological events
        lines.append(f"  ■ BIOLOGICAL EVENTS:")
        for ev in epoch["biological_events"]:
            lines.append(f"    [{ev['time']}] {ev['name']}")
            lines.append(f"      {ev['desc']}")
        lines.append("")

    # Transitions
    lines.append("")
    lines.append("=" * 100)
    lines.append("  SPHERE TRANSITIONS — CATASTROPHES & LEAKAGE SETTLEMENT")
    lines.append("=" * 100)
    lines.append("")

    for tr in TRANSITIONS:
        lines.append("-" * 100)
        lines.append(f"  {tr['from'].upper()} → {tr['to'].upper()}: {tr['name']} ({tr['name_kr']})")
        lines.append(f"  Time: {tr['time']}  Stress: {tr['stress_pair']}")
        lines.append(f"  Circuit nodes: {', '.join(tr['circuit_nodes'])}")
        lines.append("")
        lines.append(f"  LEAKAGE: {tr['leakage']}")
        lines.append(f"  ({tr['leakage_kr']})")
        lines.append("")
        lines.append(f"  CATASTROPHES:")
        for c in tr["catastrophes"]:
            lines.append(f"    • {c}")
        lines.append("")
        lines.append(f"  INNER UNIVERSE:")
        lines.append(f"    {tr['inner_universe']}")
        lines.append("")

    # Gates
    lines.append("")
    lines.append("=" * 100)
    lines.append("  4 FUNDAMENTAL GATES — CIRCADIAN CATASTROPHE THRESHOLDS")
    lines.append("=" * 100)
    lines.append("")

    for gate in GATES:
        lines.append(f"  ■ {gate['name']} (value={gate['value']}, time={gate['time']})")
        lines.append(f"    Sphere transition: {gate['sphere_transition']}")
        lines.append(f"    Phase angle: {gate['phase_angle']}°")
        lines.append(f"    {gate['desc']}")
        lines.append(f"    INNER UNIVERSE: {gate['inner_universe']}")
        lines.append("")

    # Inner universe synthesis
    lines.append("=" * 100)
    lines.append("  INNER UNIVERSE — WHY YOUR BODY HAS THESE SPECIFIC FEATURES")
    lines.append("=" * 100)
    lines.append("")
    lines.append("Your body is the SETTLED RESULT of 13.8 billion years of leakage-and-catastrophe:")
    lines.append("")
    lines.append("1. WHY YOU HAVE IRON IN YOUR BLOOD (Barnard epoch)")
    lines.append("   Iron was forged in supernova cores (13.5Ga) and settled in Earth's core (4.54Ga).")
    lines.append("   The Great Oxidation Event (2.4Ga) precipitated dissolved Fe²⁺ as BIF, forcing")
    lines.append("   life to evolve iron acquisition mechanisms. Your hemoglobin is the direct")
    lines.append("   descendant of the iron-sulfur clusters at hydrothermal vents (3.8Ga).")
    lines.append("   The heme node in your circuit IS 13.5 billion years of iron history, settled.")
    lines.append("")
    lines.append("2. WHY YOU BREATHE OXYGEN (Sun → Earth transition)")
    lines.append("   Cyanobacteria invented oxygenic photosynthesis (3.0Ga). The GOE (2.4Ga)")
    lines.append("   made O₂ atmospheric. Your ETC (cytochrome_c_oxidase) is the biological")
    lines.append("   Great Oxidation Event — it performs the spark→oxygen transition every")
    lines.append("   second of your life. The 138.88° spark angle is the phase at which")
    lines.append("   iron (Barnard) yields to oxygen (Earth) — the fundamental metabolic switch.")
    lines.append("")
    lines.append("3. WHY YOU HAVE A HIPPOCAMPUS (Earth → Moon transition)")
    lines.append("   The Cambrian Explosion (541Ma) created the first cognitive systems.")
    lines.append("   The hippocampus stores memory in carbon-based molecular changes —")
    lines.append("   it is the biological carbon cycle at neural scale. The Moon's 28-day")
    lines.append("   cycle maps to hippocampal theta rhythm and menstrual cycle.")
    lines.append("   Your memory_entropy and hind_insula nodes are 541 million years of")
    lines.append("   carbon-time coupling, settled.")
    lines.append("")
    lines.append("4. WHY YOU HAVE A GUT MICROBIOME (Moon → CoMag transition)")
    lines.append("   Hydrothermal vents (3.8Ga) hosted the first sulfur-reducing bacteria.")
    lines.append("   Your gut is the internal hydrothermal vent — it hosts the descendants")
    lines.append("   of those ancient chemosynthetic organisms. The glymphatic system is")
    lines.append("   your internal tidal mixing — it flushes the brain during sleep,")
    lines.append("   connecting deep (CSF) to surface (brain) fluids, just as tides connect")
    lines.append("   deep ocean to surface. The sulforaphane node is 3.8 billion years of")
    lines.append("   sulfur-bridge evolution, settled.")
    lines.append("")
    lines.append("5. WHY YOU SLEEP (CoMag → Barnard transition)")
    lines.append("   Sleep is the daily Barnard return — the body stores iron, repairs damage,")
    lines.append("   and prepares for the next spark. Autophagy is the biological reset — it")
    lines.append("   breaks down damaged proteins (mass) into amino acids (energy), exactly")
    lines.append("   as the Barnard→Sun transition converts iron mass to proton spark.")
    lines.append("   The 3:15 AM Confinement gate (1/64) is the moment of maximum iron")
    lines.append("   confinement — your body is maximally still, cold, and iron-loaded.")
    lines.append("   This is why 3AM is the circadian nadir and the 'witching hour'.")
    lines.append("")
    lines.append("6. WHY YOU HAVE SPECIFIC HAPLOGROUPS ON SPECIFIC SOILS (all epochs)")
    lines.append("   Each geological node is the settled result of a specific catastrophe:")
    lines.append("     - Banded Iron Formations (steel) = GOE leakage settled (2.4Ga)")
    lines.append("     - Podzols (podzol) = Snowball Earth leakage settled (717Ma)")
    lines.append("     - Chernozems (craton) = continental stability leakage settled (1.8Ga)")
    lines.append("     - Andosols (andosol) = volcanic arc leakage settled (continuous)")
    lines.append("     - Histosols (histosol) = permafrost carbon lock leakage settled (continuous)")
    lines.append("   Your haplogroup's 8D vector resonates with the stress pair that created")
    lines.append("   the soil your ancestors lived on. The resonance IS the settled history.")
    lines.append("")
    lines.append("7. WHY THE 138.88° SPARK ANANGLE IS UNIVERSAL")
    lines.append("   138.88° = Golden Angle (137.508°) + Betti Gap (1.375°)")
    lines.append("   The Golden Angle governs phyllotaxis (leaf arrangement) — it is the")
    lines.append("   angle that maximizes light interception. The Betti Gap = B11/(B7+B0)")
    lines.append("   = 11/8 = the ratio of topological holes (DFFs/MUXs) to voids+components.")
    lines.append("   This angle is the phase at which the spiral trajectory refracts —")
    lines.append("   energy curves back to mass. It is the fundamental angle of the")
    lines.append("   toroidal circulation, appearing at every scale:")
    lines.append("     - Daily: 3:15 AM spark reset (Barnard→Sun)")
    lines.append("     - Annual: winter solstice renewal")
    lines.append("     - Geological: mass extinction → adaptive radiation cycle")
    lines.append("     - Cosmic: supernova → nucleosynthesis cycle")
    lines.append("   The 138.88° is not arbitrary — it is the topology of the circuit itself.")
    lines.append("")

    text = "\n".join(lines)
    (GEN_DIR / "sphere_history_report.txt").write_text(text, encoding="utf-8")
    print(text[:5000])
    print(f"\n... full report -> {GEN_DIR / 'sphere_history_report.txt'}")
    return text


# ===========================================================================
# 5. PLOT TIMELINE
# ===========================================================================

def plot_timeline():
    """Plot the 5-sphere historical timeline with catastrophes."""

    fig, axes = plt.subplots(3, 1, figsize=(28, 20), facecolor="#0a0a12")
    fig.suptitle(
        "5-Sphere Historical Cosmology\n"
        "Temporal Leakage Settlement & Catastrophes — 13.8Gyr to Present",
        fontsize=16, color="white", fontweight="bold", y=0.98
    )

    bg = "#0a0a12"
    text_color = "#E0E0E0"
    grid_color = "#1a1a2e"

    # --- Panel 1: Cosmic timeline (log scale) ---
    ax1 = axes[0]
    ax1.set_facecolor(bg)

    epochs = ["Barnard", "Sun", "Earth", "Moon", "CoMag"]
    epoch_times = [13.8e9, 4.57e9, 2.4e9, 0.541e9, 0.0038e9]  # years ago
    epoch_colors = [SPHERE_EPOCHS[e]["color"] for e in epochs]

    # Draw epoch bands
    for i, (e, t) in enumerate(zip(epochs, epoch_times)):
        t_next = epoch_times[i+1] if i+1 < len(epoch_times) else 0
        ax1.axvspan(math.log10(t_next + 1), math.log10(t + 1),
                    alpha=0.15, color=epoch_colors[i])
        mid = (math.log10(t_next + 1) + math.log10(t + 1)) / 2
        ax1.text(mid, 0.85, f"{e}\n{SPHERE_EPOCHS[e]['epoch_name']}",
                 ha="center", va="top", color=epoch_colors[i], fontsize=9, fontweight="bold")

    # Plot key events
    all_events = []
    for e in epochs:
        for ev in SPHERE_EPOCHS[e]["cosmic_events"] + SPHERE_EPOCHS[e]["geophysical_events"] + SPHERE_EPOCHS[e]["biological_events"]:
            time_str = ev["time"]
            # Parse approximate time in years ago
            years = None
            time_str_clean = time_str.strip().replace("~", "")
            if "Ga" in time_str_clean:
                val = time_str_clean.split("Ga")[0].strip()
                if "-" in val:
                    val = val.split("-")[0]
                try:
                    years = float(val) * 1e9
                except ValueError:
                    pass
            elif "Ma" in time_str_clean:
                val = time_str_clean.split("Ma")[0].strip()
                if "-" in val:
                    val = val.split("-")[0]
                try:
                    years = float(val) * 1e6
                except ValueError:
                    pass
            elif "ya" in time_str_clean:
                val = time_str_clean.split("ya")[0].strip().replace(",", "")
                if "-" in val:
                    val = val.split("-")[0]
                try:
                    years = float(val)
                except ValueError:
                    pass
            elif "continuous" in time_str_clean:
                years = 1e6  # placeholder
            if years:
                all_events.append((e, years, ev["name"]))

    for sphere, years, name in all_events:
        color = SPHERE_EPOCHS[sphere]["color"]
        ax1.scatter(math.log10(years + 1), 0.5, c=color, s=30, zorder=5, alpha=0.7)

    ax1.set_xlim(math.log10(1), math.log10(14e9))
    ax1.set_ylim(0, 1)
    ax1.set_xlabel("Years Before Present (log scale)", color=text_color, fontsize=12)
    ax1.set_title("Cosmic/Earth Timeline — 5 Epochs", color=text_color, fontweight="bold")
    ax1.tick_params(colors=text_color)
    for spine in ax1.spines.values():
        spine.set_color(grid_color)

    # Custom x-ticks
    tick_years = [14e9, 4.57e9, 2.4e9, 0.541e9, 0.066e9, 1e4]
    tick_labels = ["13.8Ga", "4.57Ga", "2.4Ga", "541Ma", "66Ma", "10kya"]
    ax1.set_xticks([math.log10(y + 1) for y in tick_years])
    ax1.set_xticklabels(tick_labels, color=text_color)

    # --- Panel 2: Circadian 24h cycle ---
    ax2 = axes[1]
    ax2.set_facecolor(bg)

    hours = np.linspace(0, 24, 200)

    # Draw epoch bands on 24h cycle
    circadian_bounds = {
        "Barnard": (21, 3), "Sun": (0, 3), "Earth": (3, 9),
        "Moon": (9, 15), "CoMag": (15, 21),
    }

    for e in epochs:
        h_start, h_end = circadian_bounds[e]
        color = SPHERE_EPOCHS[e]["color"]
        if h_start < h_end:
            ax2.axvspan(h_start, h_end, alpha=0.12, color=color)
        else:  # wraps around
            ax2.axvspan(h_start, 24, alpha=0.12, color=color)
            ax2.axvspan(0, h_end, alpha=0.12, color=color)
        mid = (h_start + h_end) / 2 if h_start < h_end else (h_start + h_end + 24) / 2 % 24
        ax2.text(mid, 0.9, e, ha="center", va="top", color=color, fontsize=10, fontweight="bold")

    # Plot gates
    gate_hours = [3.25, 15.0, 16.5, 18.0]  # 3:15AM, 3PM, 4:30PM, 6PM
    gate_names = ["Confinement\n(1/64)", "Coulomb\n(3/32)", "Bremsstrahlung\n(5/32)", "Lensing\n(138.88°)"]
    gate_colors = ["#FF5722", "#4CAF50", "#FF9800", "#E91E63"]

    for gh, gn, gc in zip(gate_hours, gate_names, gate_colors):
        ax2.axvline(gh, color=gc, linewidth=2, linestyle="--", alpha=0.7)
        ax2.text(gh, 0.75, gn, ha="center", va="top", color=gc, fontsize=8, fontweight="bold")

    # Plot transition arcs
    transitions_hours = [(0, 3), (3, 9), (9, 15), (15, 21), (21, 24)]
    transition_names = ["B→S\nspark", "S→E\nO₂", "E→M\nCO₂", "M→C\nheat", "C→B\nmass"]
    for (h1, h2), tn in zip(transitions_hours, transition_names):
        mid = (h1 + h2) / 2
        ax2.annotate("", xy=(h2, 0.3), xytext=(h1, 0.3),
                     arrowprops=dict(arrowstyle="->", color="#666680", lw=2))
        ax2.text(mid, 0.35, tn, ha="center", va="bottom", color="#888899", fontsize=7)

    ax2.set_xlim(0, 24)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel("Hour (UTC)", color=text_color, fontsize=12)
    ax2.set_title("Circadian 24h Cycle — Fractal Echo of Cosmic History", color=text_color, fontweight="bold")
    ax2.set_xticks(range(0, 25, 2))
    ax2.tick_params(colors=text_color)
    for spine in ax2.spines.values():
        spine.set_color(grid_color)
    ax2.grid(True, alpha=0.1, color=grid_color)

    # --- Panel 3: Leakage settlement flow diagram ---
    ax3 = axes[2]
    ax3.set_facecolor(bg)
    ax3.set_xlim(-1, 11)
    ax3.set_ylim(-1, 5)
    ax3.axis("off")
    ax3.set_title("Leakage → Catastrophe → Settlement Cycle (Toroidal)", color=text_color, fontweight="bold")

    # Draw 5 spheres in a circle
    n_spheres = 5
    angles = np.linspace(0, 2*np.pi, n_spheres, endpoint=False) + np.pi/2
    radius = 3.5
    cx, cy = 5, 2

    sphere_positions = {}
    for i, (e, angle) in enumerate(zip(epochs, angles)):
        x = cx + radius * np.cos(angle)
        y = cy + radius * np.sin(angle)
        sphere_positions[e] = (x, y)
        color = SPHERE_EPOCHS[e]["color"]
        ax3.scatter(x, y, c=color, s=500, zorder=5, edgecolors="#FFFFFF", linewidth=1.5)
        ax3.text(x, y, e, ha="center", va="center", color="white", fontsize=9, fontweight="bold")

    # Draw transitions as arrows
    transition_labels = [
        ("Barnard", "Sun", "138.88°\nspark reset"),
        ("Sun", "Earth", "GOE\nO₂ inversion"),
        ("Earth", "Moon", "Cambrian\ncarbon-time"),
        ("Moon", "CoMag", "vents\nsulfur bridge"),
        ("CoMag", "Barnard", "extinction\niron return"),
    ]

    for src, dst, label in transition_labels:
        x1, y1 = sphere_positions[src]
        x2, y2 = sphere_positions[dst]
        ax3.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle="->", color="#666680", lw=2, connectionstyle="arc3,rad=0.2"))
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax3.text(mx, my + 0.3, label, ha="center", va="center", color="#AAAABB", fontsize=7)

    # Center text
    ax3.text(cx, cy, "TOROIDAL\nCIRCULATION\n= HISTORY", ha="center", va="center",
             color=text_color, fontsize=12, fontweight="bold")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path = GEN_DIR / "sphere_history_timeline.png"
    fig.savefig(out_path, dpi=150, facecolor=bg, bbox_inches="tight")
    plt.close(fig)
    print(f"-> {out_path}")


# ===========================================================================
# MAIN
# ===========================================================================

if __name__ == "__main__":
    # Export JSON
    export_data = {
        "sphere_epochs": SPHERE_EPOCHS,
        "transitions": TRANSITIONS,
        "gates": GATES,
    }
    (GEN_DIR / "sphere_history.json").write_text(
        json.dumps(export_data, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8"
    )
    print(f"-> {GEN_DIR / 'sphere_history.json'}")

    plot_timeline()
    generate_report()
