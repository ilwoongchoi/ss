"""
Parse 128x5_activities.txt into structured JSON
Then overlay haplogroup overrides + geological resonance
"""

import json
import re
import os
import csv

def parse_activities_file(filepath):
    """Parse 128x5_activities.txt into structured data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by profile headers
    profile_blocks = re.split(r'### \d+\.', content)
    profile_blocks = [b.strip() for b in profile_blocks if b.strip()]
    
    results = []
    for block in profile_blocks:
        # Parse header line: "ENTP_M_AB (ENTP M AB) — heme.out1 (AB_Discharge)"
        header_match = re.match(r'(\w+)_(\w+)_(\w+)\s+\((\w+)\s+(\w+)\s+(\w+)\)\s+—\s+(\S+)\s+\((\w+)\)', block)
        if not header_match:
            continue
        
        mbti = header_match.group(1)
        gender = header_match.group(2)
        blood = header_match.group(3)
        circuit_entity = header_match.group(7)
        blood_phase = header_match.group(8)  # AB_Discharge, A_Accumulate, etc.
        
        profile_id = f"{mbti}_{gender}_{blood}"
        
        # Parse slot rows
        slot_lines = re.findall(r'\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(.*?)\s*—\s*(\S+)\s*\|\s*(\w+)/(\w+)\s*\|\s*(\w+)\s*\|\s*(.*?)\s*\|', block)
        
        slots = {}
        activities = {}
        for slot_name, state, field, activity, entity, slot_state2, field2, pigment, params in slot_lines:
            slots[slot_name] = {
                'state': state,
                'field': field,
                'circuit_entity': entity,
                'pigment': pigment,
                'params': params.strip(),
            }
            activities[slot_name] = activity.strip()
        
        results.append({
            'profile_id': profile_id,
            'mbti': mbti,
            'gender': gender,
            'blood': blood,
            'circuit_entity': circuit_entity,
            'blood_phase': blood_phase,
            'slots': slots,
            'activities': activities,
        })
    
    return results


def parse_128_master_csv(filepath):
    """Parse 128_UNIFIED_MASTER_8D.csv for 8D vectors."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = {}
        for r in reader:
            typ = r.get('Type', '').strip()
            if typ:
                rows[typ] = r
        return rows


def merge_activities_with_8d(activities, master_csv):
    """Merge parsed activities with 8D vectors from master CSV."""
    for profile in activities:
        pid = profile['profile_id']
        csv_row = master_csv.get(pid, {})
        
        # Extract 8D vector
        vec_8d = {}
        for dim in ['r', 'h', 'd', 'p', 's', 'gamma', 'g', 'nu']:
            key = f'Vector_8D_{dim.capitalize()}'
            if dim == 'gamma':
                key = 'Vector_8D_Gamma'
            val = csv_row.get(key, '')
            try:
                vec_8d[dim] = float(val)
            except (ValueError, TypeError):
                vec_8d[dim] = None
        
        profile['8d'] = vec_8d
        
        # Add extra fields from CSV
        profile['element'] = csv_row.get('Element', '')
        profile['particle'] = csv_row.get('Particle', '')
        profile['genre_release'] = csv_row.get('Genre_Release', '')
        profile['genre_stress_growth'] = csv_row.get('Genre_Stress_Growth', '')
        profile['genre_extreme_growth'] = csv_row.get('Genre_Extreme_Growth', '')
    
    return activities


def overlay_haplogroup(profiles, haplogroup='O2'):
    """Overlay haplogroup overrides on existing profiles."""
    from anchor_definitions import HAPLOGROUPS, OBSERVER_OFFSET, GEOLOGICAL_RESONANCE_WEB
    
    hg = HAPLOGROUPS.get(haplogroup, HAPLOGROUPS['DEFAULT'])
    hg_gating = hg.get('slot_gating', {})
    geo_web = GEOLOGICAL_RESONANCE_WEB.get(haplogroup, {})
    
    for profile in profiles:
        profile['haplogroup'] = haplogroup
        profile['haplogroup_name'] = hg.get('name', '')
        profile['geological_resonance'] = geo_web
        
        # Apply slot gating
        for slot_name, slot_info in profile['slots'].items():
            gating = hg_gating.get(slot_name, {})
            if gating.get('block', False):
                slot_info['blocked'] = True
                slot_info['block_reason'] = gating.get('reason', '')
            else:
                slot_info['blocked'] = False
                slot_info['block_reason'] = ''
    
    return profiles


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(base_dir)
    generated_dir = os.path.join(base_dir, 'generated')
    os.makedirs(generated_dir, exist_ok=True)
    
    # 1. Parse activities
    activities_file = os.path.join(project_dir, '128x5_activities.txt')
    print(f"Parsing {activities_file}...")
    profiles = parse_activities_file(activities_file)
    print(f"  Parsed {len(profiles)} profiles")
    
    # 2. Parse master CSV for 8D vectors
    master_csv = os.path.join(project_dir, 'circuit-app', 'renderer', '128_UNIFIED_MASTER_8D.csv')
    print(f"Parsing {master_csv}...")
    master_data = parse_128_master_csv(master_csv)
    print(f"  Parsed {len(master_data)} CSV rows")
    
    # 3. Merge
    profiles = merge_activities_with_8d(profiles, master_data)
    
    # 4. Export base (no haplogroup)
    export_path = os.path.join(generated_dir, '128x5_base.json')
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, indent=2, ensure_ascii=False)
    print(f"Exported base: {export_path}")
    
    # 5. Export with O2 haplogroup
    profiles_o2 = json.loads(json.dumps(profiles))  # deep copy
    profiles_o2 = overlay_haplogroup(profiles_o2, 'O2')
    export_o2 = os.path.join(generated_dir, '128x5_O2_korean.json')
    with open(export_o2, 'w', encoding='utf-8') as f:
        json.dump(profiles_o2, f, indent=2, ensure_ascii=False)
    print(f"Exported O2: {export_o2}")
    
    # 6. Export with R1b haplogroup
    profiles_r1b = json.loads(json.dumps(profiles))
    profiles_r1b = overlay_haplogroup(profiles_r1b, 'R1b')
    export_r1b = os.path.join(generated_dir, '128x5_R1b_european.json')
    with open(export_r1b, 'w', encoding='utf-8') as f:
        json.dump(profiles_r1b, f, indent=2, ensure_ascii=False)
    print(f"Exported R1b: {export_r1b}")
    
    # 7. Export CSV summary
    csv_path = os.path.join(generated_dir, '128x5_summary.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['profile_id', 'mbti', 'gender', 'blood', 'circuit_entity', 'blood_phase']
        header += ['r', 'h', 'd', 'p', 's', 'gamma', 'g', 'nu']
        header += ['eh_state', 'eh_field', 'eh_activity']
        header += ['mito_state', 'mito_field', 'mito_activity']
        header += ['gaba_state', 'gaba_field', 'gaba_activity']
        header += ['bili_state', 'bili_field', 'bili_activity']
        header += ['panc_state', 'panc_field', 'panc_activity']
        writer.writerow(header)
        
        for p in profiles:
            row = [p['profile_id'], p['mbti'], p['gender'], p['blood'], p['circuit_entity'], p['blood_phase']]
            row += [p['8d'].get(d, '') for d in ['r','h','d','p','s','gamma','g','nu']]
            for slot in ['electron_hole', 'mitochondria', 'gaba_c', 'bilirubin', 'pancreas']:
                s = p['slots'].get(slot, {})
                row += [s.get('state',''), s.get('field',''), p['activities'].get(slot,'')]
            writer.writerow(row)
    print(f"Exported CSV: {csv_path}")
    
    # 8. Print sample
    print(f"\n{'='*60}")
    print("Sample (first profile):")
    p = profiles[0]
    print(f"  {p['profile_id']} — {p['circuit_entity']} ({p['blood_phase']})")
    print(f"  8D: {p['8d']}")
    for slot in ['electron_hole', 'mitochondria', 'gaba_c', 'bilirubin', 'pancreas']:
        s = p['slots'].get(slot, {})
        print(f"  {slot}: {s.get('state','')} / {s.get('field','')} → {p['activities'].get(slot,'')}")
    
    print(f"\n{'='*60}")
    print("Sample (ENTP_M_O — anchor):")
    for p in profiles:
        if p['profile_id'] == 'ENTP_M_O':
            print(f"  {p['profile_id']} — {p['circuit_entity']} ({p['blood_phase']})")
            print(f"  8D: {p['8d']}")
            for slot in ['electron_hole', 'mitochondria', 'gaba_c', 'bilirubin', 'pancreas']:
                s = p['slots'].get(slot, {})
                print(f"  {slot}: {s.get('state','')} / {s.get('field','')} → {p['activities'].get(slot,'')}")
            break
    
    print(f"\nTotal: {len(profiles)} profiles × 5 slots = {len(profiles)*5} activities")


if __name__ == '__main__':
    main()
