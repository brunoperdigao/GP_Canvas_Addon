import bpy

from .gp_canvas_move import GPC_OT_Canvas_Move
from .gp_canvas_rotate import GPC_OT_Canvas_Rotate
from .gp_canvas_init_config import GPC_OT_Canvas_Config
from .gp_canvas_reset_position import GPC_OT_Reset_Position
from .gp_canvas_reset_rotation import GPC_OT_Reset_Rotation
from .gp_canvas_last_position import GPC_OT_Last_Position
#from .gp_canvas_go_to_view import GPC_OT_Go_To_View
#from .gp_canvas_get_view import GPC_OT_Get_View
from .gp_canvas_saved_views import GPC_OT_Get_View, GPC_OT_Go_To_View, GPC_OT_Update_Value, GPC_OT_Update_Name

classes = (
    GPC_OT_Canvas_Move,
    GPC_OT_Canvas_Rotate,
    GPC_OT_Canvas_Config,
    GPC_OT_Reset_Position,
    GPC_OT_Reset_Rotation,
    GPC_OT_Last_Position,
    GPC_OT_Go_To_View,
    GPC_OT_Get_View,
    GPC_OT_Update_Value,
    GPC_OT_Update_Name
)


def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
