__author__ = 'twoods0129'
import pyglet.gl
import Visual.node


class Camera():
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.z = 0
        self.zoom = 1.0
        self.width = width
        self.height = height
        pyglet.gl.glViewport(0, 0, width, height)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glOrtho(0, width, 0, height, -1, 1)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

    def get_offset(self):
        return self.x, self.y

    def translate(self, x, y):
        dist_center_x = x - (self.width / 2)
        dist_center_y = y - (self.height / 2)
        trans_x = (x + self.x) + (dist_center_x * ((1 - self.zoom) / self.zoom))
        trans_y = (y + self.y) + (dist_center_y * ((1 - self.zoom) / self.zoom))

        return trans_x, trans_y

    def reset(self):
        self.x = 0
        self.y = 0
        self.zoom = 1.0

    def set_pos(self, x, y):
        self.x = x - (self.width / 2)
        self.y = y - (self.height / 2)
        self.zoom = 1.0

    def standard_projection(self):
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslatef(self.width / 2, self.height / 2, 0)
        pyglet.gl.glScalef(self.zoom, self.zoom, self.zoom)
        pyglet.gl.glTranslatef(-self.width / 2, -self.height / 2, 0)
        pyglet.gl.glTranslatef(-self.x, -self.y, -self.z)

    #Centers the camera on a given pixel location, returns the delta in x/y
    def center_on(self, x, y):
        delta_x = (x - (self.width / 2) - self.x) / 10
        self.x += delta_x

        delta_y = (y - (self.height / 2) - self.y) / 10
        self.y += delta_y

        return (delta_x, delta_y)

    def hud_projection(self):
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslatef(0, 0, 0)
