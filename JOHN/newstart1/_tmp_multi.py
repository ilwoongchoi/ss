import pandas as pd
import matplotlib.pyplot as plt
from geometry_package.edge_stack_master_equation import sovereign_dynamics_step

# load 128 initial states
init_df = pd.read_csv('analysis_results/final_locked_grid_128.csv')
steps = 64
traj = []
for _, row in init_df.iterrows():
    state = row[['BM','BW','SM','SW']].to_numpy()
    xs=[]; ys=[]; zs=[]
    # simple clock: advance 1 minute per step
    minute = 0
    for _ in range(steps):
        hh = int((minute//60)%24)
        mm = int(minute%60)
        clock = f"{hh:02d}:{mm:02d}"
        out = sovereign_dynamics_step(state, phase_fill=0.0, clock_hhmm=clock, dt=0.05)
        state = out['state_next']
        xs.append(state[0]); ys.append(state[1]); zs.append(state[2])
        minute += 1
    traj.append((xs,ys,zs))

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')
for xs,ys,zs in traj:
    ax.plot(xs,ys,zs,alpha=0.3,linewidth=0.4)
ax.set_xlabel('BM')
ax.set_ylabel('BW')
ax.set_zlabel('SM')
plt.tight_layout()
plt.savefig('analysis_results/final_locked_128_multi_traj.png', dpi=300)
print('saved analysis_results/final_locked_128_multi_traj.png')
