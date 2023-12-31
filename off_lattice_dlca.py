import math
import random
import pygame
from phys_aero import *
from settings import * 

class Particle (CircleCollider):
    def __init__(self, center_x, center_y, radius):
        super().__init__(center_x, center_y, radius)
        self.color = GREEN

    def move (self, vector):
        self.center += vector
    
    def get_area(self) -> float:
        return math.pi * (self.radius**2)
    
    def __str__(self) -> str:
        return f'Particle at pos {self.center}'

    def draw(self, canvas):
        pygame.draw.circle(canvas, self.color, center=(self.center.x + OFFSET, self.center.y + OFFSET), radius=self.radius)
        pygame.draw.circle(canvas, BLACK, center=(self.center.x + OFFSET, self.center.y + OFFSET), radius=self.radius, width=2)
    
    '''@staticmethod
    def is_intersects(c1, c2, canvas):
        is_checked = super().is_intersects(c1, c2)
        pygame.draw.line(canvas, (0, 0, 0), (c1.center.x,c1.center.y), (c2.center.x,c2.center.y), 2)
        return is_checked'''

class Globule:
    def __init__(self, id: int):
        self.particles = []
        self.id = id
        self.speed = 5
    
    def add_particle(self, particle: Particle) -> str:
        self.particles.append(particle)
        return f'In {self} was added {particle}'

    def remove_particle (self, particle) -> str:
        self.particles.remove(particle)
        return f'From {self} was removed {particle}'
    
    def move (self, motion):
        for p in self.particles:
            p.move(motion)

    def set_color(self, color):
        for p in self.particles:
            p.color = color

    def gradient_color(self, color):
        for p in self.particles:
            r, g, b = p.color
            
            r += color[0]
            if r > 255:
                r = 255
            elif r < 0:
                r = 0

            g += color[1]
            if g > 255:
                g = 255
            elif g < 0:
                g = 0

            b += color[2]
            if b > 255:
                b = 255
            elif b < 0:
                b = 0
            p.color = (r, g, b)
           
               

    def draw(self, canvas: pygame.Surface) -> None:
        for p in self.particles:
            p.draw(canvas)

    def get_area(self):
        area = 0
        for p in self.particles:
            area += p.get_area()
        return area

    def __str__(self) -> str:
        return f'Globule {self.id}'

class CellularAutomata:
    def __init__(self, size: Vector2, particle_radius: float, porosity: float):
        self.globules = {}
        self.__id = 1
        self.field_size = size
        self.particle_radius = particle_radius
        self.porosity = porosity
        self.log = ''
        self.steps = 10
        self.speed_mod = 0

    def initialize(self):
        current_area = 0
        final_area = self.field_size.x * self.field_size.y * (1 -  self.porosity)
        self.log += f'Final area: {final_area}\n'
        while current_area < final_area:
            self.log += f'Current area: {current_area}/{final_area}\n'            
            is_taken = True
            globule = Globule(self.__id)
            while is_taken:                
                place_pos = Vector2(random.random()*(self.field_size.x-self.particle_radius), random.random()*(self.field_size.y-self.particle_radius))
                # place_pos = Vector2(random.random()*(self.field_size.x-400)+200, random.random()*(self.field_size.y-200)+100)
                particle = Particle(place_pos.x, place_pos.y, self.particle_radius)
                globule.add_particle(particle)
                is_taken, agr_id, log = self.is_collided(globule)                
                self.log += log+'\n' 
                if is_taken:
                    globule.remove_particle(particle)
            
            self.globules[self.__id] = globule
            current_area += globule.get_area()
            self.__id += 1
        #self.speed_mod = 200 / len(self.globules)

    def update_ca(self):
        if len(self.globules) == 1:
            self.log += 'Structure created'
            return
        
        globules_for_removing = []       
        for g in self.globules: 
            single_dir = Vector2(random.random()*1.42 - 0.71, random.random()*1.42 - 0.71)
            direction = Vector2.mult_on_scalar(self.globules[g].speed, single_dir)
            for step in range (self.steps, 0, -1): 
                self.globules[g].move(direction)
                is_crossed_border = False
                for p in self.globules[g].particles:
                    if p.center.x > self.field_size.x or p.center.x < 0 or p.center.y > self.field_size.y or p.center.y < 0:
                        is_crossed_border = True
                        break
                if is_crossed_border: 
                    self.globules[g].move(-direction)

                is_aggregated, agr_id, log = self.is_collided(self.globules[g])
                if is_aggregated:
                    #self.globules[g].set_color(RED)
                    #self.globules[agr_id].set_color(RED)
                    self.globules[g].gradient_color((7, -7, 0))
                    self.globules[agr_id].gradient_color((7, -7, 0)) 
                    #self.globules[g].move(-single_dir)                    
                    self.aggregate(from_globule=self.globules[g], to_globule=self.globules[agr_id])  
                    globules_for_removing.append(g)                  
                    break
                self.log += log + '\n'

        for id in globules_for_removing:            
            del self.globules[id]

                
            
    def aggregate (self, from_globule : Globule, to_globule : Globule):
        for p in from_globule.particles:
            self.log += to_globule.add_particle(p) + '\n'
            #p.color = BLUE  
        #to_globule.speed = to_globule.speed / len(to_globule.particles)   
        #to_globule.speed = to_globule.speed - self.speed_mod   
        #to_globule.speed = min(to_globule.speed, from_globule.speed)
        #to_globule.speed = to_globule.speed - len(to_globule.particles)*0.1  
        from_globule.particles.clear()      

    def is_collided (self, globule: Globule) -> tuple ((bool, int, str)):
        for g in self.globules:
            if g == globule.id:
                continue
            for p1 in globule.particles:
                for p2 in self.globules[g].particles:
                    if CircleCollider.is_intersects(p1, p2):
                        return True, g, f'{globule} collides with {self.globules[g]}. Collided: {p1} и {p2}'

        return False, -1, f"{globule} doesn't collides"


