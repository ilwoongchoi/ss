import os
import shutil
from pathlib import Path
from datetime import datetime

def recover_files():
    # Target directory for recovered files
    recovery_dir = r"d:\Users\user\Documents\newstart\RECOVERED_EXCEL"
    if not os.path.exists(recovery_dir):
        os.makedirs(recovery_dir)
    
    # Source directory (Excel Roaming)
    source_dir = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Excel')
    
    print(f"Scanning {source_dir}...")
    
    # Patterns to look for
    # Based on the previous scan, we have many ~ar*.xar and ~ar*.xlsb files from April 14th
    count = 0
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # Check for temp file patterns
            if file.startswith('~ar') and (file.endswith('.xar') or file.endswith('.xlsb')):
                src_path = os.path.join(root, file)
                
                # Get modification time
                mtime = datetime.fromtimestamp(os.path.getmtime(src_path))
                
                # Filter for April 14th (the day the user mentions)
                if mtime.year == 2026 and mtime.month == 4 and mtime.day == 14:
                    # Create a descriptive name for the recovered file
                    time_str = mtime.strftime("%Y%m%d_%H%M%S")
                    new_name = f"RECOVERED_{time_str}_{file}.xlsb"
                    dest_path = os.path.join(recovery_dir, new_name)
                    
                    try:
                        shutil.copy2(src_path, dest_path)
                        print(f"Recovered: {file} -> {new_name} ({os.path.getsize(src_path)} bytes)")
                        count += 1
                    except Exception as e:
                        print(f"Error copying {file}: {e}")

    print(f"\nTotal files recovered to {recovery_dir}: {count}")
    print("Instructions: Open Excel, then drag these .xlsb files into Excel to check their content.")

if __name__ == "__main__":
    recover_files()
