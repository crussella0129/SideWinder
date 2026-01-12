"""
AxisSpline - Fusion 360 Add-In for Parametric XYZ Curves

Creates true 3D parametric curves where X(t), Y(t), and Z(t) are
independently defined but share a common parameter t.

This is a curve compiler, not a new kernel primitive.
"""

import adsk.core
import adsk.fusion
import traceback

# Global command handlers to keep them alive
handlers = []

# Command identifiers
CMD_ID = 'AxisSplineCommand'
CMD_NAME = 'Axis Spline'
CMD_DESC = 'Create a 3D parametric curve from separate XY and Z definitions'

# UI placement
PANEL_ID = 'SolidScriptsAddinsPanel'
WORKSPACE_ID = 'FusionSolidEnvironment'


def run(context):
    """Entry point when add-in is started."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Get the command definitions collection
        cmd_defs = ui.commandDefinitions

        # Check if command already exists and delete it
        existing_def = cmd_defs.itemById(CMD_ID)
        if existing_def:
            existing_def.deleteMe()

        # Create command definition
        cmd_def = cmd_defs.addButtonDefinition(
            CMD_ID,
            CMD_NAME,
            CMD_DESC,
            ''  # No custom icon folder
        )

        # Connect to command created event
        on_command_created = AxisSplineCommandCreatedHandler()
        cmd_def.commandCreated.add(on_command_created)
        handlers.append(on_command_created)

        # Add command to UI panel
        workspace = ui.workspaces.itemById(WORKSPACE_ID)
        if workspace:
            panel = workspace.toolbarPanels.itemById(PANEL_ID)
            if panel:
                # Check if control already exists
                existing_control = panel.controls.itemById(CMD_ID)
                if not existing_control:
                    panel.controls.addCommand(cmd_def)

        # Make command available in search
        cmd_def.execute()

    except:
        if ui:
            ui.messageBox(f'Failed to start AxisSpline:\n{traceback.format_exc()}')


def stop(context):
    """Entry point when add-in is stopped."""
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Remove command from panel
        workspace = ui.workspaces.itemById(WORKSPACE_ID)
        if workspace:
            panel = workspace.toolbarPanels.itemById(PANEL_ID)
            if panel:
                control = panel.controls.itemById(CMD_ID)
                if control:
                    control.deleteMe()

        # Delete command definition
        cmd_def = ui.commandDefinitions.itemById(CMD_ID)
        if cmd_def:
            cmd_def.deleteMe()

    except:
        if ui:
            ui.messageBox(f'Failed to stop AxisSpline:\n{traceback.format_exc()}')


class AxisSplineCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    """Handler for command creation - sets up the UI inputs."""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            cmd = args.command
            inputs = cmd.commandInputs

            # XY Spline Selector
            xy_selection = inputs.addSelectionInput(
                'xySplineSelection',
                'XY Spline',
                'Select a sketch spline for X(t) and Y(t)'
            )
            xy_selection.addSelectionFilter('SketchCurves')
            xy_selection.setSelectionLimits(1, 1)

            # Z Definition Mode dropdown
            z_mode_dropdown = inputs.addDropDownCommandInput(
                'zDefinitionMode',
                'Z Definition',
                adsk.core.DropDownStyles.TextListDropDownStyle
            )
            z_mode_dropdown.listItems.add('Z-Spline (sketch)', True)
            z_mode_dropdown.listItems.add('Z-Table (CSV/manual)', False)

            # Z-Spline Selector (visible when Z-Spline mode selected)
            z_spline_selection = inputs.addSelectionInput(
                'zSplineSelection',
                'Z Spline',
                'Select a sketch spline for Z(t) - uses Y value as Z'
            )
            z_spline_selection.addSelectionFilter('SketchCurves')
            z_spline_selection.setSelectionLimits(1, 1)

            # Z-Table input (visible when Z-Table mode selected)
            z_table_input = inputs.addTextBoxCommandInput(
                'zTableInput',
                'Z Values',
                'Enter comma-separated Z values (e.g., 0, 1, 2, 1.5, 0)',
                3,  # rows
                False  # read-only
            )
            z_table_input.isVisible = False

            # Sample Count
            sample_count = inputs.addIntegerSpinnerCommandInput(
                'sampleCount',
                'Sample Count',
                4,      # min
                500,    # max
                1,      # step
                50      # initial value
            )

            # Create as Construction option
            construction_option = inputs.addBoolValueInput(
                'createConstruction',
                'Create as Construction',
                True,   # checkbox type
                '',     # no icon
                False   # initial value
            )

            # Z Axis selection (which axis of Z-spline to use as Z value)
            z_axis_dropdown = inputs.addDropDownCommandInput(
                'zAxisSource',
                'Z Value Source',
                adsk.core.DropDownStyles.TextListDropDownStyle
            )
            z_axis_dropdown.listItems.add('Use Y axis of Z-spline', True)
            z_axis_dropdown.listItems.add('Use X axis of Z-spline', False)

            # Connect to input changed event for UI updates
            on_input_changed = AxisSplineInputChangedHandler()
            cmd.inputChanged.add(on_input_changed)
            handlers.append(on_input_changed)

            # Connect to validate inputs event
            on_validate = AxisSplineValidateHandler()
            cmd.validateInputs.add(on_validate)
            handlers.append(on_validate)

            # Connect to execute event
            on_execute = AxisSplineExecuteHandler()
            cmd.execute.add(on_execute)
            handlers.append(on_execute)

            # Connect to preview event
            on_preview = AxisSplinePreviewHandler()
            cmd.executePreview.add(on_preview)
            handlers.append(on_preview)

        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox(f'Command created failed:\n{traceback.format_exc()}')


class AxisSplineInputChangedHandler(adsk.core.InputChangedEventHandler):
    """Handler for input changes - toggles visibility of Z inputs."""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            changed_input = args.input
            inputs = args.inputs

            if changed_input.id == 'zDefinitionMode':
                z_mode = inputs.itemById('zDefinitionMode')
                z_spline = inputs.itemById('zSplineSelection')
                z_table = inputs.itemById('zTableInput')
                z_axis = inputs.itemById('zAxisSource')

                is_spline_mode = z_mode.selectedItem.name == 'Z-Spline (sketch)'

                z_spline.isVisible = is_spline_mode
                z_axis.isVisible = is_spline_mode
                z_table.isVisible = not is_spline_mode

        except:
            pass  # Silently handle UI update errors


class AxisSplineValidateHandler(adsk.core.ValidateInputsEventHandler):
    """Handler for input validation."""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            inputs = args.inputs

            # Check XY spline is selected
            xy_selection = inputs.itemById('xySplineSelection')
            if xy_selection.selectionCount < 1:
                args.areInputsValid = False
                return

            # Check Z input based on mode
            z_mode = inputs.itemById('zDefinitionMode')
            is_spline_mode = z_mode.selectedItem.name == 'Z-Spline (sketch)'

            if is_spline_mode:
                z_spline = inputs.itemById('zSplineSelection')
                if z_spline.selectionCount < 1:
                    args.areInputsValid = False
                    return
            else:
                z_table = inputs.itemById('zTableInput')
                if not z_table.text.strip():
                    args.areInputsValid = False
                    return
                # Validate CSV format
                try:
                    values = parse_z_table(z_table.text)
                    if len(values) < 2:
                        args.areInputsValid = False
                        return
                except:
                    args.areInputsValid = False
                    return

            # Check sample count
            sample_count = inputs.itemById('sampleCount')
            if sample_count.value < 4:
                args.areInputsValid = False
                return

            args.areInputsValid = True

        except:
            args.areInputsValid = False


class AxisSplinePreviewHandler(adsk.core.CommandEventHandler):
    """Handler for preview - shows the spline before final creation."""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        # Preview uses same logic as execute but with preview graphics
        # For MVP, we skip live preview
        pass


class AxisSplineExecuteHandler(adsk.core.CommandEventHandler):
    """Handler for command execution - creates the 3D spline."""

    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            design = adsk.fusion.Design.cast(app.activeProduct)

            if not design:
                ui.messageBox('No active Fusion design. Please open or create a design.')
                return

            inputs = args.command.commandInputs

            # Get input values
            xy_selection = inputs.itemById('xySplineSelection')
            z_mode = inputs.itemById('zDefinitionMode')
            sample_count = inputs.itemById('sampleCount').value
            is_construction = inputs.itemById('createConstruction').value

            # Get XY spline
            xy_entity = xy_selection.selection(0).entity
            xy_curve = get_nurbs_curve(xy_entity)

            if not xy_curve:
                ui.messageBox('Could not extract curve geometry from XY spline selection.')
                return

            # Get Z data based on mode
            is_spline_mode = z_mode.selectedItem.name == 'Z-Spline (sketch)'

            if is_spline_mode:
                z_spline = inputs.itemById('zSplineSelection')
                z_axis_source = inputs.itemById('zAxisSource')
                use_y_axis = z_axis_source.selectedItem.name == 'Use Y axis of Z-spline'

                z_entity = z_spline.selection(0).entity
                z_curve = get_nurbs_curve(z_entity)

                if not z_curve:
                    ui.messageBox('Could not extract curve geometry from Z spline selection.')
                    return

                # Sample Z values from spline
                z_values = sample_z_from_spline(z_curve, sample_count, use_y_axis)
            else:
                z_table = inputs.itemById('zTableInput')
                z_raw_values = parse_z_table(z_table.text)
                z_values = interpolate_z_table(z_raw_values, sample_count)

            # Sample XY spline
            xy_points = sample_xy_spline(xy_curve, sample_count)

            # Compose 3D points
            points_3d = compose_3d_points(xy_points, z_values)

            # Create 3D fit spline
            create_3d_spline(design, points_3d, is_construction)

        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox(f'Execution failed:\n{traceback.format_exc()}')


def get_nurbs_curve(entity):
    """Extract NURBS curve geometry from a sketch entity."""
    try:
        # Handle different sketch curve types
        if hasattr(entity, 'geometry'):
            geom = entity.geometry
            # Check if it's already a NurbsCurve3D
            if isinstance(geom, adsk.core.NurbsCurve3D):
                return geom
            # Try to get as curve
            if hasattr(geom, 'asNurbsCurve'):
                return geom.asNurbsCurve

        # For sketch splines specifically
        if hasattr(entity, 'spline'):
            return entity.spline.geometry

        # Try worldGeometry for sketch entities
        if hasattr(entity, 'worldGeometry'):
            geom = entity.worldGeometry
            if isinstance(geom, adsk.core.NurbsCurve3D):
                return geom
            if hasattr(geom, 'asNurbsCurve'):
                return geom.asNurbsCurve

        return None
    except:
        return None


def get_parameter_range(curve):
    """Get the parameter range of a curve."""
    evaluator = curve.evaluator
    (success, start_param, end_param) = evaluator.getParameterExtents()
    if success:
        return start_param, end_param
    return 0.0, 1.0


def normalize_parameter(t, t_min, t_max):
    """Normalize a parameter to the [0, 1] range."""
    if t_max == t_min:
        return 0.0
    return (t - t_min) / (t_max - t_min)


def denormalize_parameter(t_normalized, t_min, t_max):
    """Convert a normalized [0, 1] parameter back to curve parameter space."""
    return t_min + t_normalized * (t_max - t_min)


def sample_xy_spline(curve, sample_count):
    """
    Sample XY points from the spline.

    Returns list of (x, y) tuples.
    """
    evaluator = curve.evaluator
    t_min, t_max = get_parameter_range(curve)

    points = []
    for i in range(sample_count):
        # Normalized parameter t ∈ [0, 1]
        t_normalized = i / (sample_count - 1)

        # Convert to curve parameter space
        t_curve = denormalize_parameter(t_normalized, t_min, t_max)

        # Evaluate point at parameter
        (success, point) = evaluator.getPointAtParameter(t_curve)

        if success:
            points.append((point.x, point.y))
        else:
            # Fallback: linear interpolation if evaluation fails
            if points:
                points.append(points[-1])
            else:
                points.append((0.0, 0.0))

    return points


def sample_z_from_spline(curve, sample_count, use_y_axis=True):
    """
    Sample Z values from the Z-spline.

    The spline's Y (or X) value at each parameter is used as the Z value.

    Returns list of Z values.
    """
    evaluator = curve.evaluator
    t_min, t_max = get_parameter_range(curve)

    z_values = []
    for i in range(sample_count):
        # Normalized parameter t ∈ [0, 1]
        t_normalized = i / (sample_count - 1)

        # Convert to curve parameter space
        t_curve = denormalize_parameter(t_normalized, t_min, t_max)

        # Evaluate point at parameter
        (success, point) = evaluator.getPointAtParameter(t_curve)

        if success:
            z_val = point.y if use_y_axis else point.x
            z_values.append(z_val)
        else:
            # Fallback
            if z_values:
                z_values.append(z_values[-1])
            else:
                z_values.append(0.0)

    return z_values


def parse_z_table(text):
    """
    Parse comma-separated Z values from text input.

    Returns list of float values.
    """
    # Clean the input
    text = text.strip()

    # Split by comma, semicolon, or newline
    import re
    parts = re.split(r'[,;\n]+', text)

    values = []
    for part in parts:
        part = part.strip()
        if part:
            try:
                values.append(float(part))
            except ValueError:
                pass  # Skip non-numeric values

    return values


def interpolate_z_table(z_values, sample_count):
    """
    Interpolate Z table values to match sample count.

    Uses linear interpolation.
    """
    if len(z_values) == sample_count:
        return z_values

    if len(z_values) < 2:
        return [z_values[0] if z_values else 0.0] * sample_count

    result = []
    for i in range(sample_count):
        # Normalized position in output
        t = i / (sample_count - 1)

        # Position in input array
        pos = t * (len(z_values) - 1)

        # Get surrounding indices
        idx_low = int(pos)
        idx_high = min(idx_low + 1, len(z_values) - 1)

        # Interpolation factor
        frac = pos - idx_low

        # Linear interpolation
        z_interp = z_values[idx_low] * (1 - frac) + z_values[idx_high] * frac
        result.append(z_interp)

    return result


def compose_3d_points(xy_points, z_values):
    """
    Compose XY points and Z values into 3D points.

    Returns ObjectCollection of Point3D objects.
    """
    points = adsk.core.ObjectCollection.create()

    for i, ((x, y), z) in enumerate(zip(xy_points, z_values)):
        point = adsk.core.Point3D.create(x, y, z)
        points.add(point)

    return points


def create_3d_spline(design, points, is_construction=False):
    """
    Create a 3D fit spline from the composed points.

    Creates in a 3D sketch in the root component.
    """
    root_comp = design.rootComponent

    # Create a 3D sketch
    sketches = root_comp.sketches

    # For 3D sketch, we use the XY construction plane as reference
    # but the sketch will contain 3D geometry
    xy_plane = root_comp.xYConstructionPlane
    sketch = sketches.add(xy_plane)

    # Enable 3D sketch mode
    sketch.isComputeDeferred = True

    # Create the fit spline through the points
    splines = sketch.sketchCurves.sketchFittedSplines

    try:
        spline = splines.add(points)

        if spline and is_construction:
            spline.isConstruction = True

        sketch.isComputeDeferred = False

        return spline

    except Exception as e:
        sketch.isComputeDeferred = False
        raise e
