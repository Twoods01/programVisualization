__author__ = 'twoods0129'
from Parser.javaParser import *
from Graph.staticGraph import *
import pyglet, sys, getopt
from pyglet.window import key
import Utils.camera

control_color = (150, 150, 150)
progress_bar_color = (45, 45, 45)
control_height = 30
progress_bar_offset = 40
animation_playing = False

mouse_previously_inside_node = False

graph = 0
frame_rate = 60
speed = 1.0 / frame_rate
scroll_buffer = 10

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hf:")
    except getopt.GetoptError:
        print("main.py -f <flow_file> <directory> <program_args>")
        sys.exit(2)

    directory = "s1"
    visualization = StaticGraph
    p_args = None
    program_flow_file = None
    timeout = None
    processing = True

    for opt, arg in opts:
        if opt == "-h":
            print("main.py -f <flow_file> <directory> <program_args>")
            return
        elif opt == "-f":
            program_flow_file = arg
            print("flow set to " + program_flow_file)

    if len(args) < 1:
        print("main.py -f <flow_file> <directory> <program_args>")
        return

    directory = args[0]
    p_args = " ".join(args[1:])

    window = pyglet.window.Window(1200, 700)
    cam = Utils.camera.Camera(window.width, window.height)

    parsed = Javap(directory, p_args)
    global graph
    if visualization.isDynamic:
        parsed.markup_file()
        graph = visualization(parsed.run_file(processing, timeout), parsed.get_all_methods())
    else:
        parsed.markup_file()
        if program_flow_file:
            try:
                flow_file = open(program_flow_file, "r")
                flow = []
                for line in flow_file:
                    flow.append(line)
            except IOError:
                print("Unable to open file " + program_flow_file)
                return
        else:
            flow = parsed.run_file()
            flow_file = open(parsed.main.name.split("/")[-1] + ".flow", "w")
            for line in flow:
                flow_file.write(line + "\n")
        graph = visualization(parsed, window, cam, flow)

    #parsed.cleanup()

    fps_display = pyglet.clock.ClockDisplay()

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        global animation_playing
        if button == pyglet.window.mouse.LEFT:
            if visualization.isDynamic:
                #play button
                if window.width / 2 - 20 < x < window.width / 2 + 20 and control_height - 20 < y < control_height + 20:
                    animation_playing = not animation_playing
                elif window.width / 2 + 40 < x < window.width / 2 + 80 and control_height - 10 < y < control_height + 10:
                    animation_playing = False
                    graph.step_forward()
                elif window.width / 2 - 80 < x < window.width / 2 - 40 and control_height - 10 < y < control_height + 10:
                    animation_playing = False
                    graph.step_backward()
            else:
                graph.handle_input(x, y)

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.LEFT:
            graph.step_backward()
        elif symbol == pyglet.window.key.RIGHT:
            graph.step_forward()
        elif symbol == pyglet.window.key.UP:
            cam.zoom += .1
        elif symbol == pyglet.window.key.DOWN:
            if cam.zoom > 0.2:
                cam.zoom -= .1
        elif symbol == pyglet.window.key.F:
            graph.build_final()
        elif symbol == pyglet.window.key.SPACE:
            graph.auto_play = not graph.auto_play
            graph.animation_forward()
        elif symbol == pyglet.window.key.RSHIFT or symbol == pyglet.window.key.LSHIFT:
            graph.dot.step_into = not graph.dot.step_into

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        global mouse_previously_inside_node
        in_node = graph.handle_mouse(x, y)
        if mouse_previously_inside_node and not in_node:
            mouse_previously_inside_node = False
            graph.data.clear_highlights()

        elif in_node:
            mouse_previously_inside_node = True

    #This has to be after the key press handler, dumb pyglet
    keys = key.KeyStateHandler()
    window.push_handlers(keys)

    @window.event
    def on_draw():
        pyglet.clock.tick()
        window.clear()

        if keys[key.W]:
            cam.y += 50
            if graph.invis_node:
                graph.invis_node.y += 50
        if keys[key.S]:
            cam.y -= 50
            if graph.invis_node:
                graph.invis_node.y -= 50
        if keys[key.D]:
            cam.x += 50
            if graph.invis_node:
                graph.invis_node.x += 50
        if keys[key.A]:
            cam.x -= 50
            if graph.invis_node:
                graph.invis_node.x -= 50

        cam.standard_projection()
        graph.draw()
        cam.hud_projection()
        graph.draw_UI()
        # if visualization.isDynamic:
        #     draw_UI(window)
        fps_display.draw()

    pyglet.clock.schedule_interval(update, speed)
    pyglet.clock.set_fps_limit(frame_rate)
    pyglet.app.run()

def draw_UI(window):
    #Play button
    draw_arrow(window.width / 2, control_height, 1, control_color)

    #Step forward
    draw_arrow(window.width / 2 + 50, control_height, .5, control_color)
    draw_arrow(window.width / 2 + 70, control_height, .5, control_color)

    #Step backward
    draw_arrow(window.width / 2 - 50, control_height, -.5, control_color)
    draw_arrow(window.width / 2 - 70, control_height, -.5, control_color)

    #Progress bar
    draw_rect(progress_bar_offset, control_height + 40, window.width - (progress_bar_offset * 2), 5, progress_bar_color)
    #Calculate current progress
    step = (window.width - (progress_bar_offset * 2)) / (len(graph.flow) - 1)
    draw_rect(progress_bar_offset - 5 + graph.position * step, control_height + 35, 5, 15, control_color)

def draw_arrow(x, y, scale, color):
    pyglet.gl.glPushMatrix()
    pyglet.gl.glTranslatef(x, y, 0)
    pyglet.gl.glScalef(scale, scale, scale)
    pyglet.gl.glTranslatef(-x, -y, 0)
    pyglet.graphics.draw_indexed(3, pyglet.gl.GL_TRIANGLES,
                                [0, 1, 2],
                                ('v2i', (x - 20, y - 20,
                                        x - 20, y + 20,
                                        x + 20, y)),
                                ('c3B', color * 3))
    pyglet.gl.glPopMatrix()


def draw_rect(x, y, width, height, color):
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
                                [0, 1, 2, 1, 2, 3],
                                ('v2i', (x, y,
                                        x + width, y,
                                        x, y + height,
                                        x + width, y + height)),
                                ('c3B', color * 4))

def update(dt):
    if animation_playing:
        if not graph.step_forward():
            pyglet.clock.unschedule(update)
            graph.write()


if __name__ == '__main__':
    main(sys.argv[1:])
