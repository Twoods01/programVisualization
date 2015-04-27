# programVisualization

This program generates a visualization of an input java program

Download the zip, unzip and run "sudo pip install pjViz" from the root of the directory

Run the program with pjViz -f \<flow_file> \<directory> \<program_args>
  * The flow file is optional, and will be generated for you after running a program once, this reduces load times for large programs
  * directory should contain the java program you want run
  * anything passed after the directory will be treated as the java program arguments and passed directly through

Controls:
  * Move around the graph with WASD
  * Zoom in and out with up and down arrows
  * Toggle animation with space
  * Switch between animation step over and step into with shift
  
Interaction:
  * Light orange nodes are user defined methods, you can click to enter them
  * The stack is shown in the bottom right corner in green, click on a frame to pop to it
  * Data used by the current method is shown in the bottom left in purple, hovering over it will draw connections to methods which use it, hovering over methods will highlight the data they use
  * In the top right you can control the speed of the animation by click on the + - next to scale and move speed
  
Enjoy!
