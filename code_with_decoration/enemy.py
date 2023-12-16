import pygame
from code_with_decoration.tiles import AnimatedTiles
from random import randint
from create_path_on_platform import *


class Enemy(AnimatedTiles):
    """
    Represents an enemy character in the game.

    Attributes:
    - speed (int): The speed of the enemy's movement.

    Methods:
    - __init__(self, size, x, y): Initializes a new Enemy instance.
    - move(self): Moves the enemy horizontally.
    - reverse_image(self): Reverses the image of the enemy based on its movement direction.
    - reverse(self): Reverses the movement direction of the enemy.
    - update(self, shift): Updates the position and animation of the enemy.
    """

    def __init__(self, size, x, y):
        """
        Initializes a new Enemy instance.

        Parameters:
        - size (int): The size of the enemy.
        - x (int): The initial x-coordinate of the enemy.
        - y (int): The initial y-coordinate of the enemy.
        """
        super().__init__(size, x, y, create_path_on_platform('./graphics/enemy/run'))
        # приземлила на землю enemy
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3, 5)

    def move(self):
        """
        Moves the enemy horizontally.
        """
        self.rect.x += self.speed

    def reverse_image(self):
        """
        Reverses the image of the enemy based on its movement direction.
        """
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        """
        Reverses the movement direction of the enemy.
        """
        self.speed *= -1

    def update(self, shift):
        """
        Updates the position and animation of the enemy.

        Parameters:
        - shift (int): The horizontal shift applied to the enemy.
        """
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
