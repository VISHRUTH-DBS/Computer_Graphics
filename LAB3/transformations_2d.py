# transformations_2d.py
# Lab 2 - Experiment 2
# 2D Transformations using Homogeneous Coordinates
#
# Keys:
# o = original only
# t = translation
# r = rotation
# s = scaling
# f = reflection
# h = shearing
# c = composite (rotation about a pivot)
# a = show all
# q = quit

import sys
import math

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


# ----------------------------------------------------------------------
# The object to be transformed: a triangle, as homogeneous points
# Each point is [x, y, 1]
# ----------------------------------------------------------------------

TRIANGLE = [
    [40.0, 20.0, 1.0],
    [120.0, 20.0, 1.0],
    [80.0, 100.0, 1.0],
]

mode = "a"


# ----------------------------------------------------------------------
# Matrix helpers
# ----------------------------------------------------------------------

def identity():
    """Return the 3x3 identity matrix."""
    return [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]


def mat_mul(a, b):
    """Multiply two 3x3 matrices and return a * b."""
    result = [[0.0] * 3 for _ in range(3)]

    for i in range(3):
        for j in range(3):
            total = 0.0

            for k in range(3):
                total += a[i][k] * b[k][j]

            result[i][j] = total

    return result


def apply_matrix(m, points):
    """Apply a 3x3 matrix to a list of homogeneous points."""
    transformed = []

    for p in points:
        x = (
            m[0][0] * p[0]
            + m[0][1] * p[1]
            + m[0][2] * p[2]
        )

        y = (
            m[1][0] * p[0]
            + m[1][1] * p[1]
            + m[1][2] * p[2]
        )

        w = (
            m[2][0] * p[0]
            + m[2][1] * p[1]
            + m[2][2] * p[2]
        )

        transformed.append([x, y, w])

    return transformed


# ----------------------------------------------------------------------
# Transformation matrices
# ----------------------------------------------------------------------

def translation_matrix(tx, ty):
    return [
        [1.0, 0.0, tx],
        [0.0, 1.0, ty],
        [0.0, 0.0, 1.0]
    ]


def rotation_matrix(angle_degrees):
    theta = math.radians(angle_degrees)

    c = math.cos(theta)
    s = math.sin(theta)

    return [
        [c, -s, 0.0],
        [s, c, 0.0],
        [0.0, 0.0, 1.0]
    ]


def scaling_matrix(sx, sy):
    return [
        [sx, 0.0, 0.0],
        [0.0, sy, 0.0],
        [0.0, 0.0, 1.0]
    ]


def reflection_matrix(axis):
    """
    axis:
    x      = reflection about X-axis
    y      = reflection about Y-axis
    origin = reflection about origin
    yx     = reflection about y = x
    """

    if axis == "x":
        return [
            [1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1.0]
        ]

    if axis == "y":
        return [
            [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0]
        ]

    if axis == "origin":
        return [
            [-1.0, 0.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1.0]
        ]

    if axis == "yx":
        return [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0]
        ]

    return identity()


def shear_matrix(shx, shy):
    return [
        [1.0, shx, 0.0],
        [shy, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]


def rotation_about_point(angle_degrees, px, py):
    """
    Rotate an object about a pivot point.

    Steps:
    1. Translate pivot to origin.
    2. Rotate.
    3. Translate back.
    """

    to_origin = translation_matrix(-px, -py)
    rotate = rotation_matrix(angle_degrees)
    back = translation_matrix(px, py)

    return mat_mul(
        back,
        mat_mul(rotate, to_origin)
    )


# ----------------------------------------------------------------------
# Drawing helpers
# ----------------------------------------------------------------------

def draw_polygon(points, r, g, b, filled=False):
    glColor3f(r, g, b)

    if filled:
        glBegin(GL_POLYGON)
    else:
        glBegin(GL_LINE_LOOP)

    for p in points:
        glVertex2f(p[0], p[1])

    glEnd()


def draw_axes():
    glColor3f(0.7, 0.7, 0.7)

    glBegin(GL_LINES)

    # X-axis
    glVertex2f(-250.0, 0.0)
    glVertex2f(250.0, 0.0)

    # Y-axis
    glVertex2f(0.0, -250.0)
    glVertex2f(0.0, 250.0)

    glEnd()


def draw_text(x, y, text):
    glRasterPos2f(x, y)

    for ch in text:
        glutBitmapCharacter(
            GLUT_BITMAP_HELVETICA_12,
            ord(ch)
        )


# ----------------------------------------------------------------------
# Display callback
# ----------------------------------------------------------------------

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    draw_axes()

    # Original triangle
    draw_polygon(
        TRIANGLE,
        0.4,
        0.4,
        0.4
    )

    # Translation
    if mode in ("t", "a"):
        m = translation_matrix(-150.0, 60.0)

        draw_polygon(
            apply_matrix(m, TRIANGLE),
            0.0,
            0.0,
            1.0
        )

    # Rotation
    if mode in ("r", "a"):
        m = rotation_matrix(90.0)

        draw_polygon(
            apply_matrix(m, TRIANGLE),
            1.0,
            0.0,
            0.0
        )

    # Scaling
    if mode in ("s", "a"):
        m = scaling_matrix(1.5, 1.5)

        draw_polygon(
            apply_matrix(m, TRIANGLE),
            0.0,
            0.6,
            0.0
        )

    # Reflection
    if mode in ("f", "a"):
        m = reflection_matrix("x")

        draw_polygon(
            apply_matrix(m, TRIANGLE),
            0.8,
            0.0,
            0.8
        )

    # Shearing
    if mode in ("h", "a"):
        m = shear_matrix(1.0, 0.0)

        draw_polygon(
            apply_matrix(m, TRIANGLE),
            1.0,
            0.5,
            0.0
        )

    # Composite transformation
    if mode == "c":
        m = rotation_about_point(
            45.0,
            80.0,
            60.0
        )

        draw_polygon(
            apply_matrix(m, TRIANGLE),
            0.0,
            0.5,
            0.8
        )

    # Display instructions
    glColor3f(0.0, 0.0, 0.0)

    draw_text(
        -240.0,
        230.0,
        "o original  t translate  r rotate  s scale"
    )

    draw_text(
        -240.0,
        214.0,
        "f reflect  h shear  c composite  a all  q quit"
    )

    draw_text(
        -240.0,
        -240.0,
        "current mode: " + mode
    )

    glutSwapBuffers()


# ----------------------------------------------------------------------
# Keyboard callback
# ----------------------------------------------------------------------

def keyboard(key, x, y):
    global mode

    ch = key.decode("utf-8").lower()

    if ch == "q":
        sys.exit(0)

    if ch in ("o", "t", "r", "s", "f", "h", "c", "a"):
        mode = ch
        glutPostRedisplay()


# ----------------------------------------------------------------------
# OpenGL initialization
# ----------------------------------------------------------------------

def init():
    glClearColor(
        1.0,
        1.0,
        1.0,
        1.0
    )

    glLineWidth(2.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(
        -250.0,
        250.0,
        -250.0,
        250.0
    )


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------

def main():
    glutInit(sys.argv)

    glutInitDisplayMode(
        GLUT_DOUBLE | GLUT_RGB
    )

    glutInitWindowSize(
        600,
        600
    )

    glutInitWindowPosition(
        100,
        100
    )

    glutCreateWindow(
        b"2D Transformations using Homogeneous Coordinates"
    )

    init()

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)

    glutMainLoop()


# ----------------------------------------------------------------------
# Program entry point
# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
