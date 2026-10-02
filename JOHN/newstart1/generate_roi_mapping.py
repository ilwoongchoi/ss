import pandas as pd
import numpy as np

def map_to_geography(x, y):
    # Mapping logic based on x (Left/Right) and y (Height/Role)
    # Human Left (0~8), Human Right (8~16)
    if x >= 8: # Right Side
        if y >= 14: return "Himalaya / Karakoram (High Tension)"
        if y >= 12: return "Pamir / Hindu Kush (Ignition)"
        if y >= 10: return "Ural Mountains (Anchor)"
        if y >= 8: return "Siberian Craton (Ground)"
        if y >= 6: return "Deccan Traps (Confinement)"
        if y >= 4: return "Sahara / African Shield (Tension)"
        if y >= 2: return "Great Dividing Range (Stability)"
        return "Antarctic Ridge (Deep Sink)"
    else: # Left Side
        if y >= 14: return "Japan / Kuril Trench (Understanding)"
        if y >= 12: return "Fennoscandian Shield (Ancient)"
        if y >= 10: return "Alps / Rhine Valley (Process)"
        if y >= 8: return "Appalachian / Laurentia (Ghost)"
        if y >= 6: return "Amazon Basin (Volume)"
        if y >= 4: return "Andes Mountains (Leach)"
        if y >= 2: return "Nile Rift (Divergent)"
        return "Southern Ocean (Void)"

def get_vector(x, y):
    if x >= 8:
        if y >= 14: return "P+ (Proton)"
        if y >= 12: return "P+ + q"
        if y >= 10: return "H (Higgs)"
        if y >= 8: return "Z (Z-Boson)"
        if y >= 6: return "g (Gluon)"
        if y >= 4: return "q (Quark)"
        if y >= 2: return "W (W-Boson)"
        return "Z+H (Absolute Sink)"
    else:
        if y >= 14: return "ν (Neutrino)"
        if y >= 12: return "γ (Photon)"
        if y >= 10: return "W (Weak)"
        if y >= 8: return "ν + γ"
        if y >= 6: return "g + Z"
        if y >= 4: return "H + ν"
        if y >= 2: return "P+ + W"
        return "γ (Void)"

# Read the sorted ROI data
df = pd.read_csv('ROI_452_SPIRAL_SORTED.csv')

mapping_rows = []
for idx, row in df.iterrows():
    geog = map_to_geography(row['x'], row['y'])
    vector = get_vector(row['x'], row['y'])
    mapping_rows.append(f"| {int(row['idx'])} | ({row['x']:.2f}, {row['y']:.2f}) | **{geog}** | {vector} | ROI Mapping |")

with open('full_452_roi_mapping.md', 'w', encoding='utf-8') as f:
    f.write("# Full 452 Body ROI Mapping (Geographic/Vector)\n\n")
    f.write("| ROI Index | Coordinates (x, y) | Geographic / Geological Site | Particle Vector | Role |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- |\n")
    f.write("\n".join(mapping_rows))

print("Full 452 ROI mapping generated in full_452_roi_mapping.md")
