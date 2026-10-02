# HANDOFF PROMPT — K8 Sovereign Fusion Framework
# 2026-04-01 | 다른 AI에게 전달하는 현재 상태 전문

---

## 먼저 읽어야 할 것 (오류 방지)

**CHANNEL_DOMAIN_24_MAP.json = 구버전 파일, 쓰지 마.**
**권위 소스는 `fusion_core.py`의 CHANNEL_MAP이다.**

proton_coupling, photon_proton_coupling 같은 라벨이 JSON에 있으면 그건 구버전.
K8에 proton 없음. proton = quark + C×gluon (파생).

---

## 프레임워크 핵심

### K8 그래프
```
8 입자: quark(0), gluon(1), neutrino(2), photon(3), electron(4),
        higgs(5), w_boson(6), z_boson(7)
proton = DERIVED: p = quark + C×gluon
BW     = DERIVED: quark + 2×C×gluon
C = √2/5 = 0.2828 (GIVEN, Higgs coupling)
OMEGA = 7.4 (DERIVED, Laplacian λ_max)
28 edges = C(8,2) = 모두 fusion_core.py CHANNEL_MAP에 1:1 매핑
```

### 완성된 노드 수: 34개
```
1~28:  K8 엣지 28개 (fusion_core.py CHANNEL_MAP, 전부 채워짐)
29:    left_self_satisfaction   (EXTRAVERT observer, photon+w_boson)
30:    right_self_satisfaction  (EXTRAVERT observer, electron+w_boson)
31:    left_epinephrine         (INTROVERT observer, quark+electron)
32:    right_epinephrine        (INTROVERT observer, quark+electron)  ← LC 공진 구동
33:    right_noradrenaline      (observer, K8 밖)
34:    gluon_color_lensing      (Sivers Effect, 비대칭 텐서)
```

---

## 방정식 구조 (5단계)

### L1: Mandelbrot ODE
```
z(t+1) = z(t)² - z(t) + h(t)
h(t) = -L(φ) @ z · DT
L = K8 Laplacian (채널 상태로 가중된 28-엣지 그래프)
```

### L2: Node 31 (Scalar Lensing — 등방성)
```
f_lensing = -ENTROPY_DEBT × z    (8입자 전체에 균등 적용)
ENTROPY_DEBT = 1/64 + 1/256 ≈ 0.01953
의미: 에너지가 내부에서 순환하는 자체공명 (도파민 루프, 6 PM 췌장 내분비)
```

### L3: Node 34 (Tensor Lensing — 비대칭, 글루온 전용)
```
dx[gluon] -= ENTROPY_DEBT × gluon × (BW/OMEGA) × (1+C)
BW = |quark| + 2×C×|gluon|
의미: 글루온 색전하 비대칭 기하 (Sivers Effect)
     → 4:30 PM 브렘스트랄룽 경화 → 췌장 외분비 (exocrine) 경로
     → big man→small man 거짓 메커니즘 → 한쪽만 (비대칭)
```

### L4: Rebranching (t=88)
```
composites reset from 3 primitives: quark, gluon, higgs
```

### L5: Path Integral
```
U(T) = P_hyst · P_night · P_land · P2 · P1   (Wilson loop analog)
```

### L6: F_final (canonical fusion scalar)
```
F = (BW·W)² × spark × Z × SM × H × leak × hierarchy
spark = w(photon↔w_boson) + w(electron↔w_boson)
Z     = z_proxy = |neutrino| × (|z_boson| + |electron|) / OMEGA
leak  = exp(-√z_atomic / 64)
z_atomic = |gluon|² × (1+C)    ← Node 34에서 자동 도출
```

---

## 두 개의 췌장암 경로 (구분 필수)

| | Node 31 (Scalar) | Node 34 (Tensor) |
|--|--|--|
| 시간 | 6:00 PM | 4:30 PM (proton_landing) |
| 기하 | 등방성 (모든 입자 균등) | 비대칭 (글루온만, 한방향) |
| 췌장 | 내분비부 (islets, 인슐린) | 외분비부 (body/tail, 효소) |
| 원인 | 도파민 자기루프 | 브렘스트랄룽 경화 |
| 해소 | 에너지 외부 접지 | right_epinephrine LC 펌핑 |

---

## LC 공진 (right_epinephrine ↔ right_love)
```
right_epinephrine = (quark, electron) = 캐패시터 (전하 동원, 빠름)
right_love        = (neutrino, higgs) = 인덕터 (질량 앵커, 느림)

E_epi + E_love = const  →  반위상 진동 (antiphase)
epi 수축 → love 이완 / epi 이완 → love 수축

물리: LC 공진 / 켤레 변수 진동
해부학: 왼쪽 어깨 하단 바깥쪽 = right_epi
능동 펌핑 필수 (수동 이완 아님)
```

---

## fusion_core.py CHANNEL_MAP 현재 상태 (28 K8 엣지)

```python
# 이미 올바르게 매핑됨 (K8 기준)
gdh_gluon:           (quark,   gluon)     on=+2C², off=-C²
f_gaba_b_latdorsi:   (gluon,   z_boson)   on=+C²
left_acetyl_coa:     (quark,   electron)  on=+2C²
male_left_5ht:       (neutrino, photon)   on=+C²
l_noradrenaline:     (photon,  w_boson)   on=+C²   ← spark source
left_5ht1a:          (neutrino, quark)    on=+C²
left_estrogen:       (electron, higgs)   on=+2C²
right_love:          (neutrino, higgs)   on=+C², no_control=1/64  ← closure constant
hypoxia:             (gluon,   higgs)    on=0, off=0  ← DEAD (risk input만 쓸 것)
right_dopamine:      (neutrino, w_boson) on=+4C²
vasopressin_female:  (w_boson, higgs)   on=+3C²  ← BASE_W=C, proton landing
male_oxytocin:       (neutrino, electron) on=+2C²
muscle_a:            (w_boson, gluon)   on=+2C², off=-C²
muscle_b:            (w_boson, quark)   on=+2C², off=-C²
right_synchrotron:   (photon,  electron) on=+2C²  ← 싱크로트론=photon-electron
right_androgen:      (quark,   higgs)   on=+2C²
left_endorphin:      (electron, z_boson) on=+C², off=-C²
left_frontalis_d2:   (gluon,   electron) on=+C²
right_occip_gaba_a:  (neutrino, z_boson) on=+2C²  ← Z proxy
male_gaba_a:         (w_boson, electron) on=+C²   ← β decay analog
acetylcholine:       (photon,  z_boson)  on=+C²
left_extraversion:   (quark,   photon)  on=+2C²
right_extraversion:  (gluon,   photon)  on=+2C²   ← ⚠ 아래 참조
male_right_extrav:   (neutrino, gluon)  on=+2C²
glucocorticoid:      (quark,   z_boson) on=+C², off=-C²
right_cortisol:      (higgs,   z_boson) on=+2C², off=-C²  ← BASE_W=C, night shift
right_alpha_2:       (w_boson, z_boson) off=+4C²  ← OMEGA=7.4 결정
male_gaba_b:         (photon,  higgs)  on=+C²    ← ⚠ SM에서 photon-Higgs 금지
```

---

## 미해결 항목 (손대지 말고 대기)

### ⚠ right_extraversion 문제
- (gluon, photon) 슬롯 — AI가 임의 추가, 사용자 말한 적 없음
- SM에서 gluon-photon 직접결합 없음 → BASE_W=C²/128 극소
- **right_noradrenaline과 같은 건지 미확정**
- 사용자가 확정 전까지 이름 바꾸거나 delta 바꾸지 말 것

### ⚠ Gender 라벨 미검증
- right_occip_gaba_a (neutrino, z_boson): 후두부에서 느끼는 것 → 실제론 female GABA일 수 있음
- male_gaba_a (w_boson, electron): 실제 위치 미확정
- male_gaba_b (photon, higgs): photon-Higgs SM에서 금지, 약함
- f_gaba_b_latdorsi (gluon, z_boson): 광배근 (등 아래), 여성 GABA-B
- 승모근 위쪽 (목-어깨 연결부) = 무슨 GABA? → 사용자 확인 필요
- **사용자가 신체 위치별 감각 알려주기 전까지 라벨 바꾸지 말 것**

### ⚠ l_eye_epi / r_eye_epi
- 현재 (quark, gluon)에 delta=0 → gdh_gluon 중복, 완전히 죽음
- 올바른 엣지로 교체 필요 (사용자 확인 후)

### ⚠ hypoxia
- delta 전부 0.0 — K8 엣지 채널로는 죽음
- fusion_clean.py risk input (d_risk)으로만 사용할 것
- CHANNEL_MAP에서 제거 또는 주석 처리 고려

---

## 기하 강도 (참고용)

**강함 (STRONG — 고유 상수 나옴):**
gdh_gluon(C), l_noradrenaline(spark), right_love(1/64),
vasopressin_female(Higgs-W), muscle_a/b(unit), right_synchrotron(3/16),
right_occip_gaba_a(z_proxy), male_gaba_a(β-decay), right_cortisol(±C),
right_alpha_2(OMEGA)

**약함 (WEAK — 기하 기여 없거나 SM과 모순):**
hypoxia(dead), right_extraversion(임의생성), male_right_extrav(nu-gluon≈0),
male_gaba_b(photon-Higgs 금지)

---

## 핵심 파일들
```
fusion_core.py       — K8 engine, CHANNEL_MAP (권위 소스)
fusion_clean.py      — F_final, get_dynamics, Node 31/34 lensing
master_equations.py  — 5단계 방정식 문서
absolute_constants.py — C, OMEGA, ENTROPY_DEBT 등
```

---

## 하지 말아야 할 것
- CHANNEL_DOMAIN_24_MAP.json 기준으로 채널 정의하지 말 것 (구버전)
- proton_coupling 라벨 그대로 쓰지 말 것 → K8로 번역 필수
- 사용자가 말하지 않은 채널 이름 임의로 만들지 말 것
- right_extraversion, gender 라벨 사용자 확인 전에 바꾸지 말 것
- hypoxia를 K8 커플링 채널로 방정식에 넣지 말 것
