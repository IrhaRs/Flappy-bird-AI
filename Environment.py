import pygame
from pygame.locals import *
import sys
from lib import Collision as col


class Environment:
    def __init__(self, w=1280, h=720, title="Environment"):
        pygame.init()
        self.game_running = True
        #setup fps
        self.fps = 30
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
        

        #variables
        self.enable_controls = True


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
                            [bird.jump() for bird in self.lst_birds]   

            # Update
            for obj in self.lst_objects:
                obj.update()
            for bird in self.lst_birds:
                bird.update()
            self.pillar_manager.update()

            #check collisions
            pillar = self.pillar_manager.get_pillar()
            pillar.debug = True
            for bird in self.lst_birds:
                if col.AABB_Collision_rect(bird.aabb_collisionbox(10),pillar.aabb_collisionbox(15)):
                    if col.Circle_Rect_Collision2(bird.circle_collision(),pillar.box_collision_top()) or col.Circle_Rect_Collision2(bird.circle_collision(),pillar.box_collision_bottom()):
                        bird.die()
                
            # Draw.
            for obj in self.lst_objects:
                obj.draw(self.display)
            self.pillar_manager.draw(self.display)
            for bird in self.lst_birds:
                bird.draw(self.display)

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

