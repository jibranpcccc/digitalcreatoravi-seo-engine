@echo off
REM Enterprise Daily SEO & Ranking Monitor Runner
cd /d "%~dp0\.."
echo ===================================================
echo EXECUTING DAILY SEO RANKING & INDEXATION AUDIT
echo ===================================================
python tools/daily_ranking_monitor.py
python tools/build_fleet_ui.py
echo ===================================================
echo DAILY MONITOR AUDIT COMPLETE
echo ===================================================
