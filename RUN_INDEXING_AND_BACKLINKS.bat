@echo off
title Antigravity Backlinks & Indexing Suite
cd /d "%~dp0"
echo ===========================================================================
echo ⚡ ANTIGRAVITY MASTER BACKLINKS & MULTI-PROTOCOL INDEXING ENGINE
echo ===========================================================================
python tools\create_and_index_backlinks.py --all
echo.
echo ===========================================================================
echo Report generated: reports\MASTER_LIVE_BACKLINKS_REPORT.xlsx
echo ===========================================================================
pause
