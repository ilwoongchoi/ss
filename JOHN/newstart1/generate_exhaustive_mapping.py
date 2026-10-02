import pandas as pd
import numpy as np

# 1. Chemical Elements (1-118)
elements_raw = [
    (1, "H", "Hydrogen", "P+", "1:0:0:0:0:0:0:0", "Primordial Spark"),
    (2, "He", "Helium", "γ", "0:0:0:0:0:0:0:1", "Volume Void"),
    (3, "Li", "Lithium", "P+ + ν", "0.8:0:0:0:0:0.2:0:0", "Excitatory Ghost"),
    (4, "Be", "Beryllium", "Z", "0:0:1:0:0:0:0:0", "Narrow Stability"),
    (5, "B", "Boron", "q", "0:0:0:1:0:0:0:0", "Tension Link"),
    (6, "C", "Carbon", "Z", "0:0:1:0:0:0:0:0", "Structural Backbone"),
    (7, "N", "Nitrogen", "ν", "0:0:0:0:0:1:0:0", "Ghost Flux"),
    (8, "O", "Oxygen", "γ", "0:0:0:0:0:0:0:1", "Volume Platform"),
    (9, "F", "Fluorine", "ν + q", "0:0:0:0.5:0:0.5:0:0", "Tension Filter"),
    (10, "Ne", "Neon", "γ", "0:0:0:0:0:0:0:1", "Inertial Volume"),
    (11, "Na", "Sodium", "P+", "1:0:0:0:0:0:0:0", "Kinetic Ignition"),
    (12, "Mg", "Magnesium", "Z + W", "0:0:0.5:0:0.5:0:0:0", "Bridge Stabilizer"),
    (13, "Al", "Aluminum", "Z + g", "0:0.5:0.5:0:0:0:0:0", "Confinement Lock"),
    (14, "Si", "Silicon", "Z", "0:0:1:0:0:0:0:0", "Information Ground"),
    (15, "P", "Phosphorus", "q", "0:0:0:1:0:0:0:0", "ATP Tension"),
    (16, "S", "Sulphur", "W", "0:0:0:0:1:0:0:0", "Redox Bridge"),
    (17, "Cl", "Chlorine", "ν", "0:0:0:0:0:1:0:0", "Negative Balance"),
    (18, "Ar", "Argon", "γ", "0:0:0:0:0:0:0:1", "Inertial Sink"),
    (19, "K", "Potassium", "P+", "1:0:0:0:0:0:0:0", "Intracellular Spark"),
    (20, "Ca", "Calcium", "Z", "0:0:1:0:0:0:0:0", "Skeletal Anchor"),
    (21, "Sc", "Scandium", "H", "0:0:0:0:0:0:1:0", "Light Mass"),
    (22, "Ti", "Titanium", "Z + H", "0:0:0.5:0:0:0:0.5:0", "Shield Anchor"),
    (23, "V", "Vanadium", "W + P+", "0.5:0:0:0:0.5:0:0:0", "Redox Speed"),
    (24, "Cr", "Chromium", "W", "0:0:0:0:1:0:0:0", "Stability Path"),
    (25, "Mn", "Manganese", "g", "0:1:0:0:0:0:0:0", "Water Splitter"),
    (26, "Fe", "Iron", "H", "0:0:0:0:0:0:1:0", "Mass Reservoir"),
    (27, "Co", "Cobalt", "H + ν", "0:0:0:0:0:0.5:0.5:0", "Vitamin Bridge"),
    (28, "Ni", "Nickel", "H", "0:0:0:0:0:0:1:0", "Magnetic Memory"),
    (29, "Cu", "Copper", "W + H", "0:0:0:0:0.5:0:0.5:0", "Electron Sink"),
    (30, "Zn", "Zinc", "Z", "0:0:1:0:0:0:0:0", "Enzyme Node"),
    (31, "Ga", "Gallium", "g", "0:1:0:0:0:0:0:0", "Low Melt Confinement"),
    (32, "Ge", "Germanium", "Z", "0:0:1:0:0:0:0:0", "Logic Ground"),
    (33, "As", "Arsenic", "q", "0:0:0:1:0:0:0:0", "Toxic Tension"),
    (34, "Se", "Selenium", "W", "0:0:0:0:1:0:0:0", "Antioxidant Sink"),
    (35, "Br", "Bromine", "ν", "0:0:0:0:0:1:0:0", "Heavy Ghost"),
    (36, "Kr", "Krypton", "γ", "0:0:0:0:0:0:0:1", "Stable Volume"),
    (37, "Rb", "Rubidium", "P+", "1:0:0:0:0:0:0:0", "Secondary Spark"),
    (38, "Sr", "Strontium", "Z", "0:0:1:0:0:0:0:0", "Bone Mimic"),
    (39, "Y", "Yttrium", "H + Z", "0:0:0.5:0:0:0:0.5:0", "Supercon Mass"),
    (40, "Zr", "Zirconium", "Z", "0:0:1:0:0:0:0:0", "Crystal Ground"),
    (41, "Nb", "Niobium", "W + Z", "0:0:0.5:0:0.5:0:0:0", "Weak Anchor"),
    (42, "Mo", "Molybdenum", "W", "0:0:0:0:1:0:0:0", "Enzyme Bridge"),
    (43, "Tc", "Technetium", "W", "0:0:0:0:1:0:0:0", "Decay Node"),
    (44, "Ru", "Ruthenium", "H", "0:0:0:0:0:0:1:0", "Mass Catalyst"),
    (45, "Rh", "Rhodium", "H + g", "0:0.5:0:0:0:0:0.5:0", "Bind Mass"),
    (46, "Pd", "Palladium", "H", "0:0:0:0:0:0:1:0", "Proton Sponge"),
    (47, "Ag", "Silver", "W + γ", "0:0.5:0:0:0.5:0:0:0", "Photon Guide"),
    (48, "Cd", "Cadmium", "Z", "0:0:1:0:0:0:0:0", "Toxic Lock"),
    (49, "In", "Indium", "g", "0:1:0:0:0:0:0:0", "Soft Bind"),
    (50, "Sn", "Tin", "Z", "0:0:1:0:0:0:0:0", "Corrosion Shield"),
    (51, "Sb", "Antimony", "q", "0:0:0:1:0:0:0:0", "Metalloid Tension"),
    (52, "Te", "Tellurium", "W", "0:0:0:0:1:0:0:0", "Weak Path"),
    (53, "I", "Iodine", "ν", "0:0:0:0:0:1:0:0", "Thyroid Ghost"),
    (54, "Xe", "Xenon", "γ", "0:0:0:0:0:0:0:1", "Void Release"),
    (55, "Cs", "Caesium", "P+", "1:0:0:0:0:0:0:0", "Time Spark"),
    (56, "Ba", "Barium", "Z", "0:0:1:0:0:0:0:0", "Mass Shield"),
    (57, "La", "Lanthanum", "H", "0:0:0:0:0:0:1:0", "Rare Earth Start"),
    (58, "Ce", "Cerium", "H + W", "0:0:0:0:0.5:0:0.5:0", "Redox Mass"),
    (59, "Pr", "Praseodymium", "H", "0:0:0:0:0:0:1:0", "Magnetic Mass"),
    (60, "Nd", "Neodymium", "H", "0:0:0:0:0:0:1:0", "Magnet Anchor"),
    (61, "Pm", "Promethium", "W", "0:0:0:0:1:0:0:0", "Decay Ghost"),
    (62, "Sm", "Samarium", "H", "0:0:0:0:0:0:1:0", "Mass Logic"),
    (63, "Eu", "Europium", "H + γ", "0:0.5:0:0:0:0:0.5:0", "Photon Mass"),
    (64, "Gd", "Gadolinium", "H", "0:0:0:0:0:0:1:0", "Contrast Mass"),
    (65, "Tb", "Terbium", "H", "0:0:0:0:0:0:1:0", "Luminous Mass"),
    (66, "Dy", "Dysprosium", "H", "0:0:0:0:0:0:1:0", "Coercive Mass"),
    (67, "Ho", "Holmium", "H", "0:0:0:0:0:0:1:0", "Moment Mass"),
    (68, "Er", "Erbium", "H + γ", "0:0.5:0:0:0:0:0.5:0", "Optical Mass"),
    (69, "Tm", "Thulium", "H", "0:0:0:0:0:0:1:0", "Rare Mass"),
    (70, "Yb", "Ytterbium", "H", "0:0:0:0:0:0:1:0", "Clock Mass"),
    (71, "Lu", "Lutetium", "H", "0:0:0:0:0:0:1:0", "End Rare Mass"),
    (72, "Hf", "Hafnium", "Z", "0:0:1:0:0:0:0:0", "Absorber Lock"),
    (73, "Ta", "Tantalum", "Z + H", "0:0:0.5:0:0:0:0.5:0", "Stable Anchor"),
    (74, "W", "Tungsten", "Z + W", "0:0:0.5:0:0.5:0:0:0", "Heat Bridge"),
    (75, "Re", "Rhenium", "H", "0:0:0:0:0:0:1:0", "Superalloy"),
    (76, "Os", "Osmium", "H", "0:0:0:0:0:0:1:0", "Density Max"),
    (77, "Ir", "Iridium", "H", "0:0:0:0:0:0:1:0", "Impact Mass"),
    (78, "Pt", "Platinum", "H", "0:0:0:0:0:0:1:0", "Inert Mass"),
    (79, "Au", "Gold", "H + γ", "0:0.5:0:0:0:0:0.5:0", "Solar Mass"),
    (80, "Hg", "Mercury", "H + ν", "0:0:0:0:0:0.5:0.5:0", "Liquid Ghost"),
    (81, "Tl", "Thallium", "g", "0:1:0:0:0:0:0:0", "Toxic Bind"),
    (82, "Pb", "Lead", "H + W", "0:0:0:0:0.5:0:0.5:0", "Mass Sink"),
    (83, "Bi", "Bismuth", "Z + W", "0:0:0.5:0:0.5:0:0:0", "Stable Decay"),
    (84, "Po", "Polonium", "W", "0:0:0:0:1:0:0:0", "Decay Spark"),
    (85, "At", "Astatine", "ν", "0:0:0:0:0:1:0:0", "Ghost Limit"),
    (86, "Rn", "Radon", "γ + ν", "0:0.5:0:0:0:0.5:0:0", "Decay Gas"),
    (87, "Fr", "Francium", "P+", "1:0:0:0:0:0:0:0", "Short Spark"),
    (88, "Ra", "Radium", "Z", "0:0:1:0:0:0:0:0", "Bone Sink"),
    (89, "Ac", "Actinium", "H", "0:0:0:0:0:0:1:0", "Heavy Mass"),
    (90, "Th", "Thorium", "W", "0:0:0:0:1:0:0:0", "Stable Energy"),
    (91, "Pa", "Protactinium", "W", "0:0:0:0:1:0:0:0", "Decay Bridge"),
    (92, "U", "Uranium", "W", "0:0:0:0:1:0:0:0", "Heavy Decay"),
    (93, "Np", "Neptunium", "W", "0:0:0:0:1:0:0:0", "Transuranic"),
    (94, "Pu", "Plutonium", "W", "0:0:0:0:1:0:0:0", "Fission Path"),
    (95, "Am", "Americium", "W + γ", "0:0.5:0:0:0.5:0:0:0", "Sensor Path"),
    (96, "Cm", "Curium", "W", "0:0:0:0:1:0:0:0", "Heavy Path"),
    (97, "Bk", "Berkelium", "W", "0:0:0:0:1:0:0:0", "Synthetic Path"),
    (98, "Cf", "Californium", "W + P+", "0.5:0:0:0:0.5:0:0:0", "Neutron Path"),
    (99, "Es", "Einsteinium", "W", "0:0:0:0:1:0:0:0", "Logic Path"),
    (100, "Fm", "Fermium", "W", "0:0:0:0:1:0:0:0", "Stat Path"),
    (101, "Md", "Mendelevium", "W", "0:0:0:0:1:0:0:0", "Table Path"),
    (102, "No", "Nobelium", "W", "0:0:0:0:1:0:0:0", "Final Path"),
    (103, "Lr", "Lawrencium", "W", "0:0:0:0:1:0:0:0", "Exit Path"),
    (104, "Rf", "Rutherfordium", "Z + H", "0:0:0.5:0:0:0:0.5:0", "Heavy Lock"),
    (105, "Db", "Dubnium", "Z", "0:0:1:0:0:0:0:0", "Stable Synth"),
    (106, "Sg", "Seaborgium", "W", "0:0:0:0:1:0:0:0", "Current Synth"),
    (107, "Bh", "Bohrium", "W", "0:0:0:0:1:0:0:0", "Bohr Path"),
    (108, "Hs", "Hassium", "H", "0:0:0:0:0:0:1:0", "Max Synth Mass"),
    (109, "Mt", "Meitnerium", "W", "0:0:0:0:1:0:0:0", "Fission Synth"),
    (110, "Ds", "Darmstadtium", "H", "0:0:0:0:0:0:1:0", "Ground Synth"),
    (111, "Rg", "Roentgenium", "H", "0:0:0:0:0:0:1:0", "X-ray Synth"),
    (112, "Cn", "Copernicium", "H + ν", "0:0:0:0:0:0.5:0.5:0", "Ghost Metal"),
    (113, "Nh", "Nihonium", "g", "0:1:0:0:0:0:0:0", "Japan Synth"),
    (114, "Fl", "Flerovium", "Z", "0:0:1:0:0:0:0:0", "Island Lock"),
    (115, "Mc", "Moscovium", "q", "0:0:0:1:0:0:0:0", "Moscow Tension"),
    (116, "Lv", "Livermorium", "W", "0:0:0:0:1:0:0:0", "Weak Limit"),
    (117, "Ts", "Tennessine", "ν", "0:0:0:0:0:1:0:0", "Halogen Limit"),
    (118, "Og", "Oganesson", "γ", "0:0:0:0:0:0:0:1", "Absolute Limit")
]

# 2. 128 Soil Classifications (WRB + Descriptors)
wrb_groups = [
    ("Histosols", "Z", "Organic Sink"), ("Anthrosols", "P+ + Z", "Human Noise"),
    ("Leptosols", "Z", "Foundation"), ("Vertisols", "H", "Confinement"),
    ("Fluvisols", "γ", "Flow"), ("Solonchaks", "q", "Salt Tension"),
    ("Gleysols", "W", "Anoxic Bridge"), ("Andisols", "P+ + W", "Volcanic Spark"),
    ("Podzols", "ν", "Fast Leakage"), ("Plinthosols", "H", "Mass Reservoir"),
    ("Ferralsols", "H", "Oxide Sink"), ("Solonetz", "q + g", "Tension Bind"),
    ("Planosols", "H + W", "Stagnant Mass"), ("Chernozems", "g + q + Z", "Homeostasis"),
    ("Kastanozems", "g + q", "Arid Balance"), ("Phaeozems", "q + Z", "Info Storage"),
    ("Umbrisols", "Z + ν", "Acid Storage"), ("Arenosols", "ν", "Ghost Flow"),
    ("Cambisols", "P+", "Transition"), ("Luvisols", "H + Z", "Translocation"),
    ("Lixisols", "ν + W", "Nutrient Leak"), ("Acrisols", "H + ν", "Leached Sink"),
    ("Alisols", "g + Z", "Confinement Lock"), ("Nitisols", "g", "Cohesion Bind"),
    ("Ferralsols", "H", "Final Oxide"), ("Durisols", "Z + H", "Hard Anchor"),
    ("Gypsisols", "q", "Gypsum Tension"), ("Calcisols", "Z", "Skeletal Ground"),
    ("Retisols", "ν + γ", "Ghost Void"), ("Stagnosols", "W", "Current Collapse"),
    ("Cryosols", "H", "Kinetic Lock"), ("Regosols", "γ", "Recent Vol")
]
descriptors = [("Haplic", "Normal"), ("Gleyic", "Wet"), ("Lithic", "Hard"), ("Voronic", "Dense")]

soil_mappings = []
for group, particle, desc in wrb_groups:
    for d_name, d_prop in descriptors:
        soil_mappings.append((f"{d_name} {group}", particle, f"{desc} ({d_prop})"))

# 3. 452 ROI Points (from CSV)
df_roi = pd.read_csv('ROI_452_SPIRAL_SORTED.csv')

def map_to_geography(x, y):
    if x >= 8:
        if y >= 14: return "Himalaya / Karakoram"
        if y >= 12: return "Pamir / Hindu Kush"
        if y >= 10: return "Ural Mountains"
        if y >= 8: return "Siberian Craton"
        if y >= 6: return "Deccan Traps"
        if y >= 4: return "Sahara Desert"
        if y >= 2: return "Australian Shield"
        return "Antarctic Ridge"
    else:
        if y >= 14: return "Japan / Kuril"
        if y >= 12: return "Fennoscandia"
        if y >= 10: return "Alps / Rhine"
        if y >= 8: return "Appalachian"
        if y >= 6: return "Amazon Basin"
        if y >= 4: return "Andes Mountains"
        if y >= 2: return "Nile Rift"
        return "Southern Ocean"

def get_vector(x, y):
    if x >= 8:
        if y >= 14: return "P+"
        if y >= 12: return "P+ + q"
        if y >= 10: return "H"
        if y >= 8: return "Z"
        if y >= 6: return "g"
        if y >= 4: return "q"
        if y >= 2: return "W"
        return "Z+H"
    else:
        if y >= 14: return "ν"
        if y >= 12: return "γ"
        if y >= 10: return "W"
        if y >= 8: return "ν + γ"
        if y >= 6: return "g + Z"
        if y >= 4: return "H + ν"
        if y >= 2: return "P+ + W"
        return "γ"

# Generate Markdown
content = []
content.append("# D3 UNIVERSAL EXHAUSTIVE MAPPING MATRIX\n")

content.append("## 1. 118 Chemical Elements: Exhaustive Individual Mapping\n")
content.append("| # | Element | Symbol | Particle Vector | Ratio | Logic |")
content.append("|---|---|---|---|---|---|")
for row in elements_raw:
    content.append(f"| {row[0]} | {row[2]} | {row[1]} | **{row[3]}** | {row[4]} | {row[5]} |")

content.append("\n## 2. 128 Soil Classifications: Exhaustive Mapping\n")
content.append("| # | Soil Classification | Dominant Particle | Vector Logic |")
content.append("|---|---|---|---|")
for i, (name, part, logic) in enumerate(soil_mappings, 1):
    content.append(f"| {i} | {name} | **{part}** | {logic} |")

content.append("\n## 3. 452 Body ROI Points: Exhaustive Mapping\n")
content.append("| idx | Coordinates | Geographic Site | Particle Vector | Role |")
content.append("|---|---|---|---|---|")
for _, row in df_roi.iterrows():
    geog = map_to_geography(row['x'], row['y'])
    vector = get_vector(row['x'], row['y'])
    content.append(f"| {int(row['idx'])} | ({row['x']:.2f}, {row['y']:.2f}) | **{geog}** | {vector} | ROI |")

# 4. Neurochemical Receptors & Earth Geography
receptors = [
    ("D2 (Dopamine)", "California / Silicon Valley", "High-Voltage Opportunity", "(9.25, 14.75)"),
    ("GABA-A", "British Isles / Nordic Craton", "Conservative Stability", "(8.0, 16.0)"),
    ("5-HT1B (Synchrotron)", "CERN / Geneva (Alps)", "Accelerator Loop", "(14.0, 13.0)"),
    ("Alpha-2 Adrenergic", "German Rhine Valley", "Industrial Efficiency", "(6.0, 10.0)"),
    ("Vasopressin V1a", "Near East / Levant", "Territorial Conflict", "(6.5, 5.0)"),
    ("Oxytocin", "Polynesian Volcanic Chain", "Connection Flux", "(8.0, 8.5)"),
    ("ERα (Estrogen)", "Kyoto / Nara (Japan)", "Understanding Gate", "(3.0, 15.0)"),
    ("NMDA (Glutamate)", "Himalayan Ridge", "Sudden Ignition", "(8.0, 12.0)"),
    ("μ-Opioid (MOR)", "Greek Archipelago", "Harmonic Reward", "(5.0, 10.0)"),
    ("V1b (Oxytocin Switch)", "East African Rift", "Origin Divergence", "(8.0, 0.1)")
]

content.append("\n## 4. Neurochemical Receptors & Earth Geography Mapping\n")
content.append("| Receptor | Geography | Rationale | Grid Coordinates |")
content.append("|---|---|---|---|")
for row in receptors:
    content.append(f"| {row[0]} | **{row[1]}** | {row[2]} | {row[3]} |")

with open('D3_UNIVERSAL_GEOLOGICAL_ELEMENTAL_MAPPING.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(content))

print("Exhaustive mapping file generated.")
