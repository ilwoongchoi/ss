from osgeo import gdal, osr
import glob, os

files = glob.glob(r"C:\Users\User\Downloads\data\*.tif") + glob.glob(r"C:\Users\User\Downloads\lidar\*.tif")
print(f"=== Found {len(files)} Raster Files ===")
for f in sorted(files):
    ds = gdal.Open(f)
    if ds:
        proj = ds.GetProjection()
        srs = osr.SpatialReference(wkt=proj)
        epsg = srs.GetAttrValue('AUTHORITY', 1) if srs else 'Unknown'
        gt = ds.GetGeoTransform()
        print(f"File: {os.path.basename(f):32s} | Size: {ds.RasterXSize:5d}x{ds.RasterYSize:5d} | EPSG: {epsg} | Res: {gt[1]:.2f}m")
    else:
        print(f"File: {os.path.basename(f)} could not be opened")
