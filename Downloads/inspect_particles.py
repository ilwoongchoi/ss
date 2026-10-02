import csv, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\User\Downloads\128_UNIFIED_MASTER_8D_fixed.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print('Profiles with missing Particle (first 30):')
count = 0
for r in rows:
    p = r['Particle'].strip()
    if p == '-' or p == '':
        count += 1
        if count <= 30:
            t = r['Type']
            elem = r['Element']
            circ = r['Circuit_Entity']
            color = r['Color']
            print(f'  {t:15s}  Element={elem:12s}  Circuit={circ:30s}  Color={color}')
print(f'Total missing particle: {count}')
print()
print('Profiles WITH Particle:')
for r in rows:
    p = r['Particle'].strip()
    if p != '-' and p != '':
        t = r['Type']
        elem = r['Element']
        circ = r['Circuit_Entity']
        print(f'  {t:15s}  Particle={p:25s}  Element={elem:12s}  Circuit={circ}')
