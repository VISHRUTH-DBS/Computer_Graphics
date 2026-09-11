# cohen_sutherland.py
# Lab 5 - Experiment 5
# Line Clipping using the Cohen-Sutherland Algorithm
#
# Keys: 1-6 = show a single test line
#       a   = show all test lines
#       c   = toggle the clip window outline
#       q   = quit

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# -----------------------------------------------------------------
# The clipping window
# -----------------------------------------------------------------
XMIN, YMIN, XMAX, YMAX = -100.0, -100.0, 100.0, 100.0

# -----------------------------------------------------------------
# Region (outcode) bit definitions
# -----------------------------------------------------------------
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

mode = "a"
show_window = True

# -----------------------------------------------------------------
# Test lines: (x1, y1, x2, y2), chosen to exercise every case
# -----------------------------------------------------------------
LINES = [
    (-150.0, 50.0, -120.0, 80.0),    # 1: fully outside - trivial reject
    (-50.0, -30.0, 50.0, 40.0),      # 2: fully inside - trivial accept
    (-150.0, 0.0, 150.0, 0.0),       # 3: crosses left and right edges
    (-150.0, -150.0, 150.0, 150.0),  # 4: diagonal, crosses two corners
    (60.0, -150.0, 60.0, 150.0),     # 5: crosses top and bottom edges
    (-150.0, 120.0, 150.0, 80.0)     # 6: needs TWO clips (top, then right)
]


# -----------------------------------------------------------------
# Computing the outcode of a point
# -----------------------------------------------------------------
def compute_outcode(x, y):
    code = INSIDE
    if x < XMIN:
        code |= LEFT
    elif x > XMAX:
        code |= RIGHT
        
    if y < YMIN:
        code |= BOTTOM
    elif y > YMAX:
        code |= TOP
    return code


# -----------------------------------------------------------------
# The Cohen-Sutherland clipping algorithm
# -----------------------------------------------------------------
def cohen_sutherland_clip(x1, y1, x2, y2):
    """Clip the segment (x1,y1)-(x2,y2) against the window.
    Returns (accept, x1, y1, x2, y2).
    When accept is False the segment is entirely outside the window
    and must not be drawn.
    """
    outcode1 = compute_outcode(x1, y1)
    outcode2 = compute_outcode(x2, y2)
    accept = False
    
    while True:
        if outcode1 == 0 and outcode2 == 0:
            # Both endpoints inside: trivial accept
            accept = True
            break
        elif (outcode1 & outcode2) != 0:
            # Both endpoints share an outside region: trivial reject
            break
        else:
            # At least one endpoint is outside; clip against one edge
            x = y = 0.0
            outcode_out = outcode1 if outcode1 != 0 else outcode2
            
            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (YMAX - y1) / (y2 - y1)
                y = YMAX
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (YMIN - y1) / (y2 - y1)
                y = YMIN
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (XMAX - x1) / (x2 - x1)
                x = XMAX
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (XMIN - x1) / (x2 - x1)
                x = XMIN
                
            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2)
                
    return accept, x1, y1, x2, y2


# -----------------------------------------------------------------
# Drawing helpers
# -----------------------------------------------------------------
def draw_axes():
    glColor3f(0.85, 0.85, 0.85)
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glVertex2f(-250.0, 0.0); glVertex2f(250.0, 0.0)
    glVertex2f(0.0, -250.0); glVertex2f(0.0, 250.0)
    glEnd()


def draw_clip_window():
    glColor3f(0.0, 0.4, 0.9)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(XMIN, YMIN)
    glVertex2f(XMAX, YMIN)
    glVertex2f(XMAX, YMAX)
    glVertex2f(XMIN, YMAX)
    glEnd()


def draw_segment(x1, y1, x2, y2, r, g, b, width=1.5):
    glColor3f(r, g, b)
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))


def draw_one_line(index, x1, y1, x2, y2):
    # Original segment, always shown, thin grey
    draw_segment(x1, y1, x2, y2, 0.55, 0.55, 0.55, width=1.0)
    
    accept, cx1, cy1, cx2, cy2 = cohen_sutherland_clip(x1, y1, x2, y2)
    if accept:
        draw_segment(cx1, cy1, cx2, cy2, 1.0, 0.0, 0.0, width=3.0)
        label = f"{index}: kept ({cx1:.1f},{cy1:.1f})-({cx2:.1f},{cy2:.1f})"
    else:
        label = f"{index}: rejected (fully outside)"
    draw_text(x2 + 4.0, y2 + 4.0, label)


# -----------------------------------------------------------------
# Display callback
# -----------------------------------------------------------------
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_axes()
    
    if show_window:
        draw_clip_window()
        
    if mode == "a":
        for i, (x1, y1, x2, y2) in enumerate(LINES, 1):
            draw_one_line(i, x1, y1, x2, y2)
    elif mode in "123456":
        i = int(mode)
        x1, y1, x2, y2 = LINES[i - 1]
        draw_one_line(i, x1, y1, x2, y2)
        
    glColor3f(0.0, 0.0, 0.0)
    draw_text(-240.0, 230.0, "1-6 single line   a all lines   c toggle window   q quit")
    draw_text(-240.0, -240.0, "current mode: " + mode)
    glutSwapBuffers()


def keyboard(key, x, y):
    global mode, show_window
    ch = key.decode("utf-8").lower()
    
    if ch == "q":
        sys.exit(0)
    if ch in "123456a":
        mode = ch
    if ch == "c":
        show_window = not show_window
        
    glutPostRedisplay()


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-250.0, 250.0, -250.0, 250.0)


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Line Clipping using the Cohen-Sutherland Algorithm")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMainLoop()


if __name__ == "__main__":
    main()
