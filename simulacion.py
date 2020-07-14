import matplotlib.pyplot as plt
import random
import pygame
import sistema

width, height = (400, 400)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Gas')

universe = sistema.Environment((width, height))
universe.colour = (0,0,0)

def calculateRadius(mass):
    return 0.5 * mass ** 0.5

n = 100
for p in range(n):
    particle_mass = random.randint(50, 400)
    particle_size = calculateRadius(particle_mass)
    universe.addParticles(mass=particle_mass, size=particle_size, colour=(255, 255, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    universe.update()
    screen.fill(universe.colour)

    for p in universe.particles:
        if p.size<2:
            pygame.draw.rect(screen, p.colour, (int(p.r[0]), int(p.r[1]), 2, 2))
        else:
            pygame.draw.circle(screen, p.colour, (int(p.r[0]), int(p.r[1])), int(p.size), 0)
    pygame.display.flip()

    
