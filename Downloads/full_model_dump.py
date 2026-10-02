import sys, csv, json
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# Read original CSV
rows = []
with open(r'c:\Users\User\Downloads\activity.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)

# For each profile, compute full model state
results = []
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
        results.append(row + [''])
        continue
    mbti, blood, gender = parts[0], parts[1], parts[2]
    model_prof = f"{mbti}_{gender}_{blood}"
    
    # Compute full model state
    day_result = p.particles_to_dims(model_prof, 'day')
    night_result = p.particles_to_dims(model_prof, 'night')
    
    day_dims = day_result.get('dims', {})
    night_dims = night_result.get('dims', {})
    
    # Graviton and z_boson
    day_graviton = day_result.get('graviton', 0)
    night_graviton = night_result.get('graviton', 0)
    
    # EM path (s+gamma)
    day_em = day_result.get('em_path', 0)
    night_em = night_result.get('em_path', 0)
    
    # Genre from model
    day_genre = day_result.get('genre', '')
    night_genre = night_result.get('genre', '')
    
    # Profile color
    day_color = p.compute_profile_color(model_prof, 'day')
    night_color = p.compute_profile_color(model_prof, 'night')
    
    # 4-layer colors
    day_layers = p.compute_4layer_colors(model_prof, day_dims, 'day', 0)
    
    # Toroidal slot (use hour from time_val)
    hour = 0
    try:
        h_str = time_val.split(':')[0]
        hour = int(h_str)
    except:
        pass
    slot = p.get_toroidal_slot(hour)
    
    # Active layer
    active_layer = 'A'
    if slot.get('genre_type') == 'STRESS_GROWTH':
        active_layer = 'B'
    elif slot.get('genre_type') == 'EXTREME_GROWTH':
        active_layer = 'C'
    
    # Element
    elem = p.ELEMENT_MAP.get(model_prof, {})
    
    # Night color shift
    night_shifted = p.apply_night_color_shift(day_color.get('base', 'MIXED'), gender, 'night')
    
    info = {
        'prof': prof,
        'model_prof': model_prof,
        'time': time_val,
        'hour': hour,
        'slot': slot.get('label', ''),
        'genre_type': slot.get('genre_type', ''),
        'active_layer': active_layer,
        'elem_num': elem.get('number', ''),
        'elem_name': elem.get('name', ''),
        'day_dims': day_dims,
        'night_dims': night_dims,
        'day_graviton': day_graviton,
        'night_graviton': night_graviton,
        'day_em': day_em,
        'night_em': night_em,
        'day_genre_model': day_genre,
        'night_genre_model': night_genre,
        'day_color': day_color.get('base', ''),
        'night_color': night_color.get('base', ''),
        'night_shifted_color': night_shifted,
        'day_leakage': day_result.get('leakage', 0),
        'orig_music': row[2].strip(),
        'orig_act1': row[3].strip(),
        'orig_creative': row[4].strip(),
        'orig_prof': row[5].strip(),
        'orig_sport1': row[6].strip(),
        'orig_sport2': row[7].strip(),
    }
    results.append(info)

# Print all 128 with full model state
for r in results:
    d = r['day_dims']
    nd = r['night_dims']
    print(f"=== {r['prof']} (E{r['elem_num']}) t={r['time']} slot={r['slot']} layer={r['active_layer']} ===")
    print(f"  day_dims: r={d.get('r',0):.2f} h={d.get('h',0):.2f} d={d.get('d',0):.2f} p={d.get('p',0):.2f} s={d.get('s',0):.2f} g={d.get('g',0):.2f} gamma={d.get('gamma',0):.2f} nu={d.get('nu',0):.2f}")
    print(f"  night_dims: r={nd.get('r',0):.2f} h={nd.get('h',0):.2f} d={nd.get('d',0):.2f} p={nd.get('p',0):.2f} s={nd.get('s',0):.2f} g={nd.get('g',0):.2f} gamma={nd.get('gamma',0):.2f} nu={nd.get('nu',0):.2f}")
    print(f"  graviton: day={r['day_graviton']:.3f} night={r['night_graviton']:.3f}")
    print(f"  em_path: day={r['day_em']:.3f} night={r['night_em']:.3f}")
    print(f"  color: day={r['day_color']} night={r['night_color']} shifted={r['night_shifted_color']}")
    print(f"  genre_model: day={r['day_genre_model']} night={r['night_genre_model']}")
    print(f"  orig: music='{r['orig_music']}' act1='{r['orig_act1']}' creative='{r['orig_creative']}' prof='{r['orig_prof']}' s1='{r['orig_sport1']}' s2='{r['orig_sport2']}'")
    print()
