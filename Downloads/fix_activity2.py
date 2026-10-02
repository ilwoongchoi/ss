import sys, csv
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Build food mapping for all 128 profiles
food_map = {}
for mbti in p.MBTI_TYPES:
    for gender in p.GENDERS:
        for blood in p.BLOOD_TYPES:
            prof = f"{mbti}_{gender}_{blood}"
            result = p.particles_to_dims(prof, 'day')
            fp = result.get('food_pigments', {})
            food_map[prof] = f"{fp.get('1st_daily','')} | {fp.get('2nd_daily','')} | {fp.get('blood_daily','')}"

# Genre mapping based on 8D dims
def get_genre_for_profile(prof, time_phase='day'):
    result = p.particles_to_dims(prof, time_phase)
    dims = result.get('dims', {})
    sorted_dims = sorted(dims.items(), key=lambda x: -x[1])
    top1, top2 = sorted_dims[0][0], sorted_dims[1][0]
    parts = prof.split('_')
    mbti, gender, blood = parts[0], parts[1], parts[2]
    
    genre_map = {
        'r': {
            'day': ['hyperpop', 'deconstructed club', 'witch house', 'IDM', 'electronic experimental'],
            'night_m': ['dark ambient', 'power electronics', 'noise', 'industrial'],
            'night_f': ['hyperpop', 'deconstructed club', 'synthpop', 'electropop'],
        },
        'h': {
            'day': ['hauntology', 'neo-classical', 'Boards of Canada adj', 'folktronic', 'ambient folk'],
            'night_m': ['dark folk', 'neoclassical darkwave', 'hauntology', 'drone folk'],
            'night_f': ['art pop', 'chamber pop', 'neo-classical', 'dream pop'],
        },
        'd': {
            'day': ['drone', 'dark ambient', 'noise', 'power electronics', 'doom'],
            'night_m': ['funeral doom', 'dark ambient', 'drone metal', 'power electronics'],
            'night_f': ['post-metal', 'shoegaze', 'dark wave', 'gothic rock'],
        },
        'p': {
            'day': ['indie folk', 'britpop', 'ambient', 'minimalistic', 'post-rock'],
            'night_m': ['minimalistic ambient', 'drone', 'neo-classical', 'post-rock'],
            'night_f': ['indie pop', 'art pop', 'chamber pop', 'baroque pop'],
        },
        's': {
            'day': ['witch house', 'electronic experimental', 'hyperpop', 'IDM', 'synthwave'],
            'night_m': ['dark ambient', 'dungeon synth', 'atmospheric black metal', 'drone'],
            'night_f': ['electropop', 'synthpop', 'new wave', 'art pop'],
        },
        'gamma': {
            'day': ['cinematic', 'Hans Zimmer adj', 'post-rock', 'orchestral', 'epic'],
            'night_m': ['post-metal', 'atmospheric black metal', 'cinematic drone', 'dark ambient'],
            'night_f': ['cinematic pop', 'symphonic', 'art rock', 'post-rock'],
        },
        'g': {
            'day': ['piano', 'ambient', 'minimalistic', 'neo-classical', 'drone'],
            'night_m': ['dark ambient', 'drone', 'dungeon synth', 'minimalist piano'],
            'night_f': ['piano pop', 'ambient pop', 'chamber', 'neo-classical'],
        },
        'nu': {
            'day': ['free jazz', 'drone', 'piano', 'avant-garde', 'experimental'],
            'night_m': ['drone', 'dark ambient', 'free jazz fragmentation', 'noise'],
            'night_f': ['experimental pop', 'art pop', 'neo-classical', 'ambient'],
        },
    }
    
    def pick(dim, phase):
        if phase == 'night_m':
            pool = genre_map[dim]['night_m']
        elif phase == 'night_f':
            pool = genre_map[dim]['night_f']
        else:
            pool = genre_map[dim]['day']
        seed = hash(prof + dim + phase) % len(pool)
        return pool[seed]
    
    if gender == 'M':
        g1 = pick(top1, 'night_m')
        g2 = pick(top2, 'night_m')
    else:
        g1 = pick(top1, 'night_f')
        g2 = pick(top2, 'night_f')
    
    return f"{g1} / {g2}"

# Read original CSV
rows = []
with open(r'c:\Users\User\Downloads\activity.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)

# Build corrected CSV
output_rows = []
header = ['time', 'profile', 'music_genre', 'activity_1', 'creative_work', 'profession', 'sport_1', 'sport_2', 'food_mapping']
output_rows.append(header)

for row in rows:
    if len(row) < 2:
        continue
    # Pad row
    while len(row) < 8:
        row.append('')
    
    time_val = row[0].strip()
    prof = row[1].strip()
    
    # Get food mapping
    food = food_map.get(prof, 'N/A')
    
    # Get corrected genre for blanks/junk
    corrected_genre = get_genre_for_profile(prof, 'day')
    orig_music = row[2].strip()
    
    # Fix blanks and junk entries
    if orig_music == '' or orig_music == 'd' or orig_music == '9' or orig_music.lower() == '자위':
        music = corrected_genre
    else:
        music = orig_music
    
    # Clean other columns
    activity1 = row[3].strip().replace('자위', '').strip()
    creative = row[4].strip()
    profession = row[5].strip()
    sport1 = row[6].strip().replace('teboarding', 'skateboarding')
    sport2 = row[7].strip().replace(' .,mn ', '').replace('자위', '').strip()
    
    out = [time_val, prof, music, activity1, creative, profession, sport1, sport2, food]
    output_rows.append(out)

# Write with utf-8-sig for Excel compatibility
out_path = r'c:\Users\User\Downloads\activity_corrected.csv'
with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    for row in output_rows:
        writer.writerow(row)

print(f"Written {len(output_rows)-1} rows to {out_path}")

# Verify food column
print("\n=== VERIFICATION (first 5 rows) ===")
for row in output_rows[1:6]:
    print(f"  {row[1]}: music={row[2][:30]}... food={row[8][:50]}...")

# Hania Rani analysis
print("\n=== HANIA RANI ===")
print("Genre: Neo-classical / contemporary classical / electronic classical")
print("Style: Piano + synthesizer + vocals, minimalist, haunting, atmospheric")
print()

hania_scores = []
for mbti in p.MBTI_TYPES:
    for gender in p.GENDERS:
        for blood in p.BLOOD_TYPES:
            prof = f"{mbti}_{gender}_{blood}"
            result = p.particles_to_dims(prof, 'day')
            dims = result.get('dims', {})
            score = dims.get('g',0)*1.5 + dims.get('h',0)*1.2 + dims.get('nu',0)*1.0 + dims.get('p',0)*0.8 + dims.get('gamma',0)*0.5
            hania_scores.append((prof, score, dims))

hania_scores.sort(key=lambda x: -x[1])
print("TOP 10 profiles for Hania Rani (g↑ h↑ nu↑ p↑):")
for prof, score, dims in hania_scores[:10]:
    elem = p.ELEMENT_MAP.get(prof, {})
    print(f"  {prof} (E{elem.get('number','')}) score={score:.3f} g={dims.get('g',0):.2f} h={dims.get('h',0):.2f} nu={dims.get('nu',0):.2f} p={dims.get('p',0):.2f}")
