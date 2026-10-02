#!/usr/bin/env python3
"""Final recovery attempt - search ALL temp locations for ANY file modified during Excel crash window"""
import os
import shutil
from datetime import datetime
from pathlib import Path

# Target time: April 14-15, 2026 (when Excel was running and crashed)
# Focus on files that are NOT the known AutoRecover files we already checked

def search_all_locations():
    user = os.environ.get('USERPROFILE')
    
    # Comprehensive search paths
    paths = [
        os.path.join(user, 'AppData', 'Local', 'Temp'),
        os.path.join(user, 'AppData', 'Local', 'Microsoft', 'Office'),
        os.path.join(user, 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCache'),
        os.path.join(user, 'AppData', 'Roaming', 'Microsoft', 'Excel'),
        'C:\\Windows\\Temp',
    ]
    
    recovery_dir = r"d:\Users\user\Documents\newstart\FINAL_RECOVERY"
    os.makedirs(recovery_dir, exist_ok=True)
    
    print("Searching for Excel-related files from April 14-15...")
    print("=" * 80)
    
    candidates = []
    
    for base in paths:
        if not os.path.exists(base):
            continue
        
        try:
            for root, dirs, files in os.walk(base):
                # Skip massive dirs
                dirs[:] = [d for d in dirs if d not in ['WindowsApps', 'Packages', 'cache', 'CryptnetUrlCache']]
                
                for file in files:
                    try:
                        fpath = os.path.join(root, file)
                        stat = os.stat(fpath)
                        mtime = datetime.fromtimestamp(stat.st_mtime)
                        
                        # April 14-15, 2026
                        if mtime.year == 2026 and mtime.month == 4 and 14 <= mtime.day <= 15:
                            # Skip known patterns we already checked
                            if file.startswith('~ar') and file.endswith(('.xar', '.xlsb')):
                                continue
                            
                            # Look for potential Excel data files
                            size = stat.st_size
                            ext = os.path.splitext(file)[1].lower()
                            
                            # Criteria: files that could contain Excel data
                            is_candidate = (
                                # Temp files
                                ext in ['.tmp', '.temp', ''] or
                                # Excel formats
                                ext in ['.xlsx', '.xlsb', '.xls', '.xlsm'] or
                                # Database/cache files
                                ext in ['.db', '.db-wal', '.db-shm'] or
                                # Files starting with ~ or $
                                file.startswith(('~', '$')) or
                                # Large files (>5KB) that might have data
                                (size > 5000 and ext not in ['.dll', '.exe', '.sys', '.log', '.etl', '.js', '.css', '.htm', '.html', '.svg', '.png', '.jpg'])
                            )
                            
                            if is_candidate:
                                candidates.append({
                                    'path': fpath,
                                    'name': file,
                                    'size': size,
                                    'mtime': mtime,
                                    'ext': ext
                                })
                    except:
                        continue
        except:
            continue
    
    # Sort by modification time
    candidates.sort(key=lambda x: x['mtime'], reverse=True)
    
    print(f"\nFound {len(candidates)} candidate files\n")
    print(f"{'Time':<20} | {'Size (KB)':<10} | {'Ext':<8} | {'Path'}")
    print("-" * 120)
    
    for c in candidates[:100]:
        print(f"{c['mtime'].strftime('%Y-%m-%d %H:%M:%S'):<20} | {c['size']/1024:<10.1f} | {c['ext']:<8} | {c['path']}")
    
    # Copy potential Excel files to recovery folder
    print(f"\n\nCopying potential Excel files to {recovery_dir}...")
    copied = 0
    
    for c in candidates:
        # Focus on files that look like Excel data
        if c['ext'] in ['.xlsx', '.xlsb', '.xls', '.xlsm', '.tmp', '.db', '.db-wal', ''] or c['name'].startswith(('~', '$')):
            try:
                time_str = c['mtime'].strftime("%Y%m%d_%H%M%S")
                new_name = f"{time_str}_{c['name']}"
                dest = os.path.join(recovery_dir, new_name)
                shutil.copy2(c['path'], dest)
                print(f"Copied: {c['name']} -> {new_name}")
                copied += 1
            except Exception as e:
                print(f"Error copying {c['name']}: {e}")
    
    print(f"\n\nRecovery complete. Copied {copied} files to {recovery_dir}")
    print("\nNext steps:")
    print("1. Open Excel")
    print("2. Try opening files in FINAL_RECOVERY folder")
    print("3. For .tmp or files with no extension, try renaming to .xlsb and opening")

if __name__ == "__main__":
    search_all_locations()
