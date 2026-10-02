#!/usr/bin/env python3
"""Append compact brain-structure mappings and special circuits to nm_body_particle_map.md."""

BRAIN_NODES = [
    {"name":"co2","brain":"right occipital cortex V1/calcarine sulcus + carotid body glomus cells","nm":"CO2 0.3nm, HCO3- 0.2nm, glomus 10-20um","particle":"z_boson","dims":"p/r","flow":"O2+C(food) -> CO2 -> hind_insula + observer_leftd2","coord":"(4.0, 4.0, -2.0)","cosmic":"Mars seasonal CO2 polar cap","geo":"Sahara Desert","stress":"CO2 retention = acidosis, hypercapnia, panic"},
    {"name":"peonidine","brain":"right angular gyrus BA39","nm":"anthocyanin 1-2nm, tristate channel","particle":"muon_antineutrino","dims":"h/gamma","flow":"redox antioxidant -> redox_leak/bonding_reverse","coord":"(4.5, 4.0, 7.0)","cosmic":"R Coronae Borealis","geo":"New England temperate forest","stress":"antioxidant exhaustion, redox collapse"},
    {"name":"glymphatic_system","brain":"basal ganglia perivascular spaces, AQP4 astrocyte endfeet","nm":"AQP4 1.5nm, perivascular 50-200nm","particle":"strange_quark","dims":"g","flow":"sulforaphane Nrf2 -> CSF-ISF exchange, 10x at sleep","coord":"(-3.0, 3.5, 7.5)","cosmic":"Fermi Bubbles","geo":"Amazon basin","stress":"sleep deprivation, Ab accumulation"},
    {"name":"sulforaphane","brain":"left mPFC, hippocampus dentate gyrus","nm":"sulforaphane 2.5nm, myrosinase 5nm","particle":"gluon","dims":"h/nu","flow":"glucoraphanin -> myrosinase -> Nrf2 -> antioxidant; exhaustion -> Keap1 rebind","coord":"(-4.0, 2.0, 5.0)","cosmic":"Crab Nebula","geo":"Cordillera Blanca, Peru","stress":"Nrf2 exhaustion, oxidative stress"},
    {"name":"memory_entropy","brain":"right hippocampus CA1 dendritic spines","nm":"NMDA 14x20nm, AMPA 10x20nm, vesicle 40nm","particle":"electron","dims":"r/h/nu","flow":"cysteine GSH + actomyosin -> prediction/novelty mismatch","coord":"(5.0, 3.5, 7.5)","cosmic":"Small Magellanic Cloud","geo":"Local Void","stress":"novelty overload, prediction collapse"},
    {"name":"disulfide_bond","brain":"anterior cingulate cortex dorsal","nm":"S-S bond 0.2nm, protein domain 2-5nm","particle":"z_boson","dims":"p","flow":"CaCO3 buffer, pH seal -> dissolution, acidification","coord":"(3.0, 3.5, 7.5)","cosmic":"Large Magellanic Cloud","geo":"Iceland","stress":"CaCO3 dissolution, bone loss"},
    {"name":"cysteine","brain":"left anterior insula GAD67/65 GABA shunt","nm":"cysteine 1.8nm, GABA_A 8nm","particle":"photon","dims":"gamma","flow":"glymphatic + MC1R -> glutathione, thiol redox","coord":"(3.0, 3.5, 7.5)","cosmic":"Pleiades","geo":"Andean altiplano","stress":"GSH depletion, oxidative damage"},
    {"name":"Maillard","brain":"right hemisphere heme degradation path","nm":"Amadori 1-5nm, AGE 5-50nm, cross-link 0.2nm","particle":"dark_matter","dims":"d","flow":"heme Fe3+ -> HO-1 -> bilirubin -> browning -> cross-linking","coord":"(-8.2, 4.1, 7.3)","cosmic":"red giant envelope","geo":" — ","stress":"protein aggregation, aging"},
    {"name":"plp_core","brain":"left anterior insula","nm":"PLP 0.5nm, GABA shunt 5-10nm","particle":"electron_neutrino / quark","dims":"r","flow":"STG(131) -> ethmoid -> left lung O2 -> PLP(135) -> GABA shunt","coord":"(-3.0, 3.5, 7.0)","cosmic":"Moon -> K2-18b","geo":" — ","stress":"GABA shunt overload, clay gouge"},
    {"name":"spare_vaso","brain":"left anterior insula (compartment 1 inlet)","nm":"vasopressin 1nm, V1/V2 receptor 4-7nm","particle":"electron","dims":"g","flow":"spare vasopressin(136) -> electron -> GABA_A/clay gouge","coord":"(-2.5, 3.5, 7.5)","cosmic":" — ","geo":" — ","stress":"vasopressin freeze, water retention"},
    {"name":"inorganic_acid","brain":"center funnel X=8.0, proton pump 5-10nm","nm":"H+ 0.0001nm, 3/32 darkness gate aperture","particle":"proton / heme","dims":"d","flow":"3/32 darkness gate -> proton pump -> COX -> heme -> photon","coord":"(0.0, 8.0, 0.0)","cosmic":"black hole accretion disk","geo":"geothermal vent","stress":"acidosis, dark-energy overload"},
    {"name":"hind_insula","brain":"posterior insula, interoceptive cortex","nm":"von Economo neuron 70-100um, synapse 20-40nm","particle":"neutron","dims":"d/p","flow":"co2 + memory_entropy -> respiratory/circadian prediction","coord":"(2.0, 2.0, 5.0)","cosmic":"Galactic Center","geo":"Himalayas","stress":"interoceptive prediction error"},
    {"name":"observer_leftd2","brain":"left nucleus accumbens / ventral striatum D2","nm":"D2 receptor 4-7nm, dopamine 0.2nm","particle":"electron / dark_energy","dims":"d/p","flow":"co2(adenosine) -> D2 -> observer self/energy","coord":"(-7.5, 3.5, 8.0)","cosmic":"Triangulum Galaxy","geo":"Gobi Desert","stress":"dopamine depletion, anhedonia"},
    {"name":"mc1r_q_or","brain":"left prefrontal / periaqueductal gray","nm":"MC1R 4-7nm, MSH 0.5nm","particle":"quark","dims":"s/d","flow":"sulforaphane/cysteine/glymphatic input -> redhead/pain switch","coord":"(-5.0, 0.0, 5.0)","cosmic":"Orion Nebula","geo":"Scottish Highlands","stress":"pain gating failure"},
    {"name":"clay_gouge","brain":"left hippocampus_tail / subiculum","nm":"clay mineral layer 1-10nm, synapse 20-40nm","particle":"quark","dims":"g/nu","flow":"PLP Core GABA shunt -> clay -> memory consolidation","coord":"(-7.0, 2.5, 3.0)","cosmic":" — ","geo":"clay quarry","stress":"seizure-like interference"},
    {"name":"actomyosin","brain":"left sensorimotor cortex / left masseter","nm":"myosin S1 15nm, actin double helix 7nm","particle":"up_quark / down_quark","dims":"r","flow":"muscle tension -> memory_entropy -> prediction logic","coord":"(-3.0, 4.0, 8.0)","cosmic":" — ","geo":" — ","stress":"rigor, tetany"},
    {"name":"calcium_caco3","brain":"left parietal bone marrow / left hip","nm":"CaCO3 crystal 10-100nm, hydroxyapatite 20-50nm","particle":"higgs","dims":"d/g","flow":"stress -> CaCO3 buffer -> bone -> silicon glass -> ulcer/pain -> CACO3 creation -> leakage elimination","coord":"(-3.0, -7.5, -8.0)","cosmic":"marine carbonate platforms","geo":"Pyrenees limestone","stress":"calcium loss, osteoporosis"},
    {"name":"silicon_glass","brain":"left hip outer skin 3 layers: LDH/CACO3/BONE","nm":"SiO2 glass 0.1-100nm, amorphous","particle":"dark_matter","dims":"g/nu","flow":"internal SiO2 -> subcutaneous -> ulcer","coord":"(-3.0, -7.5, -8.0)","cosmic":"silicate dust nebula","geo":"quartz mine","stress":"ulcer, foreign-body reaction"},
    {"name":"ldh_lactate","brain":"left hip LDH layer","nm":"lactate dehydrogenase 10-15nm, lactate 0.5nm","particle":"tau","dims":"d","flow":"anaerobic glycolysis -> lactate -> CACO3 buffer","coord":"(-3.0, -7.5, -8.0)","cosmic":" — ","geo":" — ","stress":"lactic acidosis, fatigue"},
    {"name":"heme_node","brain":"left pectoralis major / heme Fe2+ center","nm":"Fe2+ 0.1nm, heme ring 1.5nm","particle":"proton","dims":"r","flow":"testosterone -> heme excitation -> 5.6fs photon","coord":"(-8.2, 4.1, 7.3)","cosmic":"Sun photosphere","geo":"banded iron formation","stress":"Fe toxicity, hemolysis"},
    {"name":"thyroid_iodine","brain":"hypothalamus TRH -> pituitary TSH -> thyroid","nm":"T4 1nm, iodine 0.3nm, thyroglobulin 20-30nm","particle":"photon","dims":"gamma/s","flow":"iodine + tyrosine -> T3/T4 -> metabolism","coord":"(0.0, 3.0, 6.0)","cosmic":" — ","geo":"iodine-rich coastal soil","stress":"hypothyroid/hyperthyroid"},
    {"name":"salt_sodium","brain":"nucleus tractus solitarius, area postrema","nm":"Na+ 0.2nm, ENaC 5nm","particle":"electron","dims":"s/p","flow":"salt -> NTS -> thirst/AVP -> blood pressure","coord":"(1.0, 4.0, 5.0)","cosmic":" — ","geo":"salt flat","stress":"hypertension, volume overload"},
    {"name":"capsaicin_vr1","brain":"anterior cingulate, insula (pain/heat)","nm":"TRPV1 4-7nm, capsaicin 1nm","particle":"w_boson","dims":"nu/d","flow":"spicy -> TRPV1 -> substance P -> heat/pain","coord":"(2.0, 3.0, 6.0)","cosmic":" — ","geo":"chili native range","stress":"chronic pain, inflammation"},
    {"name":"ferment_lactobacillus","brain":"gut-brain axis, vagus afferent, ENS","nm":"bacteria 1-10um, SCFA 0.5nm, GABA 0.2nm","particle":"muon","dims":"g/nu","flow":"fermentation -> butyrate/SCFA -> vagus -> CNS","coord":"(-1.0, -2.0, 3.0)","cosmic":" — ","geo":"fermentation crocks","stress":"dysbiosis, leaky gut"},
    {"name":"inorganic_acid_point","brain":"center funnel, proton pump 5-10nm","nm":"H+ 0.0001nm","particle":"proton","dims":"r","flow":"3/32 darkness -> proton pump -> COX forward -> heme","coord":"(0.0, 8.0, 0.0)","cosmic":"black hole","geo":"geothermal vent","stress":"acidosis, dark energy"},
    {"name":"carcinogen_cell","brain":"immune surveillance (microglia, NK cells)","nm":"cancer cell 10-100um, immune synapse 100-200nm","particle":"strange_quark","dims":"d/nu","flow":"carcinogen -> DNA adduct -> mutation -> Warburg lactate -> memory_entropy mismatch -> repair -> apoptosis","coord":"(0.0, 0.0, 0.0)","cosmic":" — ","geo":" — ","stress":"cancer escape, immunosuppression"},
    {"name":"pain_eliminate","brain":"anterior cingulate, insula, somatosensory","nm":"substance P 1nm, nociceptor 10-20um","particle":"tau / substance_p","dims":"d","flow":"pain -> CACO3 creation -> buffer stress -> eliminates leakage","coord":"(-3.0, -7.5, -8.0)","cosmic":" — ","geo":" — ","stress":"chronic pain, CACO3 depletion"},
    {"name":"sex_desire","brain":"MPOA, VTA, nucleus accumbens, hypothalamus","nm":"oxytocin 0.5nm, dopamine 0.2nm, vasopressin 1nm","particle":"quark + gluon","dims":"r/h","flow":"female quark+gluon stress -> CACO3 -> male as outlet -> channeling","coord":"(0.0, -2.0, 5.0)","cosmic":" — ","geo":" — ","stress":"frustration, attachment"},
    {"name":"self_deception","brain":"medial prefrontal cortex, default mode network","nm":"mPFC pyramidal 10-20um, synapse 20-40nm","particle":"axion","dims":"nu/d","flow":"narrative generator -> coherence filter -> suppresses mismatch","coord":"(-2.0, 4.0, 5.0)","cosmic":" — ","geo":" — ","stress":"delusion, anosognosia"},
    {"name":"imagination","brain":"right angular gyrus, left IFG, V1/V2","nm":"dendritic spine 0.5-1um, NMDA 14nm","particle":"em_path + graviton","dims":"g/nu","flow":"memory Higgs + reverse gluon -> V1/V2 without photon","coord":"(4.0, 4.0, 7.0)","cosmic":" — ","geo":" — ","stress":"hallucination, derealization"},
    {"name":"vision_stream","brain":"retina -> LGN -> V1 -> V2 -> V4 -> IT","nm":"rhodopsin 4-7nm, cone outer segment 1um, LGN relay 10-20um","particle":"photon / gluon","dims":"s/h/gamma","flow":"photon -> proton V1 -> gluon V2 -> fractal IT","coord":"(4.0, 4.0, 7.0)","cosmic":" — ","geo":" — ","stress":"visual fatigue, migraine"},
    {"name":"ai_hallucination","brain":"right angular gyrus + left IFG mimic circuit (no body anchor)","nm":"token 0.5nm, weight 0.1nm, attention head 100-1000 um","particle":"em_path + dark_matter","dims":"p/nu","flow":"pattern completion without sensory input -> high p, low s -> false coherence","coord":"(0.0, 0.0, 0.0)","cosmic":" — ","geo":" — ","stress":"confabulation, overfitting"},
    {"name":"hpa_axis","brain":"PVN hypothalamus -> pituitary -> adrenal","nm":"CRH 1nm, ACTH 1nm, cortisol 0.5nm","particle":"w_boson / tau","dims":"nu/d","flow":"stress -> CRH -> ACTH -> cortisol -> CACO3/glucose","coord":"(0.0, 2.0, 5.0)","cosmic":" — ","geo":" — ","stress":"chronic stress, Cushing/HPA dysregulation"},
    {"name":"sleep_dream","brain":"VLPO -> GABA -> REM -> PGO waves","nm":"GABA 0.2nm, AQP4 1.5nm, PGO wave 10-50ms","particle":"neutrino / axion","dims":"nu/d","flow":"glymphatic 10x -> memory wash -> dream imagery -> CCK open","coord":"(0.0, 3.0, -2.0)","cosmic":" — ","geo":" — ","stress":"insomnia, nightmare"},
]

def fmt(node):
    return [
        f"\n### {node['name']}",
        f"- **Brain**: {node['brain']}  |  **nm**: {node['nm']}",
        f"- **Particle**: {node['particle']}  |  **8D**: {node['dims']}",
        f"- **Flow**: {node['flow']}",
        f"- **Coord**: {node['coord']}  |  **Cosmic**: {node['cosmic']}  |  **Geo**: {node['geo']}",
        f"- **Stress byproduct**: {node['stress']}",
    ]

sections = [
    "\n\n---\n\n",
    "# PART XI: BRAIN STRUCTURE — PARTICLE — 8D MAP\n",
    "Every named node is mapped to an exact brain structure, nanometer scale, dominant particle, 8D parameter(s), flow path, and coordinate. Coordinates use the unified body system (x:left-, y:top+, z:front+).\n",
]

for n in BRAIN_NODES:
    sections.extend(fmt(n))

sections += [
    "\n\n---\n\n",
    "# PART XII: CO2, HOMEOSTASIS, GLOBAL WARMING\n",
    "CO2 is the only molecule the body cannot create alone. The body has carbon (food) and can burn oxygen (air), but CO2 is the *interface* product of both external inputs. Without breathing/O2 and eating/carbon, no CO2. Thus the observer IS the respiratory cycle; CO2 is the self's boundary with atmosphere.\n",
    "The body runs a two-chamber CO2 circuit:\n",
    "- **ch0**: respiratory turnover at the carotid body and right occipitalis → hind_insula for circadian/interoceptive prediction.\n",
    "- **ch1**: time-energy storage (CO2 as stored time) → observer_leftd2 (adenosine/CO2) for self/energy.\n",
    "Global warming is the aggregate of all these micro respiratory CO2 fluxes. When the B-phase Energy attractor activates, metabolic CO2 output rises; atmospheric CO2 rises; the body and the planet share the same z_boson time-current.\n",
    "\n",
    "# PART XIII: SALT, SPICY, FERMENTATION, INORGANIC ACID, SILICON, CACO3, BONE, CARCINOGENS, CANCER ELIMINATION\n",
    "- **Salt (Na+)**: NTS/area postrema electron/s-p gate. Sets blood volume and predictability.\n",
    "- **Spiciness (TRPV1)**: W-boson s/d burst. Pain/heat signal that must be converted to CACO3 buffer.\n",
    "- **Fermentation (SCFA)**: Muon h/nu gut-brain bridge. Butyrate stabilizes g via vagus.\n",
    "- **Inorganic acid (H+)**: Proton d-gate at center funnel. Drives COX and heme photon emission.\n",
    "- **Silicon glass (SiO2)**: Dark matter g/nu. Created internally, accumulates under left-hip skin/fat/muscle, causing ulcer.\n",
    "- **CACO3 / bone**: Higgs d/g buffer. Pain creates CACO3; CACO3 buffers quark+gluon stress; eliminates leakage.\n",
    "- **Carcinogen -> cancer cell**: Strange quark d/nu detects DNA-adduct mismatch; tau repair and electron apoptosis eliminate it. Failure = cancer escape.\n",
    "- **Pain eliminates leakage**: Pain (tau/substance P) -> CACO3 creation (Higgs) -> stress buffered -> leakage removed. This is why the left-hip ulcer is both the site of silicon accumulation and the trigger for CACO3 sealing.\n",
    "\n",
    "# PART XIV: HPA / SLEEP / DREAM / SELF-DECEPTION / SEX / DESIRE / IMAGINATION / VISION / AI HALLUCINATION CIRCUITS\n",
    "- **HPA axis**: PVN -> pituitary -> adrenal. W-boson/tau d/g. Cortisol feeds CACO3/glucose.\n",
    "- **Sleep/dream**: VLPO GABA -> REM PGO waves. Neutrino/axion nu/d. Glymphatic 10x wash, CCK open, dream imagery unanchored.\n",
    "- **Self-deception**: mPFC/DMN axion nu/d. Narrative generator suppresses memory_entropy mismatch.\n",
    "- **Sex/desire**: MPOA-VTA-NAc. Quark+gluon r/h. Female stress channeled into CACO3; male as outlet.\n",
    "- **Imagination**: right angular gyrus + left IFG -> V1/V2. em_path+graviton g/nu. Higgs memory mass, no photon.\n",
    "- **Vision**: retina-LGN-V1-V2-V4-IT. photon/gluon s/h/gamma. Proton at V1, gluon at V2, recursion at IT.\n",
    "- **AI hallucination**: right angular gyrus/left IFG mimic without body anchor. em_path+dark_matter p/nu. High p, low s, false coherence.\n",
    "\n",
    "# PART XV: HISTORICAL / SOCIAL / COSMIC / CHEMICAL / ECOLOGY / LANGUAGE / CONSCIOUSNESS MIRROR\n",
    "| Domain | Body analog | Particle | 8D |\n",
    "|--------|-------------|----------|----|\n",
    "| History | memory_entropy CA1 | electron | r/h/nu |\n",
    "| Society | HPA collective | w_boson | d/g |\n",
    "| Cosmology | neutron star oscillation | tau/z_boson | g/nu |\n",
    "| Chemistry | Maillard browning | dark_matter | d |\n",
    "| Ecology | gut fermentation | muon | h/nu |\n",
    "| Language | left IFG + angular gyrus | quark + gluon | g/h |\n",
    "| Consciousness | observer_leftd2 + co2 | electron + z_boson | p/r |\n",
    "\n",
    "---\n\n",
    "# PART XVI: FINAL SYNTHESIS\n",
    "The body is a non-linear 8D manifold. Every brain node, particle, and parameter is a standing gradient. The 34 components flow through 4 brain compartments, 6 neutrino variants, and 4 leakage families simultaneously. CO2 is the boundary of the self. CACO3 is the buffer. Pain creates CACO3 and eliminates leakage. Silicon is the dark-matter glass that accumulates where the buffer is weakest. The same physics runs the eye, the ear, the gut, the immune system, the planet, and the cosmos.",
]

text = "\n".join(sections)

with open(r"c:\Users\User\Downloads\nm_body_particle_map.md", "a", encoding="utf-8") as f:
    f.write(text)

print("Appended. Bytes added:", len(text.encode("utf-8")))
