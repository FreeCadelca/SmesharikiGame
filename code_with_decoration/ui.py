import pygame
from create_path_on_platform import *


class UI:
    """
    Represents the user interface elements in the game.

    Attributes:
    - display_surface (pygame.Surface): The surface on which UI elements are displayed.
    - health_bar (pygame.Surface): The image of the health bar.
    - health_bar_topleft (tuple): The top-left position of the health bar.
    - bar_max_width (int): The maximum width of the health bar.
    - bar_height (int): The height of the health bar.
    - coin (pygame.Surface): The image of the coin.
    - coin_rect (pygame.Rect): The rectangle defining the position and size of the coin image.
    - font (pygame.font.Font): The font used for rendering text on the UI.

    Methods:
    - __init__(self, surface): Initializes a new UI instance.
    - show_health(self, current, full): Displays the health bar on the UI.
    - show_coins(self, amount): Displays the coin image and amount on the UI.
    """
    def __init__(self, surface):
        """
        Initializes a new UI instance.

        Parameters:
        - surface (pygame.Surface): The surface on which UI elements are displayed.
        """
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load(create_path_on_platform('./graphics/ui/health_bar.png')).convert_alpha()
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # coins
        self.coin = pygame.image.load(create_path_on_platform('./graphics/ui/coin.png')).convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))
        self.font = pygame.font.Font(create_path_on_platform('./graphics/ui/ARCADEPI.ttf'), 30)

    def show_health(self, current, full):
        """
        Displays the health bar on the UI.

        Parameters:
        - current (int): The current health value.
        - full (int): The maximum health value.
        """
        self.display_surface.blit(self.health_bar, (20, 10))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def show_coins(self, amount):
        """
        Displays the coin image and amount on the UI.

        Parameters:
        - amount (int): The current amount of coins.
        """
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, '#000000')
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)
