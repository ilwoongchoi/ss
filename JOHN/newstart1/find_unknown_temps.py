#!/usr/bin/env python3
"""Find ALL temp files modified around April 14-15, 2026 - looking for unsaved Excel data"""
import os
from datetime import datetime
from pathlib import Path

def search_all_temp_locations():
    user_profile = os.environ.get('USERPROFILE')
    
    # All temp locations
    search_paths = [
        os.path.join(user_profile, 'AppData', 'Local', 'Temp'),
        os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCache'),
        os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Office'),
        'C:\\Windows\\Temp',
    ]
    
    # Time range: April 13-15, 2026
    target_files = []
    
    print("Searching for files modified April 13-15, 2026...")
    print("-" * 80)
    
    for base_path in search_paths:
        if not os.path.exists(base_path):
            continue
            
        print(f"Checking: {base_path}")
        
        try:
            for root, dirs, files in os.walk(base_path):
                # Skip certain large/irrelevant dirs
                dirs[:] = [d for d in dirs if d not in ['WindowsApps', 'Packages', 'cache']]
                
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        stat = os.stat(file_path)
                        mtime = datetime.fromtimestamp(stat.st_mtime)
                        
                        # Filter: April 13-15, 2026
                        if mtime.year == 2026 and mtime.month == 4 and 13 <= mtime.day <= 15:
                            # Skip known AutoRecover patterns we already checked
                            if file.startswith('~ar') and (file.endswith('.xar') or file.endswith('.xlsb')):
                                continue
                            
                            # Look for potential Excel temps:
                            # - Files with no extension
                            # - .tmp files
                            # - Files starting with ~
                            # - Large files (>5KB) that might contain data
                            
                            size = stat.st_size
                            _, ext = os.path.splitext(file)
                            
                            is_candidate = (
                                ext in ['', '.tmp', '.TMP'] or
                                file.startswith('~') or
                                (size > 5000 and ext not in ['.dll', '.exe', '.log', '.etl'])
                            )
                            
                            if is_candidate:
                                target_files.append({
                                    'path': file_path,
                                    'name': file,
                                    'size': size,
                                    'mtime': mtime
                                })
                    except:
                        continue
        except Exception as e:
            print(f"  Error: {e}")
    
    # Sort by modification time
    target_files.sort(key=lambda x: x['mtime'], reverse=True)
    
    print(f"\n{'Time':<20} | {'Size (KB)':<10} | {'File'}")
    print("-" * 100)
    
    for f in target_files[:100]:  # Show top 100
        print(f"{f['mtime'].strftime('%Y-%m-%d %H:%M:%S'):<20} | {f['size']/1024:<10.1f} | {f['path']}")
    
    print(f"\nTotal candidates: {len(target_files)}")
    
    # Save to file for inspection
    output_file = r"d:\Users\user\Documents\newstart\temp_file_candidates.txt"
    with open(output_file, 'w', encoding='utf-8') as out:
        for f in target_files:
            out.write(f"{f['mtime']} | {f['size']} | {f['path']}\n")
    print(f"\nFull list saved to: {output_file}")

if __name__ == "__main__":
    search_all_temp_locations()
