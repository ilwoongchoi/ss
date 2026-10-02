import pandas as pd
import re
import io

def parse_personality_matrix(md_content):
    lines = md_content.split('\n')
    data = []
    header = None
    
    # Section 2.1: 128 Trajectory Nodes
    parsing_21 = False
    for line in lines:
        if '### 2.1' in line:
            parsing_21 = True
            continue
        if parsing_21:
            if '|' in line and ':---' not in line:
                parts = [p.strip() for p in line.split('|') if p.strip() or (line.startswith('|') and p == '')]
                if line.strip().startswith('|'): parts = parts[1:]
                if line.strip().endswith('|'): parts = parts[:-1]
                parts = [p.strip() for p in parts]
                
                if not parts: continue
                if parts[0].lower() == 'id':
                    header = parts
                elif header and parts[0].isdigit():
                    if len(parts) == len(header):
                        data.append(parts)
            elif '### 2.2' in line:
                parsing_21 = False
                break
    
    df_128 = pd.DataFrame(data, columns=header)
    
    # Section 2.2: 16 Signal Control Points
    parsing_22 = False
    data_22 = []
    header_22 = None
    for line in lines:
        if '### 2.2' in line:
            parsing_22 = True
            continue
        if parsing_22:
            if '|' in line and ':---' not in line:
                parts = [p.strip() for p in line.split('|') if p.strip() or (line.startswith('|') and p == '')]
                if line.strip().startswith('|'): parts = parts[1:]
                if line.strip().endswith('|'): parts = parts[:-1]
                parts = [p.strip() for p in parts]
                
                if not parts: continue
                if parts[0].lower() == 'id':
                    header_22 = parts
                elif header_22 and (parts[0].isdigit() or parts[0].endswith('*') or parts[0].isalpha()):
                    # Match rows like 129, 130...
                    data_22.append(parts)
            elif '### 2.3' in line:
                parsing_22 = False
                break
                
    df_16 = pd.DataFrame(data_22, columns=header_22)
    
    # Section 2.3: 145th Origin Node
    parsing_23 = False
    data_23 = []
    header_23 = None
    for line in lines:
        if '### 2.3' in line:
            parsing_23 = True
            continue
        if parsing_23:
            if '|' in line and ':---' not in line:
                parts = [p.strip() for p in line.split('|') if p.strip() or (line.startswith('|') and p == '')]
                if line.strip().startswith('|'): parts = parts[1:]
                if line.strip().endswith('|'): parts = parts[:-1]
                parts = [p.strip() for p in parts]
                
                if not parts: continue
                if parts[0].lower() == 'id':
                    header_23 = parts
                elif header_23 and parts[0].isdigit():
                    data_23.append(parts)
    
    df_145 = pd.DataFrame(data_23, columns=header_23)
    
    # Combine or return as separate depending on CSV needs.
    # The user asked for "PERSONALITY_145_MATRIX.csv"
    # We will create a unified CSV with all 145 nodes.
    # Since headers differ, we will align them.
    
    # Standardize columns: ID, Type/Category, Name, Biological/Neuro, Physical/Physics, Role/Humanistic, Reset/Protocol
    unified_rows = []
    for _, r in df_128.iterrows():
        unified_rows.append({
            'ID': r['ID'],
            'Category': f"{r['MBTI']} {r['Gender']} {r['Blood']}",
            'Node Name': r['Humanistic (Phenomena)'],
            'Biological_Neuro': r['Biological (Hormone/Receptor/Enzyme)'],
            'Physical_Physics': r['Physical (Force/Particle)'],
            'Role_State': r['Quantum (State/Spin)'],
            'Reset_Protocol': r['Spark Reset Protocol']
        })
    
    for _, r in df_16.iterrows():
        unified_rows.append({
            'ID': r['ID'],
            'Category': r['Category'],
            'Node Name': r['Node Name'],
            'Biological_Neuro': r['Biological Anchor'],
            'Physical_Physics': r['Physics Identity'],
            'Role_State': r['Role'],
            'Reset_Protocol': 'Signal Node'
        })
        
    for _, r in df_145.iterrows():
        unified_rows.append({
            'ID': r['ID'],
            'Category': r['Category'],
            'Node Name': r['Node Name'],
            'Biological_Neuro': r['Element'],
            'Physical_Physics': r['Physics Identity'],
            'Role_State': r['Philosophical Role'],
            'Reset_Protocol': 'Origin'
        })
        
    return pd.DataFrame(unified_rows)

def parse_node_mapping(md_content):
    lines = md_content.split('\n')
    all_nodes = []
    
    for line in lines:
        if '|' in line and ':---' not in line:
            parts = [p.strip() for p in line.split('|') if p.strip() or (line.startswith('|') and p == '')]
            if line.strip().startswith('|'): parts = parts[1:]
            if line.strip().endswith('|'): parts = parts[:-1]
            parts = [p.strip() for p in parts]
            
            if not parts or parts[0].lower() in ['id', 'target', 'node id']:
                continue
            
            # Stage 2 Table with Brain Signal Point
            if len(parts) == 6 and parts[0].startswith('**D3'):
                 all_nodes.append({
                    'ID': parts[0].replace('**', ''),
                    'Name': parts[1].replace('**', ''),
                    'Role': 'Master Gate',
                    'Receptor': parts[2].replace('**', ''),
                    'Physical_Physics': parts[3],
                    'Target_Logic': parts[4],
                    'Brain_Signal_Point': parts[5].replace('**', '')
                })
            # Other tables (Stage 1, Stage 3) as before...
            elif len(parts) == 7 and parts[0].startswith('**S1'):
                all_nodes.append({
                    'ID': parts[0].replace('**', ''),
                    'Name': parts[1].replace('**', ''),
                    'Role': parts[2],
                    'Receptor': parts[3].replace('**', ''),
                    'Physical_Physics': parts[4],
                    'Target_Logic': 'Stage 1 Seed',
                    'Brain_Signal_Point': 'N/A'
                })
            elif len(parts) == 5 and parts[2].isdigit():
                all_nodes.append({
                    'ID': f"N{parts[2]}",
                    'Name': parts[0],
                    'Role': parts[1],
                    'Receptor': parts[3].replace('**', ''),
                    'Physical_Physics': 'Interaction Matrix',
                    'Target_Logic': parts[4],
                    'Brain_Signal_Point': 'N/A'
                })

    return pd.DataFrame(all_nodes)

# Main Execution
with open(r'd:\Users\user\Documents\newstart\128_PERSONALITY_LIFE_PHENOMENA_FULL_MATRIX.md', 'r', encoding='utf-8') as f:
    matrix_content = f.read()

matrix_df = parse_personality_matrix(matrix_content)
matrix_df.to_csv(r'd:\Users\user\Documents\newstart\PERSONALITY_145_MATRIX.csv', index=False, encoding='utf-8-sig')
print("Updated PERSONALITY_145_MATRIX.csv")

with open(r'd:\Users\user\Documents\newstart\MASTER_75_NODE_MAPPING.md', 'r', encoding='utf-8') as f:
    node_content = f.read()

nodes_df = parse_node_mapping(node_content)
nodes_df.to_csv(r'd:\Users\user\Documents\newstart\MASTER_75_NODE_MAPPING.csv', index=False, encoding='utf-8-sig')
print("Updated MASTER_75_NODE_MAPPING.csv")
