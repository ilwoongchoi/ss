import pandas as pd
import os

def generate_146_csv():
    # Define unified 146 node structure
    # 1-128: MBTI Trajectories
    # 129-136: Brain Signal Points
    # 137-144: Body Signal Points
    # 145: Origin (Pregnenolone/Zygomatics)
    # 146: Reset (Left Love/Philtrum/Endorphin)
    
    nodes = []
    
    # Placeholder/Simplified generation logic for 1-128 (using existing MD patterns)
    mbtis = ['ESTP', 'ISTP', 'ESFP', 'ISFP', 'ESTJ', 'ISTJ', 'ESFJ', 'ISFJ', 
             'ENTP', 'INTP', 'ENFP', 'INFP', 'ENTJ', 'INTJ', 'ENFJ', 'INFJ']
    genders = ['M', 'F']
    bloods = ['O', 'A', 'B', 'AB']
    
    idx = 1
    for blood in bloods:
        for gender in genders:
            for mbti in mbtis:
                nodes.append({
                    'ID': str(idx),
                    'Category': f"{mbti} {gender} {blood}",
                    'Node Name': f"Trajectory {idx}",
                    'Physical_Site': 'Various',
                    'Physics_Identity': 'MBTI Flow',
                    'Biological_Anchor': mbti,
                    'Role': 'Hardware Trajectory'
                })
                idx += 1
                if idx > 128: break
            if idx > 128: break
        if idx > 128: break

    # 129-136: Brain
    brain_points = [
        ("Spark point", "Proton", "Glutamate"),
        ("Spark point 앞", "Gluon", "Noradrenaline"),
        ("IM Understanding", "Neutrino", "Acetylcholine"),
        ("IM Under. 뒤", "Higgs", "IW-D3"),
        ("Schizo/Left Under.", "Tau", "Male GABA-A1"),
        ("Alopecia/als 뒤", "Photon", "Dopamine"),
        ("PLP", "Quark", "Male GABA-A2"),
        ("Spare vaso", "W boson", "Serotonin")
    ]
    for i, (name, phys, bio) in enumerate(brain_points):
        nodes.append({
            'ID': str(129 + i),
            'Category': 'Brain Signal',
            'Node Name': name,
            'Physical_Site': 'Brain Deep',
            'Physics_Identity': phys,
            'Biological_Anchor': bio,
            'Role': 'Ignition/Control'
        })

    # 137-144: Body
    body_points = [
        ("Genital Left", "Proton Feedback", "Spark Source"),
        ("Pancreas/Organ Muscle", "Gluon Feedback", "Noradrenaline Muscle"),
        ("Left Lung/Hypoxia", "Neutrino Feedback", "Oxygen Sensor"),
        ("Right Ribs (Jesus)", "Higgs Feedback", "Right Intercostal"),
        ("Left Procerus Bottom", "Tau Feedback", "BW/Schizo Connector"),
        ("Left Eye GABA-B Inner", "Photon Feedback", "Black Hole Sink"),
        ("Nose Patch", "Quark Feedback", "PLP Core Patch"),
        ("Appendix Muscle", "W boson Feedback", "Vaso Spare Anchor")
    ]
    for i, (name, phys, bio) in enumerate(body_points):
        nodes.append({
            'ID': str(137 + i),
            'Category': 'Body Signal',
            'Node Name': name,
            'Physical_Site': name,
            'Physics_Identity': phys,
            'Biological_Anchor': bio,
            'Role': 'Feedback Loop'
        })

    # 145-146: Origin/Reset
    nodes.append({
        'ID': '145',
        'Category': 'Origin',
        'Node Name': 'Pregnenolone (P5)',
        'Physical_Site': 'Zygomaticus Minor',
        'Physics_Identity': 'Estrogen Pivot',
        'Biological_Anchor': 'P5',
        'Role': 'Universal Birth'
    })
    nodes.append({
        'ID': '146',
        'Category': 'Reset',
        'Node Name': 'Left Love',
        'Physical_Site': 'Philtrum (Endorphin)',
        'Physics_Identity': 'Beta Decay Bridge',
        'Biological_Anchor': 'Endorphin',
        'Role': 'Spark Completion'
    })

    df = pd.DataFrame(nodes)
    output_path = r'd:\Users\user\Documents\newstart\PERSONALITY_146_MATRIX.csv'
    
    # Try to delete if exists to avoid permission issues if open in some viewers
    if os.path.exists(output_path):
        try:
            os.remove(output_path)
        except:
            print(f"Warning: Could not remove {output_path}")
            
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Generated {output_path}")

if __name__ == "__main__":
    generate_146_csv()
