r"""
Download OpenStreetMap tiles directly for Cotswolds BBox and mosaic into GeoTIFF
================================================================================
"""
import math
import io
import os
import urllib.request
import numpy as np
from PIL import Image
from osgeo import gdal, osr

gdal.UseExceptions()

# Cotswolds BBox in EPSG:27700 (British National Grid)
# BBox with margin: (360000, 150000, 450000, 255000)
# Convert BNG -> WGS84 (EPSG:4326)
src_srs = osr.SpatialReference()
src_srs.ImportFromEPSG(27700)
dst_srs = osr.SpatialReference()
dst_srs.ImportFromEPSG(4326)
transform = osr.CoordinateTransformation(src_srs, dst_srs)

# Points: SW (360000, 150000), NE (450000, 255000)
lat_min, lon_min, _ = transform.TransformPoint(360000, 150000)
lat_max, lon_max, _ = transform.TransformPoint(450000, 255000)

print(f"Cotswolds WGS84 BBox: Lon ({lon_min:.4f}, {lon_max:.4f}), Lat ({lat_min:.4f}, {lat_max:.4f})")

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg

# Zoom 11 gives ~75m resolution (high detail roads, towns, forests, place names)
ZOOM = 11
x_min, y_min = deg2num(lat_max, lon_min, ZOOM)
x_max, y_max = deg2num(lat_min, lon_max, ZOOM)

x_tiles = list(range(x_min, x_max + 1))
y_tiles = list(range(y_min, y_max + 1))

print(f"Downloading OSM Tiles at Zoom {ZOOM}: {len(x_tiles)} x {len(y_tiles)} = {len(x_tiles)*len(y_tiles)} tiles...")

width = len(x_tiles) * 256
height = len(y_tiles) * 256
mosaic = Image.new("RGB", (width, height), (255, 255, 255))

headers = {"User-Agent": "CotswoldsPermeabilityGIS/1.0 (academic research)"}

success = 0
for i, x in enumerate(x_tiles):
    for j, y in enumerate(y_tiles):
        url = f"https://tile.openstreetmap.org/{ZOOM}/{x}/{y}.png"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                tile_data = resp.read()
                tile_img = Image.open(io.BytesIO(tile_data)).convert("RGB")
                mosaic.paste(tile_img, (i * 256, j * 256))
                success += 1
        except Exception as e:
            print(f"  Failed tile {x},{y}: {e}")

print(f"Downloaded {success}/{len(x_tiles)*len(y_tiles)} tiles. Building GeoTIFF...")

# Bounds in Web Mercator (EPSG:3857)
def lon2x_3857(lon):
    return lon * 20037508.34 / 180.0

def lat2y_3857(lat):
    y = math.log(math.tan((90.0 + lat) * math.pi / 360.0)) / (math.pi / 180.0)
    return y * 20037508.34 / 180.0

lat_top, lon_left = num2deg(x_min, y_min, ZOOM)
lat_bottom, lon_right = num2deg(x_max + 1, y_max + 1, ZOOM)

x0_3857 = lon2x_3857(lon_left)
y0_3857 = lat2y_3857(lat_top)
x1_3857 = lon2x_3857(lon_right)
y1_3857 = lat2y_3857(lat_bottom)

pixel_x = (x1_3857 - x0_3857) / width
pixel_y = (y0_3857 - y1_3857) / height

temp_3857 = r"D:\새 폴더\osm_temp_3857.tif"
final_27700 = r"D:\새 폴더\cotswolds_osm_basemap_27700.tif"

arr = np.array(mosaic)
driver = gdal.GetDriverByName("GTiff")
ds = driver.Create(temp_3857, width, height, 3, gdal.GDT_Byte, ["COMPRESS=DEFLATE"])
ds.SetGeoTransform((x0_3857, pixel_x, 0, y0_3857, 0, -pixel_y))
srs_3857 = osr.SpatialReference()
srs_3857.ImportFromEPSG(3857)
ds.SetProjection(srs_3857.ExportToWkt())

for b in range(3):
    ds.GetRasterBand(b + 1).WriteArray(arr[:, :, b])
ds.FlushCache()
ds = None

print("Reprojecting OSM GeoTIFF to EPSG:27700 (British National Grid)...")
warp_opts = gdal.WarpOptions(
    dstSRS="EPSG:27700",
    format="GTiff",
    creationOptions=["COMPRESS=DEFLATE", "TILED=YES"],
    xRes=50,
    yRes=50
)
gdal.Warp(final_27700, temp_3857, options=warp_opts)

if os.path.exists(temp_3857):
    os.remove(temp_3857)

print(f"OSM Basemap GeoTIFF successfully generated: {final_27700}")
