import bpy

from .gp_canvas_move import GPC_OT_Canvas_Move
from .gp_canvas_rotate import GPC_OT_Canvas_Rotate

classes = (
    GPC_OT_Canvas_Move,
    GPC_OT_Canvas_Rotate
)


def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
