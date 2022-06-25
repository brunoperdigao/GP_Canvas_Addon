import bpy
import traceback
from bpy.props import IntProperty, FloatProperty
from mathutils import Vector
from math import radians, degrees
from ..utility.ray import mouse_raycast_to_plane
from ..utility.draw import draw_quad, draw_text, get_blf_text_dims


class GPC_OT_Canvas_Rotate(bpy.types.Operator):
    """ Rotate the canvas in 3D space """

    bl_idname = "gp_canvas.canvas_rotate"
    bl_label = "GP Canvas Rotate"
    bl_option = {'REGISTER'}

    @classmethod
    def poll(self, context):
        # only run if in grease pencil draw mode
        if context.mode == 'PAINT_GPENCIL':
            return True
        else:
            return False

    def invoke(self, context, event):

        # Properties
        self.number_options = {'0', '1', '2', '3',
                               '4', '5', '6', '7', '8', '9', '.'}
        self.number_input = []
        self.number_output = ''
        self.prefix = "angle: "
        self.x_init = context.scene.cursor.rotation_euler.x
        self.y_init = context.scene.cursor.rotation_euler.y
        self.z_init = context.scene.cursor.rotation_euler.z
        self.coord_init = (self.x_init, self.y_init, self.z_init)
        self.mouse3d_rotation = Vector((0, 0, 0))
        self.axis_type = 'PLANE'
        # Changes the way it handles de input numbers. See CONFIRM section
        self.equal_mode = False

        # Initialize
        # The Safe Draw function is to handle errors to allow the operator continues inpite of 2d shader issues
        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            self.safe_draw_shader_2d, (context,), 'WINDOW', 'POST_PIXEL')

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        
        def set_mouse_pos(equal_input, sum_input):
            if self.equal_mode:
                self.mouse3d_rotation = (Vector(self.coord_init) * Vector(sum_input)) + Vector(equal_input)
            else:
                coord = Vector(self.coord_init) + Vector(equal_input)
                self.mouse3d_rotation = Vector(coord)

        # PASS
        if event.type == 'MIDDLEMOUSE':
            return {'PASS_THROUGH'}

        # CONFIRM
        elif event.type in {'LEFTMOUSE', 'RET', 'NUMPAD_ENTER'}:
            # When Enter or Leftmouse it will check if there is any number typed
            # If yes, it will add the value according with the axis
            # It only stores values if it is in one of the axis mode
            if self.number_input != []:
                if len(self.number_input) >= 1:
                    self.number_output = radians(float(self.number_output))
                    print('depois do enter', self.number_input)
                if self.axis_type == 'X_AXIS':
                    set_mouse_pos(((self.number_output), 0, 0), (0, 1, 1))
                elif self.axis_type == 'Y_AXIS':
                    set_mouse_pos((0, (self.number_output), 0), (1, 0, 1))
                elif self.axis_type == 'Z_AXIS':
                    set_mouse_pos((0, 0, (self.number_output)), (1, 1, 0))
                context.scene.cursor.rotation_euler = self.mouse3d_rotation
            # removes shader after the operator is finished
            self.remove_shaders(context)
            return {'FINISHED'}

        # CANCEL
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.scene.cursor.rotation_euler = Vector(
                (self.x_init, self.y_init, self.z_init))
            # removes shader after the operator is cancelled
            self.remove_shaders(context)
            print("cancelado")
            return {'CANCELLED'}

        # AXIS SELECTION
        # The shift event comes first so that shift+x can work. The othter way the X button alone would overwrite this.
        elif event.type == 'X':
            self.axis_type = 'X_AXIS'

        elif event.type == 'Y':
            self.axis_type = 'Y_AXIS'

        elif event.type == 'Z':
            self.axis_type = 'Z_AXIS'

        # NUMBER INPUT
        # For each keyboard input it turns the number input list into a joined output.
        # It has a tag_redraw so the number on the screen updates everytime a key is pressed and goes to the output
        elif event.ascii:  # Talvez ao invés de usar o ascii seja melhor usar um set de events type com números, ponto, sinal de negativo e backspace.
            if self.axis_type in {'X_AXIS', 'Y_AXIS', 'Z_AXIS'}:  # Checa se eles tá no modo eixo
                if event.ascii in self.number_options:  # Checa se o input do teclado é numero ou vírgula
                    # Vai criando uma lista com cada input do teclado para formar um número. Como implementar o backspace?
                    self.number_input.append(event.ascii)
            self.number_output = ''.join(self.number_input)
            context.area.tag_redraw()
            print(self.number_input)

        elif event.type == 'BACK_SPACE' and event.value == 'PRESS':
            if self.number_input != []:
                # Creates the same list without the last item
                self.number_input = self.number_input[:-1]
            self.number_output = ''.join(self.number_input)
            context.area.tag_redraw()
            print(">>>", self.number_input)

        elif event.type in {'MINUS', 'NUMPAD_MINUS'}:
            # Checks the lenght in order to accept when you type the '-' first
            if len(self.number_input) > 1 and self.number_input[0] == '-':
                self.number_input = self.number_input[1:]
            else:
                self.number_input = ['-'] + self.number_input
            self.number_output = ''.join(self.number_input)
            context.area.tag_redraw()
            print("---", self.number_output)

        # This will allow to fill the value as a final output, and not an add value
        # Check the CONFIRM section
        elif event.type == 'EQUAL':
            self.prefix = "(absolute) angle: "
            context.area.tag_redraw()
            self.equal_mode = True
            

        # MOUSE MOVE
        elif event.type == 'MOUSEMOVE':
            camera_rotation = 1
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            camera_rotation = area.spaces[0].region_3d.view_rotation
                            center_x = region.width / 2  # Get the middle of the window

            mouse = (event.mouse_region_x, event.mouse_region_y)
            point = Vector((0, 0, 0))
            normal = Vector((0, 1, 1, 1)) * Vector((camera_rotation))
            intersection = mouse_raycast_to_plane(
                mouse, context, point, normal)

            if self.axis_type == 'PLANE':
                self.mouse3d_rotation = intersection

            else:
                # for every other axis type I chose to get the rotation value through the x mouse position on the window, not the 3D space
                # everything from the right side of the window will get me positive degree values. Left side will give me negative values.
                # at the end I have to convert the rotation value to radians
                rotation = mouse[0] - center_x
                if event.shift:  # slows down the moviment
                    rotation = rotation / 10
                if rotation >= 0:
                    while rotation > 360:
                        rotation = rotation - 360
                else:
                    while rotation < -360:
                        rotation = rotation + 360

                if self.axis_type == 'X_AXIS':
                    self.mouse3d_rotation = Vector(
                        (radians(rotation), self.y_init, self.z_init))

                if self.axis_type == 'Y_AXIS':
                    self.mouse3d_rotation = Vector(
                        (self.x_init, radians(rotation), self.z_init))

                if self.axis_type == 'Z_AXIS':
                    self.mouse3d_rotation = Vector(
                        (self.x_init, self.y_init, radians(rotation)))

            context.scene.cursor.rotation_euler = self.mouse3d_rotation

        return {'RUNNING_MODAL'}

    def remove_shaders(self, context):
        # Remove shader handle.
        if self.draw_handle != None:
            self.draw_handle = bpy.types.SpaceView3D.draw_handler_remove(
                self.draw_handle, "WINDOW")
            context.area.tag_redraw()

    def safe_draw_shader_2d(self, context):
        try:
            self.draw_shaders_2d(context)
        except:
            print('2D Shader Failed to Execute')
            traceback.print_exc()
            self.remove_shaders(context)

    def draw_shaders_2d(self, context):

        # Props
        text = self.prefix + str(self.number_output)
        font_size = 14
        dims = get_blf_text_dims(text, font_size)
        area_width = context.area.width
        padding = 8

        over_all_width = dims[0] + padding * 2
        over_all_height = dims[1] + padding * 2

        left_offset = abs((area_width - over_all_width) * .5)
        bottom_offset = 20

        top_left = (left_offset, bottom_offset + over_all_height)
        bot_left = (left_offset, bottom_offset)
        top_right = (left_offset + over_all_width,
                     bottom_offset + over_all_height)
        bot_right = (left_offset + over_all_width, bottom_offset)

        # Draw Quad
        verts = [top_left, bot_left, top_right, bot_right]
        draw_quad(vertices=verts, color=(0, 0, 0, .5))

        # Draw Text
        x = left_offset + padding
        y = bottom_offset + padding
        draw_text(text=text, x=x, y=y, size=font_size, color=(1, 1, 1, 1))
