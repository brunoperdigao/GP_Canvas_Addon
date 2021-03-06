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
        box1_title.label(text="Canvas Config")
        main_column = box1.column(align=True)    

        # Adds new grease pencil with some specific configuration
        
        main_column.operator('gp_canvas.new_stroke_gp', text='Add GP Object for Stroke', icon='GP_SELECT_STROKES')
        main_column.operator('gp_canvas.new_fill_gp', text='Add GP Object for Fill', icon='BRUSH_DATA')
        main_grid = main_column.grid_flow(columns=2, align=True)
        main_grid.operator('gp_canvas.fill_gp_set_main', text='Set to Main')
        main_grid.operator('gp_canvas.fill_gp_set_shade', text='Set to Shade')
        
        
        
        view = context.scene.view_settings
        main_column.label(text='Color Management:')
        main_column.prop(view, 'view_transform', text = "")

        background = bpy.context.space_data.shading
        main_column.label(text='Background Type:')
        main_column.prop(background, 'background_type', text='')
        main_column.prop(background, 'background_color')

        main_column.label(text='')
        main_column.operator('gp_canvas.canvas_config', text='Canvas Configuration', icon='SOLO_OFF')

        # Canvas Properties
        # The 'if' structure prevents the menu from trying to get the canvas property before entering the draw mode
        if context.mode == 'PAINT_GPENCIL':
            grid = context.object.data.grid
            canvas_column = box1.column(align=True)

            canvas_column.prop(grid, 'color')
            canvas_grid = canvas_column.grid_flow(columns=2)
            canvas_grid.prop(grid, 'scale')
            canvas_column.prop(grid, 'lines')
        else:
            pass
        
        canvas = context.space_data.overlay
        visibility_column = box1.column()
        visibility_column.prop(canvas, 'use_gpencil_grid', text='Canvas Visibility')
        visibility_column.prop(canvas, 'gpencil_grid_opacity')

       
       




        

class GPC_PT_Canvas_Panel(bpy.types.Panel):
    bl_idname = "GPC_PT_Canvas_Panel"
    bl_label = "GP Saved Canvas"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GP Canvas"
    

    def draw(self, context):
        
        # just to avoid repeating self and writing just layout in the next lines
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'

        box1 = layout.box()
        box1_title = box1.row()
        box1_title.label(text="Canvas Movement")
        operators_column = box1.column(align=True)
        operators_grid = operators_column.grid_flow(columns=2, align=True)
        operators_grid.operator('gp_canvas.canvas_move', text='Move', icon='ORIENTATION_LOCAL')
        operators_grid.operator('gp_canvas.canvas_rotate', text='Rotate', icon='ORIENTATION_GIMBAL')
        operators_grid.operator('gp_canvas.reset_position', text='Reset', icon='VIEW_ORTHO')
        operators_grid.operator('gp_canvas.reset_rotation', text='Reset', icon='MOD_LATTICE')
        operators_column.operator('gp_canvas.last_position', text='Last Position', icon='RECOVER_LAST')
        
        box2 = layout.box()
        box2.label(text='Canvas List')

        box2.operator('gp_canvas.get_canvas', text='Save New Canvas')
        box2.operator('gp_canvas.delete_all_canvas', text='Delete All Canvas')
        
        
        


class GPC_PT_Saved_Canvas(bpy.types.Panel):
    bl_idname = "GPC_PT_Saved_Canvas"
    bl_label = "View List"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GP Canvas"
    bl_parent_id = "GPC_PT_Canvas_Panel"
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    

    def draw(self, context):      
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        wm = context.window_manager
        layout.prop(wm, 'show_details', text='Show Details', toggle=-1) # 'show_details' property is defined in init.py in property folder

        
        # Saved Canvas
        saved_canvas = context.scene.gp_canvas_prop
        #layout.prop(saved_canvas, "my_enum", text="")
        for item in saved_canvas:
            # this works with the Delete Operators. It assures that the panel only shows canvass that are False in the property "delete"
            # it's a combination of property, operator and panel
            if item.deleted == True:
                pass
            else:
                box = layout.box()        
                row = box.row(align=True)
                button_go_to = row.operator('gp_canvas.go_to_own_canvas', text="", icon="PLAY")
                button_go_to.index = item.index
                row.prop(item, "name", text="")
                #row.prop(item, "index", text="")
                button_update = row.operator('gp_canvas.update_own_value', text="", icon="FILE_REFRESH")
                button_update.index = item.index
                button_delete = row.operator('gp_canvas.delete_canvas', text="", icon="TRASH")
                button_delete.index = item.index
                
                if wm.show_details == False:
                    pass
                else:
                    # box = layout.box()
                    box_col = box.column(align=True)
                    position = tuple(item.position)
                    position_str = str((round(position[0],2), round(position[1],2), round(position[2],2)))
                    rotation = tuple(item.rotation)
                    rotation_degrees = [math.degrees(item)%360 for item in rotation]
                    rotation_str = str((round(rotation_degrees[0],2), round(rotation_degrees[1],2), round(rotation_degrees[2],2)))
                    # print(rotation_degrees)
                    box_col.label(text="pos:" + position_str)
                    box_col.label(text="rot:" + rotation_str)
                    # box_col.label(text="---")

class GPC_PT_Cursor_Properties(bpy.types.Panel):
    bl_idname = "GPC_PT_Cursor_Properties"
    bl_label = "GP Cursor Position"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GP Canvas"
    
    # this is copied from the blender default view panel

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
        
    
        