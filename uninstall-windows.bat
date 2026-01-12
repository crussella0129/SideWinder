@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: AxisSpline Uninstaller for Windows
:: Removes the Fusion 360 Add-In
:: ============================================================================

echo.
echo  ============================================
echo   AxisSpline Uninstaller for Fusion 360
echo  ============================================
echo.

:: Define the target directory
set "ADDIN_DIR=%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns"
set "TARGET_DIR=%ADDIN_DIR%\AxisSpline"

:: Check if installed
if not exist "%TARGET_DIR%" (
    echo  [INFO] AxisSpline is not installed.
    echo.
    echo  Nothing to remove.
    echo.
    pause
    exit /b 0
)

echo  Found AxisSpline installation at:
echo  %TARGET_DIR%
echo.

set /p CONFIRM="  Are you sure you want to uninstall AxisSpline? (Y/N): "
if /i "!CONFIRM!" neq "Y" (
    echo.
    echo  Uninstallation cancelled.
    echo.
    pause
    exit /b 0
)

echo.
echo  Removing AxisSpline...

:: Remove the directory
rmdir /s /q "%TARGET_DIR%"

if exist "%TARGET_DIR%" (
    echo.
    echo  [ERROR] Could not remove AxisSpline.
    echo  Please close Fusion 360 and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo  ============================================
echo   Uninstallation Successful!
echo  ============================================
echo.
echo  AxisSpline has been removed from Fusion 360.
echo.
echo  If the add-in was running, restart Fusion 360
echo  to complete the removal.
echo.

pause
exit /b 0
