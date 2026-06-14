import pygame
import moderngl
import sys
import numpy as np
from PIL import Image

pygame.init()

pygame.display.set_mode(
    (1000, 1000),
    pygame.OPENGL | pygame.DOUBLEBUF
)

ctx = moderngl.create_context()
square = np.array([ -0.5,  0.5, 0.0, 0, 1, #x, y, z, u = width, v = height
                    -0.5, -0.5, 0.0, 0, 0,
                     0.5,  0.5, 0.0, 1, 1,
                     0.5, -0.5, 0.0, 1, 0,
                      ], dtype='f4')


program = ctx.program(
    vertex_shader='''
    #version 330 core
    in vec3 vector;
    in vec2 uv;
    out vec2 v_uv;
    uniform vec3 box_difference;
    void main() {
    gl_Position = vec4(vector + box_difference, 1.0);
    v_uv = uv;
    }
    ''',
    fragment_shader='''
    #version 330 core
    in vec2 v_uv;
    out vec4 Colour;
    uniform sampler2D box_texture;
    void main() {
    Colour = texture(box_texture, v_uv);
    }
    ''',

)

box = Image.open("assets/may_background.png").convert("RGBA")
box_width, box_height = box.size
box_texture = ctx.texture((box_width, box_height), 4, box.tobytes())
box_texture.filter = (ctx.NEAREST, ctx.NEAREST)
box_texture.use(location=0)
# program['box_texture'] = 0
box_pos = [0, 0, 0]

vbo = ctx.buffer(data=square)
vao = ctx.vertex_array(program, [(vbo, '3f 2f', 'vector', 'uv')])

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    key_pressed=pygame.key.get_pressed()
    if key_pressed[pygame.K_RIGHT]:
        box_pos[0] += 0.01
    if key_pressed[pygame.K_LEFT]:
        box_pos[0] -= 0.01
    program['box_difference'].value = box_pos
    ctx.clear(0.5, 0, 0.5)
    vao.render(mode=moderngl.TRIANGLE_STRIP)

    
    pygame.display.flip()

    clock.tick_busy_loop(240)
    print(f"fps: {clock.get_fps()}")
    