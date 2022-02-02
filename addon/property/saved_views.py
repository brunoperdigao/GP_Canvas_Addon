import bpy


class GPC_SavedViews(bpy.types.PropertyGroup):

    '''my_enum: bpy.props.EnumProperty(
        name="Saved Views:",
        description="",
        items=[create_enum_items()]
    )'''
    name: bpy.props.StringProperty(name="Name", default="Position")
    value: bpy.props.FloatVectorProperty(name="Value", default=(0, 0, 0))
    index: bpy.props.IntProperty(name="Index", default=0)
    

def create_enum_items(self, context):
    enum_list = []

    for item in context.scene.gp_canvas_prop:
        name = item.name
        value = tuple(item.value)
        data = (str(value), name, name)

        enum_list.append(data)

    return enum_list


'''def update_items(self, context, name, value):
    for item in context.scene.gp_canvas_prop:
        if name == item.name
            item.value = value

        enum_list.append(data)

    return enum_list'''
