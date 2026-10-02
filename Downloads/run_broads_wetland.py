import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.ops import unary_union
from scipy.spatial import cKDTree
from shapely.validation import make_valid
import zipfile, os, warnings, time

warnings.filterwarnings("ignore")

BASE = r"D:\새 폴더"
ROAD_ZIP = rf"{BASE}\oproad_essh_gb.zip"
ROAD_EXTRACT_DIR = rf"{BASE}\oproad_extracted"
OUT = rf"{BASE}\national_parks_results.gpkg"

park_name = "THE BROADS"
print(f"=== Processing Wetland Core Connectivity: {park_name} ===")

np_layer_path = rf"{BASE}\National_Parks_England.gpkg\National_Parks_England.gpkg"
parks_all = gpd.read_file(np_layer_path).to_crs("EPSG:27700")
hab_pkg = rf"{BASE}\Habitat_Networks_Individual_England.gpkg\Habitat_Networks_Individual_England.gpkg"
phi_path = rf"{BASE}\PHI_full.gpkg"

park_poly = parks_all[parks_all['name'].str.upper() == park_name.upper()].copy()
park_poly['geometry'] = park_poly['geometry'].make_valid()
bbox = tuple(park_poly.total_bounds)

# 1. Core Anchor: Lowland_Fen (3,329 patches)
print("1. Loading Anchor: Lowland_Fen...")
fen = gpd.read_file(hab_pkg, layer="Lowland_Fen", bbox=bbox).to_crs("EPSG:27700")
fen['geometry'] = fen['geometry'].make_valid()
fen_park = gpd.clip(fen, park_poly).reset_index(drop=True)
print(f"  Fen anchor patches: {len(fen_park)}")

# 2. Target Habitat: Reedbeds (4,725 patches)
print("2. Loading Target: Reedbeds...")
reed = gpd.read_file(hab_pkg, layer="Reedbeds", bbox=bbox).to_crs("EPSG:27700")
reed['geometry'] = reed['geometry'].make_valid()
reed_park = gpd.clip(reed, park_poly).reset_index(drop=True)
print(f"  Reedbeds target patches: {len(reed_park)}")

# 3. Buffer Fen (200m) & calculate Gap
print("3. Buffer Fen (200m) & Gap...")
fen_buf = unary_union(fen_park.geometry.buffer(200))
reed_union = unary_union(reed_park.geometry)
gap_geom = fen_buf.difference(reed_union)

gap_gdf = gpd.GeoDataFrame(geometry=[gap_geom], crs="EPSG:27700").explode(index_parts=False).reset_index(drop=True)
gap_gdf['geometry'] = gap_gdf['geometry'].make_valid()
gap_gdf = gap_gdf[gap_gdf.geometry.type.isin(['Polygon', 'MultiPolygon']) & (~gap_gdf.geometry.is_empty)]

# 4. Intersect with PHI
print("4. PHI clip...")
phi_park = gpd.read_file(phi_path, bbox=bbox).to_crs("EPSG:27700")
phi_park['geometry'] = phi_park['geometry'].make_valid()
phi_park = gpd.clip(phi_park, park_poly).reset_index(drop=True)
phi_park = phi_park[phi_park.geometry.area >= 200].reset_index(drop=True)

gap_phi = gpd.overlay(gap_gdf, phi_park, how="intersection")
gap_phi = gap_phi.explode(index_parts=False).reset_index(drop=True)
gap_phi['geometry'] = gap_phi['geometry'].make_valid()
gap_phi = gap_phi[gap_phi.geometry.type.isin(['Polygon', 'MultiPolygon'])].reset_index(drop=True)
gap_phi["area_ha"] = gap_phi.geometry.area / 10000.0
gap_phi = gap_phi[gap_phi["area_ha"] >= 0.05].reset_index(drop=True)
print(f"  Viable patches: {len(gap_phi)}")

# 5. Roads
print("5. Roads...")
with zipfile.ZipFile(ROAD_ZIP, 'r') as z:
    all_road_tiles = sorted(list(set(x.split('/')[1].split('_')[0] for x in z.namelist() if '_RoadLink.shp' in x)))
    road_dfs = []
    for t in all_road_tiles:
        shp_name = f"data/{t}_RoadLink.shp"
        if shp_name in z.namelist():
            for ext in ['.shp', '.shx', '.dbf', '.prj']:
                fname = f"data/{t}_RoadLink{ext}"
                if fname in z.namelist():
                    z.extract(fname, ROAD_EXTRACT_DIR)
            extracted_shp = os.path.join(ROAD_EXTRACT_DIR, "data", f"{t}_RoadLink.shp")
            try:
                r_df = gpd.read_file(extracted_shp, bbox=bbox)
                if len(r_df) > 0:
                    road_dfs.append(r_df.to_crs("EPSG:27700"))
            except:
                pass

if len(road_dfs) > 0:
    roads_all = gpd.GeoDataFrame(pd.concat(road_dfs, ignore_index=True), crs="EPSG:27700")
    roads_all['geometry'] = roads_all['geometry'].make_valid()
    gap_total_bounds = gap_phi.total_bounds
    roads_candidates = roads_all.cx[gap_total_bounds[0]:gap_total_bounds[2], gap_total_bounds[1]:gap_total_bounds[3]]
    roads_intersecting = gpd.sjoin(roads_candidates, gap_phi[['geometry']], how="inner", predicate="intersects")
    roads_intersecting = roads_intersecting.drop_duplicates(subset=["geometry"])
    print(f"  Roads near patches: {len(roads_intersecting)}")
    if len(roads_intersecting) > 0:
        road_buf = unary_union(roads_intersecting.geometry.buffer(10))
        diff_geoms = [geom.difference(road_buf) for geom in gap_phi.geometry]
        gap_phi["geometry"] = diff_geoms
        gap_phi = gap_phi.explode(index_parts=False).reset_index(drop=True)
        gap_phi['geometry'] = gap_phi['geometry'].make_valid()
        gap_phi = gap_phi[gap_phi.geometry.type.isin(['Polygon', 'MultiPolygon']) & (~gap_phi.geometry.is_empty)].reset_index(drop=True)
        gap_phi["area_ha_final"] = gap_phi.geometry.area / 10000.0
        gap_phi = gap_phi[gap_phi["area_ha_final"] >= 0.05].reset_index(drop=True)
    else:
        gap_phi["area_ha_final"] = gap_phi["area_ha"]
else:
    gap_phi["area_ha_final"] = gap_phi["area_ha"]

# 6. Scoring
print("6. Distance & Score...")
hab_pts = np.array([(p.x, p.y) for p in reed_park.geometry.centroid])
tree_hab = cKDTree(hab_pts)
opp_pts = np.array([(p.x, p.y) for p in gap_phi.geometry.centroid])
dists, _ = tree_hab.query(opp_pts, k=1)

gap_phi["Distance"] = dists
max_d = gap_phi["Distance"].max() if len(gap_phi) > 0 else 1
max_a = gap_phi["area_ha_final"].max() if len(gap_phi) > 0 else 1
if max_d <= 0: max_d = 1
if max_a <= 0: max_a = 1

gap_phi["proximity_score"] = 1.0 - (gap_phi["Distance"] / max_d)
gap_phi["area_score"] = gap_phi["area_ha_final"] / max_a
gap_phi["final_score"] = (gap_phi["proximity_score"] * 0.5) + (gap_phi["area_score"] * 0.5)
gap_phi["park_name"] = park_name
gap_phi["target_hab"] = "Reedbeds"

cols_keep = ['park_name', 'target_hab', 'Main_Habit', 'MainHabs', 'area_ha_final', 'Distance', 'proximity_score', 'area_score', 'final_score', 'geometry']
cols_actual = [c for c in cols_keep if c in gap_phi.columns]
res_layer = gap_phi[cols_actual].copy()

layer_name = "opp_the_broads"
res_layer.to_file(OUT, layer=layer_name, driver="GPKG")
print(f">>> SUCCESS: Saved '{layer_name}' with {len(res_layer)} patches!")
