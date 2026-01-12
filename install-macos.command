#!/bin/bash

# ============================================================================
# AxisSpline Installer for macOS
# Installs the Fusion 360 Add-In to the correct location
# ============================================================================

# Make the script work when double-clicked from Finder
cd "$(dirname "$0")"

echo ""
echo "============================================"
echo " AxisSpline Installer for Fusion 360"
echo "============================================"
echo ""

# Define the target directory
ADDIN_DIR="$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns"

# Check if Fusion 360 AddIns directory exists
if [ ! -d "$ADDIN_DIR" ]; then
    echo "[ERROR] Fusion 360 AddIns directory not found!"
    echo ""
    echo "Expected location:"
    echo "$ADDIN_DIR"
    echo ""
    echo "Please ensure Fusion 360 is installed and has been run at least once."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Found Fusion 360 AddIns directory:"
echo "$ADDIN_DIR"
echo ""

# Check if AxisSpline folder exists in the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ ! -d "$SCRIPT_DIR/AxisSpline" ]; then
    echo "[ERROR] AxisSpline folder not found!"
    echo ""
    echo "Please ensure this installer is in the same directory as the AxisSpline folder."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if already installed
if [ -d "$ADDIN_DIR/AxisSpline" ]; then
    echo "[WARNING] AxisSpline is already installed."
    echo ""
    read -p "Do you want to overwrite the existing installation? (y/n): " OVERWRITE
    if [ "$OVERWRITE" != "y" ] && [ "$OVERWRITE" != "Y" ]; then
        echo ""
        echo "Installation cancelled."
        echo ""
        read -p "Press Enter to exit..."
        exit 0
    fi
    echo ""
    echo "Removing existing installation..."
    rm -rf "$ADDIN_DIR/AxisSpline"
    if [ -d "$ADDIN_DIR/AxisSpline" ]; then
        echo "[ERROR] Could not remove existing installation."
        echo "Please close Fusion 360 and try again."
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Copy the AxisSpline folder
echo "Installing AxisSpline..."
cp -R "$SCRIPT_DIR/AxisSpline" "$ADDIN_DIR/"

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Installation failed!"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Verify installation
if [ -f "$ADDIN_DIR/AxisSpline/AxisSpline.py" ]; then
    echo ""
    echo "============================================"
    echo " Installation Successful!"
    echo "============================================"
    echo ""
    echo "AxisSpline has been installed to:"
    echo "$ADDIN_DIR/AxisSpline"
    echo ""
    echo "To activate the add-in:"
    echo "1. Open Fusion 360"
    echo "2. Go to Utilities > Add-Ins > Scripts and Add-Ins"
    echo "3. Find 'AxisSpline' in the Add-Ins tab"
    echo "4. Click 'Run' to start the add-in"
    echo "5. Check 'Run on Startup' to auto-load"
    echo ""
    echo "The add-in will appear in the Solid tab under Scripts/Add-Ins."
    echo ""
else
    echo ""
    echo "[ERROR] Installation verification failed!"
    echo "Some files may not have been copied correctly."
    echo ""
fi

read -p "Press Enter to exit..."
exit 0
