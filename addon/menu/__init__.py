import bpy

from .main_menu import GPC_MT_Main_Menu
from .main_panel import GPC_PT_Main_Panel

classes = (
    GPC_MT_Main_Menu,
    GPC_PT_Main_Panel
)


def register_menus():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister_menus():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
