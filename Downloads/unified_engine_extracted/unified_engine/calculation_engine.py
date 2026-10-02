"""
Unified Calculation Engine
==========================
Computes: anchor + haplogroup + personality delta + observer offset → final 8D → slots → activities

This REPLACES manual 640-entry mapping with rule-based calculation.
"""

import json
import math
import os

from anchor_definitions import (
    ANCHOR_ID, ANCHOR_8D, ANCHOR_SLOTS,
    HAPLOGROUPS, OBSERVER_OFFSET,
    GEOLOGICAL_RESONANCE_WEB, FRACTAL_SCALES,
)
from personality_deltas import (
    MBTI_DELTAS, GENDER_DELTAS, BLOOD_DELTAS,
    SLOT_RULES, ACTIVITY_TEMPLATES,
    generate_profile_id, generate_all_profile_ids,
    DEFAULT_HAPLOGROUP,
)

DIMS = ['r', 'h', 'd', 'p', 's', 'gamma', 'g', 'nu']


def clamp(val, lo=0.0, hi=1.0):
    return max(lo, min(hi, val))


def apply_haplogroup_override(vec, haplogroup_id):
    """Apply haplogroup geological resonance override to 8D vector."""
    hg = HAPLOGROUPS.get(haplogroup_id, HAPLOGROUPS['DEFAULT'])
    out = dict(vec)
    for dim, rule in hg.get('overrides', {}).items():
        if dim not in out:
            continue
        if 'mul' in rule:
            out[dim] = out[dim] * rule['mul']
        if 'fix' in rule:
            out[dim] = rule['fix']
        if 'clamp_max' in rule:
            out[dim] = min(out[dim], rule['clamp_max'])
        if 'clamp_min' in rule:
            out[dim] = max(out[dim], rule['clamp_min'])
        out[dim] = clamp(out[dim])
    return out


def apply_personality_delta(vec, mbti, gender, blood):
    """Apply MBTI + gender + blood delta to 8D vector."""
    out = dict(vec)
    for dim in DIMS:
        delta = 0.0
        delta += MBTI_DELTAS.get(mbti, {}).get(dim, 0.0)
        delta += GENDER_DELTAS.get(gender, {}).get(dim, 0.0)
        delta += BLOOD_DELTAS.get(blood, {}).get(dim, 0.0)
        out[dim] = clamp(out[dim] + delta)
    return out


def apply_observer_offset(vec, is_observer=False, circadian_phase=0.0):
    """Apply observer phase shift for r/nu/s.
    
    circadian_phase: 0.0-1.0 representing time of day (0=dawn, 0.5=dusk)
    Observer's r/nu/s are anti-phase to general population.
    """
    if not is_observer:
        return vec
    out = dict(vec)
    for dim in OBSERVER_OFFSET['applies_to']:
        amp = OBSERVER_OFFSET['phase_shift'][dim]['amplitude']
        # Anti-phase: when normal is high (cos(phase)), observer is low
        shift = amp * math.cos(2 * math.pi * (circadian_phase + 0.5))
        out[dim] = clamp(out[dim] + shift)
    return out


def determine_slot_states(vec, haplogroup_id='DEFAULT', is_observer=False):
    """Determine which slots are active, blocked, and in what state."""
    hg = HAPLOGROUPS.get(haplogroup_id, HAPLOGROUPS['DEFAULT'])
    hg_gating = hg.get('slot_gating', {})
    observer_unlock = OBSERVER_OFFSET.get('slot_unlock', {}) if is_observer else {}
    
    slots = {}
    for slot_name, rules in SLOT_RULES.items():
        # Check haplogroup gating
        gating = hg_gating.get(slot_name, {})
        blocked = gating.get('block', False)
        block_reason = gating.get('reason', '')
        
        # Check observer partial unlock
        if blocked and slot_name in observer_unlock:
            unlock = observer_unlock[slot_name]
            if unlock.get('partial'):
                blocked = False
                block_reason = f'PARTIALLY UNLOCKED (observer): {unlock.get("reason","")}'
        
        # Determine state
        state = 'forward'  # default
        state_rules = rules.get('state_rules', {})
        for rule_state, condition in state_rules.items():
            if _eval_condition(vec, condition):
                state = rule_state
                break
        
        slots[slot_name] = {
            'active': not blocked,
            'state': state if not blocked else 'blocked',
            'block_reason': block_reason,
            'field': ANCHOR_SLOTS.get(slot_name, {}).get('field', ''),
        }
    
    return slots


def _eval_condition(vec, condition):
    """Evaluate a simple condition string like 's >= 0.5 and d > 0.4'"""
    if not condition:
        return False
    try:
        # Safe evaluation: only allow dim names, operators, numbers, and/or
        parts = condition.split(' and ')
        for part in parts:
            part = part.strip()
            if ' or ' in part:
                or_parts = part.split(' or ')
                if any(_eval_single(vec, p.strip()) for p in or_parts):
                    continue
                else:
                    return False
            else:
                if not _eval_single(vec, part):
                    return False
        return True
    except Exception:
        return False


def _eval_single(vec, expr):
    """Evaluate single condition like 's >= 0.5'"""
    for op in ['>=', '<=', '>', '<', '==', '!=']:
        if op in expr:
            parts = expr.split(op)
            dim = parts[0].strip()
            val = float(parts[1].strip())
            actual = vec.get(dim, 0.0)
            if op == '>=': return actual >= val
            if op == '<=': return actual <= val
            if op == '>':  return actual > val
            if op == '<':  return actual < val
            if op == '==': return abs(actual - val) < 0.01
            if op == '!=': return abs(actual - val) >= 0.01
    return False


def generate_activity(slot_name, state, vec):
    """Generate activity description from slot + state + 8D vector."""
    templates = ACTIVITY_TEMPLATES.get(slot_name, {})
    state_templates = templates.get(state, {})
    
    # Select template based on 8D values
    r, h, d, p, s, gamma, g, nu = (vec.get(k, 0.5) for k in DIMS)
    
    if slot_name == 'electron_hole':
        if state == 'forward':
            if r > 0.6 and s > 0.6: return state_templates.get('high_r_high_s', state_templates.get('default'))
            if h > 0.5 and d < 0.4: return state_templates.get('high_h_low_d', state_templates.get('default'))
        elif state == 'reverse':
            if r > 0.6 and d > 0.6: return state_templates.get('high_r_high_d', state_templates.get('default'))
            if gamma > 0.6: return state_templates.get('high_gamma', state_templates.get('default'))
        elif state == 'spark':
            if nu > 0.5: return state_templates.get('high_nu', state_templates.get('default'))
            if gamma > 0.6: return state_templates.get('high_gamma', state_templates.get('default'))
    
    elif slot_name == 'mitochondria':
        if state == 'forward':
            if r > 0.6: return state_templates.get('high_r', state_templates.get('default'))
            if h > 0.5: return state_templates.get('high_h', state_templates.get('default'))
        elif state == 'reverse':
            if d > 0.5: return state_templates.get('high_d', state_templates.get('default'))
            if r > 0.6: return state_templates.get('high_r', state_templates.get('default'))
        elif state == 'spark':
            if h > 0.5 and r < 0.4: return state_templates.get('high_h_low_r', state_templates.get('default'))
    
    elif slot_name == 'gaba_c':
        if state == 'forward':
            if g > 0.5: return state_templates.get('high_g', state_templates.get('default'))
            if nu > 0.5: return state_templates.get('high_nu', state_templates.get('default'))
        elif state == 'reverse':
            if g < 0.3 and nu > 0.5: return state_templates.get('low_g_high_nu', state_templates.get('default'))
        elif state == 'spark':
            if r > 0.5 and nu < 0.4: return state_templates.get('high_r_low_nu', state_templates.get('default'))
    
    elif slot_name == 'bilirubin':
        if state in ('forward', 'reverse'):
            if gamma > 0.6: return state_templates.get('high_gamma', state_templates.get('default'))
        elif state == 'spark':
            if d > 0.5: return state_templates.get('high_d', state_templates.get('default'))
    
    elif slot_name == 'pancreas':
        if state == 'forward':
            if r > 0.5 and h > 0.5: return state_templates.get('high_r_high_h', state_templates.get('default'))
        elif state == 'reverse':
            if s > 0.5: return state_templates.get('high_s', state_templates.get('default'))
        elif state == 'spark':
            if d > 0.5: return state_templates.get('high_d', state_templates.get('default'))
    
    return state_templates.get('default', 'unknown activity')


def compute_profile(mbti, gender, blood, haplogroup='DEFAULT', is_observer=False, circadian_phase=0.0):
    """Compute full profile: 8D + slots + activities.
    
    Args:
        mbti: e.g. 'ENTP'
        gender: 'M' or 'F'
        blood: 'O', 'A', 'B', 'AB'
        haplogroup: e.g. 'O2', 'R1b', 'DEFAULT'
        is_observer: True if this is the circuit discoverer (user)
        circadian_phase: 0.0-1.0 for observer phase shift
    
    Returns:
        dict with profile_id, 8D, slots, activities, metadata
    """
    profile_id = generate_profile_id(mbti, gender, blood)
    
    # Step 1: Start from anchor
    vec = dict(ANCHOR_8D)
    
    # Step 2: Apply haplogroup override
    vec = apply_haplogroup_override(vec, haplogroup)
    
    # Step 3: Apply personality delta
    vec = apply_personality_delta(vec, mbti, gender, blood)
    
    # Step 4: Apply observer offset (if applicable)
    vec = apply_observer_offset(vec, is_observer, circadian_phase)
    
    # Step 5: Determine slot states
    slots = determine_slot_states(vec, haplogroup, is_observer)
    
    # Step 6: Generate activities
    activities = {}
    for slot_name, slot_info in slots.items():
        if slot_info['active']:
            activities[slot_name] = generate_activity(slot_name, slot_info['state'], vec)
        else:
            activities[slot_name] = f"BLOCKED: {slot_info['block_reason']}"
    
    return {
        'profile_id': profile_id,
        'mbti': mbti,
        'gender': gender,
        'blood': blood,
        'haplogroup': haplogroup,
        'is_observer': is_observer,
        'anchor': ANCHOR_ID,
        '8d': {k: round(v, 4) for k, v in vec.items()},
        'slots': slots,
        'activities': activities,
        'geological_resonance': GEOLOGICAL_RESONANCE_WEB.get(haplogroup, {}),
    }


def compute_all_128(haplogroup='DEFAULT', is_observer=False):
    """Compute all 128 profiles."""
    results = []
    for mbti in MBTI_DELTAS:
        for gender in ['M', 'F']:
            for blood in ['O', 'A', 'B', 'AB']:
                result = compute_profile(mbti, gender, blood, haplogroup, is_observer)
                results.append(result)
    return results


def compute_anchor():
    """Return the anchor profile (ENTP_M_O without any haplogroup)."""
    return compute_profile('ENTP', 'M', 'O', 'DEFAULT', is_observer=False)


def compute_anchor_with_haplogroup(haplogroup='O2'):
    """Return the anchor profile with haplogroup constraint applied."""
    return compute_profile('ENTP', 'M', 'O', haplogroup, is_observer=False)


def compute_anchor_as_observer(haplogroup='O2', circadian_phase=0.0):
    """Return the anchor as observer (user's self-model)."""
    return compute_profile('ENTP', 'M', 'O', haplogroup, is_observer=True, circadian_phase=circadian_phase)


def export_to_json(results, filepath):
    """Export results to JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(results)} profiles to {filepath}")


def export_to_csv(results, filepath):
    """Export results to CSV file."""
    import csv
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['profile_id', 'mbti', 'gender', 'blood', 'haplogroup', 'is_observer']
        header += [f'r_{d}' for d in DIMS]
        header += [f'{s}_state' for s in SLOT_RULES.keys()]
        header += [f'{s}_activity' for s in SLOT_RULES.keys()]
        writer.writerow(header)
        for r in results:
            row = [r['profile_id'], r['mbti'], r['gender'], r['blood'], r['haplogroup'], r['is_observer']]
            row += [r['8d'][d] for d in DIMS]
            row += [r['slots'].get(s, {}).get('state', '') for s in SLOT_RULES.keys()]
            row += [r['activities'].get(s, '') for s in SLOT_RULES.keys()]
            writer.writerow(row)
    print(f"Exported {len(results)} profiles to {filepath}")


# ============================================================
# MAIN: Generate and export
# ============================================================
if __name__ == '__main__':
    output_dir = os.path.dirname(os.path.abspath(__file__))
    generated_dir = os.path.join(output_dir, 'generated')
    os.makedirs(generated_dir, exist_ok=True)
    
    # 1. Anchor (no haplogroup)
    anchor = compute_anchor()
    print(f"\n{'='*60}")
    print(f"ANCHOR: {anchor['profile_id']} (no haplogroup)")
    print(f"8D: {anchor['8d']}")
    for s, info in anchor['slots'].items():
        print(f"  {s}: {info['state']} → {anchor['activities'][s]}")
    
    # 2. Anchor with O2 (Korean)
    anchor_o2 = compute_anchor_with_haplogroup('O2')
    print(f"\n{'='*60}")
    print(f"ANCHOR + O2 (Korean): {anchor_o2['profile_id']}")
    print(f"8D: {anchor_o2['8d']}")
    for s, info in anchor_o2['slots'].items():
        status = "BLOCKED" if not info['active'] else info['state']
        print(f"  {s}: {status} → {anchor_o2['activities'][s]}")
    
    # 3. Anchor as observer (user)
    anchor_obs = compute_anchor_as_observer('O2', circadian_phase=0.3)
    print(f"\n{'='*60}")
    print(f"ANCHOR + O2 + OBSERVER (user): {anchor_obs['profile_id']}")
    print(f"8D: {anchor_obs['8d']}")
    for s, info in anchor_obs['slots'].items():
        status = "BLOCKED" if not info['active'] else info['state']
        print(f"  {s}: {status} → {anchor_obs['activities'][s]}")
    
    # 4. All 128 with O2
    all_o2 = compute_all_128(haplogroup='O2')
    export_to_json(all_o2, os.path.join(generated_dir, '128_O2_korean.json'))
    export_to_csv(all_o2, os.path.join(generated_dir, '128_O2_korean.csv'))
    
    # 5. All 128 with DEFAULT (no haplogroup)
    all_default = compute_all_128(haplogroup='DEFAULT')
    export_to_json(all_default, os.path.join(generated_dir, '128_default.json'))
    export_to_csv(all_default, os.path.join(generated_dir, '128_default.csv'))
    
    # 6. All 128 with R1b (European)
    all_r1b = compute_all_128(haplogroup='R1b')
    export_to_json(all_r1b, os.path.join(generated_dir, '128_R1b_european.json'))
    export_to_csv(all_r1b, os.path.join(generated_dir, '128_R1b_european.csv'))
    
    # 7. Geological resonance web
    export_to_json(GEOLOGICAL_RESONANCE_WEB, os.path.join(generated_dir, 'geological_resonance_web.json'))
    
    print(f"\n{'='*60}")
    print(f"Done. Generated files in: {generated_dir}")
    print(f"  - 128_O2_korean.json/csv (Korean haplogroup)")
    print(f"  - 128_default.json/csv (no haplogroup)")
    print(f"  - 128_R1b_european.json/csv (European haplogroup)")
    print(f"  - geological_resonance_web.json")
