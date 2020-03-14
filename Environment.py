import pygame
from pygame.locals import *
import sys


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

        print("made Environment")

    def game_loop(self):
        while self.game_running:
            self.display.fill(self.background_color)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_running = False

            # Update
            for obj in self.lst_objects:
                obj.update()
            # Draw.
            for obj in self.lst_objects:
                obj.draw(self.display)
            
            pygame.display.flip()
            self.fps_clock.tick(self.fps)
        pygame.quit()
        sys.exit(1)


    def add_object(self, obj):
        self.lst_objects.append(obj)

    def run(self):
        self.game_loop()

