import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# ================= DATA KUBUS =================
vertices = (
    (1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,-1),
    (1,-1,1),(1,1,1),(-1,-1,1),(-1,1,1)
)

edges = (
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,7),(7,6),(6,4),
    (0,4),(1,5),(2,7),(3,6)
)

faces = (
    (0,1,2,3),(4,5,7,6),(0,4,5,1),
    (3,2,7,6),(1,5,7,2),(0,4,6,3)
)

cube_colors = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]

def draw_cube(mode):
    if mode == 1:
        glBegin(GL_LINES)
        glColor3f(1,1,1)
        for edge in edges:
            for v in edge:
                glVertex3fv(vertices[v])
        glEnd()
    else:
        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glColor3fv(cube_colors[i])
            for v in face:
                glVertex3fv(vertices[v])
        glEnd()

def lighting(enable):
    if enable:
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (3,3,3,1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1,1,1,1))
    else:
        glDisable(GL_LIGHTING)

def draw_square():
    glBegin(GL_QUADS)
    glColor3f(0,1,0)
    glVertex2f(-40,-40)
    glVertex2f(40,-40)
    glVertex2f(40,40)
    glVertex2f(-40,40)
    glEnd()

# ================= MAIN =================
def main():
    pygame.init()
    display = (1000, 500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)

    # === KUBUS STATE ===
    cx, cy, cz = 0, 0, -8
    rx, ry = 0, 0
    cscale = 1
    mode = 2
    light_on = True
    lighting(light_on)

    # === PERSEGI STATE ===
    sx, sy = 0, 0
    srot = 0
    sscale = 1
    shear = 0
    reflect = 1

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                run = False

        k = pygame.key.get_pressed()

        # ===== KONTROL KUBUS =====
        if k[K_w]: cy += 0.1
        if k[K_s]: cy -= 0.1
        if k[K_a]: cx -= 0.1
        if k[K_d]: cx += 0.1
        if k[K_UP]: rx += 2
        if k[K_DOWN]: rx -= 2
        if k[K_LEFT]: ry += 2
        if k[K_RIGHT]: ry -= 2
        if k[K_z]: cscale += 0.02
        if k[K_x]: cscale -= 0.02
        if k[K_1]: mode = 1
        if k[K_2]: mode = 2
        if k[K_3]:
            for i in range(6):
                cube_colors[i] = (random.random(),random.random(),random.random())
        if k[K_l]:
            light_on = not light_on
            lighting(light_on)

        # ===== KONTROL PERSEGI =====
        if k[K_i]: sy += 4
        if k[K_k]: sy -= 4
        if k[K_j]: sx -= 4
        if k[K_l]: sx += 4
        if k[K_u]: srot += 5
        if k[K_o]: srot -= 5
        if k[K_n]: sscale += 0.05
        if k[K_m]: sscale -= 0.05
        if k[K_h]: shear += 0.02
        if k[K_r]: reflect *= -1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # ===== VIEWPORT KIRI (KUBUS 3D) =====
        glViewport(0, 0, 500, 500)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1, 0.1, 50)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(cx, cy, cz)
        glRotatef(rx, 1,0,0)
        glRotatef(ry, 0,1,0)
        glScalef(cscale,cscale,cscale)
        draw_cube(mode)

        # ===== VIEWPORT KANAN (PERSEGI 2D) =====
        glViewport(500, 0, 500, 500)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-250,250,-250,250)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(sx, sy, 0)
        glRotatef(srot, 0,0,1)
        glScalef(sscale*reflect, sscale, 1)
        glMultMatrixf([
            1, shear, 0, 0,
            0,    1, 0, 0,
            0,    0, 1, 0,
            0,    0, 0, 1
        ])
        draw_square()

        pygame.display.flip()

    pygame.quit()

main()
