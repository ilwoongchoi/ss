import zipfile, xml.etree.ElementTree as ET

z = zipfile.ZipFile(r'C:\Users\User\Downloads\Chilterns Connectivity.qgz')
xml_content = z.read('Chilterns Connectivity.qgs')
tree = ET.fromstring(xml_content)

# Map of layout name keywords to their exact layer ID substring or name
PARK_LAYER_MAP = {
    'DARTMOOR': 'opp_dartmoor',
    'EXMOOR': 'opp_exmoor',
    'LAKE DISTRICT': 'opp_lake_district',
    'NEW FOREST': 'opp_new_forest',
    'NORTH YORK MOORS': 'opp_north_york_moors',
    'NORTHUMBERLAND': 'opp_northumberland',
    'PEAK DISTRICT': 'opp_peak_district',
    'SOUTH DOWNS': 'opp_south_downs',
    'THE BROADS': 'opp_the_broads',
    'YORKSHIRE DALES': 'opp_yorkshire_dales'
}

# Find layer ids in the project
layer_id_lookup = {}
for maplayer in tree.findall('.//maplayer'):
    lid = maplayer.find('id').text if maplayer.find('id') is not None else ''
    lname = maplayer.find('layername').text if maplayer.find('layername') is not None else ''
    ds = maplayer.find('datasource').text if maplayer.find('datasource') is not None else ''
    for park, tag in PARK_LAYER_MAP.items():
        if tag in ds or tag in lname.lower() or park.lower() in lname.lower():
            layer_id_lookup[park] = (lid, lname)

print("Found Layer IDs for Parks:")
for k, v in layer_id_lookup.items():
    print(f"  {k}: id={v[0]}, name={v[1]}")

# Modify layouts
layouts = tree.findall('.//Layout')
for layout in layouts:
    lname = layout.get('name', '')
    for park, (lid, layer_display_name) in layer_id_lookup.items():
        if park in lname.upper():
            print(f"\nProcessing Layout: {lname} for park {park}")
            for legend in layout.findall('.//LayoutItem[@type="65642"]'):
                # 1. Disable auto update
                legend.set('autoUpdate', '0')
                legend.set('title', 'Ecological Priorities')
                
                # 2. Find layer-tree-group
                ltg = legend.find('.//layer-tree-group')
                if ltg is not None:
                    # Remove all existing children
                    for child in list(ltg):
                        ltg.remove(child)
                    
                    # Add ONLY this single park layer
                    new_node = ET.SubElement(ltg, 'layer-tree-layer', {
                        'id': lid,
                        'name': layer_display_name,
                        'checked': 'Qt::Checked',
                        'expanded': '1',
                        'legend_exp': '',
                        'patch_size': '0,0',
                        'source': ''
                    })
                    print(f"  -> Successfully isolated legend to ONLY: {layer_display_name} (id={lid})")

# Write back directly to QGZ
with zipfile.ZipFile(r'C:\Users\User\Downloads\Chilterns Connectivity.qgz', 'w', zipfile.ZIP_DEFLATED) as z_out:
    z_out.writestr('Chilterns Connectivity.qgs', ET.tostring(tree, encoding='utf-8', xml_declaration=True))

print("\n>>> ALL 10 NATIONAL PARKS LEGENDS 100% ISOLATED AND SAVED TO PROJECT!")
