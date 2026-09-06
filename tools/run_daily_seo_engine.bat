@echo off
REM Autonomous Daily SEO Publishing & Crawl Dispatcher
echo [INFO] Starting Autonomous SEO Fleet Engine at %date% %time%...

cd /d "c:\Users\jibra\Desktop\1\digitalcreatoravi"

REM 1. Run Autonomous Publisher
python tools/autonomous_publisher.py --status >> logs/daily_run.log 2>&1

REM 2. Verify all live production sites
python tools/audit_portfolio_all5.py >> logs/daily_run.log 2>&1

REM 3. Dispatch IndexNow Pings
python tools/ping_indexnow.py >> logs/daily_run.log 2>&1

echo [INFO] Daily SEO Fleet Engine completed successfully at %date% %time%.
