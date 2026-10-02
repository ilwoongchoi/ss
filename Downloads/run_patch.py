import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.ops import unary_union
from scipy.spatial import cKDTree
import warnings
warnings.filterwarnings("ignore")

SRC = r"c:\Users\User\Downloads\chilterns_results.gpkg"
BASE = r"d:\새 폴더"
OUT = r"c:\Users\User\Downloads\chilterns_results.gpkg"

print("=== 1. Reading existing layers from GPKG ===")
chilterns = gpd.read_file(SRC, layer="chilterns_boundary")
aw_clip = gpd.read_file(SRC, layer="AW_chilterns")
cg_clip = gpd.read_file(SRC, layer="CG_chilterns")
phi_clip = gpd.read_file(SRC, layer="PHI_chilterns")
print(f"  Chilterns: {len(chilterns)}, AW: {len(aw_clip)}, CG: {len(cg_clip)}, PHI: {len(phi_clip)}")

print("=== 2. Clipping Roads ===")
road_files = [
    rf"{BASE}\oproad_essh_gb\data\SP_RoadLink.shp",
    rf"{BASE}\oproad_essh_gb\data\SU_RoadLink.shp",
    rf"{BASE}\oproad_essh_gb\data\TL_RoadLink.shp",
    rf"{BASE}\oproad_essh_gb\data\TQ_RoadLink.shp"
]
road_dfs = []
for f in road_files:
    try:
        df = gpd.read_file(f).to_crs("EPSG:27700")
        road_dfs.append(df)
        print(f"  Loaded {f}: {len(df)} links")
    except Exception as e:
        print(f"  Skip {f}: {e}")

roads = gpd.GeoDataFrame(pd.concat(road_dfs, ignore_index=True), crs="EPSG:27700")
roads_clip = gpd.clip(roads, chilterns).reset_index(drop=True)
roads_clip.to_file(OUT, layer="Roads_chilterns", driver="GPKG")
print(f"  Roads clipped: {len(roads_clip)} features")

print("=== 3. CG Centroids & Distances ===")
cg_cent = cg_clip.copy()
cg_cent["geometry"] = cg_cent.geometry.centroid
cg_pts = np.array([(p.x, p.y) for p in cg_cent.geometry])
tree_cg = cKDTree(cg_pts)

print("=== 4. AW 250m Buffer & Gap ===")
aw_union = unary_union(aw_clip.geometry)
aw_buf_geom = aw_union.buffer(250)
cg_union = unary_union(cg_clip.geometry)
gap_geom = aw_buf_geom.difference(cg_union)
gap = gpd.GeoDataFrame(geometry=[gap_geom], crs="EPSG:27700")

print("=== 5. Exploding and Intersecting Gap with PHI ===")
gap_exploded = gap.explode(index_parts=False).reset_index(drop=True)
gap_phi = gpd.overlay(gap_exploded, phi_clip, how="intersection")
gap_phi = gap_phi.explode(index_parts=False).reset_index(drop=True)
gap_phi = gap_phi[gap_phi.geometry.type.isin(['Polygon', 'MultiPolygon'])].reset_index(drop=True)
gap_phi["area_ha"] = gap_phi.geometry.area / 10000.0
gap_phi = gap_phi[gap_phi["area_ha"] >= 0.05].reset_index(drop=True)
gap_phi.to_file(OUT, layer="gap_phi_clean", driver="GPKG")
print(f"  Viable patches (>=0.05 ha): {len(gap_phi)}")

print("=== 6. Distance to CG ===")
opp_pts = np.array([(p.x, p.y) for p in gap_phi.geometry.centroid])
opp_dists, _ = tree_cg.query(opp_pts, k=1)
gap_phi["Distance"] = opp_dists

print("=== 7. Buffer Roads & Difference ===")
road_buf = unary_union(roads_clip.geometry.buffer(10))
diff_geoms = [geom.difference(road_buf) for geom in gap_phi.geometry]
gap_phi["geometry"] = diff_geoms
gap_phi = gap_phi.explode(index_parts=False).reset_index(drop=True)
gap_phi = gap_phi[gap_phi.geometry.type.isin(['Polygon', 'MultiPolygon']) & (~gap_phi.geometry.is_empty)].reset_index(drop=True)
gap_phi["area_ha_final"] = gap_phi.geometry.area / 10000.0
gap_phi = gap_phi[gap_phi["area_ha_final"] >= 0.05].reset_index(drop=True)
print(f"  Patches after road excision: {len(gap_phi)}")

print("=== 8. Scoring ===")
max_d = gap_phi["Distance"].max() if len(gap_phi) > 0 else 1
max_a = gap_phi["area_ha_final"].max() if len(gap_phi) > 0 else 1
gap_phi["proximity_score"] = 1.0 - (gap_phi["Distance"] / max_d)
gap_phi["area_score"] = gap_phi["area_ha_final"] / max_a
gap_phi["final_score"] = (gap_phi["proximity_score"] * 0.5) + (gap_phi["area_score"] * 0.5)

cols_keep = [c for c in ['Main_Habit', 'MainHabs', 'Habitat_Type', 'area_ha_final', 'Distance', 'proximity_score', 'area_score', 'final_score', 'geometry'] if c in gap_phi.columns]
final_out = gap_phi[cols_keep].copy()
final_out.to_file(OUT, layer="AW_final_opportunities", driver="GPKG")
print(f"  SUCCESS! AW_final_opportunities saved: {len(final_out)} features")
print(f"  Scores: min={final_out['final_score'].min():.3f}, mean={final_out['final_score'].mean():.3f}, max={final_out['final_score'].max():.3f}")
