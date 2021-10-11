#!/usr/bin/python

try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    import random
    import numpy as np
    import traceback
    from socket import *
    from pygame.locals import *
    from pygame.sprite import collide_circle
except ImportError as err:
    print(f"Couldn't load module. {err}")
    sys.exit(2)

def load_png(name, size):
    location = os.path.join(os.getcwd(), f"{name+str(1)}.png")
    try:
        image = pygame.image.load(location)
        if image.get_alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
    except pygame.error as message:
        print(f"Cannot load image: {name}.png")
        raise message
    print(f"{name}.png loaded successfully.")
    image = pygame.transform.scale(image, (size, size))
    return image, image.get_rect()

class TestAsteroid(pygame.sprite.Sprite):
    def __init__(self):
        boundSpeed = 50
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect() # This would be the bounding area for the sprite
        size = random.randrange(20, 100, 15)
        #size = 150 if random.randint(0, 1) else 20
        self.image, self.rect = load_png("test", size)
        #self.x, self.y = random.randint(0, self.area.width), random.randint(0, self.area.height)
        self.position = np.array((random.randint(0, self.area.width), random.randint(0, self.area.height)))
        self.size = size
        self.radius = 4*size/10
        self.velocity = np.array((random.uniform(-boundSpeed, boundSpeed)/size, 
                                  random.uniform(-boundSpeed, boundSpeed)/size))
        self.rect.center = self.position
        #self.velocity = (random.uniform(-200, 200)/size, random.uniform(-200, 200)/size)
        #self.rect.center = (self.x, self.y)
        
    def update(self, otherAst):
        newx, newy = np.add(self.position, self.velocity)
        self.rect.center = (newx, newy)

        if not self.area.contains(self.rect): # Contains needs to be a rect style object
            screenW, screenH = self.area.width, self.area.height
            if newx < 0 or newx > screenW:
                newx = (screenW + newx) % screenW
            if newy < 0 or newy > screenH:
                newy = (screenH + newy) % screenH
        self.rect.center = self.position = np.array((newx, newy))
        self.handleCollisions(otherAst, debug=True)

    def handleCollisions(self, otherAst, debug=False):

        collisions = pygame.sprite.spritecollide(self, otherAst, False, collided=collide_circle) # If collide with others, length will be >= 2
        if len(collisions) >= 2:
            if debug: pygame.draw.circle(pygame.display.get_surface(), "RED", self.position, self.radius, width=2)
            for sprite in collisions:
                if self != sprite:
                    self.velocity, sprite.velocity = self.calcElastic(self, sprite)

    def calcElastic(self, ast1, ast2):
        # Where size also refers to the mass of the object
        m1, v1, r1 = ast1.size, ast1.velocity, ast1.position
        m2, v2, r2 = ast2.size, ast2.velocity, ast2.position
        posDiff = r1 - r2
        velDiff = v1 - v2
        product1 = 2*m2 / (m1 + m2)
        product2 = np.dot(velDiff, posDiff) / np.linalg.norm(posDiff)**2
        newV1 = v1 - product1*product2*posDiff

        product1 = 2*m1 / (m1 + m2)
        product2 = np.dot(-velDiff, -posDiff) / np.linalg.norm(posDiff)**2
        newV2 = v2 - product1*product2*-posDiff
        return newV1, newV2

def main():
    # Initialise screen
    WIDTH, HEIGHT = 1200, 600
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Basic Pygame program')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Loading images has to be done after pygame is initialized and display is set
    #Stella = TestAsteroid(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.random())
    asteroid_group = pygame.sprite.Group()
    for i in range(25):
        ast = TestAsteroid()
        asteroid_group.add(ast)

    # Blit everything to the screen
    screen.blit(background, (0, 0))

    # Use to update the screen
    pygame.display.flip()

    # Event loop
    count = 1
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30) # Runs at 30 fps
        for event in pygame.event.get(): # If user clicks X, quits program
            if event.type == QUIT:
                running = False

        screen.blit(background, (0, 0)) # Erase the board(previous content)
        asteroid_group.update(asteroid_group) # Update the location for all sprites
        asteroid_group.draw(screen)

        pygame.display.flip() # Could use this or display.update()
                              # Update has added benefit of updating specific surfaces
        count += 1

if __name__ == '__main__': 
    try:
        main()
    except Exception as e:
        print(e)
    finally:
        sys.exit()
