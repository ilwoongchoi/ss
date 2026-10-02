import geopandas as gpd

GPKG = r'c:\Users\User\Downloads\chilterns_results.gpkg'

# Load Base Layers from GPKG
print("Loading base inputs...")
aw_buf = gpd.read_file(GPKG, layer='AW_250m_buffer')
cg = gpd.read_file(GPKG, layer='CG_chilterns')
heath = gpd.read_file(GPKG, layer='Heathland_chilterns')
lm = gpd.read_file(GPKG, layer='Lowland_Meadows_chilterns')
phi = gpd.read_file(GPKG, layer='PHI_chilterns')

# Ensure single dissolved polygon for gap difference
aw_buf_geom = aw_buf.geometry.unary_union

def create_phi_overlay(target_hab_gdf, out_layer_name):
    print(f"\nProcessing Overlay for: {out_layer_name}...")
    hab_union = target_hab_gdf.geometry.unary_union
    # 1. Gap (AW 250m Buffer - Target Habitat)
    gap_geom = aw_buf_geom.difference(hab_union)
    gap_gdf = gpd.GeoDataFrame(geometry=[gap_geom], crs="EPSG:27700").explode(index_parts=False).reset_index(drop=True)
    gap_gdf = gap_gdf[gap_gdf.geometry.type.isin(['Polygon', 'MultiPolygon']) & (~gap_gdf.geometry.is_empty)]
    
    # 2. Intersect with PHI (The exact step asked by user)
    gap_phi = gpd.overlay(gap_gdf, phi, how="intersection")
    gap_phi = gap_phi.explode(index_parts=False).reset_index(drop=True)
    gap_phi = gap_phi[gap_phi.geometry.type.isin(['Polygon', 'MultiPolygon']) & (~gap_phi.geometry.is_empty)].reset_index(drop=True)
    gap_phi["area_ha"] = gap_phi.geometry.area / 10000.0
    gap_phi = gap_phi[gap_phi["area_ha"] >= 0.05].reset_index(drop=True)
    
    print(f"  -> Generated {len(gap_phi)} individual exploded patches with PHI attributes!")
    gap_phi.to_file(GPKG, layer=out_layer_name, driver="GPKG")
    print(f"  -> Saved to GPKG layer: '{out_layer_name}'")

# Generate all 3 exploded raw PHI overlay layers
create_phi_overlay(cg, "phi_overlay_calcareous_grassland")
create_phi_overlay(heath, "phi_overlay_heathland")
create_phi_overlay(lm, "phi_overlay_lowland_meadows")

print("\n>>> ALL 3 RAW PHI OVERLAY INTERMEDIATE LAYERS GENERATED SUCCESSFULLY!")
