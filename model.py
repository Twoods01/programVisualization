def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def is_nested(x):
    for el in x:
        if hasattr(el, "__iter__"):
            return True

    return False

def all_nested(x):
    for el in x:
        if not hasattr(el, "__iter__"):
            return False

    return True

#Place the elements of new into arr preserving proper nesting
def add_to_array_preserve_nesting(arr, new):
    #Check if there were any method calls this statement
    if len(new) > 0:

        #If method calls were nested, preserve nesting
        if is_nested(new):

            if all_nested(new):
                arr.append(new)

            else:
                for el in new:
                    if hasattr(el, "__iter__"):
                        arr.append(el)
                    else:
                        arr.extend([el])
        #No nesting, flatten everything and extend
        else:
            arr.extend(flatten(new))

def print_nested(nested_array):
        print(build_simple_array(nested_array))

def build_simple_array(nested_array):
    result = []
    for el in nested_array:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.append(build_simple_array(el))
        else:
            result.append(el.name)
    return result

# Base node
class SourceElement(object):
    '''
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.
    '''

    def __init__(self):
        super(SourceElement, self).__init__()
        self._fields = []

    def __repr__(self):
        equals = ("{0}={1!r}".format(k, getattr(self, k))
                  for k in self._fields)
        args = ", ".join(equals)
        return "{0}({1})".format(self.__class__.__name__, args)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

    def accept(self, visitor):
        pass

    def log(self, indentation):
        for line in self.to_string().splitlines():
            print(" " * indentation + line)


class CompilationUnit(SourceElement):

    def __init__(self, package_declaration=None, import_declarations=None,
                 type_declarations=None):
        super(CompilationUnit, self).__init__()
        self._fields = [
            'package_declaration', 'import_declarations', 'type_declarations']
        if import_declarations is None:
            import_declarations = []
        if type_declarations is None:
            type_declarations = []
        self.package_declaration = package_declaration
        self.import_declarations = import_declarations
        self.type_declarations = type_declarations

    def accept(self, visitor):
        if visitor.visit_CompilationUnit(self):
            if self.package_declaration:
                self.package_declaration.accept(visitor)
            for import_decl in self.import_declarations:
                import_decl.accept(visitor)
            for type_decl in self.type_declarations:
                type_decl.accept(visitor)


class PackageDeclaration(SourceElement):

    def __init__(self, name, modifiers=None):
        super(PackageDeclaration, self).__init__()
        self._fields = ['name', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.name = name
        self.modifiers = modifiers

    def accept(self, visitor):
        visitor.visit_PackageDeclaration(self)


class ImportDeclaration(SourceElement):

    def __init__(self, name, static=False, on_demand=False):
        super(ImportDeclaration, self).__init__()
        self._fields = ['name', 'static', 'on_demand']
        self.name = name
        self.static = static
        self.on_demand = on_demand

    def accept(self, visitor):
        visitor.visit_ImportDeclaration(self)


class ClassDeclaration(SourceElement):

    def __init__(self, name, body, modifiers=None, type_parameters=None,
                 extends=None, implements=None):
        super(ClassDeclaration, self).__init__()
        self._fields = ['name', 'body', 'modifiers',
                        'type_parameters', 'extends', 'implements']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if implements is None:
            implements = []
        self.name = name
        self.body = body
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements

    def accept(self, visitor):
        if visitor.visit_ClassDeclaration(self):
            for decl in self.body:
                decl.accept(visitor)


class ClassInitializer(SourceElement):

    def __init__(self, block, static=False):
        super(ClassInitializer, self).__init__()
        self._fields = ['block', 'static']
        self.block = block
        self.static = static

    def accept(self, visitor):
        if visitor.visit_ClassInitializer(self):
            for expr in self.block:
                expr.accept(visitor)


class ConstructorDeclaration(SourceElement):

    def __init__(self, name, block, modifiers=None, type_parameters=None,
                 parameters=None, throws=None, line_num=None):
        super(ConstructorDeclaration, self).__init__()
        self._fields = ['name', 'body', 'modifiers',
                        'type_parameters', 'parameters', 'throws', 'line_num', 'end_line_num']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        self.name = name
        self.body = block
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.throws = throws
        self.line_num = line_num
        try:
            self.end_line_num = self.body[-1].line_num
        except IndexError:
            self.end_line_num = line_num
        except AttributeError:
            print("Missing line num somewhere")
            self.end_line_num = self.line_num
        self.return_type = name

    def accept(self, visitor):
        if visitor.visit_ConstructorDeclaration(self):
            for expr in self.block:
                expr.accept(visitor)

    def to_string(self):
        string = " ".join([mod for mod in self.modifiers]) + " "
        string += self.name + "(" + ", ".join([param.to_string() for param in self.parameters]) + ") {\n"

        for statement in self.body:
            string += " " * 3 + statement.to_string() + ";\n"
        return string + "}"

class EmptyDeclaration(SourceElement):

    def accept(self, visitor):
        visitor.visit_EmptyDeclaration(self)

class FieldDeclaration(SourceElement):

    def __init__(self, type, variable_declarators, modifiers=None):
        super(FieldDeclaration, self).__init__()
        self._fields = ['type', 'variable_declarators', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = type
        self.variable_declarators = variable_declarators
        self.modifiers = modifiers

    def accept(self, visitor):
        visitor.visit_FieldDeclaration(self)

    def get_method_invocations(self):
        invocations = []
        for var in self.variable_declarators:
            invocations.extend(var.get_method_invocations())
        return invocations

    def get_returns(self):
        return None

    def to_string(self):
        string = ""

        for mod in self.modifiers:
            string += mod + " "

        #If the field is a non-primitive type have to add some dereferences
        if hasattr(self.type, "name"):
            string += self.type.name.value
        else:
            string += self.type

        #Not sure why this is stored as an array, but it is
        #Maybe for something like int a, b = 1 need to test that
        for var in self.variable_declarators:
            string += " " + var.variable.name

            #Check if the variable is initialized
            if var.initializer is not None:
                #If the initializer has a value attribute then use that
                string += " = "
                if type(var.initializer) is InstanceCreation:
                    string+= " new "
                string += var.initializer.to_string()

        return string + ";"

    def log(self, indentation):
        print(" " * indentation + self.to_string())


class MethodDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, type_parameters=None,
                 parameters=None, return_type='void', body=None, abstract=False,
                 extended_dims=0, throws=None, line_num=0):
        super(MethodDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'type_parameters', 'parameters',
                        'return_type', 'body', 'abstract', 'extended_dims',
                        'throws', 'line_num', 'end_line_num']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.abstract = abstract
        self.extended_dims = extended_dims
        self.throws = throws
        self.line_num = line_num
        if self.body:
            try:
                self.end_line_num = self.body[-1].line_num
            except AttributeError:
                print("No end line set")
                self.end_line_num = None
        else:
            self.end_line_num = None

    def accept(self, visitor):
        if visitor.visit_MethodDeclaration(self):
            if self.body is not None:
                for e in self.body:
                    e.accept(visitor)


    def metrics(self):
        hash = {}
        hash["string"] = self.name
        hash["line"] = self.line_num

        count_hash = {}
        for statement in self.body:
            if type(statement) in count_hash:
                count_hash[type(statement)] += 1
            else:
                count_hash[type(statement)] = 1

        metrics_hash = {}
        metrics_hash["Parameter"] = len(self.parameters)
        for key, count in count_hash.iteritems():
            metrics_hash[str(key.__name__)] = count

        hash["metrics"] = metrics_hash
        return hash

    def get_methods(self):
        methods = []
        for statement in self.body:
            if type(statement) is MethodInvocation:
                methods.append(statement)

        return methods

    def to_string(self):
        string = ""
        for mod in self.modifiers:
            if type(mod) is str:
                string += mod + " "
            else:
                string += mod.name.value + " "

        if type(self.return_type) is str:
            string += self.return_type + " "
        else:
            string += self.return_type.name.value + " "
        string += self.name + "("

        #For each parameter append the param type and name
        if len(self.parameters) is not 0:
            for param in self.parameters:
                if hasattr(param.type, "name"):
                    string += param.type.name.value + " "
                else:
                    string += param.type + " "

                string += param.variable.name + ", "

            #Strip the last ", " from the string
            string = string[:-2]

        return string + ")"

    def log(self, indentation):
        string = self.to_string() + " {"
        print(" " * indentation + string)

        if self.body is not None:
            for statement in self.body:
               statement.log(indentation + 3)

        print(" " * indentation + "}")



class FormalParameter(SourceElement):

    def __init__(self, variable, type, modifiers=None, vararg=False):
        super(FormalParameter, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'vararg']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = type
        self.modifiers = modifiers
        self.vararg = vararg

    def to_string(self):
        return self.type.to_string() + " " + self.variable.to_string()


class Variable(SourceElement):
    # I would like to remove this class. In theory, the dimension could be added
    # to the type but this means variable declarations have to be changed
    # somehow. Consider 'int i, j[];'. In this case there currently is only one
    # type with two variable declarators;This closely resembles the source code.
    # If the variable is to go away, the type has to be duplicated for every
    # variable...

    def __init__(self, name, dimensions=0):
        super(Variable, self).__init__()
        self._fields = ['name', 'dimensions']
        self.name = name
        self.dimensions = dimensions

    def to_string(self):
        return self.name


class VariableDeclarator(SourceElement):

    def __init__(self, variable, initializer=None):
        super(VariableDeclarator, self).__init__()
        self._fields = ['variable', 'initializer']
        self.variable = variable
        self.initializer = initializer

    def get_method_invocations(self):
        inv = []
        if self.initializer is not None:
            inv.extend(self.initializer.get_method_invocations())
        return inv

    def get_returns(self):
        return None


class Throws(SourceElement):

    def __init__(self, types):
        super(Throws, self).__init__()
        self._fields = ['types']
        self.types = types


class InterfaceDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, extends=None, type_parameters=None,
                 body=None):
        super(InterfaceDeclaration, self).__init__()
        self._fields = [
            'name', 'modifiers', 'extends', 'type_parameters', 'body']
        if modifiers is None:
            modifiers = []
        if extends is None:
            extends = []
        if type_parameters is None:
            type_parameters = []
        if body is None:
            body = []
        self.name = name
        self.modifiers = modifiers
        self.extends = extends
        self.type_parameters = type_parameters
        self.body = body

    def accept(self, visitor):
        if visitor.visit_InterfaceDeclaration(self):
            for decl in self.body:
                decl.accept(visitor)


class EnumDeclaration(SourceElement):

    def __init__(self, name, implements=None, modifiers=None,
                 type_parameters=None, body=None):
        super(EnumDeclaration, self).__init__()
        self._fields = [
            'name', 'implements', 'modifiers', 'type_parameters', 'body']
        if implements is None:
            implements = []
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if body is None:
            body = []
        self.name = name
        self.implements = implements
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.body = body

    def accept(self, visitor):
        if visitor.visit_EnumDeclaration(self):
            for decl in self.body:
                decl.accept(visitor)


class EnumConstant(SourceElement):

    def __init__(self, name, arguments=None, modifiers=None, body=None):
        super(EnumConstant, self).__init__()
        self._fields = ['name', 'arguments', 'modifiers', 'body']
        if arguments is None:
            arguments = []
        if modifiers is None:
            modifiers = []
        if body is None:
            body = []
        self.name = name
        self.arguments = arguments
        self.modifiers = modifiers
        self.body = body

    def accept(self, visitor):
        if visitor.visit_EnumConstant(self):
            for expr in self.body:
                expr.accept(visitor)


class AnnotationDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, type_parameters=None, extends=None,
                 implements=None, body=None):
        super(AnnotationDeclaration, self).__init__()
        self._fields = [
            'name', 'modifiers', 'type_parameters', 'extends', 'implements',
            'body']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if implements is None:
            implements = []
        if body is None:
            body = []
        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements
        self.body = body

    def accept(self, visitor):
        if visitor.visit_AnnotationDeclaration(self):
            for decl in self.body:
                decl.accept(visitor)


class AnnotationMethodDeclaration(SourceElement):

    def __init__(self, name, type, parameters=None, default=None,
                 modifiers=None, type_parameters=None, extended_dims=0):
        super(AnnotationMethodDeclaration, self).__init__()
        self._fields = ['name', 'type', 'parameters', 'default',
                        'modifiers', 'type_parameters', 'extended_dims']
        if parameters is None:
            parameters = []
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        self.name = name
        self.type = type
        self.parameters = parameters
        self.default = default
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extended_dims = extended_dims

    def accept(self, visitor):
        visitor.visit_AnnotationMethodDeclaration(self)


class Annotation(SourceElement):

    def __init__(self, name, members=None, single_member=None):
        super(Annotation, self).__init__()
        self._fields = ['name', 'members', 'single_member']
        if members is None:
            members = []
        self.name = name
        self.members = members
        self.single_member = single_member


class AnnotationMember(SourceElement):

    def __init__(self, name, value):
        super(SourceElement, self).__init__()
        self._fields = ['name', 'value']
        self.name = name
        self.value = value


class Type(SourceElement):

    def __init__(self, name, type_arguments=None, enclosed_in=None,
                 dimensions=0):
        super(Type, self).__init__()
        self._fields = ['name', 'type_arguments', 'enclosed_in', 'dimensions']
        if type_arguments is None:
            type_arguments = []
        self.name = name
        self.type_arguments = type_arguments
        self.enclosed_in = enclosed_in
        self.dimensions = dimensions

    def to_string(self):
        return self.name.to_string()


class Wildcard(SourceElement):

    def __init__(self, bounds=None):
        super(Wildcard, self).__init__()
        self._fields = ['bounds']
        if bounds is None:
            bounds = []
        self.bounds = bounds


class WildcardBound(SourceElement):

    def __init__(self, type, extends=False, _super=False):
        super(WildcardBound, self).__init__()
        self._fields = ['type', 'extends', '_super']
        self.type = type
        self.extends = extends
        self._super = _super


class TypeParameter(SourceElement):

    def __init__(self, name, extends=None):
        super(TypeParameter, self).__init__()
        self._fields = ['name', 'extends']
        if extends is None:
            extends = []
        self.name = name
        self.extends = extends


class Expression(SourceElement):

    def __init__(self):
        super(Expression, self).__init__()
        self._fields = []

    def accept(self, visitor):
        visitor.visit_Expression(self)


class BinaryExpression(Expression):

    def __init__(self, operator, lhs, rhs, line_num):
        super(BinaryExpression, self).__init__()
        self._fields = ['operator', 'lhs', 'rhs']
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs
        self.line_num = line_num

    def accept(self, visitor):
        if visitor.visit_BinaryExpression(self):
            if type(self.lhs) is not str:
                self.lhs.accept(visitor)
            if type(self.rhs) is not str:
                self.rhs.accept(visitor)

    def to_string(self):
        return self.lhs.to_string() + " " + self.operator + " " + self.rhs.to_string()

    def get_method_invocations(self):
        invocations = []
        if not isinstance(self.lhs, basestring):
            invocations.extend(self.lhs.get_method_invocations())
        if not isinstance(self.rhs, basestring):
            invocations.extend(self.rhs.get_method_invocations())
        return invocations

    def get_returns(self):
        return None

class Assignment(BinaryExpression):
    def to_string(self):
        return self.lhs.to_string() + " " + self.operator + " " + self.rhs.to_string()


class Conditional(Expression):

    def __init__(self, predicate, if_true, if_false):
        super(self.__class__, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false


class ConditionalOr(BinaryExpression):
    pass


class ConditionalAnd(BinaryExpression):
    pass


class Or(BinaryExpression):
    pass


class Xor(BinaryExpression):
    pass


class And(BinaryExpression):
    pass


class Equality(BinaryExpression):
    pass

class InstanceOf(BinaryExpression):
    pass


class Relational(BinaryExpression):
    pass


class Shift(BinaryExpression):
    pass


class Additive(BinaryExpression):
    pass


class Multiplicative(BinaryExpression):
    pass


class Unary(Expression):

    def __init__(self, sign, expression):
        super(Unary, self).__init__()
        self._fields = ['sign', 'expression']
        self.sign = sign
        self.expression = expression

    def to_string(self):
        #I need to look into other possibilities here
        if self.sign == "x++":
            return self.expression.to_string() + self.sign[1:]
        else:
            return self.sign + self.expression.to_string()

    def get_method_invocations(self):
        return(self.expression.get_method_invocations())

    def get_returns(self):
        return None


class Cast(Expression):

    def __init__(self, target, expression):
        super(Cast, self).__init__()
        self._fields = ['target', 'expression']
        self.target = target
        self.expression = expression

    def to_string(self):
        return "(" + self.target.to_string() + ")" + self.expression.to_string()

    def get_method_invocations(self):
        return []


class Statement(SourceElement):
    pass

class Empty(Statement):
    def get_method_invocations(self):
        return []


class Block(Statement):

    def __init__(self, statements=None, line_num=None):
        super(Statement, self).__init__()
        self._fields = ['statements']
        if statements is None:
            statements = []
        self.statements = statements
        self.line_num = line_num

    def __iter__(self):
        for s in self.statements:
            yield s

    def accept(self, visitor):
        if visitor.visit_Block(self):
            [s.accept(visitor) for s in self.statements]

    def to_string(self):
        string = ""
        for statement in self.statements:
            string += " " * 3 + statement.to_string() + ";\n"
        return string

    def get_returns(self):
        returns = []
        for statement in self.statements:
            returns.append(statement.get_returns())

        return returns


class VariableDeclaration(Statement, FieldDeclaration):
    def accept(self, visitor):
        visitor.visit_VariableDeclaration(self)


class ArrayInitializer(SourceElement):
    def __init__(self, elements=None):
        super(ArrayInitializer, self).__init__()
        self._fields = ['elements']
        if elements is None:
            elements = []
        self.elements = elements


class MethodInvocation(Expression):
    def __init__(self, name, arguments=None, type_arguments=None, target=None, line_num=0):
        super(MethodInvocation, self).__init__()
        self._fields = ['name', 'arguments', 'type_arguments', 'target']
        if arguments is None:
            arguments = []
        if type_arguments is None:
            type_arguments = []
        self.name = name
        self.arguments = arguments
        self.type_arguments = type_arguments
        self.target = target
        self.line_num = line_num

    def get_method_invocations(self):
        invocations = []
        for arg in self.arguments:
            invocations.extend(arg.get_method_invocations())
        invocations.extend([self])
        return invocations

    def get_returns(self):
        return None

    def accept(self, visitor):
        visitor.visit_MethodInvocation(self)

    def to_string(self):
        string = ""
        if self.target is not None:
            #Super is stored as just a string
            if type(self.target) is str:
                string = self.target + "."
            else:
                string += self.target.to_string() + "."
        string += self.name + "("
        return string + ", ".join([arg if type(arg) is str else arg.to_string() for arg in self.arguments]) + ")"


class IfThenElse(Statement):

    def __init__(self, predicate, if_true=None, if_false=None, line_num=None):
        super(IfThenElse, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false
        self.line_num = line_num

    def accept(self, visitor):
        if visitor.visit_IfThenElse(self):
            self.predicate.accept(visitor)
            self.if_true.accept(visitor)
            if self.if_false is not None:
                self.if_false.accept(visitor)


    def get_method_invocations(self):
        array = []
        block = []
        if type(self.if_true) is Block:
            for statement in self.if_true:

                if type(statement) is IfThenElse:
                    method_in_pred = flatten(statement.predicate.get_method_invocations())
                    if len(method_in_pred) != 0:
                        block.extend(method_in_pred)
                    elif len(block) == 0:
                        block.append(MethodInvocation("InvisibleNode"))

                    invs = statement.get_method_invocations()
                    add_to_array_preserve_nesting(block, invs)

                elif type(statement) is Return:
                    block.append(MethodInvocation("Return"))
                else:
                    add_to_array_preserve_nesting(block, statement.get_method_invocations())

            if len(block) > 0:
                array.append(block)
            else:
                array.append([MethodInvocation("InvisibleNode")])

        else:
            if type(self.if_true) is Return:
                array.append([MethodInvocation("Return")])
            else:
                invs = self.if_true.get_method_invocations()
                if len(invs) > 0:
                    array.append(invs)
                else:
                    array.append([MethodInvocation("InvisibleNode")])

        block = []
        if type(self.if_false) is IfThenElse:
            method_in_pred = flatten(self.if_false.predicate.get_method_invocations())
            if len(method_in_pred) != 0:
                block.extend(method_in_pred)
            else:
                block.append(MethodInvocation("InvisibleNode"))

            if len(block) > 0:
                array.append(block)
            else:
                array.append([MethodInvocation("InvisibleNode")])

            add_to_array_preserve_nesting(block, self.if_false.get_method_invocations())

        elif type(self.if_false) is Block:
            for statement in self.if_false:
                print(statement)
                if type(statement) is IfThenElse:
                    method_in_pred = flatten(statement.predicate.get_method_invocations())
                    print("False preds " + str(method_in_pred))
                    if len(method_in_pred) != 0:
                        block.extend(method_in_pred)
                    elif len(block) == 0:
                        block.append(MethodInvocation("InvisibleNode"))
                    add_to_array_preserve_nesting(block, statement.get_method_invocations())

                elif type(statement) is Return:
                    block.append(MethodInvocation("Return"))
                else:
                    add_to_array_preserve_nesting(block, statement.get_method_invocations())


            if len(block) > 0:
                array.append(block)
            else:
                array.append([MethodInvocation("InvisibleNode")])

        elif self.if_false is None:
            if len(array) > 0:
                array.append([MethodInvocation("InvisibleNode")])
        else:
            #add_to_array_preserve_nesting(array, self.if_false.get_method_invocations())
            invs = self.if_false.get_method_invocations()
            if len(invs) > 0:
                array.append(invs)
            else:
                array.append([MethodInvocation("InvisibleNode")])

        return array

    def get_returns(self):
        returns = []

        if type(self.if_true) is Block:
            for statement in self.if_true:
                returns.append(statement.get_returns())
        else:
            returns.append(self.if_true.get_returns())

        if type(self.if_false) is Block:
            for statement in self.if_false:
                returns.append(statement.get_returns())
        elif self.if_false is not None:
            returns.append(self.if_false.get_returns())

        return returns

    def to_string(self):
        string = "if (" + self.predicate.to_string() + ") {\n"
        if type(self.if_true) is Block:
            string += self.if_true.to_string()
        else:
            string += " " * 3 + self.if_true.to_string() + "\n"
        string += "}"
        return string


class While(Statement):

    def __init__(self, predicate, body=None, line_num=None):
        super(While, self).__init__()
        self._fields = ['predicate', 'body']
        self.predicate = predicate
        self.body = body
        self.line_num = line_num

    def accept(self, visitor):
        visitor.visit_While(self)

    def get_returns(self):
        returns = []
        for statement in self.body:
            returns.append(statement.get_returns())

        return returns

    def get_method_invocations(self):
        invocations = [MethodInvocation("loopStart")]

        inside_loop = []
        inv_in_pred = flatten(self.predicate.get_method_invocations())
        if len(inv_in_pred) != 0:
            inside_loop.extend(inv_in_pred)

        if type(self.body) is Block:
            for statement in self.body:
                inv = statement.get_method_invocations()

                #Have to check predicate for method call here otherwise array structure gets ruined
                if type(statement) is IfThenElse:
                    method_in_pred = flatten(statement.predicate.get_method_invocations())
                    if len(method_in_pred) != 0:
                        inside_loop.extend(method_in_pred)

                add_to_array_preserve_nesting(inside_loop, inv)
        else:
            #Have to check predicate for method call here otherwise array structure gets ruined
            if type(self.body) is IfThenElse:
                method_in_pred = flatten(self.body.predicate.get_method_invocations())
                if len(method_in_pred) != 0:
                    inside_loop.extend(method_in_pred)

            #inside_loop.extend(self.body.get_method_invocations())
            add_to_array_preserve_nesting(inside_loop, self.body.get_method_invocations())


        invocations.append([[MethodInvocation("InvisibleNode")], inside_loop])
        invocations.append(MethodInvocation("repeat"))
        invocations.append(MethodInvocation("loopEnd"))

        return invocations


class For(Statement):

    def __init__(self, init, predicate, update, body, line_num):
        super(For, self).__init__()
        self._fields = ['init', 'predicate', 'update', 'body']
        self.init = init
        self.predicate = predicate
        self.update = update
        self.body = body
        self.line_num = line_num

    def accept(self, visitor):
        if visitor.visit_For(self):
            self.body.accept(visitor)

    def to_string(self):
        string = "for (" + self.init.to_string() + "; " + self.predicate.to_string() + ";"
        for update in self.update:
            string += " " + update.to_string()
        string += ") {\n"
        string += self.body.to_string()

        return string + "}"

    def get_method_invocations(self):
        invocations = [MethodInvocation("loopStart")]

        inside_loop = []
        inside_loop.extend(self.init.get_method_invocations())
        inside_loop.extend(self.predicate.get_method_invocations())
        for update in self.update:
            inside_loop.extend(update.get_method_invocations())

        if type(self.body) is Block:
            for statement in self.body:
                inv = statement.get_method_invocations()

                #Have to check predicate for method call here otherwise array structure gets ruined
                if type(statement) is IfThenElse:
                    method_in_pred = flatten(statement.predicate.get_method_invocations())
                    if len(method_in_pred) != 0:
                        inside_loop.extend(method_in_pred)

                add_to_array_preserve_nesting(inside_loop, inv)
        else:
            #Have to check predicate for method call here otherwise array structure gets ruined
            if type(self.body) is IfThenElse:
                method_in_pred = flatten(self.body.predicate.get_method_invocations())
                if len(method_in_pred) != 0:
                    inside_loop.extend(method_in_pred)

            #inside_loop.extend(self.body.get_method_invocations())
            add_to_array_preserve_nesting(inside_loop, self.body.get_method_invocations())

        invocations.append([[MethodInvocation("InvisibleNode")], inside_loop])
        invocations.append(MethodInvocation("repeat"))
        invocations.append(MethodInvocation("loopEnd"))
        return invocations

    def get_returns(self):
        returns = []
        for statement in self.body:
            returns.append(statement.get_returns())

        return returns

class ForEach(Statement):

    def __init__(self, type, variable, iterable, body, modifiers=None):
        super(ForEach, self).__init__()
        self._fields = ['type', 'variable', 'iterable', 'body', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = type
        self.variable = variable
        self.iterable = iterable
        self.body = body
        self.modifiers = modifiers

    def accept(self, visitor):
        if visitor.visit_ForEach(self):
            self.body.accept(visitor)

    def get_returns(self):
        returns = []
        for statement in self.body:
            returns.append(statement.get_returns())

        return returns


class Assert(Statement):

    def __init__(self, predicate, message=None):
        super(Assert, self).__init__()
        self._fields = ['predicate', 'message']
        self.predicate = predicate
        self.message = message

    def accept(self, visitor):
        visitor.visit_Assert(self)


class Switch(Statement):

    def __init__(self, expression, switch_cases):
        super(Switch, self).__init__()
        self._fields = ['expression', 'switch_cases']
        self.expression = expression
        self.switch_cases = switch_cases

    def accept(self, visitor):
        if visitor.visit_Switch(self):
            for s in self.switch_cases:
                s.accept(visitor)

    def to_string(self):
        string = "switch(" + self.expression.to_string() + ") {\n"
        for case in self.switch_cases:
            string += case.to_string()
        return string + "}"

    def get_returns(self):
        returns = []
        for case in self.switch_cases:
            returns.append(case.get_returns())

        return returns


class SwitchCase(SourceElement):

    def __init__(self, cases, body=None):
        super(SwitchCase, self).__init__()
        self._fields = ['cases', 'body']
        if body is None:
            body = []
        self.cases = cases
        self.body = body

    def accept(self, visitor):
        if visitor.visit_SwitchCase(self):
            for s in self.body:
                s.accept(visitor)

    def to_string(self):
        if(self.cases[0] == "default"):
            string = " " * 3 + "default:\n"
        else:
            string = " " * 3 + "case " + ", ".join(case.to_string() for case in self.cases) + ":\n"

        for statement in self.body:
            string += " " * 6 + statement.to_string()

        return string + "\n"

    def get_returns(self):
        returns = []
        for statement in self.body:
            returns.append(statement.get_returns())

        return returns


class DoWhile(Statement):

    def __init__(self, predicate, body=None):
        super(DoWhile, self).__init__()
        self._fields = ['predicate', 'body']
        self.predicate = predicate
        self.body = body

    def accept(self, visitor):
        if visitor.visit_DoWhile(self):
            self.body.accept(visitor)


class Continue(Statement):

    def __init__(self, label=None):
        super(Continue, self).__init__()
        self._fields = ['label']
        self.label = label

    def accept(self, visitor):
        visitor.visit_Continue(self)


class Break(Statement):

    def __init__(self, label=None):
        super(Break, self).__init__()
        self._fields = ['label']
        self.label = label

    def accept(self, visitor):
        visitor.visit_Break(self)

    def get_returns(self):
        return None

    def get_method_invocations(self):
        return [MethodInvocation("Break")]


class Return(Statement):

    def __init__(self, result=None, line_num=None):
        super(Return, self).__init__()
        self._fields = ['result', 'line_num']
        self.result = result
        self.line_num = line_num

    def accept(self, visitor):
        visitor.visit_Return(self)

    def get_method_invocations(self):
        if self.result is not None:
            return self.result.get_method_invocations()
        return []

    def get_returns(self):
        return self

    def to_string(self):
        if type(self.result) is str:
            return "return " + self.result + ";"
        else:
            return "return " + self.result.to_string() + ";"


class Synchronized(Statement):

    def __init__(self, monitor, body):
        super(Synchronized, self).__init__()
        self._fields = ['monitor', 'body']
        self.monitor = monitor
        self.body = body

    def accept(self, visitor):
        if visitor.visit_Synchronized(self):
            for s in self.body:
                s.accept(visitor)


class Throw(Statement):

    def __init__(self, exception, line_num=None):
        super(Throw, self).__init__()
        self._fields = ['exception']
        self.exception = exception
        self.line_num = line_num

    def accept(self, visitor):
        visitor.visit_Throw(self)

    def to_string(self):
        return "throw new " + self.exception.to_string() + ";"

    #Not sure about this
    def get_returns(self):
        return self

class Try(Statement):

    def __init__(self, block, catches=None, _finally=None, resources=None):
        super(Try, self).__init__()
        self._fields = ['block', 'catches', '_finally', 'resources']
        if catches is None:
            catches = []
        if resources is None:
            resources = []
        self.block = block
        self.catches = catches
        self._finally = _finally
        self.resources = resources

    def accept(self, visitor):
        if visitor.visit_Try(self):
            for s in self.block:
                s.accept(visitor)
        for c in self.catches:
            visitor.visit_Catch(c)
        if self._finally:
            self._finally.accept(visitor)

    def get_returns(self):
        returns = []
        for statement in self.block:
            returns.append(statement.get_returns())

        if self._finally:
            for statement in self._finally:
                returns.append(statement.get_returns())

        return returns

    def get_method_invocations(self):
        array = []
        block = []

        for statement in self.block:
            invs = statement.get_method_invocations()

            for inv in invs:
                if hasattr(inv, "__iter__"):
                    block.append(inv)
                else:
                    block.extend([inv])

        array.append(block)

        block = []

        for statement in self.catches:
            methods_in_statement = flatten(statement.get_method_invocations())
            if len(methods_in_statement) > 0:
                block.extend(methods_in_statement)

        if len(block) > 0:
            array.append(block)
        else:
            array.append([MethodInvocation("InvisibleNode")])

        return array


    def to_string(self):
        string = "try {\n"
        string += self.block.to_string() + "\n"

        for catch in self.catches:
            string += "} " + catch.to_string()
        return string + "}"

class Catch(SourceElement):

    def __init__(self, variable, modifiers=None, types=None, block=None):
        super(Catch, self).__init__()
        self._fields = ['variable', 'modifiers', 'types', 'block']
        if modifiers is None:
            modifiers = []
        if types is None:
            types = []
        self.variable = variable
        self.modifiers = modifiers
        self.types = types
        self.block = block

    def accept(self, visitor):
        if visitor.visit_Catch(self):
            self.block.accept(visitor)

    def get_method_invocations(self):
        inv = []
        for statment in self.block:
            inv.extend(statment.get_method_invocations())
        return inv

    def get_returns(self):
        returns = []
        for statement in self.block:
            returns.append(statement.get_returns())

        return returns

    def to_string(self):
        string = "catch(" + " ".join([t.to_string() for t in self.types])
        string += " " + self.variable.to_string() + ") {\n"
        return string + self.block.to_string()


class Resource(SourceElement):

    def __init__(self, variable, type=None, modifiers=None, initializer=None):
        super(Resource, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'initializer']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = type
        self.modifiers = modifiers
        self.initializer = initializer


class ConstructorInvocation(Statement):
    """An explicit invocations of a class's constructor.

    This is a variant of either this() or super(), NOT a "new" expression.
    """

    def __init__(self, name, target=None, type_arguments=None, arguments=None):
        super(ConstructorInvocation, self).__init__()
        self._fields = ['name', 'target', 'type_arguments', 'arguments']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        self.name = name
        self.target = target
        self.type_arguments = type_arguments
        self.arguments = arguments

    def accept(self, visitor):
        visitor.visit_ConstructorInvocation(self)

    def to_string(self):
        string = ""
        if self.target is not None:
            string += self.target.to_string + "."
        string += self.name + "(" + ", ".join([arg.to_string() for arg in self.arguments]) + ")"

        return string

    def get_returns(self):
        return None

class InstanceCreation(Expression):

    def __init__(self, type, type_arguments=None, arguments=None, body=None,
                 enclosed_in=None):
        super(InstanceCreation, self).__init__()
        self._fields = [
            'type', 'type_arguments', 'arguments', 'body', 'enclosed_in']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        if body is None:
            body = []
        self.type = type
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.body = body
        self.enclosed_in = enclosed_in

    def accept(self, visitor):
        visitor.visit_InstanceCreation(self)

    def to_string(self):
        string = self.type.to_string() + "("
        string += ", ".join([arg if type(arg) is str else arg.to_string() for arg in self.arguments]) + ")"
        return string

    def get_method_invocations(self):
        inv =  [MethodInvocation(self.type.name.value)]
        if self.arguments is not None:
            for arg in self.arguments:
                inv.extend(arg.get_method_invocations())
        return inv


class FieldAccess(Expression):

    def __init__(self, name, target):
        super(FieldAccess, self).__init__()
        self._fields = ['name', 'target']
        self.name = name
        self.target = target

    def accept(self, visitor):
        visitor.visit_FieldAccess(self)

    def get_method_invocations(self):
        return []


class ArrayAccess(Expression):

    def __init__(self, index, target):
        super(ArrayAccess, self).__init__()
        self._fields = ['index', 'target']
        self.index = index
        self.target = target

    def accept(self, visitor):
        visitor.visit_ArrayAccess(self)

    def get_method_invocations(self):
        return self.index.get_method_invocations()


class ArrayCreation(Expression):

    def __init__(self, type, dimensions=None, initializer=None):
        super(ArrayCreation, self).__init__()
        self._fields = ['type', 'dimensions', 'initializer']
        if dimensions is None:
            dimensions = []
        self.type = type
        self.dimensions = dimensions
        self.initializer = initializer

    def get_method_invocations(self):
        inv = []
        if self.initializer is not None:
            inv.extend(self.initializer.get_method_invocations())
        return inv

    def accept(self, visitor):
        visitor.visit_ArrayCreation(self)


class Literal(SourceElement):

    def __init__(self, value):
        super(Literal, self).__init__()
        self._fields = ['value']
        self.value = value

    def get_method_invocations(self):
        return []

    def get_returns(self):
        return None

    def accept(self, visitor):
        visitor.visit_Literal(self)

    def to_string(self):
        return self.value


class ClassLiteral(SourceElement):

    def __init__(self, type):
        super(ClassLiteral, self).__init__()
        self._fields = ['type']
        self.type = type

    def to_string(self):
        return self.type.to_string() + ".class"


class Name(SourceElement):

    def __init__(self, value):
        super(Name, self).__init__()
        self._fields = ['value']
        self.value = value

    def append_name(self, name):
        try:
            self.value = self.value + '.' + name.value
        except:
            self.value = self.value + '.' + name

    def accept(self, visitor):
        visitor.visit_Name(self)

    def to_string(self):
        return self.value

    def get_method_invocations(self):
        return []

    def get_returns(self):
        return None


class Visitor(object):

    def __init__(self, verbose=False):
        self.verbose = verbose

    def __getattr__(self, name):
        if not name.startswith('visit_'):
            raise AttributeError('name must start with visit_ but was {}'
                                 .format(name))

        def f(element):
            if self.verbose:
                msg = 'unimplemented call to {}; ignoring ({})'
                print(msg.format(name, element))
            return True
        return f
