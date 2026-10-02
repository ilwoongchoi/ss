import os
import re
from datetime import datetime

def find_excel_errors(evtx_path):
    print(f"Analyzing {evtx_path}...")
    try:
        with open(evtx_path, 'rb') as f:
            content = f.read()
        
        # Excel.exe crash patterns and timestamps
        # .evtx uses specific binary structures, but we can search for strings and nearby data
        # Common Excel crash strings
        patterns = [b'EXCEL.EXE', b'Microsoft Excel', b'Application Error']
        results = []
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                start = max(0, match.start() - 500)
                end = min(len(content), match.end() + 500)
                chunk = content[start:end]
                
                # Try to find something that looks like a date or timestamp in the vicinity
                # (Heuristic: Look for years like 2024 or 2026 in binary/text)
                timestamp_match = re.search(b'202[4-6]', chunk)
                context = chunk.decode('ascii', errors='ignore')
                
                results.append({
                    'pattern': pattern.decode(),
                    'offset': match.start(),
                    'context': context[:200].strip()
                })
        
        if not results:
            print("No obvious Excel crash strings found in binary scan.")
            return

        print(f"Found {len(results)} potential crash indicators. Top hits:")
        for r in results[:10]:
            print(f"- Found {r['pattern']} at offset {r['offset']}")
            print(f"  Context: {r['context']}\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    evtx_file = r"d:\Users\user\Documents\newstart\1.evtx"
    find_excel_errors(evtx_file)
