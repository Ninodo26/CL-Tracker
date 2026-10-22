# Schedule Option B (Smart Hybrid Matchday Pipeline on Windows)
# Drop 1: 18:00 (Always posts: Pre-Match Preview on matchdays, or Story/Odds on off-days)
# Drop 2: 23:00 (Only posts on Matchdays right after full-time results!)

$ScriptPath = Join-Path $PSScriptRoot "run_daily_tiktok.bat"
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# 1. 18:00 Daily Drop
$Action1 = New-ScheduledTaskAction -Execute $ScriptPath -Argument "1800"
$Trigger1 = New-ScheduledTaskTrigger -Daily -At 18:00
Register-ScheduledTask -TaskName "CL-Tracker-DailyDrop-1800" -Action $Action1 -Trigger $Trigger1 -Settings $Settings -Force
Write-Host "✅ Registered 'CL-Tracker-DailyDrop-1800' at 18:00 (Daily Preview & Story drop)" -ForegroundColor Green

# 2. 23:00 Matchday Reaction
$Action2 = New-ScheduledTaskAction -Execute $ScriptPath -Argument "2300"
$Trigger2 = New-ScheduledTaskTrigger -Daily -At 23:00
Register-ScheduledTask -TaskName "CL-Tracker-MatchdayReaction-2300" -Action $Action2 -Trigger $Trigger2 -Settings $Settings -Force
Write-Host "✅ Registered 'CL-Tracker-MatchdayReaction-2300' at 23:00 (Post-match reaction only when matches play)" -ForegroundColor Green

# Clean up older tasks
Unregister-ScheduledTask -TaskName "CL-Tracker-Daily-TikTok" -Confirm:$false -ErrorAction SilentlyContinue
Unregister-ScheduledTask -TaskName "CL-Tracker-PreMatch-1800" -Confirm:$false -ErrorAction SilentlyContinue
Unregister-ScheduledTask -TaskName "CL-Tracker-PostMatch-2300" -Confirm:$false -ErrorAction SilentlyContinue
