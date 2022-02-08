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
    # creates and index so that it can be used by update_own_value and go_to_own_view
    index: bpy.props.IntProperty(name="Index", default=0)
    # this property is used to deleted a view from the panel. It actually just hides it so that the index count continues the same
    deleted: bpy.props.BoolProperty(name="Deleted", default=False)
    

