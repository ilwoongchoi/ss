import csv
import math
import numpy as np

base = r"d:\Users\user\Documents\newstart"

# Load face ROIs
face_rois = []
with open(f"{base}\\UNMAPPED_FACE_PEAKS.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        face_rois.append({
            'x': float(row['x']),
            'y': float(row['y']),
            'score': float(row['score'])
        })

print(f"Loaded {len(face_rois)} face ROIs")

# Log spiral parameters (same as face ROIs)
a = 3.58
b = 0.0216
cx, cy = 8.0, 10.0  # spiral center at face center

# Body region definitions with anatomical proportions
# Following nerve pathway lengths (spinal cord ~45cm, vagus nerve ~15cm, etc.)
body_regions = {
    # Uroboros Circuit - Bottom Anchor
    'rectum_center': {'y': 150.0, 'x_offset': 0.0, 'region': 'uroboros_bottom'},
    'rectum_left': {'y': 150.0, 'x_offset': -2.0, 'region': 'uroboros_bottom'},
    'rectum_right': {'y': 150.0, 'x_offset': 2.0, 'region': 'uroboros_bottom'},
    
    # Zero-Point Crossing (Perineum/Testicle)
    'perineum_zero': {'y': 145.0, 'x_offset': 0.0, 'region': 'uroboros_crossing'},
    'testicle_crossing': {'y': 143.0, 'x_offset': 0.0, 'region': 'uroboros_crossing'},
    
    # Lower Back - Uroboros Ascent
    'back_lower_center': {'y': 130.0, 'x_offset': 0.0, 'region': 'uroboros_ascent'},
    'back_lower_left': {'y': 130.0, 'x_offset': -4.0, 'region': 'uroboros_ascent'},
    'back_lower_right': {'y': 130.0, 'x_offset': 4.0, 'region': 'uroboros_ascent'},
    
    # Waist - Lateral Branches
    'waist_left': {'y': 125.0, 'x_offset': -6.0, 'region': 'lateral_branch'},
    'waist_right': {'y': 125.0, 'x_offset': 6.0, 'region': 'lateral_branch'},
    
    # Side Flanks
    'side_flank_left': {'y': 120.0, 'x_offset': -7.0, 'region': 'lateral_branch'},
    'side_flank_right': {'y': 120.0, 'x_offset': 7.0, 'region': 'lateral_branch'},
    
    # Mid Back
    'back_mid_center': {'y': 115.0, 'x_offset': 0.0, 'region': 'uroboros_ascent'},
    'back_mid_left': {'y': 115.0, 'x_offset': -4.0, 'region': 'uroboros_ascent'},
    'back_mid_right': {'y': 115.0, 'x_offset': 4.0, 'region': 'uroboros_ascent'},
    
    # Upper Back - Cervical Connection
    'back_upper_center': {'y': 100.0, 'x_offset': 0.0, 'region': 'uroboros_ascent'},
    'back_upper_left': {'y': 100.0, 'x_offset': -4.0, 'region': 'uroboros_ascent'},
    'back_upper_right': {'y': 100.0, 'x_offset': 4.0, 'region': 'uroboros_ascent'},
    
    # Appendix (Right side - McBurney's point analog)
    'appendix_region': {'y': 135.0, 'x_offset': 5.0, 'region': 'visceral_branch'},
    
    # Navel Center
    'navel_center': {'y': 128.0, 'x_offset': 0.0, 'region': 'front_midline'},
    
    # Lower Limbs - Inner/Outer Bifurcation
    'thigh_inner_left': {'y': 155.0, 'x_offset': -3.0, 'region': 'lower_limb'},
    'thigh_inner_right': {'y': 155.0, 'x_offset': 3.0, 'region': 'lower_limb'},
    'thigh_outer_left': {'y': 155.0, 'x_offset': -6.0, 'region': 'lower_limb'},
    'thigh_outer_right': {'y': 155.0, 'x_offset': 6.0, 'region': 'lower_limb'},
    
    # Soles - Grounding Points
    'sole_left': {'y': 170.0, 'x_offset': -5.0, 'region': 'peripheral_ground'},
    'sole_right': {'y': 170.0, 'x_offset': 5.0, 'region': 'peripheral_ground'},
}

# Generate body ROI points using spiral physics
def generate_body_roi(name, params):
    """Generate body ROI using log spiral equation extended from face center"""
    y_base = params['y']
    x_offset = params['x_offset']
    
    # Calculate spiral angle based on y-distance from face center
    dy = y_base - cy
    dx = x_offset
    
    # Convert to polar coordinates relative to spiral center
    r = math.sqrt(dx**2 + dy**2)
    theta = math.atan2(dy, dx)
    
    # Apply log spiral equation: r = a * e^(b*θ)
    # For body points, we extend the spiral downward
    spiral_r = a * math.exp(b * theta)
    
    # Calculate score based on distance from ideal spiral
    ideal_r = a * math.exp(b * theta)
    deviation = abs(r - ideal_r)
    score = max(0.02, 0.03 - deviation * 0.001)  # Decaying score for body
    
    return {
        'roi_id': f"B{list(body_regions.keys()).index(name)+1:03d}",
        'body_name': name,
        'x': cx + x_offset,
        'y': y_base,
        'score': score,
        'spiral_r': r,
        'spiral_theta': theta,
        'region': params['region'],
        'face_connection': 'spine_continuity'  # All body connects via spine
    }

# Generate all body ROIs
body_rois = []
for name, params in body_regions.items():
    roi = generate_body_roi(name, params)
    body_rois.append(roi)

print(f"Generated {len(body_rois)} body ROIs")

# Save to CSV
with open(f"{base}\\BODY_ROI_SPIRAL.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=['roi_id', 'body_name', 'x', 'y', 'score', 
                                            'spiral_r', 'spiral_theta', 'region', 'face_connection'])
    writer.writeheader()
    writer.writerows(body_rois)

print(f"Saved: BODY_ROI_SPIRAL.csv")

# Create mapping to face ROIs via Uroboros circuit (spine connection)
# The spine is the vertical continuation from face center (8, 10) down through body
mappings = []
for body_roi in body_rois:
    # Find nearest face ROI by x-coordinate (same vertical line through spine)
    body_x = body_roi['x']
    
    # Map body x to face x (spine is vertical line through center, body spreads laterally)
    if body_roi['region'] in ['uroboros_ascent', 'uroboros_bottom', 'uroboros_crossing', 'front_midline']:
        # Center line points map to face center region
        face_x_target = 8.0
    elif 'left' in body_roi['body_name'] or body_roi['x'] < 8.0:
        # Left side body maps to left face
        face_x_target = body_x / 2  # Scale down to face coordinates (0-8)
    else:
        # Right side body maps to right face  
        face_x_target = 8.0 + (body_x - 8.0) / 2  # Scale down to face coordinates (8-16)
    
    # Find closest face ROI
    closest_face = min(face_rois, key=lambda f: abs(f['x'] - face_x_target) + abs(f['y'] - 10.0) * 0.1)
    
    mappings.append({
        'body_roi_id': body_roi['roi_id'],
        'body_name': body_roi['body_name'],
        'body_x': body_roi['x'],
        'body_y': body_roi['y'],
        'face_x': closest_face['x'],
        'face_y': closest_face['y'],
        'connection_type': 'spine_nerve_path',
        'region': body_roi['region']
    })

# Save mapping
with open(f"{base}\\FACE_BODY_UROBOROS_MAP.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=['body_roi_id', 'body_name', 'body_x', 'body_y',
                                            'face_x', 'face_y', 'connection_type', 'region'])
    writer.writeheader()
    writer.writerows(mappings)

print(f"Saved: FACE_BODY_UROBOROS_MAP.csv")
print(f"Total mappings: {len(mappings)}")

# Print summary
print("\n=== Body ROI Summary ===")
regions = {}
for roi in body_rois:
    r = roi['region']
    regions[r] = regions.get(r, 0) + 1

for region, count in sorted(regions.items()):
    print(f"  {region}: {count} points")

print("\n=== Uroboros Circuit Points ===")
uroboros_points = [r for r in body_rois if 'uroboros' in r['region']]
for p in uroboros_points:
    print(f"  {p['roi_id']}: {p['body_name']} ({p['x']:.1f}, {p['y']:.1f}) -> {p['region']}")
