import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Encaustic beeswax fitness: g↑, h↑, p↑, nu↑, d↓
# score = g + h + p + nu - d
results = []
for mbti in p.MBTI_TYPES:
    for gender in p.GENDERS:
        for blood in p.BLOOD_TYPES:
            prof = f"{mbti}_{gender}_{blood}"
            r = p.particles_to_dims(prof, 'day')
            eqd = r.get('equation_derived', {})
            dims = eqd.get('dims_equation', r.get('dims', {}))
            
            score = dims.get('g',0) + dims.get('h',0) + dims.get('p',0) + dims.get('nu',0) - dims.get('d',0)
            results.append((prof, score, dims))

results.sort(key=lambda x: -x[1])
print("=== TOP 15 ENCAUSTIC BEESWAX (day) ===")
for prof, score, dims in results[:15]:
    elem = p.ELEMENT_MAP.get(prof, {})
    print(f"  {prof} (E{elem.get('number','')}) score={score:.3f} g={dims.get('g',0):.2f} h={dims.get('h',0):.2f} p={dims.get('p',0):.2f} nu={dims.get('nu',0):.2f} d={dims.get('d',0):.2f}")

print("\n=== BOTTOM 5 ===")
for prof, score, dims in results[-5:]:
    print(f"  {prof} score={score:.3f} g={dims.get('g',0):.2f} h={dims.get('h',0):.2f} p={dims.get('p',0):.2f} nu={dims.get('nu',0):.2f} d={dims.get('d',0):.2f}")
