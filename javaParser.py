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

def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

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

                    for statement in method.body:
                        returns.append(statement.get_returns())

                    #Flatten the returns array and remove None entries
                    returns = filter(lambda x: x != None, flatten(returns))

                    #THIS IS NOT A FINAL SOLUTION
                    if ((builtin.type(method) is m.ConstructorDeclaration) or (builtin.type(method) is m.MethodDeclaration)) and len(returns) == 0:
                        returns.append(m.Throw("No return", method.end_line_num))



                #For every return, remove the returned value, store it in temp variable
                # add print out, then return variable
                for ret in returns:
                    if builtin.type(ret) is m.Return and return_type != "void":
                        return_value = file_data[ret.line_num + inserted_lines].replace("return","",1).lstrip()
                        file_data[ret.line_num + inserted_lines] = return_type + " __TEMP_VAR__ = " + return_value
                        file_data.insert(ret.line_num + inserted_lines + 1,
                                         'System.out.println("pop ' + method.name + ' ' + class_name +
                                         ' " + Thread.currentThread().getId());\n')
                        file_data.insert(ret.line_num + inserted_lines + 2, 'return __TEMP_VAR__;\n')
                        inserted_lines += 2
                    else:
                        file_data.insert(ret.line_num + inserted_lines,
                                         'System.out.println("pop ' + method.name + ' ' + class_name +
                                         ' " + Thread.currentThread().getId());\n')
                        inserted_lines += 1

            for line in file_data:
                file.write(line)

            file.close()

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
            if "push" in line or "pop" in line:
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

        return flatten(methods)

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
        invocations = flatten(invocations)

        #For each method invocation, check if it is an invocation of a user defined method
        # if so, add it to the array
        for inv in invocations:
            if inv.name in map(lambda x: x.name, array) or inv.name == "main":
                array.append(inv)

        #Sort the array by line number
        array.sort(key=lambda x: x.line_num)
        return array

    def get_method_invocations_in_method(self, method):
        methods = self.get_all_methods()
        invocations = []
        #Search through methods, to find all occurrences of MethodInvocation
        for statement in method.body:
            invocations.append(statement.get_method_invocations())

        #With all the appends, invocations is a multi dimensional list, flatten it
        invocations = flatten(invocations)

        array = []
        #For each method invocation, check if it is an invocation of a user defined method
        # if so, add it to the array
        for inv in invocations:
            if inv.name in map(lambda x: x.name, methods) or inv.name == "main":
                array.append(inv)

        array = invocations
        #User defined functions are contained in array in the order they appear in the code
        # create a nested array to represent code branches
        branch_array = [m.MethodInvocation("Start")]
        for statement in method.body:
            methods_this_statement = flatten(statement.get_method_invocations())
            #Get the intersection between user defined method invocations and method invocations this statement
            # if its not empty add stuff to branch_array
            user_methods_this_statement = set(methods_this_statement) & set(array)
            if user_methods_this_statement != set():
                if type(statement) is m.IfThenElse or type(statement) is m.Try:
                    branch_array.append(statement.get_method_invocations_per_branch())
                else:
                    for method in user_methods_this_statement:
                        branch_array.append(method)

            if type(statement) is m.Return:
                branch_array.append(m.MethodInvocation("Return"))

        try:
            if branch_array[-1].name != "Return":
                branch_array.append(m.MethodInvocation("Return"))
        except AttributeError, IndexError:
            branch_array.append(m.MethodInvocation("Return"))

        return branch_array

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