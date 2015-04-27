__author__ = 'twoods0129'
from pyglet.gl import *
from node import *

stack_width = 115
stack_color = (98, 178, 60)

class Stack():

    def __init__(self, window):
        self.stack = []
        self.window = window

    def append(self, frame):
        frame.node.set_position(self.window.width - node_width - 10, ((node_height + 5) * (len(self.stack) + 1)))
        self.stack.append(frame)

    def pop_to(self, node):
        f = self.stack[-1]
        while self.stack[-1].node != node:
            f = self.stack.pop()
        return f

    def get_frame_after_pop(self):
        return self.stack[-2]

    def draw(self):
        map(lambda x: x.node.draw(stack_color), self.stack)

    #returns the method which was clicked or none if the coordinates are not part of the stack
    def get_clicked_item(self, x, y):
        for frame in self.stack:
            if frame.node.hit(x, y):
                return frame.node
        return None

class Frame():

    def __init__(self, node, branch, index):
        self.node = node
        self.branch = branch
        self.index = index

    def __str__(self):
        return self.node.method.name + " " + str(self.branch) + ":" + str(self.index)

