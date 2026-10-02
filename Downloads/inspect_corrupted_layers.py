import geopandas as gpd

GPKG = r'c:\Users\User\Downloads\chilterns_results.gpkg'

layers_to_inspect = [
    'gap_raw', 'gap_phi', 'gap_heath_raw', 'gap_heath_phi',
    'gap_lm_raw', 'gap_lm_phi', 'AW_heath_opportunities',
    'AW_LM_opportunities', 'AW_connectivity_opportunities'
]

print("=== INSPECTING CORRUPTED / 1-ROW INTERMEDIATE LAYERS ===")
for name in layers_to_inspect:
    df = gpd.read_file(GPKG, layer=name)
    geom_types = df.geometry.type.tolist()
    areas = df.geometry.area.tolist()
    bounds = df.total_bounds
    print(f"\n[Layer: {name}]")
    print(f"  - Row count: {len(df)}")
    print(f"  - Geom Types: {geom_types}")
    print(f"  - Area (ha): {[round(a/10000.0, 4) for a in areas]}")
    print(f"  - Bounds: {bounds}")
    # inspect if multi-geometry or single small polygon
    if len(df) > 0:
        geom = df.geometry.iloc[0]
        if hasattr(geom, 'geoms'):
            print(f"  - Sub-geometries in MultiPolygon: {len(geom.geoms)}")
            sub_areas = [g.area/10000.0 for g in geom.geoms]
            print(f"    Sub-areas min={min(sub_areas):.4f}, max={max(sub_areas):.4f}, total={sum(sub_areas):.2f} ha")
        else:
            print(f"  - Single Polygon with {len(geom.exterior.coords) if hasattr(geom, 'exterior') else 0} vertices")
