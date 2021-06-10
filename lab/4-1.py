import glfw
from OpenGL.GL import *
import numpy as np

input_key = list()

def render():
    global input_key
    
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0,255,0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()

    glColor3ub(255,255,255)

    for i in reversed(input_key):
        if(i==81):#Q
            glTranslatef(-0.1, 0, 0)
            
        elif(i==69):#E
            glTranslatef(0.1, 0, 0)
            
        elif(i==65):#A
            glRotatef(10, 0, 0, 1)
            
        elif(i==68):#D
            glRotatef(-10, 0, 0, 1)
            
        elif(i==49):#1
            input_key.clear()

    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0., .5]))
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([.5, 0.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global input_key
    if((action==glfw.PRESS or action==glfw.REPEAT) and (key==81 or key==69 or key==65
                                                        or key==68 or key==49)):
        input_key.append(key)
        
def main():
    if not glfw.init():
        return

    window = glfw.create_window(480,480,"2018008804",None,None)
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

if __name__=="__main__":
    main()
