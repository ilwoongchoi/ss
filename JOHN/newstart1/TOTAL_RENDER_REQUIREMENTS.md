# TOTAL RENDER REQUIREMENTS

이 문서는 통합된 기하학 계층 구조를 시각적으로 렌더링하는 데 필요한 모든 요소와 그들 사이의 관계를 `geometry_3d_renderer.py` 및 `renderer.py`의 내용을 기반으로 정의합니다.

---

## 1. Global Coordinate System & Scaling (전역 좌표계 및 스케일링)

-   **Primary Scaling Factor (`L0`)**: 렌더링의 기준이 되는 전역 스케일 팩터입니다. `GEOMETRY_EQUATIONS.md`에 따르면 다음과 같이 정의됩니다.
    -   `L0 = 10 / r_terminus`
    -   **`r_terminus`**는 TDA(Topological Data Analysis)에서 결정되는 닫힘 경계(closure boundary)의 반경입니다. (`absolute_constants.py`의 `SH_R_STAR` 또는 `CALIBRATED_SH_R_STAR`에 해당)
    -   이 스케일링을 통해 `r_terminus`는 항상 렌더링 공간에서 반경이 10인 외부 컨테이너 구체로 그려집니다.

## 2. Geometric Primitives & Their Sources (기하학적 프리미티브 및 소스)

아래는 렌더링되어야 할 핵심 기하학적 객체들과 그 데이터를 가져와야 할 소스 상수입니다.

### **Core Structural Frames (핵심 구조 프레임)**

1.  **Outer Container Sphere (외부 컨테이너 구체)**
    -   **Source**: `r_terminus`
    -   **Description**: TDA 경계를 나타내며, 모든 기하학적 객체를 담는 가장 바깥쪽의 투명한 구체입니다. 반경은 `10`으로 고정됩니다.

2.  **Event Horizon Sphere (사건의 지평선 구체)**
    -   **Source**: `EVENT_HORIZON_RADIUS_RS`
    -   **Description**: 우주론적 경계를 나타내는 내부 구체입니다. 반경은 `EVENT_HORIZON_RADIUS_RS * L0`로 계산됩니다.

3.  **Void Disk (Void 디스크)**
    -   **Source**: `W7_EXACT (π/20)`
    -   **Description**: Level 1의 기본 연속 법칙을 나타내는 2D 원반입니다. 반경은 `sqrt(W7_EXACT / π) * L0`로 계산됩니다. Betti 7 복합체의 핵심 요소입니다.

### **Betti Topology Frames (Betti 위상 프레임)**

1.  **Betti-7 Composite Frame (Betti-7 복합 프레임)**
    -   **Source**: `Betti-7`의 7개 노드 정의 (`MOBIUS_CONTINUOUS_GEOMETRY.md`)
    -   **Description**: Void Disk를 중심으로 7개의 차원(0D~Fake 3D)을 각각 다른 기하학적 형태로 시각화합니다.
        -   **0D (Point)**: Void의 남극에 위치한 점.
        -   **1D (Line)**: Void의 적도를 도는 수평선.
        -   **1D (Vertical)**: Void의 중심을 관통하는 Z축.
        -   **2D (Plane)**: Void를 가로지르는 평면.
        -   **3D (Volume)**: 나선형으로 흐르는 입체적인 흐름.
        -   **Fake 3D (Shell)**: 3D Volume을 감싸는 단단한 와이어프레임 껍질 (`Right Cortisol`).

2.  **Betti-5 Metabolic Debt Ring (Betti-5 대사 부채 링)**
    -   **Source**: `Betti-5`
    -   **Description**: 5개의 노드로 구성된 폴리곤 링입니다. 일반적으로 Void 아래에 위치하며, 에너지 소모(엔트로피)를 시각적으로 나타냅니다.

3.  **Betti-11 Topology Bridge Ring (Betti-11 위상 브릿지 링)**
    -   **Source**: `Betti-11`
    -   **Description**: 11개의 노드로 구성된 폴리곤 링입니다. 일반적으로 Void 위에 위치하며, 매니폴드를 닫는 고차원 연결을 시각적으로 나타냅니다.

### **Discrete & Dynamic Elements (이산 및 동적 요소)**

1.  **Discrete Shells (이산 껍질)**
    -   **Source**: `1/16`, `1/32`, `1/64`, `1/128`, `3/32`
    -   **Description**: Level 3의 게이트들을 나타내는 동심원의 투명한 구체들입니다. 각 구체의 반경은 `R_T * (1 - fraction)` 공식 또는 특정 위치에 대한 절대값으로 계산될 수 있습니다. `1/128` 껍질은 '붕괴' 상태를 나타내는 특별한 시각적 처리가 필요할 수 있습니다.

2.  **Maxwell Torus (맥스웰 토러스)**
    -   **Source**: `MAXWELL_R_MAJOR`, `MAXWELL_R_MINOR`
    -   **Description**: 캐비티 앵커(cavity anchor)를 나타내는 토러스입니다. Void Disk의 크기에 비례하여 렌더링됩니다.

3.  **Spark Vector (스파크 벡터)**
    -   **Source**: `SPARK_ANGLE_DEG`, `SPARK_LEAP_DIST`
    -   **Description**: Level 4의 핵심 연산자를 나타내는 단일 벡터입니다. `3/32` 게이트와 `W7` 디스크가 만나는 지점에서 시작하여, `138.88°` 각도로 `2.5 * L0` 길이만큼 공간을 관통하는 화살표로 표현됩니다.

4.  **Main Fractal Surface (주 프랙탈 표면)**
    -   **Source**: `geometry_3d_renderer.py`의 `_cristae_fractal_surface` 로직
    -   **Description**: Betti-11과 다양한 kappa 상수들의 상호작용을 통해 생성되는, 시스템의 주된 지형(terrain)과 같은 복잡한 프랙탈 표면입니다. 이는 여러 법칙이 중첩된 최종적인 시각적 결과물 중 하나입니다.

5.  **128-Grid Trajectories (128-그리드 궤적)**
    -   **Source**: `UPDATED_generate_128_grid_v4_hysteresis_pure.py`의 `TrajectoryGenerator`
    -   **Description**: `TOTAL_CANONICAL_GEOMETRY_HIERARCHY.md`의 모든 법칙이 적용된 최종 결과물입니다. 128개의 개별 궤적을 2D 또는 3D 공간에 그려야 합니다. 각 궤적의 색상, 두께 등은 MBTI, 혈액형, 성별에 따라 다르게 표현될 수 있습니다. `is_flash` 상태가 `True`일 때 궤적에 특별한 시각 효과(예: 밝은 점)를 추가해야 합니다.

## 3. Rendering Logic & Dependencies (렌더링 로직 및 의존성)

-   **Canonical Python Renderer**: `geometry_3d_renderer.py`는 모든 상위 계층의 법칙들이 어떻게 하나의 복잡한 3D 객체(프랙탈 표면)로 통합되는지에 대한 참조 구현을 제공합니다.
-   **Pure 2D Renderer**: `renderer.py`는 Level 1과 Level 3의 충돌(Pi vs Fractions)과 그 결과인 Spark 연산자를 2D 평면에서 명확하게 시각화하는 데 중점을 둡니다.
-   **Law-Driven Grid Generator**: `UPDATED_generate_128_grid_v4_hysteresis_pure.py`는 최종적인 Level 7의 `128-Grid`를 생성하고, 이를 2D로 시각화하는 로직을 포함합니다.
-   **Data Dependency**: 모든 렌더러는 `absolute_constants.py`의 상수 값에 직접적으로 의존해야 합니다. 렌더링 코드 내에 하드코딩된 물리 상수가 있어서는 안 됩니다. 동적인 값을 계산해야 할 때는 `universal_equation.py`의 함수를 호출해야 합니다.

이 요구사항들은 모든 기하학적 요소가 단일화된 법칙과 상수로부터 일관성 있게 시각화되도록 보장합니다.
