import bpy

from .main_menu import GPC_MT_Main_Menu, GPC_MT_Name_Input
from .main_panel import GPC_PT_Main_Panel, GPC_PT_Views_Panel, GPC_PT_Saved_Views, GPC_PT_Cursor_Properties

classes = (
    GPC_MT_Main_Menu,
    GPC_MT_Name_Input,
    GPC_PT_Main_Panel,
    GPC_PT_Views_Panel,
    GPC_PT_Saved_Views,
    GPC_PT_Cursor_Properties
)


def register_menus():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_menus():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
