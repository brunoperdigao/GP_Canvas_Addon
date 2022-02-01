import bpy


class GPC_MT_Main_Menu(bpy.types.Menu):
    bl_idname = "GPC_MT_Main_Menu"
    bl_label = "GP Canvas Main Menu"

    def draw(self, context):

        @classmethod
        def poll(self, context):
            # only run if in grease pencil draw mode
            if context.mode == 'PAINT_GPENCIL':
                return True
            else:
                return False

        # just to avoid repeating self and writing just layout in the next lines
        layout = self.layout

        layout.operator_context = 'INVOKE_DEFAULT'
        layout.label(text='GP Canvas')

        layout.operator('gp_canvas.canvas_move', text='Canvas Move', icon='ORIENTATION_LOCAL')
        layout.operator('gp_canvas.canvas_rotate', text='Canvas Rotate', icon='ORIENTATION_LOCAL')
        layout.operator('gp_canvas.reset_position', text='Reset Position')
        layout.operator('gp_canvas.reset_rotation', text='Reset Rotation')
        layout.operator('gp_canvas.init_config', text='Initial Configuration')
        layout.operator('gp_canvas.last_position', text='Last Position')

class GPC_MT_Name_Input(bpy.types.Menu):
    bl_idname = "GPC_MT_Name_Input"
    bl_label = "GP Canvas Name Input"

    def draw(self, context):

        @classmethod
        def poll(self, context):
            # only run if in grease pencil draw mode
            if context.mode == 'PAINT_GPENCIL':
                return True
            else:
                return False

        # just to avoid repeating self and writing just layout in the next lines
        layout = self.layout

        layout.operator_context = 'INVOKE_DEFAULT'
        layout.label(text='Write the new name')
        
        selected_view = context.scene.gp_canvas_enum
        list_of_views = context.scene.gp_canvas_prop      


        for item in list_of_views:
            # item.value comes in a strange format so I changed to tuple
            # selected_view comes as a string, so I use eval to parse as a tuple of numbers
            if tuple(item.value) == eval(selected_view): 
                layout.prop(item, "name")