import pygame
from tiles import AnimatedTiles
from random import randint


class Enemy(AnimatedTiles):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, './graphics/enemy/run')
        # приземлила на землю enemy
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3, 5)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)
    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()

