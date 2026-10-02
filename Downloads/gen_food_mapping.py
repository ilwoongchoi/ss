import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Get food mapping for all 128 profiles
profiles = []
for mbti in p.MBTI_TYPES:
    for gender in p.GENDERS:
        for blood in p.BLOOD_TYPES:
            profiles.append(f"{mbti}_{gender}_{blood}")

print("profile,1st_daily,2nd_daily,3rd,blood_daily")
for prof in profiles:
    result = p.particles_to_dims(prof, 'day')
    fp = result.get('food_pigments', {})
    food_str = f"{fp.get('1st_daily','')};{fp.get('2nd_daily','')};{fp.get('3rd_2-3x_wk','')};{fp.get('blood_daily','')}"
    print(f"{prof},{food_str}")
