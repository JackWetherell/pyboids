'''Define the game mechanics and all possible states'''
import random
from enum import Enum
import pygame
import numpy as np
import entities
from utilities import Vector


class States(Enum):
    '''Define at the possible states the game can be in'''
    QUIT = 0
    MAIN = 1


class Universe():
    def __init__(self, resolution):
        self.state = States.MAIN
        self.resolution = resolution
        self.walls = 0.02
        self.count = 50
        self.boids = []
        for _ in range(self.count):
            position = Vector(np.random.random()*resolution[0]*0.80 + resolution[0]*0.10, np.random.random()*resolution[1]*0.80 + resolution[1]*0.10)
            angle = np.random.random()*360
            self.boids.append(entities.Boid(position, angle))

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = States.QUIT

    def update(self, resolution, fps, dt, timestep, time):
        for boid in self.boids:
            boid.update_angular_velocity(self, dt)
        for boid in self.boids:
            boid.update_velocity(self, dt)
        for boid in self.boids:
            boid.update_position(self, dt)
