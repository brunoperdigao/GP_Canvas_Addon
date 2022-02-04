import bpy
from mathutils import Vector


class GPC_OT_Get_View(bpy.types.Operator):
    """ Get selected saved view """

    bl_idname = "gp_canvas.get_view"
    bl_label = "GP Canvas Get View"
    bl_option = {'REGISTER'}

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
        newItem.name = "view"
        newItem.position = bpy.context.scene.cursor.location
        newItem.rotation = bpy.context.scene.cursor.rotation_euler
        newItem.index = self.index
        self.index += 1
                

        return {'FINISHED'}

class GPC_OT_Delete_View(bpy.types.Operator):
    """ Deleted selected saved view """

    bl_idname = "gp_canvas.delete_view"
    bl_label = "GP Canvas Delete View"
    bl_option = {'REGISTER'}

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

class GPC_OT_Delete_All_Views(bpy.types.Operator):
    """ Deleted selected saved view """

    bl_idname = "gp_canvas.delete_all_views"
    bl_label = "GP Canvas Delete AllViews"
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

class GPC_OT_Go_To_Own_View(bpy.types.Operator):
    """ Go to selected saved view """

    bl_idname = "gp_canvas.go_to_own_view"
    bl_label = "GP Canvas Go To Own View"
    bl_option = {'REGISTER'}

    index: bpy.props.IntProperty(name="index", default=0)

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        saved_view = context.scene.gp_canvas_prop
        bpy.context.scene.cursor.location = saved_view[self.index].position
        bpy.context.scene.cursor.rotation_euler = saved_view[self.index].rotation

        return {'FINISHED'}

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
        bpy.context.scene.cursor.location = Vector((saved_view))


        return {'FINISHED'}

class GPC_OT_Update_Value(bpy.types.Operator):
    """ Updates saved view value """

    bl_idname = "gp_canvas.update_value"
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
        selected_view = context.scene.gp_canvas_enum
        list_of_views = context.scene.gp_canvas_prop
        # Convert String to Tuple
        # using map() + tuple() + int + split()
        for item in list_of_views:
            # item.value comes in a strange format so I changed to tuple
            # selected_view comes as a string, so I use eval to parse as a tuple of numbers
            if tuple(item.value) == eval(selected_view): 
                print("deu certo!")
                item.value = bpy.context.scene.cursor.location

        #print(saved_view)
        
        '''saved_view = eval(saved_view) # The eval method is here to assure that only the number are parsed
        print(saved_view)
        bpy.context.scene.cursor.location = Vector((saved_view))'''


        return {'FINISHED'}

class GPC_OT_Update_Name(bpy.types.Operator):
    """ Updated the saved view name """

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
        selected_view = context.scene.gp_canvas_enum
        list_of_views = context.scene.gp_canvas_prop
        # Convert String to Tuple
        # using map() + tuple() + int + split()
        for item in list_of_views:
            # item.value comes in a strange format so I changed to tuple
            # selected_view comes as a string, so I use eval to parse as a tuple of numbers
            if tuple(item.value) == eval(selected_view): 
                #item.name = "New Name"
                bpy.ops.wm.call_menu(name="GPC_MT_Name_Input")

        return {'FINISHED'}

class GPC_OT_Update_Own_Value(bpy.types.Operator):
    """ Updated the saved view name """

    bl_idname = "gp_canvas.update_own_value"
    bl_label = "GP Canvas Update Own Value"
    bl_option = {'REGISTER'}

    index: bpy.props.IntProperty(name="index", default=0)

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def execute(self, context):
        
        list_of_views = context.scene.gp_canvas_prop
        # Convert String to Tuple
        # using map() + tuple() + int + split()

        list_of_views[self.index].position = bpy.context.scene.cursor.location
        list_of_views[self.index].rotation = bpy.context.scene.cursor.rotation_euler

        return {'FINISHED'}