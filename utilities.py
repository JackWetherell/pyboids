'''Define miscellaneous utilities'''
import copy
import numpy as np


class Vector:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        return Vector(x, y)

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __iter__(self):
        items = [self.x, self.y]
        for i in items:
            yield i

    def magnitude(self):
        return np.sqrt(self.x**2 + self.y**2)

    def set_angle(self, angle):
        angle = (angle * 2.0*np.pi) / 360.0
        magnitude = self.magnitude()
        self.x = magnitude * np.cos(angle)
        self.y = magnitude * np.sin(angle)

    def get_angle(self):
        angle = (np.arccos(self.x / self.magnitude())*360.0) / (2.0*np.pi)
        if self.y < 0:
            angle = 360.0 - angle
        return angle


def collision(entity1, entity2):
    try:
        rect1 = entity1.image.get_rect()
    except AttributeError:
        rect1 = copy.deepcopy(entity1.rect)
    try:
        rect2 = entity2.image.get_rect()
    except AttributeError:
        rect2 = copy.deepcopy(entity2.rect)
    rect1.move_ip(entity1.position.x, entity1.position.y)
    rect2.move_ip(entity2.position.x, entity2.position.y)
    return rect1.colliderect(rect2)
