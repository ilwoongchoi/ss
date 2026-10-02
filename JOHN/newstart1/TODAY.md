# Today: run the 30‑node control + WW2 empathy artifact

## 1) 30‑node “what to do, when” (day/night, forward/reverse)

### A. One-day plan (16 windows)
```powershell
cd d:\Users\user\Documents\newstart
python run_spark_plan_30.py --mode static --days 1 --steps-per-day 16 --recommend --out artifacts\spark_plan_1d.csv
```
- Output: `artifacts/spark_plan_1d.csv` + printed “Top windows” + per-window recommended single-channel flips.

### B. 14-day plan (dynamic integration)
```powershell
cd d:\Users\user\Documents\newstart
python run_spark_plan_30.py --mode dynamic --days 14 --steps-per-day 16 --dt 0.05 --x-clip 8 --topk 16 --recommend --out artifacts\spark_plan_14d.csv
```
- Output: `artifacts/spark_plan_14d.csv` (columns include `day`, `hour`, `gate`, `d3_actual`, `score`).

### C. Live “daemon” (prints what to flip right now)
```powershell
cd d:\Users\user\Documents\newstart
python spark_daemon_30.py
```
Watch mode (every 90 minutes):
```powershell
python spark_daemon_30.py --watch --interval-min 90
```

### Optional: personalize the “no_control” channels
Create a baseline vector for your body/subject and let the phase map overwrite only ON/OFF channels.

Example file: `artifacts\base_c30.json`
```json
{
  "gdh_gluon": 0.5,
  "male_gaba_a": 0.5,
  "right_acetylcholine": 0.5
}
```
Then:
```powershell
python run_spark_plan_30.py --mode dynamic --days 14 --steps-per-day 16 --dt 0.05 --x-clip 8 --base-c30 artifacts\base_c30.json --out artifacts\spark_plan_14d_personal.csv
python spark_daemon_30.py --base-c30 artifacts\base_c30.json
```

## 2) WW2 empathy artifact (Omaha + unified causality chain)

Build the package:
```powershell
cd d:\Users\user\Documents\newstart
python wien\build_ww2_empathy_package.py
```

Outputs:
- `artifacts/ww2_empathy/index.html` (timeline + tables)
- `artifacts/ww2_empathy/unified_events.json`
- `artifacts/ww2_empathy/causality_chain.json`
- `artifacts/ww2_empathy/omaha_beach_immersive.html` (Three.js scene; needs internet for CDN imports)

