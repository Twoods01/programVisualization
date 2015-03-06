__author__ = 'twoods0129'
import pyglet.gl

class Camera():
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.z = 0
        pyglet.gl.glViewport(0, 0, width, height)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
        pyglet.gl.glLoadIdentity()
        #pyglet.gl.glOrtho(0, width, 0, height, -1, 1)
        pyglet.gl.gluPerspective(60, float(width)/height, 0.1, 100)
        pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)

    def get_offset(self):
        return self.x, self.y

    def reset(self):
        self.x = 0
        self.y = 0

    def standard_projection(self):
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslatef(-self.x, -self.y, -self.z)

    def hud_projection(self):
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslatef(0, 0, 0)
