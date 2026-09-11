# midpoint_circle.py
# Lab 2 - Experiment 1
# Midpoint Circle Drawing Algorithm using Python and PyOpenGL

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()


def plot_eight_points(xc, yc, x, y):
    """Plot the eight symmetric points of a circle centred at (xc, yc)."""

    draw_pixel(xc + x, yc + y)  # Octant 1
    draw_pixel(xc - x, yc + y)  # Octant 4
    draw_pixel(xc + x, yc - y)  # Octant 8
    draw_pixel(xc - x, yc - y)  # Octant 5

    draw_pixel(xc + y, yc + x)  # Octant 2
    draw_pixel(xc - y, yc + x)  # Octant 3
    draw_pixel(xc + y, yc - x)  # Octant 7
    draw_pixel(xc - y, yc - x)  # Octant 6


def midpoint_circle(xc, yc, r):
    x = 0
    y = r
    p = 1 - r

    plot_eight_points(xc, yc, x, y)

    while x < y:
        x += 1

        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * x - 2 * y + 1

        plot_eight_points(xc, yc, x, y)

    glFlush()


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0, 0.5, 0.0)

    midpoint_circle(250, 250, 150)

    glFlush()


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(3.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(0, 500, 0, 500)


def main():
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)

    glutCreateWindow(
        b"Midpoint Circle Drawing Algorithm - Python"
    )

    init()

    glutDisplayFunc(display)

    glutMainLoop()


if __name__ == "__main__":
    main()