@echo off
echo ===============================================================
echo ? LAUNCHING AUTONOMOUS SEO FLEET ENGINE & TELEMETRY HUB
echo ===============================================================
echo Opening Fleet Command Dashboard at http://localhost:8088/
start http://localhost:8088/
cscript //nologo tools\launch_fleet_daemon_silently.vbs
echo Autonomous background daemon is running silently.
exit /b 0
