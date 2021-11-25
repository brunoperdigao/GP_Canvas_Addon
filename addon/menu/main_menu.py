import bpy


class GPC_MT_Main_Menu(bpy.types.Menu):
    bl_idname = "GPC_MT_Main_Menu"
    bl_label = "GP Canvas Main Menu"

    def draw(self, context):

        # just to avoid repeating self and writing just layout in the next lines
        layout = self.layout

        layout.operator_context = 'INVOKE_DEFAULT'
        layout.label(text='GP Canvas')

        layout.operator('gp_canvas.canvas_move',
                        text='Canvas Move', icon='ORIENTATION_LOCAL')
        layout.operator('gp_canvas.canvas_rotate',
                        text='Canvas Rotate', icon='ORIENTATION_LOCAL')
