import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
from universe_math_structures import compute_8d, mandelbrot_seed, DIMS

MBTI_TYPES = [
    'ESTJ','ESTP','ESFJ','ESFP',
    'ENTJ','ENTP','ENFJ','ENFP',
    'ISTJ','ISTP','ISFJ','ISFP',
    'INTJ','INTP','INFJ','INFP',
]
GENDERS = ['M','F']
BLOOD_TYPES = ['AB','A','O','B']

NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

def note_name(midi_num):
    octave = (midi_num // 12) - 1
    name = NOTE_NAMES[midi_num % 12]
    return f'{name}{octave}'

# Generate all 128 profiles
profiles = []
for blood in BLOOD_TYPES:
    for gender in GENDERS:
        for mbti in MBTI_TYPES:
            v = compute_8d(mbti, gender, blood)
            h = mandelbrot_seed(mbti, gender, blood)
            profiles.append({
                'mbti': mbti, 'gender': gender, 'blood': blood,
                'v8d': v, 'h': h
            })

# Check distinct values per dim
dim_values = {d: set() for d in DIMS}
for p in profiles:
    for d in DIMS:
        dim_values[d].add(round(p['v8d'][d], 4))

print("Distinct values per dim:")
for d in DIMS:
    vals = sorted(dim_values[d])
    print(f"  {d}: {len(vals)} values: {vals}")

# Total unique 8D vectors
unique_8d = len(set(tuple(round(p['v8d'][d], 4) for d in DIMS) for p in profiles))
print(f"\nUnique 8D vectors: {unique_8d} / 128")

# Mixed-radix encoding: each dim is a digit
dim_sorted = {}
for d in DIMS:
    dim_sorted[d] = sorted(dim_values[d])

for p in profiles:
    index = 0
    multiplier = 1
    for d in reversed(DIMS):
        rank = dim_sorted[d].index(round(p['v8d'][d], 4))
        index += rank * multiplier
        multiplier *= len(dim_sorted[d])
    p['unique_index'] = index

indices = [p['unique_index'] for p in profiles]
unique_indices = len(set(indices))
print(f"Unique mixed-radix indices: {unique_indices} / 128")

# Sort by unique_index, then h(t) as tiebreaker
profiles.sort(key=lambda p: (p['unique_index'], p['h']))
for i, p in enumerate(profiles):
    p['midi'] = i

# Print results
print(f"\n{'MBTI':<6} {'Sex':<4} {'Blood':<5} {'MIDI':<5} {'Note':<6} {'h(t)':>7} {'s':>5} {'d':>5} {'gamma':>5} {'h':>5} {'r':>5} {'p':>5} {'g':>5} {'nu':>5}")
print('-' * 95)
for p in profiles:
    v = p['v8d']
    midi = p['midi']
    print(f"{p['mbti']:<6} {p['gender']:<4} {p['blood']:<5} {midi:<5} {note_name(midi):<6} {p['h']:7.4f} {v['s']:5.2f} {v['d']:5.2f} {v['gamma']:5.2f} {v['h']:5.2f} {v['r']:5.2f} {v['p']:5.2f} {v['g']:5.2f} {v['nu']:5.2f}")

midi_vals = [p['midi'] for p in profiles]
print(f"\nUnique MIDI notes: {len(set(midi_vals))} / 128")
print(f"MIDI range: {min(midi_vals)} ({note_name(min(midi_vals))}) to {max(midi_vals)} ({note_name(max(midi_vals))})")
