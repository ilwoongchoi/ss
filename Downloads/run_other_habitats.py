import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.ops import unary_union
from scipy.spatial import cKDTree
import warnings
warnings.filterwarnings("ignore")

OUT = r"c:\Users\User\Downloads\chilterns_results.gpkg"

print("=== Loading Base Layers ===")
chilterns = gpd.read_file(OUT, layer="chilterns_boundary")
aw_clip = gpd.read_file(OUT, layer="AW_chilterns")
phi_clip = gpd.read_file(OUT, layer="PHI_chilterns")
roads_clip = gpd.read_file(OUT, layer="Roads_chilterns")
road_buf = unary_union(roads_clip.geometry.buffer(10))
aw_buf_geom = unary_union(aw_clip.geometry).buffer(250)

targets = [
    ("Heathland_chilterns", "AW_final_opportunities_heath"),
    ("Lowland_Meadows_chilterns", "AW_final_opportunities_meadows")
]

for in_layer, out_layer in targets:
    print(f"\nProcessing {in_layer} -> {out_layer}...")
    hab = gpd.read_file(OUT, layer=in_layer)
    if len(hab) == 0:
        print(f"  Empty layer: {in_layer}")
        continue

    # Gap
    hab_union = unary_union(hab.geometry)
    gap_geom = aw_buf_geom.difference(hab_union)
    gap = gpd.GeoDataFrame(geometry=[gap_geom], crs="EPSG:27700").explode(index_parts=False).reset_index(drop=True)

    # Intersect with PHI
    gap_phi = gpd.overlay(gap, phi_clip, how="intersection")
    gap_phi = gap_phi.explode(index_parts=False).reset_index(drop=True)
    gap_phi = gap_phi[gap_phi.geometry.type.isin(['Polygon', 'MultiPolygon'])].reset_index(drop=True)
    gap_phi["area_ha"] = gap_phi.geometry.area / 10000.0
    gap_phi = gap_phi[gap_phi["area_ha"] >= 0.05].reset_index(drop=True)

    # Distances to target habitat
    pts = np.array([(p.x, p.y) for p in hab.geometry.centroid])
    tree = cKDTree(pts)
    opp_pts = np.array([(p.x, p.y) for p in gap_phi.geometry.centroid])
    dists, _ = tree.query(opp_pts, k=1)
    gap_phi["Distance"] = dists

    # Difference roads
    diff_geoms = [geom.difference(road_buf) for geom in gap_phi.geometry]
    gap_phi["geometry"] = diff_geoms
    gap_phi = gap_phi.explode(index_parts=False).reset_index(drop=True)
    gap_phi = gap_phi[gap_phi.geometry.type.isin(['Polygon', 'MultiPolygon']) & (~gap_phi.geometry.is_empty)].reset_index(drop=True)
    gap_phi["area_ha_final"] = gap_phi.geometry.area / 10000.0
    gap_phi = gap_phi[gap_phi["area_ha_final"] >= 0.05].reset_index(drop=True)

    # Scoring
    max_d = gap_phi["Distance"].max() if len(gap_phi) > 0 else 1
    max_a = gap_phi["area_ha_final"].max() if len(gap_phi) > 0 else 1
    gap_phi["proximity_score"] = 1.0 - (gap_phi["Distance"] / max_d)
    gap_phi["area_score"] = gap_phi["area_ha_final"] / max_a
    gap_phi["final_score"] = (gap_phi["proximity_score"] * 0.5) + (gap_phi["area_score"] * 0.5)

    cols_keep = [c for c in ['Main_Habit', 'MainHabs', 'Habitat_Type', 'area_ha_final', 'Distance', 'proximity_score', 'area_score', 'final_score', 'geometry'] if c in gap_phi.columns]
    res = gap_phi[cols_keep].copy()
    res.to_file(OUT, layer=out_layer, driver="GPKG")
    print(f"  Saved {out_layer}: {len(res)} features (mean score: {res['final_score'].mean():.3f})")

print("\n=== ALL COMPLETED! ===")
