#!/usr/bin/env python3
"""
SideWinder Parametric Spline Tool - Cross-Platform Installer for Fusion 360

This installer works on Windows, macOS, and Linux.
It can be run from the command line or double-clicked in most environments.

Usage:
    python install.py           # Install the add-in
    python install.py --remove  # Uninstall the add-in
    python install.py --help    # Show help
"""

import os
import sys
import shutil
import platform
import argparse
from pathlib import Path


def get_fusion_addin_directory():
    """
    Get the Fusion 360 Add-Ins directory for the current platform.

    Returns:
        Path object to the AddIns directory, or None if not found.
    """
    system = platform.system()

    if system == "Windows":
        # Windows: %APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns
        appdata = os.environ.get("APPDATA")
        if appdata:
            addin_dir = Path(appdata) / "Autodesk" / "Autodesk Fusion 360" / "API" / "AddIns"
            return addin_dir

    elif system == "Darwin":  # macOS
        # macOS: ~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns
        home = Path.home()
        addin_dir = home / "Library" / "Application Support" / "Autodesk" / "Autodesk Fusion 360" / "API" / "AddIns"
        return addin_dir

    elif system == "Linux":
        # Linux (if Fusion runs via Wine or similar)
        # Try common Wine prefixes
        home = Path.home()
        wine_paths = [
            home / ".wine" / "drive_c" / "users" / os.environ.get("USER", "user") / "AppData" / "Roaming" / "Autodesk" / "Autodesk Fusion 360" / "API" / "AddIns",
            home / ".local" / "share" / "fusion360" / "AddIns",
        ]
        for path in wine_paths:
            if path.exists():
                return path
        # Return the most likely path even if it doesn't exist
        return wine_paths[0]

    return None


def get_script_directory():
    """Get the directory containing this script."""
    return Path(__file__).parent.resolve()


def print_header(title):
    """Print a formatted header."""
    print()
    print("=" * 50)
    print(f" {title}")
    print("=" * 50)
    print()


def print_success(message):
    """Print a success message."""
    print(f"[OK] {message}")


def print_error(message):
    """Print an error message."""
    print(f"[ERROR] {message}")


def print_warning(message):
    """Print a warning message."""
    print(f"[WARNING] {message}")


def print_info(message):
    """Print an info message."""
    print(f"[INFO] {message}")


def install_addin(force=False):
    """
    Install the AxisSpline add-in to Fusion 360.

    Args:
        force: If True, overwrite existing installation without prompting.

    Returns:
        True if installation succeeded, False otherwise.
    """
    print_header("SideWinder Parametric Spline Tool - Installer for Fusion 360")

    # Get directories
    script_dir = get_script_directory()
    source_dir = script_dir / "AxisSpline"
    addin_dir = get_fusion_addin_directory()

    # Check source exists
    if not source_dir.exists():
        print_error("SideWinder (AxisSpline) folder not found!")
        print()
        print("Please ensure this installer is in the same directory as the AxisSpline folder.")
        return False

    # Check Fusion 360 directory
    if addin_dir is None:
        print_error("Could not determine Fusion 360 AddIns directory for this platform.")
        print(f"Platform: {platform.system()}")
        return False

    if not addin_dir.exists():
        print_warning("Fusion 360 AddIns directory does not exist.")
        print()
        print(f"Expected location: {addin_dir}")
        print()
        print("This could mean:")
        print("  - Fusion 360 is not installed")
        print("  - Fusion 360 has never been run")
        print()

        try:
            response = input("Would you like to create the directory anyway? (y/n): ").strip().lower()
            if response == 'y':
                addin_dir.mkdir(parents=True, exist_ok=True)
                print_success("Created AddIns directory")
            else:
                print("Installation cancelled.")
                return False
        except (EOFError, KeyboardInterrupt):
            print("\nInstallation cancelled.")
            return False

    print_info(f"Source: {source_dir}")
    print_info(f"Target: {addin_dir}")
    print()

    target_dir = addin_dir / "AxisSpline"

    # Check for existing installation
    if target_dir.exists():
        print_warning("SideWinder is already installed.")
        print()

        if not force:
            try:
                response = input("Do you want to overwrite the existing installation? (y/n): ").strip().lower()
                if response != 'y':
                    print("Installation cancelled.")
                    return False
            except (EOFError, KeyboardInterrupt):
                print("\nInstallation cancelled.")
                return False

        print()
        print_info("Removing existing installation...")

        try:
            shutil.rmtree(target_dir)
        except Exception as e:
            print_error(f"Could not remove existing installation: {e}")
            print("Please close Fusion 360 and try again.")
            return False

    # Copy the add-in
    print_info("Installing SideWinder Parametric Spline Tool...")

    try:
        shutil.copytree(source_dir, target_dir)
    except Exception as e:
        print_error(f"Installation failed: {e}")
        return False

    # Verify installation
    if (target_dir / "AxisSpline.py").exists():
        print()
        print_header("Installation Successful!")
        print(f"SideWinder Parametric Spline Tool has been installed to:")
        print(f"  {target_dir}")
        print()
        print("To activate the add-in:")
        print("  1. Open Fusion 360")
        print("  2. Go to Utilities > Add-Ins > Scripts and Add-Ins")
        print("  3. Find 'AxisSpline' in the Add-Ins tab")
        print("  4. Click 'Run' to start the add-in")
        print("  5. Check 'Run on Startup' to auto-load")
        print()
        print("The tool will appear in the Solid tab under the Create panel.")
        return True
    else:
        print_error("Installation verification failed!")
        print("Some files may not have been copied correctly.")
        return False


def uninstall_addin():
    """
    Uninstall the AxisSpline add-in from Fusion 360.

    Returns:
        True if uninstallation succeeded, False otherwise.
    """
    print_header("SideWinder Parametric Spline Tool - Uninstaller for Fusion 360")

    addin_dir = get_fusion_addin_directory()

    if addin_dir is None:
        print_error("Could not determine Fusion 360 AddIns directory.")
        return False

    target_dir = addin_dir / "AxisSpline"

    if not target_dir.exists():
        print_warning("SideWinder is not installed.")
        return True

    print_info(f"Found installation at: {target_dir}")
    print()

    try:
        response = input("Are you sure you want to uninstall SideWinder? (y/n): ").strip().lower()
        if response != 'y':
            print("Uninstallation cancelled.")
            return False
    except (EOFError, KeyboardInterrupt):
        print("\nUninstallation cancelled.")
        return False

    print()
    print_info("Removing SideWinder...")

    try:
        shutil.rmtree(target_dir)
    except Exception as e:
        print_error(f"Could not remove installation: {e}")
        print("Please close Fusion 360 and try again.")
        return False

    if not target_dir.exists():
        print()
        print_header("Uninstallation Successful!")
        print("SideWinder has been removed from Fusion 360.")
        return True
    else:
        print_error("Uninstallation verification failed!")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SideWinder Parametric Spline Tool - Installer for Fusion 360",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python install.py           Install the add-in
    python install.py --remove  Uninstall the add-in
    python install.py --force   Install without prompts
        """
    )

    parser.add_argument(
        "--remove", "--uninstall",
        action="store_true",
        help="Uninstall the add-in instead of installing"
    )

    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force installation without confirmation prompts"
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Show installation directory info and exit"
    )

    args = parser.parse_args()

    if args.info:
        addin_dir = get_fusion_addin_directory()
        print(f"Platform: {platform.system()}")
        print(f"AddIns directory: {addin_dir}")
        print(f"Directory exists: {addin_dir.exists() if addin_dir else 'N/A'}")
        return 0

    try:
        if args.remove:
            success = uninstall_addin()
        else:
            success = install_addin(force=args.force)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 1

    print()

    # Pause on Windows if run by double-clicking
    if platform.system() == "Windows" and sys.stdin.isatty():
        try:
            input("Press Enter to exit...")
        except (EOFError, KeyboardInterrupt):
            pass

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
