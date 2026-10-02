import csv

with open(r'c:\Users\User\Downloads\creative_4shapes_v3.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        if i < 3:
            print(f"Row {i}: profile={row.get('profile','')}")
            print(f"  shape1_music={row.get('shape1_music','')[:60]}")
            print(f"  shape1_tech={row.get('shape1_tech','')[:60]}")
            print(f"  shape1_sport={row.get('shape1_sport','')[:60]}")
            print(f"  shape2_music={row.get('shape2_music','')[:60]}")
            print(f"  shape2_tech={row.get('shape2_tech','')[:60]}")
            print(f"  shape2_sport={row.get('shape2_sport','')[:60]}")
            print(f"  shape3_tech={row.get('shape3_tech','')[:60]}")
            print(f"  shape3_sport={row.get('shape3_sport','')[:60]}")
            print(f"  shape4_music={row.get('shape4_music','')[:60]}")
            print(f"  All keys: {list(row.keys())[:10]}")
            print()
