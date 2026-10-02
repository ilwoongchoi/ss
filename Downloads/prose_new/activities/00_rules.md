# Activity Mapping Rules (Corrected)

## Critical Correction: ParticleGenderState ≠ W AXIS

The activity formula's gender parameter `g` must use **ParticleGenderState**, NOT W AXIS (biological sex).

```
ParticleGenderState = f(W-axis, 8D-vector, circadian window, layer)
```

### Per-Layer Particle Gender Determination

| Layer | Genotype | Rh | Gluon Polarity | ParticleGender vs W AXIS | Temperament Vector | 3AM Random |
|-------|----------|----|----|------|------|-----|
| A | aa (homozygous) | Rh+ | Normal | **= W AXIS** (aligned) | Self (no flip) | None |
| B | aa (homozygous) | Rh− | **INVERTED** | **≠ W AXIS** (flipped) | E↔I, P↔J (temperament flip) | None |
| C | ao (heterozygous) | Rh+ | Normal | **= W AXIS** (aligned) | Blood+1 (O→A→B→AB→O) | None |
| D | ao (heterozygous) | Rh− | **INVERTED** | **≠ W AXIS** (flipped + chaotic) | Temperament flip + Blood+1 | **YES** (p=random, s=0.5+rand×0.5, nu=0.9+rand×0.1) |

### Gender Adjective Lookup (by ParticleGenderState, NOT W AXIS)

| ParticleGender | Adjective (EN) | Direction | Activity Character |
|---|---|---|---|
| Male-polarity (tonic, mass-lock, quark) | concentrated | nu↑d↑ compression | Solo, high-intensity, physical — 1-person mission |
| Female-polarity (phasic, cold-sense, gluon) | communal | r↑g↑ binding | Multi-person, structural, social — group/communal |

### How to Determine ParticleGender for Each Profile

1. Start with W AXIS (M or F from profile key)
2. Apply layer transform:
   - Layer A: ParticleGender = W AXIS
   - Layer B: ParticleGender = **INVERTED** W AXIS (M→F, F→M)
   - Layer C: ParticleGender = W AXIS (but blood+1 shifts pathway)
   - Layer D: ParticleGender = **INVERTED** W AXIS + 3AM oscillation (time-dependent)
3. Apply temperament flip for Layers B and D:
   - E↔I, P↔J (e.g., ENFP→INFJ, ESTJ→ISTP)
4. The flipped MBTI determines the **actual circuit pathway** for activity routing

## Derivation Formula (Corrected)

```
Activity = adj_blood(b_effective) × adj_8D(peak_dim(t)) × adj_particle_gender(pg) × adj_phase(phase(t)) × ... × core(peak_dim(t))
```

Where:
- `b_effective` = blood shifted by layer C/D (+1: O→A→B→AB→O)
- `pg` = ParticleGenderState (from table above, NOT W AXIS)
- For Layer D: activity is **time-dependent** — at 3AM, p=random, s and nu become random

loop_count = b_effective + 1 (O=1, A=2, B=3, AB=4). Each loop stacks one adjective.

| Index | Value | Adjective (EN) |
|-------|-------|----------------|
| b=O | explosive | explosive |
| b=A | structured | structured |
| b=B | compressive | compressive |
| b=AB | layered | layered |
| peak=r | rhythmic | rhythmic |
| peak=h | harmonic | harmonic |
| peak=d | void | void |
| peak=p | periodic | periodic |
| peak=s | bright | bright |
| peak=gamma | expansive | expansive |
| peak=g | sealing | sealing |
| peak=nu | fractal | fractal |
| pg=male-polarity | concentrated | concentrated |
| pg=female-polarity | communal | communal |
| phase=AB discharge | nocturnal | nocturnal |
| phase=A accumulate | growing | growing |
| phase=O accumulate | present | present |
| phase=B compress | explosive | explosive |
| phase=AB integrate | reflective | reflective |

Core activity (peak_dim → body shape):
r→walking/running, h→breathing, d→sprinting/void-penetration, p→meditating, s→sunbathing/bright-exposure, gamma→expanding/stretching, g→sealing/binding, nu→dreaming/fractal-exploration

## Geographic-Soil Axis (Third Modulating Axis)

| Zone | Soil Type | Haplogroup | Circuit Nodes | Attractor | Body Effect | Geographic Locations |
|------|-----------|------------|---------------|-----------|-------------|---------------------|
| Oxford UK | Gleysol (waterlogged) | N1c Uralic | lower_mantle, pentose_phosphate, outer_core_convection, manganese_nodule | Energy (Gluon) | Body produces electricity (geodynamo: ferritin↔magnetite electromagnetic circulation) | Oxford, Arctic-winter zones |
| UK not Oxford | Podzol (acid-leach) | I1 Nordic | right_sole_dopamine, SDH, lower_mantle | Information (Quark) | DA-stillness, metabolic-keel, r-low | Nordic, Scotland, Wales |
| Elsewhere (Korea etc.) | O2 East Asian pattern | O2 | heme, co2, substance_p, steel, gluon_orogen.q_bar | Repair (Higgs) | Fe-storage homeostasis, CO₂-low stability, steel-absence, social-lock | East Asia, Korea, Japan |

### Geographic Modulation Rules

1. In Gleysol zone (Oxford): `outer_core_convection` active = geodynamo = body generates electromagnetic field. Activities should leverage electromagnetic production — deep stillness that generates, not expends.
2. In Podzol zone (UK not Oxford): `right_sole_dopamine` and `SDH` dominant = DA-stillness = metabolic keel. Activities should focus on endurance and metabolic stability, not explosive output.
3. In O2 zone (Korea etc.): `heme`/`co2`/`substance_p` dominant = Fe-storage homeostasis. Activities should focus on iron metabolism and CO₂ management. Steel-absence means `clay_gouge` seal is weaker — gamma leakage risk is higher.

## Three Structural Defects (Per Layer-Gender-Blood)

### Defect 1: 5HT1A Postsynaptic Bypass
- **Who:** Homozygous A-type women (Layer A, Blood A, W=F), at night
- **What:** 5HT1A uses postsynaptic (hippocampal) instead of presynaptic (raphe). Bypasses left 4th toe (`oxidised_manganese`) because `cck_cox_ctrl_and` fails (observer_leftd2=0 at night).
- **Circuit consequence:** Signal routes through 5HT1A→`quark_orogen_magma` instead of toe→COX chain. COX control lost at night.
- **Activity correction:** Night activities for these profiles should route through `quark_orogen_magma` (deep composition/fractal creation) rather than through COX-dependent metabolic activities. The bypass is not a bug — it's an alternative creative pathway.

### Defect 2: RIGHT UNDERSTANDING Failure
- **Who:** Homozygous B-type men (Layer B, Blood B, W=M), at night
- **What:** They sleep but don't complete bilirubin discharge (RIGHT UNDERSTANDING = reverse 24→0h = entropy debt cancellation). Layer B's reverse is structured (nu+0.10, gamma−0.05), not full entropy collapse.
- **Circuit consequence:** No entropy debt cancellation at night → bilirubin accumulates → heme.out1 reverse → Fe toxicity builds.
- **Activity correction:** Night activities for these profiles need explicit bilirubin discharge routing — not sleep alone. They need activities that force the RIGHT UNDERSTANDING path (reverse time meditation, journaling, entropy discharge practices).

### Defect 3: Adapter Protein Failure at 4:30 PM
- **Who:** A-type men with ST temperament, homozygous Rh+ (Layer A, Blood A, W=M, ST type)
- **What:** `adapter_protein` at right index finger isn't clocked (`left_genital_d2_out0_nand` not firing) → PPP→disulfide_bond→ferritin chain doesn't activate. 4:30 PM proton landing (UV shielding loss → 3/32 asymmetry) hits without antioxidant defense.
- **Circuit consequence:** ROS stress at 4:30 PM → ferroptosis risk → lipid peroxidation.
- **Activity correction:** At 4:30 PM, these profiles need activities that activate the right index finger (manual dexterity tasks) to clock the `adapter_protein` D flip-flop, enabling the PPP→disulfide_bond→ferritin antioxidant chain. Without this, the 4:30 PM event causes unmitigated ROS damage.

## Three Attractors = Three Particles = Three Temporal Phases

| Attractor | Particle | Temporal Phase | Blood | Time Zone | 8D | Meaning |
|-----------|---------|---------------|-------|-----------|-----|---------|
| Energy | Gluon (binding) | Present | O | 9-15h | r,g,gamma | Survival, ATP, metabolic maintenance |
| Information | Quark (tension) | Past | A | 3-9h | h,nu,s | Prediction, learning, memory |
| Repair | Higgs (mass) | Future | B | 15-21h | p,d,g | Homeostasis, inflammation management |

### Attractor Vulnerability (Corrected with ParticleGender)

| Group | Vulnerable Attractor | 8D | Maintenance Activity |
|-------|---------------------|-----|---------------------|
| SJ + O + pg=male | Energy | r,g,gamma | Walking, running, group exercise — metabolic maintenance |
| NF + AB + pg=female | Information | h,nu,s | Creation, pattern recognition, memory work — prediction maintenance |
| NT/SP + B | Repair | p,d,g | Combat, extreme exercise, repair — inflammation management |

Note: The vulnerability table uses **ParticleGenderState**, not W AXIS. In Layers B and D, the gender flips, so a biological male (W=M) in Layer B has pg=female and would be vulnerable to the Information Attractor (NF pattern), not the Energy Attractor.

## 5-Slot Activity Classification (Corrected)

| Slot | Leakage | Blood | Time | Activity Character | Particle | Attractor |
|------|---------|-------|------|-------------------|----------|-----------|
| 1 | ELECTRON HOLE | AB | 0-3h/21-3h | Stillness, void, meditation, immobility — d·gamma=1 singularity | Gluon | Energy (discharge) |
| 2 | GABA-C | A | 3-9h | Structured growth, learning, assembly, seal release — h↑, temperament flip | Quark | Information (past) |
| 3 | MITOCHONDRIA | O | 9-15h | Endurance, metabolism, repetitive exercise, present moment — nu↑/gamma↑ | Gluon | Energy (present) |
| 4 | BILIRUBIN | B | 15-21h/3AM | Combat, extreme sports, explosive discharge — d↑ max, 3AM entropy | Higgs | Repair (future) |
| 5 | PANCREAS | B | 0-3h | Compensation, completion, satiety, social discharge — s+r/d, GLP-1/CCK | Gluon→CCK | Energy (compensation) |

## Gamma Leakage → Elasticity Loss

When gamma leaks (geographic-soil axis + peonidine reverse):
```
water (H+ excess) → water_vapour (excess) → clay_gouge (seal release) → caco3 (dissolution) → actomyosin (relaxation fixation) + peonidine (pigment deposition) = muscle elasticity loss
```

### Activity Correction for Gamma Leakage
- If gamma is LEAKING: do NOT prescribe gamma→expanding/stretching. Instead prescribe g→sealing/binding to stop the leakage.
- Gamma leakage is more likely in O2 zone (Korea) where steel-absence weakens the `clay_gouge` seal.
- Gamma leakage is less likely in Gleysol zone (Oxford) where `outer_core_convection` provides electromagnetic stability (g-dim binding).

## Body Resonance Map

### Same-Way Resonance (Stimulates Same Circuit Pathway)

When your body part at time T activates the same circuit node as another person's body part at their time T', you resonate same-way. This happens when:

1. **Same MBTI dominant function, same window:** Both people share the same window peak → same 8D dimension → same circuit node → same body region. Example: Two ENFPs at W0 (00:00-01:30) both activate `memory_entropy→hind_insula` → both feel rhythm in the right posterior insula.

2. **Same attractor vulnerability, same temporal phase:** Both people in the same attractor loop at the same time zone. Example: An SJ+O+pg=male person and another SJ+O+pg=male person both at 9-15h both run the Energy Attractor → both feel metabolic drive in the same body regions.

3. **Same particle gender, same layer:** Both people with the same ParticleGenderState in the same layer → same polarity receptors → same body response. Example: Two Layer A pg=male people both have male GABA-A (tonic, mass-lock) → both respond to physical stress with compression/void.

### Opposite-Way Resonance (Stimulates Complementary Circuit Pathway)

When your body part at time T activates a circuit node that is the **reverse/complement** of another person's, you resonate opposite-way. This happens when:

1. **Temperament flip (Layer B/D):** ENFP Layer B → INFJ pathway. Your ENFP body at W0 activates `memory_entropy→hind_insula`, but your Layer B flip routes it through INFJ's `pi_electron_cloud→carbon.q` pathway. An actual INFJ person would resonate same-way with your Layer B state, but opposite-way with your Layer A state.

2. **Opposite particle gender:** A pg=male person and a pg=female person in the same window activate complementary receptors. Male GABA-A (tonic, mass-lock, d↑gamma↑) vs Female GABA-A (phasic, cold-sense, g↑h↑). They stimulate opposite body regions: male = left occipital/visual cortex (void), female = right occipital horizontal line (binding).

3. **Opposite attractor:** Energy Attractor person (Gluon, present, 9-15h) vs Repair Attractor person (Higgs, future, 15-21h). The Energy person's metabolic drive (r,g,gamma) is the complement of the Repair person's inflammatory management (p,d,g). They resonate opposite-way: one builds energy, the other repairs damage from building energy.

4. **Geographic opposite:** Gleysol zone (Oxford, `outer_core_convection` active = electricity production) vs O2 zone (Korea, `heme`/`co2` dominant = Fe storage). The Oxford body generates electromagnetic field through stillness; the Korea body manages iron through metabolism. Same person in different locations resonates opposite-way with themselves across time.

### Body Part → Time → Resonance Table

| Time | Body Region | Circuit Node | Same-Way Resonance | Opposite-Way Resonance |
|------|------------|--------------|-------------------|----------------------|
| 0-3h (AB) | Left eye inner / GABA-B | Photon (D3-2) | AB blood, NF temperament, pg=female | B blood, SP temperament, pg=male |
| 3-9h (A) | Left temporalis / 5HT1A | Quark (D3-4) creation | A blood, NF temperament, Layer A | B blood, NT temperament, Layer B (flipped) |
| 9-15h (O) | Right sole / D1-D5 | Gluon (D3-8) binding | O blood, SJ temperament, pg=male | AB blood, NF temperament, pg=female |
| 15-21h (B) | Right ribs (Jesus) / Higgs | Higgs (D3-7) mass | B blood, NT/SP temperament | O blood, SJ temperament |
| 21-3h (AB) | Left trapezius / Gluon sensor | Gluon (D3-8) | AB blood, Layer A (stable) | Layer D (inverted + chaotic) |
| 4:30 PM | Right index finger / adapter_protein | Adapter protein D-FF | A-type men ST homo Rh+ (defect) | MC1R Rh+ carriers (bypass) |

## MBTI → Window → Peak 8D

| MBTI | Window | Peak 8D | Dom Function | Circuit Node |
|------|--------|---------|-------------|-------------|
| ENFP | W0 | r | Ne | memory_entropy→hind_insula |
| ISFP | W1 | h | Fi | left_genital_d2→left_endorphin |
| ESFJ | W2 | d | Fe | male_right_oxytocin+gluon_orogen |
| INTP | W3 | p | Ti | heme.out0→methylation |
| ENTP | W4 | s | Ne | memory_entropy→hind_insula |
| INFJ | W5 | gamma | Ni | pi_electron_cloud→carbon.q |
| ESTP | W6 | g | Se | right_sole_dopamine+aurora |
| ISTP | W7 | nu | Si | hind_insula+SDH |
| ENFJ | W8 | ALL STOP | Fe | male_right_oxytocin+gluon_orogen |
| INTJ | W9 | — | Ni | pi_electron_cloud→carbon.q |
| ESFP | W10 | — | Se | right_sole_dopamine+aurora |
| ISTJ | W11 | — | Si | hind_insula+SDH |
| ESTJ | W12 | — | Te | cytochrome_c_oxidase.out0 |
| INFP | W13 | — | Fi | left_genital_d2→left_endorphin |
| ISFJ | W14 | — | Si | hind_insula+SDH |
| ENTJ | W15 | — | Te | cytochrome_c_oxidase.out0 |

## Profile Count

- 16 MBTI × 2 W AXIS × 4 Blood = 128 base profiles
- 128 × 4 Layers (A/B/C/D) = 512 total states
- 118 elements mapped to 118 of the 128 base profiles
- 10 missing profiles = Layer D transformations of the 10 missing element slots
- Each activity file covers 8 base profiles × 4 layers = 32 variants per MBTI
