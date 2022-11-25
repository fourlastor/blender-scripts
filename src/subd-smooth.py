import bpy

bl_info = {
    "name": "Subd Smooth",
    "blender": (3, 0, 0),
    "category": "Mesh",
}


class ObjectSubdSmooth(bpy.types.Operator):
    """Subd smooth"""
    bl_idname = "object.subd_smooth"
    bl_label = "Subd Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    levels: bpy.props.IntProperty(name="Levels", default=2, min=1, max=6)

    def execute(self, context):
        scene = context.scene

        if not object or not context.object.type == 'MESH':
            return {}
        current_mode = bpy.context.object.mode  # Save the current mode
        if bpy.context.object.mode != "OBJECT":
            bpy.ops.object.mode_set(mode="OBJECT")  # Go to object mode

        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.context.object.modifiers[-1].levels = self.levels

        bpy.ops.object.modifier_apply(modifier=bpy.context.object.modifiers[-1].name)
        bpy.ops.object.mode_set(mode=current_mode)
        return {'FINISHED'}


def menu_func(self):
    self.layout.operator(ObjectSubdSmooth.bl_idname)


def register():
    bpy.utils.register_class(ObjectSubdSmooth)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(ObjectSubdSmooth)


if __name__ == "__main__":
    register()
