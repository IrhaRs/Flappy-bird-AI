import queue
from obj import Pillar
import random 

class PillarManager:
    def __init__(self):
        self.lst_pillars = []
        self.x = 0 #to scroll the pillars
        self.distance_pillars = 450 #distance between the different pillars
        self.pos_pillars = 650
        self.pillar_width = 80
        self.pillar_height = 250
        self.min_y = 100
        self.max_y = 720-100
        self.scroll_speed = 6
        self.debug = False
        self.score=0

        [self.generate_pillar() for i in range(10)]

    def update(self):
        self.x += self.scroll_speed
        for pillar in self.lst_pillars:
            pillar.update(self.x)
            if pillar.x+pillar.width < 80:
                self.lst_pillars.remove(pillar) 
                self.generate_pillar()
                self.score+=1

    def draw(self,canvas):
        [pillar.draw(canvas) for pillar in self.lst_pillars]
        
    def generate_pillar(self):
        p = Pillar.Pillar(self.pos_pillars, self.pillar_width,random.randint(self.min_y, self.max_y-self.pillar_height), self.pillar_height)
        if self.debug:
            p.debug = True
        self.lst_pillars.append(p)
        self.pos_pillars+=self.distance_pillars

    def delete_pillar(self):
        self.generate_pillar()

    def get_pillar(self):
        return self.lst_pillars[0]

    def get_x(self):
        return self.x

    