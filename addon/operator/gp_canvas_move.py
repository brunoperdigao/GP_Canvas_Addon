import bpy
import traceback
from bpy.props import IntProperty, FloatProperty
from mathutils import Vector
from ..utility.ray import mouse_raycast_to_plane
from ..utility.draw import draw_quad, draw_text, get_blf_text_dims
from ..utility.get_mouse3d_pos import get_mouse3d_pos

class GPC_OT_Canvas_Move(bpy.types.Operator):
    """ Move the canvas in 3D space """

    bl_idname = "gp_canvas.canvas_move"
    bl_label = "GP Canvas Move"
    bl_option = {'REGISTER'}

    # x_axis: FloatProperty(nameX_AXIS', default=5, min=1, max=20)

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
                               '4', '5', '6', '7', '8', '9', '.'}  # Em teste
        self.number_input = []
        self.number_output = '###'
        self.x_init = context.scene.cursor.location.x
        self.y_init = context.scene.cursor.location.y
        self.z_init = context.scene.cursor.location.z
        self.mouse3d_pos = Vector((0, 0, 0))        
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
                    self.number_output = float(self.number_output)
                    print('depois do enter', self.number_input)
                if self.axis_type == 'X_AXIS':
                    if self.equal_mode:
                        self.mouse3d_pos = Vector(
                            (self.number_output, self.y_init, self.z_init))
                    else:
                        self.mouse3d_pos = Vector(
                            (self.x_init + self.number_output, self.y_init, self.z_init))
                if self.axis_type == 'Y_AXIS':
                    if self.equal_mode:
                        self.mouse3d_pos = Vector(
                            (self.x_init, self.number_output, self.z_init))
                    else:
                        self.mouse3d_pos = Vector(
                            (self.x_init, self.y_init + self.number_output, self.z_init))
                if self.axis_type == 'Z_AXIS':
                    if self.equal_mode:
                        self.mouse3d_pos = Vector(
                            (self.x_init, self.y_init, self.number_output))
                    else:
                        self.mouse3d_pos = Vector(
                            (self.x_init, self.y_init, self.z_init + self.number_output))
                context.scene.cursor.location = self.mouse3d_pos
            # call utility function that will work with the Operator for last position
            get_mouse3d_pos(self.mouse3d_pos)
            # removes shader after the operator is finished
            self.remove_shaders(context)            
            return {'FINISHED'}

        # CANCEL
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.scene.cursor.location = Vector(
                (self.x_init, self.y_init, self.z_init))
            # removes shader after the operator is cancelled
            self.remove_shaders(context)
            return {'CANCELLED'}

        # AXIS SELECTION
        # The shift event comes first so that shift+x can work. The othter way the X button alone would overwrite this.

        elif event.shift:
            if event.type == 'X':
                self.axis_type = 'NON_X'
            elif event.type == 'Y':
                self.axis_type = 'NON_Y'
            elif event.type == 'Z':
                self.axis_type = 'NON_Z'

        elif event.type == 'X':
            self.axis_type = 'X_AXIS'

        elif event.type == 'Y':
            self.axis_type = 'Y_AXIS'

        elif event.type == 'Z':
            self.axis_type = 'Z_AXIS'
            # DESNECESSÁRIO self.number_input = []  # Toda vez que ativar algum eixo o number_input vai ser zerado

        # NUMBER INPUT
        # For each keyboard input it turns the number input list into a joined output.
        # It has a tag_redraw so the number on the screen updates everytime a key is pressed and goes to the output

        elif event.ascii:  # Talvez ao invés de usar o ascii seja melhor usar um set de events type com números, ponto, sinal de negativo e backspace.
            if self.axis_type == 'X_AXIS' or self.axis_type == 'Y_AXIS' or self.axis_type == 'Z_AXIS':  # Checa se eles tá no modo eixo
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
            self.equal_mode = True

        # MOUSE MOVE
        elif event.type == 'MOUSEMOVE':

            if self.axis_type == 'PLANE' or self.axis_type == 'Z_AXIS':

                # Get the plane that is facing camera and project an intersection
                # Define a default value of 1 for the camera rotation in case it misses to get the quaternion
                # Then it cycles through the area to get the region 3d data and get the view_rotation quarternion
                camera_rotation = 1
                for area in context.screen.areas:
                    if area.type == 'VIEW_3D':
                        for region in area.regions:
                            if region.type == 'WINDOW':
                                camera_rotation = area.spaces[0].region_3d.view_rotation

                mouse = (event.mouse_region_x, event.mouse_region_y)
                point = Vector((0, 0, 0))
                normal = Vector((0, 1, 1, 1)) * Vector((camera_rotation))
                intersection = mouse_raycast_to_plane(
                    mouse, context, point, normal)

                # For the Plane Mode the mouse position will move through the intersection plane
                if self.axis_type == 'PLANE':
                    self.mouse3d_pos = intersection

                # For the Z Mode the mouse position will use only the Z position of the intersection plane
                elif self.axis_type == 'Z_AXIS':
                    self.mouse3d_pos = Vector(
                        (self.x_init, self.y_init, intersection[2]))

                context.scene.cursor.location = self.mouse3d_pos

            elif self.axis_type == 'X_AXIS' or self.axis_type == 'Y_AXIS' or self.axis_type == 'NON_Z':

                mouse = (event.mouse_region_x, event.mouse_region_y)

                # Get the XY plane located in the current cursor position
                point = Vector((self.x_init, self.y_init, self.z_init))
                normal = Vector((0, 0, 1))
                intersection = mouse_raycast_to_plane(
                    mouse, context, point, normal
                )

                # For the X Mode the mouse will use only the X position of the intersection plane
                if self.axis_type == 'X_AXIS':
                    self.mouse3d_pos = Vector(
                        (intersection[0], self.y_init, self.z_init)
                    )
                # For the Y Mode the mouse will use only the Y position of the intersection plane
                elif self.axis_type == 'Y_AXIS':
                    self.mouse3d_pos = Vector(
                        (self.x_init, intersection[1], self.z_init)
                    )
                # For the NON_Z Mode the mouse position will move through the XY plane
                elif self.axis_type == 'NON_Z':
                    self.mouse3d_pos = Vector(
                        (intersection[0], intersection[1], self.z_init)
                    )

                context.scene.cursor.location = self.mouse3d_pos

            elif self.axis_type == 'NON_X':
                mouse = (event.mouse_region_x, event.mouse_region_y)

                # Get the YZ plane located in the current cursor position
                point = Vector((self.x_init, self.y_init, self.z_init))
                # Changed the normal to get a different plane
                normal = Vector((1, 0, 0))
                intersection = mouse_raycast_to_plane(
                    mouse, context, point, normal)

                # For the NON_X mode the mouse position will move through the YZ plane
                self.mouse3d_pos = Vector(
                    (self.x_init, intersection[1], intersection[2]))

                context.scene.cursor.location = self.mouse3d_pos

            elif self.axis_type == 'NON_Y':
                mouse = (event.mouse_region_x, event.mouse_region_y)

                # Get the XZ plane located in the current cursor position
                point = Vector((self.x_init, self.y_init, self.z_init))
                # Changed the normal to get a different plane
                normal = Vector((0, 1, 0))
                intersection = mouse_raycast_to_plane(
                    mouse, context, point, normal)

                # For the NON_Y mode the mouse position will move through the XZ plane
                self.mouse3d_pos = Vector(
                    (intersection[0], self.y_init, intersection[2]))

                context.scene.cursor.location = self.mouse3d_pos

        return {'RUNNING_MODAL'}

    def remove_shaders(self, context):
        '''Remove shader handle.'''

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
        text = str(self.number_output)
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

    def send_mouse3d_pos(self):
        return self.x_init, self.y_init, self.z_init