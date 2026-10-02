# 09 — Musical State Specification (8D → Composition Engine)

Source: `universe-prose.md:140-209`. This is the bridge between 8D parameters and actual musical output — the composition engine that `08_music_theory_readapt.md`'s mappings feed into.

---

## 1. Musical State Specification (8D → Intent Vector)

Each tile is not a raw 8D vector — it is converted to 9 "composition intent" variables. These are the inputs to the Form/Cadence Automaton and Role selection.

| State | Range | Definition | 8D Inputs | Circuit Grounding |
|-------|-------|------------|-----------|--------------------|
| `closure` | 0–1 | seal/completion degree | g (binding) · 0.5 + p (predictability) · 0.3 + NAND_LOW?0.2:0 | glymphatic_system / caco3 / MC1R |
| `tension` | 0–1 | tension/dissonance | d · 0.5 + (1−p) · 0.3 + h · 0.2 | cytochrome_c_oxidase.out1 / HO-1 ETC |
| `motion` | 0–1 | motion/drive | r · 0.6 + p · 0.4 | r-dim (Complex IV), DRD2 tonic |
| `brightness` | 0–1 | brightness/high-freq energy | s · 0.7 + gamma · 0.3 | right_sole_dopamine, steel |
| `space` | 0–1 | spatial/reverb | gamma · 0.7 + (1−g) · 0.3 | steel / plume / fold_belt |
| `recurrence` | 0–1 | pattern repeat depth | nu · 0.6 + p · 0.4 | lower_mantle / disulfide_bond |
| `density` | 0–1 | layer/binding density | g · 0.7 + r · 0.3 | water_vapour / clay_gouge |
| `direction` | −1…+1 | ascending(+)/descending(−) | (h−d) · 0.7 + (nand.isBoundary?0:0.3) | histosol vs cytochrome_c_oxidase.out1 |
| `cadenceEligibility` | 0–1 | cadence permission index | closure · 0.5 + (1−tension) · 0.3 + recurrence · 0.2 | MC1R latch, memory_entropy |

> All calculations are deterministic hash-based smoothed. No `Math.random()`.

---

## 2. Form / Cadence Automaton (MC1R + LeftD2 + memory_entropy)

1. **Cadence Index**
   `C = w_c·closure + w_r·(1−tension) + w_n·recurrence`
2. **Cadence Latch (MC1R)**
   `q = hysteresis(C − θ_cadence)` → cadence permitted
   `q̄ = 1 − q` → cadence forbidden
3. **Suspend Trigger (Disulfide Boundary)**
   `S = NAND_boundary · smooth(s) · smooth(gamma)`
4. **Priority**
   - if `S > θ_suspend` → Role = `suspend`
   - else if `q > θ_resolve` → Role = `resolve`
   - else → Role = argmax(roleScore)

---

## 3. Role Grammar (7 Roles)

| Role | Chords | Bass | Melody | Rhythm | Arrangement |
|------|--------|------|--------|--------|-------------|
| Establish | I only | Root pedal | tonic arpeggio | quarter pulse | pad off, lead single voice |
| Expand | I→IV / I→vi | step ascent | motif sequence | 8th + slight sync | pad on, bass active |
| Stress | IV→V / ii→V | rise to V | tension notes (♭7/4) | syncopated 8th | extra layer, snare fill |
| Fracture | V→vi / deceptive | abrupt drop/silence | leaps + rests | broken hits | mute pad, glitch hits |
| Suspend | sus4+add9 + pedal | pedal | slow wide arpeggio | sparse, long notes | max reverb, hi synth |
| Discharge | V→I (fast) | V→I descent | descending run | dense 8th/16th | percussive boost |
| Resolve | V→I / IV→I | V→I cadence | landing on tonic | slowdown | fade layers, sustain pad |

Legal transitions: Stress→Fracture/Discharge, Suspend→Resolve, etc. While suspended, `disulfide_bond` must return LOW before resolve is permitted.

---

## 4. Ethereal Anchor (Suspension Subroutine)

- Condition: `nand.isBoundary && s > 0.6 && gamma > 0.6`
- Execution: sus4+add9 chord set, pedal bass, tempo half, arpeggio contour: `[0, null, +4, null, +7, null, +9, null]`
- Release: resolve forbidden until NAND settles to LOW or HIGH

---

## 5. 5-Tile Recommendation ↔ Role Mapping

| Tile | Primary Attractor | Default Role Priority |
|------|-------------------|-----------------------|
| release | energy | establish → expand → resolve |
| stress_growth | information | expand → stress |
| extreme_growth | repair | stress → fracture → discharge |
| air_cavity_discharge | interface | suspend → fracture |
| carbon_integration | integration | resolve → establish |

> tile → 8D → Musical State → Automaton → Role → Composition Plan. The 5 recommended tiles are 5 complete 4–8 bar phrases.

---

## 6. Calibration / Listening Fixtures

- Role × 2 variants = 14 deterministic phrases (4 bar each)
- Listening checklist: verify closure, stress, fracture etc. against actual perception
- On regression failure: fix the corresponding Role grammar

---

## Pipeline Summary

```
Input: (MBTI, Blood, Gender, Layer, Time)
  → 8D vector (from 01-04 mappings)
  → 9 Intent Variables (Section 1 above)
  → Form/Cadence Automaton (Section 2)
  → Role selection (Section 3)
  → Composition Plan (chords, bass, melody, rhythm, arrangement)
  → Calibration check (Section 6)
  → Audio output
```
