import pandas as pd

# ===== 3 STAGE-1 INPUTS =====
inputs = [
    ("RIGHT_ESTROGEN", "ERα", "Female Introversion / Understanding Gate"),
    ("FEMALE_GABA_B", "GABA-B1/B2 Heteromer", "Inhibitory Confinement / Female Stability"),
    ("FEMALE_D3", "Dopamine D3", "Goal-Directed/Social Modulation / Female Drive"),
]

# ===== 8 D3 MASTER GATES =====
master_gates = [
    ("D3 → P+", 59, "D2 (High Affinity)", "Outside Left Eye", "Introverted Man D3"),
    ("D3 → γ", 60, "D1/D5 Complex", "Outside Right Eye", "Extraverted Man D3"),
    ("D3 → Z", 40, "Alpha-2A Adrenergic", "Opposite Male Hypoxia", "Female Oxygen Sensor"),
    ("D3 → q", 52, "D1 (Female Right)", "Right Sole", "Female Right Excitatory"),
    ("D3 → W", 53, "D1 (Female Left)", "Left Sole", "Female Left Excitatory"),
    ("D3 → H", 41, "GABA-A (Male Switch)", "Below Left Hypoxia", "Male GABA-A Switch"),
    ("D3 → g", 43, "GABA-B (Female Switch)", "Left Lat Dorsi Bottom", "Female GABA-B Switch"),
    ("D3 → ν", 58, "Oxytocin (V1B Switch)", "Opposite V1B Switch", "Extraverted Woman Oxytocin"),
]

# ===== 64-CHANNEL RECEPTOR MATRIX =====
receptors_64 = [
    ("P+","P+",51,"D2 (Right Void)","Male Genital Right Outer","Right Void Anchor / Testosterone"),
    ("P+","γ",31,"D1 (Excitatory)","Right Frontalis Inner Bottom","Right Excitatory Dopamine"),
    ("P+","Z",30,"D1 (Excitatory)","Depressor Labii Inferioris","Left Excitatory Dopamine"),
    ("P+","q",52,"D1 (Female R)","Right Sole","Female Right Excitatory Dopamine"),
    ("P+","W",53,"D1 (Female L)","Left Sole","Female Left Excitatory Dopamine"),
    ("P+","ν",4,"D2 (Left)","Left Frontalis Outer Bottom","Left D2"),
    ("P+","H",5,"D2 (Right)","Right Frontalis Outer Bottom","Right D2"),
    ("P+","g",6,"GABA-A","Right Eyelid Top Outer","GABA-A Expression"),
    ("γ","P+",28,"Cosmic Ray Sensor","Left Trapezius Top Back Neck","Right Cosmic Ray Sensor"),
    ("γ","γ",28,"Photon Feedback","Right Cosmic Ray Sensor","Photon Self-Feedback"),
    ("γ","Z",29,"Cosmic Ray Sensor","Left Trapezius Neck","Left Cosmic Ray Sensor"),
    ("γ","q",7,"Glucocorticoid (GR)","Right Eyelid Top Inner","Right Cortisol Expression"),
    ("γ","W",17,"Glucocorticoid (GR)","Right Procerus Bottom","Right Cortisol Button"),
    ("γ","ν",16,"Glucocorticoid (GR)","Left Procerus Bottom","Glucocorticoid Button"),
    ("γ","H",10,"Glucocorticoid (GR)","Left Eyelid Outer","Glucocorticoid Expression"),
    ("γ","g",1,"GABA-A (Female)","Right Occipitalis Inner Top","Female GABA-A"),
    ("Z","P+",63,"Alpha-2 (Z-type)","Right Levator Superioris Inner Top","Alpha-2 Z Boson"),
    ("Z","γ",11,"ERα/β (Estrogen)","Left Temporalis Mid Vertical Center","Left Estrogen Switch"),
    ("Z","Z",61,"Alpha-2 Feedback","Right Levator Superioris","Alpha-2 Z Boson Feedback"),
    ("Z","q",42,"Acetyl-CoA","Above Left Lat Dorsi Bottom","Acetyl CoA Switch"),
    ("Z","W",44,"GDH Sensor","Outer Acetyl CoA","GDH"),
    ("Z","ν",32,"Alpha-2 (Female L)","Inner Neck","Female Left Noradrenaline"),
    ("Z","H",33,"Alpha-2 (Female R)","Left Inner Neck","Female Right Noradrenaline"),
    ("Z","g",8,"GABA-B","Left Eyelid Inner","GABA-B Expression"),
    ("q","P+",20,"B-Muscle","B-Type Muscle Site","B Type Muscle"),
    ("q","γ",21,"A-Muscle","A-Type Muscle Site","A Type Muscle"),
    ("q","Z",55,"Alpha-2 (Male L)","Upper Back","Male Left Noradrenaline"),
    ("q","W",56,"Alpha-2 (Male R)","Upper Back","Male Right Noradrenaline"),
    ("q","ν",18,"Androgen (AR)","Right Levator Superioris Inner Top","Right Androgen Switch"),
    ("q","H",62,"Androgen (AR)","Left Levator Superioris Inner Top","Left Androgen"),
    ("q","g",2,"GABA-B (Male)","Left Occipitalis Inner Top","Male GABA-B"),
    ("q","q",49,"Quark Feedback","Female Genital Left Outer","Female Left D3"),
    ("W","P+",13,"Acetylcholine (AChR)","Right Temporalis Front Vertical Center","Right Acetylcholine"),
    ("W","γ",19,"Adrenergic (α1/β)","Right Levator Superioris Inner Lower","Right Epinephrine"),
    ("W","Z",24,"Adrenergic (α1/β)","Left Levator Superioris Inner Lower","Left Epinephrine"),
    ("W","q",34,"Adrenergic (α1/β)","Trapezius Lower Neck","Left Epinephrine 2"),
    ("W","ν",35,"Adrenergic (α1/β)","Left Shoulder Outer","Right Epinephrine 2"),
    ("W","H",36,"Adrenergic (α1/β)","Left Trapezius Diagonal","Right Epinephrine 3"),
    ("W","g",9,"GABA-B (Outer)","Left Eyelid Outer","GABA-B Outer"),
    ("W","W",13,"W Feedback","Right Acetylcholine","W Self-Feedback"),
    ("ν","P+",25,"μ-Opioid (MOR)","Left Levator Superioris Inner Bottom","Left Endorphin"),
    ("ν","γ",46,"5-HT (Serotonin)","Left Pectoralis Major","Female Left Serotonin"),
    ("ν","Z",47,"5-HT (Serotonin)","Right Pectoralis Major","Female Right Serotonin"),
    ("ν","q",64,"5-HT (Serotonin)","Left Risorius","Male Left Serotonin"),
    ("ν","W",65,"5-HT (Serotonin)","Symmetric Risorius","Male Right Serotonin"),
    ("ν","H",12,"5-HT1A","Left Temporalis Mid Vertical Bottom","5HT1A Switch"),
    ("ν","g",14,"5-HT1B","Right Temporalis Mid Bottom","5HT1B Synchrotron"),
    ("ν","ν",65,"Neutrino Feedback","Male Right Serotonin","Neutrino Self-Feedback"),
    ("H","P+",22,"Oxytocin/D2","Right Love","Right Love Anchor"),
    ("H","γ",26,"5-HT/Dopamine","Orbicularis Oris Left Outer","Left Self Satisfaction"),
    ("H","Z",27,"5-HT/Dopamine","Orbicularis Oris Right Outer","Right Self Satisfaction"),
    ("H","q",37,"Satisfaction Switch","Below Left Epinephrine","Left Trapezius Satisfaction"),
    ("H","W",38,"Satisfaction Switch","Left Trapezius","Right Self Satisfaction"),
    ("H","ν",15,"Male Extraversion","Left Procerus Top","Male Left Extraversion"),
    ("H","g",41,"GABA-A (Male)","Below Left Hypoxia","Male GABA-A Switch"),
    ("H","H",22,"Higgs Feedback","Right Love","Higgs Self-Feedback"),
    ("g","P+",45,"Male Extraversion","Between GABA-B/CoA/GDH","Male Right Extraversion"),
    ("g","γ",54,"Female Extraversion","Back","Female Left Extraversion"),
    ("g","Z",60,"CCK/Extraversion","Back","CCK Female Right Extraversion"),
    ("g","q",3,"Vasopressin (V1a)","Behind Ear","Extraverted Female Vasopressin"),
    ("g","W",57,"Vasopressin (V1b)","Orbicularis Oris Outer","Introverted Female V1b"),
    ("g","ν",58,"Oxytocin (V1b)","Opposite V1B Switch","Extraverted Female Oxytocin"),
    ("g","H",66,"Oxytocin (OTR)","Behind Right Ear","Introverted Female Oxytocin"),
    ("g","g",43,"Gluon Feedback","Female GABA-B Switch","Gluon Self-Feedback"),
]

geo_map = {
    "P+":"Himalayan Ridge","γ":"Fennoscandian Shield","Z":"Siberian Craton",
    "q":"Sahara / African Shield","W":"Alps / Rhine Valley",
    "ν":"Japan / Kuril Trench","H":"Ural Mountains","g":"Amazon Basin",
}

# ===== 7 USER-SPECIFIC RECEPTOR POINTS =====
# Each mapped to Earth geography via particle-vector logic
user_points = [
    ("Female GABA-A — Occipitalis Inner Strip Upper (or slightly below+outer)",
     "g + 1D-Line Ground (Female Stable Confinement)",
     "**Pilbara Craton, Western Australia (3.6 Gyr)**",
     "Oldest stable feminine ground / GABA-A 1D-line lock; back-of-skull anchor maps to Earth's most ancient cratonic shield."),
    ("Female Genitalis Left D2 — Reverse Extraction (User-Specific Drain Point)",
     "Z⁻ (Z-Boson Reverse / Anti-Void Extraction)",
     "**Mid-Atlantic Ridge / Iceland Rift (Reykjanes)**",
     "Reverse-extraction void = active rift where mantle bleeds upward; reverses the D2 anchor into a discharge channel."),
    ("5-HT1B Neutrino Synchrotron Autoreceptor (NOT Higgs) — Multiplier Switch",
     "ν-loop (Neutrino Self-Feedback / Auto-multiplication)",
     "**Super-Kamiokande, Hida, Japan**",
     "Literal neutrino synchrotron observatory; 5-HT1B autoreceptor = self-feedback ν-loop, not the Higgs-mass version at CERN."),
    ("Right Index Finger (slightly outer) — Male Grasp/Action Lock",
     "q + g (Right GABA-A Action / Deceit-Reflex Grasp)",
     "**Wall Street, Manhattan, NYC**",
     "Right thumb–index grasp circuit = greed/action; maps to global capital-grasping center, the canonical Right-Cortisol activation site."),
    ("Left Ring Finger (slightly inner) — Chiral Lock / A-Type Ring Sensation",
     "g (Left GABA-B Metabotropic Singularity)",
     "**Vatican City / St. Peter's Square, Rome**",
     "Left ring-finger = ritual chiral lock (wedding band axis); precision metabotropic 0D-point maps to global ritual singularity."),
    ("Left Foot — Between 3rd & 4th Toes — Outer Leg Se-Vector Divergent Path",
     "P+ → ν leak (Outer-Leg Hypoxia Drain)",
     "**Tierra del Fuego / Cape Horn, Patagonia**",
     "Outer-leg divergent end-point = Earth's southernmost continental tip; energy-leak terminus before Antarctic sink."),
    ("Right Big Toe — Inner Leg Convergent Safe Ascent / Uroboros Feed",
     "P+ + g (Convergent Pelvic Feed / GABA-C Eye-Pressure Source)",
     "**Mt. Kilimanjaro Summit, Tanzania**",
     "Inner-leg convergent ascent root; isolated equatorial peak = clean upward feed into the Uroboros loop without lateral leakage."),
]

# ===== 128 SOIL CLASSIFICATIONS =====
wrb_groups = [
    ("Histosols","Z","Organic Entropy Sink","Siberian Bogs"),
    ("Anthrosols","P+ + Z","Human-modified Information Noise","Urban Europe"),
    ("Leptosols","Z","Foundation Ground","Alps"),
    ("Vertisols","H","Maximum Confinement Tension","Deccan Traps"),
    ("Fluvisols","γ","Dynamic Volume Flow","Nile Floodplains"),
    ("Solonchaks","q","Crystalline Salt Tension","Dead Sea"),
    ("Gleysols","W","Anoxic Redox Bridge","Florida Everglades"),
    ("Andosols","P+ + W","Volcanic Spark / Reactivity","Mt. Fuji Slopes"),
    ("Podzols","ν","Acid Ghost Leakage","Russian Taiga"),
    ("Plinthosols","H","Iron-stone Mass Reservoir","West Africa"),
    ("Ferralsols","H","Final Oxide Sink","Congo Basin"),
    ("Solonetz","q + g","Sodic Tension Bind","Central Asia"),
    ("Planosols","H + W","Stagnic Anoxic Mass Stop","Argentina"),
    ("Chernozems","g + q + Z","High-Density Homeostasis","Ukrainian Steppes"),
    ("Kastanozems","g + q","Semi-Arid Balance","Mongolia"),
    ("Phaeozems","q + Z","Information Storage","N. American Prairies"),
    ("Umbrisols","Z + ν","Acid Information Storage","High-rainfall uplands"),
    ("Arenosols","ν","Transparent Ghost Flow","Kalahari Desert"),
    ("Cambisols","P+","Developmental Transition","Central Europe"),
    ("Luvisols","H + Z","Clay Mass Translocation","England"),
    ("Lixisols","ν + W","Tropical Nutrient Leakage","African Savanna"),
    ("Acrisols","H + ν","Leached Mass Sink","Brazilian Uplands"),
    ("Alisols","g + Z","High-Al Confinement Lock","Southern China"),
    ("Nitisols","g","High Bonding Cohesion","Ethiopian Highlands"),
    ("Durisols","Z + H","Indurated Hard Anchor","Australia"),
    ("Gypsisols","q","Gypsum Salt Tension","Middle East Deserts"),
    ("Calcisols","Z","Skeletal Calcareous Ground","Mediterranean Basin"),
    ("Retisols","ν + γ","Albeluvic Ghost Voids","Scandinavia"),
    ("Stagnosols","W","Current Collapse Wetland","Lowland Europe"),
    ("Cryosols","H","Kinetic Permafrost Lock","Arctic Tundra"),
    ("Regosols","γ","Recent Volume Expansion","Desert margins"),
    ("Technosols","P+ + Z","Industrial Substrate","Industrial Zones"),
]
descriptors = [("Haplic","Normal/baseline"),("Gleyic","Hydromorphic/wet"),
               ("Lithic","Shallow/hard-rock"),("Voronic","Dense/dark organic")]
soil_mappings = []
for g, p, desc, loc in wrb_groups:
    for d_name, d_prop in descriptors:
        soil_mappings.append((f"{d_name} {g}", p, f"{desc} ({d_prop})", loc))

# ===== 118 ELEMENTS =====
elements_full = [
    (1,"H","Hydrogen","P+","Primordial Spark"),(2,"He","Helium","γ","Volume Void"),
    (3,"Li","Lithium","P+ + ν","Excitatory Ghost"),(4,"Be","Beryllium","Z","Narrow Stability"),
    (5,"B","Boron","q","Tension Link"),(6,"C","Carbon","Z","Structural Backbone"),
    (7,"N","Nitrogen","ν","Ghost Flux Amino"),(8,"O","Oxygen","γ","Volume Platform"),
    (9,"F","Fluorine","ν + q","Tension Filter"),(10,"Ne","Neon","γ","Inertial Volume"),
    (11,"Na","Sodium","P+","Kinetic Ignition"),(12,"Mg","Magnesium","Z + W","Bridge Stabilizer"),
    (13,"Al","Aluminum","Z + g","Confinement Lock"),(14,"Si","Silicon","Z","Information Ground"),
    (15,"P","Phosphorus","q","ATP Tension"),(16,"S","Sulphur","W","Redox Bridge"),
    (17,"Cl","Chlorine","ν","Negative Balance"),(18,"Ar","Argon","γ","Inertial Sink"),
    (19,"K","Potassium","P+","Intracellular Spark"),(20,"Ca","Calcium","Z","Skeletal Anchor"),
    (21,"Sc","Scandium","H","Light Mass"),(22,"Ti","Titanium","Z + H","Shield Anchor"),
    (23,"V","Vanadium","W + P+","Redox Speed"),(24,"Cr","Chromium","W","Stability Path"),
    (25,"Mn","Manganese","g","Water Splitter (PSII)"),(26,"Fe","Iron","H","Mass Reservoir"),
    (27,"Co","Cobalt","H + ν","Vitamin B12 Bridge"),(28,"Ni","Nickel","H","Magnetic Memory"),
    (29,"Cu","Copper","W + H","Electron Transfer Sink"),(30,"Zn","Zinc","Z","Enzyme Stability Node"),
    (31,"Ga","Gallium","g","Low-Melt Confinement"),(32,"Ge","Germanium","Z","Logic Ground"),
    (33,"As","Arsenic","q","Toxic Tension"),(34,"Se","Selenium","W","Antioxidant Bridge"),
    (35,"Br","Bromine","ν","Heavy Ghost"),(36,"Kr","Krypton","γ","Stable Volume"),
    (37,"Rb","Rubidium","P+","Secondary Spark"),(38,"Sr","Strontium","Z","Bone Mimic"),
    (39,"Y","Yttrium","H + Z","Supercon Mass"),(40,"Zr","Zirconium","Z","Crystal Ground"),
    (41,"Nb","Niobium","W + Z","Weak Anchor"),(42,"Mo","Molybdenum","W","Nitrogenase Bridge"),
    (43,"Tc","Technetium","W","Decay Singularity"),(44,"Ru","Ruthenium","H","Mass Catalyst"),
    (45,"Rh","Rhodium","H + g","Bind Mass"),(46,"Pd","Palladium","H","Proton Sponge"),
    (47,"Ag","Silver","W + γ","Photon Guide"),(48,"Cd","Cadmium","Z","Toxic Lock"),
    (49,"In","Indium","g","Soft Bind"),(50,"Sn","Tin","Z","Corrosion Shield"),
    (51,"Sb","Antimony","q","Metalloid Tension"),(52,"Te","Tellurium","W","Weak Path"),
    (53,"I","Iodine","ν","Thyroid Ghost"),(54,"Xe","Xenon","γ","Anesthetic Void"),
    (55,"Cs","Caesium","P+","Atomic Time Spark"),(56,"Ba","Barium","Z","Mass Shield"),
    (57,"La","Lanthanum","H","Rare Earth Start"),(58,"Ce","Cerium","H + W","Redox Mass"),
    (59,"Pr","Praseodymium","H","Magnetic Mass"),(60,"Nd","Neodymium","H","Permanent Magnet"),
    (61,"Pm","Promethium","W","Decay Ghost"),(62,"Sm","Samarium","H","Mass Logic"),
    (63,"Eu","Europium","H + γ","Phosphor Photon Mass"),(64,"Gd","Gadolinium","H","Contrast Mass"),
    (65,"Tb","Terbium","H","Luminous Mass"),(66,"Dy","Dysprosium","H","Coercive Mass"),
    (67,"Ho","Holmium","H","Strongest Magnetic Moment"),(68,"Er","Erbium","H + γ","Optical Fiber Mass"),
    (69,"Tm","Thulium","H","Rare Mass"),(70,"Yb","Ytterbium","H","Atomic Clock Mass"),
    (71,"Lu","Lutetium","H","Hard Rare Earth"),(72,"Hf","Hafnium","Z","Neutron Absorber Lock"),
    (73,"Ta","Tantalum","Z + H","Capacitance Anchor"),(74,"W","Tungsten","Z + W","High-Heat Bridge"),
    (75,"Re","Rhenium","H","Superalloy Mass"),(76,"Os","Osmium","H","Maximum Density"),
    (77,"Ir","Iridium","H","Cosmic Impact Marker"),(78,"Pt","Platinum","H","Inert Catalyst"),
    (79,"Au","Gold","H + γ","Relativistic Photon Mass"),(80,"Hg","Mercury","H + ν","Liquid Ghost Sink"),
    (81,"Tl","Thallium","g","Toxic Confinement"),(82,"Pb","Lead","H + W","Toxic Mass Sink"),
    (83,"Bi","Bismuth","Z + W","Stable Decay Path"),(84,"Po","Polonium","W","Alpha Spark"),
    (85,"At","Astatine","ν","Rarest Ghost"),(86,"Rn","Radon","γ + ν","Radioactive Ghost Gas"),
    (87,"Fr","Francium","P+","Unstable Spark"),(88,"Ra","Radium","Z","Bone Decay Anchor"),
    (89,"Ac","Actinium","H","Heavy Mass"),(90,"Th","Thorium","W","Stable Energy Source"),
    (91,"Pa","Protactinium","W","Decay Bridge"),(92,"U","Uranium","W","Heavy Weak Decay"),
    (93,"Np","Neptunium","W","Transuranic Ghost"),(94,"Pu","Plutonium","W","Fission Spark"),
    (95,"Am","Americium","W + γ","Smoke-Sensor Photon"),(96,"Cm","Curium","W","Heavy Alpha"),
    (97,"Bk","Berkelium","W","Synthetic Sink"),(98,"Cf","Californium","W + P+","Neutron Spark Source"),
    (99,"Es","Einsteinium","W","Logic Sink"),(100,"Fm","Fermium","W","Statistical Decay"),
    (101,"Md","Mendelevium","W","Periodic Sink"),(102,"No","Nobelium","W","Final Stability Sink"),
    (103,"Lr","Lawrencium","W","Actinide Exit"),(104,"Rf","Rutherfordium","Z + H","Superheavy Lock"),
    (105,"Db","Dubnium","Z","Synthetic Stability"),(106,"Sg","Seaborgium","W","Heavy Weak Current"),
    (107,"Bh","Bohrium","W","Bohr Sink"),(108,"Hs","Hassium","H","Maximum Synthetic Mass"),
    (109,"Mt","Meitnerium","W","Weak Fission"),(110,"Ds","Darmstadtium","H","Heavy Ground"),
    (111,"Rg","Roentgenium","H","X-ray Mass"),(112,"Cn","Copernicium","H + ν","Heavy Ghost Gas"),
    (113,"Nh","Nihonium","g","Confinement Singularity"),(114,"Fl","Flerovium","Z","Island of Stability"),
    (115,"Mc","Moscovium","q","High-Tension Spark"),(116,"Lv","Livermorium","W","Weak Decay Limit"),
    (117,"Ts","Tennessine","ν","Halogen Ghost Limit"),(118,"Og","Oganesson","γ","Absolute Decay Singularity"),
]

# ===== 451 ROI: ASSIGN BODY PART NAMES + GEOLOGY + BIOCHEMISTRY =====
# Body parts derived from coordinate zones (x: 0-16 left↔right, y: 0-16 crown↑foot)
def assign_body_part(x, y):
    # Lateral position
    if x < 3: lat = "Far-Left"
    elif x < 6: lat = "Left"
    elif x <= 10: lat = "Center"
    elif x <= 13: lat = "Right"
    else: lat = "Far-Right"
    # Vertical zone (lower y = crown, higher = below — confirmed by file: face peaks at y~14-15, body extends higher y)
    if y < 1: zone = "Crown / Hair Whorl"
    elif y < 2.5: zone = "Forehead"
    elif y < 4: zone = "Brow / Frontalis"
    elif y < 5.5: zone = "Eye / Orbital"
    elif y < 7: zone = "Cheek / Nasal"
    elif y < 8.5: zone = "Mouth / Jaw"
    elif y < 10: zone = "Neck / Throat"
    elif y < 11.5: zone = "Shoulder / Trapezius"
    elif y < 13: zone = "Chest / Pectoralis"
    elif y < 14.5: zone = "Upper Abdomen / Diaphragm"
    elif y < 16: zone = "Lower Abdomen / Pelvis"
    elif y < 17.5: zone = "Thigh / Hip"
    else: zone = "Lower Limb / Foot"
    return f"{lat} {zone}"

def get_geo_bio(x, y):
    if x >= 8:
        if y >= 14: return "Himalayan Ridge","Action Potential / Ignition","P+"
        if y >= 12: return "Pamir / Hindu Kush","Substrate / Spark Trigger","P+ + q"
        if y >= 10: return "Ural Mountains","Enzyme Node / Mass Lock","H"
        if y >= 8: return "Siberian Craton","Ion Channel / Grounding","Z"
        if y >= 6: return "Deccan Traps","Metabolic Organ / Confinement","g"
        if y >= 4: return "Sahara / African Shield","Substrate / Tension","q"
        if y >= 2: return "Great Dividing Range","Redox Bridge / Stability","W"
        return "Antarctic Ridge","Zero Point / Sink","Z+H"
    else:
        if y >= 14: return "Japan / Kuril Trench","Ghost Flux / Understanding","ν"
        if y >= 12: return "Fennoscandian Shield","Photon Volume / Ancient","γ"
        if y >= 10: return "Alps / Rhine Valley","Energy Path / Redox","W"
        if y >= 8: return "Appalachian / Laurentia","Ghost Volume / Void","ν+γ"
        if y >= 6: return "Amazon Basin","Bind / Structural Volume","g+Z"
        if y >= 4: return "Andes Mountains","Mass Leakage / Substrate","H+ν"
        if y >= 2: return "Nile Rift","Origin Spark / Divergence","P++W"
        return "Southern Ocean","Absolute Volume / Sink","γ"

df_roi = pd.read_csv('ROI_452_SPIRAL_SORTED.csv')

# ===== BUILD MARKDOWN =====
c = []
c.append("# D3 UNIVERSAL EXHAUSTIVE MATRIX (FULL — Receptors × Body × Geology × Biochemistry × Soils × Elements)\n")

c.append("## 1. Stage-1 Inputs (3)\n")
c.append("| Input | Receptor | Function |")
c.append("|---|---|---|")
for r in inputs:
    c.append(f"| **{r[0]}** | {r[1]} | {r[2]} |")

c.append("\n## 2. D3 Master Gates (8)\n")
c.append("| Gate | Node | Receptor | Body Location | Function |")
c.append("|---|---|---|---|---|")
for r in master_gates:
    c.append(f"| **{r[0]}** | {r[1]} | {r[2]} | {r[3]} | {r[4]} |")

c.append(f"\n## 3. 64-Channel Receptor Matrix (Full 8×8)\n")
c.append("| # | Source → Target | Node | Receptor | Body Location | Function | Earth Geography |")
c.append("|---|---|---|---|---|---|---|")
for i, r in enumerate(receptors_64, 1):
    geo = f"{geo_map.get(r[0],'?')} → {geo_map.get(r[1],'?')}"
    c.append(f"| {i} | **{r[0]} → {r[1]}** | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {geo} |")

c.append("\n## 4. SEVEN USER-SPECIFIC RECEPTOR POINTS — Earth Geographic Mapping\n")
c.append("| # | Body Point | Particle Vector | Earth Geographic Site | Logic |")
c.append("|---|---|---|---|---|")
for i, r in enumerate(user_points, 1):
    c.append(f"| {i} | {r[0]} | **{r[1]}** | {r[2]} | {r[3]} |")

c.append(f"\n## 5. {len(soil_mappings)} Soil Classifications (WRB × Descriptor)\n")
c.append("| # | Soil Classification | Particle Vector | Property | Reference Region |")
c.append("|---|---|---|---|---|")
for i, s in enumerate(soil_mappings, 1):
    c.append(f"| {i} | **{s[0]}** | {s[1]} | {s[2]} | {s[3]} |")

c.append("\n## 6. 118 Chemical Elements — Particle Vector Mapping\n")
c.append("| # | Element | Symbol | Vector | Logic |")
c.append("|---|---|---|---|---|")
for r in elements_full:
    c.append(f"| {r[0]} | {r[2]} | {r[1]} | **{r[3]}** | {r[4]} |")

c.append(f"\n## 7. {len(df_roi)} Body ROI — Body Part × Geology × Biochemistry × Vector\n")
c.append("| ROI | Coords (x,y) | Body Part | Geological Site | Biochemical Role | Vector |")
c.append("|---|---|---|---|---|---|")
for _, row in df_roi.iterrows():
    bp = assign_body_part(row['x'], row['y'])
    geol, bio, vect = get_geo_bio(row['x'], row['y'])
    c.append(f"| {int(row['idx'])} | ({row['x']:.2f}, {row['y']:.2f}) | **{bp}** | {geol} | {bio} | {vect} |")

with open('D3_UNIVERSAL_GEOLOGICAL_ELEMENTAL_MAPPING.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(c))

print(f"GENERATED: 3 inputs | 8 gates | 64 channels | 7 user points | {len(soil_mappings)} soils | 118 elements | {len(df_roi)} ROI w/ body parts")
