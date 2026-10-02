import zipfile, xml.etree.ElementTree as ET

z = zipfile.ZipFile(r'C:\Users\User\Downloads\Chilterns Connectivity.qgz')
tree = ET.fromstring(z.read('Chilterns Connectivity.qgs'))

target_layout_name = "Chilterns Area of Outstanding Natural Beauty Ecosystem Connectivity Opportunity"
layout = None
for l in tree.findall('.//Layout'):
    if l.get('name') == target_layout_name:
        layout = l
        break

if layout is None:
    print("Layout not found!")
    exit()

print(f"=== Found Layout: {target_layout_name} ===")
# Inspect all child elements and attributes
for elem in layout:
    print(f"Tag: {elem.tag}, attrib: {elem.attrib}")
    if elem.tag == 'LayoutItem':
        print(f"  Item Type ID: {elem.get('type')}, position: x={elem.get('positionX')}, y={elem.get('positionY')}, w={elem.get('sizeWidth')}, h={elem.get('sizeHeight')}")
        # check for specific elements inside
        for sub in elem:
            if 'legend' in sub.tag.lower() or 'map' in sub.tag.lower() or 'text' in sub.tag.lower() or 'extent' in sub.tag.lower():
                print(f"    Sub: {sub.tag}, text={sub.text[:80] if sub.text else ''}, attrib={sub.attrib}")

# Look specifically for Legend details
for leg in layout.findall('.//LayoutItem[@type="65642"]'):
    print("\n--- Legend Properties ---")
    print("Title:", leg.get('title'))
    for child in leg:
        print(f"  {child.tag}: {child.attrib}")
        if child.tag == 'layer-tree-group':
            for layer in child.findall('.//layer-tree-layer'):
                print(f"    Legend Layer: {layer.get('name')}, id={layer.get('id')}, checked={layer.get('checked')}")

# Look for Map properties
for m in layout.findall('.//LayoutItem[@type="65639"]'):
    print("\n--- Map Properties ---")
    for child in m:
        if child.tag in ['Extent', 'crs', 'AtlasProperties']:
            print(f"  {child.tag}: {child.attrib}")
            for sc in child:
                print(f"    {sc.tag}: {sc.text if sc.text else sc.attrib}")
