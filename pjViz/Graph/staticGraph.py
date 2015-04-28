__author__ = 'twoods0129'

from pjViz.Visual.node import *
from pyglet.gl import *
from graphInterface import *
from pjViz.Parser.model import MethodDeclaration, MethodInvocation
from pjViz.Visual.stack import *
import pjViz.Visual.dataView as dv
import pjViz.Utils.arrayUtils, pjViz.Visual.animationDot


standard_color = (204, 127, 93)
path_highlight = (64, 76, 255)
library_method_color = (200, 79, 26)

horizontal_buffer = 35
vertical_buffer = 30

class StaticGraph(graphInterface):
    isDynamic = False
    frames_per_node = 10

    def __init__(self, parsed, window, cam, flow):
        self.stack = Stack(window)
        #All parsed data
        self.parsed = parsed
        #Program flow
        self.flow = flow #parsed.run_file()
        #Current branch of execution
        self.cur_branch = 0
        self.cur_branch_index = 0
        #Current index into flow
        self.cur_index = 0
        #Previous index into flow, needed to account for swapping over to into
        # initialize to anything but 0
        self.prev_index = 1
        #The currently active node in the animation
        self.active_node = None
        self.animation_path = []
        self.auto_play = False
        self.dot = pjViz.Visual.animationDot.AnimationDot(self.animation_forward, self.update_active_node)
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

        self.cam = cam
        self.window = window
        self.place_nodes(window)
        #Put the dot on start and add main and return to path
        self.dot.place(self.nodes[0][0].x, self.nodes[0][0].y)
        self.animation_path.append(self.nodes[0][1])
        self.animation_path.append(self.nodes[0][2])

    def draw(self):
        #For animation, center the camera on the active node
        if self.auto_play:
            delta = self.cam.center_on(self.dot.x, self.dot.y)
            if self.invis_node:
                self.invis_node.x += delta[0]
                self.invis_node.y += delta[1]

        #Connect(draw edges) all nodes
        for branch in self.nodes:
            for node in branch:
                for p in node.parents:
                    if (node in self.animation_path or node == self.active_node)\
                            and (p in self.animation_path or p == self.active_node):
                        node.draw_edge(p, path_highlight)
                    else:
                        node.draw_edge(p)

        #Draw all nodes
        for branch in self.nodes:
            for node in branch:
                if node.method.name in map(lambda x: x.name, self.methods):
                    if node == self.active_node:
                        node.draw(standard_color, self.dot.draw)
                    else:
                        node.draw(standard_color)
                else:
                    if node == self.active_node:
                        node.draw(library_method_color, self.dot.draw)
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

    def draw_UI(self):
        self.stack.draw()
        self.data.draw()
        self.dot.draw_ui()

    #Determines x/y coordinates to place nodes at and seeks cur_index to the proper location
    def place_nodes(self, in_animation=False):
        self.nodes = []
        x = 75
        y = self.window.height / 2
        self.chain_nodes(self.parsed.get_method_invocations_in_method(self.current.method), None, x, y, 0)

        if not in_animation:
            self.cur_index = self.find_in_flow("push " + self.current.method.name)

        self.active_node = self.nodes[self.cur_branch][self.cur_branch_index]

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

        index = self.prev_index = self.cur_index
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

    #Adds all non-user methods in the current branch into the animation path, up to |method_to_find|
    # if |method_to_find| is empty it adds the entire branch
    # return True if a return was found, false otherwise
    def handle_non_user_methods_in_current_branch(self, method_to_find = ""):
        #Need to account for non-user methods in the branch, which have no corresponding print
        while self.cur_branch_index < len(self.nodes[self.cur_branch]) and \
                        self.nodes[self.cur_branch][self.cur_branch_index].method.name != method_to_find:

            #Add the node to the path as long as it's not a manually added start node
            new_node = self.nodes[self.cur_branch][self.cur_branch_index]
            if new_node.method.name != "Start" and new_node != self.active_node:
                self.animation_path.append(new_node)
            #If we've hit a return then stop
            if self.nodes[self.cur_branch][self.cur_branch_index].method.name == "Return":
                return True
            self.cur_branch_index += 1

        return False

    #Callback used by animation dots
    def update_active_node(self, node):
        self.active_node = node
        del self.animation_path[0]

        #Done with the current method and not step into, turn off auto-play
        if self.active_node.method.name == "Return":
            if not self.dot.step_into:
                self.auto_play = False

    #Move the animation forward to the next node, called from main when spacebar pressed
    # and callback from animation_dot when it needs a new target
    def animation_forward(self, enter_method=True):
        #Autoplay not set, stop animation
        if not self.auto_play:
            return

        #If set to step into may have to take extra action
        if self.dot.step_into and enter_method:
            method = filter(lambda x: x.name == self.active_node.method.name, self.methods)

            #Currently on a user method, need to enter this method
            if len(method) > 0:
                #Make sure the method we're supposed to be entering is the one we're on, this is the if check pre-emption issue
                method_to_enter = self.flow[self.cur_index - 1].split(" ")[1]
                if self.active_node.method.name == method_to_enter:
                    self.enter_new_method(Node(method[0]), entering=True, in_animation=True)

                self.dot.wait()
                return

        #Nothing more on current path, update path
        if len(self.animation_path) == 0:
            self.step_forward()

        #If after a step forward the length is still 0 we've reached the end
        if len(self.animation_path) == 0:
            if self.dot.step_into:
                try:
                    frame = self.stack.get_frame_after_pop()
                #End of main
                except IndexError:
                    return

                self.enter_new_method(frame.node, entering=False, in_animation=True)
                self.dot.wait()
                return
            else:
                return

        #Give animation_dot it's next target
        self.dot.set_destination(self.animation_path[0])

    #Find the next method push from |flow|, this can lead to multiple animation_forwards
    def step_forward(self):
        #If we haven't finished the current animation then ignore this call
        if len(self.animation_path) > 0:
            return
        #If we're already done with this method then ignore this call
        if self.active_node.method.name == "Return":
            return

        new_branches = []
        exited_method = False
        #Find the next print out relating to a new method call
        try:
            while True:
                next_method_print = self.flow[self.cur_index].split(" ")
                self.cur_index += 1

                #New branch
                if next_method_print[0] == "branch":
                    new_branches.append(int(next_method_print[1]))
                #New method call
                elif next_method_print[0] == "push":
                    break
                #Returning from this method
                elif "pop " + self.current.method.name in self.flow[self.cur_index - 1]:
                    break

        #We've gone past the end of the file
        except IndexError:
            print("Finished file")
            #Put last node on the path and exit
            self.animation_path.append(self.nodes[-1][-1])
            return

        #If we've gone through any new branches their numbers will be in this array, need to find our way to the branch
        # and add everything in it, unless it's the last branch which is where the method we're trying to find is
        for i, branch in enumerate(new_branches):
            loop = False

            #Handle loops, need to save the original branch we are trying to get to as well as calculate the back
            # edge we will be taking
            if branch <= self.cur_branch:
                back_branch_node = self.nodes[branch - 1][0]
                loop = True
                branch = back_branch_node.child_branches[0]

            #Find path to the branch
            while self.cur_branch != branch:
                #Add everything in the current branch
                if self.handle_non_user_methods_in_current_branch():
                    break

                #If we can get to our target branch from where we currently are
                if branch in self.nodes[self.cur_branch][-1].child_branches:
                    self.cur_branch = branch
                #Otherwise take the bottom (InvisibleNode) branch unless it goes past our target
                elif self.nodes[self.cur_branch][-1].child_branches[-1] > branch:
                        self.cur_branch = self.nodes[self.cur_branch][-1].child_branches[0]
                else:
                    self.cur_branch = self.nodes[self.cur_branch][-1].child_branches[-1]

                self.cur_branch_index = 0

            #If this is a loop, we now have the path to the branch containing repeat and loopEnd
            if loop:
                #Add repeat
                self.animation_path.append(self.nodes[self.cur_branch][0])
                #Add the back_branch_node
                self.animation_path.append(back_branch_node)
                #Add loop start
                self.animation_path.append(back_branch_node.parents[0])
                #Update branches
                self.cur_branch = back_branch_node.parents[0].child_branches[-1]
                self.cur_branch_index = 0

        #Since branches can change without print-outs, need to verify that the branch we ended in actually contains
        # the method we're looking for
        while not next_method_print[1] in map(lambda x: x.method.name, self.nodes[self.cur_branch]):
            #Add everything in current method
            if self.handle_non_user_methods_in_current_branch():
                break

            #Follow the last branch out
            self.cur_branch = self.nodes[self.cur_branch][-1].child_branches[-1]
            self.cur_branch_index = 0

        if not "Return" in map(lambda x: x.method.name, self.animation_path):
            #Add everything in the final branch, up to the method
            self.handle_non_user_methods_in_current_branch(next_method_print[1])
            #Add the method
            self.animation_path.append(self.nodes[self.cur_branch][self.cur_branch_index])

            #Jump ahead to when the method we just entered gets popped
            if not self.dot.step_into:
                self.cur_index = self.find_corresponding_pop(next_method_print[1], next_method_print[2])
            else:
                self.prev_index = 0

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
                new_parents.extend(filter(lambda x: x.method.name != "Return", pjViz.Utils.arrayUtils.flatten(final_nodes_in_branch)))

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

                if len(parent_nodes) > 1:
                    branch_num += 1

                for parent in parent_nodes:
                    if break_flag or parent.method.name != "Break":
                        node.add_parent(parent)

                        parent.add_branch(branch_num)



            #Add the node to the node list
            try:
                self.nodes[branch_num].append(node)
            except IndexError:
                branches_to_insert = branch_num - (len(self.nodes) - 1)
                for i in range(0, branches_to_insert):
                    self.nodes.append([])
                self.nodes[branch_num].append(node)

            node.branch = branch_num
            node.index = len(self.nodes[branch_num]) - 1

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

    #Mouse move
    def handle_mouse(self, x, y):
        x_trans, y_trans = self.cam.translate(x, y)
        self.invis_node = None
        inside_node = False
        for branch in self.nodes:
            for node in branch:
                if node.hit(x_trans, y_trans):
                    inside_node = True
                    fields = self.parsed.get_fields_in_method(node.method)
                    self.data.highlight(fields)
                    break

        if not inside_node:
            obj = self.data.hit(x, y)
            if obj:
                inside_node = True
                self.invis_node = Node(MethodInvocation("InvisibleNode"), visible=False)
                self.invis_node.set_position(obj.x + self.cam.x, obj.y + self.cam.y)

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

    def enter_new_method(self, node, entering, in_animation = False):
        self.current = node

        if entering:
            self.stack.append(Frame(node, self.active_node.branch, self.active_node.index))
            if self.prev_index != 0:
                self.cur_index = self.prev_index
                self.prev_index = 0
            self.cur_branch = self.cur_branch_index = 0
        else:
            frame = self.stack.pop_to(node)
            self.cur_branch = frame.branch
            self.cur_branch_index = frame.index

            #If we're not in an animation, search through flow to find the first occurence of this method
            if not in_animation:
                self.cur_branch = self.cur_branch_index = 0


        self.data.add_params(node.method.parameters)

        self.place_nodes(in_animation)
        self.animation_path = []
        self.cam.set_pos(self.active_node.x, self.active_node.y)

        self.dot.place(self.active_node.x, self.active_node.y)

    #Mouse click
    def handle_input(self, x, y):
        x_trans, y_trans = self.cam.translate(x, y)
        for b_num, branch in enumerate(self.nodes):
            for index, node in enumerate(branch):
                if node.hit(x_trans, y_trans):
                    method = filter(lambda x: x.name == node.method.name, self.methods)
                    if len(method) > 0:
                        #Set up active node so that the proper branches can be pushed on the stack
                        self.active_node = self.nodes[b_num][index]
                        self.enter_new_method(Node(method[0]), True)
                    return

        node = self.stack.get_clicked_item(x, y)

        if node is not None:
            self.enter_new_method(node, False)
        else:
            self.dot.handle_input(x, y)