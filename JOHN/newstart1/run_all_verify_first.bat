@echo off
python verify_continuous_geometry.py || exit /b 1

REM add your runs below (examples)
REM python run_detune_sweep_v4_probabilistic.py
