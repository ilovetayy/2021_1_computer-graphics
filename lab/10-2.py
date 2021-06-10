import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo

gCamAng = 0.
gCamHeight = 1.

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -1 ,  1 ,  1 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  1 ,  1 ,  1 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  1 , -1 ,  1 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -1 , -1 ,  1 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -1 ,  1 , -1 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  1 ,  1 , -1 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  1 , -1 , -1 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([3.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,3.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,3.]))
    glEnd()

def l2norm(v):
    return np.sqrt(np.dot(v, v))

def normalized(v):
    l = l2norm(v)
    return 1/l * np.array(v)

def exp(rv):
    theta = l2norm(rv)
    if theta == 0:
        R = np.identity(4)
        return R

    rv = normalized(rv)
    
    x = rv[0]
    y = rv[1]
    z = rv[2]
    R = np.identity(4)
    
    R[0,0] = np.cos(theta) + x*x*(1-np.cos(theta))
    R[1,0] = y*x*(1-np.cos(theta)) + z*np.sin(theta)
    R[2,0] = z*x*(1-np.cos(theta)) - y*np.sin(theta)

    R[0,1] = x*y*(1-np.cos(theta)) - z*np.sin(theta)
    R[1,1] = np.cos(theta) + y*y*(1-np.cos(theta))
    R[2,1] = z*y*(1-np.cos(theta)) + x*np.sin(theta)

    R[0,2] = x*z*(1-np.cos(theta)) + y*np.sin(theta)
    R[1,2] = y*z*(1-np.cos(theta)) - x*np.sin(theta)
    R[2,2] = np.cos(theta) + z*z*(1-np.cos(theta))
    
    return R

def log(R):
    theta = np.arccos((R[0,0] + R[1,1] + R[2,2] - 1)/2)
    rv0 = (R[2,1] - R[1,2]) / 2*np.sin(theta)
    rv1 = (R[0,2] - R[2,0]) / 2*np.sin(theta)
    rv2 = (R[1,0] - R[0,1]) / 2*np.sin(theta)
    rv = normalized(np.array([rv0, rv1, rv2]))
    return theta*rv

def slerp(R1, R2, t):
    return R1 @ exp(t*log(R1.T @ R2))

def Rotate_X(t):
    T = np.identity(4)
    T[1:3, 1:3] = np.array([[np.cos(t), -np.sin(t)],
                             [np.sin(t), np.cos(t)]])
    return T

def Rotate_Y(t):
    T = np.identity(4)
    T[0, :3] = np.array([np.cos(t), 0, np.sin(t)])
    T[2, :3] = np.array([-np.sin(t), 0, np.cos(t)])
    return T

def Rotate_Z(t):
    T = np.identity(4)
    T[:2, :2] = np.array([[np.cos(t), -np.sin(t)],
                           [np.sin(t), np.cos(t)]])
    return T

def Rotation_R1(t):
    R1 = np.identity(4)
    tmp = np.identity(4)
    
    if t >= 0 and t < 20: 
        x = np.radians(20)
        y = np.radians(30)
        z = np.radians(30)
        R1 = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        x = np.radians(45)
        y = np.radians(60)
        z = np.radians(40)       
        tmp = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        R1 = slerp(R1, tmp, t/20)
            
    elif t >= 20 and t < 40:
        x = np.radians(45)
        y = np.radians(60)
        z = np.radians(40)
        R1 = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        x = np.radians(60)
        y = np.radians(70)
        z = np.radians(50)
        tmp = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        R1 = slerp(R1, tmp, (t - 20)/20)

    elif t >= 40 and t < 60:
        x = np.radians(60)
        y = np.radians(70)
        z = np.radians(50)
        R1 = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        x = np.radians(80)
        y = np.radians(85)
        z = np.radians(70)
        tmp = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        R1 = slerp(R1, tmp, (t - 40)/20)

    elif t == 60:
        x = np.radians(80)
        y = np.radians(85)
        z = np.radians(70)
        R1 = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

    return R1

def Rotation_R2(t):
    R2 = np.identity(4)
    tmp = np.identity(4)
    if t >= 0 and t < 20:
        x = np.radians(25)
        y = np.radians(40)
        z = np.radians(40)
        R2 = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        x = np.radians(15)
        y = np.radians(30)
        z = np.radians(25)
        tmp = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        R2 = slerp(tmp, R2, t/20)

    elif t >= 20 and t < 40:
        x = np.radians(40)
        y = np.radians(60)
        z = np.radians(50)
        R2 = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        x = np.radians(25)
        y = np.radians(40)
        z = np.radians(40)
        tmp = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        R2 = slerp(tmp, R2, (t - 20)/20)

    elif t >= 40 and t < 60:
        x = np.radians(55)
        y = np.radians(80)
        z = np.radians(65)
        R2 = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        x = np.radians(40)
        y = np.radians(60)
        z = np.radians(50)
        tmp = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

        R2 = slerp(tmp, R2, (t - 40)/20)

    elif t == 60:
        x = np.radians(55)
        y = np.radians(80)
        z = np.radians(65)

        R2 = Rotate_X(x) @ Rotate_Y(y) @ Rotate_Z(z)

    return R2

def render(t):
    global gCamAng, gCamHeight, pre_pos
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    # draw global frame
    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
  
    objectColor = (1.,1.,1.,1.)        
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)    

    R1 = Rotation_R1(t)        
    J1 = R1
    
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    R2 = Rotation_R2(t)
    T1 = np.identity(4)
    T1[0][3] = 1.

    J2 = R1 @ T1 @ R2
   
    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    frame = [0, 20, 40, 60]
    for i in frame:
        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        if i == 0:
            objectColor = (1., 0., 0., 1.)
            specularObjectColor = (1., 0., 0., 1.)
        elif i == 20:
            objectColor = (1., 1., 0., 1.)
            specularObjectColor = (1., 1., 0., 1.)
        elif i == 40:
            objectColor = (0., 1., 0., 1.)
            specularObjectColor = (0., 1., 0., 1.)
        elif i == 60:
            objectColor = (0., 0., 1., 1.)
            specularObjectColor = (0., 0., 1., 1.)
                    
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
        
        R1 = Rotation_R1(i)
        R2 = Rotation_R2(i)
           
        J1 = R1
    
        glPushMatrix()
        glMultMatrixf(J1.T)
        glPushMatrix()
        glTranslatef(0.5,0,0)
        glScalef(0.5, 0.05, 0.05)
        drawCube_glDrawElements()
        glPopMatrix()
        glPopMatrix()

        T1 = np.identity(4)
        T1[0][3] = 1.

        J2 = R1 @ T1 @ R2
       
        glPushMatrix()
        glMultMatrixf(J2.T)
        glPushMatrix()
        glTranslatef(0.5,0,0)
        glScalef(0.5, 0.05, 0.05)
        drawCube_glDrawElements()
        glPopMatrix()
        glPopMatrix()

    glDisable(GL_LIGHTING)
 
def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2018008804', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    t = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        t = (t+1) % 61
        render(t)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

