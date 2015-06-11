__author__ = 'twoods'
import pjViz.Utils.vectorMath as vm
import pyglet.gl
import pjViz.Visual.node
import pjViz.constants as const
from numpy import matrix, linalg

class Spline():
    control_point_const = 0.241
    b_control_point_const = 0.716
    line_segs = 10

    def __init__(self, start_node, stop_node, up=False, control=None):
        #Ensure that stop comes after start
        if stop_node.x < start_node.x:
            start_node, stop_node = stop_node, start_node

        self.start_point = (start_node.x, start_node.y)
        self.end_point = (stop_node.x, stop_node.y)

        if const.Constants.linear_layout:
            up = True

        if control and not const.Constants.linear_layout:
            self.control_point = control
            dist = vm.dist(const.Constants.circle_center, self.control_point)
        else:
            self.control_point = self.compute_control(up)
            dist = vm.dist(const.Constants.circle_center, self.control_point)

        self.coefficients = self.solve_system()

    def compute_control(self, up):
        mid = vm.midpoint(self.start_point, self.end_point)
        if self.start_point[1] == self.end_point[1] and not const.Constants.linear_layout:
            return mid

        #print("Midpoint is " + str(mid))
        if const.Constants.circular_layout:
            perp = vm.scale(vm.get_direction(const.Constants.circle_center, mid), Spline.b_control_point_const)
            #print("Perp is " + str(perp))
        else:
            perp = vm.perpendicular(self.start_point, self.end_point, Spline.control_point_const)
            if up:
                perp = (-perp[0], -perp[1])


        return vm.add_vectors(mid, perp)

    def draw(self, color=[255, 255, 255, 128]):
        pyglet.gl.glBegin(pyglet.gl.GL_LINE_STRIP)
        color = [color[0], color[1], color[2], 128]
        pyglet.gl.glColor4f(pyglet.gl.GLfloat(color[0] / 255.0), pyglet.gl.GLfloat(color[1] / 255.0), pyglet.gl.GLfloat(color[2] / 255.0), pyglet.gl.GLfloat(color[3] / 255.0))
        dist = vm.dist(self.end_point, self.start_point)
        segments = Spline.line_segs * (dist / float(pjViz.Visual.node.node_width))
        step = dist / segments
        i = self.start_point[0]
        while i <= self.end_point[0]:
            pyglet.gl.glVertex2f(i, self.y(i))
            i += step
        pyglet.gl.glVertex2f(self.end_point[0], self.end_point[1])
        pyglet.gl.glEnd()

    def y(self, x):
        #For circle layouts we switch to bezier curves
        if const.Constants.circular_layout:
            #Convert to a value between 0 and 1
            t = (x - self.start_point[0]) / (self.end_point[0] - self.start_point[0])
            b = vm.add_vectors(vm.add_vectors(vm.mult(self.start_point, (1 - t) ** 2), vm.mult(self.control_point, 2 * t * (1 - t))), vm.mult(self.end_point, t ** 2))
            return b[1]

        return self.coefficients[0] + (self.coefficients[1] * x) + (self.coefficients[2] * (x ** 2))

    def solve_system(self):
        row = []
        row.append((1, self.start_point[0], pow(self.start_point[0], 2)))
        row.append((1, self.control_point[0], pow(self.control_point[0], 2)))
        row.append((1, self.end_point[0], pow(self.end_point[0], 2)))
        mat = matrix([row[0], row[1], row[2]])

        y = matrix([[self.start_point[1]], [self.control_point[1]], [self.end_point[1]]])

        #Solve the system
        try:
            result = mat.I * y
        except linalg.LinAlgError:
            print("Uho")
            result = [0, 0, 0, 1]
        return result

    def uglySolver(self):
        coef = [0,0,0]
        y = [self.start_point[1], self.control_point[1], self.end_point[1]]
        coef[2] = ((y[1] - y[0]) * (self.start_point[0] - self.end_point[0]) +
                   (y[2] - y[0]) * (self.control_point[0] - self.start_point[0])) / \
                  ((self.start_point[0] - self.end_point[0]) * (self.control_point[0] ** 2 - self.start_point[0] ** 2) +
                   (self.control_point[0] - self.start_point[0]) * (self.end_point[0] ** 2 - self.start_point[0] ** 2))

    #     A = ((m_Y(2) - m_Y(1)) * (m_X(1) - m_X(3)) + _
    #      (m_Y(3) - m_Y(1)) * (m_X(2) - m_X(1))) / _
    #     ((m_X(1) - m_X(3)) * (m_X(2) ^ 2 - m_X(1) ^ 2) + _
    #      (m_X(2) - m_X(1)) * (m_X(3) ^ 2 - m_X(1) ^ 2))
    #
        coef[1] = ((y[1] - y[0]) - coef[2] * (self.control_point[0] ** 2 - self.start_point[0] ** 2)) / \
                  (self.control_point[0] - self.start_point[0])
    # B = ((m_Y(2) - m_Y(1)) - A * (m_X(2) ^ 2 - m_X(1) ^ 2)) _
    #     / (m_X(2) - m_X(1))

        coef[0] = y[0] - coef[2] * self.start_point[0] ** 2 - coef[1] * self.start_point[0]
        return coef
    # C = m_Y(1) - A * m_X(1) ^ 2 - B * m_X(1)
