__author__ = 'twoods0129'
from javaParser import *
from staticGraph import *
import pyglet, sys, getopt
import camera

control_color = (150, 150, 150)
progress_bar_color = (45, 45, 45)
control_height = 30
progress_bar_offset = 40
animation_playing = False

graph = 0
speed = .3
scroll_buffer = 10

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"d", [])
    except getopt.GetoptError:
        print("main.py -d <directory>")
        sys.exit(2)

    directory = "s1"
    visualization = StaticGraph
    timeout = None
    processing = True

    # for opt, arg in opts:
    #     if opt == "-d":
    #         directory = arg
    #     elif opt == "-s":
    #         pass
    #         #visualization = InteractiveGraph

    if directory is None:
        print("main.py -d <directory>")
        sys.exit(2)

    window = pyglet.window.Window(1200, 700)
    cam = camera.Camera(window.width, window.height)

    parsed = Javap(directory)
    global graph
    if visualization.isDynamic:
        parsed.markup_file()
        graph = visualization(parsed.run_file(processing, timeout), parsed.get_all_methods())
    else:
        graph = visualization(parsed, window)

    #parsed.cleanup()

    fps_display = pyglet.clock.ClockDisplay()

    @window.event
    def on_draw():
         if graph.needs_redraw:
            window.clear()
            cam.standard_projection()
            graph.draw(window)
            cam.hud_projection()
            graph.draw_UI(window)
            if visualization.isDynamic:
                draw_UI(window)
            #fps_display.draw()


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
                graph.handle_input(x, y, cam, window)


    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.LEFT:
            graph.step_backward()
        elif symbol == pyglet.window.key.RIGHT:
            graph.step_forward()
        elif symbol == pyglet.window.key.UP:
            #graph.zoom += .1
            cam.z += .1
            graph.redraw()
        elif symbol == pyglet.window.key.DOWN:
            cam.z -= .1
            if graph.zoom > 0.2:
                #graph.zoom -= .1
                graph.redraw()
        elif symbol == pyglet.window.key.F:
            graph.build_final()
        elif symbol == pyglet.window.key.W:
            cam.y += 50
            graph.redraw()
        elif symbol == pyglet.window.key.S:
            cam.y -= 50
            graph.redraw()
        elif symbol == pyglet.window.key.A:
            cam.x -= 50
            graph.redraw()
        elif symbol == pyglet.window.key.D:
            cam.x += 50
            graph.redraw()

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        if y > window.height - scroll_buffer:
            graph.center_y -= 10
        elif y < scroll_buffer:
            graph.center_y += 10

        if x > window.width - scroll_buffer:
            graph.center_x -= 10
        elif x < scroll_buffer:
            graph.center_x += 10

    #pyglet.clock.schedule_interval(update, speed)
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
