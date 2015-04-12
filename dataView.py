__author__ = 'twoods0129'
from model import FieldDeclaration
import pyglet

class DataView():
    initial_x = 75
    initial_y = 80
    max_nodes_in_row = 7
    x_increment = 125

    def __init__(self, parsed):
        self.objects = []
        self.parsed = parsed

    def draw(self):
        for obj in self.objects:
            obj.draw()

    def add_params(self, params):
        self.objects = []
        for param in params:
            field_array = self.parsed.get_object(param)
            x = DataView.initial_x + ((len(self.objects) % DataView.max_nodes_in_row) * DataView.x_increment)
            y = DataView.initial_y - ((len(self.objects) / DataView.max_nodes_in_row) * 100)
            self.objects.append(self.Object(param, field_array, x, y))

        print("There are " + str(len(self.objects)) + " data objects in this method")

    #Given an x, y in pixel space returns a data object that x,y position is inside of, or False if it didnt hit a
    # data object
    def hit(self, x, y):
        for obj in self.objects:
            if obj.hit(x, y):
                return obj

        return False


    def highlight(self, fields):
        for field in fields:
            for obj in self.objects:
                #Highlight this field in this object if it exists
                if obj.highlight(field):
                    field_highlighted = True

        return

    def clear_highlights(self):
        for obj in self.objects:
            obj.clear_highlights()

    def write(self):
        for obj in self.objects:
            obj.write()

    class Object():
        width = 114
        height = 50
        node_vertices = pyglet.graphics.vertex_list_indexed(4,
                                    [0, 1, 2, 0, 2, 3],
                                    ('v3i', (-57, -25, 0,
                                            57, -25, 0,
                                            57, 25, 0,
                                            -57, 25, 0)),
                                    ('c3B', (115, 83, 140) * 4))

        def __init__(self, param, field_array, x, y):
            self.x = x
            self.y = y
            self.var = self.Variable(param)
            self.highlighted = False
            self.members = []
            for el in field_array:
                self.members.append(self.Variable(el))

        def write(self):
            print(str(self.var) + " has fields: ")
            for field in self.members:
                print("\t" + str(field))
            print("")

        def hit(self, x, y):
            cur_height = self.height * (1 + 0.2 * len(self.members))
            return x > self.x  - (self.width / 2)  and x < self.x + self.width - (self.width / 2)\
               and y > self.y  - (cur_height / 2) and y < self.y + cur_height - (cur_height / 2)

        def highlight(self, field):
            self.highlighted = (self.var.name == field)

            for mem in self.members:
                mem.highlighted = (mem.name == field)

            return

        def includes(self, field):
            return (self.var.name == field) or any(map(lambda x: x == field, self.members))

        def clear_highlights(self):
            self.highlighted = False

            for mem in self.members:
                mem.highlighted = False

            return

        def draw(self):
            pyglet.gl.glPushMatrix()
            pyglet.gl.glPushMatrix()
            y_offset = -10 * len(self.members)
            pyglet.gl.glTranslatef(self.x, self.y + y_offset, 0)
            obj_height = 1 + 0.2 * len(self.members)
            pyglet.gl.glScalef(1, obj_height, 1)

            self.node_vertices.draw(pyglet.gl.GL_TRIANGLES)

            pyglet.gl.glPopMatrix()
            pyglet.gl.glTranslatef(self.x, self.y, 0)
            #Label it with name and type
            pyglet.text.Label(str(self.var),
                              font_name='Times New Roman',
                              font_size=12,
                              x = 0,
                              y = 0,
                              anchor_y = 'center',
                              anchor_x= 'center',
                              color= (30, 255, 7, 255) if self.highlighted else (255, 255, 255, 255)
            ).draw()

            pyglet.gl.glTranslatef(-50, 0, 0)
            for field in self.members:
                pyglet.gl.glTranslatef(0, -15, 0)
                pyglet.text.Label(str(field),
                              font_name='Times New Roman',
                              font_size=10,
                              x = 0,
                              y = 0,
                              anchor_y = 'center',
                              anchor_x= 'left').draw()
            pyglet.gl.glPopMatrix()

        class Variable():
            def __init__(self, param):
                if isinstance(param.type, basestring):
                    self.type = param.type
                elif isinstance(param.type.name, basestring):
                    self.type = param.type.name
                else:
                    self.type = param.type.name.value

                if issubclass(type(param), FieldDeclaration):
                    self.name = param.variable_declarators[0].variable.name
                    if param.variable_declarators[0].variable.dimensions > 0:
                        self.name += "[]"
                else:
                    self.name = param.variable.name
                    if param.variable.dimensions > 0:
                        self.name += "[]"

                self.highlighted = False

            def __str__(self):
                return str(self.type) + " " + str(self.name)

