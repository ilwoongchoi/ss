import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path


def visualize_gn_map():
    candidates = sorted(
        Path(".").glob("SOVEREIGN_GN_128x128_Z_MAP*.csv"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        print(" ERROR: no SOVEREIGN_GN_128x128_Z_MAP*.csv found.")
        return

    data_file = candidates[0]
    print(f" [LOAD] USING DATA FILE: {data_file.name}")
    z_values = pd.read_csv(data_file, header=None).values

    x = np.arange(1, 129)
    y = np.arange(0, 128)
    fig = go.Figure(
        data=[
            go.Surface(
                z=z_values,
                x=x,
                y=y,
                colorscale="Turbo",
                colorbar=dict(title="GN Potential"),
            )
        ]
    )
    fig.update_layout(
        title="SOVEREIGN GN MAP (128x128)",
        scene=dict(
            xaxis_title="Atomic Index (1..128)",
            yaxis_title="Time Window (0..127)",
            zaxis_title="GN Potential",
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=0.5),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        template="plotly_dark",
    )

    html_file = "SOVEREIGN_GN_128x128_3D_PLOT.html"
    pio.write_html(fig, file=html_file, auto_open=False)
    print(f" [SUCCESS] INTERACTIVE PLOT: {html_file}")

    try:
        png_file = "SOVEREIGN_GN_128x128_3D_PLOT.png"
        fig.write_image(png_file, width=1200, height=800)
        print(f" [SUCCESS] STATIC IMAGE: {png_file}")
    except Exception:
        print(" [INFO] Static image skipped (kaleido not available).")


if __name__ == "__main__":
    visualize_gn_map()
