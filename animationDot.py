__author__ = 'twoods0129'
import pyglet, node

class AnimationDot:
    move_steps = 10
    scale_steps = 10
    min_width = 25
    max_width = node.node_width
    width_inc = (max_width - min_width) / scale_steps

    min_height = 25
    max_height = node.node_height
    height_inc = (max_height - min_height) / scale_steps

    color = (13, 136, 204)

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

        #Methods to call when we need a new target, and when we need to update the currently active node
        self.new_target_callback = new_target_callback
        self.update_active_node_callback = update_active_node_callback
        #How far through the movement animation we are
        self.movement_frames = 0

        #Current size of the dot
        self.width = AnimationDot.max_width
        self.height = AnimationDot.max_height

    def place(self, x, y):
        self.x = x
        self.y = y

    def set_destination(self, node):
        self.target = node
        self.x_inc = (node.x - self.x) / AnimationDot.move_steps
        self.y_inc = (node.y - self.y) / AnimationDot.move_steps

        self.reached_target = False
        self.has_target = True
        self.movement_frames = 0

    def shrink(self):
        self.width -= AnimationDot.width_inc
        self.height -= AnimationDot.height_inc

    def move_to_target(self):
        self.x += self.x_inc
        self.y += self.y_inc

        if self.movement_frames == AnimationDot.move_steps / 2:
            self.update_active_node_callback(self.target)

        elif self.movement_frames == AnimationDot.move_steps:
            #Snap dot to correct position
            self.x = self.target.x
            self.y = self.target.y
            self.reached_target = True

        self.movement_frames += 1

    def grow(self):
        self.width += AnimationDot.width_inc
        self.height += AnimationDot.height_inc

    def draw(self):
        if self.has_target:
            #Shrink until we reach minimum size
            if self.width > AnimationDot.min_width and not self.reached_target:
                self.shrink()
            #Then move until we reach our target
            elif not self.reached_target:
                self.move_to_target()
            #Then grow until we reach max size
            elif self.width < AnimationDot.max_width and self.target.visible:
                self.grow()
            #Finished this animation, ask for next target
            else:
                self.has_target = False
                self.new_target_callback()

        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(self.x, self.y, 0)

        node_vertices = pyglet.graphics.vertex_list_indexed(4,
                                    [0, 1, 2, 0, 2, 3],
                                    ('v3i', (-self.width / 2, -self.height / 2, 0,
                                            self.width / 2, -self.height / 2, 0,
                                            self.width / 2, self.height / 2, 0,
                                            -self.width / 2, self.height / 2, 0)),
                                    ('c3B', AnimationDot.color * 4))

        node_vertices.draw(pyglet.gl.GL_TRIANGLES)

        pyglet.gl.glPopMatrix()