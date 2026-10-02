#!/usr/bin/env python3
"""Parse EVTX to find Excel crash times"""
import Evtx.Evtx as evtx
import Evtx.Views as e_views
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_evtx(filepath):
    """Parse evtx file and find Excel-related errors"""
    excel_crashes = []
    
    with evtx.Evtx(filepath) as log:
        for record in log.records():
            try:
                xml_str = record.xml()
                root = ET.fromstring(xml_str)
                
                # Extract timestamp
                ns = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}
                time_created = root.find('.//ns:TimeCreated', ns)
                if time_created is not None:
                    timestamp_str = time_created.get('SystemTime')
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
                else:
                    continue
                
                # Look for Excel-related content
                xml_lower = xml_str.lower()
                if any(keyword in xml_lower for keyword in ['excel', 'msoshext', 'office']):
                    # Extract key info
                    event_id_elem = root.find('.//ns:EventID', ns)
                    event_id = event_id_elem.text if event_id_elem is not None else 'Unknown'
                    
                    level_elem = root.find('.//ns:Level', ns)
                    level = level_elem.text if level_elem is not None else 'Unknown'
                    
                    provider_elem = root.find('.//ns:Provider', ns)
                    provider = provider_elem.get('Name') if provider_elem is not None else 'Unknown'
                    
                    # Get event data
                    event_data = []
                    for data_elem in root.findall('.//ns:Data', ns):
                        event_data.append(data_elem.text if data_elem.text else '')
                    
                    excel_crashes.append({
                        'timestamp': timestamp,
                        'event_id': event_id,
                        'level': level,
                        'provider': provider,
                        'data': ' | '.join(event_data),
                        'xml': xml_str[:500]  # First 500 chars
                    })
                    
            except Exception as e:
                continue
    
    return excel_crashes

if __name__ == "__main__":
    evtx_file = r"d:\Users\user\Documents\newstart\1.evtx"
    
    print("Parsing EVTX file for Excel events...")
    crashes = parse_evtx(evtx_file)
    
    if not crashes:
        print("No Excel-related events found.")
    else:
        print(f"Found {len(crashes)} Excel-related events:\n")
        
        # Sort by timestamp
        crashes.sort(key=lambda x: x['timestamp'], reverse=True)
        
        for i, crash in enumerate(crashes[:20], 1):  # Show top 20
            print(f"\n[{i}] Time: {crash['timestamp']}")
            print(f"    Event ID: {crash['event_id']}, Level: {crash['level']}")
            print(f"    Provider: {crash['provider']}")
            if crash['data']:
                print(f"    Data: {crash['data'][:200]}")
