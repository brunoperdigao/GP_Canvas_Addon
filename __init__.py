bl_info = {
    "name": "GP Canvas Addon",
    "description": "Easy way to move and rotate the Grease Pencil canvas to improve sketching in 3D space workflow",
    "author": "Bruno Perdigão",
    "version": (0, 1),
    "blender": (2, 93, 20),
    "location": "View3D",
    "category": "3D View"}


def register():
    from .addon.register import register_addon
    register_addon()


def unregister():
    from.addon.register import unregister_addon
    unregister_addon()
