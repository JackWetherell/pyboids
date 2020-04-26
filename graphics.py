'''Define the graphics, colors, and layout'''
from enum import Enum
import pygame
import entities


class Colors(Enum):
    '''Define at the possible directions'''
    BACKGROUND = (30, 0, 80)


def draw(universe, buffer):
    # draw the background
    buffer.fill(Colors.BACKGROUND.value)

    # draw the boids
    for boid in universe.boids:
        buffer.blit(pygame.transform.rotate(boid.image, -boid.velocity.get_angle()), tuple(boid.position))

    # draw the walls
    pygame.draw.rect(buffer, (0,0,0), (0, 0, universe.resolution[0]*universe.walls, universe.resolution[1]))
    pygame.draw.rect(buffer, (0,0,0), (universe.resolution[0]*(1.0 - universe.walls), 0, universe.resolution[0]*universe.walls, universe.resolution[1]))
    pygame.draw.rect(buffer, (0,0,0), (0, 0, universe.resolution[0], universe.resolution[1]*universe.walls))
    pygame.draw.rect(buffer, (0,0,0), (0, universe.resolution[1]*(1.0 - universe.walls), universe.resolution[0], universe.resolution[1]*universe.walls))
