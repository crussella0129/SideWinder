#!/bin/bash

# ============================================================================
# AxisSpline Uninstaller for macOS
# Removes the Fusion 360 Add-In
# ============================================================================

# Make the script work when double-clicked from Finder
cd "$(dirname "$0")"

echo ""
echo "============================================"
echo " AxisSpline Uninstaller for Fusion 360"
echo "============================================"
echo ""

# Define the target directory
ADDIN_DIR="$HOME/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns"
TARGET_DIR="$ADDIN_DIR/AxisSpline"

# Check if installed
if [ ! -d "$TARGET_DIR" ]; then
    echo "[INFO] AxisSpline is not installed."
    echo ""
    echo "Nothing to remove."
    echo ""
    read -p "Press Enter to exit..."
    exit 0
fi

echo "Found AxisSpline installation at:"
echo "$TARGET_DIR"
echo ""

read -p "Are you sure you want to uninstall AxisSpline? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo ""
    echo "Uninstallation cancelled."
    echo ""
    read -p "Press Enter to exit..."
    exit 0
fi

echo ""
echo "Removing AxisSpline..."

# Remove the directory
rm -rf "$TARGET_DIR"

if [ -d "$TARGET_DIR" ]; then
    echo ""
    echo "[ERROR] Could not remove AxisSpline."
    echo "Please close Fusion 360 and try again."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo ""
echo "============================================"
echo " Uninstallation Successful!"
echo "============================================"
echo ""
echo "AxisSpline has been removed from Fusion 360."
echo ""
echo "If the add-in was running, restart Fusion 360"
echo "to complete the removal."
echo ""

read -p "Press Enter to exit..."
exit 0
