# composite_transformations.py
# Lab 4 - Experiment 4
# Composite Transformations using Matrix Representation
#
# Keys: o = original only
# r = rotation about an arbitrary pivot
# s = scaling about a fixed point
# l = reflection about an arbitrary line y = mx + c
# d = order demonstration (T then S vs S then T)
# m = multi-step composite sequence
# i = inverse composite (transform, then undo it)
# a = show all
# q = quit

import sys
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# ----------------------------------------------------------------------
# The object: a house-shaped polygon, so orientation stays visible
# Each vertex is a homogeneous point [x, y, 1]
# ----------------------------------------------------------------------
HOUSE = [
    [20.0, 20.0, 1.0],
    [100.0, 20.0, 1.0],
    [100.0, 80.0, 1.0],
    [60.0, 120.0, 1.0],
    [20.0, 80.0, 1.0],
]
mode = "a"
PIVOT_X = 60.0
PIVOT_Y = 70.0

# ----------------------------------------------------------------------
# Core matrix operations
# ----------------------------------------------------------------------
def identity():
    return [[1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]]

def mat_mul(a, b):
    """Return the matrix product a * b."""
    result = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            total = 0.0
            for k in range(3):
                total += a[i][k] * b[k][j]
            result[i][j] = total
    return result

def compose(*matrices):
    """Concatenate any number of matrices into one.
    compose(A, B, C) returns A * B * C, so C is applied FIRST
    and A is applied LAST.
    """
    result = identity()
    for m in matrices:
        result = mat_mul(result, m)
    return result

def apply_matrix(m, points):
    transformed = []
    for p in points:
        x = m[0][0] * p[0] + m[0][1] * p[1] + m[0][2] * p[2]
        y = m[1][0] * p[0] + m[1][1] * p[1] + m[1][2] * p[2]
        w = m[2][0] * p[0] + m[2][1] * p[1] + m[2][2] * p[2]
        transformed.append([x, y, w])
    return transformed

# ----------------------------------------------------------------------
# Basic transformation matrices
# ----------------------------------------------------------------------
def translate(tx, ty):
    return [[1.0, 0.0, tx],
            [0.0, 1.0, ty],
            [0.0, 0.0, 1.0]]

def rotate(angle_degrees):
    t = math.radians(angle_degrees)
    c = math.cos(t)
    s = math.sin(t)
    return [[c, -s, 0.0],
            [s, c, 0.0],
            [0.0, 0.0, 1.0]]

def scale(sx, sy):
    return [[sx, 0.0, 0.0],
            [0.0, sy, 0.0],
            [0.0, 0.0, 1.0]]

def reflect_x():
    return [[1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1.0]]

# ----------------------------------------------------------------------
# Composite transformations
# ----------------------------------------------------------------------
def rotate_about_point(angle_degrees, px, py):
    """Rotate about (px, py): move pivot to origin, rotate, move back."""
    return compose(translate(px, py),
                   rotate(angle_degrees),
                   translate(-px, -py))

def scale_about_point(sx, sy, px, py):
    """Scale about the fixed point (px, py)."""
    return compose(translate(px, py),
                   scale(sx, sy),
                   translate(-px, -py))

def reflect_about_line(slope, intercept):
    """Reflect about the line y = slope*x + intercept.
    Five steps, applied right to left:
    1. translate the line down so it passes through the origin
    2. rotate the line onto the x-axis
    3. reflect about the x-axis
    4. rotate back
    5. translate back
    """
    angle = math.degrees(math.atan(slope))
    return compose(translate(0.0, intercept),
                   rotate(angle),
                   reflect_x(),
                   rotate(-angle),
                   translate(0.0, -intercept))

def inverse_of_composite(angle_degrees, px, py, sx, sy):
    """Inverse of scale_about_point(sx, sy) . rotate_about_point(angle).
    The inverse of a product reverses the order and inverts each factor:
    (A . B) inverse = (B inverse) . (A inverse)
    """
    return compose(rotate_about_point(-angle_degrees, px, py),
                   scale_about_point(1.0 / sx, 1.0 / sy, px, py))

# ----------------------------------------------------------------------
# Drawing helpers
# ----------------------------------------------------------------------
def draw_polygon(points, r, g, b, width=2.0):
    glColor3f(r, g, b)
    glLineWidth(width)
    glBegin(GL_LINE_LOOP)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()

def draw_axes():
    glColor3f(0.75, 0.75, 0.75)
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glVertex2f(-250.0, 0.0)
    glVertex2f(250.0, 0.0)
    glVertex2f(0.0, -250.0)
    glVertex2f(0.0, 250.0)
    glEnd()

def draw_line(x1, y1, x2, y2, r, g, b):
    glColor3f(r, g, b)
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def draw_marker(x, y, r, g, b):
    """Draw a small cross marking a pivot or fixed point."""
    glColor3f(r, g, b)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(x - 6.0, y)
    glVertex2f(x + 6.0, y)
    glVertex2f(x, y - 6.0)
    glVertex2f(x, y + 6.0)
    glEnd()

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))

# ----------------------------------------------------------------------
# Display callback
# ----------------------------------------------------------------------
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_axes()
    
    # The original object is shown in grey in every mode
    draw_polygon(HOUSE, 0.45, 0.45, 0.45)
    
    if mode in ("r", "a"):
        m = rotate_about_point(60.0, PIVOT_X, PIVOT_Y)
        draw_polygon(apply_matrix(m, HOUSE), 1.0, 0.0, 0.0)
        draw_marker(PIVOT_X, PIVOT_Y, 1.0, 0.0, 0.0)
        
    if mode in ("s", "a"):
        m = scale_about_point(0.6, 0.6, PIVOT_X, PIVOT_Y)
        draw_polygon(apply_matrix(m, HOUSE), 0.0, 0.6, 0.0)
        draw_marker(PIVOT_X, PIVOT_Y, 0.0, 0.6, 0.0)
        
    if mode in ("l", "a"):
        slope, intercept = 1.0, -40.0
        m = reflect_about_line(slope, intercept)
        draw_polygon(apply_matrix(m, HOUSE), 0.8, 0.0, 0.8)
        draw_line(-250.0, slope * -250.0 + intercept,
                  250.0, slope * 250.0 + intercept, 0.8, 0.0, 0.8)
                  
    if mode == "d":
        # translate first, then scale
        m1 = compose(scale(1.5, 1.5), translate(60.0, 40.0))
        draw_polygon(apply_matrix(m1, HOUSE), 1.0, 0.0, 0.0)
        # scale first, then translate
        m2 = compose(translate(60.0, 40.0), scale(1.5, 1.5))
        draw_polygon(apply_matrix(m2, HOUSE), 0.0, 0.0, 1.0)
        draw_text(-240.0, 190.0, "red: S.T (translate first) blue: T.S (scale first)")
        
    if mode == "m":
        # a four-step sequence folded into ONE matrix
        m = compose(translate(-120.0, 40.0),
                    rotate(30.0),
                    scale(0.8, 0.8),
                    translate(-60.0, -70.0))
        draw_polygon(apply_matrix(m, HOUSE), 0.0, 0.4, 0.8)
        draw_text(-240.0, 190.0, "one matrix = translate . rotate . scale . translate")
        
    if mode == "i":
        forward = compose(scale_about_point(1.4, 1.4, PIVOT_X, PIVOT_Y),
                          rotate_about_point(50.0, PIVOT_X, PIVOT_Y))
        draw_polygon(apply_matrix(forward, HOUSE), 1.0, 0.5, 0.0)
        # applying the inverse must return the object exactly to the original
        back = inverse_of_composite(50.0, PIVOT_X, PIVOT_Y, 1.4, 1.4)
        restored = apply_matrix(compose(back, forward), HOUSE)
        draw_polygon(restored, 0.0, 0.0, 1.0, width=4.0)
        draw_text(-240.0, 190.0, "orange: transformed blue: inverse applied, back over grey")
        
    glColor3f(0.0, 0.0, 0.0)
    draw_text(-240.0, 230.0, "o original r rotate-about-pivot s scale-about-point")
    draw_text(-240.0, 214.0, "l reflect-about-line d order m multi-step i inverse a all")
    draw_text(-240.0, -240.0, "current mode: " + mode)
    glutSwapBuffers()

def keyboard(key, x, y):
    global mode
    ch = key.decode("utf-8").lower()
    if ch == "q":
        sys.exit(0)
    if ch in ("o", "r", "s", "l", "d", "m", "i", "a"):
        mode = ch
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
    glutCreateWindow(b"Composite Transformations using Matrix Representation")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == "__main__":
    main()
