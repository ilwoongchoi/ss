import os, shutil
from qgis.core import QgsApplication, QgsProject, QgsLayoutExporter

app = QgsApplication([], False)
QgsApplication.initQgis()

PACKAGE_DIR = r"D:\새 폴더\BNG_Ecosystem_Connectivity_Portfolio"
SCRIPTS_DIR = os.path.join(PACKAGE_DIR, "Scripts")
EXPORT_DIR = os.path.join(PACKAGE_DIR, "Exported_Layouts")
os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(SCRIPTS_DIR, exist_ok=True)

# 1. Clean out Scripts folder - keep ONLY national parks pipeline script
for f in os.listdir(SCRIPTS_DIR):
    os.remove(os.path.join(SCRIPTS_DIR, f))

shutil.copy2(r"C:\Users\User\Downloads\run_all_national_parks.py", os.path.join(SCRIPTS_DIR, "national_parks_pipeline.py"))
print("1. Scripts folder cleaned: Kept ONLY national_parks_pipeline.py")

# 2. Delete README.md if present
readme_path = os.path.join(PACKAGE_DIR, "README.md")
if os.path.exists(readme_path):
    os.remove(readme_path)
    print("2. Deleted README.md")

# 3. Read Project and Export ALL 11 Layouts (Including DARTMOOR)
project_path = os.path.join(PACKAGE_DIR, "Ecosystem_Connectivity_National_Parks.qgz")
project = QgsProject.instance()
project.read(project_path)
lm = project.layoutManager()

print(f"3. Exporting {len(lm.layouts())} Layouts to PNG & PDF...")
for layout in lm.layouts():
    clean_name = "".join(c for c in layout.name() if c.isalnum() or c in (' ', '_', '-')).rstrip()
    png_path = os.path.join(EXPORT_DIR, f"{clean_name}.png")
    pdf_path = os.path.join(EXPORT_DIR, f"{clean_name}.pdf")
    
    exporter = QgsLayoutExporter(layout)
    img_settings = QgsLayoutExporter.ImageExportSettings()
    img_settings.dpi = 300
    pdf_settings = QgsLayoutExporter.PdfExportSettings()
    pdf_settings.dpi = 300
    
    exporter.exportToImage(png_path, img_settings)
    exporter.exportToPdf(pdf_path, pdf_settings)
    print(f"  Exported: {clean_name}")

QgsApplication.exitQgis()
print("Export complete!")
