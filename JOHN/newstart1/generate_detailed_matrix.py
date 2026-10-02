import pandas as pd
from datetime import datetime, timedelta

def generate_micro_times():
    start_time = datetime.strptime("00:00", "%H:%M")
    micro_slots = []
    # 24 hours = 1440 minutes. 1440 / 128 = 11.25 minutes per slot.
    for i in range(128):
        current_slot_start = start_time + timedelta(minutes=i * 11.25)
        current_slot_end = start_time + timedelta(minutes=(i + 1) * 11.25)
        micro_slots.append(f"{current_slot_start.strftime('%H:%M')}-{current_slot_end.strftime('%H:%M')}")
    return micro_slots

def generate_detailed_128_matrix():
    micro_times = generate_micro_times()
    
    mbtis = ['ESTP', 'ISTP', 'ESFP', 'ISFP', 'ESTJ', 'ISTJ', 'ESFJ', 'ISFJ', 
             'ENTP', 'INTP', 'ENFP', 'INFP', 'ENTJ', 'INTJ', 'ENFJ', 'INFJ']
    genders = ['M', 'F']
    bloods = ['O', 'A', 'B', 'AB']
    
    rows = []
    idx = 0
    for blood in bloods:
        for gender in genders:
            for mbti in mbtis:
                if idx >= 128: break
                
                # Logic for Action/Result based on particle dynamics and MBTI
                if 'T' in mbti:
                    action = "Metabolic Combustion / Logic Structuring"
                    result = "Entropy Reduction / Kinetic Stability"
                else:
                    action = "Neuro-Resonance / Social Bonding"
                    result = "Coherence Increase / Entropic Flow"
                
                if blood == 'O':
                    reset_protocol = "Proton Ignition Reset"
                elif blood == 'A':
                    reset_protocol = "Photon Release Reset"
                elif blood == 'B':
                    reset_protocol = "Neutrino Transition Reset"
                else:
                    reset_protocol = "Beta Decay Reset"

                rows.append({
                    'ID': idx + 1,
                    'Micro-Time': micro_times[idx],
                    'MBTI': mbti,
                    'Gender': gender,
                    'Blood': blood,
                    'Specific Action': action,
                    'Phenomena Result': result,
                    'Spark Reset Protocol': reset_protocol
                })
                idx += 1
                
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate_detailed_128_matrix()
    output_path = r'd:\Users\user\Documents\newstart\DETAILED_128_MICRO_MATRIX.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    # Generate MD Table content
    md_table = "| ID | Micro-Time | MBTI | Gender | Blood | Specific Action | Phenomena Result | Spark Reset Protocol |\n"
    md_table += "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    for _, r in df.iterrows():
        md_table += f"| {r['ID']} | {r['Micro-Time']} | {r['MBTI']} | {r['Gender']} | {r['Blood']} | {r['Specific Action']} | {r['Phenomena Result']} | {r['Spark Reset Protocol']} |\n"
    
    with open(r'd:\Users\user\Documents\newstart\DETAILED_128_MICRO_MATRIX.md', 'w', encoding='utf-8') as f:
        f.write("# Detailed 128 Micro-Time Action Matrix\n\n")
        f.write(md_table)
    
    print(f"Generated detailed matrix files at {output_path}")
