from asyncio.base_futures import _FINISHED
import bpy

class GPC_OT_Canvas_Config(bpy.types.Operator):

    """ Initial Configuration of the Canvas """

    bl_idname = "gp_canvas.init_config"
    bl_label = "GP Canvas Initial Configuration"
    bl_option = {'REGISTER'}

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        bpy.context.space_data.overlay.use_gpencil_grid = True
        bpy.context.scene.tool_settings.gpencil_stroke_placement_view3d = 'CURSOR'
        bpy.context.scene.tool_settings.gpencil_sculpt.lock_axis = 'CURSOR'
        bpy.context.object.data.grid.scale = [5, 5]
        bpy.context.object.data.grid.offset = [0, 0]
        bpy.context.object.data.grid.lines = 5     
        bpy.context.object.data.grid.color = (0.5, 0.5, 0.5)
        bpy.context.space_data.overlay.gpencil_grid_opacity = 0.5



        return {'FINISHED'}

class GPC_OT_New_Stroke_GP_Object(bpy.types.Operator):
    """ Adds new Grease Pencil Object with stroke configurations """

    bl_idname = "gp_canvas.new_stroke_gp"
    bl_label = "GP Canvas New Grease Pencil for stroke"
    bl_option = {'REGISTER'}

    def execute(self, context):
        bpy.ops.object.gpencil_add(type='EMPTY')
        bpy.context.object.use_grease_pencil_lights = False
        bpy.context.object.data.stroke_depth_order = '3D'
        bpy.ops.gpencil.paintmode_toggle()

        return {'FINISHED'}

class GPC_OT_New_Fill_GP_Object(bpy.types.Operator):
    """ Adds new Grease Pencil Object with stroke configurations """

    bl_idname = "gp_canvas.new_fill_gp"
    bl_label = "GP Canvas New Grease Pencil for fill"
    bl_option = {'REGISTER'}

    def execute(self, context):
        bpy.ops.object.gpencil_add(type='EMPTY')
        bpy.context.object.use_grease_pencil_lights = False
        bpy.context.object.data.stroke_depth_order = '3D'

        # Adds two layers e rename them
        bpy.ops.gpencil.layer_add()
        bpy.context.object.data.layers[0].info = "Main"
        bpy.context.object.data.layers[1].info = "Shade"
        bpy.context.object.data.layers["Shade"].use_mask_layer = True
        bpy.ops.gpencil.layer_mask_add(name="Main")



        # Changes the default material
        
        bpy.ops.object.material_slot_remove()
        main_mat = new_mat = bpy.data.materials.new('Main')
        bpy.data.materials.create_gpencil_data(main_mat)
        bpy.context.object.data.materials.append(main_mat)
        bpy.context.object.active_material_index = 0
        bpy.context.object.active_material.grease_pencil.show_stroke = False
        bpy.context.object.active_material.grease_pencil.show_fill = True
        bpy.context.object.active_material.grease_pencil.fill_color = (0.5, 0.5, 0, 1)
        
        # Adds a new material with low opacity to work as shade
        shade_mat = new_mat = bpy.data.materials.new('Shade')
        bpy.data.materials.create_gpencil_data(shade_mat)
        bpy.context.object.data.materials.append(shade_mat)
        bpy.context.object.active_material_index = 1
        bpy.context.object.active_material.grease_pencil.show_stroke = False
        bpy.context.object.active_material.grease_pencil.show_fill = True
        bpy.context.object.active_material.grease_pencil.fill_color = (0, 0, 0, 0.35)

        # Adds offset modifier so that the shade won't be in the same plane as the main material
        bpy.ops.object.gpencil_modifier_add(type='GP_OFFSET')
        bpy.context.object.grease_pencil_modifiers["Offset"].location = (0.01, 0.01, 0.01)
        bpy.context.object.grease_pencil_modifiers["Offset"].layer = "Shade"



        

        bpy.ops.gpencil.paintmode_toggle()

        return {'FINISHED'}