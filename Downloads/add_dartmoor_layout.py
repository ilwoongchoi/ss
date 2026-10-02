from qgis.core import (
    QgsApplication, QgsProject, QgsVectorLayer, QgsGraduatedSymbolRenderer,
    QgsRendererRange, QgsFillSymbol, QgsClassificationJenks,
    QgsPrintLayout, QgsLayoutItemMap, QgsLayoutItemLegend,
    QgsLayoutItemLabel, QgsLayoutItemPicture, QgsLayoutItemScaleBar,
    QgsLayoutSize, QgsLayoutPoint, QgsUnitTypes, QgsLayerTree
)
from qgis.PyQt.QtGui import QColor, QFont

print("=== Adding DARTMOOR Layout to QGIS Project ===")

app = QgsApplication([], False)
QgsApplication.initQgis()

PROJECT_PATH = r"C:\Users\User\Downloads\Chilterns Connectivity.qgz"
GPKG = r"D:\새 폴더\national_parks_results.gpkg"

project = QgsProject.instance()
project.read(PROJECT_PATH)

park_title = "DARTMOOR"
opp_layer_name = "opp_dartmoor"
hab_name = "Purple Moor Grass & Rush Pasture"
layout_name = f"{park_title} - Ecosystem Connectivity Opportunity"

TIER_COLORS = [
    ("#FFFFCC", "Tier 5: Very Low (<0.20)"),
    ("#FED976", "Tier 4: Low (0.20-0.35)"),
    ("#FD8D3C", "Tier 3: Moderate (0.35-0.45)"),
    ("#E31A1C", "Tier 2: High (0.45-0.56)"),
    ("#800026", "Tier 1: Very High (>0.56)")
]

# Load Opportunity Layer
opp_uri = f"{GPKG}|layername={opp_layer_name}"
opp_layer = QgsVectorLayer(opp_uri, f"{park_title} - Connectivity Opportunity", "ogr")

c_jenks = QgsClassificationJenks()
ranges_raw = c_jenks.classesV2(opp_layer, "final_score", 5)
ranges = []

for i in range(len(ranges_raw[0])):
    r_item = ranges_raw[0][i]
    color_hex, label_text = TIER_COLORS[min(i, len(TIER_COLORS)-1)]
    sym = QgsFillSymbol.createSimple({'color': color_hex, 'outline_color': 'black', 'outline_width': '0.1'})
    r = QgsRendererRange(r_item.lowerBound(), r_item.upperBound(), sym, label_text)
    ranges.append(r)
    
renderer = QgsGraduatedSymbolRenderer("final_score", ranges)
opp_layer.setRenderer(renderer)
project.addMapLayer(opp_layer, True)

layout_manager = project.layoutManager()
existing = layout_manager.layoutByName(layout_name)
if existing:
    layout_manager.removeLayout(existing)
    
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName(layout_name)
layout_manager.addLayout(layout)

# 1. Base Map
map_item = QgsLayoutItemMap(layout)
map_item.attemptMove(QgsLayoutPoint(4, 5, QgsUnitTypes.LayoutMillimeters))
map_item.attemptResize(QgsLayoutSize(289, 200, QgsUnitTypes.LayoutMillimeters))
map_item.setBackgroundColor(QColor(245, 245, 245))

extent = opp_layer.extent()
extent.scale(1.15)
map_item.setExtent(extent)
layout.addLayoutItem(map_item)

# 2. Title
title = QgsLayoutItemLabel(layout)
title.setText(f"{park_title} NATIONAL PARK\nEcosystem Connectivity & Restoration Opportunities\nTarget: {hab_name} (UKHab Standard)")
font = QFont("Arial", 12)
font.setBold(True)
title.setFont(font)
title.attemptMove(QgsLayoutPoint(15, 12, QgsUnitTypes.LayoutMillimeters))
title.attemptResize(QgsLayoutSize(190, 24, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(title)

# 3. North Arrow
north = QgsLayoutItemPicture(layout)
north.setPicturePath(":/images/north_arrows/layout_default_north_arrow.svg")
north.attemptMove(QgsLayoutPoint(15, 38, QgsUnitTypes.LayoutMillimeters))
north.attemptResize(QgsLayoutSize(12, 16, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(north)

# 4. Scale Bar
scalebar = QgsLayoutItemScaleBar(layout)
scalebar.setStyle('Single Box')
scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
scalebar.setNumberOfSegments(2)
scalebar.setNumberOfSegmentsLeft(0)
scalebar.setUnitsPerSegment(5.0)
scalebar.setUnitLabel('km')
scalebar.setFont(QFont("Arial", 9))
scalebar.setLinkedMap(map_item)
scalebar.attemptMove(QgsLayoutPoint(15, 185, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(scalebar)

# 5. Legend
legend = QgsLayoutItemLegend(layout)
legend.setTitle("Ecological Priorities")
legend.setLinkedMap(map_item)
legend.attemptMove(QgsLayoutPoint(195, 120, QgsUnitTypes.LayoutMillimeters))
legend.setAutoUpdateModel(False)

custom_tree = QgsLayerTree()
custom_tree.addLayer(opp_layer)
legend.model().setRootGroup(custom_tree)
legend.adjustBoxSize()
layout.addLayoutItem(legend)

project.write()
print(f"\n>>> DARTMOOR Layout successfully created and registered in: {PROJECT_PATH}")
QgsApplication.exitQgis()
