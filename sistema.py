import numpy as np
import random

def addVectors(v1, v2):
    if len(v1) == len(v2):
        a = [0]* len(v1)
        for i in len(v1):
            a += v1[i] + v2[i]
        return a
    return False

def combine(p1, p2):
    if math.hypot(p1.x - p2.x, p1.y - p2.y) < p1.size + p2.size:
        total_mass = p1.mass + p2.mass
        p1.x = (p1.x*p1.mass + p2.x*p2.mass)/total_mass
        p1.y = (p1.y*p1.mass + p2.y*p2.mass)/total_mass
        (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed*p1.mass/total_mass), (p2.angle, p2.speed*p2.mass/total_mass))
        p1.speed *= (p1.elasticity*p2.elasticity)
        p1.mass += p2.mass
        p1.collide_with = p2

def collide(p1, p2):
    """ Tests whether two particles overlap
        If they do, make them bounce, i.e. update their angle, speed and position """
    
    dr = p1.r - p2.r
    dist = np.linalg.norm(dr)
    if dist < p1.size + p2.size:
        u1, u2 = p1.speed, p2.speed
        m1, m2 = p1.mass, p2.mass

        v1, v2 = 2*m2 * u2 + (m1-m2)*u1, 2*m1 * u1 + (m2-m1)*u2
        v1 *= p2.elasticity/(m1+m2)
        v2 *= p1.elasticity/(m1+m2)

        p1.speed = v1
        p2.speed = v2

        if p1.infected == 1 and p2.infected == 0:
            if random.random() < p1.probability:
                print('infecta')
                p2.infected = 1
                p2.colour = (255, 0, 0)

class Particle:
    """ Objeto circular con posición, velocidad, tamaño y masa"""

    def __init__(self, r, size, mass=1):
        self.r = np.array(r)
        self.infected = 0
        self.probability = 0.4
        self.size = size
        if self.infected == 1:
            print(self.infected)
            self.colour = (255, 0, 255)
        else:
            print(self.infected)
            self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = [0, 0]
        self.mass = mass
        self.drag = 1
        self.elasticity = 1



    def move(self):
        """ Actualiza la posición de la partícula"""
        self.r += self.speed

    def drag(self):
        """ Actualiza la velocidad de la partícula con 
        la resistencia viscosa"""
        #self.speed *= self.drag
        self.speed *= 1
    def accelerate(self, vector):
        """ Acelerar la partícula según un vector vector"""
        self.speed += vector

    

class Environment:
    """ Define la situación de la simulación"""
    def __init__(self, rectangle):

        self.width, self.height = rectangle
        self.particles = []

        self.colour = (255, 255, 255)

    def addParticles(self, n=1, **kargs):
        """ Añade n partículas en función de ciertas propiedades dadas por akrgs"""

        for i in range(n):
            size = kargs.get('size', random.randint(10, 20))
            mass = kargs.get('mass', random.randint(100, 10000))
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))
            infected = kargs.get('infected', 0)

            particle = Particle([x, y], size, mass)
            particle.infected = infected
            particle.speed = kargs.get('speed', 10*np.array([random.random(), random.random()])) 
            particle.colour = kargs.get('colour')
            particle.drag = particle.mass**particle.size

            self.particles.append(particle)

    def update(self):
       """ Actualiza el sistema"""

       for i, particle in enumerate(self.particles):
           particle.move()
           self.bounce(particle)
           #particle.drag()
           for particle2 in self.particles[i+1:]:
                collide(particle, particle2) 
    def bounce(self, particle):
        """ Tests whether a particle has hit the boundary of the environment """
        particle.x, particle.y = particle.r
        if particle.x > self.width - particle.size:
            particle.x = 2*(self.width - particle.size) - particle.x
            particle.speed[0] *= -1
            particle.speed *= particle.elasticity

        elif particle.x < particle.size:
            particle.x = 2*particle.size - particle.x
            particle.speed[0] *= -1
            particle.speed *= particle.elasticity

        if particle.y > self.height - particle.size:
            particle.y = 2*(self.height - particle.size) - particle.y
            particle.speed[1] *= -1
            particle.speed *= particle.elasticity

        elif particle.y < particle.size:
            particle.y = 2*particle.size - particle.y
            particle.speed[1] *= -1
            particle.speed *= particle.elasticity

    def findParticle(self, x, y):
        """ Returns any particle that occupies position x, y """
        
        for particle in self.particles:
            if math.hypot(particle.x - x, particle.y - y) <= particle.size:
                return particle
        return None
