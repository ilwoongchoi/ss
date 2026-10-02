import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path

# ============================================================================
# SOVEREIGN 128x128 VISUALIZER (PLOTLY 3D)
# PROJECT: FINAL CLOSURE VERIFICATION
# ============================================================================

def visualize_sovereign_map():
    print(" [LOAD] READING 128x128 Z-MAP DATA...")
    candidates = sorted(
        Path(".").glob("SOVEREIGN_128x128_Z_MAP*.csv"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        print(" ERROR: no SOVEREIGN_128x128_Z_MAP*.csv found. Run the generator first.")
        return
    data_file = candidates[0]
    data = pd.read_csv(data_file, header=None)
    z_values = data.values
    print(f" [LOAD] USING DATA FILE: {data_file.name}")

    print(" [RENDER] GENERATING 3D SURFACE PLOT...")
    
    # Define axes
    elements = np.arange(1, 129) # X: 1-128
    windows = np.arange(0, 128)  # Y: 0-127
    
    fig = go.Figure(data=[go.Surface(
        z=z_values,
        x=elements,
        y=windows,
        colorscale='Viridis',
        colorbar=dict(title='Potential (F_final)'),
        lighting=dict(ambient=0.6, diffuse=0.8, fresnel=0.2, specular=0.5, roughness=0.5)
    )])

    fig.update_layout(
        title='THE SOVEREIGN UNIVERSE MAP: 128x128 DETERMINISTIC GRID',
        scene=dict(
            xaxis_title='Atomic Elements (Z=1..128)',
            yaxis_title='Time Windows (0..127)',
            zaxis_title='Sovereign Potential',
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=0.5)
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        template='plotly_dark'
    )

    # Save as HTML for interactive viewing
    output_fn = "SOVEREIGN_128x128_3D_PLOT.html"
    pio.write_html(fig, file=output_fn, auto_open=False)
    
    # Also save a static image for quick reference
    # Note: requires kaleido, if not present it will skip
    try:
        fig.write_image("SOVEREIGN_128x128_3D_PLOT.png", width=1200, height=800)
        print(f" [SUCCESS] STATIC IMAGE SAVED: SOVEREIGN_128x128_3D_PLOT.png")
    except Exception as e:
        print(" [INFO] Static image save skipped (Kaleido not found).")

    print(f" [SUCCESS] INTERACTIVE 3D PLOT GENERATED: {output_fn}")

if __name__ == "__main__":
    visualize_sovereign_map()
