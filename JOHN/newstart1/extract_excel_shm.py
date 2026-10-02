#!/usr/bin/env python3
"""Extract data from Excel db-shm file"""
import os
import struct

shm_path = r"d:\Users\user\Documents\newstart\excel_shm.db"

if not os.path.exists(shm_path):
    shm_path = r"C:\Users\User\AppData\Local\Microsoft\Office\OTele\excel.exe.db-shm"

print(f"Reading: {shm_path}")
print(f"Size: {os.path.getsize(shm_path)} bytes\n")

with open(shm_path, 'rb') as f:
    data = f.read()

# Search for text strings that might contain workbook data
text_chunks = []
current_chunk = []
for i in range(len(data)):
    byte = data[i]
    if 32 <= byte <= 126:  # Printable ASCII
        current_chunk.append(chr(byte))
    else:
        if len(current_chunk) > 10:
            text = ''.join(current_chunk)
            if any(keyword in text.lower() for keyword in ['sheet', 'workbook', 'book', 'cell', 'row', 'column', '.xlsx', '.xlsb']):
                text_chunks.append((i - len(current_chunk), text))
        current_chunk = []

print(f"Found {len(text_chunks)} text chunks with Excel keywords:\n")

for offset, text in text_chunks[:50]:
    print(f"Offset {offset}: {text[:200]}")
    print()

# Save all findings
output = r"d:\Users\user\Documents\newstart\excel_shm_analysis.txt"
with open(output, 'w', encoding='utf-8') as out:
    for offset, text in text_chunks:
        out.write(f"=== Offset {offset} ===\n{text}\n\n")

print(f"\nFull analysis saved to: {output}")
