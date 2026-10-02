# 128 성격 × 먹을거(Food) 노드 매핑

CIRCUITFILE.MD의 먹을거/대사/소화/영양 관련 노드만 추출하여 128 성격에 매핑.

총 먹을거 노드: 43개

## 먹을거 카테고리

| 카테고리 | 노드 수 | 노드 목록 |
|---|---|---|
| 단백질 | 1 | collagen |
| 단백질구조 | 1 | disulfide_bond |
| 대사구동 | 1 | bioenergetic_drive_and |
| 미네랄 | 10 | heme, hemoglobin, ferritin, NaCl, sodium, chlorine_ion_pump, copper_iron_complex, manganese_nodule, iodine, caco3 |
| 산소공급 | 1 | mangrove_aerenchyma |
| 소화 | 4 | proton_pump, carbonic_anhydrase, choline, right_acetylcholine |
| 수분 | 2 | water, water_vapour |
| 식물영양소 | 2 | sulforaphane, peonidine |
| 신경펩타이드 | 1 | substance_p |
| 아미노산 | 2 | methionine, cysteine |
| 에너지대사 | 5 | citric_acid_cycle, succinate_dehydrogenase, lactate_dehydrogenase, cytochrome_c_oxidase, pentose_phosphate |
| 자가포식 | 1 | autophagy |
| 장내미생물 | 3 | methanogenesis, nitrogenase, chrna7_vagal |
| 조리반응 | 1 | maillard |
| 탄수화물 | 2 | carbon, co2 |
| 포만허기 | 3 | opioid_and, opioid_nor, opioid_xnor_or |
| 포만호르몬 | 2 | glp1, cck |
| 항산화영양소 | 1 | glutathione |

## 먹을거 노드 색상 분포

| 색상 | Hex | 노드 수 |
|---|---|---|
| WHITE | `#FFFFFF` | 7 |
| RED | `#FF0000` | 5 |
| YELLOW | `#FFFF00` | 5 |
| PALE-YELLOW | `#FFFFC8` | 4 |
| GREEN | `#00FF00` | 4 |
| DARK-BROWN | `#654321` | 3 |
| PALE-GREEN | `#98FB98` | 3 |
| BLUE-WHITE | `#E0FFFF` | 3 |
| BLACK | `#000000` | 2 |
| DARK-GREEN | `#006400` | 2 |
| ORANGE | `#FFA500` | 1 |
| RED-PURPLE | `#A02060` | 1 |
| RED-BROWN | `#A52A2A` | 1 |
| GRAY | `#808080` | 1 |
| BROWN | `#8B4513` | 1 |

## 128 성격별 top-3 먹을거 노드 (12h 낮 기준)

| # | 성격 | 원소 | 채널 | 색상 | top-1 먹을거 | top-2 | top-3 |
|---|---|---|---|---|---|---|---|
| 1 | ENFP_M_O | H(1) | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 2 | ENFP_M_A | Sc(21) | SW | `#230FFF` | carbon(0.56) | cytochrome_c_oxidase(0.55) | ferritin(0.46) |
| 3 | ENFP_M_B | Tb(65) | SM | `#FF0F14` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 4 | ENFP_M_AB | Md(101) | BW | `#23FF14` | substance_p(0.91) | copper_iron_complex(0.91) | chrna7_vagal(0.91) |
| 5 | ENFP_F_O |  | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 6 | ENFP_F_A | Ne(10) | SW | `#230FFF` | carbon(0.56) | cytochrome_c_oxidase(0.55) | ferritin(0.46) |
| 7 | ENFP_F_B | Cr(24) | SM | `#FF0F14` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 8 | ENFP_F_AB | Zn(30) | BW | `#23FF14` | substance_p(0.91) | copper_iron_complex(0.91) | chrna7_vagal(0.91) |
| 9 | ENFJ_M_O | Ar(18) | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 10 | ENFJ_M_A | Cs(55) | SW | `#2300FF` | cytochrome_c_oxidase(0.54) | carbon(0.54) | ferritin(0.45) |
| 11 | ENFJ_M_B | Gd(64) | SM | `#FF0014` | cck(0.95) | cysteine(0.95) | proton_pump(0.95) |
| 12 | ENFJ_M_AB | Sn(50) | BW | `#23FF14` | substance_p(0.91) | copper_iron_complex(0.91) | chrna7_vagal(0.91) |
| 13 | ENFJ_F_O | Os(76) | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 14 | ENFJ_F_A | Pb(82) | SW | `#2300FF` | cytochrome_c_oxidase(0.54) | carbon(0.54) | ferritin(0.45) |
| 15 | ENFJ_F_B | K(19) | SM | `#FF0014` | cck(0.95) | cysteine(0.95) | proton_pump(0.95) |
| 16 | ENFJ_F_AB | Te(52) | BW | `#23FF14` | substance_p(0.91) | copper_iron_complex(0.91) | chrna7_vagal(0.91) |
| 17 | ENTP_M_O |  | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 18 | ENTP_M_A | Rn(86) | SW | `#0F0FFF` | carbon(0.54) | cytochrome_c_oxidase(0.52) | ferritin(0.45) |
| 19 | ENTP_M_B |  | SM | `#FF0F14` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 20 | ENTP_M_AB | Rf(104) | BW | `#0FFF14` | substance_p(0.94) | copper_iron_complex(0.94) | chrna7_vagal(0.94) |
| 21 | ENTP_F_O | Cf(98) | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 22 | ENTP_F_A | B(5) | SW | `#0F0FFF` | carbon(0.54) | cytochrome_c_oxidase(0.52) | ferritin(0.45) |
| 23 | ENTP_F_B | Ho(67) | SM | `#FF0F14` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 24 | ENTP_F_AB | Rg(111) | BW | `#0FFF14` | substance_p(0.94) | copper_iron_complex(0.94) | chrna7_vagal(0.94) |
| 25 | ENTJ_M_O | Ca(20) | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 26 | ENTJ_M_A | Sr(38) | SW | `#0F00FF` | carbon(0.52) | cytochrome_c_oxidase(0.51) | ferritin(0.44) |
| 27 | ENTJ_M_B | Pr(59) | SM | `#FF0014` | cck(0.95) | cysteine(0.95) | proton_pump(0.95) |
| 28 | ENTJ_M_AB | Y(39) | BW | `#0FFF14` | substance_p(0.94) | copper_iron_complex(0.94) | chrna7_vagal(0.94) |
| 29 | ENTJ_F_O | Db(105) | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 30 | ENTJ_F_A | Ds(110) | SW | `#0F00FF` | carbon(0.52) | cytochrome_c_oxidase(0.51) | ferritin(0.44) |
| 31 | ENTJ_F_B | Lv(116) | SM | `#FF0014` | cck(0.95) | cysteine(0.95) | proton_pump(0.95) |
| 32 | ENTJ_F_AB | Co(27) | BW | `#0FFF14` | substance_p(0.94) | copper_iron_complex(0.94) | chrna7_vagal(0.94) |
| 33 | ESFP_M_O | Al(13) | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 34 | ESFP_M_A | Ag(47) | SW | `#0F23FF` | carbon(0.56) | cytochrome_c_oxidase(0.52) | ferritin(0.46) |
| 35 | ESFP_M_B | Mg(12) | SM | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 36 | ESFP_M_AB | V(23) | BW | `#0FFF00` | substance_p(0.97) | copper_iron_complex(0.97) | chrna7_vagal(0.97) |
| 37 | ESFP_F_O | In(49) | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 38 | ESFP_F_A | Ta(73) | SW | `#0F23FF` | carbon(0.56) | cytochrome_c_oxidase(0.52) | ferritin(0.46) |
| 39 | ESFP_F_B | Cd(48) | SM | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 40 | ESFP_F_AB | Sb(51) | BW | `#0FFF00` | substance_p(0.97) | copper_iron_complex(0.97) | chrna7_vagal(0.97) |
| 41 | ESFJ_M_O | Yb(70) | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 42 | ESFJ_M_A | Li(3) | SW | `#0F14FF` | carbon(0.54) | cytochrome_c_oxidase(0.52) | ferritin(0.45) |
| 43 | ESFJ_M_B |  | SM | `#FF1400` | cck(0.95) | cysteine(0.95) | proton_pump(0.95) |
| 44 | ESFJ_M_AB |  | BW | `#0FFF00` | substance_p(0.97) | copper_iron_complex(0.97) | chrna7_vagal(0.97) |
| 45 | ESFJ_F_O | Es(99) | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 46 | ESFJ_F_A | Ni(28) | SW | `#0F14FF` | carbon(0.54) | cytochrome_c_oxidase(0.52) | ferritin(0.45) |
| 47 | ESFJ_F_B | Xe(54) | SM | `#FF1400` | cck(0.95) | cysteine(0.95) | proton_pump(0.95) |
| 48 | ESFJ_F_AB | Pt(78) | BW | `#0FFF00` | substance_p(0.97) | copper_iron_complex(0.97) | chrna7_vagal(0.97) |
| 49 | ESTP_M_O | C(6) | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 50 | ESTP_M_A | Th(90) | SW | `#2323FF` | carbon(0.59) | cytochrome_c_oxidase(0.55) | ferritin(0.47) |
| 51 | ESTP_M_B | Nd(60) | SM | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 52 | ESTP_M_AB | Lr(103) | BW | `#23FF00` | substance_p(0.92) | copper_iron_complex(0.92) | chrna7_vagal(0.92) |
| 53 | ESTP_F_O | As(33) | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 54 | ESTP_F_A | Tm(69) | SW | `#2323FF` | carbon(0.59) | cytochrome_c_oxidase(0.55) | ferritin(0.47) |
| 55 | ESTP_F_B |  | SM | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 56 | ESTP_F_AB | Sm(62) | BW | `#23FF00` | substance_p(0.92) | copper_iron_complex(0.92) | chrna7_vagal(0.92) |
| 57 | ESTJ_M_O | Cu(29) | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 58 | ESTJ_M_A |  | SW | `#2314FF` | carbon(0.57) | cytochrome_c_oxidase(0.55) | ferritin(0.46) |
| 59 | ESTJ_M_B | Cl(17) | SM | `#FF1400` | cck(0.95) | cysteine(0.95) | proton_pump(0.95) |
| 60 | ESTJ_M_AB | Ge(32) | BW | `#23FF00` | substance_p(0.92) | copper_iron_complex(0.92) | chrna7_vagal(0.92) |
| 61 | ESTJ_F_O |  | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 62 | ESTJ_F_A | Ti(22) | SW | `#2314FF` | carbon(0.57) | cytochrome_c_oxidase(0.55) | ferritin(0.46) |
| 63 | ESTJ_F_B | Er(68) | SM | `#FF1400` | cck(0.95) | cysteine(0.95) | proton_pump(0.95) |
| 64 | ESTJ_F_AB | F(9) | BW | `#23FF00` | substance_p(0.92) | copper_iron_complex(0.92) | chrna7_vagal(0.92) |
| 65 | INFP_M_O | Sg(106) | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 66 | INFP_M_A | Ce(58) | SW | `#140FFF` | carbon(0.54) | cytochrome_c_oxidase(0.53) | ferritin(0.45) |
| 67 | INFP_M_B | Ru(44) | SM | `#FF0F14` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 68 | INFP_M_AB | Lu(71) | BW | `#14FF14` | substance_p(0.94) | copper_iron_complex(0.94) | chrna7_vagal(0.94) |
| 69 | INFP_F_O |  | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 70 | INFP_F_A |  | SW | `#140FFF` | carbon(0.54) | cytochrome_c_oxidase(0.53) | ferritin(0.45) |
| 71 | INFP_F_B | Pa(91) | SM | `#FF0F14` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 72 | INFP_F_AB | Am(95) | BW | `#14FF14` | substance_p(0.94) | copper_iron_complex(0.94) | chrna7_vagal(0.94) |
| 73 | INFJ_M_O | Fr(87) | BM | `#FFFF23` | bioenergetic_drive_and(0.92) | methionine(0.92) | disulfide_bond(0.92) |
| 74 | INFJ_M_A | Rb(37) | SW | `#1400FF` | carbon(0.52) | cytochrome_c_oxidase(0.52) | ferritin(0.44) |
| 75 | INFJ_M_B |  | SM | `#FF0023` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 76 | INFJ_M_AB | Mn(25) | BW | `#14FF23` | substance_p(0.91) | copper_iron_complex(0.91) | chrna7_vagal(0.91) |
| 77 | INFJ_F_O | Hg(80) | BM | `#FFFF23` | bioenergetic_drive_and(0.92) | methionine(0.92) | disulfide_bond(0.92) |
| 78 | INFJ_F_A | Na(11) | SW | `#1400FF` | carbon(0.52) | cytochrome_c_oxidase(0.52) | ferritin(0.44) |
| 79 | INFJ_F_B | S(16) | SM | `#FF0023` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 80 | INFJ_F_AB | Nh(113) | BW | `#14FF23` | substance_p(0.91) | copper_iron_complex(0.91) | chrna7_vagal(0.91) |
| 81 | INTP_M_O | Ac(89) | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 82 | INTP_M_A | Be(4) | SW | `#000FFF` | carbon(0.52) | cytochrome_c_oxidase(0.49) | ferritin(0.44) |
| 83 | INTP_M_B | Eu(63) | SM | `#FF0F14` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 84 | INTP_M_AB | N(7) | BW | `#00FF14` | substance_p(0.95) | copper_iron_complex(0.95) | chrna7_vagal(0.95) |
| 85 | INTP_F_O | Nb(41) | BM | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 86 | INTP_F_A | Ir(77) | SW | `#000FFF` | carbon(0.52) | cytochrome_c_oxidase(0.49) | ferritin(0.44) |
| 87 | INTP_F_B | Fm(100) | SM | `#FF0F14` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 88 | INTP_F_AB | Tc(43) | BW | `#00FF14` | substance_p(0.95) | copper_iron_complex(0.95) | chrna7_vagal(0.95) |
| 89 | INTJ_M_O |  | BM | `#FFFF23` | bioenergetic_drive_and(0.92) | methionine(0.92) | disulfide_bond(0.92) |
| 90 | INTJ_M_A | Ba(56) | SW | `#0000FF` | carbon(0.50) | cytochrome_c_oxidase(0.49) | ferritin(0.43) |
| 91 | INTJ_M_B | Ra(88) | SM | `#FF0023` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 92 | INTJ_M_AB | Re(75) | BW | `#00FF23` | substance_p(0.92) | copper_iron_complex(0.92) | chrna7_vagal(0.92) |
| 93 | INTJ_F_O | Pd(46) | BM | `#FFFF23` | bioenergetic_drive_and(0.92) | methionine(0.92) | disulfide_bond(0.92) |
| 94 | INTJ_F_A | Pm(61) | SW | `#0000FF` | carbon(0.50) | cytochrome_c_oxidase(0.49) | ferritin(0.43) |
| 95 | INTJ_F_B | Og(118) | SM | `#FF0023` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 96 | INTJ_F_AB | Dy(66) | BW | `#00FF23` | substance_p(0.92) | copper_iron_complex(0.92) | chrna7_vagal(0.92) |
| 97 | ISFP_M_O | La(57) | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 98 | ISFP_M_A | Pu(94) | SW | `#0023FF` | carbon(0.54) | cytochrome_c_oxidase(0.50) | ferritin(0.44) |
| 99 | ISFP_M_B |  | SM | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 100 | ISFP_M_AB | I(53) | BW | `#00FF00` | substance_p(1.00) | copper_iron_complex(1.00) | chrna7_vagal(1.00) |
| 101 | ISFP_F_O | Bh(107) | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 102 | ISFP_F_A | He(2) | SW | `#0023FF` | carbon(0.54) | cytochrome_c_oxidase(0.50) | ferritin(0.44) |
| 103 | ISFP_F_B | Cm(96) | SM | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 104 | ISFP_F_AB | Np(93) | BW | `#00FF00` | substance_p(1.00) | copper_iron_complex(1.00) | chrna7_vagal(1.00) |
| 105 | ISFJ_M_O | Mc(115) | BM | `#FFFF0F` | bioenergetic_drive_and(0.97) | methionine(0.97) | disulfide_bond(0.97) |
| 106 | ISFJ_M_A | Ts(117) | SW | `#0014FF` | carbon(0.52) | cytochrome_c_oxidase(0.49) | ferritin(0.44) |
| 107 | ISFJ_M_B | Tl(81) | SM | `#FF140F` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 108 | ISFJ_M_AB | Rh(45) | BW | `#00FF0F` | substance_p(0.97) | copper_iron_complex(0.97) | chrna7_vagal(0.97) |
| 109 | ISFJ_F_O | No(102) | BM | `#FFFF0F` | bioenergetic_drive_and(0.97) | methionine(0.97) | disulfide_bond(0.97) |
| 110 | ISFJ_F_A | Hf(72) | SW | `#0014FF` | carbon(0.52) | cytochrome_c_oxidase(0.49) | ferritin(0.44) |
| 111 | ISFJ_F_B | Au(79) | SM | `#FF140F` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 112 | ISFJ_F_AB | Kr(36) | BW | `#00FF0F` | substance_p(0.97) | copper_iron_complex(0.97) | chrna7_vagal(0.97) |
| 113 | ISTP_M_O | Si(14) | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 114 | ISTP_M_A | O(8) | SW | `#1423FF` | carbon(0.57) | cytochrome_c_oxidase(0.53) | ferritin(0.46) |
| 115 | ISTP_M_B | P(15) | SM | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 116 | ISTP_M_AB | Cn(112) | BW | `#14FF00` | substance_p(0.95) | copper_iron_complex(0.95) | chrna7_vagal(0.95) |
| 117 | ISTP_F_O | Bi(83) | BM | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 118 | ISTP_F_A |  | SW | `#1423FF` | carbon(0.57) | cytochrome_c_oxidase(0.53) | ferritin(0.46) |
| 119 | ISTP_F_B | W(74) | SM | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 120 | ISTP_F_AB | U(92) | BW | `#14FF00` | substance_p(0.95) | copper_iron_complex(0.95) | chrna7_vagal(0.95) |
| 121 | ISTJ_M_O | Bk(97) | BM | `#FFFF0F` | bioenergetic_drive_and(0.97) | methionine(0.97) | disulfide_bond(0.97) |
| 122 | ISTJ_M_A | Br(35) | SW | `#1414FF` | carbon(0.55) | cytochrome_c_oxidase(0.53) | ferritin(0.45) |
| 123 | ISTJ_M_B | At(85) | SM | `#FF140F` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 124 | ISTJ_M_AB | Mt(109) | BW | `#14FF0F` | substance_p(0.94) | copper_iron_complex(0.94) | chrna7_vagal(0.94) |
| 125 | ISTJ_F_O | Se(34) | BM | `#FFFF0F` | bioenergetic_drive_and(0.97) | methionine(0.97) | disulfide_bond(0.97) |
| 126 | ISTJ_F_A | Fe(26) | SW | `#1414FF` | carbon(0.55) | cytochrome_c_oxidase(0.53) | ferritin(0.45) |
| 127 | ISTJ_F_B | Ga(31) | SM | `#FF140F` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 128 | ISTJ_F_AB | Mo(42) | BW | `#14FF0F` | substance_p(0.94) | copper_iron_complex(0.94) | chrna7_vagal(0.94) |

## 시간대별 먹을거 매핑 (선택 성격)

### ENFP_M_O (H(1))

| 시간 | 낮/밤 | 성격색 | top-1 | top-2 | top-3 |
|---|---|---|---|---|---|
| 02h | 밤 | `#FF0F14` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 08h | 낮 | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 12h | 낮 | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 18h | 밤 | `#FF0F14` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |
| 22h | 밤 | `#FF0F14` | cck(0.94) | cysteine(0.94) | proton_pump(0.94) |

### ISTP_M_O (Si(14))

| 시간 | 낮/밤 | 성격색 | top-1 | top-2 | top-3 |
|---|---|---|---|---|---|
| 02h | 밤 | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 08h | 낮 | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 12h | 낮 | `#FFFF00` | bioenergetic_drive_and(1.00) | methionine(1.00) | disulfide_bond(1.00) |
| 18h | 밤 | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 22h | 밤 | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |

### ENTJ_M_O (Ca(20))

| 시간 | 낮/밤 | 성격색 | top-1 | top-2 | top-3 |
|---|---|---|---|---|---|
| 02h | 밤 | `#FF0014` | cck(0.95) | cysteine(0.95) | proton_pump(0.95) |
| 08h | 낮 | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 12h | 낮 | `#FFFF14` | bioenergetic_drive_and(0.95) | methionine(0.95) | disulfide_bond(0.95) |
| 18h | 밤 | `#FF0014` | cck(0.95) | cysteine(0.95) | proton_pump(0.95) |
| 22h | 밤 | `#FF0014` | cck(0.95) | cysteine(0.95) | proton_pump(0.95) |

### INFJ_F_A (Na(11))

| 시간 | 낮/밤 | 성격색 | top-1 | top-2 | top-3 |
|---|---|---|---|---|---|
| 02h | 밤 | `#14FF23` | substance_p(0.91) | copper_iron_complex(0.91) | chrna7_vagal(0.91) |
| 08h | 낮 | `#1400FF` | carbon(0.52) | cytochrome_c_oxidase(0.52) | ferritin(0.44) |
| 12h | 낮 | `#1400FF` | carbon(0.52) | cytochrome_c_oxidase(0.52) | ferritin(0.44) |
| 18h | 밤 | `#14FF23` | substance_p(0.91) | copper_iron_complex(0.91) | chrna7_vagal(0.91) |
| 22h | 밤 | `#14FF23` | substance_p(0.91) | copper_iron_complex(0.91) | chrna7_vagal(0.91) |

### ESFP_M_B (Mg(12))

| 시간 | 낮/밤 | 성격색 | top-1 | top-2 | top-3 |
|---|---|---|---|---|---|
| 02h | 밤 | `#0F23FF` | carbon(0.56) | cytochrome_c_oxidase(0.52) | ferritin(0.46) |
| 08h | 낮 | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 12h | 낮 | `#FF2300` | cck(0.92) | cysteine(0.92) | proton_pump(0.92) |
| 18h | 밤 | `#0F23FF` | carbon(0.56) | cytochrome_c_oxidase(0.52) | ferritin(0.46) |
| 22h | 밤 | `#0F23FF` | carbon(0.56) | cytochrome_c_oxidase(0.52) | ferritin(0.46) |

