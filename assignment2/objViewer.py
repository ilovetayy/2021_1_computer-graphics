import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

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
    glVertex3fv(np.array([5.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,5.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,5.]))
    glEnd()

def drawPlane():
    glBegin(GL_LINES)
    glColor3ub(255,212,0)
    for i in range(-100,101):
        glVertex3fv(np.array([i,0,-100]))
        glVertex3fv(np.array([i,0,100]))
        glVertex3fv(np.array([-100,0,i]))
        glVertex3fv(np.array([100,0,i]))        
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
    #global zoom
    
    #if(zoom > yoffset):
     #   zoom -= yoffset

    global M
    T = np.array([[1,0,0,0],
                [0,1,0,0],
                [0,0,1,yoffset],
                [0,0,0,1]])
    M = T @ M

##########################################################################    
gVertexArray = np.empty((0,3), dtype = 'float32')
gVarrArray = np.empty((0,3), dtype = 'float32')
gIndexArray = np.empty((0,3), dtype = 'float32')
gNormArray = np.empty((0,3), dtype = 'float32')

h1VertexArray = np.empty((0,3), dtype = 'float32')
h1VarrArray = np.empty((0,3), dtype = 'float32')
h1IndexArray = np.empty((0,3), dtype = 'float32')
h1NormArray = np.empty((0,3), dtype = 'float32')

h2VertexArray = np.empty((0,3), dtype = 'float32')
h2VarrArray = np.empty((0,3), dtype = 'float32')
h2IndexArray = np.empty((0,3), dtype = 'float32')
h2NormArray = np.empty((0,3), dtype = 'float32')

h3VertexArray = np.empty((0,3), dtype = 'float32')
h3VarrArray = np.empty((0,3), dtype = 'float32')
h3IndexArray = np.empty((0,3), dtype = 'float32')
h3NormArray = np.empty((0,3), dtype = 'float32')

h_mode = 0
Z_key = 0

def render():
    global zoom, width, height, M, projection_key
    global gVarrArray, gIndexArray, gNormArray, Z_key, h_mode
    global h1VertexArray, h1VarrArray, h1IndexArray, h1NormArray, h2VertexArray, h2VarrArray, h2IndexArray, h2NormArray, h3VertexArray, h3VarrArray, h3IndexArray, h3NormArray
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    if Z_key==0:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

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
    
    drawFrame()
    drawPlane()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)

    #LIGHT0
    glPushMatrix()
    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()

    ambientLightColor0 = (.1,.0,.0, 1.)
    diffuseLightColor0 = (1.,.0,.0, 1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor0)

    #LIGHT1
    glPushMatrix()
    lightPos = (-3.,-4.,5.,1.) 
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    glPopMatrix()
    
    ambientLightColor1 = (.0,.1,.0, 1.)
    diffuseLightColor1 = (.0, 1.,.0, 1.)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLightColor1)

    #LIGHT2
    glPushMatrix()
    lightpos = (-3.,4.,-5.,1.)
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos)
    glPopMatrix()

    ambientLightColor2 = (.0,.0,.1, 1.)
    diffuseLightColor2 = (.0,.0, 1.,1.)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor2)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, diffuseLightColor2)
    
    #material
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    if h_mode==1:
        t = glfw.get_time()
        #h1
        glPushMatrix()
        glTranslatef(5*np.cos(t), 0, 5*np.sin(t))

        glPushMatrix()
        obj_drawh1()
        glPopMatrix()

        #h2
        glPushMatrix()
        glRotatef(t*(180/np.pi), 0, 1, 0)

        glPushMatrix()  
        obj_drawh2()
        glPopMatrix()

        #h3
        glPushMatrix()
        glRotatef(t*(180/np.pi), 0, 0, 1)

        glPushMatrix()
        obj_drawh3()
        glPopMatrix()

        glPopMatrix()
        glPopMatrix()
        glPopMatrix()
    else:
        glPushMatrix()
        obj_glDrawElements()
        glPopMatrix()

    glDisable(GL_LIGHTING)

def obj_ReadModels():
    global h1VertexArray, h1VarrArray, h1IndexArray, h1NormArray, h2VertexArray, h2VarrArray, h2IndexArray, h2NormArray, h3VertexArray, h3VarrArray, h3IndexArray, h3NormArray

    vertex = []
    normal = []
    varr = []
    norm = []
    iarr = []
    adjacent = []
    vertexCount = 0

    file_path_1 = open("./balloon_1.obj", 'r')

    for line in file_path_1:
        if line.startswith('#'):
            continue
        
        lines = line.split()
        lineNum = lines[1:]

        if not lines:
            continue
        
        if lines[0]=="v":
            tmp = (float(lines[1]), float(lines[2]), float(lines[3]))
            vertex.append(tmp)
            adjacent.append([.0])
            vertexCount += 1

        if lines[0]=="vn":
            tmp = (float(lines[1]), float(lines[2]), float(lines[3]))
            normal.append(tmp)

        if lines[0]=='f':
            search = lines[1].split('/')
            iarr_1 = int(search[0])
            vertex_1 = vertex[int(search[0])-1]
            normal_1 = normal[int(search[2])-1]
            varr.append(normal_1)
            varr.append(vertex_1)
            
            search = lines[2].split('/')
            iarr_2 = int(search[0])
            vertex_2 = vertex[int(search[0])-1]
            normal_2 = normal[int(search[2])-1]
            varr.append(normal_2)
            varr.append(vertex_2)
            
            search = lines[3].split('/')
            iarr_3 = int(search[0])
            vertex_3 = vertex[int(search[0])-1]
            normal_3 = normal[int(search[2])-1]
            varr.append(normal_3)
            varr.append(vertex_3)

            iarr.append((iarr_1 - 1, iarr_2 - 1, iarr_3 - 1))

            ver_1 = np.array(vertex_1)
            ver_2 = np.array(vertex_2)
            ver_3 = np.array(vertex_3)
            
            V2 = ver_2 - ver_1
            V3 = ver_3 - ver_1
            Vout = np.cross(V2, V3)
            Vsize = np.sqrt(np.dot(Vout, Vout))
            V_fn = Vout / Vsize

            line_vector = np.array([V_fn[0],V_fn[1],V_fn[2]])

            adjacent[iarr_1 - 1] += line_vector
            adjacent[iarr_2 - 1] += line_vector
            adjacent[iarr_3 - 1] += line_vector

            i = 3
            faceNum = len(lineNum)
            while ( faceNum > 3):
                search = lines[i].split('/')
                iarr_2 = int(search[0])
                vertex_2 = vertex[int(search[0])-1]
                normal_2 = normal[int(search[2])-1]
                
                search = lines[i+1].split('/')
                iarr_3 = int(search[0])
                vertex_3 = vertex[int(search[0])-1]
                normal_3 = normal[int(search[2])-1]

                iarr.append((iarr_1 - 1, iarr_2 - 1, iarr_3 - 1))

                ver_2 = np.array(vertex_2)
                ver_3 = np.array(vertex_3)
                
                V2 = ver_2 - ver_1
                V3 = ver_3 - ver_1
                Vout = np.cross(V2, V3)
                Vsize = np.sqrt(np.dot(Vout, Vout))
                V_fn = Vout / Vsize

                line_vector = np.array([V_fn[0],V_fn[1],V_fn[2]])
                
                adjacent[iarr_1 - 1] += line_vector
                adjacent[iarr_2 - 1] += line_vector
                adjacent[iarr_3 - 1] += line_vector

                varr.append(normal_1)
                varr.append(vertex_1)

                varr.append(normal_2)
                varr.append(vertex_2)
                
                varr.append(normal_3)
                varr.append(vertex_3)

                i += 1
                faceNum -= 1
                    
    for i in range(0, vertexCount):
        final_n_v = adjacent[i]
        V_n_size = np.sqrt(np.dot(final_n_v,final_n_v))
        fnv = final_n_v/V_n_size

        line_norm = (float(fnv[0]),float(fnv[1]),float(fnv[2]))
        norm.append(line_norm)

    h1VertexArray = np.array(varr, dtype = 'float32')
    h1VarrArray = np.array(vertex, dtype = 'float32')
    h1IndexArray = np.array(iarr, dtype = 'float32')
    h1NormArray = np.array(norm, dtype = 'float32')

    vertex = []
    normal = []
    varr = []
    norm = []
    iarr = []
    adjacent = []
    vertexCount = 0

    file_path_2 = open("./balloon_2.obj", 'r')

    for line in file_path_2:
        if line.startswith('#'):
            continue
        
        lines = line.split()
        lineNum = lines[1:]

        if not lines:
            continue
        
        if lines[0]=="v":
            tmp = (float(lines[1]), float(lines[2]), float(lines[3]))
            vertex.append(tmp)
            adjacent.append([.0])
            vertexCount += 1

        if lines[0]=="vn":
            tmp = (float(lines[1]), float(lines[2]), float(lines[3]))
            normal.append(tmp)

        if lines[0]=='f':
            search = lines[1].split('/')
            iarr_1 = int(search[0])
            vertex_1 = vertex[int(search[0])-1]
            normal_1 = normal[int(search[2])-1]
            varr.append(normal_1)
            varr.append(vertex_1)
            
            search = lines[2].split('/')
            iarr_2 = int(search[0])
            vertex_2 = vertex[int(search[0])-1]
            normal_2 = normal[int(search[2])-1]
            varr.append(normal_2)
            varr.append(vertex_2)
            
            search = lines[3].split('/')
            iarr_3 = int(search[0])
            vertex_3 = vertex[int(search[0])-1]
            normal_3 = normal[int(search[2])-1]
            varr.append(normal_3)
            varr.append(vertex_3)

            iarr.append((iarr_1 - 1, iarr_2 - 1, iarr_3 - 1))

            ver_1 = np.array(vertex_1)
            ver_2 = np.array(vertex_2)
            ver_3 = np.array(vertex_3)
            
            V2 = ver_2 - ver_1
            V3 = ver_3 - ver_1
            Vout = np.cross(V2, V3)
            Vsize = np.sqrt(np.dot(Vout, Vout))
            V_fn = Vout / Vsize

            line_vector = np.array([V_fn[0],V_fn[1],V_fn[2]])

            adjacent[iarr_1 - 1] += line_vector
            adjacent[iarr_2 - 1] += line_vector
            adjacent[iarr_3 - 1] += line_vector

            i = 3
            faceNum = len(lineNum)
            while ( faceNum > 3):
                search = lines[i].split('/')
                iarr_2 = int(search[0])
                vertex_2 = vertex[int(search[0])-1]
                normal_2 = normal[int(search[2])-1]
                
                search = lines[i+1].split('/')
                iarr_3 = int(search[0])
                vertex_3 = vertex[int(search[0])-1]
                normal_3 = normal[int(search[2])-1]

                iarr.append((iarr_1 - 1, iarr_2 - 1, iarr_3 - 1))

                ver_2 = np.array(vertex_2)
                ver_3 = np.array(vertex_3)
                
                V2 = ver_2 - ver_1
                V3 = ver_3 - ver_1
                Vout = np.cross(V2, V3)
                Vsize = np.sqrt(np.dot(Vout, Vout))
                V_fn = Vout / Vsize

                line_vector = np.array([V_fn[0],V_fn[1],V_fn[2]])
                
                adjacent[iarr_1 - 1] += line_vector
                adjacent[iarr_2 - 1] += line_vector
                adjacent[iarr_3 - 1] += line_vector

                varr.append(normal_1)
                varr.append(vertex_1)

                varr.append(normal_2)
                varr.append(vertex_2)
                
                varr.append(normal_3)
                varr.append(vertex_3)

                i += 1
                faceNum -= 1
                    
    for i in range(0, vertexCount):
        final_n_v = adjacent[i]
        V_n_size = np.sqrt(np.dot(final_n_v,final_n_v))
        fnv = final_n_v/V_n_size

        line_norm = (float(fnv[0]),float(fnv[1]),float(fnv[2]))
        norm.append(line_norm)

    h2VertexArray = np.array(varr, dtype = 'float32')
    h2VarrArray = np.array(vertex, dtype = 'float32')
    h2IndexArray = np.array(iarr, dtype = 'float32')
    h2NormArray = np.array(norm, dtype = 'float32')

    vertex = []
    normal = []
    varr = []
    norm = []
    iarr = []
    adjacent = []
    vertexCount = 0

    file_path_3 = open("./balloon_3.obj", 'r')

    for line in file_path_3:
        if line.startswith('#'):
            continue
        
        lines = line.split()
        lineNum = lines[1:]

        if not lines:
            continue
        
        if lines[0]=="v":
            tmp = (float(lines[1]), float(lines[2]), float(lines[3]))
            vertex.append(tmp)
            adjacent.append([.0])
            vertexCount += 1

        if lines[0]=="vn":
            tmp = (float(lines[1]), float(lines[2]), float(lines[3]))
            normal.append(tmp)

        if lines[0]=='f':
            search = lines[1].split('/')
            iarr_1 = int(search[0])
            vertex_1 = vertex[int(search[0])-1]
            normal_1 = normal[int(search[2])-1]
            varr.append(normal_1)
            varr.append(vertex_1)
            
            search = lines[2].split('/')
            iarr_2 = int(search[0])
            vertex_2 = vertex[int(search[0])-1]
            normal_2 = normal[int(search[2])-1]
            varr.append(normal_2)
            varr.append(vertex_2)
            
            search = lines[3].split('/')
            iarr_3 = int(search[0])
            vertex_3 = vertex[int(search[0])-1]
            normal_3 = normal[int(search[2])-1]
            varr.append(normal_3)
            varr.append(vertex_3)

            iarr.append((iarr_1 - 1, iarr_2 - 1, iarr_3 - 1))

            ver_1 = np.array(vertex_1)
            ver_2 = np.array(vertex_2)
            ver_3 = np.array(vertex_3)
            
            V2 = ver_2 - ver_1
            V3 = ver_3 - ver_1
            Vout = np.cross(V2, V3)
            Vsize = np.sqrt(np.dot(Vout, Vout))
            V_fn = Vout / Vsize

            line_vector = np.array([V_fn[0],V_fn[1],V_fn[2]])

            adjacent[iarr_1 - 1] += line_vector
            adjacent[iarr_2 - 1] += line_vector
            adjacent[iarr_3 - 1] += line_vector

            i = 3
            faceNum = len(lineNum)
            while ( faceNum > 3):
                search = lines[i].split('/')
                iarr_2 = int(search[0])
                vertex_2 = vertex[int(search[0])-1]
                normal_2 = normal[int(search[2])-1]
                
                search = lines[i+1].split('/')
                iarr_3 = int(search[0])
                vertex_3 = vertex[int(search[0])-1]
                normal_3 = normal[int(search[2])-1]

                iarr.append((iarr_1 - 1, iarr_2 - 1, iarr_3 - 1))

                ver_2 = np.array(vertex_2)
                ver_3 = np.array(vertex_3)
                
                V2 = ver_2 - ver_1
                V3 = ver_3 - ver_1
                Vout = np.cross(V2, V3)
                Vsize = np.sqrt(np.dot(Vout, Vout))
                V_fn = Vout / Vsize

                line_vector = np.array([V_fn[0],V_fn[1],V_fn[2]])
                
                adjacent[iarr_1 - 1] += line_vector
                adjacent[iarr_2 - 1] += line_vector
                adjacent[iarr_3 - 1] += line_vector

                varr.append(normal_1)
                varr.append(vertex_1)

                varr.append(normal_2)
                varr.append(vertex_2)
                
                varr.append(normal_3)
                varr.append(vertex_3)

                i += 1
                faceNum -= 1
                    
    for i in range(0, vertexCount):
        final_n_v = adjacent[i]
        V_n_size = np.sqrt(np.dot(final_n_v,final_n_v))
        fnv = final_n_v/V_n_size

        line_norm = (float(fnv[0]),float(fnv[1]),float(fnv[2]))
        norm.append(line_norm)

    h3VertexArray = np.array(varr, dtype = 'float32')
    h3VarrArray = np.array(vertex, dtype = 'float32')
    h3IndexArray = np.array(iarr, dtype = 'float32')
    h3NormArray = np.array(norm, dtype = 'float32')

def obj_drawh1():
    global h1VarrArray, h1IndexArray, h1NormArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 3*h1VarrArray.itemsize, h1NormArray)
    glVertexPointer(3, GL_FLOAT, 3*h1VarrArray.itemsize, h1VarrArray)
    glDrawElements(GL_TRIANGLES, h1IndexArray.size, GL_UNSIGNED_INT, h1IndexArray)
    
def obj_drawh2():
    global h2VarrArray, h2IndexArray, h2NormArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 3*h2VarrArray.itemsize, h2NormArray)
    glVertexPointer(3, GL_FLOAT, 3*h2VarrArray.itemsize, h2VarrArray)
    glDrawElements(GL_TRIANGLES, h2IndexArray.size, GL_UNSIGNED_INT, h2IndexArray)
    
def obj_drawh3():
    global h3VarrArray, h3IndexArray, h3NormArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 3*h3VarrArray.itemsize, h3NormArray)
    glVertexPointer(3, GL_FLOAT, 3*h3VarrArray.itemsize, h3VarrArray)
    glDrawElements(GL_TRIANGLES, h3IndexArray.size, GL_UNSIGNED_INT, h3IndexArray)
    
def obj_glDrawElements():
    global gVarrArray, gIndexArray, gNormArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 3*gVarrArray.itemsize, gNormArray)
    glVertexPointer(3, GL_FLOAT, 3*gVarrArray.itemsize, gVarrArray)
    glDrawElements(GL_TRIANGLES, gIndexArray.size, GL_UNSIGNED_INT, gIndexArray)

def drop_callback(window, paths):
    global gVertexArray, gVarrArray, gIndexArray, gNormArray

    vertex = []
    normal = []
    varr = []
    norm = []
    iarr = []
    adjacent = []
    face3 = 0
    face4 = 0
    faceN = 0
    vertexCount = 0

    file_path = open(" ".join(paths), 'r')

    for line in file_path:
        if line.startswith('#'):
            continue
        
        lines = line.split()
        lineNum = lines[1:]

        if not lines:
            continue
        
        if lines[0]=='v':
            tmp = (float(lines[1]), float(lines[2]), float(lines[3]))
            vertex.append(tmp)
            adjacent.append([.0])
            vertexCount += 1

        if lines[0]=='vn':
            tmp = (float(lines[1]), float(lines[2]), float(lines[3]))
            normal.append(tmp)

        if lines[0]=='f':
            if len(lineNum)==3:
                face3 += 1
            elif len(lineNum)==4:
                face4 +=1
            elif len(lineNum) > 4:
                faceN += 1

            search = lines[1].split('/')
            iarr_1 = int(search[0])
            vertex_1 = vertex[int(search[0])-1]
            normal_1 = normal[int(search[2])-1]
            varr.append(normal_1)
            varr.append(vertex_1)
            
            search = lines[2].split('/')
            iarr_2 = int(search[0])
            vertex_2 = vertex[int(search[0])-1]
            normal_2 = normal[int(search[2])-1]
            varr.append(normal_2)
            varr.append(vertex_2)
            
            search = lines[3].split('/')
            iarr_3 = int(search[0])
            vertex_3 = vertex[int(search[0])-1]
            normal_3 = normal[int(search[2])-1]
            varr.append(normal_3)
            varr.append(vertex_3)

            iarr.append((iarr_1 - 1, iarr_2 - 1, iarr_3 - 1))

            ver_1 = np.array(vertex_1)
            ver_2 = np.array(vertex_2)
            ver_3 = np.array(vertex_3)
            
            V2 = ver_2 - ver_1
            V3 = ver_3 - ver_1
            Vout = np.cross(V2, V3)
            Vsize = np.sqrt(np.dot(Vout, Vout))
            V_fn = Vout / Vsize

            line_vector = np.array([V_fn[0],V_fn[1],V_fn[2]])

            adjacent[iarr_1 - 1] += line_vector
            adjacent[iarr_2 - 1] += line_vector
            adjacent[iarr_3 - 1] += line_vector

            i = 3
            faceNum = len(lineNum)
            while ( faceNum > 3):
                search = lines[i].split('/')
                iarr_2 = int(search[0])
                vertex_2 = vertex[int(search[0])-1]
                normal_2 = normal[int(search[2])-1]
                
                search = lines[i+1].split('/')
                iarr_3 = int(search[0])
                vertex_3 = vertex[int(search[0])-1]
                normal_3 = normal[int(search[2])-1]

                iarr.append((iarr_1 - 1, iarr_2 - 1, iarr_3 - 1))

                ver_2 = np.array(vertex_2)
                ver_3 = np.array(vertex_3)
                
                V2 = ver_2 - ver_1
                V3 = ver_3 - ver_1
                Vout = np.cross(V2, V3)
                Vsize = np.sqrt(np.dot(Vout, Vout))
                V_fn = Vout / Vsize

                line_vector = np.array([V_fn[0],V_fn[1],V_fn[2]])
                
                adjacent[iarr_1 - 1] += line_vector
                adjacent[iarr_2 - 1] += line_vector
                adjacent[iarr_3 - 1] += line_vector

                varr.append(normal_1)
                varr.append(vertex_1)

                varr.append(normal_2)
                varr.append(vertex_2)
                
                varr.append(normal_3)
                varr.append(vertex_3)

                i += 1
                faceNum -= 1
                    
    for i in range(0, vertexCount):
        final_n_v = adjacent[i]
        V_n_size = np.sqrt(np.dot(final_n_v,final_n_v))
        fnv = final_n_v/V_n_size

        line_norm = (float(fnv[0]),float(fnv[1]),float(fnv[2]))
        norm.append(line_norm)

    gVertexArray = np.array(varr, dtype = 'float32')
    gVarrArray = np.array(vertex, dtype = 'float32')
    gIndexArray = np.array(iarr, dtype = 'float32')
    gNormArray = np.array(norm, dtype = 'float32')
    
    print("file name : " + str(paths))
    print("total number of faces : " +str(face3 + face4 + faceN))
    print("number of faces with 3 vertices : " + str(face3))
    print("number of faces with 4 vertices : " + str(face4))
    print("number of faces with more than 4 vertices : " + str(faceN))
    
def key_callback(window, key, scancode, action, mods):#toggle projection
    global projection_key, Z_key, h_mode
    
    if action==glfw.PRESS:
        if key==glfw.KEY_V:
            if projection_key==0:
                projection_key = 1
            else:
                projection_key = 0
                
        if key==glfw.KEY_H:
            h_mode = 1

        if key==glfw.KEY_Z:
            if Z_key==0:
                Z_key = 1
            else:
                Z_key = 0                

def main():
    if not glfw.init():
        return

    window = glfw.create_window(800,800,"assignment_2",None,None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    obj_ReadModels()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()
    
if __name__=="__main__":
    main()
