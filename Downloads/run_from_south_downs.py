import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.ops import unary_union
from scipy.spatial import cKDTree
import zipfile, os, warnings, time

warnings.filterwarnings("ignore")

BASE = r"D:\새 폴더"
ROAD_ZIP = rf"{BASE}\oproad_essh_gb.zip"
ROAD_EXTRACT_DIR = rf"{BASE}\oproad_extracted"
OUT = rf"{BASE}\national_parks_results.gpkg"

# South Downs부터 시작 (3개 공원)
PARK_HABITAT_MAP = [
    ("SOUTH DOWNS", "Traditional_Orchards"),
    ("NORTHUMBERLAND", "Upland_Fens_Flushes_and_Swamps"),
    ("YORKSHIRE DALES", "Limestone_Pavement")
]

print("=== Loading National Parks Boundaries ===")
np_layer_path = rf"{BASE}\National_Parks_England.gpkg\National_Parks_England.gpkg"
parks_all = gpd.read_file(np_layer_path).to_crs("EPSG:27700")

aw_path = rf"{BASE}\Ancient_Woodland_England.gpkg (1)\Ancient_Woodland_England.gpkg"
hab_pkg = rf"{BASE}\Habitat_Networks_Individual_England.gpkg\Habitat_Networks_Individual_England.gpkg"
phi_path = rf"{BASE}\PHI_full.gpkg"

with zipfile.ZipFile(ROAD_ZIP, 'r') as z:
    all_road_tiles = sorted(list(set(x.split('/')[1].split('_')[0] for x in z.namelist() if '_RoadLink.shp' in x)))

summary_results = []

for park_name, target_hab in PARK_HABITAT_MAP:
    t0 = time.time()
    clean_park_slug = park_name.lower().replace(" ", "_")
    print(f"\n=======================================================")
    print(f"Processing: {park_name} -> Target Habitat: {target_hab}")
    print(f"=======================================================")

    park_poly = parks_all[parks_all['name'].str.upper() == park_name.upper()]
    if len(park_poly) == 0:
        print(f"  ERROR: Park {park_name} not found!")
        continue
    
    park_geom = unary_union(park_poly.geometry)
    minx, miny, maxx, maxy = park_geom.bounds
    bbox = (minx, miny, maxx, maxy)
    
    # 1. Clip AW within Park
    print(f"  [1/6] Loading & clipping Ancient Woodland...")
    try:
        aw_park = gpd.read_file(aw_path, bbox=bbox).to_crs("EPSG:27700")
        aw_park = gpd.clip(aw_park, park_poly).reset_index(drop=True)
        print(f"    AW count: {len(aw_park)}")
    except Exception as e:
        print(f"    AW load error: {e}")
        continue

    if len(aw_park) == 0:
        print(f"    WARNING: No AW in {park_name}. Skipping.")
        continue

    # 2. Load & Clip Target Habitat
    print(f"  [2/6] Loading & clipping Target Habitat: {target_hab}...")
    try:
        hab_park = gpd.read_file(hab_pkg, layer=target_hab, bbox=bbox).to_crs("EPSG:27700")
        hab_park = gpd.clip(hab_park, park_poly).reset_index(drop=True)
        print(f"    Target Habitat patches: {len(hab_park)}")
    except Exception as e:
        print(f"    Target Habitat error: {e}")
        continue

    if len(hab_park) == 0:
        print(f"    WARNING: No {target_hab} within {park_name}. Skipping.")
        continue

    # 3. Buffer AW (250m) & calculate Gap
    print(f"  [3/6] Computing 250m AW buffer and Gap difference...")
    aw_buf_geom = unary_union(aw_park.geometry).buffer(250)
    hab_union = unary_union(hab_park.geometry)
    gap_geom = aw_buf_geom.difference(hab_union)
    
    gap_gdf = gpd.GeoDataFrame(geometry=[gap_geom], crs="EPSG:27700").explode(index_parts=False).reset_index(drop=True)
    gap_gdf = gap_gdf[gap_gdf.geometry.type.isin(['Polygon', 'MultiPolygon']) & (~gap_gdf.geometry.is_empty)]

    # 4. Intersect with PHI
    print(f"  [4/6] Intersecting Gap with PHI...")
    try:
        phi_park = gpd.read_file(phi_path, bbox=bbox).to_crs("EPSG:27700")
        phi_park = gpd.clip(phi_park, park_poly).reset_index(drop=True)
        phi_park = phi_park[phi_park.geometry.area >= 500].reset_index(drop=True)
        
        gap_phi = gpd.overlay(gap_gdf, phi_park, how="intersection")
        gap_phi = gap_phi.explode(index_parts=False).reset_index(drop=True)
        gap_phi = gap_phi[gap_phi.geometry.type.isin(['Polygon', 'MultiPolygon'])].reset_index(drop=True)
        gap_phi["area_ha"] = gap_phi.geometry.area / 10000.0
        gap_phi = gap_phi[gap_phi["area_ha"] >= 0.05].reset_index(drop=True)
        print(f"    Viable raw patches: {len(gap_phi)}")
    except Exception as e:
        print(f"    PHI intersection error: {e}")
        continue

    if len(gap_phi) == 0:
        print("    No viable intersecting patches found.")
        continue

    # 5. Extract and Buffer intersecting Roads
    print(f"  [5/6] Extracting road links & applying road buffer difference...")
    road_dfs = []
    with zipfile.ZipFile(ROAD_ZIP, 'r') as z:
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
        gap_total_bounds = gap_phi.total_bounds
        roads_candidates = roads_all.cx[gap_total_bounds[0]:gap_total_bounds[2], gap_total_bounds[1]:gap_total_bounds[3]]
        
        roads_intersecting = gpd.sjoin(roads_candidates, gap_phi[['geometry']], how="inner", predicate="intersects")
        roads_intersecting = roads_intersecting.drop_duplicates(subset=["geometry"])
        print(f"    Relevant roads near patches: {len(roads_intersecting)} (filtered from {len(roads_all)})")
        
        if len(roads_intersecting) > 0:
            road_buf = unary_union(roads_intersecting.geometry.buffer(10))
            diff_geoms = [geom.difference(road_buf) for geom in gap_phi.geometry]
            gap_phi["geometry"] = diff_geoms
            gap_phi = gap_phi.explode(index_parts=False).reset_index(drop=True)
            gap_phi = gap_phi[gap_phi.geometry.type.isin(['Polygon', 'MultiPolygon']) & (~gap_phi.geometry.is_empty)].reset_index(drop=True)
            gap_phi["area_ha_final"] = gap_phi.geometry.area / 10000.0
            gap_phi = gap_phi[gap_phi["area_ha_final"] >= 0.05].reset_index(drop=True)
        else:
            gap_phi["area_ha_final"] = gap_phi["area_ha"]
    else:
        gap_phi["area_ha_final"] = gap_phi["area_ha"]

    # 6. Distance & Scoring
    print(f"  [6/6] Computing spatial distance & BNG score...")
    hab_pts = np.array([(p.x, p.y) for p in hab_park.geometry.centroid])
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
    gap_phi["target_hab"] = target_hab

    cols_keep = ['park_name', 'target_hab', 'Main_Habit', 'MainHabs', 'area_ha_final', 'Distance', 'proximity_score', 'area_score', 'final_score', 'geometry']
    cols_actual = [c for c in cols_keep if c in gap_phi.columns]
    res_layer = gap_phi[cols_actual].copy()

    layer_name = f"opp_{clean_park_slug}"
    res_layer.to_file(OUT, layer=layer_name, driver="GPKG")
    elapsed = time.time() - t0
    print(f"  >>> SUCCESS: Saved '{layer_name}' with {len(res_layer)} patches in {elapsed:.1f}s")
    summary_results.append((park_name, target_hab, len(res_layer), res_layer['final_score'].mean()))

print("\n=======================================================")
print("SOUTH DOWNS TO YORKSHIRE DALES COMPLETED")
print("=======================================================")
for p, h, cnt, sc in summary_results:
    print(f"{p:20s} | {h:35s} | Patches: {cnt:5d} | Avg Score: {sc:.3f}")
