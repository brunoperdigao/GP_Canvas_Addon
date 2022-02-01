import bpy
from mathutils import Vector


class GPC_OT_Get_View(bpy.types.Operator):
    """ Get selected saved view """

    bl_idname = "gp_canvas.get_view"
    bl_label = "GP Canvas Get View"
    bl_option = {'REGISTER'}

    

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
        newItem.value = bpy.context.scene.cursor.location
                

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