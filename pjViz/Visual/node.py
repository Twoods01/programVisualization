__author__ = 'twoods0129'

import operator as op
import pyglet
from pjViz.constants import Constants
import pjViz.Utils.vectorMath as vm
import pjViz.Utils.spline as spline

init_radius = 150
node_height = 70
node_width = 114
x_offset = node_width / 2
y_offset = node_height / 2

node_vertices = {}

class Node:
    texture = pyglet.image.load('Visual/rr.png').get_texture()

    #Construct a new Node given a MethodDeclaration which it represents, and a parent if it has one
    def __init__(self, method, parent=None, visible=True):
        #Array of child nodes
        self.child_branches = []
        #Array of parent nodes
        self.parents = []
        if parent is not None:
            self.parents.append(parent)
        #Hash of number of times this node has been visited by other nodes
        # key is the node, value is the number of visits
        self.visit_count = {}
        #Hash of splines which form the path from this node to its parents
        #key is the parent node, value is the Spline
        self.splines = {}
        #x,y location on screen
        self.x = -1
        self.y = -1

        #Branch and index of this node
        self.branch = 0
        self.index = 0

        #The method which this node represents
        self.method = method
        self.radius = init_radius
        self.visible = visible

    def add_parent(self, parent):
        self.parents.append(parent)

    #Print for debugging
    def write(self):
        print(self.method.name)
        print(' children ' + str(self.child_branches))
        print(' parents ' + str(map(lambda x: x.method.name, self.parents)))

    #Set x,y position of this node
    def set_position(self, x, y):
        self.x = x
        self.y = y

    #Draw the node with the given color
    def draw(self, color, additional_draw_task=None, texture=True):
        if not self.visible:
            if additional_draw_task != None:
                additional_draw_task()
            return

        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslatef(self.x, self.y, 0)

        #Check if we've drawn a node of this color before, if not create a vertex list for it
        if not color in node_vertices:
            node_vertices[color] = pyglet.graphics.vertex_list_indexed(4,
                                    [0, 1, 2, 0, 2, 3],
                                    ('v3i', (-57, -35, 0,
                                            57, -35, 0,
                                            57, 35, 0,
                                            -57, 35, 0)),
                                    ('t2f', (0.0, 0.0,
                                             1.0, 0.0,
                                             1.0, 1.0,
                                             0.0, 1.0)),
                                    ('c4B', (color[0], color[1], color[2], 255) * 4))

        if texture:
            pyglet.gl.glEnable(Node.texture.target)
            pyglet.gl.glBindTexture(Node.texture.target, Node.texture.id)

        node_vertices[color].draw(pyglet.gl.GL_TRIANGLES)
        if additional_draw_task != None:
            pyglet.gl.glPopMatrix()
            additional_draw_task()
            pyglet.gl.glPushMatrix()
            pyglet.gl.glTranslatef(self.x, self.y, 0)

        #Label it with method name
        pyglet.text.Label(self.method.name + "()",
                          font_name= Constants.font,
                          font_size=12,
                          x = 0,
                          y = 0,
                          anchor_y = 'center',
                          anchor_x= 'center').draw()

        if texture:
            pyglet.gl.glDisable(Node.texture.target)
        pyglet.gl.glPopMatrix()

    def add_branch(self, branch_num):
        self.child_branches.append(branch_num)

    #Returns true if this node has been given a location, otherwise false
    def placed(self):
        return self.x != -1 and self.y != -1

    #Returns a vector containing the direction from self to node
    def get_direction(self, node):
        return vm.normalize(map(op.sub, (node.x, node.y), (self.x, self.y)))

    #Given x, y coordinate and current camera position determine if that coordinate is inside the node
    def hit(self, x, y):
        return x > self.x - x_offset  and x < self.x + node_width - x_offset\
               and y > self.y - y_offset and y < self.y + node_height - y_offset

    #Connect current node to |node| UNUSED
    def connect(self, color=[237, 255, 228]):
        pyglet.gl.glLineWidth(3)
        for p in self.parents:
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                ('v2i', (int(self.x), int(self.y),
                                         int(p.x), int(p.y))),
                                ('c3B', (color[0], color[1], color[2]) * 2))


    #Draw an edge from self to node, using a spline
    def draw_edge(self, node, color=[255, 255, 255], up=False, control=None):
        pyglet.gl.glLineWidth(3)
        if not node in self.splines:
            self.splines[node] = spline.Spline(self, node, up=up, control=control)

        if not self in node.splines:
            node.splines[self] = self.splines[node]

        self.splines[node].draw(color)