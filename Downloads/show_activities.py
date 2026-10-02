import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
from universe_math_structures import derive_activity

profiles = [
    ('ENTP','M','O'),
    ('INFJ','F','A'),
    ('ESTJ','M','B'),
    ('ISFP','F','AB'),
]

for mbti, gender, blood in profiles:
    key = f'{mbti}_{gender}_{blood}'
    print(f'=== {key} ===')
    for t in range(16):
        act = derive_activity(mbti, gender, blood, t)
        print(f'  [t={t:2d}]')
        print(f'    Music   : {act["Music"]}')
        print(f'    Solo    : {act["Solo"]}')
        print(f'    Creative: {act["Creative"]}')
        print(f'    Tech    : {act["Tech"]}')
        print(f'    Sport   : {act["Sport"]}')
        print(f'    Game    : {act["Game"]}')
    print()
