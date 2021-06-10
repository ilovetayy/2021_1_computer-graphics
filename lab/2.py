import numpy as np
import glfw
from OpenGL.GL import *

input_key = 100

gComposedM = np.array([[1.,0.,0.],
                       [0.,1.,0.],
                       [0.,0.,1.]])

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINES)
    glColor3ub(255,0,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0,255,0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv((T @ np.array([.0,.5,1.])) [:-1])
    glVertex2fv((T @ np.array([.0,.0,1.])) [:-1])
    glVertex2fv((T @ np.array([.5,.0,1.])) [:-1])
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gComposedM
    if((action == glfw.PRESS or action == glfw.REPEAT) and (key==87 or key==69 or key ==83 or
                                 key==68 or key==88 or key==67 or
                                 key==82 or key==49)):
        global input_key
        input_key = key

        if(input_key==87 ):#W
            S = np.array([[1.,0.,0.],
                          [0.,.9,0.],
                          [0.,0.,1.]])
            gComposedM = S @ gComposedM
        elif(input_key==69):#E
            S = np.array([[1.,0.,0.],
                          [0.,1.1,0.],
                          [0.,0.,1.]])
            gComposedM = S @ gComposedM
        elif(input_key==83):#S
            th = np.radians(10)
            R = np.array([[np.cos(th), -np.sin(th), 0.],
                          [np.sin(th), np.cos(th), 0.],
                          [0., 0., 1.]])
            gComposedM = R @ gComposedM
        elif(input_key==68):#D
            th = np.radians(-10)
            R = np.array([[np.cos(th), -np.sin(th), 0.],
                          [np.sin(th), np.cos(th), 0.],
                          [0., 0., 1.]])
            gComposedM = R @ gComposedM
        elif(input_key==88):#X
            M = np.array([[1., 0., .1],
                          [0., 1., 0.],
                          [0., 0., 1.]])
            gComposedM = M @ gComposedM
        elif(input_key==67):#C
            M = np.array([[1., 0., -.1],
                          [0., 1., 0.],
                          [0., 0., 1.]])
            gComposedM = M @ gComposedM
        elif(input_key==82):#R
            M = np.array([[-1., 0., 0.],
                          [0., -1., 0.],
                          [0., 0., 1.]])
            gComposedM = M @ gComposedM
        elif(input_key==49):#1
            gComposedM = np.array([[1.,0.,0.],
                                        [0.,1.,0.],
                                        [0.,0.,1.]])
            

def main():
    global gComposedM
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

        render(gComposedM)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
