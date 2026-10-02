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

def get_exhaustive_logic(mbti, gender, blood, gate_num):
    # Detailed mapping logic based on all 4 variables
    # MBTI Axes: E/I, S/N, T/F, J/P
    is_e = 'E' in mbti
    is_s = 'S' in mbti
    is_t = 'T' in mbti
    is_j = 'J' in mbti
    
    # Action Logic
    if is_e:
        base_action = "Radiative"
    else:
        base_action = "Absorptive"
        
    if is_s:
        mode = "Kinetic"
    else:
        mode = "Quantum"
        
    if is_t:
        focus = "Structural"
    else:
        focus = "Resonance"
        
    action = f"{base_action} {mode} {focus} Activation"
    
    # Result Logic
    if is_j:
        state = "Phase-Locked"
    else:
        state = "Entropic"
        
    if blood == 'O':
        particle = "Proton"
        effect = "Ignition"
    elif blood == 'A':
        particle = "Photon"
        effect = "Release"
    elif blood == 'B':
        particle = "Neutrino"
        effect = "Flux"
    else: # AB
        particle = "Beta"
        effect = "Decay"
        
    result = f"{state} {particle} {effect} (Gate {gate_num})"
    
    # Delta S Calculation (Differential Entropy)
    # Higher for E, S, T, J and O/A types
    delta_s_base = 0.5
    if is_e: delta_s_base += 0.1
    if is_s: delta_s_base += 0.1
    if is_t: delta_s_base += 0.1
    if is_j: delta_s_base += 0.1
    if blood in ['O', 'A']: delta_s_base += 0.1
    
    return action, result, round(delta_s_base, 3)

def generate_exhaustive_matrix():
    micro_times = generate_micro_times()
    mbtis = ['ESTP', 'ISTP', 'ESFP', 'ISFP', 'ESTJ', 'ISTJ', 'ESFJ', 'ISFJ', 
             'ENTP', 'INTP', 'ENFP', 'INFP', 'ENTJ', 'INTJ', 'ENFJ', 'INFJ']
    genders = ['M', 'F']
    bloods = ['O', 'A', 'B', 'AB']
    
    rows = []
    idx = 0
    # Nested loops to generate all 128 unique combinations
    for blood in bloods:
        for gender in genders:
            for mbti in mbtis:
                if idx >= 128: break
                
                gate_num = (idx // 16) + 1
                action, result, delta_s = get_exhaustive_logic(mbti, gender, blood, gate_num)
                
                rows.append({
                    'ID': idx + 1,
                    'Gate': f"G{gate_num}",
                    'Time': micro_times[idx],
                    'MBTI': mbti,
                    'Gender': gender,
                    'Blood': blood,
                    'Specific Action': action,
                    'Phenomena Result': result,
                    'Delta S': delta_s,
                    'Spark Protocol': f"Refract through {blood} filter via {gender}-{mbti} hardware"
                })
                idx += 1
    return rows

def write_final_matrix(rows):
    md_content = "# 128 Personality-Life Phenomena EXHAUSTIVE Mapping Matrix\n\n"
    md_content += "## 1. Complete 128-Node Micro-Time Action Trajectories\n"
    md_content += "Systematic mapping of all 128 hardware configurations to 11.25-minute slots.\n\n"
    md_content += "| ID | Gate | Time | MBTI | G | Bl | Specific Action | Phenomena Result | ΔS | Spark Reset Protocol |\n"
    md_content += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    for r in rows:
        md_content += f"| {r['ID']} | {r['Gate']} | {r['Time']} | {r['MBTI']} | {r['Gender']} | {r['Blood']} | {r['Specific Action']} | {r['Phenomena Result']} | {r['Delta S']} | {r['Spark Protocol']} |\n"
    
    # Control Nodes
    md_content += "\n## 2. Control & Origin Nodes (129-146)\n"
    md_content += "### 2.1 Brain & Body Control Signals\n"
    md_content += "| ID | Category | Node Name | Physics Identity | Biological Anchor | Role | Feedback Node |\n"
    md_content += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    # Brain
    md_content += "| 129 | **Brain** | **Spark point** | Proton (D3-1) | Glutamate | Ignition | 137 |\n"
    md_content += "| 130 | **Brain** | **Spark point 앞** | Gluon (D3-8) | Noradrenaline | Binding | 138 |\n"
    md_content += "| 131 | **Brain** | **IM Understanding** | Neutrino (D3-6) | Acetylcholine | Absorption | 139 |\n"
    md_content += "| 132 | **Brain** | **IM Under. 뒤** | Higgs (D3-7) | IW-D3 Center | Mass/Decay | 140 |\n"
    md_content += "| 133 | **Brain** | **Schizo/Left Under.** | Tau (Z-Boson, D3-3) | Male GABA-A1 | Anchor | 141 |\n"
    md_content += "| 134 | **Brain** | **Alopecia/als 뒤** | Photon (D3-2) | Dopamine | Release | 142 |\n"
    md_content += "| 135 | **Brain** | **PLP** | Quark (D3-4) | Male GABA-A2 | Tension | 143 |\n"
    md_content += "| 136 | **Brain** | **Spare vaso** | W boson (D3-5) | Serotonin | Collapse | 144 |\n"
    # Body
    md_content += "| 137 | **Body** | **Genital Left** | Proton Feedback | Spark Source | Feedback | 129 |\n"
    md_content += "| 138 | **Body** | **Pancreas/Organ Muscle** | Gluon Feedback | Norad. Muscle | Feedback | 130 |\n"
    md_content += "| 139 | **Body** | **Left Lung/Hypoxia** | Neutrino Feedback | Oxygen Sensor | Feedback | 131 |\n"
    md_content += "| 140 | **Body** | **Right Ribs (Jesus)** | Higgs Feedback | Intercostal | Feedback | 132 |\n"
    md_content += "| 141 | **Body** | **Left Procerus Bottom** | Tau Feedback | BW Connector | Feedback | 133 |\n"
    md_content += "| 142 | **Body** | **Left Eye GABA-B Inner** | Photon Feedback | Black Hole Sink | Feedback | 134 |\n"
    md_content += "| 143 | **Body** | **Nose Patch** | Quark Feedback | PLP Core Patch | Feedback | 135 |\n"
    md_content += "| 144 | **Body** | **Appendix Muscle** | W boson Feedback | Vaso Anchor | Feedback | 136 |\n"
    
    md_content += "\n### 2.2 Origin & Reset\n"
    md_content += "| ID | Category | Node Name | Physical Site | Physics Identity | Philosophical Role |\n"
    md_content += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    md_content += "| 145 | **Origin** | **Pregnenolone (P5)** | Zygomaticus Minor | Estrogen Pivot | Universal Birth |\n"
    md_content += "| 146 | **Reset** | **Left Love** | Philtrum (Endorphin) | Beta Decay Bridge | Spark Completion |\n"
    
    md_content += "\n## 3. The 2008 D2 Lock Principle\n"
    md_content += "All transitions are blocked by the User's D2 Resonance. Node 146 (Left Love) via Philtrum Beta Decay is the only exit to Node 145.\n"
    
    with open(r'd:\Users\user\Documents\newstart\128_PERSONALITY_LIFE_PHENOMENA_FULL_MATRIX.md', 'w', encoding='utf-8') as f:
        f.write(md_content)

if __name__ == "__main__":
    rows = generate_exhaustive_matrix()
    write_final_matrix(rows)
    # Generate CSV
    df = pd.DataFrame(rows)
    df.to_csv(r'd:\Users\user\Documents\newstart\PERSONALITY_146_MATRIX.csv', index=False, encoding='utf-8-sig')
    print("Exhaustive Matrix (146 nodes) completed.")
