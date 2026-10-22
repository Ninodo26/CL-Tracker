@echo off
cd /d "%~dp0\.."
echo ===================================================
echo [CL TRACKER] Running Smart Hybrid TikTok Pipeline
echo ===================================================

set SLOT=%1
if "%SLOT%"=="" (
    for /f "tokens=1 delims=:" %%H in ("%TIME%") do set CURR_HOUR=%%H
    set CURR_HOUR=%CURR_HOUR: =%
    if %CURR_HOUR% GEQ 21 (
        set SLOT=2300
    ) else (
        set SLOT=1800
    )
)

if "%SLOT%"=="2300" (
    echo [CL TRACKER] Slot 23:00 (Post-Match Reaction). Checking if matches were played today...
    python scripts\build_tiktok_video.py --type standings --matchdays-only
) else (
    echo [CL TRACKER] Slot 18:00 (Pre-Match / Story Drop)...
    python scripts\build_tiktok_video.py --type match
)

rem Check if a new video was generated (errorlevel 0)
if %ERRORLEVEL% EQU 0 (
    if exist "%USERPROFILE%\.cl_tiktok_chrome_profile" (
        echo [CL TRACKER] Authenticated TikTok profile found. Auto-posting...
        python scripts\tiktok_publisher.py --auto-post
    ) else (
        echo [CL TRACKER] No saved TikTok session found. Opening video for review...
        python scripts\tiktok_publisher.py --open
    )
) else (
    echo [CL TRACKER] Pipeline exited cleanly (no action needed).
)
