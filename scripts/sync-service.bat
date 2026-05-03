@echo off
setlocal

set "SERVICE_NAME=SkillSync"
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

if "%~1"=="" goto :usage
if /i "%~1"=="install" goto :install
if /i "%~1"=="uninstall" goto :uninstall
if /i "%~1"=="status" goto :status
goto :usage

:install
echo Installing %SERVICE_NAME% service...
nssm install %SERVICE_NAME% "node" "scripts\sync-watch.js"
nssm set %SERVICE_NAME% AppDirectory "%PROJECT_ROOT%"
nssm set %SERVICE_NAME% DisplayName "Skill Auto Sync Service"
nssm set %SERVICE_NAME% Description "Monitors source skills folder and auto-syncs to project with git push"
nssm set %SERVICE_NAME% Start SERVICE_AUTO_START
nssm set %SERVICE_NAME% AppRestartDelay 10000
nssm set %SERVICE_NAME% AppStdout "%PROJECT_ROOT%\sync-service.log"
nssm set %SERVICE_NAME% AppStderr "%PROJECT_ROOT%\sync-service-error.log"
nssm set %SERVICE_NAME% AppRotateFiles 1
nssm set %SERVICE_NAME% AppRotateBytes 1048576
nssm start %SERVICE_NAME%
echo %SERVICE_NAME% service installed and started successfully.
goto :eof

:uninstall
echo Uninstalling %SERVICE_NAME% service...
nssm stop %SERVICE_NAME%
nssm remove %SERVICE_NAME% confirm
echo %SERVICE_NAME% service uninstalled successfully.
goto :eof

:status
nssm status %SERVICE_NAME%
goto :eof

:usage
echo Usage: sync-service.bat [install^|uninstall^|status]
echo   install   - Install SkillSync as Windows service (requires admin)
echo   uninstall - Remove SkillSync Windows service (requires admin)
echo   status    - Check SkillSync service status
goto :eof
