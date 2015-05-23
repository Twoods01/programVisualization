__author__ = 'twoods'
import pjViz.Utils.vectorMath as vm
import pyglet.gl
from numpy import matrix

class Spline():
    control_point_const = 0.21763
    line_segs = 15

    def __init__(self, start_node, stop_node, up=False, control=None):
        #Ensure that stop comes after start
        if stop_node.x < start_node.x:
            start_node, stop_node = stop_node, start_node

        self.start_point = (start_node.x, start_node.y)
        self.end_point = (stop_node.x, stop_node.y)
        if control:
            self.control_point = control
        else:
            self.control_point = self.compute_control(up)
        self.coefficients = self.solve_system()

    def compute_control(self, up):

        mid = vm.midpoint(self.start_point, self.end_point)
        if self.start_point[1] == self.end_point[1]:
            return mid

        perp = vm.perpendicular(self.start_point, self.end_point, Spline.control_point_const)
        if up:
            perp = (-perp[0], -perp[1])

        return vm.add_vectors(mid, perp)

    def draw(self, color=[255, 255, 255]):
        pyglet.gl.glBegin(pyglet.gl.GL_LINE_STRIP)
        pyglet.gl.glColor3f(pyglet.gl.GLfloat(color[0] / 255.0), pyglet.gl.GLfloat(color[1] / 255.0), pyglet.gl.GLfloat(color[2] / 255.0))
        step = (self.end_point[0] - self.start_point[0]) / Spline.line_segs
        for i in range(self.start_point[0], self.end_point[0], step):
            pyglet.gl.glVertex2f(i, self.y(i))

        pyglet.gl.glEnd()

    def y(self, x):
        return self.coefficients[0] + self.coefficients[1] * x + self.coefficients[2] * (x ** 2)

    def solve_system(self):

        row = []
        row.append((1, self.start_point[0], pow(self.start_point[0], 2)))
        row.append((1, self.control_point[0], pow(self.control_point[0], 2)))
        row.append((1, self.end_point[0], pow(self.end_point[0], 2)))
        mat = matrix([row[0], row[1], row[2]])

        y = matrix([[self.start_point[1]], [self.control_point[1]], [self.end_point[1]]])
        #Solve the system
        result = mat.I * y
        return result