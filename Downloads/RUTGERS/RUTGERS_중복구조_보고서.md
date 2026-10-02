# RUTGERS 안 “거의 완전히 일치하는” 폴더/구조 정리

직접 지울 때 참고용. 아래는 **완전 일치** 또는 **80% 이상 겹치는** 폴더들만 정리한 거예요.

---

## [1] 내용이 완전히 같은 폴더들 (같은 파일구조+같은 개수)

여러 개 나오면 **하나만 남기고 나머지는 지울 후보**입니다.

### evidence_store (파일 2개씩, 3곳 동일)
- `verification\_automation\evidence_store\graphite_scirep_2020_pdf`
- `verification\_automation\evidence_store\blackp_arxiv_1503_06167v1_pdf`
- `verification\_automation\evidence_store\blackp_natcomm_ncomms9573_pdf`

### neuroscience – ds003380 / openneuro_download (동일 구조가 두 군데)
`verification\domains\neuroscience\_merged_from_neuro\evidence\external_openneuro_ds003380\` 아래:

- **ds003380** vs **openneuro_download** 가 쌍으로 거의 같은 구조
- `ds003380\sub-01` ~ `sub-12` ↔ `openneuro_download\sub-01` ~ `sub-12` (각각 동일)
- `ds003380\sub-XX\eeg` ↔ `openneuro_download\sub-XX\eeg` (각각 동일)
- `.git\refs\heads` vs `.git\logs\refs\heads` 등 git 내부 폴더도 동일 구조 2벌

→ **한쪽만 남기고** (예: `openneuro_download` 또는 `ds003380` 하나만 두고) 나머지 통째로 지우면 중복 제거됨.

### particle_physics evidence vs quarantine_auto 복사본
- `verification\domains\particle_physics\evidence\qec_p_th_1108_5738`  
  ↔ `verification\_automation\_outputs\quarantine_auto\QEC_PTH_EXPANSION__20260111_071430Z\qec_p_th_1108_5738`
- `verification\domains\particle_physics\evidence\qec_p_th_2106_02621`  
  ↔ `...\quarantine_auto\...\qec_p_th_2106_02621`
- `verification\domains\particle_physics\evidence\qec_p_th_2208_02191`  
  ↔ `...\quarantine_auto\...\qec_p_th_2208_02191`

→ **evidence**가 원본이면 quarantine 쪽 복사본 삭제, 반대면 evidence 쪽 삭제.

### automation outputs – audit / anchor_audit
- `verification\_automation\_outputs\audit`
- `verification\_automation\_outputs\anchor_audit`  
→ 구조 동일. 하나만 쓰면 되면 하나만 남기기.

### __pycache__
- `verification\_automation\RCAEval-main\RCAEval\__pycache__`
- `verification\_automation\RCAEval-main\RCAEval\utility\__pycache__`  
→ 둘 다 빌드 캐시. 지워도 다시 생기므로, 정리하려면 둘 다 삭제해도 됨.

---

## [2] 한 폴더가 다른 폴더 “안에” 들어있는 구조 (내장된 중복)

스크립트 기준으로는 “상위/하위 겹침 50% 이상”인 경우만 뽑았는데, 이번 rutgers에서는 별도로 더 찾은 건 없음.  
위 [1]에 나온 `ds003380` vs `openneuro_download` 가 “한 트리 안에 같은 구조가 두 벌” 있는 대표 예시.

---

## [3] 파일 목록 80% 이상 겹치는 폴더쌍 (이름/경로 기준)

아래는 **쌍으로** 묶어서 보면 됩니다. 한쪽만 남기고 한쪽 지우면 됨.

| 한쪽 경로 | 다른쪽 경로 | 비고 |
|-----------|--------------|------|
| `verification\_automation\RCAEval-main\RCAEval\__pycache__` | `...\RCAEval\utility\__pycache__` | 둘 다 캐시, 둘 다 삭제 가능 |
| `verification\_automation\_outputs\anchor_audit` | `...\audit` | 하나만 남기기 |
| `verification\_automation\_outputs\quarantine_auto\...\qec_p_th_1108_5738` | `verification\domains\particle_physics\evidence\qec_p_th_1108_5738` | 한쪽만 남기기 |
| `verification\_automation\_outputs\quarantine_auto\...\qec_p_th_2106_02621` | `verification\domains\particle_physics\evidence\qec_p_th_2106_02621` | 한쪽만 남기기 |
| `verification\_automation\_outputs\quarantine_auto\...\qec_p_th_2208_02191` | `verification\domains\particle_physics\evidence\qec_p_th_2208_02191` | 한쪽만 남기기 |
| `verification\_automation\evidence_store\bio_pmc5686090_proton_leak_primary` | `...\bio_pmc6800189_proton_leak_ros_primary` | 구조 거의 동일, 하나만 남기기 |
| `...\evidence_store\blackp_arxiv_1503_06167v1_pdf` | `...\blackp_natcomm_ncomms9573_pdf` | 위 [1]과 동일 3개 중 2개 |
| `...\blackp_arxiv_1503_06167v1_pdf` | `...\graphite_scirep_2020_pdf` | 위 [1]과 동일 3개 중 2개 |
| `...\ds003380\sub-01` ~ `sub-12` | `...\openneuro_download\sub-01` ~ `sub-12` | 각 sub-XX 쌍별로 한쪽만 남기기 |
| `...\ds003380\sub-XX\eeg` | `...\openneuro_download\sub-XX\eeg` | 위와 같이 같은 sub 내에서 한쪽만 |
| `...\ds003380\.git\refs\heads` | `...\ds003380\.git\logs\refs\heads` | git 내부, 필요 없으면 둘 다 삭제 가능 |
| `verification\domains\seismology\evidence\...\global_earthquakes_net_M5` | `verification\domains\space_weather\evidence\...\solar_wind_speed700` | 도메인 다르지만 파일 목록만 80% 겹침 → 내용 확인 후 하나만 남길지 결정 |

---

## 지울 때 추천 순서

1. **캐시/자동 생성물**  
   - `__pycache__` 전부  
   - `verification\_automation\_outputs\audit` vs `anchor_audit` 중 하나
2. **evidence_store**  
   - graphite_scirep / blackp_arxiv / blackp_natcomm 셋 중 실제로 쓰는 것만 남기고 나머지 삭제
3. **ds003380 vs openneuro_download**  
   - 하나만 “원본”으로 정하고, 다른 쪽 통째로 삭제
4. **particle_physics evidence vs quarantine_auto**  
   - 원본/백업 역할 정한 뒤, 복사본 쪽만 삭제
5. **그 외 80% 겹침 쌍**  
   - 위 표 보면서 “이 경로는 남긴다 / 이 경로는 지운다”만 정해서 한쪽만 삭제

실제 삭제는 탐색기나 터미널에서 위 경로만 보고 **직접** 지우시면 됩니다.
