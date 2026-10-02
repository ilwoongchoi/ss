import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Check all 128 profiles for coasteering fitness
# Coasteering needs: r↑, d↑, s↑, gamma↑, p↓ (low predictability = high adaptability)
results = []
for mbti in p.MBTI_TYPES:
    for gender in p.GENDERS:
        for blood in p.BLOOD_TYPES:
            prof = f"{mbti}_{gender}_{blood}"
            r = p.particles_to_dims(prof, 'day')
            dims = r.get('dims', {})
            eqd = r.get('equation_derived', {})
            dims_eq = eqd.get('dims_equation', dims)
            
            # Coasteering fitness score: r + d + s + gamma - p (high risk, high sensory, high activity, low predictability)
            score = dims_eq.get('r',0) + dims_eq.get('d',0) + dims_eq.get('s',0) + dims_eq.get('gamma',0) - dims_eq.get('p',0)
            results.append((prof, score, dims_eq))

results.sort(key=lambda x: -x[1])
print("=== TOP 10 COASTEERING (day) ===")
for prof, score, dims in results[:10]:
    elem = p.ELEMENT_MAP.get(prof, {})
    print(f"  {prof} (E{elem.get('number','')}) score={score:.3f} r={dims.get('r',0):.2f} d={dims.get('d',0):.2f} s={dims.get('s',0):.2f} gamma={dims.get('gamma',0):.2f} p={dims.get('p',0):.2f}")

print("\n=== BOTTOM 5 (worst for coasteering) ===")
for prof, score, dims in results[-5:]:
    print(f"  {prof} score={score:.3f} r={dims.get('r',0):.2f} d={dims.get('d',0):.2f} s={dims.get('s',0):.2f} gamma={dims.get('gamma',0):.2f} p={dims.get('p',0):.2f}")

# Also check night
results_n = []
for mbti in p.MBTI_TYPES:
    for gender in p.GENDERS:
        for blood in p.BLOOD_TYPES:
            prof = f"{mbti}_{gender}_{blood}"
            r = p.particles_to_dims(prof, 'night')
            dims = r.get('dims', {})
            eqd = r.get('equation_derived', {})
            dims_eq = eqd.get('dims_equation', dims)
            score = dims_eq.get('r',0) + dims_eq.get('d',0) + dims_eq.get('s',0) + dims_eq.get('gamma',0) - dims_eq.get('p',0)
            results_n.append((prof, score, dims_eq))

results_n.sort(key=lambda x: -x[1])
print("\n=== TOP 10 COASTEERING (night) ===")
for prof, score, dims in results_n[:10]:
    elem = p.ELEMENT_MAP.get(prof, {})
    print(f"  {prof} (E{elem.get('number','')}) score={score:.3f} r={dims.get('r',0):.2f} d={dims.get('d',0):.2f} s={dims.get('s',0):.2f} gamma={dims.get('gamma',0):.2f} p={dims.get('p',0):.2f}")
