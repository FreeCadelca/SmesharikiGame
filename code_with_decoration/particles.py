import pygame
from support import import_folder
from create_path_on_platform import *


class ParticEffect(pygame.sprite.Sprite):
    """
    Represents a particle effect in the game.

    Attributes:
    - frame_index (float): The current frame index for animation.
    - animation_speed (float): The speed of the animation.
    - frames (list): A list containing frames of the particle effect animation.

    Methods:
    - __init__(self, pos, type): Initializes a new ParticEffect instance.
    - animate(self): Animates the particle effect.
    - update(self, x_shift): Updates the position and animation of the particle effect.
    """
    def __init__(self, pos, type):
        """
        Initializes a new ParticEffect instance.

        Parameters:
        - pos (tuple): The initial position (x, y) of the particle effect.
        - type (str): The type of particle effect ('explosion' for now).
        """
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        if type == 'explosion':
            self.frames = import_folder(create_path_on_platform('./graphics/enemy/explosion'))
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        """
        Animates the particle effect.
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        """
        Updates the position and animation of the particle effect.

        Parameters:
        - x_shift (int): The horizontal shift applied to the particle effect.
        """
        self.animate()
        self.rect.x += x_shift
