import bpy
import math

class GPC_PT_Main_Panel(bpy.types.Panel):
    bl_idname = "GPC_PT_Main_Panel"
    bl_label = "GP Canvas"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GP Canvas"


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

        # Main Config
        box1 = layout.box()
        box1_title = box1.row()
        box1_title.label(text="Convas Config")
        main_column = box1.column(align=True)    

        new_gpencil = "object.gpencil_add"
        main_column.operator(new_gpencil, text='Add Grease Pencil Object', icon='GP_SELECT_STROKES')
        main_column.operator('gp_canvas.init_config', text='Initial Configuration', icon='SOLO_OFF')
        
        # Canvas Properties
        # The if structure prevents the menu from trying to get the canvas property before entering the draw mode
        if context.mode == 'PAINT_GPENCIL':
            grid = context.object.data.grid
            canvas_column = box1.column(align=True)

            canvas_column.prop(grid, 'color')
            canvas_grid = canvas_column.grid_flow(columns=2)
            canvas_grid.prop(grid, 'scale')
            canvas_column.prop(grid, 'lines')
        else:
            pass
        ### grid = context.object.data.grid # Get the grid from the current object
        # It will only create these properties if a grease pencil object is selected
        '''canvas_column = box1.column(align=True)

        canvas_column.prop(grid, 'color')
        canvas_grid = canvas_column.grid_flow(columns=2)
        canvas_grid.prop(grid, 'scale')
        canvas_column.prop(grid, 'lines')'''

        canvas = context.space_data.overlay
        visibility_column = box1.column()
        visibility_column.prop(canvas, 'use_gpencil_grid', text='Canvas Visibility')
        visibility_column.prop(canvas, 'gpencil_grid_opacity')

       
        box2 = layout.box()
        box2_title = box2.row()
        box2_title.label(text="Canvas Movement")
        operators_column = box2.column(align=True)
        operators_grid = operators_column.grid_flow(columns=2, align=True)
        operators_grid.operator('gp_canvas.canvas_move', text='Move', icon='ORIENTATION_LOCAL')
        operators_grid.operator('gp_canvas.canvas_rotate', text='Rotate', icon='ORIENTATION_GIMBAL')
        operators_grid.operator('gp_canvas.reset_position', text='Reset', icon='VIEW_ORTHO')
        operators_grid.operator('gp_canvas.reset_rotation', text='Reset', icon='MOD_LATTICE')
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
        layout.operator('gp_canvas.delete_all_views', text='Delete All Views')

        # DELETE
        '''layout.prop(context.scene, "gp_canvas_enum", text="Choose a View")

        if not context.scene.gp_canvas_enum:
            layout.label(text='No saved view')
        else:    
            layout.operator('gp_canvas.go_to_view', text='Go To View')
            layout.operator('gp_canvas.update_value', text='Update Value')
            layout.operator('gp_canvas.update_name', text='Update Name')'''

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
            if item.deleted == True:
                pass
            else:
                row = layout.row(align=True)
                button_go_to = row.operator('gp_canvas.go_to_own_view', text="", icon="PLAY")
                button_go_to.index = item.index
                row.prop(item, "name", text="")
                #row.prop(item, "index", text="")
                button_update = row.operator('gp_canvas.update_own_value', text="", icon="FILE_REFRESH")
                button_update.index = item.index
                button_delete = row.operator('gp_canvas.delete_view', text="", icon="TRASH")
                button_delete.index = item.index
                
                box = layout.box()
                box_col = box.column(align=True)
                position = tuple(item.position)
                position_str = str((round(position[0],2), round(position[1],2), round(position[2],2)))
                rotation = tuple(item.rotation)
                rotation_degrees = [math.degrees(item)%360 for item in rotation]
                rotation_str = str((round(rotation_degrees[0],2), round(rotation_degrees[1],2), round(rotation_degrees[2],2)))
                # print(rotation_degrees)
                box_col.label(text="pos:" + position_str)
                box_col.label(text="rot:" + rotation_str)

class GPC_PT_Cursor_Properties(bpy.types.Panel):
    bl_idname = "GPC_PT_Cursor_Properties"
    bl_label = "Cursor Position"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GP Canvas"
    

    def draw(self, context):
        layout = self.layout

        cursor = context.scene.cursor

        layout.column().prop(cursor, "location", text="Location")
        rotation_mode = cursor.rotation_mode
        if rotation_mode == 'QUATERNION':
            layout.column().prop(cursor, "rotation_quaternion", text="Rotation")
        elif rotation_mode == 'AXIS_ANGLE':
            layout.column().prop(cursor, "rotation_axis_angle", text="Rotation")
        else:
            layout.column().prop(cursor, "rotation_euler", text="Rotation")
        layout.prop(cursor, "rotation_mode", text="")
        
    
        