import sqlite3

c = sqlite3.connect(r'c:\Users\User\Downloads\chilterns_results.gpkg')
cur = c.cursor()
for name in ['AW_final_opportunities', 'AW_final_opportunities_heath', 'AW_final_opportunities_meadows', 'gap_phi', 'gap_phi_clean']:
    cols = [r[1] for r in cur.execute(f"PRAGMA table_info([{name}])").fetchall()]
    cnt = cur.execute(f"SELECT COUNT(*) FROM [{name}]").fetchone()[0]
    print(f"{name:32s}: count={cnt:5d} | cols={cols}")
c.close()
