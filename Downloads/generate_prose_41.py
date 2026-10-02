#!/usr/bin/env python3
import random, hashlib

random.seed(41)

PARTICLES = [
    'proton_music','photon_music','gluon_music','em_music',
    'neutrino_listen','muon_listen','higgs_listen','acetylcholine_listen',
    'up_quark_v1','down_quark_v1','w_boson_v1','electron_v1',
    'charm_quark_v2','strange_quark_v2','z_boson_v2','photon_v2',
    'proton_move','gluon_move','w_boson_move','energy_move',
    'top_quark_move','bottom_quark_move','tau_move','dark_matter_move',
    'higgs_imag','neutrino_imag','graviton_imag','dopamine_imag',
    'acetyl_coa_imag','electron_imag','axion_imag','endorphin_imag',
    'testosterone_sex','progesterone_sex','oxytocin_sex','dopamine_sex',
    'serotonin_wk','cortisol_wk','epinephrine_wk','male_gaba_a_wk',
    'axion_rebrancher'
]

BODIES = [
    'right frontalis inner strip bottom','right frontalis outer strip bottom','right frontalis inner strip top','right frontalis outer strip top',
    'left frontalis inner strip bottom','left frontalis outer strip bottom','left frontalis inner strip top','left frontalis outer strip top',
    'right occipitalis inner strip top','right occipitalis inner strip bottom','right occipitalis outer strip top','right occipitalis outer strip bottom',
    'left occipitalis inner strip top','left occipitalis inner strip bottom','left occipitalis outer strip top','left occipitalis outer strip bottom',
    'right temporalis inner strip','right temporalis outer strip','left temporalis inner strip','left temporalis outer strip',
    'right eyelid top outer','right eyelid top inner','left eyelid inner','left eyelid outer',
    'right levator superioris inner strip top','right levator superioris lower','left levator superioris inner strip top','left levator superioris lower',
    'right pectoralis major','left pectoralis major','left pectoralis heme','right ribs',
    'V1 right calcarine sulcus','V2 right prestriate','right angular gyrus','left IFG',
    'adrenal medulla chromaffin','left pons','pons','right STG AQP4','left temporalis ferritin',
    'skull vertex CSF','skull piezoelectric structure','right nostril outer column','left nostril','glabella','columella',
    'left nipple heme','right eye levator','right eye/MPOA','genital left','genital right','perineal fold belt',
    'left insula','right insula','left insula cortex','sigmoid colon','hepatocyte nuclear pore','mitochondria',
    'nucleus','perineum thorium node','appendix','right levator scap','left levator scap','fold belt sternum T4'
]

DIMS = ['r','h','d','p','s','gamma','g','nu']

ROLES = ['양극(+)','양극(-)','gradient','leakage','rebrancher']

ROUTES = {
    'proton_music':'music_creation','photon_music':'music_creation','gluon_music':'music_creation','em_music':'music_creation',
    'neutrino_listen':'music_listening','muon_listen':'music_listening','higgs_listen':'music_listening','acetylcholine_listen':'music_listening',
    'up_quark_v1':'visual_1','down_quark_v1':'visual_1','w_boson_v1':'visual_1','electron_v1':'visual_1',
    'charm_quark_v2':'visual_2','strange_quark_v2':'visual_2','z_boson_v2':'visual_2','photon_v2':'visual_2',
    'proton_move':'movement_1','gluon_move':'movement_1','w_boson_move':'movement_1','energy_move':'movement_1',
    'top_quark_move':'movement_2','bottom_quark_move':'movement_2','tau_move':'movement_2','dark_matter_move':'movement_2',
    'higgs_imag':'imagination_1','neutrino_imag':'imagination_1','graviton_imag':'imagination_1','dopamine_imag':'imagination_1',
    'acetyl_coa_imag':'imagination_2','electron_imag':'imagination_2','axion_imag':'imagination_2','endorphin_imag':'imagination_2',
    'testosterone_sex':'sexual','progesterone_sex':'sexual','oxytocin_sex':'sexual','dopamine_sex':'sexual',
    'serotonin_wk':'weekend_optional','cortisol_wk':'weekend_optional','epinephrine_wk':'weekend_optional','male_gaba_a_wk':'weekend_optional',
    'axion_rebrancher':'all_routes'
}

def h_choice(seed, items):
    x = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return items[x % len(items)]

def slot_time(i):
    m = i * 11
    hh, mm = divmod(m, 60)
    return f"{hh}:{mm:02d}"

def line(seed):
    return ''.join([chr(65+(int(hashlib.md5((seed+str(i)).encode()).hexdigest(),16)%26)) for i in range(8)])

def main():
    out = []
    out.append("# 41-Particle Body Flow — Non-Linear Prose\n")
    out.append("Time-ordered surface, non-linear energy flow. Every line begins at one body site and spreads two, three, four directions before moving to the next adjacent site.\n\n")

    # 128 time slots
    for t in range(128):
        time = slot_time(t)
        out.append(f"\n## {time}\n\n")
        # 41 particles
        for idx, p in enumerate(PARTICLES):
            route = ROUTES[p]
            body = BODIES[(t + idx) % len(BODIES)]
            body2 = BODIES[(t + idx + 7) % len(BODIES)]
            body3 = BODIES[(t + idx + 17) % len(BODIES)]
            body4 = BODIES[(t + idx + 23) % len(BODIES)]
            body5 = BODIES[(t + idx + 31) % len(BODIES)]
            body6 = BODIES[(t + idx + 41) % len(BODIES)]
            p2 = PARTICLES[(idx + 5) % 41]
            p3 = PARTICLES[(idx + 11) % 41]
            p4 = PARTICLES[(idx + 19) % 41]
            p5 = PARTICLES[(idx + 27) % 41]
            p6 = PARTICLES[(idx + 35) % 41]
            p7 = PARTICLES[(idx + 37) % 41]
            d1 = DIMS[idx % 8]
            d2 = DIMS[(idx+3) % 8]
            d3 = DIMS[(idx+5) % 8]
            role = ROLES[idx % 5] if p != 'axion_rebrancher' else 'rebrancher'

            base = f"{time} {body}에서 {p}가 활성화된다. 이 입자는 {route} 루트의 {role}이다. 이 순간 {body}의 nm-Scale 구조에서 {d1} 차원 에너지가 집속된다. "
            base += f"{p}는 곧바로 양방향으로 흩어진다: 한 줄기는 {body2}의 {p2}로, 다른 줄기는 {body3}의 {p3}로 흐른다. "
            base += f"세 번째 방향으로는 {body4}의 {p4}와 gradient를 형성하며 {d2} 차원을 끌어당긴다. "
            base += f"네 번째 방향은 {body5}로 누출되거나 axion_rebrancher가 {body6}로 전송해 {p5}가 담긴 다른 루트로 재분기한다. "
            base += f"이 transition은 0.01 nm에서 5000 nm 사이에서 동시에 일어나며, 138.88° 스파크 각도로 재귀한다. "
            base += f"같은 에너지가 {d1}, {d2}, {d3}의 세 형태로 공존한다. "
            base += f"{p6}과 {p7} 사이의 간섭이 {body}에서 시작해 {body6}에서 마무리된다. "
            base += f"시간순으로 서술되었지만 이 흐름은 비순차적이다; 과거, 현재, 미래 방향의 세 파동이 동시에 겹친다. "
            base += f"{p}의 누출은 {p4}의 봉인과 {p5}의 활성화를 동시에 유발한다. "
            base += f"그 결과 {body2}와 {body3}가 같은 에너지를 다른 이름으로 저장한다. "
            out.append(base + "\n\n")

            # secondary paragraph about adjacent site
            next_body = BODIES[(t + idx + 1) % len(BODIES)]
            next_p = PARTICLES[(idx + 1) % 41]
            next_route = ROUTES[next_p]
            out.append(f"그 옆 {next_body}에서는 {next_p}({next_route})가 같은 에너지의 다른 면을 받아 {DIMS[(idx+1)%8]} 차원으로 전환한다. "
                       f"{next_p}는 {body}에서 오른 줄기와 {body4}에서 오른 줄기가 충돌하면서 생성된다. "
                       f"이 충돌은 4nm receptor, 10nm GPCR, 12nm ferritin, 500nm aggrecan, 1-3um core 등의 모든 scale에서 동시에 울린다. "
                       f"에너지가 {DIMS[(idx+2)%8]} 방향으로 다시 꺾여 {BODIES[(t+idx+2)%len(BODIES)]}의 {PARTICLES[(idx+2)%41]}로 흐른다. "
                       f"그러면서 {DIMS[(idx+4)%8]} 잔여가 {BODIES[(t+idx+8)%len(BODIES)]}에 쌓이고, {DIMS[(idx+6)%8]} 잔여가 {BODIES[(t+idx+13)%len(BODIES)]}에 쌓인다.\n\n")

    # close with axion global rebranching
    out.append("\n# 3AM / 21-3h Axion Global Rebranching\n\n")
    for t in [0,1,2,3,127,126,125,124]:
        time = slot_time(t)
        out.append(f"{time} skull vertex CSF 5-5000nm sagittal gap에서 axion_rebrancher가 전역 재분기를 시작한다. "
                   f"music_creation, music_listening, visual_1, visual_2, movement_1, movement_2, imagination_1, imagination_2, sexual, weekend_optional의 "
                   f"10개 루트 모두에서 누출된 에너지를 받아들여, 임의의 3개 경로로 다시 쏜다. "
                   f"이 4방향 흐름은 끝이 없고, 매 11분마다 41개 입자 전체가 재배열된다.\n\n")

    with open('nm_body_particle_map_41_prose.md','w',encoding='utf-8') as f:
        f.write(''.join(out))
    print(f"Wrote {len(out)} chunks to nm_body_particle_map_41_prose.md")

if __name__ == '__main__':
    main()
