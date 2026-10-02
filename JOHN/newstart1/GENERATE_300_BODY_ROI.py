import csv
import math

base = r"d:\Users\user\Documents\newstart"

# 1. Load Face ROIs for mapping
face_rois = []
try:
    with open(f"{base}\\UNMAPPED_FACE_PEAKS.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            face_rois.append({'x': float(row['x']), 'y': float(row['y'])})
except:
    face_rois = [{'x': 8.0, 'y': 10.0}]

# 2. Spiral Parameters
a, b = 3.58, 0.0216
cx, cy = 8.0, 10.0

# 3. Generate 300+ Body ROIs
body_data = []

def add_pts(name_base, y_start, y_end, x_offsets, region, system):
    steps = 5
    for i in range(steps):
        curr_y = y_start + (y_end - y_start) * (i / steps)
        for x_off in x_offsets:
            name = f"{name_base}_{i}_{x_off}"
            # Log spiral logic
            r = math.sqrt(x_off**2 + (curr_y-cy)**2)
            theta = math.atan2(curr_y-cy, x_off)
            score = max(0.01, 0.03 - abs(r - a*math.exp(b*theta))*0.001)
            
            body_data.append({
                'roi_id': f"B{len(body_data)+1:03d}",
                'name': name,
                'x': cx + x_off,
                'y': curr_y,
                'score': score,
                'region': region,
                'system': system
            })

# Brain/Cervical
add_pts("brain_cervical", 15, 30, [-4, -2, 0, 2, 4], "neuro_central", "nervous")
# Thoracic/Heart/Lungs
add_pts("thoracic_visceral", 35, 60, [-8, -6, -4, -2, 0, 2, 4, 6, 8], "thoracic", "mixed")
# Lumbar/GI/Renal
add_pts("lumbar_abdominal", 65, 90, [-7, -5, -3, -1, 0, 1, 3, 5, 7], "abdominal", "mixed")
# Pelvis/Gonadal/Uroboros
add_pts("pelvic_uroboros", 95, 120, [-5, -3, -1, 0, 1, 3, 5], "pelvic", "reproductive")
# Lower Limbs/Grounding
add_pts("limbs_ground", 125, 170, [-10, -8, -6, 6, 8, 10], "limbs", "skeletal")

# 4. Save to CSV
with open(f"{base}\\BODY_ROI_300_EXTENDED.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=['roi_id', 'name', 'x', 'y', 'score', 'region', 'system'])
    writer.writeheader()
    writer.writerows(body_data)

# 5. Save Mapping
mappings = []
for b_roi in body_data:
    # Logic: Map body lateral spread to face lateral spread
    f_x = cx + (b_roi['x'] - cx) * 0.5
    f_y = cy + (b_roi['y'] - cy) * 0.05 # Compress body Y to face Y range
    mappings.append({
        'body_id': b_roi['roi_id'],
        'body_name': b_roi['name'],
        'face_x_target': round(f_x, 2),
        'face_y_target': round(f_y, 2),
        'connection': 'nerve_current'
    })

with open(f"{base}\\FACE_BODY_300_MAP.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=['body_id', 'body_name', 'face_x_target', 'face_y_target', 'connection'])
    writer.writeheader()
    writer.writerows(mappings)

print(f"Generated {len(body_data)} ROIs.")
