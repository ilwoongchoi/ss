import sys, csv
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Build food mapping
food_map = {}
for mbti in p.MBTI_TYPES:
    for gender in p.GENDERS:
        for blood in p.BLOOD_TYPES:
            prof = f"{mbti}_{gender}_{blood}"
            result = p.particles_to_dims(prof, 'day')
            fp = result.get('food_pigments', {})
            food_map[prof] = f"{fp.get('1st_daily','')} | {fp.get('2nd_daily','')} | {fp.get('blood_daily','')}"

# Read original CSV and check profile matching
with open(r'c:\Users\User\Downloads\activity.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i < 3:
            prof = row[1].strip() if len(row) > 1 else ''
            print(f"CSV profile: '{prof}' (len={len(prof)}) -> in food_map: {prof in food_map}")
            # Check char by char
            for j, c in enumerate(prof):
                print(f"  char {j}: '{c}' (ord={ord(c)})")
