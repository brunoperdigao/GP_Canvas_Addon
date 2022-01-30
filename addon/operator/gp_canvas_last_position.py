import bpy
from ..utility.get_mouse3d_pos import get_mouse3d_pos

class GPC_OT_Last_Position(bpy.types.Operator):
    """ Get Canvas Last Position """

    bl_idname = "gp_canvas.last_position"
    bl_label = "GP Canvas Last Position"
    bl_option = {'REGISTER'}

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        last_position = get_mouse3d_pos(None)
        context.scene.cursor.location = last_position[0]
        return {'FINISHED'}