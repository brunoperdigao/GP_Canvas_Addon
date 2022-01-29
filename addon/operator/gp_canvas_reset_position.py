import bpy

class GPC_OT_Reset_Position(bpy.types.Operator):
    """ Reset the Position of the Canvas """

    bl_idname = "gp_canvas.reset_position"
    bl_label = "GP Canvas Reset Position"
    bl_option = {'REGISTER'}

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        bpy.context.scene.cursor.location = (0, 0, 0)


        return {'FINISHED'}