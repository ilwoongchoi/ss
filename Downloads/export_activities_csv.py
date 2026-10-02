import sys, csv
sys.path.insert(0, r'c:\Users\User\Downloads')
from universe_math_structures import derive_activity

ALL_MBTI = [
    'ESTJ','ESTP','ESFJ','ESFP',
    'ENTJ','ENTP','ENFJ','ENFP',
    'ISTJ','ISTP','ISFJ','ISFP',
    'INTJ','INTP','INFJ','INFP',
]
ALL_GENDERS = ['M','F']
ALL_BLOOD = ['AB','A','O','B']

rows = []
for blood in ALL_BLOOD:
    for gender in ALL_GENDERS:
        for mbti in ALL_MBTI:
            profile = f'{mbti}_{gender}_{blood}'
            for t in range(16):
                act = derive_activity(mbti, gender, blood, t)
                rows.append([
                    profile, mbti, gender, blood, t,
                    act.get('Music',''),
                    act.get('Solo',''),
                    act.get('Creative',''),
                    act.get('Tech',''),
                    act.get('Sport',''),
                    act.get('Game',''),
                ])

outpath = r'c:\Users\User\Downloads\all_activities_128x16x6.csv'
with open(outpath, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['Profile','MBTI','Gender','Blood','TimeWindow','Music','Solo','Creative','Tech','Sport','Game'])
    w.writerows(rows)

print(f'Done: {len(rows)} rows -> {outpath}')
print(f'Unique Music: {len(set(r[5] for r in rows))}')
print(f'Unique Solo: {len(set(r[6] for r in rows))}')
print(f'Unique Creative: {len(set(r[7] for r in rows))}')
print(f'Unique Tech: {len(set(r[8] for r in rows))}')
print(f'Unique Sport: {len(set(r[9] for r in rows))}')
print(f'Unique Game: {len(set(r[10] for r in rows))}')
total_unique = len(set(tuple(r[5:]) for r in rows))
print(f'Unique 6-tuples: {total_unique} / {len(rows)}')
