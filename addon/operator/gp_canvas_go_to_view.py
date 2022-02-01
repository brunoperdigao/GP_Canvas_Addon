import bpy
from mathutils import Vector


class GPC_OT_Go_To_View(bpy.types.Operator):
    """ Go to selected saved view """

    bl_idname = "gp_canvas.go_to_view"
    bl_label = "GP Canvas Go To View"
    bl_option = {'REGISTER'}

    

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        saved_view = context.scene.gp_canvas_enum
        # Convert String to Tuple
        # using map() + tuple() + int + split()
        saved_view = eval(saved_view) # The eval method is here to assure that only the number are parsed
        print(saved_view)
        bpy.context.scene.cursor.location = Vector((saved_view))


        return {'FINISHED'}