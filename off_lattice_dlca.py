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
        pygame.draw.circle(canvas, self.color, center=(self.center.x, self.center.y), radius=self.radius)
    
    '''@staticmethod
    def is_intersects(c1, c2, canvas):
        is_checked = super().is_intersects(c1, c2)
        pygame.draw.line(canvas, (0, 0, 0), (c1.center.x,c1.center.y), (c2.center.x,c2.center.y), 2)
        return is_checked'''

class Globule:
    def __init__(self, id: int):
        self.particles = []
        self.id = id
        self.speed = 2
    
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

    def initialize(self):
        current_area = 0
        final_area = self.field_size.x * self.field_size.y * (1 -  self.porosity)
        self.log += f'Final are: {final_area}\n'
        while current_area < final_area:
            self.log += f'Current area: {current_area}/{final_area}\n'            
            is_taken = True
            globule = Globule(self.__id)
            while is_taken:                
                place_pos = Vector2(random.random()*(self.field_size.x-self.particle_radius), random.random()*(self.field_size.y-self.particle_radius))
                particle = Particle(place_pos.x, place_pos.y, self.particle_radius)
                globule.add_particle(particle)
                is_taken, agr_id, log = self.is_collided(globule)                
                self.log += log+'\n' 
                if is_taken:
                    globule.remove_particle(particle)
            
            self.globules[self.__id] = globule
            current_area += globule.get_area()
            self.__id += 1

    def move_all_globules(self):
        for g in self.globules:
            direction = Vector2(random.random()*1.42 - 0.71, random.random()*1.42 - 0.71)
            direction = Vector2.mult_on_scalar(self.globules[g].speed, direction)
            for step in range (self.steps, 0, -1):                 
                self.globules[g].move(direction)
                is_aggregated, agr_id, log = self.is_collided(self.globules[g])
                if is_aggregated:
                    self.globules[g].set_color(RED)
                    self.globules[agr_id].set_color(RED)                    
                    step = 0
                self.log += log + '\n'

            
            
    
    def is_collided (self, globule: Globule) -> tuple ((bool, int, str)):
        for g in self.globules:
            if g == globule.id:
                continue
            for (p1, p2) in zip(globule.particles, self.globules[g].particles):
                if CircleCollider.is_intersects(p1, p2):
                    return True, g, f'{globule} collides with {self.globules[g]}. Collided: {p1} и {p2}'

        return False, -1, f"{globule} doesn't collides"


