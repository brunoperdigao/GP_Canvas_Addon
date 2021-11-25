import bpy
import mathutils
from bpy_extras import view3d_utils
from mathutils import Vector


def mouse_raycast_to_plane(mouse_pos, context, point, normal):

    region = context.region
    rv3d = context.region_data
    intersection = Vector((0, 0, 0))
    try:
        # Camera Origin
        origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, mouse_pos)
        # Mouse origin (gives the direction)
        mouse = view3d_utils.region_2d_to_vector_3d(region, rv3d, mouse_pos)
        # Camera Origin + Mouse
        ray_origin = origin + mouse
        # From the mouse to the viewport
        loc = view3d_utils.region_2d_to_location_3d(
            region, rv3d, mouse_pos, ray_origin - origin)
        # Ray to plane
        intersection = mathutils.geometry.intersect_line_plane(
            ray_origin, loc, point, normal)

    except:
        intersection = Vector((0, 0, 0))

    if intersection == None:
        intersection = Vector((0, 0, 0))

    return intersection
