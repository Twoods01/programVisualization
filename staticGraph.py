__author__ = 'twoods0129'

from node import *
from pyglet.gl import *
from graphInterface import *
from model import MethodDeclaration, MethodInvocation
from stack import *
import dataView as dv
import arrayUtils


standard_color = (158, 136, 124)
path_highlight = (250, 255, 41)
active_color = (13, 136, 204)
library_method_color = (200, 73, 38)

horizontal_buffer = 35
vertical_buffer = 30

class StaticGraph(graphInterface):
    isDynamic = False
    frames_per_node = 10

    def __init__(self, parsed, window):
        self.stack = Stack(window)
        #All parsed data
        self.parsed = parsed
        #Program flow
        self.flow = parsed.run_file()
        #Current branch of execution
        self.cur_branch = 0
        self.cur_branch_index = 0
        #Current index into flow
        self.cur_index = 0
        #The currently active node in the animation
        self.active_node = None
        self.animation_path = []
        self.auto_play = False
        self.frames = 0

        #Array of MethodDeclarations
        self.methods = parsed.get_all_methods()
        #current node, starts as a fake function which calls main
        specical_start_node = MethodDeclaration("", body = [MethodInvocation("main")])

        #The current method being visualized
        self.current = Node(specical_start_node)
        #Array of nodes for methods within current
        self.nodes = []
        self.data = dv.DataView(parsed)

        #Invisible node which we can place underneath data to connect them to other methods
        self.invis_node = None

        self.place_nodes(window)

    def draw(self, window, cam):

        #Move forward on the animation path if necessary
        if len(self.animation_path) > 0 and self.frames >= self.frames_per_node:
            self.active_node = self.animation_path[0]
            del self.animation_path[0]
            self.frames = 0
        #Nothing more to animate, determine next animation step
        elif self.auto_play and self.frames >= self.frames_per_node:
            self.step_forward()
            self.frames = 0

        #For animation, center the camera on the active node
        if self.auto_play:
            cam.center_on(self.active_node)

        #Connect(draw edges) all nodes
        for branch in self.nodes:
            for node in branch:
                if node in self.animation_path:
                    node.connect(path_highlight)
                else:
                    node.connect()

        #Draw all nodes
        for branch in self.nodes:
            for node in branch:
                if node == self.active_node:
                    node.draw(active_color)
                elif node.method.name in map(lambda x: x.name, self.methods):
                    node.draw(standard_color)
                else:
                    node.draw(library_method_color)

        #If mousing over data, show connections to all usages
        if self.invis_node:
            self.invis_node.connect()

        #For animation, highlight data relating to active node
        if self.auto_play:
            fields = self.parsed.get_fields_in_method(self.active_node.method)
            self.data.clear_highlights()
            self.data.highlight(fields)

        self.frames += 1


    def draw_UI(self, window):
        self.stack.draw()
        self.data.draw(window)

    def place_nodes(self, window):
        self.nodes = []

        x = 75
        y = window.height / 2
        self.chain_nodes(self.parsed.get_method_invocations_in_method(self.current.method), None, x, y, 0)
        self.active_node = self.nodes[0][0]
        self.cur_branch = self.cur_branch_index = 0

        self.cur_index = self.find_in_flow("push " + self.current.method.name)

    #Find the first occurence of this string in flow and return that index
    def find_in_flow(self, string):
        index = 0
        for line in self.flow:
            index += 1
            if string in line:
                break

        return index

    #Finds the corresponding pop to the push at cur_index
    def find_corresponding_pop(self, method_name=None, class_name=None):
        index = self.cur_index
        if not method_name:
            print_out = self.flow[index].split(" ")
            method_name = print_out[1]
            class_name = print_out[2]

        #The pop we're looking for
        string_to_find = "pop " + method_name + " " + class_name
        #If the current method is called again before the pop is found we need to keep track
        additional_call_string = "push " + method_name + " " + class_name
        additional_method_calls = 0

        for line in self.flow[self.cur_index:]:
            index += 1
            if string_to_find in line:
                if additional_method_calls == 0:
                    break
                else:
                    additional_method_calls -= 1
            elif additional_call_string in line:
                additional_method_calls += 1

        return index

    def handle_non_user_methods_in_current_branch(self, method_to_find):
        #Need to account for non-user methods in the branch, which have no corresponding print
        while self.cur_branch_index < len(self.nodes[self.cur_branch]) and \
                        self.nodes[self.cur_branch][self.cur_branch_index].method.name != method_to_find:

            self.animation_path.append(self.nodes[self.cur_branch][self.cur_branch_index])
            #If we've hit a return then stop
            if self.nodes[self.cur_branch][self.cur_branch_index].method.name == "Return":
                break
            self.cur_branch_index += 1

    def step_forward(self):
        #If we havent finished the current animation then ignore this call
        if len(self.animation_path) > 0:
            return
        #If we're already done with this method then ignore this call
        if self.active_node.method.name == "Return":
            return

        new_branch = None
        exited_method = False
        #Find the next print out relating to a new method call
        try:
            while True:
                next_method_print = self.flow[self.cur_index].split(" ")
                self.cur_index += 1

                #New branch
                if next_method_print[0] == "branch":
                    new_branch = int(next_method_print[1])
                #New method call
                elif next_method_print[0] == "push":
                    break
                #Returning from this method
                elif "pop " + self.current.method.name in self.flow[self.cur_index - 1]:
                    exited_method = True
                    break



        #We've gone past the end of the file
        except IndexError:
            #Set active node to last node
            self.active_node = self.nodes[-1][-1]
            return

        #If we exited the method, add everything left in the current branch
        if exited_method:
            if new_branch:
                self.cur_branch = new_branch
                self.cur_branch_index = 0
            self.animation_path.extend(self.nodes[self.cur_branch][self.cur_branch_index:])

        else:
            #Branch hasn't changed and there's more nodes in this branch
            if not new_branch and self.cur_branch_index < len(self.nodes[self.cur_branch]) - 1:
                self.cur_branch_index += 1
                self.handle_non_user_methods_in_current_branch(next_method_print[1])
             #Ran out of nodes in this branch without a new branch printout, this means we
            # took a branch with an invisible node
            elif not new_branch:
                #Get everything remaining from current branch
                self.handle_non_user_methods_in_current_branch("")

                #Get the branch number for the invisible branch we took
                invis_node_branch = self.active_node.child_branches[1]
                #Add the invisible node
                self.animation_path.append(self.nodes[invis_node_branch][0])

                #Follow the invisible branch to it's child
                self.cur_branch = self.nodes[invis_node_branch][0].child_branches[0]
                self.cur_branch_index = 0

                #Get anything in new branch before actual method
                self.handle_non_user_methods_in_current_branch(next_method_print[1])

            #Branch changed
            #If the new branch is smaller then we went backwards in the file, aka a loop
            elif new_branch <= self.cur_branch:
                self.cur_branch = new_branch
                back_branch_node = self.nodes[self.cur_branch - 1][0]
                #Get the repeat node, it is the first node in this nodes child branch
                self.animation_path.append(self.nodes[back_branch_node.child_branches[0]][0])

                #Get the back edge, it should always be the previous branch
                self.animation_path.append(back_branch_node)

                #Get the loop start, it should always be the last node 2 branches prior
                self.animation_path.append(self.nodes[self.cur_branch - 2][-1])


            #Standard new forward branch
            elif new_branch > self.cur_branch:
                #Get everything remaining from current branch
                self.handle_non_user_methods_in_current_branch("")

                #Update current branch
                self.cur_branch = new_branch
                self.cur_branch_index = 0

                #Get anything in new branch before actual method
                self.handle_non_user_methods_in_current_branch(next_method_print[1])


            #Add the actual method
            self.animation_path.append(self.nodes[self.cur_branch][self.cur_branch_index])

            #Jump ahead to when the method we just entered gets popped
            self.cur_index = self.find_corresponding_pop(next_method_print[1], next_method_print[2])

        return

    #Recursively chains branched_node_array together, returns the parents of the previous branch
    def chain_nodes(self, branched_node_array, parent_nodes, x, y, branch_num, break_flag=False):
        if len(branched_node_array) == 0:
            return None, branch_num

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
                final_nodes_in_branch, branch_num = self.chain_nodes(branch, parent_nodes, x, y, branch_num + 1)
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
            final_nodes, branch_num = self.chain_nodes(branched_node_array[1:], new_parents, x + ((node_width + horizontal_buffer) * longest_array_length), y, branch_num)

            #If the returned node was None, this node is the final in a branch, return it
            if final_nodes is None:
                return new_parents, branch_num
            #Else final node has already been found, pass it along
            else:
                return final_nodes, branch_num

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

                        if parent.method.name == "InvisibleNode":
                            parent.add_branch(branch_num + 1)
                        else:
                            parent.add_branch(branch_num)

                if len(parent_nodes) > 1:
                    branch_num += 1

            #Add the node to the node list
            try:
                self.nodes[branch_num].append(node)
            except IndexError:
                self.nodes.append([])
                self.nodes[branch_num].append(node)

            #Recurse on remaining array
            final_node, branch_num = self.chain_nodes(branched_node_array[1:], parents, x + node_width + horizontal_buffer, y, branch_num, break_flag=len(parents) > 1)

            #If the returned node was None, this node is the final in a branch, return it
            if final_node is None:
                return [node], branch_num
            #Else final node has already been found, pass it along
            else:
                return [final_node], branch_num

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

    #Need to handle cam zoom somehow
    def handle_mouse(self, x, y, cam):
        self.invis_node = None
        inside_node = False
        for branch in self.nodes:
            for node in branch:
                if node.hit(x, y, cam.x, cam.y):
                    inside_node = True
                    fields = self.parsed.get_fields_in_method(node.method)
                    self.data.highlight(fields)
                    break

        if not inside_node:
            obj = self.data.hit(x, y)
            if obj:
                inside_node = True
                self.invis_node = Node(MethodInvocation("InvisibleNode"), visible=False)
                self.invis_node.set_position(obj.x + cam.x, obj.y + cam.y)

                for branch in self.nodes:
                    for node in branch:
                        fields = self.parsed.get_fields_in_method(node.method)
                        for field in fields:
                            if obj.includes(field):
                                self.invis_node.add_parent(node)


        return inside_node

    def print_branched_nodes(self):
        for i, branch in enumerate(self.nodes):
            print("branch " + str(i) + " is " + str(map(lambda x: x.method.name, branch)))
            map(lambda x: x.write(), branch)


    def handle_input(self, x, y, cam, window):

        for branch in self.nodes:
            for node in branch:
                if node.hit(x, y, cam.x, cam.y):
                    method = filter(lambda x: x.name == node.method.name, self.methods)
                    if len(method) > 0:
                        self.current = Node(method[0])
                        self.data.add_params(method[0].get_data())
                        self.stack.append(self.current)
                        cam.reset()
                        self.place_nodes(window)
                    return

        node = self.stack.get_clicked_item(x, y)

        if node is not None:
            self.current = node
            self.stack.pop_to(node)
            self.data.add_params(node.method.parameters)
            cam.reset()
            self.place_nodes(window)