import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Kitesurfing fitness: r↑, d↑, gamma↑, s↑, p↓
# score = r + d + gamma + s - p
results = []
for mbti in p.MBTI_TYPES:
    for gender in p.GENDERS:
        for blood in p.BLOOD_TYPES:
            prof = f"{mbti}_{gender}_{blood}"
            r = p.particles_to_dims(prof, 'day')
            eqd = r.get('equation_derived', {})
            dims = eqd.get('dims_equation', r.get('dims', {}))
            
            score = dims.get('r',0) + dims.get('d',0) + dims.get('gamma',0) + dims.get('s',0) - dims.get('p',0)
            results.append((prof, score, dims))

results.sort(key=lambda x: -x[1])
print("=== TOP 15 KITESURFING (day) ===")
for prof, score, dims in results[:15]:
    elem = p.ELEMENT_MAP.get(prof, {})
    print(f"  {prof} (E{elem.get('number','')}) score={score:.3f} r={dims.get('r',0):.2f} d={dims.get('d',0):.2f} gamma={dims.get('gamma',0):.2f} s={dims.get('s',0):.2f} p={dims.get('p',0):.2f}")

# Direct comparison
print("\n=== DIRECT COMPARISON ===")
targets = ['ENTJ_F_A', 'ESTP_F_O', 'ESTP_M_O', 'ENTJ_M_A', 'ISTP_M_O', 'ENTP_M_O']
for prof in targets:
    r = p.particles_to_dims(prof, 'day')
    eqd = r.get('equation_derived', {})
    dims = eqd.get('dims_equation', r.get('dims', {}))
    score = dims.get('r',0) + dims.get('d',0) + dims.get('gamma',0) + dims.get('s',0) - dims.get('p',0)
    print(f"  {prof}: score={score:.3f} r={dims.get('r',0):.2f} d={dims.get('d',0):.2f} gamma={dims.get('gamma',0):.2f} s={dims.get('s',0):.2f} p={dims.get('p',0):.2f}")
