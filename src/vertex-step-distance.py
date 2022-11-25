import bpy

bl_info = {
    "name": "Vertex step distance",
    "blender": (2, 8, 0),
    "category": "Vertex",
}


class VertexStepDistance(bpy.types.Operator):
    """Vertex Step Distance"""
    bl_idname = "vertex.step_distance"
    bl_label = "Step distance"
    bl_options = {'REGISTER', 'UNDO'}

    axis: bpy.props.EnumProperty(items=(
        ("x", "X", ""),
        ("y", "Y", ""),
        ("z", "Z", ""),
    ), name="Axis", default="y")

    def execute(self, context):
        if not object or not context.object.type == 'MESH':
            return {}

        if self.axis == 'x':
            axis_coord = 0
        elif self.axis == 'y':
            axis_coord = 1
        else:
            axis_coord = 2

        def get_coordinate(v):
            return v.co[axis_coord]

        def set_coordinate(v, value):
            v.co[axis_coord] = value

        current_mode = bpy.context.object.mode  # Save the current mode
        if bpy.context.object.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")  # Go to object mode

        selected_vertices = [v for v in context.active_object.data.vertices if v.select]

        sorted_v = sorted(selected_vertices, key=get_coordinate)
        max_co = get_coordinate(sorted_v[-1])
        min_co = get_coordinate(sorted_v[0])
        v_count = len(sorted_v)
        step = (max_co - min_co) / v_count

        for i in range(0, v_count):
            v = sorted_v[i]
            set_coordinate(v, i * step + min_co)

        bpy.ops.object.mode_set(mode=current_mode)

        return {'FINISHED'}


def menu_func(self):
    self.layout.operator(VertexStepDistance.bl_idname)


def register():
    bpy.utils.register_class(VertexStepDistance)
    bpy.types.VIEW3D_MT_edit_mesh_vertices.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(VertexStepDistance)


if __name__ == "__main__":
    register()
