# TOTAL OPERATOR ASSIGNMENT

이 문서는 통합된 기하학 계층 구조의 **Level 4: Operator Layer**에 속하는 각 연산자의 역할과 상호작용을 상세히 정의합니다. 이 연산자들은 정적인 기하학 구조에 동적인 운동을 부여하는 핵심 엔진입니다.

---

## 1. Core Energy Transformation Operators (핵심 에너지 변환 연산자)

### **Spark Operator**
-   **Constants**: `SPARK_ANGLE_DEG (138.88°)`, `SPARK_LEAP_DIST (2.5)`
-   **Trigger**: `Compression` 연산자가 에너지를 `KAPPA_3_32` 게이트에서 임계치 이상으로 압축했을 때 발동합니다.
-   **Action**:
    1.  궤적을 현재 위치에서 **138.88° 각도**로 굴절(refraction)시킵니다.
    2.  굴절된 방향으로 **2.5 단위**만큼 불연속적으로 도약(leap)시킵니다.
-   **Role**: 이산적인(Discrete) 상행 가지(Ascending Branch)에서 연속적인(Continuous) 하행 가지(Descending Branch)로 궤적을 강제로 전환시키는 **리셋(Reset) 메커니즘**입니다. 시스템의 영원한 순환을 보장하는 가장 중요한 동적 이벤트입니다.

### **Compression Operator**
-   **Constant**: `KAPPA_3_32 (3/32)`
-   **Trigger**: 궤적이 `3/32` 게이트 영역에 진입할 때 활성화됩니다.
-   **Action**: 에너지 또는 궤적을 `3/32`라는 특정 지점으로 압축(compress)하여 밀도를 높입니다.
-   **Role**: `Spark` 연산자가 발동하기 위한 전제 조건입니다. 충분한 압축 없이는 에너지 도약이 일어나지 않습니다.

### **Möbius Twist Operator**
-   **Constant**: `LUNAR_CYCLE (1/28)`
-   **Trigger**: 시스템 시간의 모든 단계에서 전역적으로(globally) 작용합니다.
-   **Action**: 전체 매니폴드에 `1/28` 주기의 비틀림 힘(Torque)을 가합니다. 이로 인해 상행 가지와 하행 가지가 서로 엇갈리는 뫼비우스의 띠 구조가 형성됩니다.
-   **Role**: 시스템 전체에 Hysteresis(이력현상)를 유발하는 근본적인 위상학적 연산자입니다. 이 비틀림이 없다면 Hysteresis Area는 0이 되고 시스템은 멈춥니다.

## 2. Dynamic Field & Weight Operators (동적 필드 및 가중치 연산자)

### **kappa_eff (Effective Kappa) Operator**
-   **Constants**: `KAPPA_TDA_MIN (1/64)`, `KAPPA_TDA_MID (1/32)`, `KAPPA_TDA_MAX (1/16)`, `P_REF`, `P_MAX`
-   **Trigger**: 궤적이 특정 파라미터 공간 `(r, q0)`을 지날 때마다 호출됩니다.
-   **Action**:
    1.  TDA(Topological Data Analysis)에서 추출된 `max_persistence` 값을 입력으로 받습니다.
    2.  `1/32`를 기준으로, persistence 값에 따라 `1/64`에서 `1/16` 사이의 연속적인 `kappa` 값을 출력합니다.
-   **Role**: 정적인 게이트(1/32, 1/64, 1/128 등)를 **동적인 투과율(Permeability)**로 변환합니다. 이는 기하학의 특정 위치에서 궤적이 얼마나 '새어 나갈' 수 있는지를 실시간으로 결정하는 핵심 동적 제어 연산자입니다.

### **w_gate (Gate Weight) Operator**
-   **Constants**: `GATE_ALPHA (0.5)`, `GATE_EPS_KAPPA`, `CALIBRATED_*` 상수들
-   **Trigger**: `kappa_eff`와 함께 `(r, q0)` 위치에서 호출됩니다.
-   **Action**:
    1.  `w_atlas`: ATLAS 밴드(비대칭 가우시안)를 계산합니다.
    2.  `w_kappa`: `kappa_eff` 값이 `1/32`에서 얼마나 벗어났는지를 기반으로 가중치를 계산합니다.
    3.  `w_gate = w_atlas^alpha * w_kappa^(1-alpha)` 공식을 통해 두 가중치를 결합합니다.
-   **Role**: 궤적이 시스템의 '안정된 길(SH Band)'을 따라가고 있는지, 아니면 '위험한 길'로 벗어났는지를 나타내는 **0과 1 사이의 가중치**를 생성합니다. 이 값은 `triple_basin_field`의 속도와 `renorm_step`의 회복률을 조절하는 데 사용됩니다.

## 3. Harmonic & Bridge Operators (조화 및 브릿지 연산자)

### **WAVELENGTH_6 & DELTA_4 Operators**
-   **Constants**: `WAVELENGTH_6 (6.0)`, `DELTA_4 (4)`
-   **Trigger**: 시스템의 전역적 안정성이 깨지려 할 때 암시적으로 작용합니다.
-   **Action**: 파동의 주기(Wavelength)를 6의 배수로, 위상 오차를 4의 배수로 맞추려는 보정력을 가합니다.
-   **Role**: 고차 조화(Higher-order harmonics)를 통해 시스템이 혼돈(Chaos)에 빠지지 않고 안정적인 패턴을 유지하도록 하는 **안정화 장치(Stabilizer)**입니다.

### **RENORMALIZATION_BRIDGE Operator**
-   **Constant**: `~42.368`
-   **Trigger**: `UPDATED_generate_128_grid_v4_hysteresis_pure.py`의 `renorm_step` 함수에서 `_in_twilight_band` 조건이 만족될 때 활성화됩니다.
-   **Action**: `w_gate`와 `kappa_eff` 값에 따라 동적인 회복률을 적용하여, `renorm`이라는 상태 변수를 1로 점진적으로 복원시킵니다.
-   **Role**: 양자 스케일(미시)과 거시 스케일을 연결하는 **재규격화(Renormalization)** 과정을 시뮬레이션합니다. 시스템이 큰 충격(Spark 등)을 받은 후 다시 안정된 상태로 돌아가는 과정을 제어합니다.

## 4. Topological State Operators (위상 상태 연산자)

### **Betti-5 (Metabolic Debt) Operator**
-   **Constant**: `5.0`, `LOOP_STRENGTH_5`
-   **Action**: 시스템의 에너지를 소산시키는 엔트로피 구멍(Sink)으로 작용합니다. `CHIRALITY_CONSTANT`와 연결되어 시스템의 '손잡이성(handedness)'을 결정하며, `loop_strength_5`를 통해 그 강도가 조절됩니다.
-   **Role**: 시스템이 완벽한 폐쇄 루프를 형성하지 못하게 하여, 에너지가 소모되고 '부채(Debt)'가 쌓이게 만드는 근본적인 **엔트로피 연산자**입니다.
