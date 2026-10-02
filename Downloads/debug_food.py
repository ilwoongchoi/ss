import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Check profile label format
csv_profiles = ['ENTP_AB_M', 'INTP_AB_M', 'ENTJ_AB_M']
for prof in csv_profiles:
    result = p.particles_to_dims(prof, 'day')
    fp = result.get('food_pigments', {})
    print(f"{prof}: 1st={fp.get('1st_daily','')} 2nd={fp.get('2nd_daily','')} blood={fp.get('blood_daily','')}")
    print(f"  keys in result: {list(result.keys())[:10]}")
    print(f"  food_pigments type: {type(fp)}")
    if fp:
        print(f"  food_pigments keys: {list(fp.keys())}")
    print()
