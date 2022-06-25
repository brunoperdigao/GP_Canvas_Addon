from asyncio.base_futures import _FINISHED
import bpy

class GPC_OT_Canvas_Config(bpy.types.Operator):

    """ Initial Configuration of the Canvas """

    bl_idname = "gp_canvas.canvas_config"
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

    @classmethod
    def poll(self, context):
        # only run if in object mode
        if context.mode == 'OBJECT':
            return True
        else:
            return False

    def execute(self, context):
        bpy.ops.object.gpencil_add(type='EMPTY')
        # bpy.context.object.use_grease_pencil_lights = False
        bpy.context.object.data.stroke_depth_order = '3D'
        bpy.context.object.data.layers[0].info = "Stroke"
        bpy.context.object.data.layers[0].use_lights = False
        bpy.ops.gpencil.paintmode_toggle()

        return {'FINISHED'}

class GPC_OT_New_Fill_GP_Object(bpy.types.Operator):

    """ Adds new Grease Pencil Object with stroke configurations """

    bl_idname = "gp_canvas.new_fill_gp"
    bl_label = "GP Canvas New Grease Pencil for fill"
    bl_option = {'REGISTER'}

    @classmethod
    def poll(self, context):
        # only run if in object mode
        if context.mode == 'OBJECT':
            return True
        else:
            return False    

    def execute(self, context):
        bpy.ops.object.gpencil_add(type='EMPTY')
        # bpy.context.object.use_grease_pencil_lights = False
        bpy.context.object.data.stroke_depth_order = '3D'

        # Adds two layers e rename them
        bpy.ops.gpencil.layer_add()
        bpy.context.object.data.layers[0].info = "Main Material"
        bpy.context.object.data.layers[0].use_lights = False
        bpy.context.object.data.layers[1].info = "Shade"
        bpy.context.object.data.layers[1].use_lights = False
        bpy.context.object.data.layers["Shade"].use_mask_layer = True
        bpy.ops.gpencil.layer_mask_add(name="Main Material")
        bpy.context.object.data.layers.active_index=0

        # Changes the default material        
        bpy.ops.object.material_slot_remove()
        main_mat = new_mat = bpy.data.materials.new("Main Material")
        bpy.data.materials.create_gpencil_data(main_mat)
        bpy.context.object.data.materials.append(main_mat)
        bpy.context.object.active_material_index = 0
        bpy.context.object.active_material.grease_pencil.show_stroke = False
        bpy.context.object.active_material.grease_pencil.show_fill = True
        bpy.context.object.active_material.grease_pencil.fill_color = (0.9, 0.9, 0.9, 1)
        
        # Adds a new material with low opacity to work as shade
        shade_mat = new_mat = bpy.data.materials.new('Shade')
        bpy.data.materials.create_gpencil_data(shade_mat)
        bpy.context.object.data.materials.append(shade_mat)
        bpy.context.object.active_material_index = 1
        bpy.context.object.active_material.grease_pencil.show_stroke = False
        bpy.context.object.active_material.grease_pencil.show_fill = True
        bpy.context.object.active_material.grease_pencil.fill_color = (0, 0, 0, 0.35)

        bpy.context.object.active_material_index = 0

        # Adds offset modifier so that the shade won't be in the same plane as the main material
        bpy.ops.object.gpencil_modifier_add(type='GP_OFFSET')
        bpy.context.object.grease_pencil_modifiers["Offset"].location = (0.01, 0.01, 0.01)
        bpy.context.object.grease_pencil_modifiers["Offset"].layer = "Shade"

        bpy.ops.gpencil.paintmode_toggle()

        return {'FINISHED'}

class GPC_OT_Fill_Set_Main(bpy.types.Operator):
    """ Set Material and Layer to Main Material """

    bl_idname = "gp_canvas.fill_gp_set_main"
    bl_label = "Set Material and Layer to Main Material"
    bl_option = {'REGISTER'}

    @classmethod
    def poll(self, context):
        # only run if in object mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False    

    def execute(self, context):
        
        for i, layer in enumerate(bpy.context.object.data.layers):
            if "Main Material" in layer.info:
                bpy.context.object.data.layers.active_index=i

        for j, material in enumerate(bpy.context.object.data.materials):
            if "Main Material" in material.name:
                bpy.context.object.active_material_index = j

        return {'FINISHED'}

class GPC_OT_Fill_Set_Shade(bpy.types.Operator):
    """ Set Material and Layer to Shade """

    bl_idname = "gp_canvas.fill_gp_set_shade"
    bl_label = "Set Material and Layer to Shade"
    bl_option = {'REGISTER'}

    @classmethod
    def poll(self, context):
        # only run if in object mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False    

    def execute(self, context):
        
        for i, layer in enumerate(bpy.context.object.data.layers):
            if "Shade" in layer.info:
                bpy.context.object.data.layers.active_index=i

        for j, material in enumerate(bpy.context.object.data.materials):
            if "Shade" in material.name:
                bpy.context.object.active_material_index = j

        return {'FINISHED'}