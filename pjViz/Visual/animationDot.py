__author__ = 'twoods0129'
import pyglet, node
import datetime

class AnimationDot:
    move_duration = 1.0
    scale_duration = 0.5
    min_width = 25
    wait_duration = 0.75
    max_width = node.node_width
    width_inc = (max_width - min_width) / scale_duration

    min_height = 25
    max_height = node.node_height
    height_inc = (max_height - min_height) / scale_duration

    step_over_color = (64, 74, 110)
    step_in_color = (136, 140, 62)

    def __init__(self, new_target_callback, update_active_node_callback):
        #X/y position
        self.x = 0
        self.y = 0

        #The amount to increment in x and y each step
        self.x_inc = 0
        self.y_inc = 0

        #If a target is currently set and if we've reached that target
        self.has_target = False
        self.reached_target = False
        #The target node we are going for
        self.target = None

        self.step_into = True
        #Methods to call when we need a new target, and when we need to update the currently active node
        self.new_target_callback = new_target_callback
        self.update_active_node_callback = update_active_node_callback
        #How far through the movement animation we are
        self.movement_duration = 0
        self.updated_active_node = False

        #Current size of the dot
        self.width = AnimationDot.max_width
        self.height = AnimationDot.max_height

        self.last_update = datetime.datetime.now()
        self.wait_duration = 0


    def place(self, x, y):
        self.x = x
        self.y = y

    def wait(self):
        self.wait_duration = AnimationDot.wait_duration

    def set_destination(self, node):
        self.target = node
        self.x_inc = (node.x - self.x) / AnimationDot.move_duration
        self.y_inc = (node.y - self.y) / AnimationDot.move_duration

        self.reached_target = False
        self.updated_active_node = False
        self.has_target = True
        self.movement_duration = 0

    def shrink(self, delta_t):
        self.width -= int(AnimationDot.width_inc * delta_t)
        self.height -= int(AnimationDot.height_inc * delta_t)

    def move_to_target(self, delta_t):
        self.x += self.x_inc * delta_t
        self.y += self.y_inc * delta_t

        if self.movement_duration >= AnimationDot.move_duration / 2 and not self.updated_active_node:
            self.updated_active_node = True
            self.update_active_node_callback(self.target)

        elif self.movement_duration > AnimationDot.move_duration:
            #Snap dot to correct position
            self.x = self.target.x
            self.y = self.target.y
            self.reached_target = True

        self.movement_duration += delta_t

    def grow(self, delta_t):
        self.width += int(AnimationDot.width_inc * delta_t)
        self.height += int(AnimationDot.height_inc * delta_t)

    def draw(self):
        cur_time = datetime.datetime.now()
        delta_t = (cur_time - self.last_update).total_seconds()

        if self.wait_duration >= 0:
            self.wait_duration -= delta_t
            if self.wait_duration <= 0:
                self.new_target_callback(False)


        if self.has_target:
            #Shrink until we reach minimum size
            if self.width > AnimationDot.min_width and not self.reached_target:
                self.shrink(delta_t)
            #Then move until we reach our target
            elif not self.reached_target:
                self.width = AnimationDot.min_width
                self.height = AnimationDot.min_height
                self.move_to_target(delta_t)
            #Then grow until we reach max size
            elif self.width < AnimationDot.max_width and self.target.visible:
                self.grow(delta_t)
            #Finished this animation, ask for next target
            else:
                if self.target.visible:
                    self.width = AnimationDot.max_width
                    self.height = AnimationDot.max_height
                self.has_target = False
                self.new_target_callback()



        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(self.x, self.y, 0)
        if self.step_into:
            color = AnimationDot.step_in_color
        else:
            color = AnimationDot.step_over_color

        node_vertices = pyglet.graphics.vertex_list_indexed(4,
                                    [0, 1, 2, 0, 2, 3],
                                    ('v3i', (-self.width / 2, -self.height / 2, 0,
                                            self.width / 2, -self.height / 2, 0,
                                            self.width / 2, self.height / 2, 0,
                                            -self.width / 2, self.height / 2, 0)),
                                    ('c3B', color * 4))

        node_vertices.draw(pyglet.gl.GL_TRIANGLES)

        pyglet.gl.glPopMatrix()

        self.last_update = datetime.datetime.now()

    def handle_input(self, x, y):

        if x > 1125 and x < 1145 and y > 670 and y < 682:
            AnimationDot.scale_duration += 0.1
            AnimationDot.width_inc = (AnimationDot.max_width - AnimationDot.min_width) / AnimationDot.scale_duration
            AnimationDot.height_inc = (AnimationDot.max_height - AnimationDot.min_height) / AnimationDot.scale_duration
        elif x > 1140 and x < 1160 and y > 670 and y < 682:
            if AnimationDot.scale_duration > 0.2:
                AnimationDot.scale_duration -= 0.1
                AnimationDot.width_inc = (AnimationDot.max_width - AnimationDot.min_width) / AnimationDot.scale_duration
                AnimationDot.height_inc = (AnimationDot.max_height - AnimationDot.min_height) / AnimationDot.scale_duration
        elif x > 1130 and x < 1142 and y > 641 and y < 653:
            AnimationDot.move_duration += 0.1
        elif x > 1145 and x < 1157 and y > 641 and y < 653:
            if AnimationDot.move_duration > 0.2:
                AnimationDot.move_duration -= 0.1

    def draw_ui(self):
        pyglet.text.Label("Scale: " + str(AnimationDot.scale_duration) + " s  +  -",
                          font_name='Times New Roman',
                          font_size=12,
                          x = 1100,
                          y = 680,
                          anchor_y = 'center',
                          anchor_x= 'center').draw()

        pyglet.text.Label("Move: " + str(AnimationDot.move_duration) + " s  +  -",
                          font_name='Times New Roman',
                          font_size=12,
                          x = 1100,
                          y = 650,
                          anchor_y = 'center',
                          anchor_x= 'center').draw()