import json
import pandas as pd
import numpy as np
import os

def merge_unmapped_points():
    print("Initiating Final Data Unification (816 Points)...")
    
    # 1. Load Unmapped (454 points)
    unmapped_path = 'UNMAPPED_FACE_PEAKS.json'
    if not os.path.exists(unmapped_path):
        print(f"Error: {unmapped_path} not found.")
        return
        
    with open(unmapped_path, 'r') as f:
        unmapped_data = json.load(f)
    
    unmapped_df = pd.DataFrame(unmapped_data, columns=['x', 'y', 'score'])
    unmapped_df['label'] = 'PHASE_TRANSITION_ANCHOR'
    
    # 2. Load Existing (362 points)
    existing_path = 'SPHERE_POINT_LABELS.csv'
    if os.path.exists(existing_path):
        existing_df = pd.read_csv(existing_path)
        print(f"Existing Mapped Points: {len(existing_df)}")
    else:
        existing_df = pd.DataFrame(columns=['x', 'y', 'score', 'label'])
        print("Warning: No existing mapping found. Creating from scratch.")

    # 3. Concatenate and Deduplicate
    # We use a small epsilon for coordinate matching to avoid duplication of the same physical receptor
    merged = pd.concat([existing_df, unmapped_df], ignore_index=True)
    
    # Sort by coordinates to ensure stable deduplication
    merged = merged.sort_values(by=['x', 'y', 'score'], ascending=[True, True, False])
    
    # Round to 6 decimal places for extreme precision (Micro-unit scale)
    merged['x_round'] = merged['x'].round(6)
    merged['y_round'] = merged['y'].round(6)
    
    final_df = merged.drop_duplicates(subset=['x_round', 'y_round'], keep='first')
    
    # Check if we still lost too many points and adjust if necessary
    if len(final_df) < 800:
        print(f"Warning: Low point count ({len(final_df)}). Retaining original entries.")
        final_df = merged.drop_duplicates(subset=['x', 'y', 'score'], keep='first')
    
    # Cleanup
    final_df = final_df.drop(columns=['x_round', 'y_round'])
    
    print(f"Final Unified Manifold Count: {len(final_df)} points.")
    
    # 4. Save the Final Truth
    output_filename = 'SPHERE_POINT_LABELS_COMPLETE_816.csv'
    final_df.to_csv(output_filename, index=False)
    
    # Also update the JSON registry for the renderers
    registry = final_df.to_dict(orient='records')
    with open('AUTO_ANCHORS_COMPLETE_816.json', 'w') as f:
        json.dump(registry, f, indent=2)
        
    print(f"Success: {output_filename} and AUTO_ANCHORS_COMPLETE_816.json generated.")

if __name__ == "__main__":
    merge_unmapped_points()
