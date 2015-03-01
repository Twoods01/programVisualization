__author__ = 'twoods0129'

import operator as op
import pyglet
import vectorMath as vm

init_radius = 150
node_height = 70
node_width = 115

class Node:
    #Construct a new Node given a MethodDeclaration which it represents, and a parent if it has one
    def __init__(self, method, parent=None, visible=True):
        #Array of child nodes
        self.children = []
        #Array of parent nodes
        self.parents = []
        if parent is not None:
            self.parents.append(parent)
        #Hash of number of times this node has been visited by other nodes
        # key is the node, value is the number of visits
        self.visit_count = {}
        #x,y location on screen
        self.x = -1
        self.y = -1
        #The method which this node represents
        self.method = method
        self.radius = init_radius
        self.visible = visible

    #Print for debugging
    def write(self):
        print(self.method.name)
        print(' children ' + str(map(lambda x: x.method.name, self.children)))
        print(' parents ' + str(map(lambda x: x.method.name, self.parents)))

    #Set x,y position of this node
    def set_position(self, x, y):
        self.x = x
        self.y = y

    #Draw the node with the given color
    def draw(self, color):
        if not self.visible:
            return

        #Draw the method as a box
        pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                    [0, 1, 2, 0, 2, 3],
                                    ('v2i', (self.x, self.y,
                                            self.x + node_width, self.y,
                                            self.x + node_width, self.y + node_height,
                                            self.x, self.y + node_height)),
                                    ('c3B', (color[0], color[1], color[2]) * 4))
        #Label it with method name
        pyglet.text.Label(self.method.name + "()",
                          font_name='Times New Roman',
                          font_size=12,
                          x = self.x + (node_width / 2),
                          y = self.y + (node_height / 2),
                          anchor_y = 'center',
                          anchor_x= 'center').draw()

    #Returns true if this node has been given a location, otherwise false
    def placed(self):
        return self.x != -1 and self.y != -1

    #Returns a vector containing the direction from self to node
    def get_direction(self, node):
        return vm.normalize(map(op.sub, (node.x, node.y), (self.x, self.y)))

    #Given x, y coordinate determine if that coordinate is inside the node
    def hit(self, x, y):
        return x > self.x  and x < self.x + node_width and y > self.y and y < self.y + node_height


    #Connect current node to |node|
    def connect(self, node):
        pyglet.gl.glLineWidth(3)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            ('v2i', (self.x + (node_width / 2), self.y + (node_height / 2),
                                     node.x + (node_width / 2), node.y + (node_height / 2))))
