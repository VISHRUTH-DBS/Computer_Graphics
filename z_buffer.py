# z_buffer.py
# Lab 6 - Experiment 6
# Hidden Surface Removal using the Z-Buffer Algorithm
#
# Keys: 1 = triangle 1 only
#       2 = triangle 2 only
#       a = both, RED drawn first
#       b = both, BLUE drawn first
#       z = visualise the z-buffer as a greyscale depth map
#       q = quit

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

WIDTH, HEIGHT = 300, 300
BACKGROUND = (255, 255, 255)
NEAR_Z, FAR_Z = 0.0, 1.0

mode = "a"

# Two triangles that cross in depth
TRI1 = (
    (40.0, 150.0, 0.2),
    (260.0, 80.0, 0.8),
    (260.0, 220.0, 0.8)
)  # Red

TRI2 = (
    (40.0, 80.0, 0.8),
    (40.0, 220.0, 0.8),
    (260.0, 150.0, 0.2)
)  # Blue

RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Edge function: twice the signed area of triangle (a, b, p)
def edge(ax, ay, bx, by, px, py):
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def make_buffers():
    framebuffer = [
        [BACKGROUND for _ in range(HEIGHT)]
        for _ in range(WIDTH)
    ]

    zbuffer = [
        [float("inf") for _ in range(HEIGHT)]
        for _ in range(WIDTH)
    ]

    return framebuffer, zbuffer


# Z-Buffer algorithm applied to one triangle
def rasterize_triangle(v0, v1, v2, color, framebuffer, zbuffer):
    (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = v0, v1, v2

    xmin = max(int(min(x0, x1, x2)), 0)
    xmax = min(int(max(x0, x1, x2)), WIDTH - 1)
    ymin = max(int(min(y0, y1, y2)), 0)
    ymax = min(int(max(y0, y1, y2)), HEIGHT - 1)

    denom = edge(x0, y0, x1, y1, x2, y2)

    if denom == 0:
        return  # Degenerate triangle: zero area

    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            px, py = x + 0.5, y + 0.5

            w0 = edge(x1, y1, x2, y2, px, py)
            w1 = edge(x2, y2, x0, y0, px, py)
            w2 = edge(x0, y0, x1, y1, px, py)

            inside = (
                (w0 >= 0 and w1 >= 0 and w2 >= 0)
                or
                (w0 <= 0 and w1 <= 0 and w2 <= 0)
            )

            if not inside:
                continue

            b0, b1, b2 = w0 / denom, w1 / denom, w2 / denom

            # Interpolate depth at this pixel
            z = b0 * z0 + b1 * z1 + b2 * z2

            # Keep the nearer pixel
            if z < zbuffer[x][y]:
                zbuffer[x][y] = z
                framebuffer[x][y] = color


def render(order):
    """Render triangles in the specified drawing order."""
    framebuffer, zbuffer = make_buffers()

    for (v0, v1, v2), color in order:
        rasterize_triangle(
            v0, v1, v2, color, framebuffer, zbuffer
        )

    return framebuffer, zbuffer


def zbuffer_to_greyscale(zbuffer):
    framebuffer = [
        [BACKGROUND for _ in range(HEIGHT)]
        for _ in range(WIDTH)
    ]

    for x in range(WIDTH):
        for y in range(HEIGHT):
            z = zbuffer[x][y]

            if z == float("inf"):
                continue

            # 0 = nearest, 1 = farthest
            t = (z - NEAR_Z) / (FAR_Z - NEAR_Z)

            # Nearer pixels appear brighter
            grey = int(255 * (1.0 - t))

            framebuffer[x][y] = (grey, grey, grey)

    return framebuffer


# Upload framebuffer pixels to the screen
def draw_framebuffer(framebuffer):
    pixels = bytearray(WIDTH * HEIGHT * 3)
    i = 0

    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = framebuffer[x][y]

            pixels[i] = r
            pixels[i + 1] = g
            pixels[i + 2] = b

            i += 3

    glDrawPixels(
        WIDTH,
        HEIGHT,
        GL_RGB,
        GL_UNSIGNED_BYTE,
        bytes(pixels)
    )


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glRasterPos2i(0, 0)

    if mode == "1":
        fb, _ = render([(TRI1, RED)])

    elif mode == "2":
        fb, _ = render([(TRI2, BLUE)])

    elif mode == "a":
        fb, _ = render([
            (TRI1, RED),
            (TRI2, BLUE)
        ])

    elif mode == "b":
        fb, _ = render([
            (TRI2, BLUE),
            (TRI1, RED)
        ])

    elif mode == "z":
        _, zb = render([
            (TRI1, RED),
            (TRI2, BLUE)
        ])

        fb = zbuffer_to_greyscale(zb)

    draw_framebuffer(fb)
    glutSwapBuffers()


def keyboard(key, x, y):
    global mode

    ch = key.decode("utf-8").lower()

    if ch == "q":
        sys.exit(0)

    if ch in "12abz":
        mode = ch
        glutPostRedisplay()


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(0, WIDTH, 0, HEIGHT)


def main():
    glutInit(sys.argv)

    glutInitDisplayMode(
        GLUT_DOUBLE | GLUT_RGB
    )

    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(100, 100)

    glutCreateWindow(
        b"Hidden Surface Removal using the Z-Buffer Algorithm"
    )

    init()

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)

    glutMainLoop()


if __name__ == "__main__":
    main()
