import bpy

class GPC_OT_Reset_Rotation(bpy.types.Operator):
    """ Reset the Rotation of the Canvas """

    bl_idname = "gp_canvas.reset_rotation"
    bl_label = "GP Canvas Reset Rotation"
    bl_option = {'REGISTER'}

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        bpy.context.scene.cursor.rotation_euler = (0, 0, 0)


        return {'FINISHED'}