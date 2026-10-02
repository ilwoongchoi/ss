import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as mpatches

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

# Load body ROIs
body_rois = []
with open(f"{base}\\BODY_ROI_SPIRAL.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        body_rois.append({
            'roi_id': row['roi_id'],
            'body_name': row['body_name'],
            'x': float(row['x']),
            'y': float(row['y']),
            'score': float(row['score']),
            'region': row['region']
        })

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(14, 20))

# Plot face ROIs (upper portion)
face_x = [r['x'] for r in face_rois]
face_y = [r['y'] for r in face_rois]
face_scores = [r['score'] for r in face_rois]

scatter_face = ax.scatter(face_x, face_y, c=face_scores, cmap='viridis', 
                          s=20, alpha=0.7, label='Face ROIs (451)')

# Plot body ROIs (lower portion)
body_x = [r['x'] for r in body_rois]
body_y = [r['y'] for r in body_rois]
body_scores = [r['score'] for r in body_rois]

# Color by region
region_colors = {
    'uroboros_bottom': '#FF0000',      # Red - bottom anchor
    'uroboros_crossing': '#FF4500',    # Orange-red - zero point
    'uroboros_ascent': '#00FF00',      # Green - spine ascent
    'lateral_branch': '#0000FF',       # Blue - side branches
    'visceral_branch': '#FF00FF',      # Magenta - visceral
    'front_midline': '#00FFFF',        # Cyan - front
    'lower_limb': '#FFFF00',           # Yellow - limbs
    'peripheral_ground': '#800080',    # Purple - grounding
}

for roi in body_rois:
    color = region_colors.get(roi['region'], '#888888')
    ax.scatter(roi['x'], roi['y'], c=color, s=80, alpha=0.9, edgecolors='black', linewidths=1)
    # Add label for key points
    if 'center' in roi['body_name'] or 'crossing' in roi['body_name'] or 'zero' in roi['body_name']:
        ax.annotate(roi['body_name'], (roi['x'], roi['y']), 
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=7, alpha=0.8)

# Draw spine connection (vertical line through center)
ax.plot([8, 8], [15, 150], 'k--', linewidth=2, alpha=0.5, label='Spine/Uroboros')

# Draw lateral nerve connections
for roi in body_rois:
    if 'left' in roi['body_name'] and roi['region'] in ['lateral_branch', 'lower_limb', 'uroboros_ascent']:
        # Draw line from spine center to left point
        ax.plot([8, roi['x']], [roi['y'], roi['y']], 'b-', linewidth=0.5, alpha=0.3)
    elif 'right' in roi['body_name'] and roi['region'] in ['lateral_branch', 'lower_limb', 'uroboros_ascent']:
        # Draw line from spine center to right point
        ax.plot([8, roi['x']], [roi['y'], roi['y']], 'b-', linewidth=0.5, alpha=0.3)

# Draw log spiral fit curve (extended to body)
theta_fit = np.linspace(-np.pi, np.pi * 2, 500)
a, b = 3.58, 0.0216
cx, cy = 8.0, 10.0
r_fit = a * np.exp(b * theta_fit)
x_fit = cx + r_fit * np.cos(theta_fit)
y_fit = cy + r_fit * np.sin(theta_fit)

# Filter to show only relevant spiral arms
mask = (y_fit > 5) & (y_fit < 170)
ax.plot(x_fit[mask], y_fit[mask], 'k:', linewidth=1, alpha=0.4, label='Log Spiral')

# Mark spiral center
ax.plot(cx, cy, 'r*', markersize=20, label='Spiral Center')

# Mark zero-point crossing
zero_point = [r for r in body_rois if 'zero' in r['body_name'] or 'crossing' in r['body_name']]
if zero_point:
    zp = zero_point[0]
    ax.plot(zp['x'], zp['y'], 'w*', markersize=15, markeredgecolor='red', 
            markeredgewidth=2, label='Zero-Point Crossing')

# Formatting
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_title('Face-Body ROI Spiral Connection\n(Uroboros Circuit via Spine)', fontsize=14)
ax.set_aspect('equal')
ax.invert_yaxis()  # Face orientation at top

# Legend for body regions
legend_elements = [mpatches.Patch(color=color, label=region.replace('_', ' ').title())
                   for region, color in region_colors.items()]
legend_elements.append(mpatches.Patch(color='none', label='Face: 451 ROIs'))
legend_elements.append(mpatches.Patch(color='none', label=f'Body: {len(body_rois)} ROIs'))
ax.legend(handles=legend_elements, loc='upper left', fontsize=8)

# Add grid
ax.grid(True, alpha=0.3)

# Set limits
ax.set_xlim(-2, 18)
ax.set_ylim(175, 0)

plt.tight_layout()
plt.savefig(f"{base}\\FACE_BODY_SPIRAL_CONNECTION.png", dpi=150, bbox_inches='tight')
plt.close()

print(f"Saved: FACE_BODY_SPIRAL_CONNECTION.png")
print(f"Face ROIs: {len(face_rois)}")
print(f"Body ROIs: {len(body_rois)}")
print(f"Total mapped points: {len(face_rois) + len(body_rois)}")
