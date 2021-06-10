#Smooth shaded cube
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.
gCamHeight = 1.
lightColor = (1., 1., 1., 1.)
objectColor = [0., 0., 0., 1.]
gVertexArrayIndexed = None
gIndexArray = None

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, varr)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)     

def createVertexAndIndexArrayIndexed():
    a = 0.5773502691896258
    b = 0.8164965809277261
    c = 0.4082482904639631
    
    varr = np.array([
            (-1, 1, 1, -a,a,a),
            (1, 1, 1, b,c,c),
            (1, -1, 1, c,-c,b),
            (-1, -1, 1, -c,-b,c),
            (-1, 1, -1, -c,c,-b),
            (1, 1, -1, c,b,-c),
            (1, -1, -1, a,-a,-a),
            (-1, -1, -1, -b,-c,-c)
            ], 'float32')

    iarr = np.array([
            (0, 2, 1),
            (0, 3, 2),
            (4, 5, 6),
            (4, 6, 7),
            (0, 1, 5),
            (0, 5, 4),
            (3, 6, 2),
            (3, 7, 6),
            (1, 2, 6),
            (1, 6, 5),
            (0, 7, 3),
            (0, 4, 7)
            ])

    return varr, iarr

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, objectColor
    
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_R:
            objectColor[0] += 1
            if objectColor[0]==2:
                objectColor[0] = 0
        elif key==glfw.KEY_G:
            objectColor[1] += 1
            if objectColor[1]==2:
                objectColor[1] = 0
        elif key==glfw.KEY_B:
            objectColor[2] += 1
            if objectColor[2]==2:
                objectColor[2] = 0

def render():
    global gCamAng, gCamHeight, lightColor, objectColor
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_NORMALIZE)

    glPushMatrix()

    t = glfw.get_time()

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()

    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 30)

    glPushMatrix()
    
    #glColor3ub(0, 0, 255)
    drawCube_glDrawElements()
    glPopMatrix()

    glDisable(GL_LIGHTING)
    
def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    
    window = glfw.create_window(480,480,'2018008804', None,None)
    
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()
  
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
