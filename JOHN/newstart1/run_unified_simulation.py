import numpy as np
import matplotlib.pyplot as plt
import sovereign_dynamics as sd
import constants
import fusion_core

def run_simulation(n_steps=128, dt=0.01):
    """Runs a full simulation using the unified sovereign dynamics."""
    # Initial state (example)
    z = np.random.rand(8) * (1 + 1j) * 0.1
    z_history = [z]

    # Observer nodes state (example)
    observers = np.random.rand(4) * 0.1
    observer_history = [observers]

    # Channel state (example, all 'off')
    channels = {name: 'off' for name in fusion_core.CHANNEL_MAP.keys()}

    for t in range(n_steps):
        # Main K8 dynamics
        z = sd.get_dynamics_update(z, phase='phase1', channels=channels, dt=dt)

        # Lensing
        z += sd.get_lensing_update(z) * dt

        # Rebranching at t=88
        if t == 88:
            primitives = z[[fusion_core.IDX['quark'], fusion_core.IDX['gluon'], fusion_core.IDX['higgs']]]
            z = sd.rebranch(primitives)

        # Calculate observer states from K8 particles
        observers = sd.calculate_observers(z)
        # Apply Clifford Torus constraint
        observers = sd.apply_clifford_constraint(observers)

        z_history.append(z)
        observer_history.append(observers)

        # Verify diagonality in the plasma phase (example: t > 100)
        if t > 100:
            w = fusion_core.apply_channels(channels)
            L = fusion_core.laplacian(w)
            diagonality = sd.verify_diagonality(L)
            print(f'Step {t}: Diagonality = {diagonality:.4f}')

    return np.array(z_history), np.array(observer_history)

if __name__ == '__main__':
    z_traj, obs_traj = run_simulation()

    # Plotting results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # K8 particle trajectories
    for i in range(8):
        ax1.plot(np.abs(z_traj[:, i]), label=fusion_core.SUBJECTS[i])
    ax1.set_title('K8 Particle Amplitudes')
    ax1.legend()
    ax1.set_xlabel('Time Step')
    ax1.set_ylabel('Amplitude')

    # Observer node trajectories on Clifford Torus planes
    ax2.plot(obs_traj[:, 0], obs_traj[:, 1], label='Extravert Plane (LSS vs RSS)')
    ax2.plot(obs_traj[:, 2], obs_traj[:, 3], label='Introvert Plane (LE vs RE)')
    ax2.set_title('Observer Nodes on Clifford Torus Projections')
    ax2.set_xlabel('Left Node')
    ax2.set_ylabel('Right Node')
    ax2.legend()
    ax2.set_aspect('equal')

    plt.tight_layout()
    plt.savefig('unified_simulation_results.png')
    print('Simulation complete. Results saved to unified_simulation_results.png')
