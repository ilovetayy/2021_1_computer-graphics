import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

M = np.identity(4)
projection_key = 0 #0:perspective, 1:orthogonal
mouse_btn = 0 #1:left 2:right

x_pos = 0.
y_pos = 0.

cur_x = 0.
cur_y = 0.

x_rot = 0.
y_rot = 0.
z_rot = 0.

zoom = 50.

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([50.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,50.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,50.]))
    glEnd()

def drawPlane():
    glBegin(GL_LINES)
    glColor3ub(100,100,100)
    for i in range(-50,51):
        glVertex3fv(np.array([i,0,-50]))
        glVertex3fv(np.array([i,0,50]))
        glVertex3fv(np.array([-50,0,i]))
        glVertex3fv(np.array([50,0,i]))        
    glEnd()

def mouse_button_callback(window, btn, action, mods):
    global mouse_btn
    
    if action==glfw.PRESS:
        if btn==glfw.MOUSE_BUTTON_LEFT:
            mouse_btn = 1
        elif btn==glfw.MOUSE_BUTTON_RIGHT:
            mouse_btn = 2      
    if action==glfw.RELEASE:
        mouse_btn = 0  

def cursor_pos_callback(window, xpos, ypos):
    global x_pos, y_pos, x_rot, y_rot, cur_x, cur_y, M
    
    if mouse_btn==1:#orbit
        x_rot = (xpos - cur_x)*0.5
        y_rot = (ypos - cur_y)*0.5

        rotate_y_axis = np.array([[np.cos(x_rot*np.pi/180),0,np.sin(x_rot*np.pi/180),0],
                                  [0,                       1,                     0, 0],
                                  [-np.sin(x_rot*np.pi/180),0,np.cos(x_rot*np.pi/180),0],
                                  [0,                       0,                     0, 1]])
        
        rotate_x_axis = np.array([[1,                      0,                        0, 0],
                                  [0,np.cos(-y_rot*np.pi/180),-np.sin(-y_rot*np.pi/180),0],
                                  [0,np.sin(-y_rot*np.pi/180),np.cos(-y_rot*np.pi/180),0],
                                  [0,                      0,                       0, 1]])
        M = rotate_x_axis @ M
        M = rotate_y_axis @ M
        
    elif mouse_btn==2:#panning
        x_pos = xpos - cur_x
        y_pos = ypos - cur_y

        T = np.array([[1,0,0,x_pos/200],
                      [0,1,0,-y_pos/200],
                      [0,0,1,         0],
                      [0,0,0,         1]])
        M = T @ M

    cur_x = xpos
    cur_y = ypos

def scroll_callback(window, xoffset, yoffset):#zoom
    global zoom

    if zoom > yoffset:
        zoom -= yoffset
#############################################################################
jName = []
jNum = 0
channels = []
jMotion = []
fNum = 0
fps = 0.0
jOffset = []
brackets = []

animation = 0 #1:animation starts

t = 1

fileName = ""

def key_callback(window, key, scancode, action, mods):#toggle projection
    global projection_key, animation
    
    if action==glfw.PRESS:
        if key==glfw.KEY_V:
            if projection_key==0:
                projection_key = 1
            else:
                projection_key = 0

        if key==glfw.KEY_SPACE:
            if animation==0:
                animation = 1
            else:
                animation = 0
                
def drop_callback(window, paths):
    global jName, jNum, channels, jMotion, fNum, fps, jOffset, brackets
    global animation, t, fileName
    
    file = open(" ".join(paths), 'r')
    jName = []
    jNum = 0
    channels = []
    jMotion = []
    fNum = 0
    fps = 0.0
    jOffset = []
    brackets = []
    t = 1
    animation = 0
    fileName = paths[0]
    
    for line in file:
        lines = line.split()
        if len(lines)==0:
            continue
        
        if lines[0]=="HIERARCHY" or lines[0]=="MOTION" or lines[0]=="End":
            continue
        elif lines[0]=="ROOT" or lines[0]=="JOINT":
            jName.append(lines[1])
            jNum += 1
        elif lines[0]=="{":
            brackets.append(lines[0])
        elif lines[0]=="}":
            brackets.append(lines[0])
        elif lines[0]=="OFFSET":
            tmp = (float(lines[1]), float(lines[2]), float(lines[3]))
            jOffset.append(tmp)
        elif lines[0]=="CHANNELS":
            channels.append(int(lines[1]))
            for i in range(int(lines[1])):
                jMotion.append([])
                j = len(jMotion)-1
                if lines[i+2].upper()=="XPOSITION":
                    jMotion[j].append(1.0)
                    jMotion[j].append(0.0)
                elif lines[i+2].upper()=="YPOSITION":
                    jMotion[j].append(2.0)
                    jMotion[j].append(0.0)
                elif lines[i+2].upper()=="ZPOSITION":
                    jMotion[j].append(3.0)
                    jMotion[j].append(0.0)
                elif lines[i+2].upper()=="XROTATION":
                    jMotion[j].append(4.0)
                    jMotion[j].append(0.0)
                elif lines[i+2].upper()=="YROTATION":
                    jMotion[j].append(5.0)
                    jMotion[j].append(0.0)
                elif lines[i+2].upper()=="ZROTATION":
                    jMotion[j].append(6.0)
                    jMotion[j].append(0.0)

        elif lines[0]=="Frames:":
            fNum = int(lines[1])
        elif lines[0]=="Frame":
            fps = 1.0 / float(lines[2])
        else:
            for i in range(len(jMotion)):
                jMotion[i].append(lines[i])

    print(" ")
    print("file name: "+str(paths))
    print("number of frames: "+str(fNum))
    print("FPS: "+str(fps))
    print("number of joints (including root): "+str(jNum))
    print("list of all joint names:")
    for i in range(jNum):
        print("   "+str(jName[i]))

def l2norm(v):
    return np.sqrt(np.dot(v, v))

def normalized(v):
    l = l2norm(v)
    return 1/l * np.array(v)

def drawUnitCube():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))
def createVertexArraySeparate():
    varr = np.array([
            [0,1,0],            # v0 normal
            [ 0.05, 1.,-0.05],   # v0 position
            [0,1,0],            # v1 normal
            [-0.05, 1.,-0.05],   # v1 position
            [0,1,0],            # v2 normal
            [-0.05, 1., 0.05],   # v2 position

            [0,1,0],            # v3 normal
            [ 0.05, 1.,-0.05],   # v3 position
            [0,1,0],            # v4 normal
            [-0.05, 1., 0.05],   # v4 position
            [0,1,0],            # v5 normal
            [ 0.05, 1., 0.05],   # v5 position

            [0,-1,0],           # v6 normal
            [ 0.05, 0., 0.05],   # v6 position
            [0,-1,0],           # v7 normal
            [-0.05, 0., 0.05],   # v7 position
            [0,-1,0],           # v8 normal
            [-0.05, 0.,-0.05],   # v8 position

            [0,-1,0],
            [ 0.05, 0., 0.05],
            [0,-1,0],
            [-0.05, 0.,-0.05],
            [0,-1,0],
            [ 0.05, 0.,-0.05],

            [0,0,1],
            [ 0.05, 1., 0.05],
            [0,0,1],
            [-0.05, 1., 0.05],
            [0,0,1],
            [-0.05, 0., 0.05],

            [0,0,1],
            [ 0.05, 1., 0.05],
            [0,0,1],
            [-0.05, 0., 0.05],
            [0,0,1],
            [ 0.05, 0., 0.05],

            [0,0,-1],
            [ 0.05, 0.,-0.05],
            [0,0,-1],
            [-0.05, 0.,-0.05],
            [0,0,-1],
            [-0.05, 1.,-0.05],

            [0,0,-1],
            [ 0.05, 0.,-0.05],
            [0,0,-1],
            [-0.05, 1.,-0.05],
            [0,0,-1],
            [ 0.05, 1.,-0.05],

            [-1,0,0],
            [-0.05, 1., 0.05],
            [-1,0,0],
            [-0.05, 1.,-0.05],
            [-1,0,0],
            [-0.05, 0.,-0.05],

            [-1,0,0],
            [-0.05, 1., 0.05],
            [-1,0,0],
            [-0.05, 0.,-0.05],
            [-1,0,0],
            [-0.05, 0., 0.05],

            [1,0,0],
            [ 0.05, 1.,-0.05],
            [1,0,0],
            [ 0.05, 1., 0.05],
            [1,0,0],
            [ 0.05, 0., 0.05],

            [1,0,0],
            [ 0.05, 1.,-0.05],
            [1,0,0],
            [ 0.05, 0., 0.05],
            [1,0,0],
            [ 0.05, 0.,-0.05],
            # ...
            ], 'float32')
    return varr

def drawSkeleton():
    global animation, jOffset, jMotion, brackets, t, fileName

    j = 0
    c_i = 0
    m_i = 0

    split = fileName.split('\\')
    fileName = split[-1]
    
    if fileName=="sample-walk.bvh":
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        lightPos = (5., 5., 5., 1.)
        lightColor = (1., 1., 1., 1.)
        ambientLightColor = (.1, .1, .1, 1.)
        
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

        objectColor = (0, 1., 0., 1.)
        specularObjectColor = (1., 1., 1., 1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 30)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

                   
    for i in range(len(brackets)):
        if brackets[i]=="{":
            glPushMatrix()
            
            v1 = np.array((0,0,0))
            v2 = v1 + np.array(jOffset[j])
            tmp = np.array(jOffset[j])
            
            if fileName != "sample-walk.bvh":
                glLineWidth(6)
                glBegin(GL_LINES)
                glColor3ub(0,0,255)
                glVertex3fv(v1)
                glVertex3fv(v2)
                glEnd()
                
            elif fileName == "sample-walk.bvh":
                glPushMatrix()
                vector = np.array([tmp[0], tmp[1], tmp[2]])    
                boxSize = l2norm(vector)       
                
                vector = normalized(vector)     
                rot = np.cross(np.array([0, 1, 0]), vector)     

                theta = np.arcsin(l2norm(rot))      
                theta = np.rad2deg(theta)

                if np.dot(vector, np.array([0, 1, 0])) < 0:
                    theta = 180-theta

                glRotate(theta, rot[0], rot[1], rot[2])
                glScale(1, boxSize, 1)
                drawUnitCube()
                glPopMatrix()

            glTranslatef(tmp[0], tmp[1], tmp[2])
            j += 1

            if brackets[i+1]=="}":
                continue
            elif channels[c_i]==3:
                first = [0,0,0]
                second = [0,0,0]
                third = [0,0,0]
                
                first[int(jMotion[m_i][0])-4] = 1
                second[int(jMotion[m_i+1][0])-4] = 1
                third[int(jMotion[m_i+2][0])-4] = 1

                glRotatef(float(jMotion[m_i][t]), first[0], first[1], first[2])
                glRotatef(float(jMotion[m_i+1][t]), second[0], second[1], second[2])
                glRotatef(float(jMotion [m_i+2][t]), third[0], third[1], third[2])
                
                m_i += 3
            elif channels[c_i]==6:
                translation = [.0, .0, .0]
                translation[int(jMotion[m_i][0])-1] = jMotion[m_i][t]
                translation[int(jMotion[m_i+1][0])-1] = jMotion[m_i+1][t]
                translation[int(jMotion[m_i+2][0])-1] = jMotion[m_i+2][t]
                
                glTranslatef(float(translation[0]), float(translation[1]), float(translation[2]))
                first = [0,0,0]
                second = [0,0,0]
                third = [0,0,0]
                
                first[int(jMotion[m_i+3][0])-4] = 1
                second[int(jMotion[m_i+4][0])-4] = 1
                third[int(jMotion[m_i+5][0])-4] = 1

                glRotatef(float(jMotion[m_i+3][t]), first[0], first[1], first[2])
                glRotatef(float(jMotion[m_i+4][t]), second[0], second[1], second[2])
                glRotatef(float(jMotion[m_i+5][t]), third[0], third[1], third[2])
                
                m_i += 6
            c_i += 1

        elif brackets[i]=="}":
            glPopMatrix()

    if animation==1:
        t += 1
    if t==fNum-1:
        t = 2

    glDisable(GL_LIGHTING)

def render():
    global M, projection_key, zoom

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    
    near = 5.
    far = 100.
    tmp = np.tan(zoom/360*np.pi)*near

    if projection_key==0:
        glFrustum(-tmp,tmp, -tmp,tmp, near,far)
        #gluPerspective(50,1,near,far)
    elif projection_key==1:
        glOrtho(-tmp*3,tmp*3, -tmp*3,tmp*3, near,far)
    
    glTranslatef(0, 0, -15)
    glMultMatrixf(M.T)

    glLineWidth(0.5)
    drawFrame()
    drawPlane()

    drawSkeleton()

gVertexArraySeparate = None

def main():
    global gVertexArraySeparate
    
    if not glfw.init():
        return

    window = glfw.create_window(800,800,"assignment_3",None,None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    glfw.swap_interval(1)
    gVertexArraySeparate = createVertexArraySeparate()
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()
    
if __name__=="__main__":
    main()
