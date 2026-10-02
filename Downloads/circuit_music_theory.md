# Circuit Music Theory — 8D Vector-Based Generative Music

Derived from universe-prose.md, circuitfile-rewritten.md, and HAPLOGROUP_1318_MASTER.csv.

---

## 1. Core 8D Parameters

| Parameter | Range | Circuit Definition | Music Function |
|-----------|-------|-------------------|----------------|
| r | [0.2, 1.0] | rhythm density / ADSR / tempo | Pulse count, attack speed |
| h | [0.2, 0.9] | harmonic overtone complexity | FM ratio, modulator depth |
| d | [0.1, 0.95] | freq interval / beat-freq dissonance | Dissonance gain, filter Q |
| p | [0.1, 1.0] | waveform periodicity / pattern repeatability | Sustain level, chaos |
| s | [0.1, 1.0] | high-freq energy / spectral brightness | Saw/tri mix, filter cutoff |
| gamma | [0.0, 1.0] | reverb / spatial delay / expansion | Wet mix, delay time |
| g | [0.0, 1.0] | freq-band binding density | Unison spread, voicing |
| nu | [0.0, 1.0] | waveform self-similarity / fractal | Octave layers, tremolo |

---

## 2. Scale/Mode — Derived from ABO Blood Type

Grounded in gemini 타일추천.txt: "ABO=A → Dorian", "ABO=AB → Phrygian+Lydian"

| Blood Type | Mode Name | Intervals (semitones) | Character |
|------------|-----------|----------------------|-----------|
| A | Dorian | 0, 2, 3, 5, 7, 9, 10 | Warm, folk-like, minor with raised 6th |
| B | Mixolydian | 0, 2, 4, 5, 7, 9, 10 | Bright, rock, major with lowered 7th |
| AB | Phrygian+Lydian | 0, 1, 4, 5, 7, 8, 11 | Exotic, unresolved, Spanish/Middle-Eastern |
| O | Aeolian | 0, 2, 3, 5, 7, 8, 10 | Dark, sad, natural minor |

---

## 3. Layer — Derived from Genotype (동형/이형) + RH Factor

Grounded in universe-prose.md:1110-1149:

| Layer | Genotype | RH | Root Stability | 8D Modification | Music Character |
|-------|----------|-----|----------------|-----------------|-----------------|
| **A** | 동형 (aa) | Rh+ | Most stable | None (baseline) | Consistent, predictable key |
| **B** | 동형 (aa) | Rh− | Stable but reversed | nu+0.10, gamma−0.05 | Opposite key (E↔I), darker |
| **C** | 이형 (ao) | Rh+ | Evolving | Blood type +1 | Complexity increases |
| **D** | 이형 (ao) | Rh− | Most unstable | 3AM random (p/s/nu) | Highest entropy, unpredictable |

**Root Note (루프) Interpretation:**
- **Layer A (동형 Rh+)**: Root stays in original key — maximum stability
- **Layer B (동형 Rh−)**: Root in opposite temperament key (ENFP→INFJ's key)
- **Layer C (이형 Rh+)**: Root shifts by blood type +1 (O→A→B→AB)
- **Layer D (이형 Rh−)**: Root becomes random in 3AM zone — maximum variation

**Music Effect:**
- 동형 (aa) = homozygous = consistent root, less variation
- 이형 (ao) = heterozygous = evolving root, more variation
- Rh+ = normal polarity, forward direction
- Rh− = reversed polarity, nu+0.10 (more fractal), gamma-0.05 (drier)
---

## 4. Chord Voicing — Derived from g (Binding Density)

Grounded in gemini 타일추천.txt: "g=0.7 → voicing spread", "g=0.4 → voicing close"

| g Value | Voicing | Intervals | Character |
|---------|---------|-----------|-----------|
| g > 0.5 | Wide/Spread | root, +5th(+7), +10th(+12) | Open, atmospheric |
| g ≤ 0.5 | Close | root, +3rd(+4), +5th(+7) | Tight, focused |

---

## 5. Pattern Depth — Derived from nu (Fractal Self-Similarity)

Grounded in gemini 타일추천.txt: "nu=0.4 → shallow", "nu=0.7 → deep recursion"

| nu Range | Recursion Depth | Behavior |
|----------|-----------------|----------|
| 0.0 - 0.25 | 1 | Each bar completely different |
| 0.25 - 0.5 | 2 | Simple motif repeat |
| 0.5 - 0.75 | 3 | Variation with development |
| 0.75 - 1.0 | 4 | Deep fractal recursion |

---

## 6. Rhythm Emphasis — Derived from Gender

Grounded in gemini 타일추천.txt: "gender M → downbeat", "gender F → upbeat"

| Gender | Emphasis | Grid Lock | Syncopation |
|--------|----------|-----------|-------------|
| M | Downbeat (beat 1) | 0.8 | 0.2 |
| F | Upbeat (off-beat) | 0.4 | 0.6 |

---

## 7. Melodic Contour — Derived from Toroidal Hysteresis Phase

Grounded in circuit energy flow (discharge/accumulate/transition):

| Phase | Contour | Direction | Psychological Effect |
|-------|---------|-----------|---------------------|
| discharge | ascending | Energy rising | "Create more" impulse |
| accumulate | descending | Energy falling | Resolution + gap |
| transition | stationary | Energy stable | Satisfaction + want to return |

---

## 8. Toroidal Hysteresis — ±15% Shuffle

Grounded in vectors.py line 25-27 and tile_engine.py:291-310:

| Phase | r (rhythm) | d (dissonance) | s (brightness) |
|-------|------------|----------------|-----------------|
| discharge | ↑ +15% | ↑ +15% | ↑ +15% |
| accumulate | ↓ -15% | ↓ -15% | ↓ -15% |
| transition | no change | no change | no change |

**Note:** h (harmonic) and p (periodicity) are fixed skeleton — never shuffled.

---

## 9. Rhythm Generation — r and p Only

Grounded in universe-prose.md line 988 and line 16:

- **r** (rhythm density): Pulse count on fixed 8-step grid (1..8 hits)
- **p** (periodicity): Predictability vs chaos
  - p = 1 → clean Euclidean pattern (drum-machine)
  - p = 0 → deterministic perturbation (free jazz/improvised)

**No other parameter (d, nu, gamma, h) touches rhythm** — they are timbral properties only.

---

## 10. Envelope (ADSR) — r, d, p

Grounded in universe-prose.md: "r = rhythm density / ADSR / tempo"

| Parameter | Envelope Control |
|-----------|-----------------|
| r | Attack speed (r↑ = fast attack) |
| d | Decay + Release length (d↑ = longer) |
| p | Sustain level (p↑ = higher sustain) |

---

## 11. Timbre — s, gamma, d

| Parameter | Timbre Effect |
|-----------|---------------|
| s (brightness) | 0 = pure triangle (mellow), 1 = pure sawtooth (buzzy) |
| gamma (reverb) | Higher = more wet, longer delay, more spacious |
| d (dissonance) | Higher = higher filter Q, more "biting" sound |

---

## 12. FM Synthesis — h, p

| Parameter | FM Effect |
|-----------|-----------|
| h (harmonic) | Modulator ratio (1.0 + h*0.9) |
| h + p | Depth index (h*0.6 + p*0.9) |

---

## 13. Octave Layers — nu

Grounded in universe-prose.md: "nu = waveform self-similarity / fractal"

| nu Range | +12 Octave | +24 Octave |
|----------|------------|------------|
| 0.35 - 0.75 | fades in | off |
| 0.65 - 0.98 | on | fades in |

---

## 14. Tremolo — nu

| nu | Tremolo Rate | Tremolo Depth |
|----|--------------|---------------|
| 0.0 | 1 Hz | 0% |
| 1.0 | 12 Hz | 50% |

---

## 15. 3AM Entropy Zone — Special Rules

Grounded in universe-prose.md: "3AM memory_entropy 붕괴"

When slot position is 1-16 (3AM zone):
- p = random
- s = 0.5 + random*0.5
- nu = 0.9 + random*0.1

---

## 16. 221 Grouping Rules — Release Tile

Grounded in gemini 타일추천.txt:

| Blood Type | Fixed | Variable |
|------------|-------|----------|
| O | ENERGY (R+D) | TONE (H+S) |
| A | TONE (H+S) | ENERGY (R+D) |
| B | PREDICTABILITY (P) | ENERGY (R+D) |
| AB | All independent | — |

---

## 17. Tempo — Derived from r (Rhythm Density)

Grounded in universe-prose.md: "r = rhythm density / ADSR / tempo"

| r Range | BPM | Character |
|---------|-----|-----------|
| 0.2 - 0.4 | 60 - 90 | Slow, ambient, drone |
| 0.4 - 0.6 | 90 - 120 | Moderate, groove |
| 0.6 - 0.8 | 120 - 150 | Fast, driving |
| 0.8 - 1.0 | 150 - 180 | Very fast, intense |

---

## 18. Time Signature — Derived from Gender + p (Periodicity)

| Gender | p > 0.5 | p ≤ 0.5 | Character |
|--------|---------|---------|-----------|
| M | 4/4 | 3/4 | Downbeat emphasis, waltz option |
| F | 6/8 | 5/4 | Upbeat emphasis, asymmetric |

---

## 19. Dynamic Range — Derived from s (Brightness) + Phase

| Condition | Dynamic | Character |
|-----------|---------|-----------|
| discharge + high s | Loud (ff) | Bright, energetic |
| accumulate + low s | Soft (pp) | Quiet, introspective |
| transition | Medium (mf) | Balanced |

---

## 20. Chord Progression — Derived from ABO + Layer

Grounded in diatonic harmony theory (I-IV-V-I progression):

| ABO | Mode | Typical Progression | Character |
|-----|------|---------------------|-----------|
| A | Dorian | i - IV - v - I | Minor with major tonic |
| B | Mixolydian | I - IV - V - I | Major, rock |
| AB | Phrygian+Lydian | i - bII - IV - i | Exotic, unresolved |
| O | Aeolian | i - iv - VII - I | Minor, sad |

**Layer Modification:**
- Layer A: Standard progression
- Layer B: Reverse (I becomes i, etc.)
- Layer C: Extended (adds +2 degrees)
- Layer D: Randomized (chaos in 3AM zone)

---

## 21. Voice Leading — Derived from g (Binding Density)

Grounded in voice leading principles (minimum motion, common tones):

| g Value | Voice Leading | Character |
|---------|---------------|-----------|
| g > 0.7 | Contrary motion, wide spacing | Classical, smooth |
| g 0.4 - 0.7 | Mixed motion | Balanced |
| g < 0.4 | Parallel motion, close | Pop, modern |

**Principles (per circuit):**
- Common tones: stay in same voice when possible
- Stepwise: move by step (conjunct) not leap (disjunct)
- Contrary motion: voices move opposite directions

---

## 22. Harmonic Rhythm — Derived from d (Dissonance)

Grounded in: "d = freq interval / beat-freq dissonance"

| d Range | Chord Change Rate | Character |
|---------|------------------|-----------|
| 0.1 - 0.3 | Slow (1 chord per 4 bars) | Static, ambient |
| 0.3 - 0.6 | Medium (1 chord per bar) | Standard |
| 0.6 - 0.95 | Fast (2+ chords per bar) | Active, tense |

---

## 23. Texture — Derived from nu (Fractal Self-Similarity)

| nu Range | Texture | Character |
|----------|---------|-----------|
| 0.0 - 0.3 | Monophonic | Single line, clear |
| 0.3 - 0.6 | Homophonic | Chordal, aligned |
| 0.6 - 0.8 | Polyphonic | Multiple independent lines |
| 0.8 - 1.0 | Textural layers | Dense, fractal, ambient |

---

## 24. Form (Musical Structure) — Derived from Hysteresis Phase

| Phase | Form | Structure |
|-------|------|-----------|
| discharge | Rondo (ABACA) | Energy builds, returns |
| accumulate | Binary (AB) | Resolution, ending |
| transition | Ternary (ABA') | Statement, contrast, return |

---

## 25. Register — Derived from Melodic Contour + s

| Contour | s > 0.5 | s ≤ 0.5 |
|---------|---------|---------|
| ascending | High register | Mid register |
| descending | Mid register | Low register |
| stationary | Mid register | Low register |

---

## 26. Articulation — Derived from r (Attack) + p

| r | p | Articulation | Character |
|---|---|--------------|-----------|
| high | high | Staccato, detached | Precise, mechanical |
| high | low | Marcato | Accented |
| low | high | Legato | Smooth, connected |
| low | low | Tenuto | Sustained, expressive |

---

## 27. Ornaments — Derived from nu (Fractal) + h (Harmonic)

| nu | h | Ornaments |
|----|---|-----------|
| > 0.7 | > 0.5 | Trills, turns, complex |
| > 0.7 | ≤ 0.5 | Simple ornaments |
| ≤ 0.7 | any | Few or none |

---

## 28. Accompaniment Pattern — Derived from g + p

Grounded in algorithmic composition theory:

| g | p | Pattern | Character |
|---|---|---------|-----------|
| < 0.3 | > 0.5 | Block chords | Stable, chordal |
| < 0.3 | ≤ 0.5 | Alberti bass | Classical |
| 0.3 - 0.7 | any | Arpeggiated | Standard |
| > 0.7 | > 0.5 | Stride | Jazz, energetic |
| > 0.7 | ≤ 0.5 | Tremolo | Textural |

---

## 30. Counterpoint Motion — Derived from g (Binding Density)

Grounded in voice leading theory:

| g Value | Motion Type | Character |
|---------|-------------|-----------|
| > 0.7 | Contrary motion | Classical, independent voices |
| 0.4 - 0.7 | Similar motion | Balanced, modern |
| < 0.4 | Parallel motion | Pop, electronic |

**Motion Types:**
- **Contrary**: Voices move opposite directions — most independent
- **Parallel**: Voices move same direction, same interval — creates power
- **Similar**: Both move up or down, different intervals
- **Oblique**: One voice stationary, other moves

---

## 31. Polyrhythm / Polymeter — Derived from d (Dissonance) + p

| d | p | Rhythm | Character |
|---|---|--------|-----------|
| > 0.6 | < 0.3 | 3:2 polyrhythm | Complex, African/ Jazz |
| > 0.6 | > 0.7 | 5:4 polymeter | Avant-garde |
| < 0.4 | any | Simple meter | Clear, straightforward |

---

## 32. Syncopation — Derived from Gender + p

| Gender | p | Syncopation Level |
|--------|---|-------------------|
| M | < 0.5 | Low (downbeat emphasis) |
| F | > 0.5 | High (upbeat + syncopation) |

**Implementation:** Off-beat accents, tied notes across bar lines.

---

## 33. Pedal Point — Derived from nu (Fractal Self-Similarity)

| nu | Pedal | Character |
|----|-------|-----------|
| > 0.8 | Sustained bass note | Drone, ambient |
| < 0.3 | No pedal | Clear harmony |

Pedal point (organ point) = sustained bass tone while harmony changes above.

---

## 34. Modulation — Derived from Layer + Phase

Grounded in modulation theory:

| Layer | Phase | Modulation Type | Target |
|-------|-------|-----------------|--------|
| A | transition | None (stable) | Same key |
| B | discharge | Parallel (major↔minor) | Same tonic, different quality |
| C | accumulate | Relative (major↔minor) | Same key signature |
| D | any | Pivot chord | Distantly related |

**Techniques:**
- **Pivot chord**: Common chord between keys
- **Common tone**: Shared note between keys
- **Chromatic**: Direct chromatic shift

---

## 35. Tonicization — Derived from h (Harmonic Complexity)

| h Range | Tonicization | Character |
|---------|--------------|-----------|
| > 0.7 | Strong (secondary dominants) | Classical, complex |
| 0.4 - 0.7 | Moderate | Standard |
| < 0.4 | None | Simple, diatonic |

Tonicization = temporarily treating a non-tonic chord as tonic (e.g., V/V → V).

---

## 36. Cadence Types — Derived from Phase + ABO

| Phase | ABO | Cadence | Character |
|-------|-----|---------|-----------|
| accumulate | any | Authentic (V→I) | Full resolution |
| discharge | B/O | Plagal (IV→I) | Soft resolution |
| transition | AB | Deceptive (V→vi) | Surprise |
| any | C | Half (I→V) | Open, continuing |

---

## 37. Bass Line Motion — Derived from g + d

| Condition | Bass Motion | Character |
|-----------|-------------|-----------|
| g > 0.5, d > 0.5 | By leap | Dramatic, classical |
| g < 0.5, d < 0.5 | Stepwise | Smooth, modern |
| g > 0.5, d < 0.5 | Arpeggiated | Standard |

---

## 38. Countermelody — Derived from nu (Fractal) + Layer

| nu | Layer | Countermelody |
|----|-------|---------------|
| > 0.6 | A/C | Active counterpoint |
| > 0.6 | B/D | Sparse, contrasting |
| < 0.6 | any | None or minimal |

Countermelody = secondary melodic line complementary to main melody.

---

## 39. Mode Mixture — Derived from ABO + Phase

| ABO | Phase | Mode Mixture |
|-----|-------|--------------|
| A | discharge | Mixolydian notes in Dorian |
| B | accumulate | Dorian notes in Mixolydian |
| AB | transition | Phrygian notes in Lydian |
| O | any | Minor/major blending |

Mode mixture = borrowing chords from parallel mode.

---

## 40. Secondary Dominants — Derived from h + d

| h | d | Secondary Dominants |
|---|---|---------------------|
| > 0.6 | > 0.5 | V/V, V/vi, V/ii, V/IV |
| > 0.6 | ≤ 0.5 | V/V only |
| ≤ 0.6 | any | None |

Secondary dominants = dominant of non-tonic chords.

---

## 41. Chromatic Mediant — Derived from Layer D

| Layer | Chromatic Mediant |
|-------|-------------------|
| D | Strong (↑ or ↓ 3 semitones) |
| A/B/C | Weak or none |

Chromatic mediant = chord relationship by third, chromatic shift.

---

## 42. Augmented Sixth Chords — Derived from d + h

| d | h | Augmented Sixth |
|---|---|-----------------|
| > 0.7 | > 0.5 | Italian, French, German |
| other | other | None |

Augmented sixth = chromatic predominant (Neapolitan, etc.).

---

## 43. Suspended Chords — Derived from p (Periodicity)

| p | Sus Chord |
|---|-----------|
| < 0.3 | Sus4 (stable, unresolved) |
| > 0.7 | Sus2 (open, ambiguous) |
| 0.3 - 0.7 | No sus |

---

## 44. Power Chords — Derived from r + s

| r | s | Power Chords |
|---|---|--------------|
| > 0.7 | > 0.6 | Yes (root + 5th only) |
| other | other | No (triads/seventh) |

---

## 45. Slash Chords — Derived from g + d

| g | d | Slash Chords |
|---|---|--------------|
| < 0.3 | > 0.5 | Yes (e.g., G/B) |
| other | other | No |

Slash chords = bass note different from chord root.

---

## 46. Tritone Substitution — Derived from d + Layer

| d | Layer | Tritone Sub |
|---|---|-------------|
| > 0.6 | B/D | Yes (jazz, reharmonization) |
| other | other | No |

Tritone substitution = dominant chord replaced by chord a tritone away.

---

## 48. Ostinato — Derived from nu (Fractal Self-Similarity) + r

| nu | r | Ostinato Type |
|----|---|---------------|
| > 0.7 | > 0.5 | Complex rhythmic ostinato |
| > 0.7 | ≤ 0.5 | Melodic ostinato |
| < 0.3 | any | No ostinato |

Ostinato = repeatedly played melodic/rhythmic pattern.

---

## 49. Ritardando / Accelerando — Derived from Phase + r

| Phase | r | Tempo Motion |
|-------|---|--------------|
| accumulate | < 0.5 | Ritardando (slow down) |
| discharge | > 0.5 | Accelerando (speed up) |
| transition | any | Steady tempo |

---

## 50. Rubato — Derived from p (Periodicity) + Phase

| p | Phase | Rubato Type |
|---|-------|-------------|
| < 0.3 | discharge | Agogic rubato (structural) |
| < 0.3 | accumulate | Contrametric rubato (melodic) |
| > 0.7 | any | None (steady) |

Rubato = subtle tempo flexibility within steady pulse.

---

## 51. Hemiola — Derived from d (Dissonance) + Time Signature

| d | Time Sig | Hemiola |
|---|----------|---------|
| > 0.5 | 6/8 or 3/4 | Yes (3 against 2 feel) |
| other | other | No |

Hemiola = temporary 3:2 polyrhythmic feel in duple meter.

---

## 52. Metric Modulation — Derived from Layer D + d

| Layer | d | Metric Modulation |
|-------|---|-------------------|
| D | > 0.7 | Yes (complex) |
| D | ≤ 0.7 | Yes (simple) |
| A/B/C | any | No |

Metric modulation = tempo change via rhythmic ratio pivot.

---

## 53. Note Clustering — Derived from h (Harmonic) + g

| h | g | Cluster Type |
|---|---|--------------|
| > 0.7 | > 0.5 | Dense clusters (tone clusters) |
| > 0.7 | ≤ 0.5 | Sparse clusters |
| ≤ 0.7 | any | No clusters |

Note clustering = multiple adjacent notes sounding simultaneously.

---

## 54. Bitonality / Polytonality — Derived from Layer + h

| Layer | h | Tonality |
|-------|---|----------|
| D | > 0.8 | Bitonality (two keys) |
| B | > 0.6 | Extended tonality |
| other | other | Single tonality |

---

## 55. Serialism / Twelve-Tone — Derived from Layer D + d

| Layer | d | Technique |
|-------|---|-----------|
| D | > 0.8 | Twelve-tone row |
| D | 0.5 - 0.8 | Partial serialism |
| other | other | Diatonic |

---

## 56. Aleatoric / Chance Music — Derived from Layer D + p

| Layer | p | Aleatoric Degree |
|------|---|------------------|
| D | < 0.2 | High (controlled chance) |
| D | 0.2 - 0.4 | Moderate |
| other | other | None (deterministic) |

---

## 57. Pointillism — Derived from nu + s

| nu | s | Texture |
|----|---|---------|
| > 0.8 | > 0.7 | Pointillistic (isolated notes) |
| < 0.5 | < 0.5 | Connected lines |

---

## 58. Drone / Sustained Tones — Derived from nu + gamma

| nu | gamma | Drone Type |
|----|-------|------------|
| > 0.7 | > 0.5 | Harmonic drone |
| > 0.7 | ≤ 0.5 | Single pitch drone |
| < 0.3 | any | No drone |

---

## 59. Glissando / Portamento — Derived from s + p

| s | p | Glissando |
|---|---|-----------|
| > 0.7 | < 0.3 | Yes (smooth slide) |
| other | other | No |

---

## 60. Tremolo / Vibrato — Derived from nu + s

| nu | s | Effect |
|----|---|--------|
| > 0.5 | > 0.5 | Fast tremolo |
| < 0.5 | > 0.5 | Vibrato |
| < 0.5 | < 0.5 | None |

---

## 61. Harmonics / Flageolet — Derived from h + nu

| h | nu | Harmonics |
|----|----|-----------|
| > 0.6 | > 0.5 | Natural harmonics |
| ≤ 0.6 | any | None |

---

## 62. Sforzando / Accent — Derived from d + Phase

| d | Phase | Accent Type |
|---|---|------------|
| > 0.7 | discharge | Strong sforzando |
| > 0.5 | any | Medium accent |
| ≤ 0.5 | any | Subtle |

---

## 63. Fermata / Hold — Derived from Phase + p

| Phase | p | Fermata |
|-------|---|---------|
| transition | > 0.5 | Yes (long hold) |
| accumulate | > 0.7 | Yes (medium) |
| other | other | No |

---

## 64. Coda / Outro — Derived from Phase + nu

| Phase | nu | Ending |
|-------|-----|--------|
| accumulate | > 0.5 | Gradual fade |
| transition | < 0.3 | Abrupt coda |
| discharge | any | Open ending |

---

## 65. Introduction / Outro — Derived from Phase + r

| Phase | r | Intro Type |
|-------|---|------------|
| discharge | < 0.3 | Slow intro (drum build) |
| discharge | > 0.7 | Fast intro |
| accumulate | any | No intro |

---

## 66. Call and Response — Derived from gender + nu

| Gender | nu | Pattern |
|--------|-----|---------|
| M | < 0.5 | Call → Response |
| F | > 0.5 | Question → Answer |
| any | > 0.7 | Echo |

---

## 67. Imitation / Canon — Derived from nu + g

| nu | g | Imitation |
|----|---|-----------|
| > 0.6 | > 0.5 | Canon |
| > 0.6 | ≤ 0.5 | Simple imitation |
| ≤ 0.6 | any | No imitation |

---

## 68. Augmentation / Diminution — Derived from nu + r

| nu | r | Time Modification |
|----|---|-------------------|
| > 0.7 | < 0.3 | Augmentation (longer notes) |
| > 0.7 | > 0.7 | Diminution (shorter notes) |
| ≤ 0.7 | any | Original duration |

---

## 69. Inversion / Retrograde — Derived from Layer + h

| Layer | h | Transformation |
|-------|---|----------------|
| B | > 0.5 | Melodic inversion |
| D | > 0.7 | Retrograde (reverse) |
| other | other | None |

---

## 70. Augmentation (Interval) — Derived from g + s

| g | s | Interval Size |
|---|---|---------------|
| > 0.7 | > 0.5 | Wide intervals |
| < 0.3 | < 0.5 | Narrow intervals |

---

## 72. Appoggiatura — Derived from h + Phase

| h | Phase | Appoggiatura |
|----|-------|--------------|
| > 0.5 | discharge | Yes (strong resolution) |
| > 0.5 | transition | Yes (delayed) |
| ≤ 0.5 | any | No |

Appoggiatura = unresolved melodic embellishment resolving by step.

---

## 73. Acciaccatura — Derived from p + d

| p | d | Acciaccatura |
|---|---|--------------|
| < 0.5 | > 0.5 | Yes (quick crush) |
| other | other | No |

Acciaccatura = quick melodic crush note.

---

## 74. Passing Tone — Derived from h + g

| h | g | Passing Tone |
|----|---|--------------|
| > 0.4 | < 0.6 | Yes (diatonic) |
| > 0.6 | > 0.6 | Yes (chromatic) |
| ≤ 0.4 | any | No |

Passing tone = stepwise motion between chord tones.

---

## 75. Neighbor Tone — Derived from h + nu

| h | nu | Neighbor Tone |
|----|-----|---------------|
| > 0.4 | < 0.6 | Yes (upper/lower) |
| > 0.6 | > 0.6 | Yes (double) |
| ≤ 0.4 | any | No |

Neighbor tone = stepwise motion to adjacent note and back.

---

## 76. Escape Tone — Derived from p + h

| p | h | Escape Tone |
|---|---|-------------|
| < 0.4 | > 0.5 | Yes |
| other | other | No |

Escape tone = stepwise then leap away.

---

## 77. Anticipation — Derived from Phase + d

| Phase | d | Anticipation |
|-------|---|--------------|
| accumulate | > 0.5 | Yes |
| transition | any | Yes |
| other | other | No |

Anticipation = early note of next chord.

---

## 78. Suspension — Derived from d + Phase

| d | Phase | Suspension Type |
|---|---|-----------------|
| > 0.6 | discharge | 4-3 suspension |
| > 0.6 | accumulate | 7-6 suspension |
| ≤ 0.6 | any | No |

Suspension = held note resolving down.

---

## 79. Retardation — Derived from Phase + h

| Phase | h | Retardation |
|-------|---|-------------|
| transition | > 0.5 | Yes (upward resolution) |
| other | other | No |

Retardation = held note resolving up.

---

## 80. Borrowed Chords — Derived from ABO + Layer

| ABO | Layer | Borrowed Chords |
|-----|-------|-----------------|
| O | any | Minor iv in major |
| A | B | Major bIII in minor |
| AB | C | bVI, bVII |
| B | D | Mixolydian chords |

Borrowed chords = chords from parallel mode.

---

## 81. Planing — Derived from s + g

| s | g | Planing Type |
|---|---|-------------|
| > 0.7 | > 0.5 | Yes (parallel) |
| > 0.5 | > 0.7 | Yes (root movement) |
| other | other | No |

Planing = parallel chord movement (Debussy, Impressionism).

---

## 82. Parallel Fifths/Octaves — Derived from g + Layer

| g | Layer | Allowed? |
|---|---|----------|
| < 0.3 | D | Yes (modern) |
| < 0.3 | A/B/C | No (classical) |
| > 0.3 | any | Avoid |

---

## 83. Harmonic Series — Derived from h + nu

| h | nu | Harmonic Series Usage |
|----|-----|----------------------|
| > 0.7 | > 0.5 | Yes (overtone-based) |
| ≤ 0.7 | any | Equal temperament |

---

## 84. Inversions — Derived from g + d

| g | d | Inversion Usage |
|---|---|-----------------|
| > 0.5 | < 0.5 | Many inversions |
| < 0.5 | > 0.5 | Root position |
| > 0.7 | any | Bass movement |

---

## 85. Spread Voicing — Derived from g + s

| g | s | Voicing Type |
|---|---|-------------|
| > 0.7 | > 0.5 | Spread (root-10th-5th) |
| < 0.3 | < 0.5 | Block (root-3rd-5th) |
| 0.3 - 0.7 | any | Drop-2, Drop-3 |

---

## 86. Drop-2 Voicing — Derived from g + nu

| g | nu | Drop-2 |
|----|-----|--------|
| > 0.4 | > 0.5 | Yes |
| ≤ 0.4 | any | No |

Drop-2 = jazz voicing technique.

---

## 87. Quartal Harmony — Derived from nu + g

| nu | g | Quartal |
|----|-----|--------|
| > 0.6 | < 0.4 | Yes (stack of 4ths) |
| other | other | No |

Quartal = chords built in 4ths (McCoy Tyner).

---

## 88. Polychord — Derived from h + g

| h | g | Polychord |
|---|---|----------|
| > 0.7 | > 0.5 | Yes (stacked) |
| > 0.7 | ≤ 0.5 | Yes (simple) |
| ≤ 0.7 | any | No |

Polychord = two chords stacked.

---

## 89. Upper Structure — Derived from h + Layer

| h | Layer | Upper Structure |
|----|-------|-----------------|
| > 0.6 | B/D | Yes (triads on top) |
| other | other | No |

Upper structure = triad over bass note.

---

## 90. Tritone Resolution — Derived from d + Layer

| d | Layer | Resolution |
|---|---|-----------|
| > 0.6 | B | B2→T (dominant tension) |
| > 0.6 | D | Altered resolution |
| ≤ 0.6 | any | Standard |

---

## 91. Leading Tone — Derived from ABO + h

| ABO | h | Leading Tone |
|-----|---|--------------|
| O | > 0.5 | Strong (♯7) |
| A | > 0.5 | Moderate |
| B | > 0.5 | Mixolydian (♭7) |
| AB | > 0.5 | Weak |

---

## 92. Tendency Tones — Derived from h + Phase

| h | Phase | Tendency |
|----|-------|----------|
| > 0.6 | discharge | ♯4→5, ♯7→1 |
| > 0.6 | accumulate | ♭6→5, ♭2→1 |
| ≤ 0.6 | any | Stable |

---

## 93. Functional Harmony — Derived from ABO + d

| ABO | d | Function Focus |
|-----|---|-----------------|
| A | > 0.5 | Tonic-Predominant-Dominant |
| B | > 0.5 | Dominant-heavy |
| O | > 0.5 | Tonic-heavy |
| AB | any | All balanced |

---

## 94. Phrygian Cadence — Derived from AB + d

| AB | d | Phrygian Cadence |
|----|---|------------------|
| AB | > 0.5 | Yes (♭2→1 in bass) |
| other | other | No |

Phrygian cadence = half-cadence with ♭2 in bass.

---

## 95. Tierce de Picardie — Derived from O + Phase

| O | Phase | Tierce de Picardie |
|----|-------|-------------------|
| O | accumulate | Yes (major tonic in minor) |
| other | other | No |

Tierce de Picardie = major tonic ending in minor key.

---

## 96. Picardy Third — Same as above

---

## 97. Deceptive Cadence — Derived from AB + Phase

| AB | Phase | Deceptive |
|----|-------|-----------|
| AB | transition | V→vi |
| B | transition | V→IV |
| other | other | No |

---

## 98. Half Cadence — Derived from p + d

| p | d | Half Cadence |
|---|---|--------------|
| < 0.5 | > 0.5 | Yes (V) |
| > 0.7 | any | No |
| other | other | Possible |

---

## 99. Plagal Cadence — Derived from ABO + Phase

| ABO | Phase | Plagal |
|-----|-------|--------|
| B | accumulate | IV→I |
| O | accumulate | iv→i |
| other | other | Possible |

---

## 100. Perfect Authentic Cadence — Derived from h + Phase

| h | Phase | PAC |
|----|-------|-----|
| > 0.5 | accumulate | V→I (both in root) |
| other | other | No |

---

## 101. Interrupted Cadence — Same as Deceptive Cadence

---

## 102. Evaded Cadence — Derived from d + g

| d | g | Evaded |
|---|---|--------|
| > 0.6 | > 0.5 | Yes (inversion resolution) |
| other | other | No |

---

## 103. Enclosures — Derived from h + p

| h | p | Enclosure Type |
|----|---|----------------|
| > 0.5 | < 0.5 | Yes (tone-semitone) |
| > 0.6 | any | Chromatic enclosure |
| ≤ 0.5 | any | No |

Enclosures = approach chord tone from both sides.

---

## 104. Approach Chords — Derived from d + h

| d | h | Approach |
|---|---|----------|
| > 0.5 | > 0.5 | Chromatic approach |
| > 0.5 | ≤ 0.5 | Diatonic approach |
| ≤ 0.5 | any | Direct |

---

## 105. Reharmonization — Derived from Layer D + d

| Layer | d | Reharmonization |
|-------|---|-----------------|
| D | > 0.5 | Yes (extensive) |
| D | ≤ 0.5 | Moderate |
| other | any | Minimal |

---

## 106. Pivot Chord Modulation — Derived from Layer + g

| Layer | g | Pivot Chord |
|-------|---|-------------|
| C | > 0.5 | Yes (common chord) |
| D | any | Yes (multiple) |
| A/B | any | Limited |

---

## 107. Common Tone Modulation — Derived from nu + h

| nu | h | Common Tone |
|----|-----|-------------|
| > 0.5 | > 0.4 | Yes |
| ≤ 0.5 | any | No |

Common tone = shared pitch between keys.

---

## 108. enharmonic Modulation — Derived from Layer D + d

| Layer | d | Enharmonic |
|-------|---|------------|
| D | > 0.7 | Yes (dim7, aug6) |
| other | other | No |

Enharmonic = same sound, different spelling.

---

## 109. Chromatic Mediant — Derived from ABO + Layer

| ABO | Layer | Mediant |
|-----|-------|---------|
| AB | D | Strong |
| O | C | Moderate |
| A/B | B | Weak |

---

## 110. Parallel Key Change — Derived from Layer + Phase

| Layer | Phase | Parallel |
|-------|-------|----------|
| B | discharge | Major↔minor |
| D | any | Yes |
| other | other | No |

---

## 111. Relative Key Change — Derived from ABO + Phase

| ABO | Phase | Relative |
|-----|-------|----------|
| O | accumulate | Minor↔major |
| A | transition | Same |
| other | other | Possible |

---

## 112. Diatonic Common Tone — Derived from h + ABO

| h | ABO | Diatonic CT |
|----|-----|-------------|
| > 0.5 | O | Yes (scale-based) |
| > 0.5 | AB | Multiple |
| ≤ 0.5 | any | Limited |

---

## 113. Secondary Function — Derived from h + d

| h | d | Secondary Function |
|----|---|---------------------|
| > 0.6 | > 0.5 | V/V, V/vi, V/ii, V/IV |
| > 0.6 | ≤ 0.5 | V/V only |
| ≤ 0.6 | any | None |

---

## 114. Modal Interchange — Same as Borrowed Chords (Section 80)

---

## 115. Blues Scale — Derived from O + s

| O | s | Blues Scale |
|----|---|--------------|
| O | > 0.5 | Yes (♭3, ♭5, ♭7) |
| other | other | No |

---

## 116. Pentatonic Scale — Derived from nu + p

| nu | p | Pentatonic |
|----|---|------------|
| < 0.3 | > 0.5 | Major pentatonic |
| < 0.3 | ≤ 0.5 | Minor pentatonic |
| ≥ 0.3 | any | Full scale |

---

## 117. Whole Tone Scale — Derived from h + Layer

| h | Layer | Whole Tone |
|----|-------|------------|
| > 0.8 | D | Yes |
| > 0.6 | B | Yes (partial) |
| other | other | No |

---

## 118. Chromatic Scale — Derived from Layer D + d

| Layer | d | Chromatic |
|-------|---|-----------|
| D | > 0.8 | Yes (full) |
| D | 0.5-0.8 | Partial |
| other | other | No |

---

## 119. Diminished Scale — Derived from d + Layer

| d | Layer | Diminished |
|---|---|-----------|
| > 0.7 | B/D | Yes (whole-half) |
| > 0.5 | other | Half-whole |
| ≤ 0.5 | any | No |

---

## 120. Altered Scale — Derived from d + h

| d | h | Altered |
|---|---|---------|
| > 0.7 | > 0.6 | Yes (♭9, ♯9, ♯11, ♭13) |
| other | other | No |

---

## 121. Melodic Minor Scale — Derived from ABO + Phase

| ABO | Phase | Melodic Minor |
|-----|-------|---------------|
| O | transition | Ascending major |
| A | accumulate | Descending natural |
| other | other | Standard |

---

## 122. Harmonic Minor Scale — Derived from ABO + h

| ABO | h | Harmonic Minor |
|-----|---|----------------|
| O | > 0.5 | Yes (raised 7) |
| AB | > 0.5 | Yes (raised 7 + lowered 6) |
| other | other | Natural |

---

## 123. Bebop Scale — Derived from d + Layer

| d | Layer | Bebop |
|---|---|-------|
| > 0.6 | B | Dominant bebop |
| > 0.6 | D | Major bebop |
| other | other | No |

---

## 124. Gypsy Scale — Derived from AB + h

| AB | h | Gypsy |
|----|---|-------|
| AB | > 0.6 | Yes (Hungarian minor) |
| other | other | No |

---

## 125. Hirajoshi Scale — Derived from nu + Layer

| nu | Layer | Hirajoshi |
|----|-------|-----------|
| > 0.7 | D | Yes |
| other | other | No |

---

## 126. Diminished Arpeggio — Derived from d + nu

| d | nu | Dim Arpeggio |
|---|---|--------------|
| > 0.6 | > 0.5 | Yes (alternating) |
| other | other | No |

---

## 127. Augmented Arpeggio — Derived from h + nu

| h | nu | Aug Arpeggio |
|---|---|-------------|
| > 0.6 | > 0.5 | Yes |
| other | other | No |

---

## 128. Spread Triad — Derived from g + s

| g | s | Spread Triad |
|---|---|-------------|
| > 0.7 | > 0.5 | Root-10th-6th |
| > 0.7 | ≤ 0.5 | Root-10th-5th |
| ≤ 0.7 | any | Close position |

---

## 129. Locked Hands — Derived from g + r

| g | r | Locked Hands |
|---|---|-------------|
| < 0.3 | > 0.5 | Yes (parallel) |
| other | other | No |

Locked hands = parallel block chords (Marian McPartland).

---

## 130. Shell Voicing — Derived from g + p

| g | p | Shell Voicing |
|---|---|--------------|
| < 0.3 | > 0.5 | Yes (3rd-7th) |
| other | other | Full voicing |

Shell = minimal voicing (root-3rd-7th).

---

## 131. Rootless Voicing — Derived from g + nu

| g | nu | Rootless |
|----|-----|----------|
| < 0.3 | > 0.5 | Yes (3rd-7th-9th) |
| other | other | Root present |

---

## 132. Voice Leading (Detailed) — Derived from g + h

| g | h | Voice Leading |
|---|---|---------------|
| > 0.7 | > 0.5 | Smooth (stepwise) |
| > 0.7 | ≤ 0.5 | Mixed |
| < 0.4 | any | Direct |

---

## 133. Common Tone — Derived from g + ABO

| g | ABO | Common Tone |
|----|-----|-------------|
| > 0.5 | O | Keep root |
| > 0.5 | A | Keep 3rd |
| > 0.5 | B | Keep 5th |
| > 0.5 | AB | Any |

---

## 134. Tendency Voice — Derived from h + Phase

| h | Phase | Tendency Voice |
|----|-------|----------------|
| > 0.6 | discharge | Leading tone up |
| > 0.6 | accumulate | 7th down |
| ≤ 0.6 | any | Stable |

---

## 135. Counterpoint Species — Derived from Layer + nu

| Layer | nu | Species |
|-------|-----|---------|
| A | > 0.5 | Note-against-note (1st) |
| B | > 0.5 | Note-against-two (2nd) |
| C | > 0.5 | Note-against-three (3rd) |
| D | any | Florid (4th-5th) |

---

## 136. Cantus Firmus — Derived from nu + p

| nu | p | Cantus Firmus |
|----|-----|---------------|
| < 0.3 | > 0.5 | Yes (long notes) |
| other | other | No |

Cantus firmus = fixed melodic line (Renaissance).

---

## 137. Contrapuntal Technique — Derived from g + Layer

| g | Layer | Technique |
|---|---|----------|
| > 0.6 | A | Imitation |
| > 0.6 | B | Canon |
| > 0.6 | C | Fugue |
| > 0.6 | D | Free counterpoint |

---

## 138. Stretto — Derived from nu + Layer

| nu | Layer | Stretto |
|----|-------|---------|
| > 0.7 | B/C | Yes (overlapping) |
| other | other | No |

Stretto = overlapping subject entries (fugue).

---

## 139. Augmentation (Counterpoint) — Derived from nu + r

| nu | r | Augmentation |
|----|-----|--------------|
| > 0.7 | < 0.3 | Yes (longer values) |
| other | other | No |

---

## 140. Diminution (Counterpoint) — Derived from nu + r

| nu | r | Diminution |
|----|-----|------------|
| > 0.7 | > 0.7 | Yes (shorter values) |
| other | other | No |

---

## 141. Invertible Counterpoint — Derived from g + Layer

| g | Layer | Invertible |
|---|---|-----------|
| > 0.6 | B | Yes (at octave) |
| > 0.6 | D | Yes (at any interval) |
| ≤ 0.6 | any | No |

---

## 142. Canon — Derived from nu + g

| nu | g | Canon Type |
|----|-----|-----------|
| > 0.6 | > 0.5 | True canon |
| > 0.6 | ≤ 0.5 | Round |
| ≤ 0.6 | any | No |

---

## 143. Fugue Subject — Derived from h + nu

| h | nu | Subject |
|----|-----|---------|
| > 0.5 | > 0.4 | Yes (characteristic) |
| ≤ 0.5 | any | Simple subject |

---

## 144. Fugue Answer — Derived from h + Layer

| h | Layer | Answer |
|----|-------|--------|
| > 0.5 | B | Real answer |
| > 0.5 | D | Tonal answer |
| ≤ 0.5 | any | Direct |

---

## 145. Fugue Exposition — Derived from nu + Layer

| nu | Layer | Exposition |
|----|-------|------------|
| > 0.5 | B | Standard (S-A-T-B) |
| > 0.5 | D | Extended |
| ≤ 0.5 | any | Brief |

---

## 146. Episode — Derived from nu + Phase

| nu | Phase | Episode |
|----|-------|---------|
| > 0.5 | transition | Yes (modulating) |
| > 0.5 | accumulate | Yes (sequential) |
| ≤ 0.5 | any | No |

---

## 147. Codetta — Derived from Phase + nu

| Phase | nu | Codetta |
|-------|-----|---------|
| accumulate | > 0.5 | Yes (tonic) |
| transition | > 0.7 | Extended |
| other | other | Brief |

---

## 148. Coda (Extended) — Derived from Phase + nu

| Phase | nu | Coda |
|-------|-----|------|
| accumulate | > 0.7 | Yes (extended) |
| transition | < 0.3 | Yes (abrupt) |
| discharge | any | No |

---

## 149. Da Capo — Derived from Phase + nu

| Phase | nu | Da Capo |
|-------|-----|---------|
| transition | < 0.3 | Yes (repeat from start) |
| other | other | No |

---

## 150. Dal Segno — Derived from Phase + g

| Phase | g | Dal Segno |
|-------|---|-----------|
| transition | > 0.5 | Yes (from sign) |
| other | other | No |

---

## 151. Rounded Binary — Derived from nu + Phase

| nu | Phase | Binary |
|----|-------|--------|
| > 0.4 | accumulate | Rounded (return to tonic) |
| ≤ 0.4 | any | Simple |

---

## 152. Ternary (ABA) — Derived from Phase + nu

| Phase | nu | Ternary |
|-------|-----|---------|
| transition | > 0.5 | Yes (A-B-A) |
| other | other | Possible |

---

## 153. Rondo Form — Derived from Phase + nu

| Phase | nu | Rondo |
|-------|-----|-------|
| discharge | > 0.5 | ABACA |
| discharge | > 0.7 | ABACADA |
| other | other | Simple |

---

## 154. Sonata Form — Derived from Layer + h

| Layer | h | Sonata Form |
|-------|---|-------------|
| A | > 0.5 | Exposition-Development-Recap |
| B | > 0.5 | With double exposition |
| D | > 0.5 | Modified |

---

## 155. Theme and Variations — Derived from nu + h

| nu | h | Variations |
|----|-----|------------|
| > 0.5 | > 0.4 | Yes (multiple) |
| > 0.7 | any | Complex variations |
| ≤ 0.5 | any | Simple |

---

## 156. Theme Type — Derived from h + p

| h | p | Theme |
|----|---|-------|
| > 0.5 | > 0.5 | Period (antecedent-consequent) |
| > 0.5 | ≤ 0.5 | Sentence (statement-answer) |
| ≤ 0.5 | any | Phrase |

---

## 157. Phrase Length — Derived from r + p

| r | p | Phrase Length |
|---|---|---------------|
| > 0.6 | > 0.5 | 4 bars |
| > 0.6 | ≤ 0.5 | 8 bars |
| ≤ 0.4 | any | Variable |

---

## 158. Period — Derived from h + r

| h | r | Period Type |
|----|---|-------------|
| > 0.5 | > 0.5 | Parallel (same ending) |
| > 0.5 | ≤ 0.5 | Contrasting (different) |
| ≤ 0.5 | any | Single phrase |

---

## 159. Sentence — Derived from p + h

| p | h | Sentence |
|---|---|----------|
| > 0.5 | > 0.5 | Yes (statement-continue-cadence) |
| other | other | No |

---

## 160. Paragraph — Derived from nu + r

| nu | r | Paragraph |
|----|-----|-----------|
| > 0.5 | > 0.5 | Yes (multiple periods) |
| other | other | No |

---

## 161. Motif — Derived from h + p

| h | p | Motif Type |
|----|---|------------|
| > 0.5 | > 0.5 | Rhythmic motif |
| ≤ 0.5 | > 0.5 | Melodic motif |
| any | ≤ 0.5 | Thematic |

---

## 162. Leitmotif — Derived from Layer + h

| Layer | h | Leitmotif |
|-------|---|-----------|
| B | > 0.6 | Yes (character) |
| D | > 0.6 | Yes (situational) |
| other | other | No |

---

## 163. Thematic Development — Derived from nu + h

| nu | h | Development |
|----|-----|-------------|
| > 0.6 | > 0.5 | Yes (variation) |
| > 0.7 | > 0.6 | Yes (fragmentation) |
| ≤ 0.6 | any | Repetition |

---

## 164. Sequence — Derived from d + nu

| d | nu | Sequence |
|---|---|----------|
| > 0.4 | > 0.4 | Yes (diatonic) |
| > 0.6 | > 0.6 | Yes (chromatic) |
| ≤ 0.4 | any | No |

---

## 165. Fragmentation — Derived from nu + r

| nu | r | Fragmentation |
|----|-----|---------------|
| > 0.7 | > 0.5 | Yes (motif pieces) |
| other | other | No |

---

## 166. Elaboration — Derived from h + d

| h | d | Elaboration |
|----|-----|------------|
| > 0.5 | > 0.5 | Yes (embellish) |
| other | other | No |

---

## 167. Thinning — Derived from nu + s

| nu | s | Thinning |
|----|---|----------|
| > 0.6 | < 0.5 | Yes (reduce voices) |
| other | other | No |

---

## 168. Thickening — Derived from nu + s

| nu | s | Thickening |
|----|---|------------|
| > 0.6 | > 0.5 | Yes (add voices) |
| other | other | No |

---

## 169. Register Shift — Derived from s + Phase

| s | Phase | Register |
|---|---|---------|
| > 0.6 | discharge | Upward |
| > 0.6 | accumulate | Downward |
| ≤ 0.4 | any | Stable |

---

## 170. Octave Displacement — Derived from g + p

| g | p | Displacement |
|---|---|--------------|
| > 0.5 | < 0.5 | Yes |
| ≤ 0.5 | any | No |

---

## 171. Summary: Complete Circuit → Music Mapping

```
User Profile (MBTI, ABO, Gender, RH, Time)
         ↓
    8D Vector (from circuit state)
         ↓
    ┌──────────────────────────────────────────────────────────────┐
    │ r → pulse density + tempo + articulation + power chords     │
    │ p → pattern predictability + time sig + suspended chords    │
    │ h → FM harmonic complexity + ornaments + tonicization       │
    │ d → dissonance + harmonic rhythm + polyrhythm + tritone sub │
    │ s → brightness + dynamic + register                         │
    │ gamma → reverb/wet mix + texture                            │
    │ g → voicing + voice leading + pattern + slash chords        │
    │ nu → fractal depth + texture + form + pedal point           │
    └──────────────────────────────────────────────────────────────┘
         ↓
    ABO → Scale/Mode (Dorian/Mixolydian/etc)
    Layer → Root stability + modulation + chromatic mediant
    Gender → Rhythm emphasis + time signature + syncopation
    Phase → Melodic contour + form + dynamics + cadence
    Hysteresis → ±15% shuffle on r,d,s
         ↓
    Advanced Harmony:
    ├── Counterpoint motion (contrary/parallel/similar)
    ├── Chord progression (I-IV-V-I variants)
    ├── Modulation (pivot/relative/parallel)
    ├── Mode mixture + secondary dominants
    ├── Augmented sixth + Neapolitan
    └── Countermelody + bass line motion
         ↓
    Generated Music
```

---

## Key Principles

1. **Parameter-first, not genre-first**: No "genre selection" step. Music emerges from 8D vector values.
2. **Deterministic**: Same vector + same time = same music (no random in core synthesis).
3. **Continuous**: No discrete switches — all parameters crossfade smoothly.
4. **Residual stress**: Music never fully resolves — 30% stress remains to drive user toward other creative activities.
5. **Self-listen satisfying loop**: Ascending contour → "create more" → other hobbies → satisfaction → return to music.
