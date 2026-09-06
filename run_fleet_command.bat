@echo off
title Fleet Master Command Center
echo ===================================================
echo [!] STARTING FLEET MASTER COMMAND & TRAFFIC HUB...
echo ===================================================
start "" "http://localhost:8088/"
python tools/fleet_command_server.py
pause
