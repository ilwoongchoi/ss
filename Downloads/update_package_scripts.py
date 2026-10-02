import os, shutil

PACKAGE_DIR = r"D:\새 폴더\BNG_Ecosystem_Connectivity_Portfolio"
SCRIPTS_DIR = os.path.join(PACKAGE_DIR, "Scripts")
os.makedirs(SCRIPTS_DIR, exist_ok=True)

# Clean out scripts folder first
for f in os.listdir(SCRIPTS_DIR):
    os.remove(os.path.join(SCRIPTS_DIR, f))

# Copy Production Scripts with clear numbering
scripts_to_copy = [
    (r"D:\새 폴더\chilterns_analysis.py", "01_chilterns_bng_analysis.py"),
    (r"D:\새 폴더\run_all_national_parks.py", "02_national_parks_full_pipeline_mcda.py"),
    (r"D:\새 폴더\ukhab_palette.py", "03_ukhab_standard_palette_definitions.py"),
    (r"D:\새 폴더\generate_all_national_park_layouts_standalone.py", "04_national_parks_layout_automation.py"),
    (r"C:\Users\User\Downloads\isolate_all_legends_xml.py", "05_batch_legend_isolation_engine.py")
]

print("=== Copying Core Scripts to Package ===")
for src, dst_name in scripts_to_copy:
    if os.path.exists(src):
        dst = os.path.join(SCRIPTS_DIR, dst_name)
        shutil.copy2(src, dst)
        print(f"  + Added: {dst_name}")
    else:
        print(f"  - Missing: {src}")

# Also update project file in package with isolated legends & Dartmoor
shutil.copy2(r"C:\Users\User\Downloads\Chilterns Connectivity.qgz", os.path.join(PACKAGE_DIR, "Ecosystem_Connectivity_National_Parks.qgz"))
print("  + Synced latest QGIS project with 11 isolated layouts")

# Re-zip
zip_path = r"D:\새 폴더\BNG_Ecosystem_Connectivity_Portfolio_OxygenConservation.zip"
if os.path.exists(zip_path):
    os.remove(zip_path)
