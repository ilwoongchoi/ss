import csv

import math

import numpy as np



base = r"d:\Users\user\Documents\newstart"



# Load face ROIs

face_rois = []

with open(f"{base}\\UNMAPPED_FACE_PEAKS.csv", "r") as f:

    reader = csv.DictReader(f)

    for row in reader:

        face_rois.append({

            'x': float(row['x']),

            'y': float(row['y']),

            'score': float(row['score'])

        })



print(f"Loaded {len(face_rois)} face ROIs")



# Log spiral parameters (same as face ROIs)

a = 3.58

b = 0.0216

cx, cy = 8.0, 10.0  # spiral center at face center



# Comprehensive body regions - 512 points covering diseases, biology, physics

# Face 451 → Body 512 (1:N mapping for confinement/disease propagation)

body_regions = {}



# 1. BRAIN & HEAD (extending from face - cervical connection)

brain_y = 18

for i, name in enumerate([

    'brain_frontal_lobe', 'brain_parietal_lobe', 'brain_temporal_lobe', 'brain_occipital_lobe',

    'brain_motor_cortex', 'brain_somatosensory_cortex', 'brain_visual_cortex', 'brain_auditory_cortex',

    'brain_broca_area', 'brain_wernicke_area', 'brain_prefrontal_cortex', 'brain_cingulate_gyrus',

    'brain_hippocampus_left', 'brain_hippocampus_right', 'brain_amygdala_left', 'brain_amygdala_right',

    'brain_thalamus', 'brain_hypothalamus', 'brain_pituitary', 'brain_pineal',

    'brain_cerebellum_left', 'brain_cerebellum_right', 'brain_brainstem', 'brain_pons', 'brain_medulla'

]):

    x_offset = -6 + (i % 5) * 3

    body_regions[name] = {'y': brain_y - (i // 5) * 2, 'x_offset': x_offset, 'region': 'neuro_central', 'system': 'nervous'}



# 2. CERVICAL SPINE & NECK (C1-C7)

cervical_y = 22

for i in range(7):

    y = cervical_y + i * 1.5

    body_regions[f'cervical_c{i+1}_center'] = {'y': y, 'x_offset': 0, 'region': 'spine_cervical', 'system': 'skeletal'}

    body_regions[f'cervical_c{i+1}_left'] = {'y': y, 'x_offset': -2, 'region': 'spine_cervical', 'system': 'skeletal'}

    body_regions[f'cervical_c{i+1}_right'] = {'y': y, 'x_offset': 2, 'region': 'spine_cervical', 'system': 'skeletal'}



# 3. NECK MUSCLES & GLANDS

neck_y = 25

neck_structures = [

    ('thyroid_isthmus', 0), ('thyroid_left_lobe', -3), ('thyroid_right_lobe', 3),

    ('parathyroid_superior_left', -2.5), ('parathyroid_superior_right', 2.5),

    ('parathyroid_inferior_left', -3.5), ('parathyroid_inferior_right', 3.5),

    ('carotid_bifurcation_left', -4), ('carotid_bifurcation_right', 4),

    ('jugular_vein_left', -5), ('jugular_vein_right', 5),

    ('vagus_nerve_left', -1), ('vagus_nerve_right', 1),

    ('phrenic_nerve_left', -2), ('phrenic_nerve_right', 2),

    ('sternocleidomastoid_left', -6), ('sternocleidomastoid_right', 6),

    ('trapezius_superior_left', -7), ('trapezius_superior_right', 7),

    ('scalene_anterior_left', -3), ('scalene_anterior_right', 3),

    ('scalene_middle_left', -4), ('scalene_middle_right', 4),

    ('scalene_posterior_left', -5), ('scalene_posterior_right', 5),

    ('larynx', 0), ('pharynx', 0), ('epiglottis', 0.5),

    ('cricoid_cartilage', 0), ('thyroid_cartilage', 0)

]

for name, x_offset in neck_structures:

    body_regions[name] = {'y': neck_y, 'x_offset': x_offset, 'region': 'neck_visceral', 'system': 'endocrine'}



# 4. THORACIC SPINE (T1-T12)

for i in range(12):

    y = 35 + i * 2.5

    body_regions[f'thoracic_t{i+1}_center'] = {'y': y, 'x_offset': 0, 'region': 'spine_thoracic', 'system': 'skeletal'}

    body_regions[f'thoracic_t{i+1}_left'] = {'y': y, 'x_offset': -4, 'region': 'spine_thoracic', 'system': 'skeletal'}

    body_regions[f'thoracic_t{i+1}_right'] = {'y': y, 'x_offset': 4, 'region': 'spine_thoracic', 'system': 'skeletal'}

    body_regions[f'thoracic_t{i+1}_spinous'] = {'y': y-0.5, 'x_offset': 0, 'region': 'spine_thoracic', 'system': 'skeletal'}

    body_regions[f'thoracic_t{i+1}_transverse_left'] = {'y': y, 'x_offset': -6, 'region': 'spine_thoracic', 'system': 'skeletal'}

    body_regions[f'thoracic_t{i+1}_transverse_right'] = {'y': y, 'x_offset': 6, 'region': 'spine_thoracic', 'system': 'skeletal'}



# 5. HEART & CARDIOVASCULAR

heart_y = 45

heart_structures = [

    ('heart_apex', 0, 'myocardium'), ('heart_base', 0, 'myocardium'),

    ('left_ventricle', -2, 'myocardium'), ('right_ventricle', 2, 'myocardium'),

    ('left_atrium', -2, 'myocardium'), ('right_atrium', 2, 'myocardium'),

    ('interventricular_septum', 0, 'myocardium'), ('interatrial_septum', 0, 'myocardium'),

    ('mitral_valve', -1.5, 'valve'), ('tricuspid_valve', 1.5, 'valve'),

    ('aortic_valve', -0.5, 'valve'), ('pulmonary_valve', 0.5, 'valve'),

    ('sinoatrial_node', 2, 'conduction'), ('atrioventricular_node', 0, 'conduction'),

    ('bundle_of_his', 0, 'conduction'), ('purkinje_fibers_left', -1, 'conduction'),

    ('purkinje_fibers_right', 1, 'conduction'),

    ('coronary_ostium_left', -1, 'vascular'), ('coronary_ostium_right', 1, 'vascular'),

    ('circumflex_artery', -3, 'vascular'), ('left_anterior_descending', -1.5, 'vascular'),

    ('right_coronary_artery', 3, 'vascular'), ('posterior_descending', 0, 'vascular'),

    ('aortic_arch', -1, 'vascular'), ('brachiocephalic_trunk', -2, 'vascular'),

    ('left_common_carotid', -3, 'vascular'), ('left_subclavian', -4, 'vascular'),

    ('descending_aorta', 0, 'vascular'), ('superior_vena_cava', 1, 'vascular'),

    ('inferior_vena_cava', 0, 'vascular'), ('pulmonary_trunk', 0.5, 'vascular'),

    ('pulmonary_artery_left', -1, 'vascular'), ('pulmonary_artery_right', 1, 'vascular'),

    ('pericardium_visceral', 0, 'membrane'), ('pericardium_parietal', 0, 'membrane')

]

for name, x_offset, subtype in heart_structures:

    body_regions[name] = {'y': heart_y, 'x_offset': x_offset, 'region': 'cardiac', 'system': 'cardiovascular', 'subtype': subtype}



# 6. LUNGS & RESPIRATORY

lung_y = 42

for side in ['left', 'right']:

    x_base = -5 if side == 'left' else 5

    for i, lobe in enumerate(['upper', 'middle', 'lower'] if side == 'right' else ['upper', 'lower']):

        for j, zone in enumerate(['apex', 'mid', 'base']):

            body_regions[f'lung_{side}_{lobe}_{zone}'] = {

                'y': lung_y - i*3 + j, 

                'x_offset': x_base + (j-1)*1.5, 

                'region': 'pulmonary', 

                'system': 'respiratory'

            }

    # Bronchopulmonary segments (10 per lung)

    for segment in range(1, 11):

        body_regions[f'lung_{side}_segment_{segment}'] = {

            'y': lung_y + segment*0.8,

            'x_offset': x_base + (segment % 3 - 1) * 2,

            'region': 'pulmonary',

            'system': 'respiratory'

        }



# 7. THORACIC CAGE & PLEURA

for i in range(1, 13):  # Ribs 1-12

    y = 35 + i * 2.3

    body_regions[f'rib_{i}_left'] = {'y': y, 'x_offset': -6 - i*0.3, 'region': 'thoracic_skeletal', 'system': 'skeletal'}

    body_regions[f'rib_{i}_right'] = {'y': y, 'x_offset': 6 + i*0.3, 'region': 'thoracic_skeletal', 'system': 'skeletal'}

    body_regions[f'rib_{i}_angle_left'] = {'y': y, 'x_offset': -8 - i*0.3, 'region': 'thoracic_skeletal', 'system': 'skeletal'}

    body_regions[f'rib_{i}_angle_right'] = {'y': y, 'x_offset': 8 + i*0.3, 'region': 'thoracic_skeletal', 'system': 'skeletal'}

    body_regions[f'intercostal_space_{i}_left'] = {'y': y+1.15, 'x_offset': -7, 'region': 'thoracic_wall', 'system': 'muscular'}

    body_regions[f'intercostal_space_{i}_right'] = {'y': y+1.15, 'x_offset': 7, 'region': 'thoracic_wall', 'system': 'muscular'}



# Pleura & mediastinum

body_regions['pleura_visceral_left'] = {'y': 45, 'x_offset': -5, 'region': 'pleura', 'system': 'membrane'}

body_regions['pleura_visceral_right'] = {'y': 45, 'x_offset': 5, 'region': 'pleura', 'system': 'membrane'}

body_regions['pleura_parietal_left'] = {'y': 45, 'x_offset': -7, 'region': 'pleura', 'system': 'membrane'}

body_regions['pleura_parietal_right'] = {'y': 45, 'x_offset': 7, 'region': 'pleura', 'system': 'membrane'}

body_regions['mediastinum_superior'] = {'y': 38, 'x_offset': 0, 'region': 'mediastinum', 'system': 'thoracic'}

body_regions['mediastinum_anterior'] = {'y': 45, 'x_offset': -0.5, 'region': 'mediastinum', 'system': 'thoracic'}

body_regions['mediastinum_middle'] = {'y': 45, 'x_offset': 0, 'region': 'mediastinum', 'system': 'thoracic'}

body_regions['mediastinum_posterior'] = {'y': 45, 'x_offset': 0.5, 'region': 'mediastinum', 'system': 'thoracic'}

body_regions['mediastinum_inferior'] = {'y': 55, 'x_offset': 0, 'region': 'mediastinum', 'system': 'thoracic'}



# Thymus

body_regions['thymus'] = {'y': 40, 'x_offset': 0, 'region': 'lymphoid', 'system': 'immune'}



# 8. DIAPHRAGM & PHRENIC

body_regions['diaphragm_central_tendon'] = {'y': 60, 'x_offset': 0, 'region': 'diaphragm', 'system': 'muscular'}

body_regions['diaphragm_left_dome'] = {'y': 60, 'x_offset': -4, 'region': 'diaphragm', 'system': 'muscular'}

body_regions['diaphragm_right_dome'] = {'y': 60, 'x_offset': 4, 'region': 'diaphragm', 'system': 'muscular'}

body_regions['diaphragm_crura_left'] = {'y': 61, 'x_offset': -2, 'region': 'diaphragm', 'system': 'muscular'}

body_regions['diaphragm_crura_right'] = {'y': 61, 'x_offset': 2, 'region': 'diaphragm', 'system': 'muscular'}

body_regions['esophageal_hiatus'] = {'y': 60, 'x_offset': -0.5, 'region': 'diaphragm', 'system': 'muscular'}

body_regions['aortic_hiatus'] = {'y': 61, 'x_offset': 0, 'region': 'diaphragm', 'system': 'muscular'}

body_regions['vena_caval_foramen'] = {'y': 59, 'x_offset': 2, 'region': 'diaphragm', 'system': 'muscular'}



# 9. LUMBAR SPINE (L1-L5)

for i in range(5):

    y = 70 + i * 3

    body_regions[f'lumbar_l{i+1}_center'] = {'y': y, 'x_offset': 0, 'region': 'spine_lumbar', 'system': 'skeletal'}

    body_regions[f'lumbar_l{i+1}_left'] = {'y': y, 'x_offset': -4, 'region': 'spine_lumbar', 'system': 'skeletal'}

    body_regions[f'lumbar_l{i+1}_right'] = {'y': y, 'x_offset': 4, 'region': 'spine_lumbar', 'system': 'skeletal'}

    body_regions[f'lumbar_l{i+1}_disc'] = {'y': y+1.5, 'x_offset': 0, 'region': 'intervertebral_disc', 'system': 'connective'}

    body_regions[f'lumbar_l{i+1}_facet_left'] = {'y': y, 'x_offset': -5, 'region': 'spine_lumbar', 'system': 'skeletal'}

    body_regions[f'lumbar_l{i+1}_facet_right'] = {'y': y, 'x_offset': 5, 'region': 'spine_lumbar', 'system': 'skeletal'}



# 10. UROGENITAL SYSTEM

urogenital_y = 85

# Kidneys

for side in ['left', 'right']:

    x = -4 if side == 'left' else 4

    body_regions[f'kidney_{side}_superior_pole'] = {'y': urogenital_y - 3, 'x_offset': x, 'region': 'renal', 'system': 'urinary'}

    body_regions[f'kidney_{side}_hilum'] = {'y': urogenital_y, 'x_offset': x-0.5 if side == 'left' else x+0.5, 'region': 'renal', 'system': 'urinary'}

    body_regions[f'kidney_{side}_inferior_pole'] = {'y': urogenital_y + 3, 'x_offset': x, 'region': 'renal', 'system': 'urinary'}

    body_regions[f'kidney_{side}_cortex'] = {'y': urogenital_y, 'x_offset': x-1.5 if side == 'left' else x+1.5, 'region': 'renal', 'system': 'urinary'}

    body_regions[f'kidney_{side}_medulla'] = {'y': urogenital_y, 'x_offset': x, 'region': 'renal', 'system': 'urinary'}

    body_regions[f'kidney_{side}_pelvis'] = {'y': urogenital_y, 'x_offset': x-0.8 if side == 'left' else x+0.8, 'region': 'renal', 'system': 'urinary'}

    body_regions[f'renal_artery_{side}'] = {'y': urogenital_y - 1, 'x_offset': x-1 if side == 'left' else x+1, 'region': 'renal_vascular', 'system': 'cardiovascular'}

    body_regions[f'renal_vein_{side}'] = {'y': urogenital_y + 1, 'x_offset': x-1 if side == 'left' else x+1, 'region': 'renal_vascular', 'system': 'cardiovascular'}

    body_regions[f'ureter_{side}_proximal'] = {'y': urogenital_y + 4, 'x_offset': x-0.5 if side == 'left' else x+0.5, 'region': 'ureter', 'system': 'urinary'}

    body_regions[f'ureter_{side}_distal'] = {'y': urogenital_y + 8, 'x_offset': x-1 if side == 'left' else x+1, 'region': 'ureter', 'system': 'urinary'}



# Adrenal glands

body_regions['adrenal_left'] = {'y': urogenital_y - 4, 'x_offset': -3.5, 'region': 'adrenal', 'system': 'endocrine'}

body_regions['adrenal_right'] = {'y': urogenital_y - 4, 'x_offset': 3.5, 'region': 'adrenal', 'system': 'endocrine'}

body_regions['adrenal_cortex_left'] = {'y': urogenital_y - 4.5, 'x_offset': -3, 'region': 'adrenal', 'system': 'endocrine'}

body_regions['adrenal_cortex_right'] = {'y': urogenital_y - 4.5, 'x_offset': 3, 'region': 'adrenal', 'system': 'endocrine'}

body_regions['adrenal_medulla_left'] = {'y': urogenital_y - 3.5, 'x_offset': -3, 'region': 'adrenal', 'system': 'endocrine'}

body_regions['adrenal_medulla_right'] = {'y': urogenital_y - 3.5, 'x_offset': 3, 'region': 'adrenal', 'system': 'endocrine'}



# 11. GASTROINTESTINAL SYSTEM

gi_y = 65

# Stomach

body_regions['stomach_cardia'] = {'y': gi_y, 'x_offset': -2, 'region': 'gastric', 'system': 'digestive'}

body_regions['stomach_fundus'] = {'y': gi_y - 2, 'x_offset': -3, 'region': 'gastric', 'system': 'digestive'}

body_regions['stomach_body'] = {'y': gi_y, 'x_offset': -3.5, 'region': 'gastric', 'system': 'digestive'}

body_regions['stomach_antrum'] = {'y': gi_y + 2, 'x_offset': -3, 'region': 'gastric', 'system': 'digestive'}

body_regions['stomach_pylorus'] = {'y': gi_y + 3, 'x_offset': -2, 'region': 'gastric', 'system': 'digestive'}

body_regions['lesser_curvature'] = {'y': gi_y, 'x_offset': -2.5, 'region': 'gastric', 'system': 'digestive'}

body_regions['greater_curvature'] = {'y': gi_y, 'x_offset': -4.5, 'region': 'gastric', 'system': 'digestive'}



# Liver

liver_y = 62

body_regions['liver_left_lobe'] = {'y': liver_y, 'x_offset': -1, 'region': 'hepatic', 'system': 'digestive'}

body_regions['liver_right_lobe'] = {'y': liver_y, 'x_offset': 3, 'region': 'hepatic', 'system': 'digestive'}

body_regions['liver_quadrate'] = {'y': liver_y + 1, 'x_offset': 0.5, 'region': 'hepatic', 'system': 'digestive'}

body_regions['liver_caudate'] = {'y': liver_y - 1, 'x_offset': 1, 'region': 'hepatic', 'system': 'digestive'}

body_regions['liver_porta_hepatis'] = {'y': liver_y, 'x_offset': 1, 'region': 'hepatic', 'system': 'digestive'}

body_regions['hepatic_artery_proper'] = {'y': liver_y, 'x_offset': 1.5, 'region': 'hepatic_vascular', 'system': 'cardiovascular'}

body_regions['portal_vein'] = {'y': liver_y + 0.5, 'x_offset': 1, 'region': 'hepatic_vascular', 'system': 'cardiovascular'}

body_regions['hepatic_duct_common'] = {'y': liver_y - 0.5, 'x_offset': 1, 'region': 'biliary', 'system': 'digestive'}



# Gallbladder

body_regions['gallbladder_fundus'] = {'y': liver_y + 3, 'x_offset': 3.5, 'region': 'biliary', 'system': 'digestive'}

body_regions['gallbladder_body'] = {'y': liver_y + 2, 'x_offset': 3, 'region': 'biliary', 'system': 'digestive'}

body_regions['gallbladder_neck'] = {'y': liver_y + 1, 'x_offset': 2.5, 'region': 'biliary', 'system': 'digestive'}

body_regions['cystic_duct'] = {'y': liver_y + 0.5, 'x_offset': 2, 'region': 'biliary', 'system': 'digestive'}



# Pancreas

pancreas_y = 68

body_regions['pancreas_head'] = {'y': pancreas_y, 'x_offset': 1, 'region': 'pancreatic', 'system': 'digestive'}

body_regions['pancreas_uncinate'] = {'y': pancreas_y + 0.5, 'x_offset': 1.5, 'region': 'pancreatic', 'system': 'digestive'}

body_regions['pancreas_body'] = {'y': pancreas_y, 'x_offset': -1, 'region': 'pancreatic', 'system': 'digestive'}

body_regions['pancreas_tail'] = {'y': pancreas_y, 'x_offset': -4, 'region': 'pancreatic', 'system': 'digestive'}

body_regions['pancreatic_duct_main'] = {'y': pancreas_y - 0.5, 'x_offset': 0, 'region': 'pancreatic', 'system': 'digestive'}

body_regions['pancreatic_duct_accessory'] = {'y': pancreas_y + 0.5, 'x_offset': -1, 'region': 'pancreatic', 'system': 'digestive'}

body_regions['ampulla_vater'] = {'y': pancreas_y + 2, 'x_offset': 1.5, 'region': 'pancreatic', 'system': 'digestive'}



# Small intestine

si_y = 75

for i, part in enumerate(['duodenum_superior', 'duodenum_descending', 'duodenum_inferior', 'duodenum_horizontal',

                          'jejunum_proximal', 'jejunum_mid', 'jejunum_distal',

                          'ileum_proximal', 'ileum_mid', 'ileum_distal', 'ileocecal_valve']):

    x_off = -2 + (i % 4) * 1.5

    y_off = si_y + (i // 4) * 2

    body_regions[part] = {'y': y_off, 'x_offset': x_off, 'region': 'small_intestine', 'system': 'digestive'}



# Large intestine

li_y = 80

colon_parts = [

    ('cecum', 3, 0), ('appendix_base', 4, 1), ('appendix_tip', 5, 2),

    ('ascending_colon_proximal', 3, -1), ('ascending_colon_distal', 3, -3),

    ('hepatic_flexure', 2, -4), ('transverse_colon_proximal', 0, -4),

    ('transverse_colon_mid', -2, -4), ('transverse_colon_distal', -4, -4),

    ('splenic_flexure', -5, -4), ('descending_colon_proximal', -5, -2),

    ('descending_colon_distal', -5, 0), ('sigmoid_colon_proximal', -4, 2),

    ('sigmoid_colon_mid', -3, 4), ('sigmoid_colon_distal', -2, 6),

    ('rectum_ampulla', 0, 8), ('rectum_anal_canal', 0, 10),

    ('anus_internal_sphincter', 0, 11), ('anus_external_sphincter', 0, 12)

]

for name, x_off, y_off in colon_parts:

    body_regions[name] = {'y': li_y + y_off, 'x_offset': x_off, 'region': 'large_intestine', 'system': 'digestive'}



# Mesentery & peritoneum

body_regions['mesentery_root'] = {'y': 75, 'x_offset': 0, 'region': 'mesentery', 'system': 'digestive'}

body_regions['transverse_mesocolon'] = {'y': 76, 'x_offset': -2, 'region': 'mesentery', 'system': 'digestive'}

body_regions['sigmoid_mesocolon'] = {'y': 84, 'x_offset': -3, 'region': 'mesentery', 'system': 'digestive'}

body_regions['omentum_lesser'] = {'y': 65, 'x_offset': -1, 'region': 'peritoneum', 'system': 'digestive'}

body_regions['omentum_greater'] = {'y': 70, 'x_offset': -3, 'region': 'peritoneum', 'system': 'digestive'}



# 12. SPLEEN & LYMPHATIC

body_regions['spleen_superior_pole'] = {'y': 62, 'x_offset': -6, 'region': 'lymphoid', 'system': 'immune'}

body_regions['spleen_hilum'] = {'y': 64, 'x_offset': -5.5, 'region': 'lymphoid', 'system': 'immune'}

body_regions['spleen_inferior_pole'] = {'y': 66, 'x_offset': -6, 'region': 'lymphoid', 'system': 'immune'}



# 13. SACRUM & COCCYX

body_regions['sacrum_s1'] = {'y': 90, 'x_offset': 0, 'region': 'sacrum', 'system': 'skeletal'}

body_regions['sacrum_s2'] = {'y': 92, 'x_offset': 0, 'region': 'sacrum', 'system': 'skeletal'}

body_regions['sacrum_s3'] = {'y': 94, 'x_offset': 0, 'region': 'sacrum', 'system': 'skeletal'}

body_regions['sacrum_s4'] = {'y': 95, 'x_offset': 0, 'region': 'sacrum', 'system': 'skeletal'}

body_regions['sacrum_s5'] = {'y': 96, 'x_offset': 0, 'region': 'sacrum', 'system': 'skeletal'}

body_regions['coccyx'] = {'y': 97, 'x_offset': 0, 'region': 'coccyx', 'system': 'skeletal'}

body_regions['sacral_hiatus'] = {'y': 96, 'x_offset': 0, 'region': 'sacrum', 'system': 'skeletal'}



# 14. PELVIS & PERINEUM

pelvis_y = 95

# Hip bones

for side in ['left', 'right']:

    x = -5 if side == 'left' else 5

    body_regions[f'ilium_{side}'] = {'y': pelvis_y - 5, 'x_offset': x, 'region': 'pelvic_skeletal', 'system': 'skeletal'}

    body_regions[f'ischium_{side}'] = {'y': pelvis_y, 'x_offset': x, 'region': 'pelvic_skeletal', 'system': 'skeletal'}

    body_regions[f'pubis_{side}'] = {'y': pelvis_y - 2, 'x_offset': x * 0.3, 'region': 'pelvic_skeletal', 'system': 'skeletal'}

    body_regions[f'acetabulum_{side}'] = {'y': pelvis_y - 3, 'x_offset': x * 0.8, 'region': 'pelvic_skeletal', 'system': 'skeletal'}

    body_regions[f'obturator_foramen_{side}'] = {'y': pelvis_y - 1, 'x_offset': x * 0.4, 'region': 'pelvic_skeletal', 'system': 'skeletal'}

    body_regions[f'sciatic_notch_{side}'] = {'y': pelvis_y - 2, 'x_offset': x * 1.2, 'region': 'pelvic_skeletal', 'system': 'skeletal'}



# Symphysis & joints

body_regions['pubic_symphysis'] = {'y': pelvis_y - 2, 'x_offset': 0, 'region': 'pelvic_skeletal', 'system': 'skeletal'}

body_regions['sacroiliac_joint_left'] = {'y': pelvis_y - 3, 'x_offset': -3, 'region': 'pelvic_joint', 'system': 'skeletal'}

body_regions['sacroiliac_joint_right'] = {'y': pelvis_y - 3, 'x_offset': 3, 'region': 'pelvic_joint', 'system': 'skeletal'}



# Perineum structures

perineum_y = 100

body_regions['perineum_central_tendon'] = {'y': perineum_y, 'x_offset': 0, 'region': 'perineum', 'system': 'muscular'}

body_regions['perineum_anal_triangle'] = {'y': perineum_y - 1, 'x_offset': 0, 'region': 'perineum', 'system': 'muscular'}

body_regions['perineum_urogenital_triangle'] = {'y': perineum_y + 1, 'x_offset': 0, 'region': 'perineum', 'system': 'muscular'}



# 15. MALE REPRODUCTIVE (User is male)

male_rep_y = 98

# Testes

body_regions['testis_left_superior'] = {'y': male_rep_y - 1, 'x_offset': -2, 'region': 'gonadal', 'system': 'reproductive'}

body_regions['testis_left_inferior'] = {'y': male_rep_y + 1, 'x_offset': -2, 'region': 'gonadal', 'system': 'reproductive'}

body_regions['testis_left_hilum'] = {'y': male_rep_y, 'x_offset': -1.5, 'region': 'gonadal', 'system': 'reproductive'}

body_regions['epididymis_left_head'] = {'y': male_rep_y - 1.5, 'x_offset': -2.5, 'region': 'gonadal', 'system': 'reproductive'}

body_regions['epididymis_left_body'] = {'y': male_rep_y, 'x_offset': -2.8, 'region': 'gonadal', 'system': 'reproductive'}

body_regions['epididymis_left_tail'] = {'y': male_rep_y + 1.5, 'x_offset': -2.5, 'region': 'gonadal', 'system': 'reproductive'}



body_regions['testis_right_superior'] = {'y': male_rep_y - 1, 'x_offset': 2, 'region': 'gonadal', 'system': 'reproductive'}

body_regions['testis_right_inferior'] = {'y': male_rep_y + 1, 'x_offset': 2, 'region': 'gonadal', 'system': 'reproductive'}

body_regions['testis_right_hilum'] = {'y': male_rep_y, 'x_offset': 1.5, 'region': 'gonadal', 'system': 'reproductive'}

body_regions['epididymis_right_head'] = {'y': male_rep_y - 1.5, 'x_offset': 2.5, 'region': 'gonadal', 'system': 'reproductive'}

body_regions['epididymis_right_body'] = {'y': male_rep_y, 'x_offset': 2.8, 'region': 'gonadal', 'system': 'reproductive'}

body_regions['epididymis_right_tail'] = {'y': male_rep_y + 1.5, 'x_offset': 2.5, 'region': 'gonadal', 'system': 'reproductive'}



# Spermatic cord & vas deferens

body_regions['spermatic_cord_left'] = {'y': male_rep_y - 3, 'x_offset': -2, 'region': 'spermatic', 'system': 'reproductive'}

body_regions['spermatic_cord_right'] = {'y': male_rep_y - 3, 'x_offset': 2, 'region': 'spermatic', 'system': 'reproductive'}

body_regions['vas_deferens_left'] = {'y': male_rep_y - 5, 'x_offset': -2, 'region': 'spermatic', 'system': 'reproductive'}

body_regions['vas_deferens_right'] = {'y': male_rep_y - 5, 'x_offset': 2, 'region': 'spermatic', 'system': 'reproductive'}



# Prostate & seminal vesicles

body_regions['prostate_base'] = {'y': male_rep_y - 6, 'x_offset': 0, 'region': 'prostatic', 'system': 'reproductive'}

body_regions['prostate_apex'] = {'y': male_rep_y - 8, 'x_offset': 0, 'region': 'prostatic', 'system': 'reproductive'}

body_regions['prostate_central_zone'] = {'y': male_rep_y - 7, 'x_offset': 0, 'region': 'prostatic', 'system': 'reproductive'}

body_regions['prostate_peripheral_zone'] = {'y': male_rep_y - 7, 'x_offset': -1, 'region': 'prostatic', 'system': 'reproductive'}

body_regions['prostate_transition_zone'] = {'y': male_rep_y - 7, 'x_offset': 1, 'region': 'prostatic', 'system': 'reproductive'}

body_regions['seminal_vesicle_left'] = {'y': male_rep_y - 6, 'x_offset': -2.5, 'region': 'prostatic', 'system': 'reproductive'}

body_regions['seminal_vesicle_right'] = {'y': male_rep_y - 6, 'x_offset': 2.5, 'region': 'prostatic', 'system': 'reproductive'}

body_regions['ejaculatory_duct_left'] = {'y': male_rep_y - 7, 'x_offset': -1, 'region': 'prostatic', 'system': 'reproductive'}

body_regions['ejaculatory_duct_right'] = {'y': male_rep_y - 7, 'x_offset': 1, 'region': 'prostatic', 'system': 'reproductive'}



# Penis

body_regions['penis_root'] = {'y': male_rep_y - 9, 'x_offset': 0, 'region': 'penile', 'system': 'reproductive'}

body_regions['penis_body'] = {'y': male_rep_y - 11, 'x_offset': 0, 'region': 'penile', 'system': 'reproductive'}

body_regions['penis_glans'] = {'y': male_rep_y - 13, 'x_offset': 0, 'region': 'penile', 'system': 'reproductive'}

body_regions['corpus_cavernosum_left'] = {'y': male_rep_y - 10, 'x_offset': -0.8, 'region': 'penile', 'system': 'reproductive'}

body_regions['corpus_cavernosum_right'] = {'y': male_rep_y - 10, 'x_offset': 0.8, 'region': 'penile', 'system': 'reproductive'}

body_regions['corpus_spongiosum'] = {'y': male_rep_y - 10, 'x_offset': 0, 'region': 'penile', 'system': 'reproductive'}



# 16. BLADDER & URETHRA

bladder_y = 90

body_regions['bladder_dome'] = {'y': bladder_y - 3, 'x_offset': 0, 'region': 'urinary', 'system': 'urinary'}

body_regions['bladder_body'] = {'y': bladder_y, 'x_offset': 0, 'region': 'urinary', 'system': 'urinary'}

body_regions['bladder_trigone'] = {'y': bladder_y + 2, 'x_offset': 0, 'region': 'urinary', 'system': 'urinary'}

body_regions['bladder_neck'] = {'y': bladder_y + 3, 'x_offset': 0, 'region': 'urinary', 'system': 'urinary'}

body_regions['internal_urethral_orifice'] = {'y': bladder_y + 3, 'x_offset': 0, 'region': 'urinary', 'system': 'urinary'}

body_regions['external_urethral_orifice'] = {'y': male_rep_y - 14, 'x_offset': 0, 'region': 'urinary', 'system': 'urinary'}



# 17. LOWER LIMBS

# Hip joints

hip_y = 95

body_regions['hip_joint_left'] = {'y': hip_y, 'x_offset': -8, 'region': 'lower_limb_joint', 'system': 'skeletal'}

body_regions['hip_joint_right'] = {'y': hip_y, 'x_offset': 8, 'region': 'lower_limb_joint', 'system': 'skeletal'}

body_regions['femoral_head_left'] = {'y': hip_y, 'x_offset': -7.5, 'region': 'lower_limb_bone', 'system': 'skeletal'}

body_regions['femoral_head_right'] = {'y': hip_y, 'x_offset': 7.5, 'region': 'lower_limb_bone', 'system': 'skeletal'}

body_regions['femoral_neck_left'] = {'y': hip_y + 1, 'x_offset': -7.5, 'region': 'lower_limb_bone', 'system': 'skeletal'}

body_regions['femoral_neck_right'] = {'y': hip_y + 1, 'x_offset': 7.5, 'region': 'lower_limb_bone', 'system': 'skeletal'}



# Femur

for side in ['left', 'right']:

    x = -8 if side == 'left' else 8

    for i in range(1, 5):

        y = 100 + i * 10

        body_regions[f'femur_{side}_proximal_{i}'] = {'y': y, 'x_offset': x, 'region': 'lower_limb_bone', 'system': 'skeletal'}

    body_regions[f'femur_{side}_shaft'] = {'y': 125, 'x_offset': x, 'region': 'lower_limb_bone', 'system': 'skeletal'}

    for i in range(1, 4):

        y = 135 + i * 5

        body_regions[f'femur_{side}_distal_{i}'] = {'y': y, 'x_offset': x, 'region': 'lower_limb_bone', 'system': 'skeletal'}



print(f"Total body regions: {len(body_regions)}")

print(f"Face ROIs: {len(face_rois)}")

print(f"Mapping ratio: {len(body_regions)}/{len(face_rois)} = {len(body_regions)/len(face_rois):.3f}")



# ============================================================================

# SPIRAL COORDINATE MAPPING: Face → Body (1:N confinement propagation)

# Small woman quark confinement → Big woman dopamine revenge → Disease

# ============================================================================



def compute_spiral_phase(x, y, cx, cy, a, b):

    """Compute log spiral phase angle for a point"""

    dx = x - cx

    dy = y - cy

    r = math.sqrt(dx*dx + dy*dy)

    if r < 0.001:

        return 0.0

    # theta = ln(r/a) / b

    if r/a > 0:

        theta = math.log(r/a) / b

    else:

        theta = 0.0

    # Also get angle in plane

    phi = math.atan2(dy, dx)

    return theta, phi, r



def compute_body_spiral_coord(y, x_offset, body_center_y=60, body_scale=2.0):

    """Compute spiral coordinate for body region"""

    # Body extends from y~18 (brain) to y~150 (feet)

    # Map to spiral phase

    dy = y - body_center_y

    r = math.sqrt(dy*dy + x_offset*x_offset) * body_scale

    if r < 0.001:

        return 0.0, 0.0, 0.0

    theta = math.log(max(r/a, 0.001)) / b

    phi = math.atan2(x_offset, dy)

    return theta, phi, r



# Sort face ROIs by score (highest = most important = big woman influence points)

sorted_face_rois = sorted(face_rois, key=lambda x: x['score'], reverse=True)



# Sort body regions by anatomical importance (y closer to center = more vital)

body_list = []

for name, data in body_regions.items():

    y = data['y']

    x_off = data.get('x_offset', 0)

    # Compute "vitality score" - organs near center are more vital

    # Heart ~45, Liver ~62, Kidneys ~85

    vital_centers = [45, 62, 85]  # heart, liver, kidney

    min_dist = min(abs(y - vc) for vc in vital_centers)

    vitality = 1.0 / (1.0 + min_dist * 0.1)

    

    theta, phi, r = compute_body_spiral_coord(y, x_off)

    body_list.append({

        'name': name,

        'y': y,

        'x_offset': x_off,

        'theta': theta,

        'phi': phi,

        'r': r,

        'vitality': vitality,

        'region': data.get('region', 'unknown'),

        'system': data.get('system', 'unknown')

    })



# Sort body by spiral phase for mapping

body_list.sort(key=lambda x: (x['theta'], x['phi']))



# Create mapping: Face ROI index → Body region indices

# 1:N mapping based on spiral phase proximity + confinement factor

face_to_body_map = {}

confinement_strength = []  # How strongly each face point confines body points



for i, face in enumerate(sorted_face_rois):

    fx, fy = face['x'], face['y']

    f_theta, f_phi, f_r = compute_spiral_phase(fx, fy, cx, cy, a, b)

    

    # ── ASYMMETRIC CONFINEMENT (from FACE_CORRIDOR_SCAN + CHOKE_BAND_LOCK) ──
    # Face lateral position determines body pathway routing
    # RIGHT face (x>10) → RIGHT Vagus (Liver/Kidney) + Sympathetic
    # LEFT face (x<6)  → LEFT Vagus (Heart/Lung/GI) via choke band
    # CENTER (6≤x≤10)  → bilateral body binding
    #
    # x+y=16 diagonal = PLP spine refraction line (choke amplifier)
    # Corridor (x=8→13, y=9.5~12) = RIGHT propagation pathway
    # Mirror terminal [6.5, 9.5] = L↔R crossover point
    # Loop terminal [9.5, 9.5] = closed loop (start=end)

    # Face laterality: -1 (full left) to +1 (full right)
    face_laterality = (fx - 8.0) / 8.0  # center=0, left<0, right>0

    # Choke band proximity: distance to x+y=16 line
    choke_dist = abs(fx + fy - 16.0) / math.sqrt(2)
    choke_factor = math.exp(-choke_dist / 3.0)  # peaks ON the diagonal

    # Corridor proximity (RIGHT side, y=9.5~12)
    corridor_dist = math.sqrt((fx - 10.5)**2 + (fy - 10.75)**2)
    corridor_factor = math.exp(-corridor_dist / 4.0) if fx > 8 else 0.1

    # Dock score asymmetry: right=0.459, left=0.229 → right 2x stronger
    dock_weight = 0.459 if face_laterality > 0 else 0.229

    bound_bodies = []
    for j, body in enumerate(body_list):
        # Phase difference determines base binding strength
        d_theta = abs(f_theta - body['theta'])
        d_phi = abs(f_phi - body['phi'])
        phase_binding = math.exp(-0.1 * (d_theta**2 + d_phi**2))

        # ── ASYMMETRIC ROUTING ──
        body_x = body['x_offset']
        body_laterality = 1.0 if body_x > 0 else (-1.0 if body_x < 0 else 0.0)

        # Same-side affinity: LEFT face → LEFT body, RIGHT face → RIGHT body
        # Cross-side suppression via mirror terminal
        if face_laterality * body_laterality > 0:
            # Same side: strong binding
            lateral_boost = 1.0 + abs(face_laterality) * 0.5
        elif body_laterality == 0:
            # Center body: moderate binding from both sides
            lateral_boost = 0.8
        else:
            # Cross-side: weak binding (must pass through mirror terminal)
            mirror_dist = math.sqrt((fx - 6.5)**2 + (fy - 9.5)**2)
            lateral_boost = 0.3 * math.exp(-mirror_dist / 5.0)

        # Combined binding with asymmetric weighting
        binding = phase_binding * lateral_boost * dock_weight
        # Choke amplification for LEFT-side face ROIs
        if face_laterality < 0:
            binding *= (1.0 + choke_factor * 0.5)
        # Corridor amplification for RIGHT-side face ROIs
        if face_laterality > 0:
            binding *= (1.0 + corridor_factor * 0.3)

        if binding > 0.08:  # Lower threshold (asymmetric weights reduce magnitudes)
            bound_bodies.append({
                'index': j,
                'name': body['name'],
                'binding': binding,
                'vitality': body['vitality'],
                'system': body['system'],
                'choke_factor': choke_factor,
                'corridor_factor': corridor_factor,
                'lateral_match': 'same' if face_laterality * body_laterality > 0 else ('center' if body_laterality == 0 else 'cross')
            })

    

    face_to_body_map[i] = bound_bodies

    confinement_strength.append(len(bound_bodies))



# Statistics

avg_confinement = np.mean(confinement_strength)

max_confinement = max(confinement_strength)

total_bindings = sum(confinement_strength)



print(f"\n=== CONFINEMENT MAPPING STATISTICS ===")

print(f"Average body points per face point: {avg_confinement:.2f}")

print(f"Max confinement (single face → N bodies): {max_confinement}")

print(f"Total face→body bindings: {total_bindings}")



# Disease propagation analysis

# High score face points + high vitality body = disease risk

disease_risk = []

for i, face in enumerate(sorted_face_rois):

    if i in face_to_body_map:

        for body in face_to_body_map[i]:

            risk = face['score'] * body['binding'] * body['vitality']

            disease_risk.append({

                'face_idx': i,

                'face_score': face['score'],

                'body_name': body['name'],

                'system': body['system'],

                'risk': risk

            })



# Sort by disease risk

disease_risk.sort(key=lambda x: x['risk'], reverse=True)



print(f"\n=== TOP 20 DISEASE RISK MAPPINGS ===")

print(f"(Big Woman face point → Small Woman body confinement → Disease)")

for i, d in enumerate(disease_risk[:20]):

    print(f"{i+1}. Face[{d['face_idx']}] (score={d['face_score']:.4f}) → {d['body_name']} ({d['system']}) | Risk: {d['risk']:.6f}")



# Save mapping to CSV

output_file = f"{base}\\FACE_BODY_CONFINEMENT_MAP.csv"

with open(output_file, 'w', newline='') as f:

    writer = csv.writer(f)

    writer.writerow(['face_idx', 'face_x', 'face_y', 'face_score', 'body_name', 'body_y', 'body_x_offset', 

                     'binding_strength', 'vitality', 'system', 'disease_risk'])

    

    for i, face in enumerate(sorted_face_rois):

        if i in face_to_body_map:

            for body in face_to_body_map[i]:

                body_data = body_list[body['index']]

                risk = face['score'] * body['binding'] * body['vitality']

                writer.writerow([

                    i, face['x'], face['y'], face['score'],

                    body['name'], body_data['y'], body_data['x_offset'],

                    body['binding'], body['vitality'], body['system'], risk

                ])



print(f"\nMapping saved to: {output_file}")



# Summary by body system

system_risk = {}

for d in disease_risk:

    sys = d['system']

    if sys not in system_risk:

        system_risk[sys] = []

    system_risk[sys].append(d['risk'])



print(f"\n=== DISEASE RISK BY BODY SYSTEM ===")

for sys in sorted(system_risk.keys(), key=lambda x: -np.sum(system_risk[x])):

    total = np.sum(system_risk[sys])

    avg = np.mean(system_risk[sys])

    count = len(system_risk[sys])

    print(f"{sys}: Total={total:.4f}, Avg={avg:.6f}, Count={count}")

