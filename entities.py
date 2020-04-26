'''Define all entities'''
import random
from abc import ABC as Interface
from abc import abstractmethod
import pygame
import numpy as np
from utilities import Vector


class IDynamic(Interface):
    @abstractmethod
    def update_position(self):
        pass

    @abstractmethod
    def update_velocity(self):
        pass


class Boid(IDynamic):

    def __init__(self, position, angle):
        self.image = pygame.transform.scale(pygame.transform.rotate(pygame.image.load('data/boid.png'), -90.0), (13, 8))
        self.width = self.image.get_rect()[2]
        self.hieght = self.image.get_rect()[3]
        self.position = position
        self.speed = 150
        self.velocity = Vector(self.speed, 0)
        self.velocity.set_angle(angle)
        self.angular_velocity = 0
        self.inerial_time = 0.2

    def update_angular_velocity(self, universe, dt):
        pref_vector = Vector(0, 0)
        pref_vector += self.avoid_walls(universe, dt)
        if pref_vector.magnitude() > 0.00001:
            angle_difference = (np.arccos((pref_vector.x*self.velocity.x + pref_vector.y*self.velocity.y) / (pref_vector.magnitude()*self.velocity.magnitude()))*360.0) / (2.0*np.pi)
            direction = (pref_vector.x*self.velocity.y - pref_vector.y*self.velocity.x) / (pref_vector.magnitude()*self.velocity.magnitude())
            self.angular_velocity = -np.sign(direction)*angle_difference / self.inerial_time
        else:
            self.angular_velocity = 0

    def avoid_walls(self, universe, dt):
        pref_vector = Vector(0, 0)
        if self.position.x - universe.resolution[0]*universe.walls < universe.walls*2000:
            pref_vector += Vector(1.0, 0.0)
        if universe.resolution[0]*(1.0 - universe.walls) - self.position.x < universe.walls*2000:
            pref_vector += Vector(-1.0, 0.0)
        if universe.resolution[1]*(1.0 - universe.walls) - self.position.y < universe.walls*2000:
            pref_vector += Vector(0.0, -1.0)
        if self.position.y - universe.resolution[1]*universe.walls < universe.walls*2000:
            pref_vector += Vector(0.0, 1.0)
        return pref_vector

    def update_velocity(self, universe, dt):
        self.velocity.set_angle(self.velocity.get_angle() + self.angular_velocity * dt)

    def update_position(self, universe, dt):
        self.position += self.velocity * dt
