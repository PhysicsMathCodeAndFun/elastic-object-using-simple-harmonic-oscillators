import pygame
import sys
import random
import math



pygame.init()
info = pygame.display.Info()
w, h = info.current_w, info.current_h
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
pygame.display.set_caption('physics, math, code & fun')

pygame.mixer.init()
beep = pygame.mixer.Sound("beep.mp3")
font = pygame.font.SysFont('Arial', 50)
clock = pygame.time.Clock()

size = 20
t = 0
delta_time = 0.0
dt = 0.01

class Particles:
    def __init__(self, x, y):
        self.rect =  pygame.Rect(x, y, size, size)
        self.visible = True
        self.color = [50,200,50]
        self.F = [0,0]
        
        self.x = [x,y]
        self.x0 = [x,y]
        self.m = 1.0

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect)

            

particles = []
x_c, y_c = w//2, h//2
c_radius = 500
angle = 0
last_x, last_y = 0, 0
size2 = 100 

while angle < 2 * math.pi:

    x = c_radius * math.cos(angle) + x_c
    y = c_radius * math.sin(angle) + y_c
    
    if not (int(x) == int(last_x) and int(y) == int(last_y)):
        particles.append(Particles(x, y))    
        angle += (2 * math.pi) / 150

    last_x = x
    last_y = y
    
player = pygame.Rect(w//2, 400, 100, 100)
mousePress = False
idClicks = []


def Update(screen):
    global t
    global delta_time

    screen.fill((0,0,0))

    
    last_p = particles
    
    for i in range(0, len(last_p)):      
        k1 = 1.0
        k2 = 1.0
        m = last_p[i].m
        
        x_i, x_i_p1, x_i_m1 = 0, 0, 0
        y_i, y_i_p1, y_i_m1 = 0, 0, 0
        
        Fx = particles[i].F[0]
        Fy = particles[i].F[1]
        
        if i != 0 and i != len(last_p) - 1:              
            x_i, x_i_p1, x_i_m1 = last_p[i].x[0] - last_p[i].x0[0], last_p[i + 1].x[0] - last_p[i + 1].x0[0], last_p[i - 1].x[0] - last_p[i - 1].x0[0]
            y_i, y_i_p1, y_i_m1 = last_p[i].x[1] - last_p[i].x0[1], last_p[i + 1].x[1] - last_p[i + 1].x0[1], last_p[i - 1].x[1] - last_p[i - 1].x0[1]
        if i == 0:
            x_i, x_i_p1, x_i_m1 = last_p[i].x[0] - last_p[i].x0[0], last_p[i + 1].x[0] - last_p[i + 1].x0[0], last_p[len(last_p) - 1].x[0] - last_p[len(last_p) - 1].x0[0]
            y_i, y_i_p1, y_i_m1 = last_p[i].x[1] - last_p[i].x0[1], last_p[i + 1].x[1] - last_p[i + 1].x0[1], last_p[len(last_p) - 1].x[1] - last_p[len(last_p) - 1].x0[1]
        if i == len(last_p) - 1:
            x_i, x_i_p1, x_i_m1 = last_p[i].x[0] - last_p[i].x0[0], last_p[0].x[0] - last_p[0].x0[0], last_p[i - 1].x[0] - last_p[i - 1].x0[0]
            y_i, y_i_p1, y_i_m1 = last_p[i].x[1] - last_p[i].x0[1], last_p[0].x[1] - last_p[0].x0[1], last_p[i - 1].x[1] - last_p[i - 1].x0[1]

        particles[i].x[0] = last_p[i].x0[0] + ((1.0 / (k1 + 2*k2)) * (k2 * (x_i_p1 + x_i_m1) + Fx)) 
        particles[i].x[1] = last_p[i].x0[1] + ((1.0 / (k1 + 2*k2)) * (k2 * (y_i_p1 + y_i_m1) + Fy))           
         
        particles[i].draw(screen)
        
        particles[i].rect.centerx = particles[i].x[0]
        particles[i].rect.centery = particles[i].x[1]
        
        
        
        if abs(x_i) >= 1.0:
            particles[i].color = [150,20,50]
        else:
            particles[i].color = [50,200,50]
            

    text = font.render('github.com/PhysicsMathCodeAndFun', True, (255,255,255))
    screen.blit(text, pygame.Rect(30, 0, 400,300))
    pygame.draw.rect(screen, (255, 0, 255), player, width=2)
    
    if mousePress:
        for l in idClicks:
            particles[l].F[0] = 1.0 * (player.centerx - particles[l].x0[0])
            particles[l].F[1] = 1.0 * (player.centery - particles[l].x0[1])
            particles[l].color = [255,255,255]
    else:           
        if len(idClicks) != 0:
            for l in idClicks:
                particles[l].F[0] = 0
                particles[l].F[1] = 0
                
            idClicks.clear()
            beep.play()

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        player.width += 1
        player.height += 1
    if keys[pygame.K_s]:
        player.width -= 1
        player.height -= 1
    
    delta_time = clock.tick(60) / 1000
    pygame.display.flip()
    t += 1
    

isEnd = False
while not isEnd:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isEnd = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(0, len(particles)):
                if player.colliderect(particles[i].rect):
                    mousePress = True
                    idClicks.append(i)
                    
            
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            player.centerx = mouse_pos[0]
            player.centery = mouse_pos[1]

        
        if event.type == pygame.MOUSEBUTTONUP:
            mousePress = False    
        
            
    Update(screen)
    
pygame.quit()
sys.exit()
