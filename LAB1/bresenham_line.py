# bresenham_line.py
# Lab 1 - Experiment 2
# Bresenham's Line Drawing Algorithm using Python and PyOpenGL

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()


def bresenham_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    x = x1
    y = y1

    if dx > dy:
        # Gentle slope: x is the driving axis
        p = 2 * dy - dx

        for _ in range(dx + 1):
            draw_pixel(x, y)
            x += sx

            if p < 0:
                p += 2 * dy
            else:
                y += sy
                p += 2 * dy - 2 * dx

    else:
        # Steep slope: y is the driving axis
        p = 2 * dx - dy

        for _ in range(dy + 1):
            draw_pixel(x, y)
            y += sy

            if p < 0:
                p += 2 * dx
            else:
                x += sx
                p += 2 * dx - 2 * dy

    glFlush()


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(0.0, 0.0, 1.0)

    bresenham_line(100, 100, 400, 300)

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
        b"Bresenham Line Drawing Algorithm - Python"
    )

    init()

    glutDisplayFunc(display)

    glutMainLoop()


if __name__ == "__main__":
    main()