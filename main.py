
import pygame
from pygame.locals import *
import glm
from gl import Renderer
from model import Model
from shaders import *
from obj import Obj

width = 500
height = 400

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()
pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.play(-1)
rend = Renderer(screen)
rend.setShader(vertex_shader, fragmet_shader1)
actualvertex=vertex_shader
actualfragment=fragmet_shader1
obj = Obj("objet-tex/cat.obj")
gato = Model(obj.assemble())
gato.loadTexture("objet-tex/Cat.jpg")
gato.position.z = 0
gato.scale = glm.vec3(0.17,0.17,0.17)
gato.rotation = glm.vec3(0,0,0)

rend.scene.append(gato)
rend.target = gato.position


menu_open = False
background_colors = [(0, 0, 0), (1, 1, 1), (0.5, 0.5, 0.5)] 
current_color_index = 0

def load_new_model(obj_path, tex_path, scale):
    global gato  
    rend.scene.remove(gato) 

    obj = Obj(obj_path)
    gato = Model(obj.assemble())
    gato.loadTexture(tex_path)
    gato.position.z =0
    gato.scale = glm.vec3(*scale) 
    gato.rotation = glm.vec3(0,0,0)

    rend.scene.append(gato)  
    rend.target = gato.position


isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 100
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_SPACE:
                rend.toggleFilledMode()
            elif event.key == pygame.K_1:
                load_new_model("objet-tex/bird.obj", "objet-tex/bird.jpg", (0.12, 0.12, 0.12))
              
                
            elif event.key == pygame.K_2:
                
                load_new_model("objet-tex/bird2.obj", "objet-tex/bird2.jpg", (0.4, 0.4, 0.4))
            elif event.key == pygame.K_3:
                
                load_new_model("objet-tex/fox.obj", "objet-tex/fox.jpg", (0.08, 0.08, 0.08))
            elif event.key == pygame.K_4:
                load_new_model("objet-tex/cat.obj", "objet-tex/Cat.jpg", (0.17, 0.17, 0.17))
                   
            elif event.key == pygame.K_5:
                rend.setShader(vertex_shader, fragmet_shader)
                actualfragment=fragmet_shader1
                rend.setShader(actualvertex, fragmet_shader1)
                

                rend.setShader(vertex_shader2, fragmet_shader)
                actualvertex=vertex_shader2
                rend.setShader(vertex_shader2, actualfragment) 
                
            elif event.key == pygame.K_6:
                rend.setShader(vertex_shader, fragmet_shader)
                actualfragment=fragmet_shader2
                rend.setShader(actualvertex, fragmet_shader2)
                rend.setShader(vertex_shader, fragmet_shader)
                actualvertex=vertex_shader3
                rend.setShader(vertex_shader3, actualfragment) 
            elif event.key == pygame.K_7:
                rend.setShader(vertex_shader, fragmet_shader)
                actualfragment=fragmet_shader3
                rend.setShader(actualvertex, fragmet_shader3)
                rend.setShader(vertex_shader, fragmet_shader)
                actualvertex=vertex_shader1
                rend.setShader(vertex_shader1, actualfragment)
                
            elif event.key == pygame.K_8:
                rend.setShader(vertex_shader, fragmet_shader)
                actualfragment=fragmet_shader4
                rend.setShader(actualvertex, fragmet_shader4)
                rend.setShader(vertex_shader, fragmet_shader)
                actualvertex=vertex_shader4
                rend.setShader(vertex_shader4, actualfragment)

            if event.key == pygame.K_m:  # Presionar 'M' para abrir/cerrar el menú
                menu_open = not menu_open
            elif menu_open and event.key == pygame.K_n:  # Cambiar color de fondo
                current_color_index = (current_color_index + 1) % len(background_colors)
                rend.changeClearColor(background_colors[current_color_index])
      


    if keys[K_a]:
        rend.camPosition.x += 5 * deltaTime
    elif keys[K_d]:
        rend.camPosition.x -= 5 * deltaTime

    if keys[K_w]:
        rend.camPosition.y += 5 * deltaTime
    elif keys[K_s]:
        rend.camPosition.y -= 5 * deltaTime

    if keys[K_q]:
        rend.camPosition.z += 5 * deltaTime
    elif keys[K_e]:
        rend.camPosition.z -= 5 * deltaTime
    elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.rel
            rend.rotateCamera(mouse_x * 0.002)  
            rend.moveCameraVertical(-mouse_y * 0.002)  
    elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                rend.zoomCamera(-0.5)  
            elif event.button == 3:  
                rend.zoomCamera(0.5)  

    rend.update()
    rend.render()

    rend.elapsedTime += deltaTime

    rend.update()
    rend.render()

    pygame.display.flip()
pygame.mixer.music.stop()
pygame.quit()
