__author__ = 'twoods0129'
#!/usr/bin/env python2

import __builtin__ as builtin
import parser
import model as m
import subprocess
import shutil
import os
from os import walk
import cStringIO
import threading
import arrayUtils

def timeout(process):
    if process.poll is None:
        process.kill()

class Javap:

    def __init__(self, dir):
        p = parser.Parser()
        self.dir = dir
        self.files = {}
        #Get all files in dir
        for (dirpath, dirnames, filenames) in walk(self.dir):
            file_array = dirpath.split("/")
            if not "markup" in file_array:
                for file in filenames:
                    if file.endswith(".java"):
                        self.files[dirpath + "/" + file] = p.parse_file(dirpath + "/" + file)

        self.main = None
        self.methods = self.get_all_methods()
        self.objects = self.get_all_objects()

    def get_package_name(self):
        if self.tree.package_declaration is not None:
            return self.tree.package_declaration.name.value
        else:
            return None

    def list_attr(self):
        print(self.tree.__dict__.keys())

    def get_imports(self):
        imports = []
        for impt in self.tree.import_declarations:
            imports.append(impt.name.value)
        return imports

    def markup_file(self):
        #Make a markup directory inside the given directory if one doesnt exist
        if not os.path.exists(self.dir + "/markup"):
            os.makedirs(self.dir + "/markup")

        for file_string, parsed_data in self.files.iteritems():
            print("Marking up " + file_string)
            #Open the file and read in data
            file = open(file_string, "r")
            file.seek(0)
            file_data = file.readlines()

            #Add markup to the file path
            file_array = file_string.split("/")
            file_array.insert(1, "markup")
            markup_file_path = "/".join(file_array[0:len(file_array) - 1])

            #Verify the path to this file exists, create if it doesnt
            if not os.path.exists(markup_file_path):
                os.makedirs(markup_file_path)

            #Create new file within markup folder
            file = open("/".join(file_array), "w")

            file_data.insert(1, "import java.lang.Thread;\n")
            inserted_lines = 1
            #THIS WON'T WORK FOR INNER CLASSES
            class_name = file_array[-1].replace(".java", "")
            #Go through each method, mark when method is entered and every return statement
            for method in self.get_methods(parsed_data):
                #Once we find which file has main, store it
                if method.name == "main":
                    self.main = file

                returns = []
                if method.body is not None:
                    #If constructor calling super, need to put the print after super call
                    if builtin.type(method) is m.ConstructorDeclaration and builtin.type(method.body[0]) is m.ConstructorInvocation:
                        file_data.insert(method.line_num + inserted_lines + 1,
                                         'System.out.println("push ' + method.name + ' ' + class_name +
                                         ' " + Thread.currentThread().getId());\n')
                    else:
                        file_data.insert(method.line_num + inserted_lines,
                                         'System.out.println("push ' + method.name + ' ' + class_name +
                                         ' " + Thread.currentThread().getId());\n')

                    inserted_lines += 1

                    return_type = method.return_type
                    if builtin.type(return_type) is m.Type:
                        return_type = return_type.name.value

                    #The start of the method is considered branch 0 but never marked
                    branch_num = 1
                    #Find all returns in this method
                    for statement in method.body:
                        returns.append(statement.get_returns())

                    #Flatten the returns array and remove None entries
                    returns = filter(lambda x: x != None, arrayUtils.flatten(returns))

                    #Manually add a "return" if the last statement in the method isn't one, e.g a void method
                    if ((builtin.type(method) is m.ConstructorDeclaration) or (builtin.type(method) is m.MethodDeclaration))\
                            and builtin.type(method.body[-1]) is not m.Return:
                        returns.append(m.Throw("No return", method.end_line_num))


                    return_index = 0
                    previous_was_branch = False
                    #We need to insert all lines, branches and returns, in order, in one pass
                    for statement in method.body:
                        #If the statement is a branch it has branch_line_nums, an array of line numbers marking
                        # the start of each branch it produces
                        if m.is_visual_branch(statement):
                            previous_was_branch = True
                            for line in statement.branch_line_nums:
                                #Make sure we've put all returns which come before this line
                                while returns[return_index].line_num < line and return_index < len(returns) - 1:
                                    inserted_lines = self.add_return_print(file_data, returns[return_index], inserted_lines, return_type, method.name, class_name)
                                    return_index += 1

                                inserted_lines, branch_num = self.add_branch_print(file_data, line, inserted_lines, branch_num)

                        elif previous_was_branch:
                            previous_was_branch = False
                            inserted_lines, branch_num = self.add_branch_print(file_data, statement.line_num, inserted_lines, branch_num)

                    #Make sure we've printed every return
                    while return_index < len(returns):
                        inserted_lines = self.add_return_print(file_data, returns[return_index], inserted_lines, return_type, method.name, class_name)
                        return_index += 1

                    #If we had to manually insert a "return" we may have to manually insert the last branch
                    if ((builtin.type(method) is m.ConstructorDeclaration) or (builtin.type(method) is m.MethodDeclaration))\
                            and builtin.type(method.body[-1]) is not m.Return:
                        if m.is_visual_branch(method.body[-1]):
                            inserted_lines, branch_num = self.add_branch_print(file_data, method.end_line_num - 1, inserted_lines, branch_num)

            for line in file_data:
                file.write(line)

            file.close()

    def add_branch_print(self, file_data, line, inserted_lines, branch_num):
        #line numbers of -1 represent invisible nodes, don't have a print for them, but need to
        # increment branch_num
        if line > 0:
            #This handles ifs of the form
            #if (true)
            #{
            if file_data[line + inserted_lines].lstrip() == "{\n":
                line -= 1

            file_data.insert(line + inserted_lines,
                             'System.out.println("branch ' + str(branch_num) + '");\n')
            inserted_lines += 1
        branch_num += 1

        return inserted_lines, branch_num

    def add_return_print(self, file_data, ret, inserted_lines, return_type, method_name, class_name):
        #If this return is actually a return and not void
        if builtin.type(ret) is m.Return and return_type != "void":
            return_value = file_data[ret.line_num + inserted_lines].replace("return","",1).lstrip()
            file_data[ret.line_num + inserted_lines] = return_type + " __TEMP_VAR__ = " + return_value
            file_data.insert(ret.line_num + inserted_lines + 1,
                             'System.out.println("pop ' + method_name + ' ' + class_name +
                             ' " + Thread.currentThread().getId());\n')
            file_data.insert(ret.line_num + inserted_lines + 2, 'return __TEMP_VAR__;\n')
            inserted_lines += 2

        #Void return or a manually added "return"
        else:
            file_data.insert(ret.line_num + inserted_lines,
                             'System.out.println("pop ' + method_name + ' ' + class_name +
                             ' " + Thread.currentThread().getId());\n')
            inserted_lines += 1

        return inserted_lines

    def run_file(self, processing=False, timeout=None):
        #Split the file with main into directories and file name
        file_array = self.main.name.split("/")

        classpath = os.path.abspath(self.dir + "/markup")
        if processing:
            classpath += ":" + os.path.abspath(self.dir + "/core.jar")

        #Compile the files
        javac = subprocess.Popen("javac -cp " + classpath + " " + os.path.abspath(self.dir + "/markup/" + file_array[-1]),
                                 shell=True,
                                 stdout=subprocess.PIPE)


        errors = javac.communicate()[1]
        if errors:
            for line in cStringIO.StringIO(errors):
                print(line)

        #Run the file
        java = subprocess.Popen("java -cp " + classpath + " " + file_array[-1].replace(".java", ""),
          shell=True,
          stdout=subprocess.PIPE)

        if timeout:
            t = threading.Timer(timeout, timeout, [java])
            t.start()
            t.join()

        #Go through each line of output and add print statements to program_flow
        program_flow = []
        for line in cStringIO.StringIO(java.communicate()[0]):
            if "push" in line or "pop" in line or "branch" in line:
                program_flow.append(line.replace("\n", ""))

        if timeout:
            t.cancel()

        return program_flow

    def cleanup(self):
        print("Cleaning " + self.dir + "/markup")
        shutil.rmtree(self.dir + "/markup")

    def get_all_methods(self):
        methods = []
        for file_string, parsed_data in self.files.iteritems():
            methods.append(self.get_methods(parsed_data))

        return arrayUtils.flatten(methods)

    #Returns an array of all MethodDeclaration's found in parsed_data
    def get_methods(self, parsed_data, start_point = None):
        method_array = []

        if start_point is not None:
            tree = start_point
        else:
            tree = parsed_data.type_declarations

        for cls in tree:
            for element in cls.body:
                if builtin.type(element) is m.ClassDeclaration:
                    method_array += self.get_methods(parsed_data, [element])
                elif builtin.type(element) is m.MethodDeclaration:
                    method_array.append(element)
                elif builtin.type(element) is m.ConstructorDeclaration:
                    method_array.append(element)

        return method_array

    def get_method_declarations_and_invocations(self):

        array = self.get_methods()

        invocations = []
        #Search through methods, to find all occurrences of MethodInvocation
        for method in array:
            for statement in method.body:
                invocations.append(statement.get_method_invocations())

        #With all the appends, invocations is a multi dimensional list, flatten it
        invocations = arrayUtils.flatten(invocations)

        #For each method invocation, check if it is an invocation of a user defined method
        # if so, add it to the array
        for inv in invocations:
            if inv.name in map(lambda x: x.name, array) or inv.name == "main":
                array.append(inv)

        #Sort the array by line number
        array.sort(key=lambda x: x.line_num)
        return array

    def get_method_invocations_in_method(self, method):

        methods = self.methods
        invocations = []
        #Search through methods, to find all occurrences of MethodInvocation
        for statement in method.body:
            invocations.append(statement.get_method_invocations())

        #With all the appends, invocations is a multi dimensional list, flatten it
        invocations = arrayUtils.flatten(invocations)

        array = []
        #For each method invocation, check if it is an invocation of a user defined method
        # if so, add it to the array
        for inv in invocations:
            if inv.name in map(lambda x: x.name, methods) or inv.name == "main":
                array.append(inv)

        #User defined functions are contained in array in the order they appear in the code
        # create a nested array to represent code branches
        branch_array = [m.MethodInvocation("Start")]
        for statement in method.body:

            if type(statement) is m.For:
                print("For loop statement " + str(statement))

            methods_this_statement = statement.get_method_invocations()

            #Have to check predicate for method call here otherwise array structure gets ruined
            if m.is_branch(statement):
                method_in_pred = arrayUtils.flatten(statement.get_predicate().get_method_invocations())
                if len(method_in_pred) != 0:
                    branch_array.extend(method_in_pred)

            #if user_methods_this_statement != set():
            if type(statement) is m.IfThenElse or type(statement) is m.Try:
                branch_array.append(statement.get_method_invocations())
            else:
                branch_array.extend(methods_this_statement)

            if type(statement) is m.Return:
                branch_array.append(m.MethodInvocation("Return"))

        #Make sure we have a return at the end of the method
        try:
            if branch_array[-1].name != "Return":
                branch_array.append(m.MethodInvocation("Return"))
        except AttributeError, IndexError:
            branch_array.append(m.MethodInvocation("Return"))

        self.separate_subsequent_branches(branch_array)
        return branch_array


    #Check the array to ensure there is no situation with 2 subsequent branches with no method calls between them
    # if there are, add an invisible node between
    def separate_subsequent_branches(self, branch_array):
        if not hasattr(branch_array, '__iter__'):
            return branch_array

        for i in range(0, len(branch_array)):

            if hasattr(branch_array[i], "__iter__"):
                for el in branch_array[i]:
                    if hasattr(el, "__iter__"):
                        for branch in el:
                            if hasattr(branch, "__iter__"):
                                self.separate_subsequent_branches(branch)

                if i < len(branch_array) - 1 and hasattr(branch_array[i + 1], "__iter__"):
                    if hasattr(branch_array[i][0], "__iter__") and hasattr(branch_array[i + 1][0], "__iter__"):
                        branch_array.insert(i + 1, m.MethodInvocation("InvisibleNode"))

        return branch_array


    def get_all_objects(self):
        objs = []
        for file_string, parsed_data in self.files.iteritems():
            objs.append(self.get_objects(parsed_data))

        return arrayUtils.flatten(objs)

    #Returns an array of all MethodDeclaration's found in parsed_data
    def get_objects(self, parsed_data, start_point = None):
        obj_array = []

        if start_point is not None:
            tree = start_point
        else:
            tree = parsed_data.type_declarations

        for cls in tree:
            for element in cls.body:
                if builtin.type(element) is m.ClassDeclaration:
                    obj_array += self.get_objects(parsed_data, [element])
            obj_array.append(cls)


        return obj_array

    def get_object(self, param):
        #Store the type of the parameter
        if isinstance(param.type, basestring):
            cls = param.type
        elif isinstance(param.type.name, basestring):
            cls = param.type.name
        else:
            cls = param.type.name.value

        #Check if the parameter is an object
        for obj in self.objects:
            #Found the object
            if obj.name == cls:
                obj_fields = []

                for statement in obj.body:
                    if builtin.type(statement) is m.FieldDeclaration:
                        obj_fields.append(statement)
                return obj_fields

        #Parameter is not an object, it's a primative
        return []

    def get_fields_in_method(self, method):
        fields = []
        try:
            if method.target is not None:
                fields.append(method.target.value)

        #No target on InstanceCreation
        except AttributeError:
            pass

        for arg in method.arguments:
            a = arg.get_args()
            if not isinstance(a, basestring) and len(a) > 0:
                fields.extend(a)
            else:
                fields.append(a)

        return arrayUtils.flatten(fields)

    def get_method_metrics(self):
        return map(lambda method: method.metrics(), self.get_methods())

    def print_file(self, indentation = 0, start_point = None):
        if start_point is not None:
            tree = start_point
        else:
            tree = self.tree.type_declarations

        for cls in tree:
            class_string = ""
            class_string += " ".join([mod for mod in cls.modifiers])
            class_string += " class " + cls.name
            #Extends
            if cls.extends is not None:
                class_string += " extends " + str(cls.extends.name.value)

            #Implements
            if len(cls.implements) > 0:
                class_string += " implements " + ', '.join([type.name.value for type in cls.implements])

            class_string += " {"
            print(" " * indentation + class_string)

            #Class Body, made up of fields and methods
            #Could also be an inner class
            for element in cls.body:
                if builtin.type(element) is m.ClassDeclaration:
                    print("")
                    self.print_file(indentation + 3, [element])
                else:
                    element.log(indentation + 3)

            print(" " * indentation + "}")