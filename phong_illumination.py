# phong_illumination.py
# Computer Graphics Laboratory
# Implementation of Phong Illumination Model
# Python + PyOpenGL + OpenGL/GLUT

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

WIDTH = 700
HEIGHT = 600

shader_program = None

vertex_shader_source = """
#version 120
varying vec3 fragNormal;
varying vec3 fragPosition;

void main()
{
    vec4 position = gl_ModelViewMatrix * gl_Vertex;
    fragNormal = normalize(gl_NormalMatrix * gl_Normal);
    fragPosition = position.xyz;
    gl_Position = gl_ProjectionMatrix * position;
}
"""

fragment_shader_source = """
#version 120

varying vec3 fragNormal;
varying vec3 fragPosition;

uniform vec3 lightPosition;
uniform vec3 lightColor;
uniform vec3 objectColor;

uniform float ambientStrength;
uniform float specularStrength;
uniform float shininess;

void main()
{
    vec3 N = normalize(fragNormal);
    vec3 L = normalize(lightPosition - fragPosition);
    vec3 V = normalize(-fragPosition);

    vec3 R = reflect(-L, N);

    vec3 ambient = ambientStrength * lightColor;

    float diff = max(dot(N, L), 0.0);
    vec3 diffuse = diff * lightColor;

    float spec = pow(max(dot(R, V), 0.0), shininess);
    vec3 specular = specularStrength * spec * lightColor;

    vec3 finalColor = (ambient + diffuse) * objectColor + specular;

    gl_FragColor = vec4(finalColor, 1.0);
}
"""


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    status = glGetShaderiv(shader, GL_COMPILE_STATUS)

    if not status:
        error = glGetShaderInfoLog(shader).decode()
        print("Shader Compilation Error:")
        print(error)
        sys.exit(1)

    return shader


def create_shader_program():
    vertex_shader = compile_shader(
        vertex_shader_source,
        GL_VERTEX_SHADER
    )

    fragment_shader = compile_shader(
        fragment_shader_source,
        GL_FRAGMENT_SHADER
    )

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    status = glGetProgramiv(program, GL_LINK_STATUS)

    if not status:
        error = glGetProgramInfoLog(program).decode()
        print("Shader Linking Error:")
        print(error)
        sys.exit(1)

    return program


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(
        0.0, 0.0, 6.0,
        0.0, 0.0, 0.0,
        0.0, 1.0, 0.0
    )

    glUseProgram(shader_program)

    light_position = glGetUniformLocation(
        shader_program, "lightPosition"
    )

    light_color = glGetUniformLocation(
        shader_program, "lightColor"
    )

    object_color = glGetUniformLocation(
        shader_program, "objectColor"
    )

    ambient_strength = glGetUniformLocation(
        shader_program, "ambientStrength"
    )

    specular_strength = glGetUniformLocation(
        shader_program, "specularStrength"
    )

    shininess = glGetUniformLocation(
        shader_program, "shininess"
    )

    glUniform3f(light_position, 3.0, 3.0, 5.0)
    glUniform3f(light_color, 1.0, 1.0, 1.0)
    glUniform3f(object_color, 0.2, 0.5, 1.0)

    glUniform1f(ambient_strength, 0.15)
    glUniform1f(specular_strength, 0.8)
    glUniform1f(shininess, 32.0)

    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)

    gluSphere(
        quadric,
        1.5,
        50,
        50
    )

    gluDeleteQuadric(quadric)

    glUseProgram(0)
    glutSwapBuffers()


def init():
    global shader_program

    glClearColor(0.05, 0.05, 0.05, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    shader_program = create_shader_program()


def reshape(width, height):
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(
        45.0,
        width / float(height),
        1.0,
        100.0
    )

    glMatrixMode(GL_MODELVIEW)


def keyboard(key, x, y):
    key = key.decode("utf-8").lower()

    if key == "q":
        sys.exit(0)


def main():
    glutInit(sys.argv)

    glutInitDisplayMode(
        GLUT_DOUBLE |
        GLUT_RGB |
        GLUT_DEPTH
    )

    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(100, 100)

    glutCreateWindow(
        b"Phong Illumination Model"
    )

    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    glutMainLoop()


if __name__ == "__main__":
    main()
