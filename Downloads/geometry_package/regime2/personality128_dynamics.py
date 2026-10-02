from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from generate_128_grid_v4_hysteresis_pure import (
    ALL_MBTI,
    BLOODS,
    GENDERS,
    generate_trajectory_pure,
)


MICRO_PER_MACRO = 4
MACRO_WINDOWS = 4
TOTAL_STEPS = MICRO_PER_MACRO * MACRO_WINDOWS  # 16


def _build_full_day_trajectory(mbti: str, blood: str, gender: str):
    points_sr, flash_sr = generate_trajectory_pure(mbti, blood, gender, "sunrise")
    points_ss, flash_ss = generate_trajectory_pure(mbti, blood, gender, "sunset")

    if len(points_sr) != TOTAL_STEPS or len(points_ss) != TOTAL_STEPS:
        raise ValueError(f"Expected {TOTAL_STEPS} steps per branch, got {len(points_sr)} and {len(points_ss)}")

    merged_points = []
    for macro_idx in range(MACRO_WINDOWS):
        # Macro time is forward (0->1->2->3).
        # Inside each macro window, micro time runs reverse (3->2->1->0).
        branch_points = points_sr if macro_idx < 2 else points_ss
        for micro_idx in range(MICRO_PER_MACRO):
            local_rev = (MICRO_PER_MACRO - 1) - micro_idx
            src_idx = macro_idx * MICRO_PER_MACRO + local_rev
            merged_points.append(branch_points[src_idx])

    merged_flash = [
        {**event, "source_branch": "sunrise"} for event in flash_sr
    ] + [
        {**event, "source_branch": "sunset"} for event in flash_ss
    ]
    return merged_points, merged_flash


def generate_128_personality_trajectories(branch_mode: str = "full_day") -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    if branch_mode not in ("full_day", "sunrise", "sunset"):
        raise ValueError("branch_mode must be 'full_day', 'sunrise', or 'sunset'")
    for mbti in ALL_MBTI:
        for blood in BLOODS:
            for gender in GENDERS:
                if branch_mode == "full_day":
                    points, flash_events = _build_full_day_trajectory(mbti, blood, gender)
                    branch_label = "full_day"
                else:
                    points, flash_events = generate_trajectory_pure(mbti, blood, gender, branch_mode)
                    branch_label = branch_mode
                rows.append(
                    {
                        "mbti": mbti,
                        "blood": blood,
                        "gender": gender,
                        "branch": branch_label,
                        "trajectory": [
                            {
                                "step": int(i),
                                "x": float(p[0]),
                                "y": float(p[1]),
                                "renorm": float(p[2]),
                                "is_flash_step": bool(p[3]),
                            }
                            for i, p in enumerate(points)
                        ],
                        "flash_events": flash_events,
                        "flash_count": int(len(flash_events)),
                    }
                )
    return rows


def save_128_personality_trajectories(output_dir: str = "out/regime2", branch_mode: str = "full_day") -> Dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = generate_128_personality_trajectories(branch_mode=branch_mode)

    json_path = out / "personality128_trajectories.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    summary_path = out / "personality128_summary.csv"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("mbti,blood,gender,branch,steps,flash_count\n")
        for row in rows:
            f.write(
                f"{row['mbti']},{row['blood']},{row['gender']},{row['branch']},{len(row['trajectory'])},{row['flash_count']}\n"
            )

    return {"json": str(json_path), "summary_csv": str(summary_path)}


if __name__ == "__main__":
    paths = save_128_personality_trajectories()
    print(paths["json"])
    print(paths["summary_csv"])
