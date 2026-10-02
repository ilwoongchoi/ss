# structural_plot.py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ----------------------------------
# 1. 간단한 노드 • 레이어 좌표 정의
#    (필요하면 좌표만 바꿔서 확장)
# ----------------------------------
layers = {
    0: {'nodes': ['O'],                     'r': 0},
    1: {'nodes': ['A', 'B', 'C', 'D'],      'r': 2},
    2: {'nodes': ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'], 'r': 4},
    3: {'nodes': ['M', 'N', 'P', 'Q'],      'r': 6},
    4: {'nodes': ['R', 'S', 'T', 'U'],      'r': 8},   # 예: 추가 24-node용
    5: {'nodes': ['D3'],                    'r': 10},  # Dark-Funnel
}

# 각 레이어에 고르게 배치된 극좌표 → 직교좌표
coords = {}
for level, info in layers.items():
    n = len(info['nodes'])
    for i, nid in enumerate(info['nodes']):
        theta = 2 * 3.14159265 * i / n
        r = info['r']
        coords[nid] = (r * np.cos(theta), r * np.sin(theta), level)  # z축으로 레이어 분리

# ----------------------------------
# 2. 플럭스튜브(경로) 예시
# ----------------------------------
flux_tubes = [
    ('B', 'A'), ('B', 'C'), ('D', 'A'), ('D', 'C'),
    ('G', 'E'), ('G', 'I'), ('F', 'E'), ('F', 'H'),
    # 완전 구속 / 자유 표시용 예시
    ('M', 'N'), ('P', 'Q'),
    # D3 노드가 끌어당기는 경로 예시
    ('D3', 'A'), ('D3', 'Q')
]

# ----------------------------------
# 3. 그림
# ----------------------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')
ax.grid(False)
ax.set_axis_off()

# 노드 색상 맵: 레이어별 색
layer_colors = ['yellow', 'red', 'blue', 'green', 'violet', 'cyan']

for nid, (x, y, z) in coords.items():
    level = int(z)
    ax.scatter(x, y, z, s=200, c=layer_colors[level], edgecolors='white', linewidths=1.5)
    ax.text(x, y, z+0.3, nid, color='white', fontsize=9, ha='center')

# 플럭스튜브는 반투명 라인
for a, b in flux_tubes:
    x = [coords[a][0], coords[b][0]]
    y = [coords[a][1], coords[b][1]]
    z = [coords[a][2], coords[b][2]]
    ax.plot(x, y, z, color='lime', alpha=0.6, linewidth=2)

plt.title('Universal Node & Flux-Tube Structure', color='white', pad=20)
plt.show()
