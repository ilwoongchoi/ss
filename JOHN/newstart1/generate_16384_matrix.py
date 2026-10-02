import pandas as pd
from datetime import datetime, timedelta

def generate_micro_times():
    start_time = datetime.strptime("00:00", "%H:%M")
    micro_slots = []
    for i in range(128):
        current_slot_start = start_time + timedelta(minutes=i * 11.25)
        current_slot_end = start_time + timedelta(minutes=(i + 1) * 11.25)
        micro_slots.append(f"{current_slot_start.strftime('%H:%M')}-{current_slot_end.strftime('%H:%M')}")
    return micro_slots

def get_exhaustive_logic(mbti, gender, blood, gate_idx):
    is_e = 'E' in mbti
    is_s = 'S' in mbti
    is_t = 'T' in mbti
    is_j = 'J' in mbti
    
    # Action Logic
    action_type = "Radiative" if is_e else "Absorptive"
    mode = "Kinetic" if is_s else "Quantum"
    focus = "Structural" if is_t else "Resonance"
    action = f"{action_type} {mode} {focus} Activation"
    
    # Result Logic
    state = "Phase-Locked" if is_j else "Entropic"
    if blood == 'O':
        particle, effect = "Proton", "Ignition"
    elif blood == 'A':
        particle, effect = "Photon", "Release"
    elif blood == 'B':
        particle, effect = "Neutrino", "Flux"
    else: # AB
        particle, effect = "Beta", "Decay"
        
    result = f"{state} {particle} {effect} (Gate {gate_idx + 1})"
    
    # Delta S
    delta_s = 0.5
    if is_e: delta_s += 0.1
    if is_s: delta_s += 0.1
    if is_t: delta_s += 0.1
    if is_j: delta_s += 0.1
    if blood in ['O', 'A']: delta_s += 0.1
    
    return action, result, round(delta_s, 3)

def generate_16384_matrix():
    micro_times = generate_micro_times()
    mbtis = ['ESTP', 'ISTP', 'ESFP', 'ISFP', 'ESTJ', 'ISTJ', 'ESFJ', 'ISFJ', 
             'ENTP', 'INTP', 'ENFP', 'INFP', 'ENTJ', 'INTJ', 'ENFJ', 'INFJ']
    genders = ['M', 'F']
    bloods = ['O', 'A', 'B', 'AB']
    
    # Generate all 128 hardware configurations
    hardware_configs = []
    for b in bloods:
        for g in genders:
            for m in mbtis:
                hardware_configs.append((m, g, b))
    
    all_data = []
    # Exhaustive 16,384: 128 Hardware x 128 Time Slots
    for h_idx, (mbti, gender, blood) in enumerate(hardware_configs):
        for t_idx, time_slot in enumerate(micro_times):
            gate_idx = t_idx // 16
            action, result, delta_s = get_exhaustive_logic(mbti, gender, blood, gate_idx)
            
            all_data.append({
                'Hardware_ID': h_idx + 1,
                'Time_Slot_ID': t_idx + 1,
                'Time': time_slot,
                'MBTI': mbti,
                'Gender': gender,
                'Blood': blood,
                'Specific Action': action,
                'Phenomena Result': result,
                'Delta S': delta_s,
                'Spark Protocol': f"Refract through {blood} filter via {gender}-{mbti} hardware at {time_slot}"
            })
            
    return all_data

if __name__ == "__main__":
    data = generate_16384_matrix()
    df = pd.DataFrame(data)
    output_path = r'd:\Users\user\Documents\newstart\EXHAUSTIVE_16384_MATRIX.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Exhaustive 16,384 Matrix generated at {output_path}")

    # Generate a condensed MD summary for the user to verify structure
    md_summary = "# Exhaustive 16,384 Matrix Summary\n\n"
    md_summary += "This matrix covers every possible combination of 128 hardware configurations across 128 micro-time slots.\n\n"
    md_summary += "| Hardware ID | Time Slot | MBTI | Blood | Action | Result |\n"
    md_summary += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    for i in range(0, 16384, 128): # Show the first slot for each hardware
        r = data[i]
        md_summary += f"| {r['Hardware_ID']} | {r['Time']} | {r['MBTI']} | {r['Blood']} | {r['Specific Action']} | {r['Phenomena Result']} |\n"
        if i > 1000: break # Truncate for display
        
    with open(r'd:\Users\user\Documents\newstart\EXHAUSTIVE_16384_SUMMARY.md', 'w', encoding='utf-8') as f:
        f.write(md_summary)
