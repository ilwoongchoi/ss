#!/usr/bin/env python3
"""Map ALL activities/professions/music/sports from user's extended list to 128 profiles."""
from particle_to_8d import particles_to_dims, MBTI_TYPES, BLOOD_TYPES, GENDERS

PROFILES = [f"{mbti}_{g}_{b}" for mbti in MBTI_TYPES for g in GENDERS for b in BLOOD_TYPES]

# ===== PROFESSIONS =====
PROFESSIONS = {
    # Computational / parametric design
    "Computational_Designer":               {"p":3,"s":3,"h":3,"d":2,"r":3,"gamma":2,"g":3,"nu":3},
    "Parametric_Architect":                 {"p":3,"s":3,"h":2,"d":2,"r":2,"gamma":3,"g":3,"nu":3},
    "Computational_Architect":              {"p":3,"s":2,"h":2,"d":2,"r":2,"gamma":3,"g":4,"nu":3},
    # Ecology / environment
    "Landscape_Ecologist":                  {"p":2,"s":2,"h":2,"d":1,"r":2,"gamma":3,"g":2,"nu":4},
    "Ecological_Designer":                  {"p":2,"s":3,"h":3,"d":1,"r":1,"gamma":3,"g":2,"nu":3},
    "Geospatial_Data_Scientist":            {"p":3,"s":3,"h":1,"d":2,"r":2,"gamma":3,"g":3,"nu":3},
    "Remote_Sensing_Specialist":            {"p":4,"s":3,"h":1,"d":3,"r":2,"gamma":2,"g":3,"nu":3},
    "Urban_Systems_Designer":               {"p":3,"s":2,"h":2,"d":2,"r":2,"gamma":3,"g":4,"nu":3},
    "Environmental_Modeller":               {"p":3,"s":2,"h":1,"d":2,"r":2,"gamma":3,"g":3,"nu":4},
    "Hydrological_Modeller":                {"p":4,"s":2,"h":1,"d":3,"r":3,"gamma":3,"g":3,"nu":3},
    "Climate_Risk_Modeller":                {"p":4,"s":2,"h":1,"d":3,"r":2,"gamma":2,"g":3,"nu":4},
    # Digital fabrication / robotics
    "Digital_Fabrication_Designer":         {"p":3,"s":4,"h":2,"d":2,"r":3,"gamma":2,"g":3,"nu":2},
    "Robotics_Designer":                    {"p":3,"s":2,"h":2,"d":3,"r":3,"gamma":2,"g":4,"nu":3},
    "Mechatronics_Prototype_Engineer":      {"p":3,"s":2,"h":1,"d":3,"r":4,"gamma":2,"g":4,"nu":2},
    "Physical_Computing_Designer":          {"p":3,"s":3,"h":2,"d":2,"r":3,"gamma":2,"g":3,"nu":2},
    # Creative tech
    "Creative_Technologist":                {"p":2,"s":3,"h":3,"d":2,"r":3,"gamma":2,"g":2,"nu":3},
    "Interaction_Designer":                 {"p":2,"s":4,"h":3,"d":1,"r":2,"gamma":2,"g":2,"nu":2},
    "Generative_Design_Engineer":           {"p":2,"s":3,"h":3,"d":2,"r":2,"gamma":2,"g":3,"nu":4},
    # Game / simulation
    "Procedural_World_Designer":            {"p":2,"s":3,"h":3,"d":2,"r":2,"gamma":3,"g":3,"nu":4},
    "Technical_Artist":                     {"p":3,"s":5,"h":2,"d":2,"r":3,"gamma":2,"g":2,"nu":1},
    "Environment_Artist":                   {"p":1,"s":5,"h":3,"d":1,"r":2,"gamma":3,"g":1,"nu":2},
    "Level_Designer":                       {"p":2,"s":4,"h":3,"d":2,"r":2,"gamma":4,"g":2,"nu":2},
    "Simulation_Designer":                  {"p":3,"s":2,"h":2,"d":3,"r":2,"gamma":3,"g":3,"nu":3},
    "Systems_Designer":                     {"p":3,"s":2,"h":2,"d":3,"r":2,"gamma":2,"g":4,"nu":3},
    # Audio / visual
    "Technical_Sound_Designer":             {"p":3,"s":2,"h":3,"d":2,"r":3,"gamma":3,"g":2,"nu":2},
    "Spatial_Audio_Designer":               {"p":2,"s":3,"h":3,"d":2,"r":2,"gamma":5,"g":2,"nu":3},
    "Lighting_Programmer":                  {"p":4,"s":4,"h":2,"d":2,"r":3,"gamma":3,"g":2,"nu":1},
    "Architectural_Lighting_Designer":      {"p":2,"s":4,"h":3,"d":1,"r":2,"gamma":4,"g":2,"nu":2},
    # Exhibition / theme park
    "Exhibition_Designer":                  {"p":2,"s":4,"h":4,"d":1,"r":2,"gamma":3,"g":2,"nu":2},
    "Museum_Exhibition_Technologist":       {"p":3,"s":3,"h":2,"d":2,"r":3,"gamma":2,"g":3,"nu":2},
    "Scenographer":                         {"p":2,"s":4,"h":4,"d":1,"r":2,"gamma":4,"g":2,"nu":3},
    "Set_Designer":                         {"p":2,"s":4,"h":4,"d":1,"r":2,"gamma":4,"g":2,"nu":2},
    "ThemePark_Systems_Designer":           {"p":3,"s":3,"h":3,"d":2,"r":2,"gamma":3,"g":4,"nu":2},
    "Ride_Systems_Engineer":                {"p":4,"s":2,"h":1,"d":4,"r":3,"gamma":2,"g":4,"nu":2},
    # Conservation / archaeology
    "Conservation_Technologist":            {"p":3,"s":3,"h":2,"d":2,"r":2,"gamma":2,"g":2,"nu":3},
    "Digital_Archaeologist":                {"p":3,"s":3,"h":2,"d":2,"r":2,"gamma":3,"g":2,"nu":3},
    "Photogrammetry_Specialist":            {"p":4,"s":4,"h":1,"d":2,"r":3,"gamma":3,"g":2,"nu":2},
    "3D_Scanning_Specialist":               {"p":4,"s":4,"h":1,"d":2,"r":3,"gamma":2,"g":2,"nu":2},
    "Terrain_Modeller":                     {"p":2,"s":4,"h":2,"d":2,"r":2,"gamma":3,"g":2,"nu":3},
    "Cartographic_Designer":                {"p":3,"s":4,"h":2,"d":2,"r":2,"gamma":3,"g":2,"nu":2},
    # Scientific
    "Scientific_Illustrator":               {"p":3,"s":5,"h":3,"d":2,"r":2,"gamma":2,"g":1,"nu":2},
    "Scientific_Visualisation_Designer":    {"p":3,"s":5,"h":2,"d":2,"r":2,"gamma":3,"g":2,"nu":2},
    "Biomimicry_Designer":                  {"p":2,"s":3,"h":3,"d":2,"r":2,"gamma":2,"g":2,"nu":4},
    "Biomaterials_Designer":                {"p":3,"s":3,"h":3,"d":2,"r":2,"gamma":2,"g":2,"nu":3},
    "Restoration_Ecologist":                {"p":2,"s":2,"h":2,"d":1,"r":2,"gamma":3,"g":2,"nu":4},
    "Peatland_Scientist":                   {"p":3,"s":2,"h":1,"d":2,"r":2,"gamma":2,"g":2,"nu":4},
    "Soil_Modeller":                        {"p":3,"s":2,"h":1,"d":2,"r":2,"gamma":2,"g":3,"nu":4},
    "Coastal_Systems_Engineer":             {"p":3,"s":2,"h":1,"d":3,"r":3,"gamma":3,"g":3,"nu":3},
    "River_Restoration_Designer":           {"p":2,"s":3,"h":2,"d":2,"r":2,"gamma":4,"g":2,"nu":3},
    "Environmental_Infrastructure_Designer":{"p":3,"s":2,"h":2,"d":2,"r":2,"gamma":3,"g":4,"nu":3},
}

# ===== CREATIVE ACTIVITIES / HOBBIES =====
CREATIVE = {
    # Spatial / constructed
    "Architectural_Modelmaking":            {"p":3,"s":4,"h":2,"d":1,"r":2,"gamma":3,"g":2,"nu":1},
    "Architectural_Paper_Engineering":      {"p":3,"s":4,"h":3,"d":1,"r":2,"gamma":3,"g":2,"nu":1},
    "Kinetic_Architecture_Models":          {"p":2,"s":3,"h":3,"d":2,"r":2,"gamma":3,"g":3,"nu":2},
    "Miniature_Urbanism":                   {"p":2,"s":4,"h":3,"d":1,"r":2,"gamma":3,"g":2,"nu":2},
    "Terrain_Modelling":                    {"p":2,"s":4,"h":2,"d":1,"r":2,"gamma":3,"g":2,"nu":2},
    # Generative
    "Algorithmic_Weaving":                  {"p":2,"s":3,"h":3,"d":1,"r":2,"gamma":2,"g":3,"nu":3},
    "Generative_Typography":                {"p":2,"s":4,"h":3,"d":1,"r":2,"gamma":1,"g":2,"nu":3},
    "Generative_Ceramics":                  {"p":2,"s":3,"h":3,"d":1,"r":2,"gamma":2,"g":2,"nu":3},
    "Procedural_Texture_Creation":          {"p":2,"s":4,"h":2,"d":1,"r":3,"gamma":2,"g":2,"nu":3},
    "Generative_Landscape_Design":          {"p":2,"s":3,"h":3,"d":1,"r":2,"gamma":3,"g":2,"nu":4},
    # Material
    "Bookbinding":                          {"p":3,"s":3,"h":2,"d":1,"r":2,"gamma":1,"g":2,"nu":1},
    "Marquetry":                            {"p":4,"s":4,"h":2,"d":1,"r":2,"gamma":2,"g":1,"nu":1},
    "Intarsia":                             {"p":4,"s":4,"h":2,"d":1,"r":2,"gamma":2,"g":1,"nu":1},
    "Basketry":                             {"p":2,"s":3,"h":3,"d":1,"r":2,"gamma":2,"g":1,"nu":2},
    "Wire_Sculpture":                       {"p":2,"s":3,"h":3,"d":1,"r":2,"gamma":3,"g":1,"nu":2},
    "Bone_Wood_Inlay":                      {"p":4,"s":4,"h":2,"d":1,"r":2,"gamma":2,"g":1,"nu":1},
    "Glass_Fusing":                         {"p":2,"s":4,"h":3,"d":1,"r":2,"gamma":2,"g":1,"nu":2},
    # Image / light
    "Camera_Obscura":                       {"p":2,"s":4,"h":3,"d":1,"r":1,"gamma":4,"g":1,"nu":2},
    "Lumen_Printing":                       {"p":1,"s":4,"h":4,"d":1,"r":1,"gamma":2,"g":1,"nu":3},
    "Photogrammetry_Art":                   {"p":3,"s":4,"h":2,"d":2,"r":2,"gamma":3,"g":2,"nu":2},
    "Projection_Sculpture":                 {"p":2,"s":4,"h":4,"d":1,"r":2,"gamma":4,"g":2,"nu":2},
    "Shadow_Art_Installation":              {"p":1,"s":4,"h":4,"d":1,"r":1,"gamma":4,"g":1,"nu":3},
    "Slit_Scan_Photography":                {"p":3,"s":4,"h":2,"d":2,"r":2,"gamma":3,"g":2,"nu":2},
    # Nature
    "Botanical_Cyanotype":                  {"p":2,"s":4,"h":3,"d":1,"r":1,"gamma":2,"g":1,"nu":3},
    "Moss_Art":                             {"p":1,"s":3,"h":3,"d":1,"r":1,"gamma":2,"g":1,"nu":3},
    "Miniature_Ecosystem_Construction":     {"p":2,"s":3,"h":3,"d":1,"r":1,"gamma":3,"g":2,"nu":3},
    "Natural_Dye_Printing":                 {"p":2,"s":3,"h":3,"d":1,"r":2,"gamma":2,"g":1,"nu":2},
    "Pressed_Plant_Composition":            {"p":2,"s":4,"h":3,"d":1,"r":1,"gamma":2,"g":1,"nu":2},
    # Spatial storytelling
    "Architectural_Storytelling":           {"p":1,"s":3,"h":4,"d":1,"r":1,"gamma":3,"g":1,"nu":3},
    "Miniature_Film_Sets":                  {"p":2,"s":4,"h":3,"d":1,"r":2,"gamma":3,"g":2,"nu":2},
    "Speculative_City_Modelling":           {"p":2,"s":3,"h":4,"d":1,"r":2,"gamma":3,"g":2,"nu":3},
    "Alternate_History_Mapmaking":          {"p":2,"s":3,"h":4,"d":1,"r":2,"gamma":3,"g":2,"nu":3},
    # Mechanical
    "Automata_Making":                      {"p":2,"s":3,"h":3,"d":2,"r":3,"gamma":2,"g":3,"nu":2},
    "Mechanical_Sculpture":                 {"p":2,"s":3,"h":3,"d":2,"r":2,"gamma":3,"g":3,"nu":2},
    "Kinetic_Mobiles":                      {"p":1,"s":3,"h":3,"d":1,"r":2,"gamma":4,"g":2,"nu":2},
    "Clockwork_Modelling":                  {"p":4,"s":3,"h":2,"d":2,"r":3,"gamma":2,"g":3,"nu":1},
    "Mechanical_Toy_Design":                {"p":2,"s":3,"h":3,"d":2,"r":3,"gamma":2,"g":3,"nu":2},
    # Digital/physical
    "LaserCut_Topographic_Art":             {"p":3,"s":4,"h":2,"d":2,"r":3,"gamma":3,"g":2,"nu":1},
    "CNC_Relief_Carving":                   {"p":3,"s":4,"h":2,"d":2,"r":3,"gamma":2,"g":2,"nu":1},
    "3D_Printed_Sculpture":                 {"p":2,"s":4,"h":3,"d":1,"r":2,"gamma":3,"g":2,"nu":2},
    "Arduino_Kinetic_Art":                  {"p":2,"s":3,"h":3,"d":2,"r":3,"gamma":2,"g":3,"nu":2},
    "Physical_Computing_Art":               {"p":2,"s":3,"h":3,"d":2,"r":3,"gamma":2,"g":3,"nu":3},
    # Sound
    "Found_Object_Percussion":              {"p":1,"s":2,"h":4,"d":1,"r":2,"gamma":3,"g":1,"nu":3},
    "Field_Recording_Composition":          {"p":1,"s":2,"h":3,"d":1,"r":1,"gamma":4,"g":1,"nu":4},
    "Acoustic_Ecology":                     {"p":1,"s":2,"h":3,"d":1,"r":1,"gamma":4,"g":1,"nu":4},
    "Tape_Loop_Composition":                {"p":1,"s":2,"h":3,"d":1,"r":2,"gamma":2,"g":1,"nu":4},
    "Electroacoustic_Sculpture":            {"p":2,"s":3,"h":4,"d":2,"r":2,"gamma":3,"g":2,"nu":3},
    # Movement
    "Contact_Improvisation":                {"p":1,"s":2,"h":3,"d":1,"r":2,"gamma":3,"g":1,"nu":2},
    "Aerial_Silks":                         {"p":2,"s":2,"h":2,"d":2,"r":3,"gamma":4,"g":1,"nu":1},
    "Poi_Flow":                             {"p":1,"s":2,"h":2,"d":1,"r":3,"gamma":3,"g":1,"nu":2},
    "Staff_Spinning":                       {"p":1,"s":2,"h":2,"d":1,"r":3,"gamma":3,"g":1,"nu":2},
    "Juggling":                             {"p":2,"s":3,"h":2,"d":1,"r":4,"gamma":2,"g":1,"nu":2},
    "Object_Manipulation":                  {"p":1,"s":3,"h":3,"d":1,"r":4,"gamma":2,"g":1,"nu":2},
    # Hobbies - spatial/construction
    "Model_Railway_Scenery":                {"p":2,"s":4,"h":2,"d":1,"r":2,"gamma":3,"g":2,"nu":1},
    "Dollhouse_Architecture":               {"p":2,"s":4,"h":3,"d":1,"r":1,"gamma":3,"g":1,"nu":2},
    "LEGO_Technic_Engineering":             {"p":2,"s":3,"h":2,"d":2,"r":3,"gamma":2,"g":3,"nu":1},
    "Meccano_Mechanisms":                   {"p":3,"s":3,"h":2,"d":2,"r":3,"gamma":2,"g":3,"nu":1},
    "Scale_Bridge_Construction":            {"p":3,"s":3,"h":2,"d":2,"r":2,"gamma":3,"g":3,"nu":1},
    "Model_Shipbuilding":                   {"p":3,"s":4,"h":2,"d":1,"r":2,"gamma":3,"g":2,"nu":1},
    "Model_Aircraft_Building":              {"p":3,"s":4,"h":2,"d":1,"r":2,"gamma":3,"g":2,"nu":1},
    "Miniature_Landscape_Gardening":        {"p":2,"s":4,"h":3,"d":1,"r":1,"gamma":3,"g":1,"nu":2},
    # Hobbies - technical/computational
    "Blender_Procedural_Modelling":         {"p":2,"s":4,"h":3,"d":1,"r":2,"gamma":3,"g":2,"nu":3},
    "Houdini_Procedural_Art":               {"p":2,"s":3,"h":3,"d":2,"r":2,"gamma":3,"g":3,"nu":4},
    "GIS_Mapping":                          {"p":3,"s":3,"h":1,"d":2,"r":2,"gamma":3,"g":3,"nu":2},
    "3D_Scanning":                          {"p":3,"s":4,"h":1,"d":2,"r":3,"gamma":2,"g":2,"nu":2},
    "Raspberry_Pi_Projects":                {"p":2,"s":2,"h":2,"d":2,"r":3,"gamma":1,"g":3,"nu":3},
    "Arduino_Projects":                     {"p":2,"s":3,"h":2,"d":2,"r":3,"gamma":1,"g":3,"nu":2},
    "FPGA_Experimentation":                 {"p":4,"s":1,"h":1,"d":3,"r":3,"gamma":1,"g":4,"nu":2},
    "PCB_Design":                           {"p":4,"s":3,"h":1,"d":3,"r":3,"gamma":1,"g":4,"nu":1},
    "CNC_Machining":                        {"p":4,"s":3,"h":1,"d":3,"r":3,"gamma":2,"g":3,"nu":1},
    "Laser_Cutting":                        {"p":3,"s":4,"h":2,"d":2,"r":3,"gamma":2,"g":2,"nu":1},
    "3D_Printing":                          {"p":3,"s":4,"h":2,"d":1,"r":2,"gamma":2,"g":2,"nu":2},
    "CAD_Modelling":                        {"p":4,"s":4,"h":1,"d":2,"r":2,"gamma":3,"g":3,"nu":1},
    "Digital_Fabrication":                  {"p":3,"s":3,"h":2,"d":2,"r":3,"gamma":2,"g":3,"nu":2},
    # Hobbies - natural/geographical
    "Rock_Collecting":                      {"p":2,"s":3,"h":1,"d":2,"r":1,"gamma":2,"g":1,"nu":2},
    "Geological_Field_Sketching":           {"p":2,"s":4,"h":2,"d":2,"r":1,"gamma":3,"g":1,"nu":2},
    "Fossil_Hunting":                       {"p":2,"s":3,"h":1,"d":2,"r":1,"gamma":2,"g":1,"nu":3},
    "Botanical_Field_Recording":            {"p":2,"s":3,"h":2,"d":1,"r":1,"gamma":2,"g":1,"nu":3},
    "Bird_Surveying":                       {"p":2,"s":3,"h":1,"d":1,"r":1,"gamma":2,"g":1,"nu":3},
    "Forest_Mapping":                       {"p":2,"s":3,"h":1,"d":2,"r":2,"gamma":3,"g":2,"nu":3},
    "River_Mapping":                        {"p":2,"s":3,"h":1,"d":2,"r":2,"gamma":3,"g":2,"nu":3},
    "Coastal_Surveying":                    {"p":3,"s":3,"h":1,"d":2,"r":2,"gamma":3,"g":2,"nu":3},
    "Stargazing":                           {"p":1,"s":3,"h":2,"d":1,"r":1,"gamma":4,"g":1,"nu":3},
    "Amateur_Meteorology":                  {"p":2,"s":2,"h":1,"d":1,"r":1,"gamma":3,"g":2,"nu":3},
    "Orienteering":                         {"p":2,"s":3,"h":1,"d":2,"r":3,"gamma":4,"g":2,"nu":1},
    "Rogaining":                            {"p":2,"s":3,"h":1,"d":2,"r":3,"gamma":4,"g":2,"nu":1},
    "Geocaching":                           {"p":2,"s":3,"h":2,"d":1,"r":2,"gamma":3,"g":2,"nu":2},
    "Landscape_Photography":                {"p":1,"s":4,"h":3,"d":1,"r":1,"gamma":4,"g":1,"nu":2},
    # Hobbies - craft
    "Wood_Turning":                         {"p":3,"s":3,"h":2,"d":2,"r":3,"gamma":2,"g":2,"nu":1},
    "Leather_Tooling":                      {"p":3,"s":3,"h":3,"d":1,"r":2,"gamma":1,"g":1,"nu":1},
    "Blacksmithing":                        {"p":2,"s":2,"h":2,"d":3,"r":3,"gamma":1,"g":2,"nu":1},
    "Glass_Blowing":                        {"p":2,"s":4,"h":3,"d":2,"r":3,"gamma":2,"g":1,"nu":2},
    "Ceramic_Wheel_Throwing":               {"p":2,"s":3,"h":3,"d":1,"r":3,"gamma":2,"g":1,"nu":2},
    "Raku":                                 {"p":2,"s":3,"h":3,"d":2,"r":2,"gamma":2,"g":1,"nu":3},
    "Natural_Dyeing":                       {"p":2,"s":3,"h":3,"d":1,"r":1,"gamma":2,"g":1,"nu":2},
    "Hand_Weaving":                         {"p":2,"s":3,"h":3,"d":1,"r":2,"gamma":2,"g":2,"nu":2},
    "Basket_Weaving":                       {"p":1,"s":3,"h":3,"d":1,"r":1,"gamma":2,"g":1,"nu":2},
    "Tatting":                              {"p":3,"s":3,"h":2,"d":1,"r":2,"gamma":1,"g":1,"nu":1},
    "Linocut":                              {"p":2,"s":4,"h":3,"d":1,"r":2,"gamma":1,"g":1,"nu":1},
    "Wood_Engraving":                       {"p":3,"s":4,"h":2,"d":2,"r":2,"gamma":1,"g":1,"nu":1},
    "Drypoint":                             {"p":3,"s":4,"h":2,"d":1,"r":2,"gamma":1,"g":1,"nu":1},
    "Screen_Printing":                      {"p":2,"s":4,"h":3,"d":1,"r":2,"gamma":1,"g":2,"nu":1},
}

# ===== MUSIC GENRES =====
MUSIC = {
    "Dark_Ambient":                         {"p":1,"s":1,"h":3,"d":2,"r":1,"gamma":4,"g":1,"nu":4},
    "Drone":                                {"p":1,"s":1,"h":2,"d":2,"r":1,"gamma":3,"g":1,"nu":5},
    "Ambient_Techno":                       {"p":2,"s":2,"h":2,"d":1,"r":3,"gamma":3,"g":3,"nu":3},
    "IDM":                                  {"p":2,"s":2,"h":4,"d":2,"r":4,"gamma":2,"g":3,"nu":4},
    "Electroacoustic":                      {"p":1,"s":2,"h":4,"d":2,"r":2,"gamma":3,"g":1,"nu":4},
    "Acousmatic_Music":                     {"p":1,"s":2,"h":4,"d":2,"r":1,"gamma":4,"g":1,"nu":4},
    "Musique_Concrete":                     {"p":1,"s":2,"h":4,"d":2,"r":2,"gamma":3,"g":1,"nu":4},
    "Lowercase":                            {"p":1,"s":3,"h":3,"d":1,"r":1,"gamma":3,"g":1,"nu":4},
    "Field_Recording_Ambient":              {"p":1,"s":2,"h":3,"d":1,"r":1,"gamma":4,"g":1,"nu":4},
    "Berlin_School":                        {"p":2,"s":2,"h":3,"d":1,"r":3,"gamma":3,"g":3,"nu":4},
    "Kosmische_Musik":                      {"p":1,"s":2,"h":3,"d":1,"r":2,"gamma":4,"g":2,"nu":4},
    "Hypnagogic_Pop":                       {"p":1,"s":3,"h":3,"d":1,"r":2,"gamma":2,"g":1,"nu":3},
    "Dream_Pop":                            {"p":1,"s":3,"h":4,"d":1,"r":2,"gamma":3,"g":1,"nu":2},
    "Darkwave":                             {"p":2,"s":2,"h":3,"d":2,"r":2,"gamma":3,"g":2,"nu":3},
    "Coldwave":                             {"p":2,"s":2,"h":2,"d":3,"r":2,"gamma":2,"g":2,"nu":2},
    "Minimal_Wave":                         {"p":3,"s":2,"h":2,"d":2,"r":3,"gamma":2,"g":3,"nu":2},
    "EBM":                                  {"p":3,"s":1,"h":1,"d":3,"r":4,"gamma":1,"g":3,"nu":1},
    "Future_Garage":                        {"p":2,"s":2,"h":3,"d":1,"r":3,"gamma":3,"g":2,"nu":3},
    "Downtempo":                            {"p":2,"s":2,"h":3,"d":1,"r":2,"gamma":3,"g":2,"nu":2},
    "Trip_Hop":                             {"p":2,"s":2,"h":3,"d":1,"r":3,"gamma":2,"g":2,"nu":2},
    "Dub_Techno":                           {"p":3,"s":2,"h":2,"d":1,"r":3,"gamma":3,"g":3,"nu":3},
    "Minimal_Techno":                       {"p":4,"s":2,"h":1,"d":1,"r":4,"gamma":2,"g":4,"nu":1},
    "Microhouse":                           {"p":4,"s":3,"h":2,"d":1,"r":4,"gamma":2,"g":3,"nu":2},
    "Glitch":                               {"p":2,"s":3,"h":3,"d":2,"r":4,"gamma":2,"g":2,"nu":3},
    "Glitch_Hop":                           {"p":2,"s":3,"h":3,"d":2,"r":4,"gamma":2,"g":2,"nu":2},
    "Math_Rock":                            {"p":3,"s":2,"h":3,"d":2,"r":4,"gamma":2,"g":3,"nu":2},
    "Post_Rock":                            {"p":2,"s":2,"h":4,"d":1,"r":3,"gamma":3,"g":2,"nu":3},
    "Post_Metal":                           {"p":2,"s":2,"h":3,"d":3,"r":3,"gamma":3,"g":2,"nu":3},
    "Art_Pop":                              {"p":1,"s":3,"h":4,"d":1,"r":2,"gamma":2,"g":1,"nu":3},
    "Avant_Pop":                            {"p":1,"s":3,"h":4,"d":1,"r":2,"gamma":2,"g":1,"nu":4},
    "Chamber_Pop":                          {"p":2,"s":3,"h":4,"d":1,"r":2,"gamma":2,"g":2,"nu":2},
    "Progressive_Electronic":               {"p":3,"s":2,"h":3,"d":2,"r":3,"gamma":2,"g":3,"nu":3},
    "Zeuhl":                                {"p":1,"s":2,"h":4,"d":2,"r":3,"gamma":3,"g":2,"nu":4},
    "Canterbury_Scene":                     {"p":1,"s":2,"h":4,"d":2,"r":3,"gamma":2,"g":2,"nu":4},
    "Ritual_Ambient":                       {"p":1,"s":1,"h":3,"d":2,"r":1,"gamma":4,"g":1,"nu":4},
    "Isolationism":                         {"p":1,"s":1,"h":2,"d":3,"r":1,"gamma":3,"g":1,"nu":5},
    "Sound_Collage":                        {"p":1,"s":2,"h":4,"d":1,"r":2,"gamma":2,"g":1,"nu":4},
    "Musique_Actuelle":                     {"p":1,"s":2,"h":4,"d":2,"r":2,"gamma":2,"g":1,"nu":4},
    "Free_Improvisation":                   {"p":1,"s":2,"h":4,"d":2,"r":3,"gamma":2,"g":1,"nu":4},
    "Prepared_Piano_Composition":           {"p":2,"s":2,"h":4,"d":2,"r":2,"gamma":2,"g":2,"nu":4},
    "Spectral_Music":                       {"p":2,"s":2,"h":4,"d":2,"r":2,"gamma":3,"g":2,"nu":4},
    "Minimalism":                           {"p":4,"s":2,"h":2,"d":1,"r":4,"gamma":2,"g":3,"nu":2},
    "Micropolyphony":                       {"p":3,"s":2,"h":4,"d":1,"r":3,"gamma":2,"g":2,"nu":4},
    "Algorithmic_Composition":              {"p":3,"s":2,"h":3,"d":2,"r":2,"gamma":2,"g":3,"nu":4},
    # Music activities
    "Modular_Synth_Patching":               {"p":2,"s":2,"h":3,"d":2,"r":3,"gamma":2,"g":3,"nu":3},
    "Tape_Loop_Construction":               {"p":1,"s":2,"h":3,"d":1,"r":2,"gamma":2,"g":1,"nu":4},
    "Field_Recording_Walks":                {"p":1,"s":2,"h":2,"d":1,"r":1,"gamma":3,"g":1,"nu":4},
    "Soundscape_Composition":               {"p":1,"s":2,"h":4,"d":1,"r":1,"gamma":4,"g":1,"nu":4},
    "Circuit_Bent_Instrument_Building":     {"p":2,"s":2,"h":4,"d":2,"r":3,"gamma":2,"g":2,"nu":3},
    "Granular_Synthesis":                   {"p":2,"s":2,"h":3,"d":2,"r":3,"gamma":2,"g":3,"nu":4},
    "Algorithmic_Music_Generation":         {"p":3,"s":2,"h":3,"d":2,"r":2,"gamma":2,"g":3,"nu":4},
    "Generative_Sequencer_Design":          {"p":3,"s":2,"h":3,"d":2,"r":3,"gamma":2,"g":3,"nu":4},
    "Live_AV_Performance":                  {"p":1,"s":4,"h":4,"d":1,"r":3,"gamma":3,"g":2,"nu":3},
    "Spatial_Ambisonic_Music":              {"p":2,"s":3,"h":3,"d":1,"r":2,"gamma":5,"g":2,"nu":3},
    "Foley_Sound_Design":                   {"p":2,"s":3,"h":4,"d":1,"r":3,"gamma":3,"g":2,"nu":2},
    "Film_Score_Reconstruction":            {"p":3,"s":2,"h":3,"d":2,"r":2,"gamma":3,"g":2,"nu":3},
    "Found_Object_Instrument_Building":     {"p":1,"s":3,"h":4,"d":2,"r":2,"gamma":2,"g":2,"nu":3},
}

# ===== SPORTS =====
SPORTS = {
    # Flow / aerial
    "Aerial_Hoop":                          {"p":2,"s":2,"h":2,"d":2,"r":3,"gamma":4,"g":1,"nu":1},
    "Trapeze":                              {"p":2,"s":2,"h":2,"d":3,"r":3,"gamma":4,"g":1,"nu":1},
    "Pole_Sport":                           {"p":3,"s":2,"h":2,"d":2,"r":4,"gamma":3,"g":1,"nu":1},
    "Slackline":                            {"p":2,"s":3,"h":1,"d":2,"r":3,"gamma":4,"g":1,"nu":1},
    "Highline":                             {"p":2,"s":3,"h":1,"d":3,"r":2,"gamma":5,"g":1,"nu":1},
    "Flow_Arts":                            {"p":1,"s":2,"h":2,"d":1,"r":3,"gamma":3,"g":1,"nu":2},
    "Acrobatic_Gymnastics":                 {"p":3,"s":2,"h":2,"d":2,"r":4,"gamma":3,"g":2,"nu":1},
    # Board / wheel
    "Freestyle_BMX":                        {"p":2,"s":3,"h":2,"d":3,"r":4,"gamma":3,"g":1,"nu":1},
    "BMX_Flatland":                         {"p":3,"s":4,"h":3,"d":2,"r":4,"gamma":2,"g":2,"nu":2},
    "Dirt_Jumping":                         {"p":2,"s":2,"h":1,"d":3,"r":4,"gamma":3,"g":1,"nu":1},
    "Pump_Track":                           {"p":3,"s":3,"h":1,"d":2,"r":5,"gamma":3,"g":1,"nu":1},
    "Downhill_Longboarding":                {"p":2,"s":3,"h":1,"d":3,"r":4,"gamma":4,"g":1,"nu":1},
    "Freeride_Longboarding":                {"p":2,"s":3,"h":2,"d":2,"r":4,"gamma":3,"g":1,"nu":1},
    "Street_Luge":                          {"p":2,"s":3,"h":1,"d":4,"r":4,"gamma":4,"g":1,"nu":1},
    "Mountainboarding":                     {"p":2,"s":2,"h":1,"d":3,"r":3,"gamma":3,"g":1,"nu":1},
    "Inline_Aggressive_Skating":            {"p":2,"s":3,"h":2,"d":2,"r":4,"gamma":3,"g":1,"nu":1},
    "Artistic_Roller_Skating":              {"p":3,"s":3,"h":3,"d":1,"r":3,"gamma":3,"g":2,"nu":1},
    "Roller_Derby":                         {"p":2,"s":2,"h":2,"d":3,"r":4,"gamma":2,"g":2,"nu":1},
    "Freestyle_Scootering":                 {"p":2,"s":3,"h":2,"d":2,"r":4,"gamma":3,"g":1,"nu":1},
    # Water
    "Whitewater_Rafting":                   {"p":2,"s":2,"h":1,"d":3,"r":4,"gamma":3,"g":2,"nu":1},
    "River_Surfing":                        {"p":2,"s":3,"h":2,"d":2,"r":4,"gamma":3,"g":1,"nu":1},
    "Wing_Foiling":                         {"p":3,"s":3,"h":2,"d":2,"r":4,"gamma":4,"g":2,"nu":1},
    "Foil_Surfing":                         {"p":3,"s":3,"h":2,"d":2,"r":3,"gamma":4,"g":2,"nu":1},
    "Bodyboarding":                         {"p":2,"s":2,"h":1,"d":2,"r":4,"gamma":3,"g":1,"nu":1},
    "Windsurfing_Freestyle":                {"p":3,"s":3,"h":2,"d":2,"r":4,"gamma":4,"g":2,"nu":1},
    "Kayak_Surfing":                        {"p":2,"s":3,"h":2,"d":2,"r":4,"gamma":3,"g":1,"nu":1},
    "Sea_Kayaking":                         {"p":2,"s":2,"h":1,"d":2,"r":3,"gamma":4,"g":2,"nu":2},
    "Canyoning":                            {"p":2,"s":3,"h":2,"d":3,"r":3,"gamma":4,"g":1,"nu":1},
    "Coasteering":                          {"p":2,"s":3,"h":2,"d":3,"r":3,"gamma":4,"g":1,"nu":1},
    "Open_Water_Endurance_Swimming":        {"p":3,"s":2,"h":1,"d":2,"r":4,"gamma":3,"g":2,"nu":1},
    "Underwater_Rugby":                     {"p":2,"s":2,"h":2,"d":2,"r":4,"gamma":4,"g":2,"nu":1},
    "Finswimming":                          {"p":3,"s":2,"h":1,"d":1,"r":5,"gamma":3,"g":2,"nu":1},
    # Mountain / terrain
    "Ski_Mountaineering":                   {"p":2,"s":3,"h":1,"d":3,"r":3,"gamma":4,"g":2,"nu":1},
    "Alpine_Climbing":                      {"p":2,"s":3,"h":1,"d":4,"r":3,"gamma":5,"g":1,"nu":1},
    "Ice_Climbing":                         {"p":3,"s":3,"h":1,"d":4,"r":3,"gamma":4,"g":1,"nu":1},
    "Via_Ferrata":                          {"p":2,"s":3,"h":1,"d":3,"r":3,"gamma":4,"g":1,"nu":1},
    "Scrambling":                           {"p":2,"s":2,"h":1,"d":2,"r":3,"gamma":4,"g":1,"nu":1},
    "Fell_Running":                         {"p":2,"s":2,"h":1,"d":2,"r":5,"gamma":3,"g":1,"nu":1},
    "Mountain_Orienteering":                {"p":2,"s":3,"h":1,"d":2,"r":4,"gamma":5,"g":2,"nu":1},
    "Adventure_Racing":                     {"p":2,"s":3,"h":2,"d":3,"r":4,"gamma":4,"g":2,"nu":1},
    "Skyrunning":                           {"p":2,"s":2,"h":1,"d":2,"r":5,"gamma":4,"g":1,"nu":1},
    "Trail_Ultrarunning":                   {"p":3,"s":2,"h":1,"d":2,"r":5,"gamma":3,"g":2,"nu":2},
    "Snowshoe_Racing":                      {"p":2,"s":2,"h":1,"d":2,"r":4,"gamma":3,"g":1,"nu":1},
    # Technical combat
    "Savate":                               {"p":3,"s":3,"h":2,"d":2,"r":4,"gamma":2,"g":2,"nu":1},
    "HEMA":                                 {"p":3,"s":3,"h":2,"d":3,"r":3,"gamma":2,"g":2,"nu":2},
    "Kendo":                                {"p":4,"s":3,"h":1,"d":2,"r":4,"gamma":2,"g":2,"nu":1},
    "Iaido":                                {"p":4,"s":3,"h":2,"d":2,"r":3,"gamma":2,"g":2,"nu":2},
    "Eskrima":                              {"p":3,"s":3,"h":2,"d":2,"r":4,"gamma":2,"g":2,"nu":1},
    "Kali":                                 {"p":3,"s":3,"h":2,"d":2,"r":4,"gamma":2,"g":2,"nu":1},
    "Brazilian_JiuJitsu":                   {"p":3,"s":2,"h":3,"d":2,"r":3,"gamma":2,"g":3,"nu":2},
    "Wrestling":                            {"p":3,"s":2,"h":2,"d":3,"r":4,"gamma":1,"g":2,"nu":1},
    "Sanda":                                {"p":3,"s":2,"h":2,"d":2,"r":4,"gamma":2,"g":2,"nu":1},
    "Combat_Sambo":                         {"p":3,"s":2,"h":2,"d":3,"r":4,"gamma":1,"g":2,"nu":1},
    "Olympic_Fencing":                      {"p":4,"s":3,"h":2,"d":2,"r":4,"gamma":3,"g":2,"nu":1},
    "Historical_Fencing":                   {"p":3,"s":3,"h":2,"d":3,"r":3,"gamma":2,"g":2,"nu":2},
    # Precision / strategic
    "Sport_Climbing":                       {"p":3,"s":4,"h":2,"d":2,"r":3,"gamma":4,"g":2,"nu":1},
    "Target_Archery":                       {"p":5,"s":3,"h":1,"d":1,"r":2,"gamma":2,"g":2,"nu":1},
    "Field_Archery":                        {"p":3,"s":3,"h":1,"d":2,"r":3,"gamma":4,"g":2,"nu":1},
    "Disc_Golf":                            {"p":2,"s":3,"h":1,"d":1,"r":3,"gamma":3,"g":2,"nu":1},
    "Curling":                              {"p":4,"s":3,"h":2,"d":1,"r":2,"gamma":3,"g":3,"nu":2},
    "Billiards":                            {"p":4,"s":4,"h":2,"d":1,"r":2,"gamma":2,"g":2,"nu":1},
    "Snooker":                              {"p":5,"s":4,"h":2,"d":1,"r":2,"gamma":2,"g":2,"nu":1},
    "Table_Tennis":                         {"p":3,"s":4,"h":1,"d":1,"r":5,"gamma":2,"g":2,"nu":1},
    "Squash":                               {"p":3,"s":3,"h":1,"d":2,"r":5,"gamma":3,"g":2,"nu":1},
    "Padel":                                {"p":3,"s":3,"h":2,"d":1,"r":4,"gamma":3,"g":2,"nu":1},
    "Biathlon":                             {"p":4,"s":3,"h":1,"d":2,"r":4,"gamma":3,"g":2,"nu":1},
}


def top3(weights):
    scored = []
    for label in PROFILES:
        d = particles_to_dims(label, "day")["dims"]
        score = sum(d.get(dim, 0.5) * w for dim, w in weights.items())
        scored.append((label, round(score, 4)))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:3]


def print_section(title, items):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    for name, w in items.items():
        tops = top3(w)
        print(f"  {name}: {tops[0][0]} | {tops[1][0]} | {tops[2][0]}")


def main():
    print_section("PROFESSIONS", PROFESSIONS)
    print_section("CREATIVE ACTIVITIES & HOBBIES", CREATIVE)
    print_section("MUSIC GENRES & ACTIVITIES", MUSIC)
    print_section("SPORTS & PHYSICAL ACTIVITIES", SPORTS)


if __name__ == "__main__":
    main()
