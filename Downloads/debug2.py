import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Check what profiles look like
print("MBTI_TYPES:", p.MBTI_TYPES[:4])
print("GENDERS:", p.GENDERS)
print("BLOOD_TYPES:", p.BLOOD_TYPES)

# Build a few
for mbti in p.MBTI_TYPES[:2]:
    for gender in p.GENDERS[:1]:
        for blood in p.BLOOD_TYPES[:2]:
            prof = f"{mbti}_{gender}_{blood}"
            result = p.particles_to_dims(prof, 'day')
            fp = result.get('food_pigments', {})
            print(f"  {prof}: food_pigments empty? {not fp}, keys={list(fp.keys()) if fp else 'NONE'}")
            if fp:
                print(f"    1st_daily={fp.get('1st_daily','')}")
