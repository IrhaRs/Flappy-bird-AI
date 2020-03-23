import pygame

class Pillar:
    def __init__(self, x=500, width=50, gap_pos=300, gap_height=250):
        self.x = x
        self.origin_x = x
        self.width=width
        self.gap_pos = gap_pos
        self.gap_height = gap_height
        self.color = (255,255,255)


        #performance switches
        self.update_switch = True
        self.draw_switch = True
        self.debug = False



    def update(self, x_translate):
        if self.update_switch:
            self.x = self.origin_x - x_translate
            

    def draw(self,canvas):
        if self.draw_switch:
            #draw the pillars
            pygame.draw.rect(canvas, self.color, pygame.Rect(self.x, 0, self.width, self.gap_pos))
            pygame.draw.rect(canvas, self.color, pygame.Rect(self.x, self.gap_height+self.gap_pos, self.width, 720))
            if self.debug:
                #AABB shown
                pygame.draw.rect(canvas, (0,220,0), pygame.Rect(self.aabb_collisionbox(15)),1)
                #show top col
                pygame.draw.rect(canvas, (0,0,220), pygame.Rect(self.box_collision_top()),1)
                #show bottom col
                pygame.draw.rect(canvas, (0,0,220), pygame.Rect(self.box_collision_bottom()),1)
                

    def aabb_collisionbox(self,padding):
        x = self.x -padding
        y = 0 - padding
        w = self.width + (padding*2)
        h = 720 + (padding*2)
        return (x,y,w,h)

    def box_collision_top(self):
        return (self.x, 0, self.width,self.gap_pos)
    
    def box_collision_bottom(self):
        return (self.x, self.gap_height+self.gap_pos, self.width, 720)
   