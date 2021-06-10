import numpy as np
import glfw
from OpenGL.GL import *

global input_key
input_key = 100

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    for i in range(0, 12):
        glVertex2f(np.cos(2*i*np.pi/12), np.sin(2*i*np.pi/12))
    glEnd()

    glBegin(GL_LINES)
    
    if(input_key == 100):
        glVertex2f(0,0)
        glVertex2f(0,1)
    elif(input_key>=49 and input_key<=57):
        glVertex2f(0,0)
        glVertex2f(np.cos(np.pi*(0.5-(int(input_key)-48)/6)), np.sin(np.pi*(0.5-(int(input_key)-48)/6)))
    elif(input_key == 48):
        glVertex2f(0,0)
        glVertex2f(np.cos(5*np.pi/6), np.sin(5*np.pi/6))
    elif(input_key == 81):
        glVertex2f(0,0)
        glVertex2f(np.cos(2*np.pi/3), np.sin(2*np.pi/3))
    elif(input_key == 87):
        glVertex2f(0,0)
        glVertex2f(0,1)

    glEnd()

def key_callback(window, key, scnacode, action, mods):
    if(action == glfw.PRESS and ((key>=48 and key<=57) or key==81 or key==87)):
        global input_key
        input_key = key

def main():
    if not glfw.init():
        return

    window = glfw.create_window(480, 480, "2018008804", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    
    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
