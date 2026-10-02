"""
지구 내부 입자-지질 통합 3D 시각화
====================================
4가지 데이터 모델을 하나의 구체에 투영:
  1. LLVP (하부 맨틀 거대 블롭) - 지진파 토모그래피
  2. Slab2 (섭입대 킹크) - 판구조 3D
  3. AGM2015 (지표 안티뉴트리노 방출)
  4. Andosols (화산재 토양 안테나 배열)

실행:
    pip install plotly numpy
    python earth_particle_circuit.py
"""

import numpy as np
import plotly.graph_objects as go


# ---------------------------------------------------------------------------
# 유틸: 위경도 -> 3D 직교좌표 변환 (반지름 r에서의 위치)
# ---------------------------------------------------------------------------
def latlon_to_xyz(lat, lon, r):
    lat = np.radians(lat)
    lon = np.radians(lon)
    x = r * np.cos(lat) * np.cos(lon)
    y = r * np.cos(lat) * np.sin(lon)
    z = r * np.sin(lat)
    return x, y, z


# ---------------------------------------------------------------------------
# 1) 기본 구체 레이어 (지각, 맨틀 전이대, 외핵, 내핵)
# ---------------------------------------------------------------------------
R_SURFACE = 6371      # 지표
R_MANTLE_TZ = 5711    # 660km 전이대
R_CMB = 3480          # 핵-맨틀 경계 (Core-Mantle Boundary)
R_INNER = 1220        # 내핵

def sphere(r, n=60):
    u = np.linspace(0, 2 * np.pi, n)
    v = np.linspace(0, np.pi, n)
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones_like(u), np.cos(v))
    return x, y, z


# ---------------------------------------------------------------------------
# 2) LLVP 블롭 (아프리카 Tuzo, 태평양 Jason) - 하부 맨틀 CMB 바로 위
# ---------------------------------------------------------------------------
# 실제 지진파 토모그래피 근사 위치
LLVPS = [
    {"name": "African LLVP (Tuzo)", "lat": 0, "lon": 20, "size": 2200},
    {"name": "Pacific LLVP (Jason)", "lat": -10, "lon": -170, "size": 2400},
]

def make_blob(lat, lon, size, r_base=R_CMB + 400):
    """CMB 위 약 400km 고도에 박힌 납작한 타원체 블롭."""
    cx, cy, cz = latlon_to_xyz(lat, lon, r_base)
    # 지구 중심에서 블롭 중심 방향 단위벡터
    n = np.array([cx, cy, cz]) / np.linalg.norm([cx, cy, cz])
    # 접평면 상의 두 기저
    tmp = np.array([0, 0, 1]) if abs(n[2]) < 0.9 else np.array([1, 0, 0])
    u = np.cross(n, tmp); u /= np.linalg.norm(u)
    v = np.cross(n, u)
    # 타원체: 접평면 방향으로 넓게, 방사 방향으로 얇게
    phi = np.linspace(0, 2 * np.pi, 40)
    th = np.linspace(0, np.pi, 20)
    P, T = np.meshgrid(phi, th)
    a, b, c = size, size, size * 0.35
    X = a * np.sin(T) * np.cos(P)
    Y = b * np.sin(T) * np.sin(P)
    Z = c * np.cos(T)
    pts = (X[..., None] * u + Y[..., None] * v + Z[..., None] * n)
    return pts[..., 0] + cx, pts[..., 1] + cy, pts[..., 2] + cz


# ---------------------------------------------------------------------------
# 3) Slab 킹크 (섭입판) - 주요 6곳
# ---------------------------------------------------------------------------
SLABS = [
    {"name": "Bermuda-Caribbean Kink", "lat": 25, "lon": -65, "depth": 900,
     "dip": 55, "strike": 30, "note": "고대 Farallon 슬랩 잔해 (난소 킹크)"},
    {"name": "Andes (Nazca)", "lat": -20, "lon": -70, "depth": 700, "dip": 30, "strike": 0},
    {"name": "Japan (Pacific)", "lat": 38, "lon": 142, "depth": 660, "dip": 45, "strike": 200},
    {"name": "Sumatra", "lat": -2, "lon": 100, "depth": 600, "dip": 40, "strike": 315},
    {"name": "Aleutian", "lat": 52, "lon": -175, "depth": 500, "dip": 50, "strike": 280},
    {"name": "Tonga", "lat": -20, "lon": -175, "depth": 700, "dip": 60, "strike": 200},
]

def slab_line(lat, lon, depth, dip, strike, length=1500):
    """지표에서 맨틀 내부로 꺾여 들어가는 슬랩을 꺾인 선으로 표현."""
    # 1) 지표에서 시작
    x0, y0, z0 = latlon_to_xyz(lat, lon, R_SURFACE)
    # 2) 얕은 섭입 구간
    r1 = R_SURFACE - 300
    x1, y1, z1 = latlon_to_xyz(lat - 2, lon + 2, r1)
    # 3) 전이대에서 꺾임 (킹크)
    r2 = R_SURFACE - depth
    x2, y2, z2 = latlon_to_xyz(lat - 4, lon + 4, r2)
    # 4) 하부 맨틀 정체
    r3 = max(R_CMB + 200, R_SURFACE - depth - 300)
    x3, y3, z3 = latlon_to_xyz(lat - 4, lon + 6, r3)
    return [x0, x1, x2, x3], [y0, y1, y2, y3], [z0, z1, z2, z3]


# ---------------------------------------------------------------------------
# 4) AGM2015 안티뉴트리노 방출 핫스팟 (지각 U/Th/K 농축지)
# ---------------------------------------------------------------------------
NU_HOTSPOTS = [
    ("Himalaya-Tibet", 30, 85, 9.5),
    ("Andes", -20, -68, 8.8),
    ("Bermuda Anomaly", 28, -65, 7.5),
    ("Scandinavia Shield", 65, 20, 8.2),
    ("Canadian Shield", 55, -95, 8.0),
    ("East Africa Rift", -3, 36, 7.8),
    ("Japan Arc", 36, 138, 7.6),
    ("Western Australia", -25, 120, 7.2),
]


# ---------------------------------------------------------------------------
# 5) 안도솔 (화산재 토양) 주요 분포대 - 환태평양 + 동아프리카
# ---------------------------------------------------------------------------
ANDOSOLS = [
    ("Andes Belt", -20, -70),
    ("Central America", 12, -85),
    ("Cascades", 45, -122),
    ("Kamchatka", 55, 160),
    ("Japan", 36, 138),
    ("Philippines", 13, 123),
    ("Indonesia", -6, 110),
    ("New Zealand", -38, 176),
    ("Kilimanjaro-EAR", -3, 37),
    ("Iceland", 64, -19),
    ("Italy", 41, 14),
    ("Hawaii", 20, -156),
]


# ---------------------------------------------------------------------------
# Figure 조립
# ---------------------------------------------------------------------------
fig = go.Figure()

# 지표 (반투명)
x, y, z = sphere(R_SURFACE)
fig.add_surface(x=x, y=y, z=z, opacity=0.08,
                colorscale=[[0, '#1f77b4'], [1, '#1f77b4']],
                showscale=False, name='Crust', hoverinfo='skip')

# 660km 전이대
x, y, z = sphere(R_MANTLE_TZ)
fig.add_surface(x=x, y=y, z=z, opacity=0.05,
                colorscale=[[0, '#8c564b'], [1, '#8c564b']],
                showscale=False, hoverinfo='skip')

# 외핵
x, y, z = sphere(R_CMB)
fig.add_surface(x=x, y=y, z=z, opacity=0.35,
                colorscale=[[0, '#ff7f0e'], [1, '#ffbb78']],
                showscale=False, name='Outer Core', hoverinfo='skip')

# 내핵
x, y, z = sphere(R_INNER)
fig.add_surface(x=x, y=y, z=z, opacity=0.9,
                colorscale=[[0, '#d62728'], [1, '#ffff99']],
                showscale=False, name='Inner Core', hoverinfo='skip')

# LLVP 블롭
for b in LLVPS:
    bx, by, bz = make_blob(b["lat"], b["lon"], b["size"])
    fig.add_surface(x=bx, y=by, z=bz, opacity=0.55,
                    colorscale=[[0, '#6a0dad'], [1, '#b388ff']],
                    showscale=False, name=b["name"],
                    hovertext=f"{b['name']}<br>철-규산염 블롭 / 밀도 5.5~6.0 g/cm³<br>뮤온·페로브스카이트 매질")

# Slab 킹크
for s in SLABS:
    sx, sy, sz = slab_line(s["lat"], s["lon"], s["depth"], s["dip"], s["strike"])
    color = 'magenta' if 'Bermuda' in s['name'] else '#00bcd4'
    width = 10 if 'Bermuda' in s['name'] else 5
    fig.add_trace(go.Scatter3d(
        x=sx, y=sy, z=sz, mode='lines+markers',
        line=dict(color=color, width=width),
        marker=dict(size=4, color=color),
        name=f"Slab: {s['name']}",
        hovertext=s.get('note', s['name'])
    ))

# 안티뉴트리노 핫스팟
nu_x, nu_y, nu_z, nu_size, nu_text = [], [], [], [], []
for name, lat, lon, flux in NU_HOTSPOTS:
    px, py, pz = latlon_to_xyz(lat, lon, R_SURFACE * 1.02)
    nu_x.append(px); nu_y.append(py); nu_z.append(pz)
    nu_size.append(flux * 2.5)
    nu_text.append(f"{name}<br>ν̄ flux: {flux} TNU<br>U/Th/K 붕괴 유래")

fig.add_trace(go.Scatter3d(
    x=nu_x, y=nu_y, z=nu_z, mode='markers+text',
    marker=dict(size=nu_size, color='yellow', opacity=0.9,
                line=dict(color='orange', width=1)),
    text=[t.split('<br>')[0] for t in NU_HOTSPOTS and [h[0] for h in NU_HOTSPOTS]],
    textposition='top center',
    textfont=dict(color='yellow', size=10),
    hovertext=nu_text,
    name='Antineutrino Hotspots (AGM2015)'
))

# 안도솔 안테나
an_x, an_y, an_z, an_text = [], [], [], []
for name, lat, lon in ANDOSOLS:
    px, py, pz = latlon_to_xyz(lat, lon, R_SURFACE * 1.01)
    an_x.append(px); an_y.append(py); an_z.append(pz)
    an_text.append(f"Andosol: {name}<br>Al/Fe/알로판<br>타우 뉴트리노 안테나")

fig.add_trace(go.Scatter3d(
    x=an_x, y=an_y, z=an_z, mode='markers',
    marker=dict(size=7, color='lime', symbol='diamond',
                line=dict(color='green', width=1)),
    hovertext=an_text, name='Andosols (안테나 배열)'
))

# 핵심 회로 노드 라벨
CIRCUIT_NODES = [
    ("Bermuda Kink (Sink)", 28, -65, 'magenta'),
    ("Kilimanjaro (Proc)", -3, 37, 'cyan'),
    ("Andes (Output)", -20, -68, 'lime'),
    ("Oman (Basin)", 21, 57, 'orange'),
    ("Nepal (Foot)", 28, 84, 'white'),
    ("Ethiopia (N)", 9, 40, 'red'),
    ("Patagonia (GND)", -50, -70, 'pink'),
    ("Hudson Bay (In)", 60, -85, 'aqua'),
]
cn_x, cn_y, cn_z, cn_text, cn_col = [], [], [], [], []
for name, lat, lon, col in CIRCUIT_NODES:
    px, py, pz = latlon_to_xyz(lat, lon, R_SURFACE * 1.08)
    cn_x.append(px); cn_y.append(py); cn_z.append(pz)
    cn_text.append(name); cn_col.append(col)

fig.add_trace(go.Scatter3d(
    x=cn_x, y=cn_y, z=cn_z, mode='markers+text',
    marker=dict(size=10, color=cn_col, symbol='x'),
    text=cn_text, textposition='top center',
    textfont=dict(color='white', size=11),
    name='Circuit Nodes'
))

# 레이아웃
fig.update_layout(
    title=dict(
        text="<b>지구 내부 입자-지질 통합 회로</b><br>"
             "<sub>LLVP 블롭 · Slab 킹크 · 안티뉴트리노 방출 · 안도솔 안테나</sub>",
        x=0.5, font=dict(color='white', size=16)
    ),
    paper_bgcolor='black',
    scene=dict(
        bgcolor='black',
        xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        aspectmode='data',
        camera=dict(eye=dict(x=1.5, y=1.5, z=0.9))
    ),
    legend=dict(bgcolor='rgba(0,0,0,0.5)', font=dict(color='white')),
    margin=dict(l=0, r=0, t=60, b=0),
    height=900
)

out = "earth_particle_circuit.html"
fig.write_html(out)
print(f"Saved -> {out} (브라우저로 열면 회전·줌 가능)")
fig.show()
