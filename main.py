import pygame
import engine
import graphics


def main(resolution, fps):
    # initialse pygame
    pygame.init()

    # set up frame rate
    clock = pygame.time.Clock()
    dt = 1.0 / float(fps)
    timestep = 0
    time = 0.0

    # create the buffer and display
    buffer = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Boids')
    pygame.display.set_icon(pygame.image.load('data/boid.png'))

    # enable smooth controls
    pygame.key.set_repeat(10,10)

    # initialse the game
    universe = engine.Universe(resolution)

    # main game loop
    while universe.state is not engine.States.QUIT:
        universe.check_input()
        universe.update(resolution, fps, dt, timestep, time)
        graphics.draw(universe, buffer)
        pygame.display.flip()
        clock.tick(fps)
        timestep += 1
        time += dt


if __name__ == '__main__':
    main(resolution=(1000, 700), fps=120)
