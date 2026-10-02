import geopandas as gpd
import sqlite3

GPKG = r"D:\새 폴더\national_parks_results.gpkg"
conn = sqlite3.connect(GPKG)
cur = conn.cursor()
cur.execute("SELECT table_name FROM gpkg_contents")
layers = [r[0] for r in cur.fetchall()]
conn.close()

print(f"=== Validating {len(layers)} Layers in national_parks_results.gpkg ===")
for l in sorted(layers):
    df = gpd.read_file(GPKG, layer=l)
    print(f"\n[Layer: {l}]")
    print(f"  - Count: {len(df)}")
    print(f"  - Park: {df['park_name'].iloc[0] if 'park_name' in df.columns else 'N/A'}")
    print(f"  - Target Habitat: {df['target_hab'].iloc[0] if 'target_hab' in df.columns else 'N/A'}")
    print(f"  - Columns: {list(df.columns)}")
    print(f"  - Area (ha): min={df['area_ha_final'].min():.3f}, mean={df['area_ha_final'].mean():.3f}, max={df['area_ha_final'].max():.3f}, total={df['area_ha_final'].sum():.1f} ha")
    print(f"  - Distance (m): min={df['Distance'].min():.1f}, mean={df['Distance'].mean():.1f}, max={df['Distance'].max():.1f}")
    print(f"  - Score: min={df['final_score'].min():.3f}, mean={df['final_score'].mean():.3f}, max={df['final_score'].max():.3f}")
    print(f"  - Valid geom check: null={df.geometry.isnull().sum()}, empty={df.geometry.is_empty.sum()}")
