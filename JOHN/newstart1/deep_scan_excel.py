import os
from datetime import datetime, timedelta

def find_recent_files():
    # Define search paths
    user_profile = os.environ.get('USERPROFILE')
    search_paths = [
        os.path.join(user_profile, 'AppData', 'Local', 'Temp'),
        os.path.join(user_profile, 'AppData', 'Roaming', 'Microsoft', 'Excel'),
        os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Office', 'UnsavedFiles')
    ]
    
    # Time window: last 48 hours
    time_threshold = datetime.now() - timedelta(days=2)
    
    print(f"Searching for files modified after: {time_threshold}")
    print("-" * 60)
    
    found_files = []
    
    for path in search_paths:
        if not os.path.exists(path):
            continue
            
        print(f"Checking: {path}")
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if mtime > time_threshold:
                            size = os.path.getsize(file_path)
                            # Look for potential Excel temp files
                            # Patterns: ~ar*.xar, *.xlsb, ~df*.tmp, or any large tmp files
                            is_excel_related = any([
                                file.lower().endswith(('.xar', '.xlsb', '.tmp')),
                                file.startswith('~')
                            ])
                            
                            found_files.append({
                                'path': file_path,
                                'mtime': mtime,
                                'size': size,
                                'excel_like': is_excel_related
                            })
                    except Exception:
                        continue
        except Exception as e:
            print(f"Error accessing {path}: {e}")

    # Sort by modification time descending
    found_files.sort(key=lambda x: x['mtime'], reverse=True)
    
    if not found_files:
        print("No recent files found in temp locations.")
    else:
        print(f"{'Last Modified':<20} | {'Size (KB)':<10} | {'Path'}")
        print("-" * 100)
        for f in found_files:
            # Highlight likely Excel files
            prefix = "[!]" if f['excel_like'] else "   "
            print(f"{prefix} {f['mtime'].strftime('%Y-%m-%d %H:%M:%S'):<20} | {f['size']/1024:<10.2f} | {f['path']}")

if __name__ == "__main__":
    find_recent_files()
