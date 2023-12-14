import pygame
from code_with_decoration.support import import_folder


class Tile(pygame.sprite.Sprite):
    """
    Represents a basic tile in the game.

    Attributes:
    - image (pygame.Surface): The surface representing the tile.
    - rect (pygame.Rect): The rectangle that defines the position and size of the tile.

    Methods:
    - __init__(self, size, x, y): Initializes a new Tile instance.
    - update(self, shift): Updates the position of the tile with a horizontal shift.
    """
    def __init__(self, size, x, y):
        """
        Initializes a new Tile instance.

        Parameters:
        - size (int): The size of the tile.
        - x (int): The initial x-coordinate of the tile.
        - y (int): The initial y-coordinate of the tile.
        """
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        """
        Updates the position of the tile with a horizontal shift.

        Parameters:
        - shift (int): The horizontal shift applied to the tile.
        """
        self.rect.x += shift


class StaticTile(Tile):
    """
    Represents a static tile in the game with a fixed image.

    Attributes:
    - image (pygame.Surface): The fixed surface representing the static tile.

    Methods:
    - __init__(self, size, x, y, surface): Initializes a new StaticTile instance.
    """
    def __init__(self, size, x, y, surface):
        """
        Initializes a new StaticTile instance.

        Parameters:
        - size (int): The size of the static tile.
        - x (int): The initial x-coordinate of the static tile.
        - y (int): The initial y-coordinate of the static tile.
        - surface (pygame.Surface): The fixed surface representing the static tile.
        """
        super().__init__(size, x, y)
        self.image = surface


class AnimatedTiles(Tile):
    """
    Represents an animated tile in the game.

    Attributes:
    - frames (list): A list containing frames of the animation.
    - frame_index (float): The current frame index for animation.

    Methods:
    - __init__(self, size, x, y, path): Initializes a new AnimatedTiles instance.
    - animate(self): Animates the tile by changing its image.
    - update(self, shift): Updates the position and animation of the tile with a horizontal shift.
    """
    def __init__(self, size, x, y, path):
        """
        Initializes a new AnimatedTiles instance.

        Parameters:
        - size (int): The size of the animated tile.
        - x (int): The initial x-coordinate of the animated tile.
        - y (int): The initial y-coordinate of the animated tile.
        - path (str): The path to the folder containing frames for animation.
        """
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        """
        Animates the tile by changing its image.
        """
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        """
        Updates the position and animation of the tile with a horizontal shift.

        Parameters:
        - shift (int): The horizontal shift applied to the tile.
        """
        self.animate()
        self.rect.x += shift


class Coin(AnimatedTiles):
    """
    Represents a coin object in the game.

    Attributes:
    - value (int): The value of the coin.

    Methods:
    - __init__(self, size, x, y, path, value): Initializes a new Coin instance.
    """
    def __init__(self, size, x, y, path, value):
        """
        Initializes a new Coin instance.

        Parameters:
        - size (int): The size of the coin.
        - x (int): The initial x-coordinate of the coin.
        - y (int): The initial y-coordinate of the coin.
        - path (str): The path to the folder containing frames for coin animation.
        - value (int): The value of the coin.
        """
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.value = value
