import re
from collections import Counter

with open(r'c:\Users\User\Downloads\circuitfile.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all particle= values
pattern = r'particle=(\S+?)(?:\s*\||\s*$)'
particles = re.findall(pattern, content, re.MULTILINE)
particles = [p.strip().lower().replace(' ', '_') for p in particles]
counts = Counter(particles)

print('=== ALL particle= values in circuitfile.md ===')
for p, c in sorted(counts.items(), key=lambda x: -x[1]):
    print(f'  {p}: {c}')

print(f'\nTotal unique particle names: {len(counts)}')

# 36 target particles
target_36 = [
    'proton', 'gluon', 'muon', 'electron', 'higgs', 'w_boson', 'z_boson',
    'neutrino', 'tau', 'photon', 'em', 'electromagnetism',
    'up_quark', 'down_quark', 'charm_quark', 'strange_quark',
    'top_quark', 'bottom_quark', 'tau_neutrino', 'electron_antineutrino',
    'muon_neutrino', 'muon_antineutrino', 'tau_antineutrino',
    'neutron', 'neutron_star', 'dark_matter', 'dark_energy',
    'female_gaba', 'energy', 'clathrate_buffer', 'malate_dehydrogenase',
    'ego_d2', 'progesterone', 'testosterone', 'acetyl_coa',
    'graviton', 'axion'
]

# Aliases
alias = {
    'electromagnetic_wave': 'em',
    'electron_neutrino': 'neutrino',
}

print('\n=== 36 TARGET PARTICLES CHECK ===')
missing = []
for t in target_36:
    found = t in counts
    if not found:
        for orig, norm in alias.items():
            if norm == t and orig in counts:
                found = True
                break
    status = 'FOUND' if found else 'MISSING'
    cnt = counts.get(t, 0)
    print(f'  {t}: {status} ({cnt})')
    if not found:
        missing.append(t)

print(f'\nMISSING: {missing if missing else "NONE"}')
