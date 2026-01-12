# SideWinder - AxisSpline Add-In for Fusion 360

Create true 3D parametric curves by composing independent X(t), Y(t), and Z(t) functions.

## Overview

AxisSpline lets you build complex 3D curves by defining each axis independently:

- **X(t), Y(t)**: From a 2D sketch spline
- **Z(t)**: From a secondary spline or manual values

No more dragging spline points in Z. Define your curves mathematically and let AxisSpline compose them into smooth 3D geometry.

## Features

- **Two Input Modes for Z**:
  - **Z-Spline**: Use another sketch spline's Y (or X) values as your Z profile
  - **Z-Table**: Enter comma-separated values for manual control

- **Adjustable Sample Count**: Control curve smoothness (4-500 points)

- **Construction Geometry Option**: Create as construction lines for reference

- **Parameter Synchronization**: Both inputs share a common parameter t for precise composition

## Installation

### Quick Install (Not Yet Fully Validated - Use Manual Install if unsuccessful)

**Windows:**
1. Download and extract the SideWinder package
2. Double-click `install-windows.bat`
3. Follow the on-screen instructions

**macOS:**
1. Download and extract the SideWinder package
2. Double-click `install-macos.command`
3. If prompted about security, right-click and select "Open"
4. Follow the on-screen instructions

### Cross-Platform Install (Python)

If you have Python 3 installed:

```bash
python install.py
```

Options:
- `python install.py --remove` - Uninstall the add-in
- `python install.py --force` - Install without prompts
- `python install.py --info` - Show installation directory

### Manual Installation (Verified on Windows 11)

Copy the `AxisSpline` folder to your Fusion 360 Add-Ins directory:

- **Windows**: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
- **macOS**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`

## Activation

1. Open **Fusion 360**
2. Go to **Utilities** > **Add-Ins** > **Scripts and Add-Ins**
3. In the **Add-Ins** tab, find **AxisSpline**
4. Click **Run** to start the add-in
5. Check **Run on Startup** to auto-load on future sessions

## Usage

### Basic Workflow

1. **Create your XY profile**: Draw a spline in a sketch (this defines X(t) and Y(t))

2. **Create your Z profile** (choose one):
   - **Z-Spline**: Draw another spline where the Y-values represent your Z heights
   - **Z-Table**: Prepare comma-separated Z values

3. **Run AxisSpline**: Find it in the Solid tab under Scripts/Add-Ins

4. **Configure**:
   - Select your XY spline
   - Choose Z definition mode
   - Select Z spline or enter Z values
   - Adjust sample count as needed

5. **Click OK** to create the 3D curve

### Example Use Cases

- **Helical Paths**: Circular XY spline + linear Z ramp - or - orthogonal cosin and sin waves in xy and z
- **Wave Surfaces**: Straight XY path + sinusoidal Z values
- **Complex Toolpaths**: Artistic XY profile + controlled Z engagement
- **Architectural Curves**: Organic XY shapes + structural Z profiles

## Uninstallation

**Windows**: Double-click `uninstall-windows.bat`

**macOS**: Double-click `uninstall-macos.command`

**Python**: `python install.py --remove`

**Manual**: Delete the `AxisSpline` folder from your Add-Ins directory

## Requirements

- Autodesk Fusion 360 (latest version recommended)
- Windows 10/11 or macOS 10.14+

## Support

For issues and feature requests, please visit the [GitHub repository](https://github.com/crussella0129/SideWinder/issues).

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

---

*Built with the Fusion 360 API*
