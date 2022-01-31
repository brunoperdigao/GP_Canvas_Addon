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