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
        self.vision_radius = 30

    def find_visible_boids(self, universe, dt):
        self.visible_boids = []
        for boid in universe.boids:
            if boid is not self:
                if (self.position - boid.position).magnitude() < self.vision_radius:
                    self.visible_boids.append(boid)

    def update_angular_velocity(self, universe, fps, dt, timestep):
        if timestep % int(fps / 5.0) == 0:
            self.find_visible_boids(universe, dt)
        pref_vector = Vector(0, 0)
        pref_vector += self.avoid_walls(universe, dt)
        pref_vector += self.separation(universe, dt)
        pref_vector += self.alignment(universe, dt)
        pref_vector += self.cohesion(universe, dt)
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
        return pref_vector * 100.0

    def separation(self, universe, dt):
        pref_vector = Vector(0, 0)
        for vb in self.visible_boids:
            pref_vector += (vb.position - self.position)*(-1.0 / (vb.position - self.position).magnitude()*100)
        return pref_vector * 1.7

    def alignment(self, universe, dt):
        pref_vector = Vector(0, 0)
        for vb in self.visible_boids:
            pref_vector += (vb.velocity*(1.0/vb.velocity.magnitude()) - self.velocity*(1.0/self.velocity.magnitude()))
        if len(self.visible_boids) > 0:
            pref_vector = pref_vector * (1.0 / len(self.visible_boids))
        return pref_vector * 50.0

    def cohesion(self, universe, dt):
        pref_vector = Vector(0, 0)
        for vb in self.visible_boids:
            pref_vector += (vb.position - self.position)
        if len(self.visible_boids) > 0:
            pref_vector = pref_vector
        return pref_vector * 6.0

    def update_velocity(self, universe, dt):
        self.velocity.set_angle(self.velocity.get_angle() + self.angular_velocity * dt)

    def update_position(self, universe, dt):
        self.position += self.velocity * dt
