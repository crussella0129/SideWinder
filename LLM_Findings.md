# LLM Findings Log

## 2026-01-12 - Bug Fix and Feature Removal

### Issue Encountered
Tool failed with error when using multi-curve selection:
```
TypeError: CurveEvaluator3D.getLengthAtParameter() missing 1 required positional argument: 'toParameter'
```

### Root Cause
The Fusion 360 API's `getLengthAtParameter()` method requires TWO arguments (`fromParameter`, `toParameter`), but the code was only passing one argument.

### Fix Applied
- Corrected `getLengthAtParameter()` calls in `sample_chained_xy_curves()` to pass both parameters

### Feature Removed: Refresh Command
The "Refresh SideWinder Sketch" command has been removed because:
1. Entity token storage via `findEntityByToken()` does not reliably work for sketch curves in Fusion 360
2. The parametric refresh feature was not functional as intended

### Current Working Features
- Branding: "SideWinder Parametric Spline Tool"
- Menu location: Solid > Create panel
- Multi-curve selection for XY path chaining
- Automatic curve ordering by endpoint proximity

---

## 2026-01-12 - Phase 2 Implementation

### Work Completed

#### 1. Branding Update
- Changed command name from "Axis Spline" to "SideWinder Parametric Spline Tool" in:
  - `AxisSpline.py` - CMD_NAME constant and error messages
  - `install.py` - All installer messages and help text
  - `install-windows.bat` - All batch file messages
- Note: Folder name "AxisSpline" retained per instructions (folder names unchanged)

#### 2. Menu Placement
- Moved tool from `SolidScriptsAddinsPanel` (Utilities > Add-Ins) to `SolidCreatePanel` (Solid > Create)
- Tool now accessible directly from the Create panel in the Solids workspace

#### 3. Selection Chaining
- Modified XY spline selection to accept multiple curves (unlimited)
- Implemented `sample_chained_xy_curves()` function that:
  - Distributes sample points proportionally across curves based on arc length
  - Orders curves by endpoint proximity to form a proper chain
  - Avoids duplicate points at curve joints
- Implemented `order_curves_by_proximity()` for automatic curve ordering

#### 4. Refresh Functionality (REMOVED - see entry above)
- Initially added "Refresh SideWinder Sketch" command
- Used entity tokens to store curve references
- **Later removed**: Entity token approach did not work reliably for sketch curves

### Impossibilities / Limitations Encountered

#### True Parametric Linking Not Possible
**Issue**: The LLM_Instructions requested full parametric linking where "changes to the drawings that originally composed it" would automatically update the generated spline.

**Finding**: True parametric linking (where Fusion 360 automatically updates the generated spline when source sketches change) is not achievable with the current Fusion 360 API for the following reasons:

1. **Sketch entities are not parametric features**: Fusion 360's parametric timeline system tracks features (extrusions, revolves, etc.) but sketch curves generated via the API are not registered as parametric features that respond to upstream changes.

2. **No native "Compute All" event hook**: The Fusion 360 API does not expose an event that fires when the user runs "Compute All" (Edit > Compute All or Ctrl+Q). There is no `ComputeAllEvent` or equivalent handler available.

3. **Custom features limitations**: While Fusion 360 has a Custom Feature API, it is designed for creating new feature types that appear in the timeline, not for making sketch geometry parametric to other sketch geometry.

**Workaround Implemented**: A "Refresh SideWinder Sketch" command was added that:
- Stores references to source curves using entity tokens
- Allows manual regeneration of the spline when the user chooses
- Preserves all settings (sample count, Z mode, construction flag)

**Alternative Considered but Not Implemented**: Creating a Fusion 360 Custom Feature would make the spline appear in the timeline, but this approach would:
- Significantly increase implementation complexity
- Require users to understand a new feature type
- Still not provide automatic updates without explicit recalculation

#### Tangent Selection Not Implemented
**Issue**: The instructions mentioned "perhaps even tangent selections if available along valid paths just like is allowed in sweep operations."

**Finding**: While sweep operations in Fusion 360 have built-in tangent chain selection, replicating this behavior in the API requires:
1. Implementing tangent continuity detection between adjacent curves
2. Creating a custom selection algorithm that follows tangent chains
3. This is possible but adds significant complexity

**Decision**: Not implemented in this phase. The current endpoint-proximity ordering provides functional chaining for most use cases. Tangent chain selection can be added as a future enhancement if needed.

### Files Modified
- `AxisSpline/AxisSpline.py` - Major updates for chaining and refresh
- `install.py` - Branding updates
- `install-windows.bat` - Branding updates

### New Features Added
- Multi-curve selection for XY path chaining
- Automatic curve ordering by endpoint proximity
