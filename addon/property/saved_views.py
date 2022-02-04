import bpy


class GPC_SavedViews(bpy.types.PropertyGroup):

    '''my_enum: bpy.props.EnumProperty(
        name="Saved Views:",
        description="",
        items=[create_enum_items()]
    )'''
    name: bpy.props.StringProperty(name="Name", default="Position")
    position: bpy.props.FloatVectorProperty(name="Position", default=(0, 0, 0))
    rotation: bpy.props.FloatVectorProperty(name="Rotation", default=(0, 0, 0))
    index: bpy.props.IntProperty(name="Index", default=0)
    deleted: bpy.props.BoolProperty(name="Deleted", default=False)
    

def create_enum_items(self, context):
    enum_list = []

    for item in context.scene.gp_canvas_prop:
        name = item.name
        value = item.position # !!!! ISSO TÁ QUEBRADO ver como eu faço pra passar position e rotation juntos
        data = (str(value), name, name)

        enum_list.append(data)

    return enum_list


'''def update_items(self, context, name, value):
    for item in context.scene.gp_canvas_prop:
        if name == item.name
            item.value = value

        enum_list.append(data)

    return enum_list'''
