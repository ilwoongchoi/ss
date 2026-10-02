import os, glob

# Check all python files used across today's run
scripts = glob.glob(r"C:\Users\User\Downloads\*.py") + glob.glob(r"D:\새 폴더\*.py")

print("=== CHECKING HOW INTERMEDIATE DATA WAS HANDLED IN SCRIPTS ===")
for s in scripts:
    with open(s, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        if "national_parks_results.gpkg" in content or "run_all" in s or "chilterns" in s:
            print(f"\nScript: {os.path.basename(s)}")
            # check if to_file was called on intermediates or memory
            lines = [line.strip() for line in content.split('\n') if 'to_file' in line or 'OUT' in line]
            for l in lines[:5]:
                print(f"  {l}")
