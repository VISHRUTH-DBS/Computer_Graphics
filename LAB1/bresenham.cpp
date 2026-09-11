#include <GL/freeglut.h>
#include <cstdlib>
#include <iostream>

using namespace std;

void drawPixel(int x, int y)
{
    glBegin(GL_POINTS);
    glVertex2i(x, y);
    glEnd();
}

void bresenhamLine(int x1, int y1, int x2, int y2)
{
    int dx = abs(x2 - x1);
    int dy = abs(y2 - y1);

    int sx = (x1 < x2) ? 1 : -1;
    int sy = (y1 < y2) ? 1 : -1;

    int x = x1;
    int y = y1;

    if (dx > dy)
    {
        // Gentle slope: x is the driving axis
        int p = 2 * dy - dx;

        for (int i = 0; i <= dx; i++)
        {
            drawPixel(x, y);

            x += sx;

            if (p < 0)
            {
                p += 2 * dy;
            }
            else
            {
                y += sy;
                p += 2 * dy - 2 * dx;
            }
        }
    }
    else
    {
        // Steep slope: y is the driving axis
        int p = 2 * dx - dy;

        for (int i = 0; i <= dy; i++)
        {
            drawPixel(x, y);

            y += sy;

            if (p < 0)
            {
                p += 2 * dx;
            }
            else
            {
                x += sx;
                p += 2 * dx - 2 * dy;
            }
        }
    }

    glFlush();
}

void display()
{
    glClear(GL_COLOR_BUFFER_BIT);

    // Blue color
    glColor3f(0.0, 0.0, 1.0);

    // Draw line from (100,100) to (400,300)
    bresenhamLine(100, 100, 400, 300);

    glFlush();
}

void init()
{
    // White background
    glClearColor(1.0, 1.0, 1.0, 1.0);

    // Default drawing color
    glColor3f(0.0, 0.0, 0.0);

    // Pixel size
    glPointSize(3.0);

    // Set 2D projection
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    gluOrtho2D(0, 500, 0, 500);
}

int main(int argc, char** argv)
{
    glutInit(&argc, argv);

    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);

    glutInitWindowSize(500, 500);
    glutInitWindowPosition(100, 100);

    glutCreateWindow("Bresenham Line Drawing Algorithm");

    init();

    glutDisplayFunc(display);

    glutMainLoop();

    return 0;
}