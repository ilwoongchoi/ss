import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.ops import unary_union
from scipy.spatial import cKDTree
import os, warnings
warnings.filterwarnings("ignore")

BASE = r"d:\새 폴더"
OUT = r"d:\새 폴더\chilterns_results.gpkg"

print("=== Step 1: Load & filter Chilterns boundary ===")
aonb = gpd.read_file(rf"{BASE}\Areas_of_Outstanding_Natural_Beauty_England.gpkg", layer="Areas_of_Outstanding_Natural_Beauty_England")
chilterns = aonb[aonb["name"].str.contains("Chiltern", case=False, na=False)].copy()
chilterns = chilterns.to_crs("EPSG:27700")
chilterns_geom = unary_union(chilterns.geometry)
print(f"  Chilterns: {len(chilterns)} feature(s)")

print("=== Step 2: Clip Ancient Woodland ===")
aw = gpd.read_file(rf"{BASE}\Ancient_Woodland_England.gpkg (1)\Ancient_Woodland_England.gpkg", layer="Ancient_Woodland_England")
aw = aw.to_crs("EPSG:27700")
aw_clip = gpd.clip(aw, chilterns).reset_index(drop=True)
aw_clip.to_file(OUT, layer="AW_chilterns", driver="GPKG")
print(f"  AW: {len(aw_clip)} features")

print("=== Step 3: Clip Calcareous Grassland ===")
cg = gpd.read_file(rf"{BASE}\Habitat_Networks_Individual_England.gpkg\Habitat_Networks_Individual_England.gpkg", layer="Calcareous_grassland")
cg = cg.to_crs("EPSG:27700")
cg_clip = gpd.clip(cg, chilterns).reset_index(drop=True)
cg_clip.to_file(OUT, layer="CG_chilterns", driver="GPKG")
print(f"  CG: {len(cg_clip)} features")

print("=== Step 4: Clip PHI ===")
phi = gpd.read_file(rf"{BASE}\Priority_Habitats_Inventory_England.geojson\Priority_Habitat_Inventory_England.geojson")
phi = phi.to_crs("EPSG:27700")
phi_clip = gpd.clip(phi, chilterns).reset_index(drop=True)
phi_clip.to_file(OUT, layer="PHI_chilterns", driver="GPKG")
print(f"  PHI: {len(phi_clip)} features")

print("=== Step 5: Clip Roads ===")
road_files = [rf"{BASE}\oproad_essh_gb\data\SP_RoadLink.shp",
              rf"{BASE}\oproad_essh_gb\data\SU_RoadLink.shp",
              rf"{BASE}\oproad_essh_gb\data\TL_RoadLink.shp"]
roads = gpd.GeoDataFrame(pd.concat([gpd.read_file(f).to_crs("EPSG:27700") for f in road_files], ignore_index=True))
roads_clip = gpd.clip(roads, chilterns).reset_index(drop=True)
roads_clip.to_file(OUT, layer="Roads_chilterns", driver="GPKG")
print(f"  Roads: {len(roads_clip)} features")

print("=== Step 6: CG centroids ===")
cg_cent = cg_clip.copy()
cg_cent["geometry"] = cg_cent.geometry.centroid
cg_cent["grass_id"] = range(1, len(cg_cent) + 1)
cg_cent.to_file(OUT, layer="CG_centroids", driver="GPKG")

print("=== Step 7: AW centroids ===")
aw_cent = aw_clip.copy()
aw_cent["geometry"] = aw_cent.geometry.centroid
aw_cent.to_file(OUT, layer="AW_centroids", driver="GPKG")

print("=== Step 8: AW to CG nearest distance ===")
aw_pts = np.array([(p.x, p.y) for p in aw_cent.geometry])
cg_pts = np.array([(p.x, p.y) for p in cg_cent.geometry])
tree = cKDTree(cg_pts)
dists, idxs = tree.query(aw_pts, k=1)
aw_clip["Distance"] = dists
aw_clip["NearestCG_ID"] = [cg_cent["grass_id"].iloc[i] for i in idxs]
aw_clip.to_file(OUT, layer="AW_distance_to_CG", driver="GPKG")
print(f"  AW distance range: {dists.min():.0f} - {dists.max():.0f} m")

print("=== Step 9: 250m Buffer ===")
aw_buf_geom = aw_clip.geometry.buffer(250)
aw_buf = gpd.GeoDataFrame(geometry=[unary_union(aw_buf_geom)], crs="EPSG:27700")
aw_buf.to_file(OUT, layer="AW_250m_buffer", driver="GPKG")

print("=== Step 10: Gap (buffer - CG) ===")
gap_geom = aw_buf.geometry.iloc[0].difference(unary_union(cg_clip.geometry))
gap = gpd.GeoDataFrame(geometry=[gap_geom], crs="EPSG:27700")
gap = gap[gap.geometry.notna() & ~gap.geometry.is_empty]
print(f"  Gap: {len(gap)} feature(s)")

print("=== Step 11: Gap x PHI intersection ===")
gap_phi = gpd.overlay(gap, phi_clip, how="intersection", keep_geom_type=False)
if len(gap_phi) == 0:
    print("  WARNING: No intersection with PHI! Using gap as-is.")
    gap_phi = gap.copy()
    gap_phi["MainHabs"] = "Unknown"
gap_phi["area_ha"] = gap_phi.geometry.area / 10000.0
gap_phi.to_file(OUT, layer="gap_phi", driver="GPKG")
print(f"  Gap x PHI: {len(gap_phi)} features")

print("=== Step 12: Suitable habitats ===")
if "MainHabs" in gap_phi.columns:
    suitable = gap_phi[gap_phi["MainHabs"].notna()].reset_index(drop=True).copy()
else:
    suitable = gap_phi.copy()
if len(suitable) == 0:
    suitable = gap_phi.copy()
suitable.to_file(OUT, layer="AW_connectivity_opportunities", driver="GPKG")
print(f"  Opportunities: {len(suitable)} features")

print("=== Step 13: Opportunity to CG distance ===")
opp_cent = suitable.copy()
opp_cent["geometry"] = opp_cent.geometry.centroid
opp_pts = np.array([(p.x, p.y) for p in opp_cent.geometry])
tree2 = cKDTree(cg_pts)
opp_dists, opp_idxs = tree2.query(opp_pts, k=1)
suitable["Distance"] = opp_dists
suitable["NearestCG_ID"] = [cg_cent["grass_id"].iloc[i] for i in opp_idxs]
suitable.to_file(OUT, layer="opp_with_distance", driver="GPKG")
print(f"  Distance range: {opp_dists.min():.0f} - {opp_dists.max():.0f} m")

print("=== Step 14: Remove roads ===")
road_buf_geom = roads_clip.geometry.buffer(10)
road_buf_union = unary_union(road_buf_geom)
opp_final = suitable.copy()
opp_final["geometry"] = opp_final.geometry.difference(road_buf_union)
opp_final = opp_final[opp_final.geometry.notna() & ~opp_final.geometry.is_empty].reset_index(drop=True)
opp_final["area_ha_final"] = opp_final.geometry.area / 10000.0
print(f"  After road removal: {len(opp_final)} features")

print("=== Step 15: Final score ===")
max_d = opp_final["Distance"].max() if len(opp_final) > 0 else 1
max_a = opp_final["area_ha_final"].max() if len(opp_final) > 0 else 1
if max_d <= 0: max_d = 1
if max_a <= 0: max_a = 1
opp_final["priority"] = 1 - (opp_final["Distance"] / max_d)
opp_final["final_score"] = (opp_final["priority"] * 0.5) + (opp_final["area_ha_final"] / max_a * 0.5)
opp_final.to_file(OUT, layer="AW_final_opportunities", driver="GPKG")
print(f"  Max Distance: {max_d:.0f} m, Max Area: {max_a:.2f} ha")
print(f"  Score range: {opp_final['final_score'].min():.3f} - {opp_final['final_score'].max():.3f}")

print(f"\n=== DONE ===")
print(f"All layers saved to: {OUT}")
print("Layers: AW_chilterns, CG_chilterns, PHI_chilterns, Roads_chilterns, AW_distance_to_CG, AW_250m_buffer, gap_phi, AW_connectivity_opportunities, AW_final_opportunities")
print("AW_final_opportunities has: priority, final_score, Distance, area_ha_final")
