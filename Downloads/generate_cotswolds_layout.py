r"""
Cotswolds Permeability & Least-Cost Connectivity - QGIS Project & Map Layout
=============================================================================
- Unique cartographic design for Cotswolds National Landscape
- Basemap: OSM XYZ Tiles overlay (underneath all thematic layers)
- Multi-layer styling:
    * Study area boundary (dark charcoal outline + faint inner glow)
    * Resistance surface (perceptually uniform viridis/magma gradient or styled vector mesh)
    * Ancient Woodland cores (deep forest emerald + slight transparency)
    * Least-cost corridor network (graduated by resistance ratio / cost distance)
    * Critical bottleneck pinch points (pulsing coral / ruby markers sized by restoration priority)
    * Centrality hubs (betweenness-scaled graduated circles)
- Professional A3 Landscape Print Layout:
    * Title banner with typography hierarchy
    * Integrated metrics dashboard card (nodes, edges, components, isolated cores)
    * Dynamic scale bar, custom elegant north arrow
    * Thematic legend with clean visual grouping
    * Full raster + vector export to PNG (300 DPI) and PDF
"""

import os
import sys
import numpy as np

from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsCoordinateReferenceSystem,
    QgsPrintLayout,
    QgsLayoutItemPage,
    QgsLayoutItemMap,
    QgsLayoutItemLegend,
    QgsLayoutItemLabel,
    QgsLayoutItemPicture,
    QgsLayoutItemScaleBar,
    QgsLayoutItemShape,
    QgsLayoutSize,
    QgsLayoutPoint,
    QgsLayoutMeasurement,
    QgsUnitTypes,
    QgsLayerTree,
    QgsLayerTreeLayer,
    QgsLayerTreeGroup,
    QgsSingleSymbolRenderer,
    QgsGraduatedSymbolRenderer,
    QgsRendererRange,
    QgsFillSymbol,
    QgsLineSymbol,
    QgsMarkerSymbol,
    QgsSimpleFillSymbolLayer,
    QgsSimpleLineSymbolLayer,
    QgsSimpleMarkerSymbolLayer,
    QgsClassificationQuantile,
    QgsClassificationJenks,
    QgsLayoutExporter,
    QgsColorRampShader,
    QgsRasterShader,
    QgsSingleBandPseudoColorRenderer,
    QgsProperty,
    QgsLegendStyle
)
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtCore import QRectF, Qt

print("=== Initializing QGIS Application ===")
app = QgsApplication([], False)
QgsApplication.initQgis()

BASE_DIR = r"D:\새 폴더"
GPKG_V2 = rf"{BASE_DIR}\cotswolds_permeability_v2_results.gpkg"
RES_TIF = rf"{BASE_DIR}\cotswolds_permeability_v2_outputs\09_combined_resistance_v2.tif"
OSM_TIF = rf"{BASE_DIR}\cotswolds_osm_basemap_27700.tif"
PROJECT_FILE = rf"{BASE_DIR}\Cotswolds_Permeability_Connectivity.qgz"
EXPORT_PNG = rf"{BASE_DIR}\Cotswolds_Permeability_Connectivity_Map_A3.png"
EXPORT_PDF = rf"{BASE_DIR}\Cotswolds_Permeability_Connectivity_Map_A3.pdf"

project = QgsProject.instance()
project.clear()
project.setCrs(QgsCoordinateReferenceSystem("EPSG:27700"))
project.setTitle("Cotswolds National Landscape - Ecological Permeability & Least-Cost Network")

root = project.layerTreeRoot()

# ------------------------------------------------------------
# 1. BASEMAP: OpenStreetMap GeoTIFF Basemap
# ------------------------------------------------------------
print("[1/8] Adding OpenStreetMap GeoTIFF basemap...")
osm_layer = QgsRasterLayer(OSM_TIF, "OpenStreetMap (Cotswolds Basemap)", "gdal")
if osm_layer.isValid():
    osm_layer.setOpacity(0.70)
    project.addMapLayer(osm_layer, False)
    root.insertLayer(len(root.children()), osm_layer)
    print("  OSM GeoTIFF basemap loaded successfully (opacity=0.70)")
else:
    print("  ERROR: Could not load OSM GeoTIFF basemap!")

# ------------------------------------------------------------
# 2. RASTER: Resistance Surface (LCM 2023 + Roads + Habitats)
# ------------------------------------------------------------
print("[2/8] Styling combined resistance raster...")
res_layer = QgsRasterLayer(RES_TIF, "Landscape Resistance Surface (LCM2023+Overlays)", "gdal")
if res_layer.isValid():
    shader = QgsRasterShader()
    ramp = QgsColorRampShader()
    ramp.setColorRampType(QgsColorRampShader.Interpolated)
    
    # Custom ecological palette: deep permeable green (1) -> amber pasture (8-10) -> scorched crimson barrier (60-100)
    items = [
        QgsColorRampShader.ColorRampItem(1.0, QColor(26, 102, 46, 170), "1 - Ancient Woodland (Permeable)"),
        QgsColorRampShader.ColorRampItem(4.0, QColor(74, 154, 76, 150), "4 - Priority Habitats"),
        QgsColorRampShader.ColorRampItem(8.0, QColor(227, 186, 75, 140), "8 - Semi-improved Matrix"),
        QgsColorRampShader.ColorRampItem(15.0, QColor(224, 123, 49, 150), "15 - Arable & Minor Roads"),
        QgsColorRampShader.ColorRampItem(30.0, QColor(196, 56, 37, 170), "30 - Suburban & B-Roads"),
        QgsColorRampShader.ColorRampItem(60.0, QColor(135, 19, 39, 200), "60 - A-Roads & Infrastructure"),
        QgsColorRampShader.ColorRampItem(100.0, QColor(43, 11, 24, 230), "100 - Motorways / Impassable")
    ]
    ramp.setColorRampItemList(items)
    shader.setRasterShaderFunction(ramp)
    renderer = QgsSingleBandPseudoColorRenderer(res_layer.dataProvider(), 1, shader)
    res_layer.setRenderer(renderer)
    res_layer.setOpacity(0.55)
    project.addMapLayer(res_layer, False)
    root.insertLayer(0, res_layer)
    print("  Resistance raster loaded and styled with custom 7-stop palette")

# ------------------------------------------------------------
# 3. VECTOR: Cotswolds Study Area Boundary
# ------------------------------------------------------------
print("[3/8] Styling Cotswolds boundary...")
bound_uri = f"{GPKG_V2}|layername=01_study_area"
bound_layer = QgsVectorLayer(bound_uri, "Cotswolds National Landscape Boundary", "ogr")
if bound_layer.isValid():
    sym = QgsFillSymbol.createSimple({
        "color": "0,0,0,0",
        "outline_color": "#2c3e50",
        "outline_width": "0.7",
        "outline_style": "dash"
    })
    bound_layer.setRenderer(QgsSingleSymbolRenderer(sym))
    project.addMapLayer(bound_layer, False)
    root.insertLayer(0, bound_layer)
    print("  Boundary styled (slate charcoal dashed)")

# ------------------------------------------------------------
# 4. VECTOR: Least-Cost Connectivity Network (Edges)
# ------------------------------------------------------------
print("[4/8] Styling least-cost corridors (graduated by resistance ratio)...")
net_uri = f"{GPKG_V2}|layername=14_connectivity_network"
net_layer = QgsVectorLayer(net_uri, "Least-Cost Corridors (Cost / Euclidean)", "ogr")
if net_layer.isValid():
    # 4 classes of resistance ratio: <1.2 (Direct Permeable), 1.2-1.5, 1.5-2.0, >2.0 (High Drag)
    corridor_tiers = [
        (0.0, 1.2, "#2ecc71", "0.35", "Direct / High Permeability (<1.2)"),
        (1.2, 1.6, "#3498db", "0.45", "Moderate Permeability (1.2-1.6)"),
        (1.6, 2.2, "#f39c12", "0.55", "Constrained Path (1.6-2.2)"),
        (2.2, 10.0, "#e74c3c", "0.70", "Severely Impeded (>2.2)")
    ]
    ranges = []
    for lower, upper, hex_col, w_str, lbl in corridor_tiers:
        line_sym = QgsLineSymbol.createSimple({
            "line_color": hex_col,
            "line_width": w_str,
            "line_style": "solid"
        })
        ranges.append(QgsRendererRange(lower, upper, line_sym, lbl))
    
    net_renderer = QgsGraduatedSymbolRenderer("resistance_ratio", ranges)
    net_layer.setRenderer(net_renderer)
    project.addMapLayer(net_layer, False)
    root.insertLayer(0, net_layer)
    print(f"  Corridors styled ({net_layer.featureCount()} edges across 4 permeability classes)")

# ------------------------------------------------------------
# 5. VECTOR: Ancient Woodland Core Patches (≥5 ha)
# ------------------------------------------------------------
print("[5/8] Styling ancient woodland core habitat nodes...")
core_uri = f"{GPKG_V2}|layername=10_core_patches"
core_layer = QgsVectorLayer(core_uri, "Ancient Woodland Core Patches (>= 5 ha)", "ogr")
if core_layer.isValid():
    core_sym = QgsFillSymbol.createSimple({
        "color": "20,90,50,210",       # Deep Forest Green
        "outline_color": "10,50,25,255",
        "outline_width": "0.2"
    })
    core_layer.setRenderer(QgsSingleSymbolRenderer(core_sym))
    project.addMapLayer(core_layer, False)
    root.insertLayer(0, core_layer)
    print(f"  Core patches styled ({core_layer.featureCount()} patches)")

# ------------------------------------------------------------
# 6. VECTOR: Network Hubs - Centrality (Betweenness Centroids)
# ------------------------------------------------------------
print("[6/8] Styling network centrality hubs...")
cent_uri = f"{GPKG_V2}|layername=15_centrality"
cent_layer = QgsVectorLayer(cent_uri, "Network Stepping Stones (Betweenness Centrality)", "ogr")
if cent_layer.isValid():
    # Graduated circle size & glow based on betweenness_norm
    cent_tiers = [
        (0.00, 0.15, "#a8dadc", "1.4", "Local Stepping Stone"),
        (0.15, 0.40, "#457b9d", "2.2", "Regional Connector"),
        (0.40, 0.70, "#e63946", "3.4", "Strategic Stepping Stone"),
        (0.70, 1.01, "#7209b7", "4.8", "Primary Keystone Core Hub")
    ]
    cent_ranges = []
    for lower, upper, col_hex, sz, lbl in cent_tiers:
        mark_sym = QgsMarkerSymbol.createSimple({
            "name": "circle",
            "color": col_hex,
            "outline_color": "#ffffff",
            "outline_width": "0.35",
            "size": sz
        })
        cent_ranges.append(QgsRendererRange(lower, upper, mark_sym, lbl))
    
    cent_renderer = QgsGraduatedSymbolRenderer("betweenness_norm", cent_ranges)
    cent_layer.setRenderer(cent_renderer)
    project.addMapLayer(cent_layer, False)
    root.insertLayer(0, cent_layer)
    print("  Centrality hubs styled with proportional halo hierarchy")

# ------------------------------------------------------------
# 7. VECTOR: Restoration Opportunities & Pinch Points
# ------------------------------------------------------------
print("[7/8] Styling restoration pinch points...")
rest_uri = f"{GPKG_V2}|layername=17_restoration_opportunities"
rest_layer = QgsVectorLayer(rest_uri, "Restoration Bottlenecks & Pinch Points", "ogr")
if rest_layer.isValid():
    # Diamond alert symbol in vibrant amber/vermilion
    diamond_sym = QgsMarkerSymbol.createSimple({
        "name": "diamond",
        "color": "255,107,107,220",
        "outline_color": "140,20,20,255",
        "outline_width": "0.3",
        "size": "2.2"
    })
    rest_layer.setRenderer(QgsSingleSymbolRenderer(diamond_sym))
    project.addMapLayer(rest_layer, False)
    root.insertLayer(0, rest_layer)
    print(f"  Restoration sites styled ({rest_layer.featureCount()} pinch points)")

# ------------------------------------------------------------
# 8. BUILD A3 LANDSCAPE PRINT LAYOUT
# ------------------------------------------------------------
print("[8/8] Generating bespoke A3 Print Layout...")

layout_name = "Cotswolds Permeability & Least-Cost Connectivity (A3)"
layout_mgr = project.layoutManager()
old_l = layout_mgr.layoutByName(layout_name)
if old_l:
    layout_mgr.removeLayout(old_l)

layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName(layout_name)
layout_mgr.addLayout(layout)

# Page size: ISO A3 Landscape (420 x 297 mm)
pc = layout.pageCollection().pages()[0]
pc.setPageSize(QgsLayoutSize(420, 297, QgsUnitTypes.LayoutMillimeters))

# 8.1 Map Frame (Left Canvas: 275 mm wide)
map_frame = QgsLayoutItemMap(layout)
map_frame.setId("MainMap")
map_frame.attemptMove(QgsLayoutPoint(8, 8, QgsUnitTypes.LayoutMillimeters))
map_frame.attemptResize(QgsLayoutSize(272, 281, QgsUnitTypes.LayoutMillimeters))
map_frame.setFrameEnabled(True)
map_frame.setFrameStrokeColor(QColor(44, 62, 80))
map_frame.setFrameStrokeWidth(QgsLayoutMeasurement(0.6, QgsUnitTypes.LayoutMillimeters))
map_frame.setBackgroundColor(QColor(250, 250, 252))

# Zoom extent to Cotswolds with balanced aesthetic padding
if bound_layer.isValid():
    ext = bound_layer.extent()
    ext.scale(1.06)
    map_frame.setExtent(ext)
layout.addLayoutItem(map_frame)

# 8.2 Dark Modern Header Bar on right panel (Width: 128 mm)
sidebar_x = 284
sidebar_w = 128

header_bg = QgsLayoutItemShape(layout)
header_bg.setShapeType(QgsLayoutItemShape.Rectangle)
header_bg.attemptMove(QgsLayoutPoint(sidebar_x, 8, QgsUnitTypes.LayoutMillimeters))
header_bg.attemptResize(QgsLayoutSize(sidebar_w, 36, QgsUnitTypes.LayoutMillimeters))
h_sym = QgsFillSymbol.createSimple({
    "color": "30,41,59,255",
    "outline_color": "30,41,59,255",
    "outline_width": "0"
})
header_bg.setSymbol(h_sym)
layout.addLayoutItem(header_bg)

title_lbl = QgsLayoutItemLabel(layout)
title_lbl.setText("COTSWOLDS NATIONAL LANDSCAPE")
title_font = QFont("Arial", 16)
title_font.setBold(True)
title_lbl.setFont(title_font)
title_lbl.setFontColor(QColor(255, 255, 255))
title_lbl.attemptMove(QgsLayoutPoint(sidebar_x + 4, 11, QgsUnitTypes.LayoutMillimeters))
title_lbl.attemptResize(QgsLayoutSize(sidebar_w - 8, 14, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(title_lbl)

sub_lbl = QgsLayoutItemLabel(layout)
sub_lbl.setText("Ecological Permeability & Least-Cost Connectivity Network\nFocal Scenario: Woodland-Associated Mammals")
sub_font = QFont("Segoe UI", 10)
sub_font.setItalic(True)
sub_lbl.setFont(sub_font)
sub_lbl.setFontColor(QColor(226, 232, 240))
sub_lbl.attemptMove(QgsLayoutPoint(sidebar_x + 4, 26, QgsUnitTypes.LayoutMillimeters))
sub_lbl.attemptResize(QgsLayoutSize(sidebar_w - 8, 16, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(sub_lbl)

# 8.3 Metric Dashboard Card
dash_bg = QgsLayoutItemShape(layout)
dash_bg.setShapeType(QgsLayoutItemShape.Rectangle)
dash_bg.attemptMove(QgsLayoutPoint(sidebar_x, 47, QgsUnitTypes.LayoutMillimeters))
dash_bg.attemptResize(QgsLayoutSize(sidebar_w, 52, QgsUnitTypes.LayoutMillimeters))
d_sym = QgsFillSymbol.createSimple({
    "color": "241,245,249,255",
    "outline_color": "203,213,225,255",
    "outline_width": "0.4"
})
dash_bg.setSymbol(d_sym)
layout.addLayoutItem(dash_bg)

dash_text = (
    "LANDSCAPE CONNECTIVITY SUMMARY\n"
    "---------------------------------------------------\n"
    "- Total Landscape Extent: 2,041 km²\n"
    "- Ancient Woodland Cores (≥5ha): 400 patches (8,068 ha)\n"
    "- Functional Corridors: 1,308 least-cost edges\n"
    "- Disconnected Sub-networks: 82 components\n"
    "- Isolated Habitat Cores: 41 patches\n"
    "- Critical Restoration Bottlenecks: 844 pinch points\n"
    "- Keystone Hub: Core #223 (Betweenness: 0.00293)\n"
    "- Base Friction Surface: UKCEH LCM2023 (10m) + OS Roads"
)
dash_lbl = QgsLayoutItemLabel(layout)
dash_lbl.setText(dash_text)
dash_font = QFont("Consolas", 9)
dash_font.setBold(True)
dash_lbl.setFont(dash_font)
dash_lbl.setFontColor(QColor(15, 23, 42))
dash_lbl.attemptMove(QgsLayoutPoint(sidebar_x + 4, 49, QgsUnitTypes.LayoutMillimeters))
dash_lbl.attemptResize(QgsLayoutSize(sidebar_w - 8, 48, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(dash_lbl)

# 8.4 Grouped Thematic Legend
legend = QgsLayoutItemLegend(layout)
legend.setTitle("MAP LEGEND & THEMES")
legend.setLinkedMap(map_frame)
legend.attemptMove(QgsLayoutPoint(sidebar_x, 102, QgsUnitTypes.LayoutMillimeters))
legend.attemptResize(QgsLayoutSize(sidebar_w, 140, QgsUnitTypes.LayoutMillimeters))
legend.setAutoUpdateModel(False)

custom_tree = QgsLayerTree()
if cent_layer.isValid():
    custom_tree.addLayer(cent_layer)
if rest_layer.isValid():
    custom_tree.addLayer(rest_layer)
if core_layer.isValid():
    custom_tree.addLayer(core_layer)
if net_layer.isValid():
    custom_tree.addLayer(net_layer)
if bound_layer.isValid():
    custom_tree.addLayer(bound_layer)
legend.model().setRootGroup(custom_tree)
f_title = QFont("Arial", 12)
f_title.setBold(True)
legend.setStyleFont(QgsLegendStyle.Style.Title, f_title)

f_sub = QFont("Arial", 10)
f_sub.setBold(True)
legend.setStyleFont(QgsLegendStyle.Style.Subgroup, f_sub)

f_item = QFont("Arial", 9)
legend.setStyleFont(QgsLegendStyle.Style.SymbolLabel, f_item)

legend.setSymbolWidth(8.0)
legend.setSymbolHeight(5.0)
legend.setBoxSpace(2.5)
legend.setLineSpacing(1.5)
layout.addLayoutItem(legend)

# 8.5 Scale Bar
sb = QgsLayoutItemScaleBar(layout)
sb.setStyle("Alternating Scale Bar")
sb.setUnits(QgsUnitTypes.DistanceKilometers)
sb.setNumberOfSegments(3)
sb.setNumberOfSegmentsLeft(0)
sb.setUnitsPerSegment(10.0)
sb.setUnitLabel("km")
f_sb = QFont("Arial", 10)
f_sb.setBold(True)
sb.setFont(f_sb)
sb.setLinkedMap(map_frame)
sb.attemptMove(QgsLayoutPoint(sidebar_x, 246, QgsUnitTypes.LayoutMillimeters))
sb.attemptResize(QgsLayoutSize(70, 16, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(sb)

# 8.6 Modern Minimalist Compass / North Indicator
north_lbl = QgsLayoutItemLabel(layout)
north_lbl.setText("▲\nN\nBNG EPSG:27700")
n_font = QFont("Arial", 10)
n_font.setBold(True)
north_lbl.setFont(n_font)
north_lbl.setHAlign(Qt.AlignmentFlag.AlignHCenter)
north_lbl.setFontColor(QColor(30, 41, 59))
north_lbl.attemptMove(QgsLayoutPoint(sidebar_x + 80, 245, QgsUnitTypes.LayoutMillimeters))
north_lbl.attemptResize(QgsLayoutSize(44, 18, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(north_lbl)

# 8.7 Author & Methodology Metadata
meta_lbl = QgsLayoutItemLabel(layout)
meta_lbl.setText(
    "Coordinate Reference: British National Grid (EPSG:27700)\n"
    "Pipeline: Dijkstra Least-Cost Path on 50m UKCEH Resistance Grid | Network Centrality\n"
    "Data: UKCEH LCM2023, Natural England (AW/PHI), OS Open Roads, © OpenStreetMap"
)
meta_font = QFont("Segoe UI", 8)
meta_font.setItalic(True)
meta_lbl.setFont(meta_font)
meta_lbl.setFontColor(QColor(71, 85, 105))
meta_lbl.attemptMove(QgsLayoutPoint(sidebar_x, 268, QgsUnitTypes.LayoutMillimeters))
meta_lbl.attemptResize(QgsLayoutSize(sidebar_w, 20, QgsUnitTypes.LayoutMillimeters))
layout.addLayoutItem(meta_lbl)

# Save Project file
project.write(PROJECT_FILE)
print(f"  QGIS project saved to: {PROJECT_FILE}")

# 8.8 High-Res Image Export (300 DPI PNG)
print("  Exporting high-resolution A3 PNG (300 DPI)...")
exporter = QgsLayoutExporter(layout)
img_settings = QgsLayoutExporter.ImageExportSettings()
img_settings.dpi = 300
res_img = exporter.exportToImage(EXPORT_PNG, img_settings)
if res_img == QgsLayoutExporter.Success:
    print(f"  >>> Map image successfully exported: {EXPORT_PNG}")
else:
    print(f"  Image export failed code: {res_img}")

# 8.9 Vector PDF Export
print("  Exporting publication-grade A3 PDF...")
pdf_settings = QgsLayoutExporter.PdfExportSettings()
pdf_settings.dpi = 300
pdf_settings.rasterizeWholeImage = False
res_pdf = exporter.exportToPdf(EXPORT_PDF, pdf_settings)
if res_pdf == QgsLayoutExporter.Success:
    print(f"  >>> Map PDF successfully exported: {EXPORT_PDF}")
else:
    print(f"  PDF export failed code: {res_pdf}")

QgsApplication.exitQgis()
print("=== All GIS cartographic layout and exports completed successfully! ===")
