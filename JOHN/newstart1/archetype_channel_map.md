# Archetype Channel Map (Day/Night)

## Archetype Day/Night Mapping
- EW: day=`muon`, night=`gluon`
- IW: day=`quark`, night=`electron`
- IM: day=`neutrino`, night=`higgs`
- EM: day=`photon`, night=`tau`

## Category Counts
- cross_time: 12
- day_day: 6
- night_night: 6
- self_transition: 4

## Channel Classification
| Channel | Edge | Archetypes | Phases | Category | Tag |
|---|---|---|---|---|---|
| `right_alpha_2` | `(muon, tau)` | EW–EM | day–night | cross_time | EW_day × EM_night |
| `vasopressin_female` | `(higgs, muon)` | IM–EW | night–day | cross_time | EW_day × IM_night |
| `right_self_satisfaction` | `(muon, electron)` | EW–IW | day–night | cross_time | EW_day × IW_night |
| `right_extraversion` | `(gluon, photon)` | EW–EM | night–day | cross_time | EW_night × EM_day |
| `male_right_extraversion` | `(gluon, neutrino)` | EW–IM | night–day | cross_time | EW_night × IM_day |
| `gdh_gluon` | `(quark, gluon)` | IW–EW | day–night | cross_time | EW_night × IW_day |
| `right_occipitalis_gaba_a` | `(neutrino, tau)` | IM–EM | day–night | cross_time | IM_day × EM_night |
| `male_gaba_b` | `(photon, higgs)` | EM–IM | day–night | cross_time | IM_night × EM_day |
| `glucocorticoid` | `(quark, tau)` | IW–EM | day–night | cross_time | IW_day × EM_night |
| `right_androgen` | `(quark, higgs)` | IW–IM | day–night | cross_time | IW_day × IM_night |
| `right_5ht1b_synchrotron` | `(photon, electron)` | EM–IW | day–night | cross_time | IW_night × EM_day |
| `male_oxytocin` | `(neutrino, electron)` | IM–IW | day–night | cross_time | IW_night × IM_day |
| `left_self_satisfaction` | `(photon, muon)` | EM–EW | day–day | day_day | EW_day × EM_day |
| `right_dopamine` | `(neutrino, muon)` | IM–EW | day–day | day_day | EW_day × IM_day |
| `muscle_b` | `(quark, muon)` | IW–EW | day–day | day_day | EW_day × IW_day |
| `male_left_5ht` | `(neutrino, photon)` | IM–EM | day–day | day_day | IM_day × EM_day |
| `left_extraversion` | `(quark, photon)` | IW–EM | day–day | day_day | IW_day × EM_day |
| `left_estrogen` | `(quark, neutrino)` | IW–IM | day–day | day_day | IW_day × IM_day |
| `female_gaba_b_latdorsi` | `(gluon, tau)` | EW–EM | night–night | night_night | EW_night × EM_night |
| `hypoxia` | `(gluon, higgs)` | EW–IM | night–night | night_night | EW_night × IM_night |
| `left_frontalis_d2` | `(gluon, electron)` | EW–IW | night–night | night_night | EW_night × IW_night |
| `right_cortisol` | `(higgs, tau)` | IM–EM | night–night | night_night | IM_night × EM_night |
| `left_endorphin` | `(electron, tau)` | IW–EM | night–night | night_night | IW_night × EM_night |
| `left_temporalis_5ht1a` | `(electron, higgs)` | IW–IM | night–night | night_night | IW_night × IM_night |
| `right_acetylcholine` | `(photon, tau)` | EM–EM | day–night | self_transition | EM_day × EM_night |
| `muscle_a` | `(gluon, muon)` | EW–EW | night–day | self_transition | EW_day × EW_night |
| `right_epinephrine` | `(neutrino, higgs)` | IM–IM | day–night | self_transition | IM_day × IM_night |
| `left_epinephrine` | `(quark, electron)` | IW–IW | day–night | self_transition | IW_day × IW_night |
