"""Canonical engine constants.
All numeric parameters collected from repository documentation.
Import this module anywhere constants are needed.
"""
from __future__ import annotations

import math

# Fundamental coupling constants
C: float = math.sqrt(2.0) / 5.0  # ≈0.2828427125
C2: float = C * C  # 0.08

# Homeostasis equilibrium scaling
OMEGA: float = 7.4

# Spark parameters
SPARK_ANGLE_DEG: float = 138.88
SPARK_ANGLE_RAD: float = math.radians(SPARK_ANGLE_DEG)
NEUTRON_TIME_SYNC: float = 0.3857

# Complex spark constant C_spark = NEUTRON_TIME_SYNC * e^{i θ}
SPARK_CONSTANT_C: complex = NEUTRON_TIME_SYNC * math.e ** (1j * SPARK_ANGLE_RAD)  # type: ignore[arg-type]

# Risk-memory dynamics ṙ = -λ r + M d_risk
LAMBDA_RISK_DECAY: float = 0.05
M_RISK_GAIN: float = 0.20

# Gate default inputs
NOR_DEFAULT: float = 5.0 / 32.0
PLP_DEFAULT: float = 3.0 / 32.0
BINDING_IMPEDANCE: float = 0.25  # 1/4

# Derived values
SPARK_MAGNITUDE: float = abs(SPARK_CONSTANT_C)
