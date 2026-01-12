@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: AxisSpline Installer for Windows
:: Installs the Fusion 360 Add-In to the correct location
:: ============================================================================

echo.
echo  ============================================
echo   AxisSpline Installer for Fusion 360
echo  ============================================
echo.

:: Check if running as administrator (not required, but informative)
net session >nul 2>&1
if %errorLevel% == 0 (
    echo  Running with administrator privileges
) else (
    echo  Running as standard user
)
echo.

:: Define the target directory
set "ADDIN_DIR=%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns"

:: Check if Fusion 360 AddIns directory exists
if not exist "%ADDIN_DIR%" (
    echo  [ERROR] Fusion 360 AddIns directory not found!
    echo.
    echo  Expected location:
    echo  %ADDIN_DIR%
    echo.
    echo  Please ensure Fusion 360 is installed and has been run at least once.
    echo.
    pause
    exit /b 1
)

echo  Found Fusion 360 AddIns directory:
echo  %ADDIN_DIR%
echo.

:: Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

:: Check if AxisSpline folder exists in the script directory
if not exist "%SCRIPT_DIR%AxisSpline" (
    echo  [ERROR] AxisSpline folder not found!
    echo.
    echo  Please ensure this installer is in the same directory as the AxisSpline folder.
    echo.
    pause
    exit /b 1
)

:: Check if already installed
if exist "%ADDIN_DIR%\AxisSpline" (
    echo  [WARNING] AxisSpline is already installed.
    echo.
    set /p OVERWRITE="  Do you want to overwrite the existing installation? (Y/N): "
    if /i "!OVERWRITE!" neq "Y" (
        echo.
        echo  Installation cancelled.
        echo.
        pause
        exit /b 0
    )
    echo.
    echo  Removing existing installation...
    rmdir /s /q "%ADDIN_DIR%\AxisSpline"
    if exist "%ADDIN_DIR%\AxisSpline" (
        echo  [ERROR] Could not remove existing installation.
        echo  Please close Fusion 360 and try again.
        echo.
        pause
        exit /b 1
    )
)

:: Copy the AxisSpline folder
echo  Installing AxisSpline...
xcopy /e /i /h /y "%SCRIPT_DIR%AxisSpline" "%ADDIN_DIR%\AxisSpline" >nul

if %errorLevel% neq 0 (
    echo.
    echo  [ERROR] Installation failed!
    echo  Error code: %errorLevel%
    echo.
    pause
    exit /b 1
)

:: Verify installation
if exist "%ADDIN_DIR%\AxisSpline\AxisSpline.py" (
    echo.
    echo  ============================================
    echo   Installation Successful!
    echo  ============================================
    echo.
    echo  AxisSpline has been installed to:
    echo  %ADDIN_DIR%\AxisSpline
    echo.
    echo  To activate the add-in:
    echo  1. Open Fusion 360
    echo  2. Go to Utilities ^> Add-Ins ^> Scripts and Add-Ins
    echo  3. Find "AxisSpline" in the Add-Ins tab
    echo  4. Click "Run" to start the add-in
    echo  5. Check "Run on Startup" to auto-load
    echo.
    echo  The add-in will appear in the Solid tab under Scripts/Add-Ins.
    echo.
) else (
    echo.
    echo  [ERROR] Installation verification failed!
    echo  Some files may not have been copied correctly.
    echo.
)

pause
exit /b 0
