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
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def drawPlane():
    glBegin(GL_LINES)
    glColor3ub(255,212,0)
    for i in range(-10,11):
        glVertex3fv(np.array([i,0,-10]))
        glVertex3fv(np.array([i,0,10]))
        glVertex3fv(np.array([-10,0,i]))
        glVertex3fv(np.array([10,0,i]))        
    glEnd()
    
def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)
 
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()
    
def render():
    global zoom, width, height, M, projection_key
    
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

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
    glColor3ub(255,255,255)
    drawCube()
    
def key_callback(window, key, scancode, action, mods):#toggle projection
    global projection_key
    
    if ((action==glfw.PRESS) and (key==glfw.KEY_V)):
        if(projection_key==0):
            projection_key = 1
        else:
            projection_key = 0
            
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
    
    if(zoom > yoffset):
        zoom -= yoffset
    
    
def main():
    if not glfw.init():
        return

    window = glfw.create_window(800,800,"assignment_1",None,None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__=="__main__":
    main()
