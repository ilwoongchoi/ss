# 8x8 Route Mapping (grounded in circuitfile1.md)

Source of truth: [circuitfile1.md](circuitfile1.md). Every cell below is anchored to an
actual node/wire in that file (line numbers given at the dimension header). Where no
direct wire exists for a cell, it is marked `(inferred via <node>)` — meaning the path is
reconstructed from adjacent real edges, not invented from scratch.

8 route-functions (columns), applied to each of the 8 dimensions (rows of tables):

1. Permission — which gate allows the dimension to become active
2. Buffer/coherence — what stability check must pass
3. Activation/event — the mechanical/metabolic commit
4. Clock/latch-write — what makes the state durable
5. Forward-expression — the "normal" outward signal
6. Reverse/reset — what tears the state down
7. Structural-routing — where it drains into slow/structural nodes
8. Observer/feedback — what evaluates it against `mor_presynaptic` (recovery baseline)

## Parameter mapping (visual dimension + named home nodes)

This is the source table from the parameter mapping (universe-prose1.md) that fixes,
for every 8D axis, its visual/spatial sense and its named circuit home nodes. All rows
below use these home nodes as the anchor set — not just inline `-dim` comments.

| 8D | 공간 감각 (visual dim) | 핵심 회로 노드 |
|---|---|---|
| r | 수평 1차원 선 | `cytochrome_c_oxidase` |
| h | 점(dot) | `histosol`, `collagen`, `male_right_oxytocin`, `disulfide_bond` |
| d | void/공허 | `cytochrome_c_oxidase` (ch1), `heme` (ch1), `chlorine_ion_pump` |
| p | 깊이(depth) | `drd2s_presynaptic`, `nonobserver_left_d2` (aka `drd2l_postsynaptic`), `mc1r`, `drd2_mpoa` |
| s | 나선 소용돌이 | `right_sole_dopamine` (aka `drd1_peripheral`/`drd1_observer`), `aurora`, `heme` (ch0) |
| gamma | 수평 확장 | `steel`, `plume`, `lower_mantle`, `basin`, `fold_belt` |
| g | fake 3D depth into perspective | `water_vapour`, `clay_gouge`, `glymphatic_system`, `caco3_final_and` |
| nu | 끊어지는 discreteness | `lower_mantle` (q), `basin` (q), `quark_orogen_magma`, `carbon`, `disulfide_bond` |

---

## r — respiratory/forward rhythm axis
Home anchors: `cytochrome_c_oxidase` (L520), `NaCl` r/d (L2208), `sodium` r/s (L2268)

| # | Route | Path |
|---|---|---|
| 1 | Permission | `drd2s_presynaptic.out0` → `caco3_drd2s_podzol_observer_and` → `caco3_final_and` gates `succinate_dehydrogenase.ctrl0` (Krebs forward channel) |
| 2 | Buffer | `caco3_final_and` (mineral-lactate AND permissive arm) must be HIGH before COX forward is trusted |
| 3 | Activation | `cck_heath_aerenchyma_and.out` XOR `bioenergetic_drive_and.out` → `cytochrome_c_oxidase_in0_xor` → `cytochrome_c_oxidase.in0` |
| 4 | Clock/latch | `succinate_dehydrogenase.out0` clocks `carbon.clk` (r-state becomes part of carbon phase memory) |
| 5 | Forward | `cytochrome_c_oxidase.out0` → `chrna7_vagal.in0` (ACh) and → `male_left_noradrenaline.in1` (NE) — rhythm/attack expression |
| 6 | Reverse/reset | `ferritin.out0` XOR `mor_presynaptic.out` → `cytochrome_c_oxidase_in1_xor` → `cytochrome_c_oxidase.in1` → `out1` → `carbon.reset` |
| 7 | Structural | `cytochrome_c_oxidase.out1` → `heme_in1_xor.in0` → heme → steel → water_vapour → clay_gouge (sealing cascade) |
| 8 | Observer | `cytochrome_c_oxidase_ctrl1_combined` (self-loop AND vasopressin XOR) feeds `ctrl1` back into COX |

---

## h — harmonic/structural-complexity axis
Home anchors: `collagen` (L1976), `cambisol` h/g (L2071), `peonidine` h/gamma (L3332), `male_right_oxytocin` h/nu (L3823)

| # | Route | Path |
|---|---|---|
| 1 | Permission | `succinate_dehydrogenase_out1_or` (SDH out1 OR `mor_presynaptic`) must pass before `collagen.ctrl0` opens |
| 2 | Buffer | `cambisol` MUX ctrl0 = `SDH_out1_or`; needs autophagic-vacuole coherence (h/g-dim) before collagen synthesis |
| 3 | Activation | `cambisol.out0` (autophagic debris: Pro/Gly/Hyp) → `collagen.in0` — event that supplies raw structural substrate |
| 4 | Clock/latch | `male_right_oxytocin` D-ff: `clk <- actomyosin.out1`, `enable <- drd2_mpoa_out0_nand.out` — harmonic/bonding state only writes on actomyosin relaxation edge |
| 5 | Forward | `collagen.out0` (Sr(38)/tau_neutrino) = harmonic overtone expression → feeds `copper_iron_complex.in1` |
| 6 | Reverse/reset | `disulfide_bond` NAND(`pentose_phosphate_out_1_xnor`, `peonidine.out0`) — oxidizing condition collapses harmonic flexibility |
| 7 | Structural | `peonidine.out0` → `disulfide_bond.in1` → `ferritin_in1_xor` / `sulfur_iron_complex.ctrl1` (mineral lock-in) |
| 8 | Observer | `male_right_oxytocin.q` / `.q_bar` → `male_right_oxytocin_q_or` / `_q_bar_or` (evaluated against `mor_presynaptic`) |

---

## d — retrograde-stress/dissonance axis
Home anchors: `chlorine_ion_pump` d-dim (L2718), `NaCl` r/d (L2123), heme ch1 d-dim (L3753)

| # | Route | Path |
|---|---|---|
| 1 | Permission | `podzol_out0_nand.out` → `chlorine_ion_pump.in0`; requires lysosomal-acidification mismatch to open |
| 2 | Buffer | `chlorine_ctrl0_combined` self-loop AND `female_gaba_b` — Cl⁻ pump only stabilizes with GABA-B coincidence |
| 3 | Activation | `water_out0_nand.out` → `chlorine_ion_pump.enable` — cytosolic H⁺ pool triggers pump |
| 4 | Clock/latch | `autophagy.r_out` → `NaCl_in0_xor.in0` — reset event writes ionic (Na⁺/Cl⁻) state |
| 5 | Forward | `NaCl` ch0 (Pu(94), ionic conduction) → `collagen_in1_or.in0` — normal depolarization signal |
| 6 | Reverse/reset | `cytochrome_c_oxidase.out1` → `carbon.reset` and → `heme_in1_xor.in0` — retrograde tears down carbon phase |
| 7 | Structural | `chlorine_ion_pump.out0` → `heme_in0_xor.in0` → HO-1 activation → steel/water cascade |
| 8 | Observer | `NaCl` ch1 (Am(95), evaporite dissonance) evaluated via `adapter_protein_q_and` XOR `mor_presynaptic` |

---

## p — predictability/pattern-latch axis
Home anchors: `mc1r` p-dim (L1061, L3211, L3510), `nitrogenase` p/nu (L2582)

| # | Route | Path |
|---|---|---|
| 1 | Permission | `drd2s_presynaptic.out0` (master permissive bus) gates most p-branch downstream AND gates |
| 2 | Buffer | `caco3_drd2s_podzol_observer_and` (3-input AND incl. `drd1_observer.q`) confirms permissive coherence |
| 3 | Activation | `manganese_nodule` q → `mc1r.d` — Mn deposition event writes predictability data |
| 4 | Clock/latch | `mc1r.clk <- glp1_q_or.out` (`glp1.q OR mor_presynaptic`) — satiety/incretin clocks MC1R |
| 5 | Forward | `mc1r_q_or.out` (high cAMP/predictability) → feeds `water_vapour_ach_or`, `carbon_q_or` type gates |
| 6 | Reverse/reset | `mc1r_q_bar_or.out` (low cAMP) → `autophagy.ctrl0` (phasic/low-predictability gating) |
| 7 | Structural | `nitrogenase` decoder (p/nu-dim) out_1/out_2 → `quark_orogen_magma`, `copper_iron_complex` deep routing |
| 8 | Observer | `mc1r` q/q_bar evaluated implicitly via downstream OR/NAND gates against `mor_presynaptic` |

---

## s — brightness/mass-spike axis
Home anchors: `heme` s-dim (L487), `succinate_dehydrogenase.out2` s-dim (L1952), `sodium` r/s (L2268)

| # | Route | Path |
|---|---|---|
| 1 | Permission | `aurora.out0` (Na⁺ threshold detector) gates `drd2_mpoa.in0` before s-branch expression |
| 2 | Buffer | `caco3_final_and` (ctrl2 on `actomyosin_ctrl`) must hold for s-axis mechanical support |
| 3 | Activation | `sodium.in0 <- ...osmosis` (Na⁺/ECF concentration event) — s-dim ionic activation |
| 4 | Clock/latch | `adapter_protein` D-ff `preset <- sodium.out0` — osmotic stability primes adapter latch |
| 5 | Forward | `succinate_dehydrogenase.out2` (Ga(31), s-dim) → `andosol.ctrl0` — soil-Mn/ambient brightness path |
| 6 | Reverse/reset | `sodium` ch1 (Tc(43), depolarization) driven by `chlorine_ion_pump` Cl⁻ efflux — inversion/brake |
| 7 | Structural | `andosol` (ROS buffer) → `fold_belt` / `oxidised_manganese` mineral routing |
| 8 | Observer | `succinate_dehydrogenase_out2_nand` NAND against `mor_presynaptic` gates `andosol.ctrl0` |

---

## gamma — spatial-expansion/width axis
Per the parameter mapping (universe-prose1.md), gamma's visual dimension is **수평 확장**
(horizontal expansion), with named home nodes **steel, plume, lower_mantle, basin,
fold_belt**. All five are real, defined nodes in circuitfile1.md (L722 `steel`, L1640
`fold_belt`, L2879 `lower_mantle`, L2944 `basin`, L5033 `plume`). The earlier version of
this table understated gamma by only using the inline `h/gamma`/`nu/gamma`/`g/gamma`
comment tags; it should use these five named nodes directly.

| # | Route | Path |
|---|---|---|
| 1 | Permission | `heme.out1` gates `steel.ctrl0` (ferritic channel); `drd2s_presynaptic.out0` gates `steel.ctrl1` (austenitic channel) |
| 2 | Buffer | `basin_q_bar_or.out` gates `fold_belt.ctrl0` — expansion into fold-belt requires metabolite-pool-depletion coherence |
| 3 | Activation | `steel_in0_xor.out` (π-electron cloud XOR observer) → `steel.in0`; `steel_in1_xor.out` (monazite XOR observer) → `steel.in1` — ferritic/austenitic expansion event |
| 4 | Clock/latch | `lower_mantle` D-ff: `clk <- methylation.out0`, `d <- basin_q_or` — expansion state written into matrix stable/stress latch |
| 5 | Forward | `steel.out0` → `water_vapour_in0_xor.in0` (O₂/hydration expansion); `basin.q` → `basin_q_or` → `citric_acid_cycle.in0` (metabolite pool expansion) |
| 6 | Reverse/reset | `lower_mantle.q_bar` → `lower_mantle_q_bar_or` → `basin.enable`; `fold_belt.out1` (Lr(103), deep/metamorphic) → `mc1r.reset` — collapses predictability on deep structural stress |
| 7 | Structural | `steel.out1` → `laterite.enable`; `fold_belt.out0` → `histosol_in0_xor.in0`, `andosol.in0`, `mangrove_aerenchyma.in0`; `plume.out0` → `plume_out0_nand` → `lower_mantle.preset` |
| 8 | Observer | `plume` MUX (`ctrl0 <- craton.out1`, `in1 <- water_out0_nand.out`) → `plume_out0_nand` (plume status NAND `mor_presynaptic`) — expansion evaluated against recovery baseline |

---

## g — binding/sealing-depth axis
Home anchors: `sulforaphane` g/nu (L1254), `water` g-dim (L2553), `cambisol` h/g (L2071), `basin` g/gamma (L2942)

| # | Route | Path |
|---|---|---|
| 1 | Permission | `drd1_peripheral.q` gates `sulforaphane.ctrl0` (D1 motor drive gates Nrf2 activation) |
| 2 | Buffer | `sodium.out0` gates `sulforaphane.ctrl1` (Na⁺ status gates GSH program) |
| 3 | Activation | `sulforaphane.out1` AND `mc1r_q_or.out` → `glymphatic_system` (AQP4-mediated clearance) |
| 4 | Clock/latch | `water` tristate: `ctrl0 <- t_ff_out` (autophagy-mode selector picks Fe-S vs ROS water source) |
| 5 | Forward | `water.out0` (Fm(100), g-dim) → binding/sealing forward expression (PIANO/DRONE/ambient register) |
| 6 | Reverse/reset | `water_out0_nand` (water.out0 NAND `mor_presynaptic`) → drives `chlorine_ion_pump.enable`, `plume.in1` |
| 7 | Structural | `steel.out0` → `water_vapour` ch0 → `clay_gouge` (D2-permission gated) → `water_vapour` ch1 (sealed) |
| 8 | Observer | `sulforaphane` out_1/out_2 evaluated via `pentose_phosphate_out_1_xnor` / `_out_2_nor` |

---

## nu — fractal-recursion/discreteness axis
Home anchors: `mycorradicin` nu-dim (L2340), `quark_orogen_magma` nu-dim (L2566), `nitrogenase` p/nu (L2582), `male_right_oxytocin` h/nu (L3823)

| # | Route | Path |
|---|---|---|
| 1 | Permission | `basin_q_or.out` (metabolite pool) → `nitrogenase.in_ctrl` — recursion needs available substrate pool |
| 2 | Buffer | `copper_iron_complex.out0` (Cu-Fe redox) → `nitrogenase.in_sub` — electron-transfer coherence required |
| 3 | Activation | `nitrogenase` decoder `logic_1 = AND(basin, hypoxia)` → `out_1` — primary N₂-fixation event |
| 4 | Clock/latch | `male_right_oxytocin` D-ff: `d <- peonidine.out1`, `enable <- drd2_mpoa_out0_nand.out` — recursion writes into bonding latch |
| 5 | Forward | `quark_orogen_magma` (Ne(10), nu-dim, fractal self-similarity) — flexible recursive expression |
| 6 | Reverse/reset | `disulfide_bond` NAND collapse → `ferritin_in1_xor` / `sulfur_iron_complex.ctrl1` rigidifies recursion into fixed mineral lock |
| 7 | Structural | `nitrogenase.out_1` → deep synthesis → `quark_orogen_magma` → `basin` / `lower_mantle` / `gluon_orogen` |
| 8 | Observer | `mycorradicin.out0` XOR `mor_presynaptic` → `actomyosin_in0_xor` — recursion stress evaluated against recovery |

---

## Cross-axis coupling summary (already grounded above)

```text
p permission (drd2s_presynaptic)
  -> r activation (COX forward XOR)
  -> s brightness (sodium/heme)
  -> gamma expansion (podzol/lower_mantle/basin)
  -> g binding (water/sulforaphane/clay)
  -> h complexity (collagen/cambisol/peonidine)
  -> nu recursion (nitrogenase/quark_orogen_magma/disulfide)
  -> d reverse-pressure audit (chlorine/NaCl/heme ch1/COX retrograde)
  -> back to p (carbon/mc1r latch write)
```

## Inverse-reciprocal pair audit (against circuitfile.md, unmodified)

The prose (universe-prose1.md) claims 4 "inverse reciprocal" pairs across the 8D axes.
Checked each against the real, untouched circuitfile.md:

| Pair | Claimed relationship | Verdict |
|---|---|---|
| p ↔ s | `left_genital_d2` → `right_sole_dopamine.clk` (positive correlation) | **Confirmed real wire**: `drd2_mpoa.out0 -> drd1_peripheral.clk` at circuitfile.md L3014. `drd2_mpoa` = left_genital_d2 alias, `drd1_peripheral` = right_sole_dopamine alias. This is the only one of the 4 pairs actually implemented as a direct wire. |
| nu ↔ r | `male_gaba_a` (nu) ↔ `female_gaba_a` (r) | **Not present**. `female_gaba_a` does not appear anywhere in circuitfile.md, not even as a reference. `male_gaba_a` is referenced (L4640, L5361) but never defined — one of the original 17 undefined-reference gaps, only given a body in circuitfile1.md's restoration block. The r-dim's real implemented node is `cytochrome_c_oxidase`, not a "female_gaba_a" node. |
| g ↔ gamma | `right_cortisol` (g) ↔ `right_d2` (gamma) | **Not present**. Both `right_cortisol` and `right_d2` are referenced-but-undefined in circuitfile.md — the same original gap list, only restored in circuitfile1.md. There is no native g↔gamma wire in the working circuit. |
| female GABA-B ↔ male GABA-B | h ↔ d polarity pair | **Not present**. No `male_gaba_b` node exists anywhere in circuitfile.md, not even as a reference — unlike the other three "missing" nodes, this one was never referenced at all. Only `female_gaba_b`/`female_gaba_b_2` are real. |

**Conclusion**: only 1 of the 4 claimed inverse-reciprocal pairs is actually wired into
the circuit. The other 3 depend on nodes that either don't exist at all, or exist only
as name-references that were never given a body until the circuitfile1.md restoration
block was added. They should be treated as narrative/interpretive claims layered on top
of the circuit, not as verified circuit behavior.

- Earlier version of this file claimed `gamma` had "no standalone home node." That was
  wrong — it ignored the parameter mapping, which explicitly names `steel`, `plume`,
  `lower_mantle`, `basin`, `fold_belt` as gamma's home nodes with visual dimension
  "수평 확장" (horizontal expansion). The gamma section above has been rebuilt using
  those five named nodes and their real wires in circuitfile1.md.
- `d`, `h`, `nu`, `s`, `p` sections above were built from inline `-dim` comment tags
  found by direct search; they are consistent with the parameter-mapping home nodes
  shown in the table, so no further correction was needed for those axes.
- Fixed `lower_mantle` clock wire: was written as `methylation.out`, actual file uses
  `methylation.out0` (channel-numbered output).
- Fixed `mc1r` clock wire: was written as `glp1_mor_or.out`, actual file uses
  `glp1_q_or.out`.
- Fixed `male_right_oxytocin` enable line (used in both the h and nu sections): was
  written as `left_genital_d2_out0_nand`, actual file uses `drd2_mpoa_out0_nand.out`.

## Validation against circuitfile.md (original, untouched)

Checked every node name used in this matrix against the real, unmodified
[circuitfile.md](circuitfile.md):

- 36 of 37 node names used above are defined there exactly as named.
- The one exception, `right_sole_dopamine`, is a deliberate alias for
  `drd1_peripheral`/`drd1_observer` (already noted in the parameter-mapping table) — not
  a gap.
- Spot-checked 6 specific wires cited in the gamma section (steel ctrl0/out0/out1,
  lower_mantle q_bar, fold_belt.out1→mc1r.reset, plume.out0→plume_out0_nand) — all exist
  verbatim in `circuitfile.md` at the cited behavior, confirming the matrix reflects the
  real circuit and not just the restoration block added in `circuitfile1.md`.
- One expected exception: `citric_acid_cycle.in0` is a real wire *target* in
  `circuitfile.md` (L2920), but `citric_acid_cycle` itself is only defined in
  `circuitfile1.md`'s restoration block — this is the same structural gap identified
  earlier, not a new inconsistency.
