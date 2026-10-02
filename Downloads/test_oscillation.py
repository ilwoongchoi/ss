지금 바나나사러왔는데 약간 까매진 짙노란 콜럼비아산 바나나, 돌레 코스타리카산 바나나 , 덜익은 코스타리카산 , 약간 초록 덜익은 콜럼비아산 바나나 플랜팅, 완전히 까매진 콜럼비아 플랜팅 이렇게 네개있는데 뭐먹어야돼.아님그냥세인스버리에 파는 돌레랑 비슷한 슈퍼마켓산 먹어야되나? 뭐가항상성에 제일 좋아import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
from universe_math_structures import compute_8d, compute_4layers, integrate_8d, DIMS

v = compute_8d('ENTP', 'M', 'O')
layers = compute_4layers(v)

for layer_name in ['body', 'observer', 'bridge', 'dark']:
    V = dict(layers[layer_name])
    t_h = 0.0
    print(f'\n=== {layer_name} (weight-based) ===')
    for t in range(16):
        if t > 0:
            V, _ = integrate_8d(layers[layer_name], t_h, t * 1.5, dt=0.5, init_pos=V)
            t_h = t * 1.5
        vals = {d: round(V[d], 2) for d in DIMS}
        levels = {d: int(V[d] * 16) for d in DIMS}
        print(f't={t:2d}: {vals}  L={levels}')
