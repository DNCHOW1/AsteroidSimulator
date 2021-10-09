#!/usr/bin/python

from pygame.sprite import collide_circle


try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    import random
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print(f"Couldn't load module. {err}")
    sys.exit(2)

def load_png(name, size):
    location = os.path.join(os.getcwd(), f"{name}.png")
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
        pygame.sprite.Sprite.__init__(self)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect() # This would be the bounding area for the sprite
        size = random.randrange(20, 100, 15)
        self.image, self.rect = load_png("test", size)
        self.x, self.y = random.randint(0, self.area.width), random.randint(0, self.area.height)
        self.velocity = (random.uniform(-200, 200)/size, random.uniform(-200, 200)/size)
        self.size = size
        self.radius = 4*size/10
        self.rect.center = (self.x, self.y)
        
    def update(self, otherAst, grow=None):
        vx, vy = self.velocity
        newx, newy = self.x + vx, self.y + vy
        self.rect.center = (newx, newy)

        if not self.area.contains(self.rect): # Contains needs to be a rect style object
            screenW, screenH = self.area.width, self.area.height
            if newx < 0 or newx > screenW:
                newx = (screenW + newx) % screenW
            if newy < 0 or newy > screenH:
                newy = (screenH + newy) % screenH
        self.rect.center = (newx, newy)
        self.x, self.y = newx, newy
        '''
        if grow % 6 == 0: 
            self.size += 1
            self.image = pygame.transform.scale(self.image, (self.size, self.size))'''
        self.handleCollisions(otherAst, debug=True)

    def handleCollisions(self, otherAst, debug=False):

        collisions = pygame.sprite.spritecollide(self, otherAst, False, collided=collide_circle) # If collide with others, length will be >= 2
        if len(collisions) >= 2:
            if debug: pygame.draw.circle(pygame.display.get_surface(), "RED", (self.x, self.y), self.radius, width=2)

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
    for i in range(20):
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
        asteroid_group.update(asteroid_group, count) # Update the location for all sprites
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
