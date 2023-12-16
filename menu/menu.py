import pygame
from .Sections.MainMenuSection import MainMenuSection
from .Sections.AccountSection import AccountSection
from .Sections.SettingsSection import SettingsSection
from .Sections.AboutUsSection import AboutUsSection
from .Sections.LogInSection import LogInSection
from .Sections.SignInSection import SignInSection

from config import *
from Client import *

"""
Class that represents the menu.

Attributes:
    SECTIONS (list): a list of all the menu sections
    bars_sprites: list of bar sprites to update
    surface: a 2D surface for game visualisation
    id_current_section (int): the number of current section of the menu
    last_pressed_keys (dict): a dictionary representing the last keys pressed in the last frame. It is used to 
        get rid of duplicate key reading
    section (AbstractSection): the current section of the menu
    create_overworld (func): function passed from class Game that used to create the overworld in the game
    max_level (int): the maximum level in the game

Methods:
    init: Initializes the new Menu with surface, function create_overworld, max_level
    input: method to receive input from the user
    setup_bars: method to set up all the bars on the screen (surface)
    run: method to run (activate) the menu
"""


class Menu:
    SECTIONS = [MainMenuSection, AccountSection, SettingsSection, AboutUsSection, LogInSection, SignInSection]

    def __init__(self, surface, create_overworld, max_level=2):
        """
        The constructor for Menu class.

        Args:
            surface: surface for menu rendering
            create_overworld: function passed from class Game that used to create the overworld in the game
            max_level (int): the maximum level in the game
        """
        self.bars_sprites = None
        self.surface = surface
        self.id_current_section = 0
        """
        0: main_menu
        1: account
        2: settings
        3: about us
        4: log in
        5: sign in
        """
        self.last_pressed_keys = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_RETURN: False,
            pygame.K_ESCAPE: False
        }
        self.section = MainMenuSection()
        self.create_overworld = create_overworld
        self.max_level = max_level

    def input(self, events, client: Client):
        """
        Method to receive input from the players

        Args:
        events: list of events in pygame
        client (Client): the client object, that connected to the server
        """
        previous_section = self.id_current_section
        self.id_current_section = self.section.input(
            pygame.key.get_pressed(), self.last_pressed_keys, self.id_current_section, events, client)
        if self.id_current_section == -1:
            self.create_overworld(1, self.max_level)
        if previous_section != self.id_current_section:
            self.section = Menu.SECTIONS[self.id_current_section]()

    def setup_bars(self):
        """
        Method to set up the bars on the screen
        """
        cfg = config_parse()
        self.bars_sprites = pygame.sprite.Group()
        self.section.setup_bars(self.bars_sprites, cfg)

    def run(self, events, client: Client):
        """
        Method to run the menu
        """
        self.setup_bars()
        self.input(events, client)
        self.bars_sprites.update()
        self.bars_sprites.draw(self.surface)
