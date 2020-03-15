import pygame
import math

class bird:
    def __init__(self, x=150, y=100, update=True, draw=True):
        #variables
        self.pos = [x, y]
        self.size = 30
        self.vel_y = 0
        self.jump_strength= 20
        self.gravity = 1.8
        self.max_vel = 15
        self.neural_network = None
        self.color = (255,180,0)
        self.hitcolor = (220,0,0)
        self.hit = False
        self.dead = False
        
        #performance switches
        self.update_switch = update
        self.draw_switch = draw
        self.debug = False
        

    def update(self):
        if self.update_switch:
            if self.vel_y <= self.max_vel or self.vel_y >= -self.max_vel:
                self.vel_y += self.gravity
            

            #apply the velocity
            if self.pos[1]<=720-self.size:
                self.pos[1] += self.vel_y
                self.pos[1] = math.floor(self.pos[1])
            
        
    def draw(self, canvas):
        if self.draw_switch:
            col = self.color
            if self.hit:
                col = self.hitcolor
            pygame.draw.circle(canvas, col, self.pos, self.size, 0)
            
            if self.debug:
                pygame.draw.rect(canvas, (0,220,0), pygame.Rect(self.aabb_collisionbox(10)),1)
                cx,cy,rad = self.circle_collision()
                pygame.draw.circle(canvas,(0,0,220), (cx,cy),rad,1)
    
    def aabb_collisionbox(self,padding):
        x = (self.pos[0]-self.size)-padding
        y = (self.pos[1]-self.size)-padding
        w = (self.size*2) + (padding*2)
        h = w
        return (x,y,w,h)
    
    def circle_collision(self):
        return (self.pos[0],self.pos[1],self.size)
    
    def jump(self):
        if not self.dead:
            if self.vel_y <= self.max_vel or self.vel_y >= -self.max_vel:
                self.vel_y -= self.jump_strength

    def die(self):
        self.dead = True
        self.hit = True