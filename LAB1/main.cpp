#include <GL/freeglut.h>
#include <cmath>
#include <iostream>
using namespace std;
void drawPixel(float x, float y)
{
glBegin(GL_POINTS);
glVertex2f(x, y);
glEnd();
}
void ddaLine(float x1, float y1, float x2, float y2)
{
float dx = x2 - x1;
float dy = y2 - y1;
float steps;
if (fabs(dx) > fabs(dy))
steps = fabs(dx);
else
steps = fabs(dy);
float xInc = dx / steps;
float yInc = dy / steps;
float x = x1;
float y = y1;
for (int i = 0; i <= steps; i++)
{
drawPixel(round(x), round(y));
x += xInc;
y += yInc;
}
glFlush();
}
void display()
{
glClear(GL_COLOR_BUFFER_BIT);
glColor3f(1.0, 0.0, 0.0);
ddaLine(100, 100, 400, 300);
glFlush();
}
void init()
{
glClearColor(1.0, 1.0, 1.0, 1.0);
glColor3f(0.0, 0.0, 0.0);
glPointSize(3.0);
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
glutCreateWindow("DDA Line Drawing Algorithm");
init();
glutDisplayFunc(display);
glutMainLoop();
return 0;
}