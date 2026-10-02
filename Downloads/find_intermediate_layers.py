import sqlite3

c = sqlite3.connect(r'c:\Users\User\Downloads\chilterns_results.gpkg')
cur = c.cursor()
tables = [r[0] for r in cur.execute("SELECT table_name FROM gpkg_contents").fetchall()]

print("=== Checking all raw/intermediate layers in chilterns_results.gpkg ===")
for t in tables:
    if 'gap' in t.lower() or 'phi' in t.lower() or 'opp' in t.lower():
        cnt = cur.execute(f"SELECT COUNT(*) FROM [{t}]").fetchone()[0]
        cols = [r[1] for r in cur.execute(f"PRAGMA table_info([{t}])").fetchall()]
        print(f"  - Table: {t:30s} | Rows: {cnt:5d} | Columns: {cols[:6]}")
c.close()
