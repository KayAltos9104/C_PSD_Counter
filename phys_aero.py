import math
import pygame

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @staticmethod
    def mult_on_scalar(scalar, vector):
        return Vector2(vector.x * scalar, vector.y*scalar)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y
    
    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def __neg__(self):
        return Vector2(-self.x, -self.y)
    

class CircleCollider:
    def __init__(self, center_x, center_y, radius):
        self.center = Vector2(center_x, center_y)
        self.radius = radius
    
    @staticmethod
    def is_intersects (c1, c2):
        distance = abs(c2.center - c1.center)
        return distance < c1.radius + c2.radius

class Particle (CircleCollider):
    def __init__(self, center_x, center_y, radius):
        super().__init__(center_x, center_y, radius)
        self.color = (0, 255, 0)
    
    def draw(self, canvas):
        pygame.draw.circle(canvas, self.color, center=(self.center.x, self.center.y), radius= self.radius)
    
    @staticmethod
    def is_intersects(c1, c2, canvas):
        is_checked = super().is_intersects(c1, c2)
        pygame.draw.line(canvas, (0, 0, 0), (c1.center.x,c1.center.y), (c2.center.x,c2.center.y), 2)
        return is_checked