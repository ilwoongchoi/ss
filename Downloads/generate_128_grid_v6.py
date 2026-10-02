"""
128-Type Neurochemical Trajectory Grid — V6

Remake focused on:
- 16 columns (8 archetypes × 2 cells)
- EJ/EP women separated
- INTP O♀ full traverse diagonal
- many lines converging through the same hub cell (not radial burst)
- hand-traced lines reused where available + generated completion for all 128
"""

import os
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False

# ═══════════════════════════════════════════════════════════════
# GRID
# ═══════════════════════════════════════════════════════════════

N_COLS = 16
N_ROWS = 18

ROW_LABELS = {
    1: "해뜨기전",
    2: "해뜨기 직전",
    3: "해뜬수",
    4: "아침",
    5: "오후",
    6: "피로시작",
    7: "멜라토닌 분비\n(해지기직전)",
    8: "남자 두번째\n멜라토닌 분비",
    9: "해진후",
    10: "저녁",
    11: "밤",
    12: "남자 렘수면",
    13: "코르티졸 다운",
    14: "여자 멜라토닌 다운",
    15: "남 꿈",
    16: "페이크 렘",
    17: "여자들 꿈, 남자 애",
}

# Left→Right: IP-W | IJ-W | EP-W | EJ-W | IP-M | IJ-M | EP-M | EJ-M
COL_GROUPS = [
    ("IP\nWOMEN", 0, 2),
    ("IJ\nWOMEN", 2, 4),
    ("EP\nWOMEN", 4, 6),
    ("EJ\nWOMEN", 6, 8),
    ("IP\nMEN", 8, 10),
    ("IJ\nMEN", 10, 12),
    ("EP\nMEN", 12, 14),
    ("EJ\nMEN", 14, 16),
]

ARCH_COL = {
    ("IP", "F"): 1.0,
    ("IJ", "F"): 3.0,
    ("EP", "F"): 5.0,
    ("EJ", "F"): 7.0,
    ("IP", "M"): 9.0,
    ("IJ", "M"): 11.0,
    ("EP", "M"): 13.0,
    ("EJ", "M"): 15.0,
}

GROUP_HUB = {
    ("IP", "F"): (1.0, 10.6),
    ("IJ", "F"): (3.0, 7.0),
    ("EP", "F"): (5.0, 4.0),
    ("EJ", "F"): (7.0, 2.0),
    ("IP", "M"): (9.0, 10.6),
    ("IJ", "M"): (11.0, 7.0),
    ("EP", "M"): (13.0, 4.0),
    ("EJ", "M"): (15.0, 2.0),
}

GROUP_START_ROW = {
    "EJ": 1.2,
    "EP": 3.0,
    "IJ": 6.0,
    "IP": 9.0,
}

BLOOD_COLORS = {
    "O": "#DD3333",
    "A": "#33AA33",
    "B": "#4499DD",
    "AB": "#9944CC",
}

BLOOD_2x2 = {
    "O": (-0.4, -0.4),
    "A": (0.4, -0.4),
    "B": (-0.4, 0.4),
    "AB": (0.4, 0.4),
}

ALL_MBTI = [
    "ESTJ", "ENTJ", "ESFJ", "ENFJ",
    "ESTP", "ENTP", "ESFP", "ENFP",
    "ISTJ", "INTJ", "ISFJ", "INFJ",
    "ISTP", "INTP", "ISFP", "INFP",
]
BLOODS = ["O", "A", "B", "AB"]
GENDERS = ["M", "F"]


def get_group(mbti: str) -> str:
    return mbti[0] + mbti[3]


def clamp_point(x, y):
    x = max(0.2, min(N_COLS - 0.2, x))
    y = max(0.5, min(17.0, y))
    return (x, y)


def stable_jitter(mbti, blood, gender):
    s = sum(ord(c) for c in (mbti + blood + gender))
    jx = ((s % 7) - 3) * 0.05
    jy = (((s // 7) % 7) - 3) * 0.04
    return jx, jy


def parse_label_key(label):
    # "MBTI B ♂" / "MBTI A ♀"
    parts = label.split()
    mbti = parts[0]
    blood = parts[1]
    gender = "M" if "♂" in label else "F"
    return mbti, blood, gender


def remap_x_14_to_16(mbti, gender, x):
    # V4 was 14 cols with BIG WOMEN merged and men shifted left by 2
    # V6 is 16 cols with EP-W and EJ-W separated.
    shift = 0.0
    if gender == "M":
        shift += 2.0
    if gender == "F" and get_group(mbti) == "EJ":
        shift += 2.0
    return x + shift


# ═══════════════════════════════════════════════════════════════
# HAND-TRACED BASE (from V4), then remapped to 16-column grid
# ═══════════════════════════════════════════════════════════════

HAND_TRACED_BASE = [
    ("ISFP O ♀", "#DD3333", 1.3, [(0.4, 1.0), (0.4, 3.0), (0.4, 5.0), (0.4, 7.0), (0.4, 9.0), (0.4, 11.0), (0.4, 12.0)]),
    ("INFP O ♀", "#DD3333", 1.1, [(0.9, 1.2), (0.8, 3.5), (0.9, 5.5), (1.0, 7.5), (0.9, 9.5), (0.8, 11.5)]),
    ("ISTP A ♀", "#33AA33", 1.3, [(1.4, 1.5), (1.5, 3.5), (1.4, 5.5), (1.5, 7.5), (1.6, 9.5), (1.5, 11.0)]),
    ("INTP A ♀", "#33AA33", 1.1, [(1.8, 1.8), (1.7, 4.0), (1.8, 6.0), (1.7, 8.0), (1.8, 10.0), (1.7, 11.5)]),

    ("ISTJ O ♀", "#DD3333", 1.3, [(2.4, 1.5), (2.5, 3.5), (2.7, 5.5), (2.8, 7.0), (3.0, 8.5), (2.8, 10.0), (2.6, 11.5)]),
    ("INTJ A ♀", "#33AA33", 1.3, [(3.0, 1.5), (3.2, 3.5), (3.4, 5.5), (3.5, 7.5), (3.3, 9.5), (3.0, 11.0)]),
    ("ISFJ A ♀", "#33AA33", 2.0, [(2.8, 2.5), (3.0, 3.5), (3.3, 5.0), (3.5, 6.0), (3.8, 7.0), (4.0, 8.0), (3.8, 9.0), (3.5, 10.0), (3.0, 11.0), (2.8, 12.0)]),
    ("INFJ AB ♀", "#9944CC", 1.3, [(3.5, 2.0), (3.7, 4.5), (3.8, 6.5), (4.0, 8.0), (3.8, 9.5), (3.5, 11.0)]),

    ("ESFJ A ♀", "#33AA33", 2.2, [(3.8, 3.0), (4.2, 4.5), (4.5, 6.0), (4.8, 7.0), (5.0, 7.5), (4.8, 8.5), (4.5, 9.5), (4.0, 10.5)]),
    ("ENFJ B ♀", "#4499DD", 1.3, [(4.5, 2.0), (5.0, 3.5), (5.3, 5.0), (5.0, 6.5), (4.8, 8.0), (5.0, 9.5), (5.3, 11.0)]),
    ("ESTJ O ♀", "#DD3333", 1.0, [(5.5, 2.5), (5.2, 4.0), (5.5, 5.5), (5.8, 7.0), (5.5, 8.5), (5.2, 10.0)]),

    ("ISTP O ♂", "#DD3333", 1.5, [(6.2, 1.5), (6.8, 1.5), (7.4, 1.5), (8.0, 1.5)]),
    ("INTP O ♂", "#DD3333", 1.5, [(6.2, 2.3), (6.8, 2.3), (7.4, 2.3), (8.0, 2.5)]),
    ("ISTP A ♂", "#33AA33", 1.3, [(6.2, 3.0), (6.8, 3.0), (7.4, 3.2), (8.0, 3.5)]),
    ("INTP A ♂", "#33AA33", 1.2, [(6.5, 4.0), (7.0, 4.0), (7.5, 4.2), (8.0, 4.5)]),
    ("ISFP B ♂", "#4499DD", 1.0, [(6.5, 4.8), (7.0, 4.8), (7.5, 5.0), (8.0, 5.3)]),

    ("ESFP O ♂", "#DD3333", 2.0, [(5.5, 5.0), (6.0, 5.5), (6.5, 6.0), (7.0, 6.5), (7.2, 7.0), (7.0, 7.5), (6.5, 8.0)]),
    ("ENTJ O ♂", "#DD3333", 2.0, [(7.5, 4.5), (8.0, 5.0), (8.3, 5.5), (8.5, 6.0), (8.3, 6.5), (8.0, 7.0), (7.5, 7.5)]),
    ("INTJ O ♂", "#DD3333", 2.0, [(7.0, 7.0), (7.3, 7.5), (7.5, 8.0), (7.3, 8.5), (7.5, 9.0), (8.0, 9.5)]),
    ("ESFP A ♂", "#33AA33", 2.0, [(6.0, 7.5), (6.5, 8.0), (7.0, 8.3), (7.5, 8.5), (7.0, 9.0), (6.5, 9.5)]),

    ("ESTP O ♂", "#DD3333", 1.8, [(6.5, 8.5), (7.2, 9.0), (7.8, 9.5), (7.2, 10.0), (7.8, 10.5), (7.2, 11.0)]),
    ("ENTP O ♂", "#DD3333", 1.5, [(7.0, 9.0), (7.5, 9.5), (8.0, 9.0), (8.5, 9.5), (8.0, 10.0), (7.5, 10.5)]),

    ("ENFP B ♀", "#4499DD", 2.8, [(0.5, 1.0), (1.5, 2.5), (3.0, 4.0), (4.5, 5.5), (6.0, 7.0), (7.5, 8.5), (9.0, 10.0), (10.5, 11.5), (12.0, 13.0), (13.5, 15.0)]),

    ("ESTP B ♂", "#4499DD", 1.8, [(9.0, 8.5), (9.5, 9.0), (10.0, 9.3), (10.5, 9.0), (11.0, 9.5), (11.5, 10.0)]),
    ("ENTP A ♂", "#33AA33", 1.5, [(9.5, 9.5), (10.0, 10.0), (10.5, 10.3), (11.0, 10.0), (11.5, 10.5), (12.0, 10.8)]),
    ("ESFP B ♂", "#4499DD", 1.2, [(10.0, 7.5), (10.5, 8.0), (11.0, 8.5), (11.5, 9.0)]),
    ("ENTJ A ♂", "#33AA33", 2.0, [(10.0, 8.0), (10.5, 8.5), (11.0, 9.5), (11.5, 10.0), (11.0, 10.5), (10.5, 11.0)]),

    ("ISTJ O ♂", "#DD3333", 1.2, [(8.5, 3.0), (9.0, 3.5), (9.5, 4.0), (10.0, 4.5), (10.5, 5.0)]),
    ("INTJ A ♂", "#33AA33", 1.0, [(8.5, 5.0), (9.0, 5.5), (9.5, 6.0), (10.0, 6.5)]),
    ("ESTP A ♂", "#33AA33", 1.3, [(10.5, 2.5), (11.0, 3.0), (11.5, 3.5), (12.0, 4.0)]),
    ("ENTP B ♂", "#4499DD", 1.0, [(10.5, 4.5), (11.0, 5.5), (11.5, 6.5), (12.0, 7.5)]),

    ("ESTJ O ♂", "#DD3333", 1.8, [(12.5, 2.0), (13.0, 1.5), (13.5, 1.0), (14.0, 0.5)]),
    ("ENTJ O ♂", "#DD3333", 1.8, [(12.5, 2.0), (13.0, 2.0), (13.5, 2.0), (14.0, 2.0)]),
    ("ESFJ O ♂", "#DD3333", 1.5, [(13.0, 2.0), (12.5, 1.5), (12.0, 1.0)]),
    ("ENFJ A ♂", "#33AA33", 1.8, [(12.5, 2.0), (13.0, 2.5), (13.5, 3.0), (13.8, 3.5)]),
    ("ESTJ A ♂", "#33AA33", 1.5, [(13.0, 2.0), (13.0, 3.0), (12.8, 4.0), (13.0, 5.0), (13.2, 6.0), (13.0, 7.0), (12.8, 8.0), (13.0, 9.0), (13.2, 10.0), (13.0, 11.0), (12.8, 12.0)]),
    ("ENTJ B ♂", "#4499DD", 1.3, [(13.0, 2.5), (12.5, 3.0), (12.0, 3.5), (11.5, 4.0)]),
    ("ENFJ AB ♂", "#9944CC", 1.3, [(13.5, 2.0), (13.5, 3.5), (13.8, 5.0), (13.5, 6.5), (13.8, 8.0), (13.5, 9.5), (13.8, 11.0)]),

    ("ESTJ AB ♂", "#111111", 2.2, [(13.8, 2.0), (14.0, 4.0), (13.9, 6.0), (14.0, 8.0), (13.8, 10.0), (13.5, 12.0), (13.0, 14.0), (12.5, 16.0)]),
    ("INFJ B ♀", "#4499DD", 1.8, [(3.0, 3.0), (3.5, 4.5), (4.0, 6.0), (5.0, 7.5), (6.0, 8.5), (7.0, 9.5), (8.0, 10.0), (9.0, 10.5), (10.0, 11.0)]),
    ("ENFP A ♀", "#33AA33", 1.3, [(5.0, 9.0), (5.5, 9.5), (6.0, 10.0), (6.5, 10.5), (7.0, 11.0), (7.5, 11.5)]),
    ("INFP B ♀", "#4499DD", 1.0, [(1.0, 12.0), (1.5, 13.0), (2.0, 14.0), (2.5, 15.0), (3.0, 16.0), (3.5, 17.0)]),
    ("ENFJ AB ♀", "#9944CC", 1.0, [(12.5, 12.0), (12.8, 13.0), (13.0, 14.0), (12.8, 15.0), (12.5, 16.0)]),
]


def build_hand_traced_map():
    out = {}
    for label, _color, lw, points in HAND_TRACED_BASE:
        mbti, blood, gender = parse_label_key(label)
        remapped = []
        for x, y in points:
            nx = remap_x_14_to_16(mbti, gender, x)
            remapped.append(clamp_point(nx, y))
        out[(mbti, blood, gender)] = {
            "points": remapped,
            "lw": lw,
            "is_custom": True,
        }

    # Explicit correction: INTP O♀ is the full traverse
    full_diag = [
        (0.5, 16.2),
        (1.7, 15.5),
        (3.0, 14.0),
        (4.2, 12.5),
        (5.7, 10.8),
        (7.0, 9.0),
        (8.2, 7.2),
        (9.7, 6.0),
        (11.2, 5.0),
        (12.8, 4.0),
        (14.1, 3.0),
        (15.5, 1.8),
    ]
    out[("INTP", "O", "F")] = {
        "points": [clamp_point(x, y) for (x, y) in full_diag],
        "lw": 3.2,
        "is_custom": True,
    }

    # ENFP B♀ is NOT the full-traverse line.
    # Keep it as a strong EP-women diagonal that enters center but does not cross the whole grid.
    enfp_b_local = [
        (4.4, 2.8),
        (4.9, 4.0),
        (5.4, 5.4),
        (6.0, 6.8),
        (6.6, 8.2),
        (6.2, 9.5),
        (5.4, 10.7),
    ]
    out[("ENFP", "B", "F")] = {
        "points": [clamp_point(x, y) for (x, y) in enfp_b_local],
        "lw": 2.4,
        "is_custom": True,
    }

    return out


# ═══════════════════════════════════════════════════════════════
# GENERATED FILLER (for remaining keys), converging through hubs
# ═══════════════════════════════════════════════════════════════

GROUP_TEMPLATE = {
    "EJ": [(0.0, 0.0), (0.0, 2.0), (0.2, 4.0), (-0.1, 6.0), (0.1, 8.2)],
    "EP": [(0.0, 0.0), (0.5, 1.4), (-0.4, 3.1), (0.8, 4.9), (-0.3, 6.8)],
    "IJ": [(0.0, 0.0), (0.2, -1.5), (-0.2, -3.0), (0.3, -4.6), (-0.1, -6.0)],
    "IP": [(0.0, 0.0), (-0.2, -1.4), (0.4, -2.8), (-0.4, -4.4), (0.3, -6.1)],
}

BLOOD_X_SHIFT = {"O": 0.30, "A": 0.10, "B": -0.10, "AB": -0.30}
BLOOD_Y_SHIFT = {"O": -0.8, "A": -0.2, "B": 0.8, "AB": 1.6}


def cleanup_points(pts):
    clean = []
    for p in pts:
        cp = clamp_point(p[0], p[1])
        if not clean:
            clean.append(cp)
            continue
        px, py = clean[-1]
        if abs(px - cp[0]) > 0.03 or abs(py - cp[1]) > 0.03:
            clean.append(cp)
    return clean


def infer_shared_hub(hand_map):
    """Infer the dense pass-through cell from hand-traced geometry."""
    counts = Counter()
    cx0 = N_COLS / 2.0
    cy0 = N_ROWS / 2.0

    for meta in hand_map.values():
        pts = meta["points"]
        if len(pts) == 1:
            x, y = pts[0]
            cell = (int(round(x)), int(round(y)))
            if 1 <= cell[0] <= (N_COLS - 2) and 1 <= cell[1] <= (N_ROWS - 2):
                counts[cell] += 1
            continue

        for i in range(len(pts) - 1):
            x0, y0 = pts[i]
            x1, y1 = pts[i + 1]
            steps = max(1, int(max(abs(x1 - x0), abs(y1 - y0)) * 4.0))
            for s in range(steps + 1):
                t = s / steps
                x = x0 + (x1 - x0) * t
                y = y0 + (y1 - y0) * t
                cell = (int(round(x)), int(round(y)))
                if 1 <= cell[0] <= (N_COLS - 2) and 1 <= cell[1] <= (N_ROWS - 2):
                    counts[cell] += 1

    if not counts:
        return (8.0, 8.0)

    def score(item):
        (x, y), cnt = item
        dist = abs(x - cx0) + abs(y - cy0)
        return cnt - 0.05 * dist

    best_cell, _ = max(counts.items(), key=score)
    return (float(best_cell[0]), float(best_cell[1]))


def generate_filler_path(mbti, blood, gender):
    grp = get_group(mbti)
    ns = mbti[1]
    tf = mbti[2]

    gx = ARCH_COL[(grp, gender)]
    hx, hy = GROUP_HUB[(grp, gender)]
    bxo, byo = BLOOD_2x2[blood]

    tf_shift = 0.55 if tf == "T" else -0.55
    ns_shift = 0.25 if ns == "N" else -0.05
    g_shift = 0.18 if gender == "M" else -0.18
    bx_shift = BLOOD_X_SHIFT[blood]
    by_shift = BLOOD_Y_SHIFT[blood]
    jx, jy = stable_jitter(mbti, blood, gender)

    start = (
        gx + bxo * 0.8 + tf_shift * 0.15 + jx,
        GROUP_START_ROW[grp] + byo * 0.8 + jy,
    )

    # All generated lines pass through the exact group hub cell.
    pts = [start, (hx, hy)]

    # Add cross-grid bridge for NP/NT roaming signatures.
    if mbti in {"ENTP", "ENFP", "INTP", "INFP", "INTJ", "ENTJ"}:
        bridge_x = 8.0 + (0.4 if tf == "T" else -0.4)
        bridge_y = 8.2 + by_shift * 0.25
        pts.append((bridge_x, bridge_y))

    for dx, dy in GROUP_TEMPLATE[grp][1:]:
        x = hx + dx + tf_shift + ns_shift + g_shift + bx_shift + jx
        y = hy + dy + by_shift + (0.18 if ns == "N" else 0.0) + jy
        pts.append((x, y))

    # EJ-M AB/O often drop down the far-right side.
    if grp == "EJ" and gender == "M" and blood in {"A", "AB"}:
        tail_x = 15.6 if blood == "AB" else 15.2
        pts.extend([(tail_x, 12.5 + by_shift), (15.0, 15.3 if blood == "AB" else 13.8)])

    return cleanup_points(pts)


# ═══════════════════════════════════════════════════════════════
# BUILD 128
# ═══════════════════════════════════════════════════════════════

hand_map = build_hand_traced_map()
shared_hub = infer_shared_hub(hand_map)

trajectories = []
for mbti in ALL_MBTI:
    for blood in BLOODS:
        for gender in GENDERS:
            key = (mbti, blood, gender)
            if key in hand_map:
                pts = hand_map[key]["points"]
                lw = hand_map[key]["lw"]
                is_custom = hand_map[key]["is_custom"]
            else:
                pts = generate_filler_path(mbti, blood, gender)
                lw = 0.95
                is_custom = False

            trajectories.append(
                {
                    "mbti": mbti,
                    "blood": blood,
                    "gender": gender,
                    "points": pts,
                    "label": f"{mbti} {blood} {'♂' if gender == 'M' else '♀'}",
                    "lw": lw,
                    "custom": is_custom,
                }
            )

# Route eligible generated lines through the inferred shared pass-through cell.
for t in trajectories:
    if t["custom"]:
        continue

    pts = t["points"]
    if not pts:
        continue

    has_hub = any(abs(x - shared_hub[0]) < 0.22 and abs(y - shared_hub[1]) < 0.22 for x, y in pts)
    if has_hub:
        continue

    start_x = pts[0][0]
    end_x = pts[-1][0]
    crosses_halves = (
        (start_x < shared_hub[0] - 1.2 and end_x > shared_hub[0] + 1.2)
        or (start_x > shared_hub[0] + 1.2 and end_x < shared_hub[0] - 1.2)
    )
    roaming = t["mbti"] in {"ENTP", "ENFP", "INTP", "INFP", "INTJ", "ENTJ"}

    if not (crosses_halves or roaming):
        continue

    if len(pts) >= 2:
        t["points"] = [pts[0], shared_hub] + pts[1:]
    elif len(pts) == 1:
        t["points"] = [pts[0], shared_hub]
    else:
        t["points"] = [shared_hub]

print(f"Generated {len(trajectories)} trajectories.")

# ═══════════════════════════════════════════════════════════════
# DRAW
# ═══════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(40, 22))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Checkerboard
for r in range(N_ROWS):
    for c in range(N_COLS):
        fc = "#D8B4FE" if (r + c) % 2 == 0 else "#FFFFFF"
        ax.add_patch(
            mpatches.Rectangle((c, r), 1, 1, facecolor=fc, edgecolor="#C4A0E8", linewidth=0.35)
        )

# Grid lines
for c in range(N_COLS + 1):
    lw = 1.45 if c % 2 == 0 else 0.28
    ax.axvline(c, color="#9966CC", linewidth=lw, alpha=0.38)
for r in range(N_ROWS + 1):
    ax.axhline(r, color="#9966CC", linewidth=0.28, alpha=0.32)

# PLP/Energy diagonal
ax.plot([15.0, 1.0], [1.6, 15.0], color="#FFD700", linestyle="--", linewidth=2.4, alpha=0.45, zorder=3)

# Shared pass-through cell inferred from traced lines
ax.plot(shared_hub[0], shared_hub[1], "s", color="#222222", markersize=6, alpha=0.35, zorder=4)

# Headers
for label, xs, xe in COL_GROUPS:
    cx = (xs + xe) / 2
    ax.text(cx, -0.4, label, ha="center", va="center", fontsize=11, fontweight="bold", color="#222")

# Row labels
for r, txt in ROW_LABELS.items():
    ax.text(-0.15, r + 0.5, txt, ha="right", va="center", fontsize=6, color="#444")

# 2x2 blood start squares
for label, xs, xe in COL_GROUPS:
    grp = label.replace("\n", " ").split()[0]
    cx = (xs + xe) / 2
    if grp == "EJ":
        sy_base = 1.0
    elif grp == "EP":
        sy_base = 3.0
    elif grp == "IJ":
        sy_base = 6.0
    else:
        sy_base = 9.0

    for blood, (ox, oy) in BLOOD_2x2.items():
        sx = cx + ox * 0.9
        sy = sy_base + oy * 0.9
        ax.plot(sx, sy, "s", color=BLOOD_COLORS[blood], markersize=7, alpha=0.62, zorder=8, markeredgecolor="white", markeredgewidth=0.5)

# Draw lines
cardinals = {
    ("INTP", "O", "M"), ("ENTJ", "A", "M"), ("INTJ", "B", "M"), ("ENTP", "AB", "M"),
    ("INTP", "O", "F"), ("ISFJ", "A", "F"), ("ENFP", "B", "F"), ("INFJ", "AB", "F"),
}

for t in trajectories:
    mbti = t["mbti"]
    blood = t["blood"]
    gender = t["gender"]
    label = t["label"]
    pts = t["points"]

    color = BLOOD_COLORS[blood]
    is_traverse = (mbti == "INTP" and blood == "O" and gender == "F")
    is_cardinal = (mbti, blood, gender) in cardinals

    pair = mbti[1] + mbti[2]
    if pair == "NT":
        ls = "-"
    elif pair == "NF":
        ls = "--"
    elif pair == "ST":
        ls = "-."
    else:
        ls = ":"

    if is_traverse:
        line_color = "#FF3333"
        lw = 3.4
        alpha = 0.95
        z = 11
    elif is_cardinal:
        line_color = color
        lw = max(2.0, t["lw"])
        alpha = 0.86
        z = 9
    elif t["custom"]:
        line_color = color
        lw = max(1.0, t["lw"])
        alpha = 0.74
        z = 7
    else:
        line_color = color
        lw = 0.9
        alpha = 0.48
        z = 5

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]

    ax.plot(xs, ys, color=line_color, linestyle=ls, linewidth=lw, alpha=alpha, zorder=z, solid_capstyle="round")

    if len(xs) >= 2:
        ax.annotate(
            "",
            xy=(xs[-1], ys[-1]),
            xytext=(xs[-2], ys[-2]),
            arrowprops=dict(arrowstyle="-|>", color=line_color, lw=max(0.45, lw * 0.5), mutation_scale=10 + lw * 1.8, alpha=alpha * 0.9),
            zorder=z,
        )

    if is_traverse:
        mid = len(xs) // 2
        ax.text(
            xs[mid], ys[mid] - 0.28, label,
            ha="center", va="top", fontsize=8.2, fontweight="bold", color=line_color,
            bbox=dict(boxstyle="round,pad=0.13", facecolor="white", edgecolor=line_color, alpha=0.9, linewidth=0.8),
            zorder=12,
        )
    elif is_cardinal:
        ax.text(
            xs[0] + 0.12, ys[0] - 0.12, label,
            ha="left", va="top", fontsize=5.8, fontweight="bold", color=line_color,
            bbox=dict(boxstyle="round,pad=0.09", facecolor="white", edgecolor=line_color, alpha=0.82, linewidth=0.45),
            zorder=10,
        )
    else:
        ax.text(xs[0], ys[0] - 0.07, label, ha="center", va="top", fontsize=3.0, color=line_color, alpha=max(0.46, alpha), zorder=6)

# Legend
legend_items = [
    mpatches.Patch(facecolor="#DD3333", label="O"),
    mpatches.Patch(facecolor="#33AA33", label="A"),
    mpatches.Patch(facecolor="#4499DD", label="B"),
    mpatches.Patch(facecolor="#9944CC", label="AB"),
    Line2D([0], [0], color="#FF3333", lw=3, label="INTP O ♀ Traverse"),
    Line2D([0], [0], color="#FFD700", lw=2, ls="--", label="PLP/Energy"),
    Line2D([0], [0], marker="s", markersize=6, markerfacecolor="#222222", markeredgecolor="#222222", color="white", label="Shared pass-through cell"),
]
ax.legend(
    handles=legend_items,
    loc="upper left",
    bbox_to_anchor=(1.005, 1.0),
    fontsize=8,
    title="Legend",
    title_fontsize=10,
    facecolor="white",
    edgecolor="#888",
)

ax.set_title(
    "128-Type Neurochemical Trajectory Grid\n"
    "16 Columns: IP-W | IJ-W | EP-W | EJ-W | IP-M | IJ-M | EP-M | EJ-M\n"
    "All lines labeled · EJ/EP women split · INTP O♀ full traverse",
    fontsize=14,
    fontweight="bold",
    color="#222",
    pad=18,
)

ax.set_xlim(-0.2, N_COLS + 0.2)
ax.set_ylim(N_ROWS + 0.3, -1.4)
ax.set_aspect(0.65)
ax.axis("off")
plt.tight_layout()

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "128_Trajectory_Grid_2D.png")
plt.savefig(out, dpi=220, bbox_inches="tight", facecolor="white")
print(f"Saved: {out}")
plt.close()
