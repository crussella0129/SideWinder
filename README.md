# SideWinder - Parametric Spline Generator Add-In for Fusion 360

Create true 3D parametric curves by composing independent X(t), Y(t), and Z(t) functions.

## Overview

AxisSpline lets you build complex 3D curves by defining each axis independently:

- **X(t), Y(t)**: From a 2D sketch spline
- **Z(t)**: From a secondary spline or manual values

No more dragging spline points in Z. Define your curves mathematically and let AxisSpline compose them into smooth 3D geometry.

## Features

- **Two Input Modes for Z**:
  - **Z-Spline**: Use a sketch curve as a 3D path - the XY shape follows this path as a rail
  - **Z-Table**: Enter comma-separated values for manual control

- **3D Sweep Behavior**: The Z-path defines both height (Z) and lateral offset (X), creating true parametric 3D curves

- **Adjustable Sample Count**: Control curve smoothness (4-500 points)

- **Axis Inversion**: Flip X, Y, or Z independently with checkboxes

- **Construction Geometry Option**: Create as construction lines for reference

- **Parameter Synchronization**: Both inputs share a common parameter t for precise composition

## Installation

### Quick Install (Not Yet Fully Validated on MacOS - Use Manual Install if unsuccessful)

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
   - **Z-Spline**: Draw a curve that defines the 3D path your XY shape will follow
   - **Z-Table**: Prepare comma-separated Z values

   > **IMPORTANT**: When using Z-Spline mode, create your Z-path sketch on the **Front plane (XZ plane)**. In this sketch:
   > - Horizontal movement (X-axis) = lateral offset of the XY shape
   > - Vertical movement (Z-axis) = height of the resulting curve
   >
   > The tool uses world coordinates, so only the Front plane orientation produces correct results.

3. **Run the tool**: Find "Parametric Spline Tool" in the Solid > Create panel

4. **Configure**:
   - Select your XY curve(s) - multiple curves will be chained
   - Choose Z definition mode
   - Select Z curve(s) or enter Z values
   - Adjust sample count as needed
   - Use Invert checkboxes to flip axes if needed

5. **Click OK** to create the 3D curve

### Example Use Cases

- **Helical Paths**: Circle (XY) + diagonal line going up (Z on Front plane) = helix
- **Helix with Lateral Shift**: Circle (XY) + path that goes up then right (Z) = helix that rises then moves sideways
- **Wave Along a Path**: Straight line (XY) + sinusoidal curve (Z) = wavy 3D curve
- **Complex Toolpaths**: Artistic XY profile + controlled Z engagement path
- **Architectural Curves**: Organic XY shapes + structural Z profiles

### Tips

- **Curve Chaining**: Select multiple curves for XY or Z paths - they're automatically ordered by endpoint proximity
- **Sample Count**: Start with 50. Increase for smoother curves, decrease for faster generation
- **Invert Checkboxes**: Use these to mirror your curve without redrawing
- **Z-Path Orientation**: Always use Front plane for Z-path sketches to ensure correct world coordinate mapping

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
