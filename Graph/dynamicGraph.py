import math
import Utils.vectorMath as vm
from Visual.node import *
from pyglet.gl import *
from graphInterface import *

standard_color = (158, 136, 124)
active_color = (20, 73, 208)
stack_color = (44, 215, 98)

radius_increment = 45
stack_width = 115


class DynamicGraph (graphInterface):
    isDynamic = True

    #Create a visual graph given the program flow, and a list of MethodDeclarations
    def __init__(self, flow, methods):
        #Start node, always main
        self.start = Node(filter(lambda x: x.name == "main", methods)[0])
        #Hash map of class names to method names to nodes
        self.nodes = {}
        #Current node
        self.current = self.start
        #Program flow, an array of strings
        self.flow = flow
        #Array of MethodDeclarations
        self.methods = methods
        #Current position within flow
        self.position = 0
        #Variables for layout of graph
        #self.center_x = 0
        #self.center_y = 0
        #self.zoom = 1
        #Representation of program stack, made up of nodes
        self.stack = []
        self.stacks = {}
        self.cur_thread = 0
        self.central_node = self.start



    #Check if thread_num is the current thread, if not switch
    def check_thread(self, thread_num):
         #Check which thread this command was from and switch cur_thread if necessary
        if thread_num != self.cur_thread:
            #Set stack to the stack for the new thread
            try:
                #print("Switching from thread " + str(self.cur_thread))
                #print(map(lambda x: x.method.name, self.stack))
                self.stack = self.stacks[thread_num]
                #print("To thread " + str(thread_num))
                #print(map(lambda x: x.method.name, self.stack))
                if len(self.stack) > 0:
                    self.current = self.stack[-1]

            #No stack yet exists for this thread, start a new one
            except KeyError:
                #print("Creating new stack for thread " + str(thread_num))
                self.stack = []
                self.stacks[thread_num] = self.stack

            self.cur_thread = thread_num

    #Move forward one step in the program flow
    def step_forward(self):
        if len(self.flow) == 0:
            return False

        if self.position >= len(self.flow):
            return False

        #Retrieve the next command from the program flow in the form
        # push/pop method_name class_name thread_id
        command = self.flow[self.position].split(" ")
        self.check_thread(command[-1])

        if command[0] == "push":
            node = self.get_node(command[1], command[2])
            if node is None:
                node = self.add_node(command[1], command[2])

            self.visit(node)
            self.current = node
            self.stack.append(node)
        else:
            self.stack.pop()

            if len(self.stack) > 0:
                self.current = self.stack[-1]

        self.position += 1

        return True

    #Move one step backwards through the program flow
    def step_backward(self):
        if self.position <= 1:
            return False

        self.position -= 1
        #Get the last executed command so we can reverse it
        command = self.flow[self.position].split(" ")
        #Pop whatever was pushed, decrement visit count, remove if necessary, set current to new end of stack
        if command[0] == "push":
            self.stack.pop()
            node = self.stack[-1]
            node.visit_count[self.current] -= 1

            if node.visit_count[self.current] == 0:
                node.children.remove(self.current)

            self.current = node
        #Push Whatever was popped, and set current to it
        else:
            node = self.get_node(command[2])
            self.stack.append(node)
            self.current = node

        return True

    #Resets the graph to its initial state
    def reset(self):
        self.start = Node(filter(lambda x: x.name == "main", self.methods)[0])
        self.current = self.central_node = self.start
        self.position = 0
        del self.stack[:]

    def build_final(self):
        while self.step_forward():
            pass
        print("Constructed a graph of " + str(len(self.nodes)) + " nodes")
        print("From an array of " + str(len(self.flow)) + " steps")
        self.write()


    #Adds a new node onto the graph for the method with given |node_name| whose parent
    # is the current node
    def add_node(self, node_name, class_name):
        #Find the method with matching name in methods
        #PROBLEM HERE FOR OVERLOADED METHODS
        method = filter(lambda x: x.name == node_name, self.methods)[0]
        node = Node(method, self.current)
        self.current.children.append(node)
        if len(self.current.children) > len(self.central_node.children):
            self.central_node = self.current

        #Add the node into nodes hash
        try:
            self.nodes[class_name][method.name] = node
        except KeyError:
            self.nodes[class_name] = {}
            self.nodes[class_name][method.name] = node

        return node

    #Finds a node by method name and returns it, or None if a node by that name
    # is not in the graph
    def get_node(self, node_name, class_name):
        try:
            class_hash = self.nodes[class_name]
            return class_hash[node_name]
        except KeyError:
            return None

    #Visit the given node from the current node, incrementing it's visit_count
    def visit(self, node):
        #If the node we are going to is not in the current node's children list, add it
        if not node in self.current.children and self.current != node:
            self.current.children.append(node)
            self.current.radius += radius_increment
        #If the node we are going to hasn't yet been visited make an entry in visit_count
        if not node in self.current.visit_count:
            self.current.visit_count[node] = 0
        self.current.visit_count[node] += 1

    #Determines the color for a given node based on current execution
    def get_color(self, node):
        if node == self.current:
            return active_color
        elif node in self.stack:
            return stack_color
        else:
            return standard_color

    #Draws the current state of the graph
    def draw(self, window):
        #Main's position set first
        pyglet.gl.glPushMatrix()
        #Translate to center of window to scale without moving nodes then translate back
        pyglet.gl.glTranslatef(window.width / 2 + node_width / 2, window.height / 2 + node_height / 2, 0)
        pyglet.gl.glScalef(self.zoom, self.zoom, self.zoom)
        pyglet.gl.glTranslatef(-(window.width / 2 + node_width / 2), -(window.height / 2 + node_height / 2), 0)
        #Translate by current center position
        pyglet.gl.glTranslatef(self.center_x, self.center_y, 0)

        self.central_node.set_position(window.width / 2, window.height / 2)

        self.place_nodes()
        self.connect_nodes()
        self.draw_nodes()
        pyglet.gl.glPopMatrix()

        self.draw_stack(window)

        #Main drawn last
        pyglet.gl.glPushMatrix()
        #Translate to center of window to scale without moving nodes then translate back
        pyglet.gl.glTranslatef(window.width / 2 + node_width / 2, window.height / 2 + node_height / 2, 0)
        pyglet.gl.glScalef(self.zoom, self.zoom, self.zoom)
        pyglet.gl.glTranslatef(-(window.width / 2 + node_width / 2), -(window.height / 2 + node_height / 2), 0)
        #Translate by current center position
        pyglet.gl.glTranslatef(self.center_x, self.center_y, 0)

        self.central_node.draw(self.get_color(self.central_node))
        pyglet.gl.glPopMatrix()


    def place_nodes(self):
        stack = [self.start]
        placed_nodes = []
        while len(stack) > 0:
            parent = stack.pop()
            map(lambda x: stack.append(x) if x not in placed_nodes else None, reversed(parent.children))

            for node in parent.children:
                if node not in placed_nodes:
                    if not node.placed():
                        self.set_position(node, parent)
                    self.update_position(node, parent)
                    placed_nodes.append(node)

    def connect_nodes(self):
        stack = [self.start]
        connected_nodes = []
        while len(stack) > 0:
            parent = stack.pop()
            if parent not in connected_nodes:
                map(lambda x: stack.append(x) if x not in connected_nodes else None, reversed(parent.children))

                for node in parent.children:
                    parent.connect(node)

                connected_nodes.append(parent)

    def draw_nodes(self):
        stack = [self.start]
        drawn_nodes = []
        while len(stack) > 0:
            parent = stack.pop()
            if parent not in drawn_nodes:
                map(lambda x: stack.append(x), reversed(parent.children))
                parent.draw(self.get_color(parent))
                drawn_nodes.append(parent)


    def draw_stack(self, window):
        for i, node in enumerate(self.stack):
            pyglet.gl.glPushMatrix()

            x_center = window.width - (stack_width / 2) - 10
            y_center = ((node_height * (i + 1)) - (node_height / 2)) + 80

            pyglet.gl.glTranslatef(x_center, y_center, 0)
            pyglet.gl.glScalef(.9, .9, 1)
            pyglet.gl.glTranslatef(-x_center, -y_center, 0)
            pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                        [0, 1, 2, 1, 2, 3],
                                        ('v2i', (window.width - stack_width - 10,(node_height * (i + 1)) + 80,
                                                window.width - 10, (node_height * (i + 1)) + 80,
                                                window.width - stack_width - 10, (node_height * i) + 80,
                                                window.width - 10, (node_height * i) + 80)),
                                        ('c3B', (103, 72, 194) * 4))

            pyglet.gl.glPopMatrix()
            pyglet.text.Label(node.method.name + "()",
                          font_name='Times New Roman',
                          font_size=12,
                          x = x_center,
                          y = y_center,
                          anchor_y = 'center',
                          anchor_x= 'center').draw()


    #Sets the initial position of |node| based on its parent location and the location of |central_node|
    def set_position(self, node, parent):

        if parent is self.central_node:
            direction = vm.normalize((math.sin(math.pi / 4) + len(parent.children), math.cos(math.pi / 4)))
            node.set_position(int(parent.x + (parent.radius * direction[0])),
                              int(parent.y + (parent.radius * direction[1])))
        else:
            direction = self.central_node.get_direction(parent)
            #Small offset based on number of children, this makes nodes not spawn right on top of each other
            direction = vm.normalize((direction[0] + len(parent.children), direction[1]))
            node.set_position(int(parent.x + (parent.radius * direction[0])),
                              int(parent.y + (parent.radius * direction[1])))

    #Updates the position of |node| based on its siblings locations and the location of main
    def update_position(self, node, parent):
        movement = vm.add_vectors(parent.get_direction(node), self.central_node.get_direction(node))
        for sibling in parent.children:
            if sibling is not node:
                #Get the direction going away from the sibling, and add it into total movement vector
                movement = vm.add_vectors(movement, sibling.get_direction(node))

        movement = vm.normalize(movement)

        new_x = int(parent.x + (parent.radius * movement[0]))
        new_y = int(parent.y + (parent.radius * movement[1]))
        node.set_position(new_x, new_y)

    def write(self):
        stack = [self.start]
        visited_nodes = []
        while len(stack) > 0:
            node = stack.pop()
            map(lambda x: stack.append(x) if not x in visited_nodes else None, node.children)
            node.write()
            visited_nodes.append(node)

