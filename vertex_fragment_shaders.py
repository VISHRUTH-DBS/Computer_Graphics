import glfw
from OpenGL.GL import *
import numpy as np

# Vertex shader: sets the position of each vertex
vertex_shader_source = """
#version 330 core
layout (location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos, 1.0);
}
"""

# Fragment shader: sets the colour of each fragment
fragment_shader_source = """
#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(0.0, 0.5, 1.0, 1.0);
}
"""


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        message = glGetShaderInfoLog(shader).decode()
        raise RuntimeError("Shader compilation failed: " + message)

    return shader


# Initialize GLFW
if not glfw.init():
    raise RuntimeError("GLFW initialization failed")

# Request OpenGL 3.3 core profile
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)

glfw.window_hint(
    glfw.OPENGL_PROFILE,
    glfw.OPENGL_CORE_PROFILE
)

# Create the graphics window
window = glfw.create_window(
    800,
    600,
    "OpenGL: Vertex and Fragment Shaders",
    None,
    None
)

if not window:
    glfw.terminate()
    raise RuntimeError("Window creation failed")

glfw.make_context_current(window)

# Compile the shaders
vertex_shader = compile_shader(
    vertex_shader_source,
    GL_VERTEX_SHADER
)

fragment_shader = compile_shader(
    fragment_shader_source,
    GL_FRAGMENT_SHADER
)

# Create and link the shader program
shader_program = glCreateProgram()

glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, fragment_shader)
glLinkProgram(shader_program)

if not glGetProgramiv(shader_program, GL_LINK_STATUS):
    message = glGetProgramInfoLog(shader_program).decode()
    raise RuntimeError("Program linking failed: " + message)

# The individual shader objects are no longer needed
glDeleteShader(vertex_shader)
glDeleteShader(fragment_shader)

# Three vertices: bottom-left, bottom-right, and top
vertices = np.array([
    -0.5, -0.5, 0.0,
     0.5, -0.5, 0.0,
     0.0,  0.5, 0.0
], dtype=np.float32)

# Create and bind a Vertex Array Object and Vertex Buffer Object
VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)

glBindVertexArray(VAO)
glBindBuffer(GL_ARRAY_BUFFER, VBO)

glBufferData(
    GL_ARRAY_BUFFER,
    vertices.nbytes,
    vertices,
    GL_STATIC_DRAW
)

# Attribute 0 contains 3 floating-point position values
glVertexAttribPointer(
    0,
    3,
    GL_FLOAT,
    GL_FALSE,
    0,
    None
)

glEnableVertexAttribArray(0)

# Unbind to avoid accidental modification
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

# Main rendering loop
while not glfw.window_should_close(window):
    glClearColor(0.08, 0.08, 0.10, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader_program)
    glBindVertexArray(VAO)

    glDrawArrays(GL_TRIANGLES, 0, 3)

    glfw.swap_buffers(window)
    glfw.poll_events()

# Release OpenGL resources
glDeleteVertexArrays(1, [VAO])
glDeleteBuffers(1, [VBO])
glDeleteProgram(shader_program)

glfw.terminate()
