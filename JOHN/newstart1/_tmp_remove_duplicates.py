import os
import hashlib
from collections import defaultdict

def get_file_hash(file_path):
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except:
        return None

def main():
    print("Scanning for duplicates...")
    hashes = defaultdict(list)
    count = 0
    for root, dirs, files in os.walk('.'):
        # Skip git and gemini internal folders
        if '.git' in root or '.gemini' in root:
            continue
        for file in files:
            # Skip the script itself
            if file == '_tmp_remove_duplicates.py':
                continue
            full_path = os.path.abspath(os.path.join(root, file))
            file_hash = get_file_hash(full_path)
            if file_hash:
                hashes[file_hash].append(full_path)
                count += 1
    
    print(f"Scanned {count} files.")
    deleted_count = 0
    for file_hash, paths in hashes.items():
        if len(paths) >= 2:
            paths.sort(key=len) # Keep the one with the shortest path/name
            original = paths[0]
            duplicates = paths[1:]
            for dup in duplicates:
                try:
                    os.remove(dup)
                    print(f"Deleted: {dup}")
                    deleted_count += 1
                except Exception as e:
                    print(f"Failed to delete {dup}: {e}")
    
    print(f"\nCleanup complete. Total duplicates removed: {deleted_count}")

if __name__ == "__main__":
    main()
