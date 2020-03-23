import pygame
import math
import random
import copy
from lib import NeuralNetwork

class bird:
    def __init__(self, x=150, y=100, update=True, draw=True, nn=None):
        #variables
        self.pos = [x, y]
        self.size = 30
        self.vel_y = 0
        self.jump_strength= 20
        self.gravity = 1.8
        self.max_vel = 25
        self.neural_network = nn
        if nn is not None:
            self.neural_network = self.neural_network.copy()
        self.threshold_jump = 0.5
        self.color = (255,180,0)
        self.hitcolor = (220,0,0)
        self.hit = False
        self.dead = False
        self.fitness = 0
        self.fitness_rate = 0.2
        self.mutation_rate = 10

        self.top_pillar = [0,0]
        self.bottom_pillar = [0,0]

        

        #performance switches
        self.update_switch = update
        self.draw_switch = draw
        self.debug = False
        
    def __repr__(self):
        return repr(self.fitness)

    def update(self):
        if self.update_switch:
            if self.neural_network != None:
                #input_params = [self.pos[1], self.vel_y, self.top_pillar[0], self.top_pillar[1], self.bottom_pillar[0], self.bottom_pillar[1]]
                input_params = [self.pos[1]/720, self.vel_y/10, self.top_pillar[0]/1280, self.top_pillar[1]/720, self.bottom_pillar[1]/720]
                result = self.neural_network.predict(input_params)
                
                if result[0][0]<=self.threshold_jump:
                    self.jump()

            self.vel_y += self.gravity
            

            #apply the velocity
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
                #line top pillar
                pygame.draw.line(canvas,(220,0,0),self.pos,[self.top_pillar[0],self.top_pillar[1]])
                #line bot pillar
                pygame.draw.line(canvas,(220,0,0),self.pos,[self.bottom_pillar[0],self.bottom_pillar[1]])
    
    def aabb_collisionbox(self,padding):
        x = (self.pos[0]-self.size)-padding
        y = (self.pos[1]-self.size)-padding
        w = (self.size*2) + (padding*2)
        h = w
        return (x,y,w,h)
    
    def circle_collision(self):
        return (self.pos[0],self.pos[1],self.size)
    
    def set_pillar(self,pillar):
        x = pillar.x + (pillar.width/2)
        y_top = pillar.gap_pos
        y_bottom = pillar.gap_pos + pillar.gap_height
        
        self.top_pillar[0]=x
        self.top_pillar[1]=y_top
        self.bottom_pillar[0]=x
        self.bottom_pillar[1]=y_bottom


    def jump(self):
        if not self.dead:
            if self.vel_y < self.max_vel:
                self.vel_y -= self.jump_strength

    def die(self):
        self.dead = True
        self.hit = True
        self.debug=False

    def create_neural_network(self, hidden):
        self.neural_network = NeuralNetwork.NeuralNetwork(5,hidden,1)
        self.controls_active = False

    def mutate_neural_network(self):
        self.neural_network.mutate(self.mutation_rate)
        self.nudge_color()

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, val, score):
        if not self.dead:
            self.fitness = ((val+(val*self.fitness_rate))/100) + score
    
    def reset(self, x=150, y=100):
        self.pos = [x, y]
        self.vel_y = 0
        self.fitness = 0
        self.hit = False
        self.dead = False
        self.top_pillar = [0,0]
        self.bottom_pillar = [0,0]

    def get_nn(self):
        return self.neural_network
        

    def get_y(self):
        return self.pos[1]

    def nudge_color(self):
        nudge_amount = 10
        r,g,b = self.color
        index = random.randint(0,2)
        if index == 0:
            if r > 255-nudge_amount:
                r-=nudge_amount
            elif r < nudge_amount:
                r+=nudge_amount
            else:
                r += random.randint(-nudge_amount,nudge_amount)
        elif index == 1:
            if g > 255-nudge_amount:
                g-=nudge_amount
            elif g < nudge_amount:
                g+=nudge_amount
            else:
                g += random.randint(-nudge_amount,nudge_amount)
        else:
            if b > 250-nudge_amount:
                b-=nudge_amount
            elif b < nudge_amount:
                b+=nudge_amount
            else:
                b += random.randint(-nudge_amount,nudge_amount)
        self.color = (r,g,b)