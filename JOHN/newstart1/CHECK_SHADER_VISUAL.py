import numpy as np
import matplotlib.pyplot as plt

# Shader constants from TRUE_RESONANCE_SHADER.html
TENSION = 1.0/9.0 - np.pi/20.0
K_LOOP = 1.0/32.0
BETTI_11 = 11.0
SPARK_RAD = 2.4239

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, 16)
ax.set_ylim(16, 0) # Inverted Y to match shader

for a_id in range(128):
    is_male = 1.0 if a_id >= 64 else 0.0
    base_x = a_id % 16.0
    
    xs, ys = [], []
    for phase in np.linspace(0, 1, 100):
        y_raw = phase * 16.0
        fold_y = 13.0 if is_male else 13.5
        is_folded = 1.0 if y_raw >= fold_y else 0.0
        in_spark = 1.0 if 10.0 <= y_raw <= 11.5 else 0.0
        
        # Destiny math from shader
        mod_aid_2 = a_id % 2.0
        destiny_x_female = 2.0 if mod_aid_2 == 0 else 8.0
        destiny_x_male = 14.0 if mod_aid_2 == 0 else 8.0
        destiny_x = destiny_x_male if is_male else destiny_x_female
        
        swirl = np.sin(y_raw * BETTI_11 * K_LOOP + a_id) * 2.0
        
        # Smoothstep equivalent
        t = y_raw / 16.0
        t = t * t * (3.0 - 2.0 * t)
        
        x_raw = base_x * (1-t) + destiny_x * t + swirl
        
        x_raw += in_spark * np.cos(SPARK_RAD) * 2.0
        y_final = y_raw + in_spark * np.sin(SPARK_RAD)
        
        x_true = 8.0 if is_folded else x_raw
        y_true = 0.5 if is_folded else y_final
        
        xs.append(x_true)
        ys.append(y_true)
        
    ax.plot(xs, ys, alpha=0.5)

plt.savefig("SHADER_MATH_CHECK.png")
print("Visual check generated.")
