__author__ = 'twoods0129'
from pyglet.gl import *
from node import *

stack_width = 115
stack_color = (44, 215, 98)

class Stack:

    def __init__(self, window):
        self.stack = []
        self.window = window

    def append(self, node):
        node.set_position(self.window.width - node_width - 10, ((node_height + 5) * (len(self.stack) + 1)))
        self.stack.append(node)

    def pop_to(self, node):
        while self.stack[-1] != node:
            self.stack.pop()

    def draw(self):
        map(lambda x: x.draw(stack_color), self.stack)


    #returns the method which was clicked or none if the coordinates are not part of the stack
    def get_clicked_item(self, x, y):
        for node in self.stack:
            if node.hit(x, y):
                return node
        return None

