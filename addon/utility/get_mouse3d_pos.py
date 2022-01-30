import bpy
 

last_position = []

# stores the actual and the last position
def get_mouse3d_pos(position):      
    if position == None: # this options is to work with the last position operator that will pass no argument
        pass
    else:
        last_position.append(position)
        if len(last_position) > 2:
            del last_position[0]
    return last_position



