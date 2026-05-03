@echo off
setlocal

set "TASK_NAME=SkillSync"
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "NODE_EXE=D:\apps\nvm4w\nodejs\node.exe"
set "SYNC_SCRIPT=scripts\sync-watch.js"

if "%~1"=="" goto :usage
if /i "%~1"=="install" goto :install
if /i "%~1"=="uninstall" goto :uninstall
if /i "%~1"=="status" goto :status
goto :usage

:install
echo Installing %TASK_NAME% service...
nssm install %TASK_NAME% "%NODE_EXE%" "%SYNC_SCRIPT%"
nssm set %TASK_NAME% AppDirectory "%PROJECT_ROOT%"
nssm set %TASK_NAME% DisplayName "Skill Auto Sync Service"
nssm set %TASK_NAME% Description "Monitors source skills folder and auto-syncs to project with git push"
nssm set %TASK_NAME% Start SERVICE_AUTO_START
nssm set %TASK_NAME% AppRestartDelay 10000
nssm set %TASK_NAME% AppStdout "%PROJECT_ROOT%\sync-service.log"
nssm set %TASK_NAME% AppStderr "%PROJECT_ROOT%\sync-service-error.log"
nssm set %TASK_NAME% AppRotateFiles 1
nssm set %TASK_NAME% AppRotateBytes 1048576
echo.
echo IMPORTANT: Please set the service to run under your user account:
echo   1. Run: nssm edit %TASK_NAME%
echo   2. Go to "Log on" tab
echo   3. Select "This account" and enter your Windows username and password
echo   4. Click "Edit service"
echo.
echo Starting %TASK_NAME%...
nssm start %TASK_NAME%
echo %TASK_NAME% service installed and started.
goto :eof

:uninstall
echo Stopping %TASK_NAME%...
nssm stop %TASK_NAME% 2>nul
echo Removing %TASK_NAME% service...
nssm remove %TASK_NAME% confirm
echo %TASK_NAME% service removed.
goto :eof

:status
nssm status %TASK_NAME% 2>nul || echo %TASK_NAME% service not found.
goto :eof

:usage
echo Usage: sync-service.bat [install^|uninstall^|status]
echo   install   - Install SkillSync as Windows service (requires admin)
echo   uninstall - Remove SkillSync Windows service (requires admin)
echo   status    - Check SkillSync service status
goto :eof
