__author__ = 'twoods0129'

class graphInterface:

    def __init__(self, flow, methods):
        #Variables for layout of graph
        self.center_x = 0
        self.center_y = 0
        self.zoom = 1
        pass

    isDynamic = False

    def draw(self, window):
        raise NotImplementedError( "Should have implemented this" )

    def step_forward(self):
        raise NotImplementedError( "Should have implemented this" )

    def step_backwards(self):
        raise NotImplementedError( "Should have implemented this" )

    def write(self):
        raise NotImplementedError( "Should have implemented this" )