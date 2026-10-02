import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Marksmanship fitness: p↑, s↑, r↓, d↓, gamma↓
# score = p + s - r - d - gamma
results = []
for mbti in p.MBTI_TYPES:
    for gender in p.GENDERS:
        for blood in p.BLOOD_TYPES:
            prof = f"{mbti}_{gender}_{blood}"
            r = p.particles_to_dims(prof, 'day')
            eqd = r.get('equation_derived', {})
            dims = eqd.get('dims_equation', r.get('dims', {}))
            
            score = dims.get('p',0) + dims.get('s',0) - dims.get('r',0) - dims.get('d',0) - dims.get('gamma',0)
            results.append((prof, score, dims))

results.sort(key=lambda x: -x[1])
print("=== TOP 15 MARKSMANSHIP (day) ===")
for prof, score, dims in results[:15]:
    elem = p.ELEMENT_MAP.get(prof, {})
    print(f"  {prof} (E{elem.get('number','')}) score={score:.3f} p={dims.get('p',0):.2f} s={dims.get('s',0):.2f} r={dims.get('r',0):.2f} d={dims.get('d',0):.2f} gamma={dims.get('gamma',0):.2f}")

# Specifically compare ISTP_M_O vs ESTJ_M_O vs ISTP_F_O vs ESTJ_F_O
print("\n=== DIRECT COMPARISON ===")
targets = ['ISTP_M_O', 'ESTJ_M_O', 'ISTP_F_O', 'ESTJ_F_O', 'ISTP_M_A', 'ESTJ_M_A']
for prof in targets:
    r = p.particles_to_dims(prof, 'day')
    eqd = r.get('equation_derived', {})
    dims = eqd.get('dims_equation', r.get('dims', {}))
    score = dims.get('p',0) + dims.get('s',0) - dims.get('r',0) - dims.get('d',0) - dims.get('gamma',0)
    print(f"  {prof}: score={score:.3f} p={dims.get('p',0):.2f} s={dims.get('s',0):.2f} r={dims.get('r',0):.2f} d={dims.get('d',0):.2f} gamma={dims.get('gamma',0):.2f}")
