
import sys
import os

sys.path.append(os.getcwd())

try:
    import geometry_package.absolute_constants as ac
    print("Successfully imported geometry_package.absolute_constants")
    print(f"File: {ac.__file__}")
    
    expected = ["GATE_5_32", "UNIT_64", "RESID_DATA_5_32"]
    for attr in expected:
        if hasattr(ac, attr):
            print(f"Has {attr}: {getattr(ac, attr)}")
        else:
            print(f"MISSING {attr}")
            
except Exception as e:
    print(f"Import failed: {e}")
