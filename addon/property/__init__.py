import bpy

from .saved_views import GPC_SavedViews


classes = (
    GPC_SavedViews,
)


def register_properties():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.gp_canvas_prop = bpy.props.CollectionProperty(type=GPC_SavedViews)
    bpy.types.WindowManager.show_details = bpy.props.BoolProperty()


def unregister_properties():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.gp_canvas_prop