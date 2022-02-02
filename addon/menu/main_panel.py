import bpy


class GPC_PT_Main_Panel(bpy.types.Panel):
    bl_idname = "GPC_PT_Main_Panel"
    bl_label = "GP Canvas"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GP Canvas"


    def draw(self, context):

        '''@classmethod
        def poll(self, context):
            # only run if in grease pencil draw mode
            if context.mode == 'PAINT_GPENCIL':
                return True
            else:
                return False'''

        # just to avoid repeating self and writing just layout in the next lines
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'

        # Main Config
        box1 = layout.box()
        box1_title = box1.row()
        box1_title.label(text="Convas Config")
        main_column = box1.column(align=True)    

        new_gpencil = "object.gpencil_add"
        main_column.operator(new_gpencil, text='Add Grease Pencil Object', icon='GP_SELECT_STROKES')
        main_column.operator('gp_canvas.init_config', text='Initial Configuration', icon='SOLO_OFF')
        
        # Canvas Properties
        obj = context.active_object.name # Get the active object name as a string to use to get the property
        grid = bpy.data.grease_pencils[obj].grid # Get the grid from the current active object
        # It will only create these properties if a grease pencil object is selected
        canvas_column = box1.column(align=True)

        canvas_column.prop(grid, 'color')
        canvas_column.prop(grid, 'scale')
        canvas_column.prop(grid, 'lines')

        canvas = context.space_data.overlay
        visibility_column = box1.column()
        visibility_column.prop(canvas, 'use_gpencil_grid', text='Canvas Visibility')
        visibility_column.prop(canvas, 'gpencil_grid_opacity')

       
        box2 = layout.box()
        box2_title = box2.row()
        box2_title.label(text="Canvas Movement")
        operators_column = box2.column(align=True)
        operators_column.operator('gp_canvas.canvas_move', text='Canvas Move', icon='ORIENTATION_LOCAL')
        operators_column.operator('gp_canvas.canvas_rotate', text='Canvas Rotate', icon='ORIENTATION_GIMBAL')
        operators_column.operator('gp_canvas.reset_position', text='Reset Position', icon='VIEW_ORTHO')
        operators_column.operator('gp_canvas.reset_rotation', text='Reset Rotation', icon='MOD_LATTICE')
        operators_column.operator('gp_canvas.last_position', text='Last Position', icon='RECOVER_LAST')




        

class GPC_PT_Views_Panel(bpy.types.Panel):
    bl_idname = "GPC_PT_Views_Panel"
    bl_label = "GP Saved Canvas"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GP Canvas"
    

    def draw(self, context):

        # just to avoid repeating self and writing just layout in the next lines
        layout = self.layout

        layout.operator_context = 'INVOKE_DEFAULT'
        layout.label(text='Choose a saved view')

        layout.operator('gp_canvas.get_view', text='Save New View')

        layout.prop(context.scene, "gp_canvas_enum", text="Choose a View")

        layout.operator('gp_canvas.go_to_view', text='Go To View')
        layout.operator('gp_canvas.update_value', text='Update Value')
        layout.operator('gp_canvas.update_name', text='Update Name')

class GPC_PT_Saved_Views(bpy.types.Panel):
    bl_idname = "GPC_PT_Saved_Views"
    bl_label = "List of Views"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GP Canvas"
    bl_parent_id = "GPC_PT_Views_Panel"
    

    def draw(self, context):      
        
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'

        # Saved Views
        saved_view = context.scene.gp_canvas_prop
        #layout.prop(saved_view, "my_enum", text="")
        for item in saved_view:
            layout.prop(item, "name", text="")
            layout.prop(item, "index", text="")
            button = layout.operator('gp_canvas.update_own_value', text="Update Value")
            button.index = item.index

            
        
        # TESTE!!!!
        # Saved Views
        
    
        