import sys, csv
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Load creative_4shapes_v3.csv for model-derived activities
shapes_data = {}
with open(r'c:\Users\User\Downloads\creative_4shapes_v3.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        prof = row.get('profile', '')
        if prof:
            shapes_data[prof] = row

# Read original CSV
rows = []
with open(r'c:\Users\User\Downloads\activity.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)

# For each row, compute model state and fill blanks
output_rows = []
header = ['time', 'profile', 'music_genre', 'activity_1', 'creative_work', 'profession', 'sport_1', 'sport_2']
output_rows.append(header)

for row in rows:
    if len(row) < 2:
        continue
    while len(row) < 8:
        row.append('')
    
    time_val = row[0].strip()
    prof = row[1].strip()
    
    # CSV format: MBTI_BLOOD_GENDER -> model format: MBTI_GENDER_BLOOD
    parts = prof.split('_')
    if len(parts) != 3:
        output_rows.append(row[:8])
        continue
    mbti, blood, gender = parts[0], parts[1], parts[2]
    model_prof = f"{mbti}_{gender}_{blood}"
    
    # Compute model state
    result = p.particles_to_dims(model_prof, 'day')
    dims = result.get('dims', {})
    profile_color = result.get('profile_color', {})
    color_base = profile_color.get('base', 'MIXED')
    night_shifted = result.get('night_shifted_color', color_base)
    graviton = result.get('graviton', 0)
    em_path = result.get('em_path', 0)
    model_genre = result.get('genre', '')
    creative_shapes = result.get('creative_4shapes', {})
    
    # Get shape data from CSV
    sd = shapes_data.get(model_prof, {})
    
    # Determine time phase from hour
    hour = 0
    try:
        hour = int(time_val.split(':')[0])
    except:
        pass
    
    # Toroidal slot
    slot = p.get_toroidal_slot(hour)
    genre_type = slot.get('genre_type', 'RELEASE')
    
    # Day/night: 0-3 = AB(night), 3-9 = A(day), 9-15 = O(day), 15-21 = B(day), 21-0 = AB(night)
    is_night = (hour < 3 or hour >= 21)
    time_phase = 'night' if is_night else 'day'
    
    # Recompute with correct time phase
    result_tp = p.particles_to_dims(model_prof, time_phase)
    dims_tp = result_tp.get('dims', {})
    color_tp = result_tp.get('profile_color', {})
    color_base_tp = color_tp.get('base', 'MIXED')
    night_shifted_tp = result_tp.get('night_shifted_color', color_base_tp)
    model_genre_tp = result_tp.get('genre', '')
    graviton_tp = result_tp.get('graviton', 0)
    
    # Graviton→z_boson shift: day swaps tau→z_boson (line 212, 436-437)
    # In day: tau particle becomes z_boson (DARK-NAVY color)
    # z_boson dims: p=0.7, g=0.3 (PARTICLE_DIM_COUPLING)
    # This means: day tau profiles get z_boson influence → p↑, g↑
    # Night: tau reverts, graviton = (g+nu)/2 + night offset
    # The shift affects genre: z_boson day = structured/predictable, graviton night = deep/emergent
    
    # Creative shapes from CSV
    shape1_music = sd.get('shape1_music', '')
    shape2_music = sd.get('shape2_music', '')
    shape3_music = sd.get('shape3_music', '')
    shape4_music = sd.get('shape4_music', '')
    
    shape1_tech = sd.get('shape1_tech', '')
    shape2_tech = sd.get('shape2_tech', '')
    shape3_tech = sd.get('shape3_tech', '')
    shape4_tech = sd.get('shape4_tech', '')
    
    shape1_sport = sd.get('shape1_sport', '')
    shape2_sport = sd.get('shape2_sport', '')
    shape3_sport = sd.get('shape3_sport', '')
    shape4_sport = sd.get('shape4_sport', '')
    
    dominant_shape = creative_shapes.get('dominant', 'FLOW')
    ranked = creative_shapes.get('ranked', ['FLOW', 'CONTRAST', 'STRUCTURE', 'EMERGENCE'])
    
    # Map shapes to columns:
    # music_genre: dominant shape's music, with night color shift applied
    # activity_1: composition activity (from music genre text)
    # creative_work: shape2_tech (second dominant)
    # profession: shape3_tech (third)
    # sport_1: shape1_sport (dominant shape's sport)
    # sport_2: shape2_sport (second shape's sport)
    
    shape_idx = {'STRUCTURE': 1, 'FLOW': 2, 'CONTRAST': 3, 'EMERGENCE': 4}
    
    def get_shape_field(shape_name, field):
        idx = shape_idx.get(shape_name, 1)
        return sd.get(f'shape{idx}_{field}', '')
    
    s1 = ranked[0] if len(ranked) > 0 else 'FLOW'
    s2 = ranked[1] if len(ranked) > 1 else 'CONTRAST'
    s3 = ranked[2] if len(ranked) > 2 else 'STRUCTURE'
    s4 = ranked[3] if len(ranked) > 3 else 'EMERGENCE'
    
    model_music = get_shape_field(s1, 'music')
    model_creative = get_shape_field(s2, 'tech')
    model_profession = get_shape_field(s3, 'tech')
    model_sport1 = get_shape_field(s1, 'sport')
    model_sport2 = get_shape_field(s2, 'sport')
    
    # Apply graviton/z_boson shift to genre
    # z_boson (day): p↑ g↑ → more structured, predictable genres
    # graviton (night): g↑ nu↑ → more deep, emergent, fractal genres
    # The shift modifies which shape's music is dominant:
    # - Day with z_boson shift (tau profiles): STRUCTURE shape music (structured)
    # - Night with graviton: EMERGENCE shape music (deep/emergent)
    
    blood_gender_particle = p.BLOOD_GENDER_PARTICLE.get((blood, gender), 'photon')
    is_tau_profile = (blood_gender_particle == 'tau')
    
    if is_tau_profile and time_phase == 'day':
        # tau→z_boson day shift: pick STRUCTURE shape music
        z_boson_music = get_shape_field('STRUCTURE', 'music')
        if z_boson_music:
            model_music = z_boson_music
    
    if time_phase == 'night' and graviton_tp > 0.5:
        # graviton high at night: pick EMERGENCE shape music
        graviton_music = get_shape_field('EMERGENCE', 'music')
        if graviton_music:
            model_music = graviton_music
    
    # Night color shift for genre text
    # Men: RED→DEEP-PINK = darker/heavier genre suffix
    # Women: PINK→RED = brighter/more aggressive genre suffix
    if is_night:
        if gender == 'M' and color_base_tp in ('RED', 'RED-ORANGE', 'PINK'):
            # DEEP-PINK shift: genre becomes darker variant
            pass  # The shape music already encodes this via dim values
        elif gender == 'F' and color_base_tp in ('PINK', 'LIGHT-RED'):
            # RED shift: genre becomes brighter variant
            pass
    
    # Now fill blanks: keep original if present, use model if blank
    orig_music = row[2].strip()
    orig_act1 = row[3].strip()
    orig_creative = row[4].strip()
    orig_prof = row[5].strip()
    orig_sport1 = row[6].strip()
    orig_sport2 = row[7].strip()
    
    # Clean junk
    junk_vals = {'d', '9', '자위'}
    
    # Music genre: use original if valid, else model
    if orig_music and orig_music not in junk_vals and '자위' not in orig_music.lower():
        music = orig_music
    else:
        music = model_music
    
    # Activity 1: composition activity from original or model music
    if orig_act1 and '자위' not in orig_act1.lower():
        act1 = orig_act1
    else:
        # Derive from model music: extract genre + "composition"
        act1 = f"{model_music} composition" if model_music else ''
    
    # Creative work: original or model shape2_tech
    if orig_creative and '자위' not in orig_creative.lower():
        creative = orig_creative
    else:
        creative = model_creative
    
    # Profession: original or model shape3_tech
    if orig_prof and '자위' not in orig_prof.lower():
        profession = orig_prof
    else:
        profession = model_profession
    
    # Sport 1: original or model
    if orig_sport1 and '자위' not in orig_sport1.lower() and orig_sport1 != ' .,mn ':
        sport1 = orig_sport1.replace('teboarding', 'skateboarding').strip()
    else:
        sport1 = model_sport1
    
    # Sport 2: original or model
    if orig_sport2 and '자위' not in orig_sport2.lower():
        sport2 = orig_sport2.replace(' .,mn ', '').strip()
    else:
        sport2 = model_sport2
    
    out = [time_val, prof, music, act1, creative, profession, sport1, sport2]
    output_rows.append(out)

# Write
out_path = r'c:\Users\User\Downloads\activity_corrected.csv'
with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    for row in output_rows:
        writer.writerow(row)

print(f"Written {len(output_rows)-1} rows to {out_path}")

# Verify
print("\n=== VERIFICATION (first 15 rows) ===")
for row in output_rows[1:16]:
    print(f"  {row[1]}: music={row[2][:40]}...")
    print(f"    act1={row[3][:40]}  creative={row[4][:40]}")
    print(f"    prof={row[5][:40]}  s1={row[6][:30]}  s2={row[7][:30]}")
    print()

# Count blanks remaining
blanks = 0
for row in output_rows[1:]:
    for i, val in enumerate(row[2:], 2):
        if not val.strip():
            blanks += 1
print(f"Remaining blanks: {blanks}")
