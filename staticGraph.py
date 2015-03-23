__author__ = 'twoods0129'

from node import *
from pyglet.gl import *
from graphInterface import *
from model import MethodDeclaration, MethodInvocation
from stack import *
import dataView as dv
import arrayUtils


standard_color = (158, 136, 124)
library_method_color = (200, 73, 38)

horizontal_buffer = 35
vertical_buffer = 30

class StaticGraph(graphInterface):
    isDynamic = False

    def __init__(self, parsed, window):
        self.stack = Stack(window)
        #All parsed data
        self.parsed = parsed
        #Array of MethodDeclarations
        self.methods = parsed.get_all_methods()
        #current node, starts as a fake function which calls main
        specical_start_node = MethodDeclaration("", body = [MethodInvocation("main")])
        self.current = Node(specical_start_node)
        #Array of nodes for methods within current
        self.nodes = []
        self.data = dv.DataView(parsed)
        self.needs_redraw = True
        self.frames_drawn = 0

        #Invisible node which we can place underneath data to connect them to other methods
        self.invis_node = None

        self.place_nodes(window)

    def draw(self, window):
        if not self.needs_redraw:
            return

        for node in self.nodes:
            node.connect()

        for node in self.nodes:
            if node.method.name in map(lambda x: x.name, self.methods):
                node.draw(standard_color)
            else:
                node.draw(library_method_color)

        if self.invis_node:
            self.invis_node.connect()

        self.frames_drawn += 1

        if self.frames_drawn == 2:
            self.needs_redraw = False

    def draw_UI(self, window):
        self.stack.draw()
        self.data.draw(window)

    def place_nodes(self, window):
        self.nodes = []

        x = 75
        y = window.height / 2
        self.chain_nodes(self.parsed.get_method_invocations_in_method(self.current.method), None, x, y)

    #Recursively chains branched_node_array together, returns the parents of the previous branch
    def chain_nodes(self, branched_node_array, parent_nodes, x, y, break_flag=False):
        if len(branched_node_array) == 0:
            return None

        #New branch
        if hasattr(branched_node_array[0], '__iter__'):
            #Store the Y position the branch starts at
            start_y = y
            #Calculate the total number of branches in this branch recursively
            number_of_branches = self.count_branches(branched_node_array[0])

            #Height of this branch is the height of a node times the number of branches
            total_height = ((vertical_buffer + node_height) * number_of_branches)

            #For the first path in this branch, determine half of it's height
            half_height_cur_branch = ((self.count_branches(branched_node_array[0][0]) * (node_height + vertical_buffer)) / 2)
            #Increment Y by half the total height minus half the height of the first path
            y += (total_height / 2) - half_height_cur_branch

            #Find the longest path within this branch
            longest_array_length = self.longest_array(branched_node_array[0])
            new_parents = []
            i = 0

            #For every path in this branch
            for branch in branched_node_array[0]:
                #Recurse on the path, store the returned final_node and add it to our new parent set
                final_nodes_in_branch = self.chain_nodes(branch, parent_nodes, x, y)
                #Filter out nodes with method name Return, as this stops execution
                new_parents.extend(filter(lambda x: x.method.name != "Return", arrayUtils.flatten(final_nodes_in_branch)))

                #Calculate half of the height of this path and the next path if there is one
                half_height_this_branch = (((self.count_branches(branch) + 1) * (node_height + vertical_buffer)) / 2)
                try:
                    half_height_next_branch = (((self.count_branches(branched_node_array[0][i + 1]) - 1) * (node_height + vertical_buffer)) / 2)
                except IndexError:
                    half_height_next_branch = 0

                #Decrement Y by half the height of this path and half the height of the next
                y -= half_height_this_branch + half_height_next_branch
                i += 1

            #Return Y to its initial position
            y = start_y
            #Recurse on the remaining array, with new_parents, and x incremented by the longest path in the branch
            final_nodes = self.chain_nodes(branched_node_array[1:], new_parents, x + ((node_width + horizontal_buffer) * longest_array_length), y)

            #If the returned node was None, this node is the final in a branch, return it
            if final_nodes is None:
                return new_parents
            #Else final node has already been found, pass it along
            else:
                return final_nodes

        #Single Node
        else:
            #Create the node, set it's position and connect it to all of it's parents
            visible = branched_node_array[0].name != "InvisibleNode"
            node = Node(branched_node_array[0], visible=visible)
            node.set_position(x, y)

            parents = [node]

            if parent_nodes is not None:

                if not break_flag:
                    parents.extend(filter(lambda x: x.method.name == "Break", parent_nodes))

                for parent in parent_nodes:
                    if break_flag or parent.method.name != "Break":
                        node.add_parent(parent)

            #Add the node to the node list
            self.nodes.append(node)

            #Recurse on remaining array
            final_node = self.chain_nodes(branched_node_array[1:], parents, x + node_width + horizontal_buffer, y, break_flag=len(parents) > 1)

            #If the returned node was None, this node is the final in a branch, return it
            if final_node is None:
                return [node]
            #Else final node has already been found, pass it along
            else:
                return [final_node]

    #Returns the length of the longest array found within |nested_array|
    def longest_array(self, nested_array):
        #Not an array
        if not hasattr(nested_array, '__iter__'):
            return 1
        #Non-Nested array
        if not any(hasattr(el, '__iter__') for el in nested_array):
            return len(nested_array)
        #Nested array
        else:
            total_len = 0
            longest = 0
            for branch in nested_array:
                if hasattr(branch, '__iter__'):
                    length = self.longest_array(branch)

                    if length > longest:
                        longest = length

                else:
                    total_len += 1 + longest
                    longest = 0

            if longest != 0:
                total_len += longest

            return total_len

    #Returns the number of branches within nested_array
    def count_branches(self, nested_array):
        if not hasattr(nested_array, '__iter__'):
            return 0

        branches = 0
        has_inner_branches = False
        for branch in nested_array:
            if hasattr(branch, '__iter__'):
                has_inner_branches = True
                branches += self.count_branches(branch)

        if not has_inner_branches:
            branches += 1

        return branches

    def redraw(self):
        self.needs_redraw = True
        self.frames_drawn = 0

    #Need to handle cam zoom somehow
    def handle_mouse(self, x, y, cam):
        self.invis_node = None
        inside_node = False
        for node in self.nodes:
            if node.hit(x, y, cam.x, cam.y):
                inside_node = True
                fields = self.parsed.get_fields_in_method(node.method)
                self.data.highlight(fields)
                self.redraw()
                break

        if not inside_node:
            obj = self.data.hit(x, y)
            if obj:
                inside_node = True
                self.invis_node = Node(MethodInvocation("InvisibleNode"), visible=False)
                self.invis_node.set_position(obj.x + cam.x, obj.y + cam.y)

                for node in self.nodes:
                    fields = self.parsed.get_fields_in_method(node.method)
                    for field in fields:
                        if obj.includes(field):
                            self.invis_node.add_parent(node)

                self.redraw()

        return inside_node

    def handle_input(self, x, y, cam, window):

        for node in self.nodes:
            if node.hit(x, y, cam.x, cam.y):
                method = filter(lambda x: x.name == node.method.name, self.methods)
                if len(method) > 0:
                    self.current = Node(method[0])
                    self.data.add_params(method[0].get_data())
                    self.stack.append(self.current)
                    self.redraw()
                    cam.reset()
                    self.place_nodes(window)
                return

        node = self.stack.get_clicked_item(x, y)

        if node is not None:
            self.current = node
            self.stack.pop_to(node)
            self.data.add_params(node.method.parameters)
            self.redraw()
            cam.reset()
            self.place_nodes(window)