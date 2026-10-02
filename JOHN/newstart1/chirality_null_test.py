"""chirality_null_test.py

Null hypothesis test for "R-L-R" body-lateralisation pattern found in
spatial_binding.py:
  - Noble gases (7):       R,R,R, L,L,L, R    (6→4→6 periods)
  - Bifurcation (12):      R,R,R, L,L,L,L,L,L, R,R,R

Test: shuffle the body-side assignment 10,000 times and ask how often we
see an R-block followed by an L-block followed by an R-block with group
sizes ≥ given observation.  If p < 0.05, pattern is real.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent
df = pd.read_csv(ROOT / "Z_SPATIAL_ANCHORS.csv")

# code body_name to side: "right" vs "left"
def side(name: str) -> str:
    if "right" in name: return "R"
    if "left"  in name: return "L"
    return "C"

df["side"] = df["body_name"].apply(side)

# observed: RLR block structure for noble & bifurcation
noble_Z = [2, 10, 18, 36, 54, 86, 118]
bifurc_Z = df[df["bifurc"] > 0.99]["Z"].tolist()

def rlr_score(sides: list[str]) -> tuple[int, int, int]:
    """Return sizes of (leading_R, middle_L, trailing_R).  If not RLR, return (0,0,0)."""
    i = 0
    while i < len(sides) and sides[i] == "R":
        i += 1
    r1 = i
    while i < len(sides) and sides[i] == "L":
        i += 1
    L = i - r1
    while i < len(sides) and sides[i] == "R":
        i += 1
    r2 = i - r1 - L
    # remainder must be empty or other, else NOT RLR
    if i < len(sides):
        return (0, 0, 0)
    if r1 == 0 or L == 0 or r2 == 0:
        return (0, 0, 0)
    return (r1, L, r2)


def observed_sides(Z_list):
    return df[df["Z"].isin(Z_list)].sort_values("Z")["side"].tolist()


def null_test(Z_list, n_trials: int = 10000, seed: int = 0):
    obs_sides = observed_sides(Z_list)
    obs_rlr = rlr_score(obs_sides)
    print(f"  Observed sides:  {''.join(obs_sides)}")
    print(f"  Observed RLR:    {obs_rlr}")
    if obs_rlr == (0, 0, 0):
        print("  -> not a pure RLR pattern, null test skipped")
        return
    # pool of sides across all 128 (preserves global R:L ratio)
    side_pool = df["side"].tolist()
    rng = np.random.default_rng(seed)
    k = len(obs_sides)
    hits = 0
    min_sizes = obs_rlr
    for _ in range(n_trials):
        shuffled = rng.choice(side_pool, size=k, replace=False).tolist()
        sh = rlr_score(shuffled)
        # hit if shuffled also forms RLR with groups all >= observed
        if sh != (0, 0, 0) and sh[0] >= min_sizes[0] and sh[1] >= min_sizes[1] and sh[2] >= min_sizes[2]:
            hits += 1
    p = hits / n_trials
    print(f"  p-value (RLR with group sizes >= obs, {n_trials} shuffles): {p:.4f}")
    print(f"  {'REJECT null (pattern real)' if p < 0.05 else 'Fail to reject null'}")


print("=" * 72)
print("Null test: R-L-R chirality in noble gases (n=7)")
print("=" * 72)
null_test(noble_Z)

print("\n" + "=" * 72)
print("Null test: R-L-R chirality in bifurcation elements (n=12)")
print("=" * 72)
null_test(bifurc_Z)

# Global R/L counts
print("\n" + "=" * 72)
print(f"Global distribution of body-sides across 128 Z")
print("=" * 72)
cnt = df["side"].value_counts()
print(cnt)

# Stronger test: just count runs
print("\n" + "=" * 72)
print("Run-length test (more lenient): only 3 runs, first + third same side")
print("=" * 72)
def run_test(Z_list, n_trials: int = 10000, seed: int = 1):
    obs = observed_sides(Z_list)
    def n_runs_and_first(s):
        if not s: return 0, None, None
        runs = 1
        for a, b in zip(s, s[1:]):
            if a != b: runs += 1
        return runs, s[0], s[-1]
    n_obs, first_obs, last_obs = n_runs_and_first(obs)
    match_obs = (n_obs == 3 and first_obs == last_obs)
    print(f"  Observed: {''.join(obs)}  runs={n_obs}  first={first_obs} last={last_obs}  "
          f"3-run+symmetric={'YES' if match_obs else 'NO'}")
    rng = np.random.default_rng(seed)
    pool = df["side"].tolist()
    k = len(obs)
    hits = 0
    for _ in range(n_trials):
        sh = rng.choice(pool, size=k, replace=False).tolist()
        n_sh, f_sh, l_sh = n_runs_and_first(sh)
        if n_sh == 3 and f_sh == l_sh:
            hits += 1
    p = hits / n_trials
    print(f"  p(random shuffle has 3-run + symmetric endings): {p:.4f}")

run_test(noble_Z)
run_test(bifurc_Z)
