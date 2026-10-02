# Read the slot mapping output
with open('_slot_final.md', 'r', encoding='utf-8') as f:
    slot_content = f.read()

# Read the original nm_body_particle_map.md
with open('nm_body_particle_map.md', 'r', encoding='utf-8') as f:
    original = f.read()

# Find the insertion point: after PART V last line, before PART VI
marker = '- **118. Og (INTJ_F_B)** → RELEASE:post-rock, STRESS_GROWTH:electronic experimental, EXTREME_GROWTH:dark ambient'
parts = original.split(marker)

if len(parts) == 2:
    # Insert slot mapping between PART V and PART VI
    new_content = parts[0] + marker + '\n\n' + slot_content + '\n\n' + parts[1]
    with open('nm_body_particle_map.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Success: inserted {len(slot_content)} chars into nm_body_particle_map.md')
else:
    print(f'ERROR: marker found {len(parts)-1} times')
