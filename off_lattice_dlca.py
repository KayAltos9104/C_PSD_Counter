import math
from phys_aero import *
from settings import * 

class Globule:
    def __init__(self, size: Vector2, particle_radius: float, porosity: float):
        self.particles = {}
        self.__id = 1
        self.field_size = size

    def initialize(self):
        pass


class CellularAutomata:
    def __init__(self):
        pass

class Particle (CircleCollider):
    def __init__(self, center_x, center_y, radius):
        super().__init__(center_x, center_y, radius)
        self.color = GREEN

    def move (self, vector):
        self.center += vector
    
    def get_area(self) -> float:
        return 2 * math.pi * self.radius
    
    def draw(self, canvas):
        pygame.draw.circle(canvas, self.color, center=(self.center.x, self.center.y), radius=self.radius)
    
    '''@staticmethod
    def is_intersects(c1, c2, canvas):
        is_checked = super().is_intersects(c1, c2)
        pygame.draw.line(canvas, (0, 0, 0), (c1.center.x,c1.center.y), (c2.center.x,c2.center.y), 2)
        return is_checked'''