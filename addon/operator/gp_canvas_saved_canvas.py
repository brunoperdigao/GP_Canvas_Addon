import bpy
from mathutils import Vector


class GPC_OT_Get_Canvas(bpy.types.Operator):
    """ Save current canvas """

    bl_idname = "gp_canvas.get_canvas"
    bl_label = "GP Canvas Get Canvas"
    bl_option = {'REGISTER'}

    # creates and index so that it can be used by update_own_value and go_to_own_canvas
    index: bpy.props.IntProperty(name="index", default=0)

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        newItem = context.scene.gp_canvas_prop.add()
        newItem.name = "Canvas." + str(self.index)
        newItem.position = bpy.context.scene.cursor.location
        newItem.rotation = bpy.context.scene.cursor.rotation_euler
        newItem.index = self.index
        self.index += 1
                

        return {'FINISHED'}

class GPC_OT_Delete_Canvas(bpy.types.Operator):
    """ Deleted selected saved canvas """

    bl_idname = "gp_canvas.delete_canvas"
    bl_label = "GP Canvas Delete Canvas"
    bl_option = {'REGISTER'}

    # index is called in the main panel, so that the operator acts in the related property.
    # the properties are a collection, so the index assures that the right one is being chosen.
    index: bpy.props.IntProperty(name="index", default=0)

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        
        item = context.scene.gp_canvas_prop[self.index]
        item.deleted = True
                        

        return {'FINISHED'}

class GPC_OT_Delete_All_Canvas(bpy.types.Operator):
    """ Deleted selected saved canvas """

    bl_idname = "gp_canvas.delete_all_canvas"
    bl_label = "GP Canvas Delete All Canvas"
    bl_option = {'REGISTER'}

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
       
        for item in context.scene.gp_canvas_prop:
            item.deleted = True
       
                

        return {'FINISHED'}

class GPC_OT_Go_To_Own_Canvas(bpy.types.Operator):
    """ Go to selected saved canvas """

    bl_idname = "gp_canvas.go_to_own_canvas"
    bl_label = "GP Canvas Go To Own Canvas"
    bl_option = {'REGISTER'}

    # index is called in the main panel, so that the operator acts in the related property.
    # the properties are a collection, so the index assures that the right one is being chosen.
    index: bpy.props.IntProperty(name="index", default=0)

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        saved_canvas = context.scene.gp_canvas_prop
        bpy.context.scene.cursor.location = saved_canvas[self.index].position
        bpy.context.scene.cursor.rotation_euler = saved_canvas[self.index].rotation

        return {'FINISHED'}

class GPC_OT_Update_Name(bpy.types.Operator):
    """ Updated the saved canvas name """

    bl_idname = "gp_canvas.update_name"
    bl_label = "GP Canvas Update Name"
    bl_option = {'REGISTER'}

    

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        selected_canvas = context.scene.gp_canvas_enum
        list_of_canvas = context.scene.gp_canvas_prop
        # Convert String to Tuple
        # using map() + tuple() + int + split()
        for item in list_of_canvas:
            # item.value comes in a strange format so I changed to tuple
            # selected_canvas comes as a string, so I use eval to parse as a tuple of numbers
            if tuple(item.value) == eval(selected_canvas): 
                #item.name = "New Name"
                bpy.ops.wm.call_menu(name="GPC_MT_Name_Input")

        return {'FINISHED'}

class GPC_OT_Update_Own_Value(bpy.types.Operator):
    """ Updated the saved canvas name """

    bl_idname = "gp_canvas.update_own_value"
    bl_label = "GP Canvas Update Own Value"
    bl_option = {'REGISTER'}

    # index is called in the main panel, so that the operator acts in the related property.
    # the properties are a collection, so the index assures that the right one is being chosen.
    index: bpy.props.IntProperty(name="index", default=0)

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        
        list_of_canvas = context.scene.gp_canvas_prop
        # Convert String to Tuple
        # using map() + tuple() + int + split()

        list_of_canvas[self.index].position = bpy.context.scene.cursor.location
        list_of_canvas[self.index].rotation = bpy.context.scene.cursor.rotation_euler

        return {'FINISHED'}