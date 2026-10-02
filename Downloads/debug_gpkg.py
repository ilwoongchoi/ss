import sqlite3
conn = sqlite3.connect(r'c:\Users\User\Downloads\chilterns_results.gpkg')
cur = conn.cursor()

# Check key intermediate layers
layers = [
    'AW_250m_buffer',
    'gap_raw',
    'gap_phi',
    'AW_connectivity_opportunities',
    'opp_centroids',
    'opp_with_distance',
    'road_10m_buffer',
    'AW_final_opportunities',
    'gap_heath_raw',
    'gap_heath_phi',
    'AW_heath_opportunities',
    'heath_opp_with_distance',
    'AW_final_opportunities_heath',
    'gap_lm_raw',
    'gap_lm_phi',
    'AW_LM_opportunities',
    'lm_opp_with_distance',
    'AW_final_opportunities_meadows',
]

for t in layers:
    cur.execute(f'SELECT COUNT(*) FROM "{t}"')
    cnt = cur.fetchone()[0]
    # Get geometry type
    cur.execute("SELECT geometry_type_name FROM gpkg_contents WHERE table_name=?", (t,))
    gtype = cur.fetchone()
    gtype = gtype[0] if gtype else '?'
    # Check total area if polygon
    if cnt > 0:
        cur.execute(f'SELECT TotalArea = SUM(ST_Area(geom)) FROM "{t}"' if False else f'SELECT COUNT(*) FROM "{t}" WHERE geom IS NOT NULL')
        non_null = cur.fetchone()[0]
        print(f"{t}: {cnt} features, geom_type={gtype}, non_null_geom={non_null}")
    else:
        print(f"{t}: {cnt} features, geom_type={gtype}")

print("\n--- Checking road_10m_buffer source ---")
# Check if road layer exists
cur.execute("SELECT table_name FROM gpkg_contents WHERE table_name LIKE '%road%'")
print("Road layers:", [r[0] for r in cur.fetchall()])

# Check opp_with_distance fields
print("\n--- opp_with_distance columns ---")
cur.execute('PRAGMA table_info(opp_with_distance)')
cols = cur.fetchall()
for c in cols:
    print(f"  {c[1]} ({c[2]})")

# Check AW_connectivity_opportunities fields
print("\n--- AW_connectivity_opportunities columns ---")
cur.execute('PRAGMA table_info(AW_connectivity_opportunities)')
cols = cur.fetchall()
for c in cols:
    print(f"  {c[1]} ({c[2]})")

# Check gap_phi columns
print("\n--- gap_phi columns ---")
cur.execute('PRAGMA table_info(gap_phi)')
cols = cur.fetchall()
for c in cols:
    print(f"  {c[1]} ({c[2]})")

conn.close()
