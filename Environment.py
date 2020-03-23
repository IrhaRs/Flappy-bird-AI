import pygame
from pygame.locals import *
import sys
import random
from lib import Collision as col
from obj import EvolutionManager as Evo_man
from obj import PillarManager


class Environment:
    def __init__(self, w=1280, h=720, title="Environment"):
        pygame.init()
        self.game_running = True
        #setup fps
        self.fps = 120
        self.fps_clock = pygame.time.Clock()

        #setup width/height
        self.width = w
        self.height = h
        #make display
        self.background_color = (0, 0, 0)
        self.display = pygame.display.set_mode((self.width, self.height))
        self.title = title
        pygame.display.set_caption(self.title)
        

        #objects
        self.lst_objects = []
        self.lst_birds = []
        self.pillar_manager = []
        self.evolution_manager = []
        self.top_screen = (0,-1000,self.width,950)
        self.bottom_screen = (0,self.height,self.width,50+self.height)

        #variables
        self.enable_controls = True
        self.pause = False
        self.pause_time = 30

        print("made Environment")

    def game_loop(self):
        while self.game_running:
            #set bg
            self.display.fill(self.background_color)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_running = False
                if self.enable_controls:
                    if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_SPACE :
                            [bird.jump() for bird in self.evolution_manager.get_population()]   
            
            
            #####################################################################################################
            if self.pause:
                print("generation complete")
            else:
                # Update
                for obj in self.lst_objects:
                    obj.update()
                for bird in self.evolution_manager.get_population():
                    bird.update()
                self.pillar_manager.update()

                #check collisions
                pillar = self.pillar_manager.get_pillar()
                
                for bird in self.evolution_manager.get_population():
                    if not bird.dead:
                        bird.set_pillar(pillar)
                        if not(bird.get_y() > 0) or not(bird.get_y() < self.height):
                            self.bird_dies(bird,True)
                        elif col.AABB_Collision_rect(bird.aabb_collisionbox(10),pillar.aabb_collisionbox(15)):
                            if col.Circle_Rect_Collision2(bird.circle_collision(),pillar.box_collision_top()) or col.Circle_Rect_Collision2(bird.circle_collision(),pillar.box_collision_bottom()):
                                #set fitness and BIRD DIES 
                                self.bird_dies(bird)
                    
                # Draw.
                for obj in self.lst_objects:
                    obj.draw(self.display)
                self.pillar_manager.draw(self.display)
                for bird in self.evolution_manager.get_population():
                    bird.draw(self.display)
                    

                if self.evolution_manager.is_population_dead():
                    self.new_generation()

            pygame.display.flip()
            self.fps_clock.tick(self.fps)


        pygame.quit()
        sys.exit(1)


    def add_object(self, obj):
        self.lst_objects.append(obj)

    def add_bird(self, bird):
        self.lst_birds.append(bird)

    def run(self):
        self.game_loop()

    def bird_dies(self,bird,outofmap=False):
        #set fitness and BIRD DIES 
        #fitness = self.pillar_manager.get_x()
        
        p = self.pillar_manager.get_pillar()
        middlepipe= [p.x+(p.width/2),p.gap_pos+(p.gap_height/3)]
        dist_middlepipe = col.Distance_Line(bird.pos[0],bird.pos[1],middlepipe[0],middlepipe[1])


        fitness = 10/(dist_middlepipe)
        score = self.pillar_manager.score *10
        if outofmap and bird.fitness < 300 and self.evolution_manager.generation == 0:
            fitness = 0
        bird.set_fitness(fitness, score)
        bird.die()
        self.evolution_manager.add_dead(bird)

    def new_generation(self):
        #make new generation and reset the game
        self.pause=True
        self.evolution_manager.new_generation()
        self.pillar_manager = PillarManager.PillarManager()
        
        self.pause = False

    