import bpy
from mathutils import Vector


class GPC_OT_Get_View(bpy.types.Operator):
    """ Get selected saved view """

    bl_idname = "gp_canvas.get_view"
    bl_label = "GP Canvas Get View"
    bl_option = {'REGISTER'}

    

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        newItem = context.scene.gp_canvas_prop.add()
        newItem.name = "view"
        newItem.value = bpy.context.scene.cursor.location
                

        return {'FINISHED'}