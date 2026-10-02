import pandas as pd
import itertools
import os

# 사용자 제공 로직: 메인 몸체와 고립된 섬 사이의 누락된 연결 고리 생성
MAIN = set(['1','2','3','4','10','11','12','13','14',
            'flash:center_in','flash_bridge','gateway_peak','mediator:synthetic_alpha'])
ISLAND = set(['core_center','right_branch'])

# 기존에 시도했던 실패 기록 로드
fail_file = "seam_failure_table.csv"
if os.path.exists(fail_file):
    fail = pd.read_csv(fail_file)
else:
    fail = pd.DataFrame(columns=["seam_a", "seam_b"])

seen = set()
for _, r in fail.iterrows():
    a = str(r.get("seam_a","")).strip()
    b = str(r.get("seam_b","")).strip()
    if a and b:
        seen.add(tuple(sorted([a,b])))

rows = []
# 모든 ISLAND 노드와 MAIN 노드 간의 조합을 생성 (기존에 없던 것만)
for a, b in itertools.product(sorted(ISLAND), sorted(MAIN)):
    key = tuple(sorted([a,b]))
    if key not in seen:
        rows.append({"seam_a": a, "seam_b": b})

out = pd.DataFrame(rows)
out.to_csv("missing_bridge_jobs.csv", index=False)
print("missing_bridge_jobs.csv rows =", len(out))
