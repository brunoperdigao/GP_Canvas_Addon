import bpy

keys = []


def register_keymap():

    # stores blender api info into variable shorten up things
    wm = bpy.context.window_manager
    addon_keyconfig = wm.keyconfigs.addon
    kc = addon_keyconfig

    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new('gp_canvas.canvas_move', 'G', 'PRESS')
    #kmi.properties.name = 'GPC_OT_Cursor3d_Move'
    keys.append((km, kmi))

    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new('gp_canvas.canvas_rotate', 'R', 'PRESS')
    keys.append((km, kmi))


def unregister_keymap():

    for km, kmi in keys:
        km.keymap_items.remove(kmi)

    keys.clear()
