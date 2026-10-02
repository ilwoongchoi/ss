import sys
sys.path.insert(0, r'c:\Users\User\Downloads')
import particle_to_8d as p

# 1. Check 128 elements
print(f"=== 128 ELEMENTS ===")
print(f"Element list count: {len(p.ELEMENTS_118)}")
print(f"Last 5 elements:")
for e in p.ELEMENTS_118[-5:]:
    print(f"  {e[0]}: {e[1]} = {e[2]}_{e[3]} genre={e[4]}")
print(f"E128 = {p.ELEMENTS_118[-1]}")

# 2. Check E119-E127 nodes
print(f"\n=== E119-E127 RECEPTOR NODES ===")
print(f"Count: {len(p.E119_E127_NODES)}")
for eid, einfo in p.E119_E127_NODES.items():
    print(f"  {eid}: {einfo['name']} receptor={einfo['receptor']} dim_effect={einfo.get('dim_effect', {})}")

# 3. Check 128 profiles
print(f"\n=== 128 PROFILES ===")
print(f"MBTI types: {len(p.MBTI_TYPES)}")
print(f"Genders: {p.GENDERS}")
print(f"Blood types: {p.BLOOD_TYPES}")
print(f"Total profiles: {len(p.MBTI_TYPES) * len(p.GENDERS) * len(p.BLOOD_TYPES)}")

# 4. Check Solenoid
print(f"\n=== SOLENOID ===")
print(f"Found in EM_BYPASS_ROUTE circuit_nodes: Solenoid_3/32")

# 5. Check 41 particles
print(f"\n=== 41 PARTICLES ===")
print(f"Particle coupling count: {len(p.PARTICLE_DIM_COUPLING)}")
print(f"Route particles: {len(p.ROUTE_PARTICLES_41)}")

# 6. Check heliosphere 7 layers (E128 = observer)
print(f"\n=== HELIOSPHERE 7 LAYERS ===")
for k, v in p.HELIOSPHERE_7_LAYERS.items():
    print(f"  {k}: {v['name']} particle={v['particle']}")

# 7. Run all 128 profiles and check if equation solves
print(f"\n=== EQUATION SOLVE CHECK (all 128 profiles, day) ===")
solved = 0
failed = 0
for mbti in p.MBTI_TYPES:
    for gender in p.GENDERS:
        for blood in p.BLOOD_TYPES:
            prof = f"{mbti}_{gender}_{blood}"
            try:
                r = p.particles_to_dims(prof, 'day')
                eqd = r.get('equation_derived', {})
                after = eqd.get('equation_after', None)
                if after is not None and abs(after) < 1e-10:
                    solved += 1
                else:
                    failed += 1
                    print(f"  FAILED: {prof} after={after}")
            except Exception as e:
                failed += 1
                print(f"  ERROR: {prof} {e}")

print(f"\nSolved: {solved}/128, Failed: {failed}/128")

# 8. Check night too
print(f"\n=== EQUATION SOLVE CHECK (all 128 profiles, night) ===")
solved_n = 0
failed_n = 0
for mbti in p.MBTI_TYPES:
    for gender in p.GENDERS:
        for blood in p.BLOOD_TYPES:
            prof = f"{mbti}_{gender}_{blood}"
            try:
                r = p.particles_to_dims(prof, 'night')
                eqd = r.get('equation_derived', {})
                after = eqd.get('equation_after', None)
                if after is not None and abs(after) < 1e-10:
                    solved_n += 1
                else:
                    failed_n += 1
                    print(f"  FAILED: {prof} after={after}")
            except Exception as e:
                failed_n += 1
                print(f"  ERROR: {prof} {e}")

print(f"\nSolved: {solved_n}/128, Failed: {failed_n}/128")
