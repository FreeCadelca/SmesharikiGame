import pygame, sys
from settings import *
from create_path_on_platform import *
from level import Level
from overworld import Overworld
from ui import UI
import moviepy.editor

class Game:
    """
    The Game class manages the overall game state, including overworld and level transitions, player attributes,
    audio, user interface, and the main game loop.

    Attributes:
    - max_level (int): Maximum level of the game.
    - max_health (int): Maximum health of the player.
    - cur_health (int): Current health of the player.
    - coins (int): Player's coin count.
    - level_music (pygame.mixer.Sound): Sound object for level music.
    - overworld_music (pygame.mixer.Sound): Sound object for overworld music.
    - overworld (Overworld): Instance of the Overworld class.
    - status (str): Current game state ('overworld' or 'level').
    - ui (UI): Instance of the UI class.

    Methods:
    - __init__(self): Initializes the game with default attributes and creates instances of the necessary classes.
    - create_level(self, current_level): Creates a new level with the specified level number.
    - create_overworld(self, current_level, new_max_level): Creates a new overworld with the specified parameters.
    - change_coins(self, amount): Updates the coin count by the specified amount.
    - change_health(self, amount): Updates the player's health by the specified amount.
    - check_game_over(self): Checks if the player's health is zero and resets the game if necessary.
    - run(self): Executes the game loop based on the current game status.
    """
    def __init__(self):
        """
        Initializes the Game class with default attributes and creates instances of the necessary classes.
        """
        # game attributes
        self.max_level = 2
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # audio
        self.level_music = pygame.mixer.Sound(create_path_on_platform('./audio/level_music.wav'))
        #
        self.overworld_music = pygame.mixer.Sound(create_path_on_platform('./audio/overworld_music.wav'))
        #

        # метод запуска overworld creation
        self.overworld = Overworld(1, self.max_level, screen, self.create_level)
        # для переключения между двумя различными состояниями игры: overworld or level
        self.status = 'overworld'
        self.overworld_music.play(loops=-1)
        self.overworld_music.set_volume(-0.5)

        # user interface
        self.ui = UI(screen)



    def create_level(self, current_level):
        """
        Creates a new level with the specified level number.

        Args:
        - current_level (int): The current level number.
        """
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_music.stop()
        self.level_music.play(loops=-1)
        self.level_music.set_volume(0.25)

    def create_overworld(self, current_level, new_max_level):
        """
        Creates a new overworld with the specified parameters.

        Args:
        - current_level (int): The current level number.
        - new_max_level (int): The new maximum level unlocked.
        """
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.level_music.stop()
        self.overworld_music.play(-1)
        self.overworld_music.set_volume(-0.5)


    def change_coins(self, amount):
        """
        Updates the coin count by the specified amount.

        Args:
        - amount (int): The amount to change the coin count.
        """
        self.coins += amount

    def change_health(self, amount):
        """
        Updates the player's health by the specified amount.

        Args:
        - amount (int): The amount to change the player's health.
        """
        self.cur_health += amount

    def check_game_over(self):
        """
        Checks if the player's health is zero and resets the game if necessary.
        """
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'

    def run(self):
        """
        Executes the main game loop based on the current game status.
        """
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, 100)
            self.ui.show_coins(self.coins)
            self.check_game_over()

# Pygame setup

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()
video = moviepy.editor.VideoFileClip(create_path_on_platform("./intro.mp4"))
intro = video.resize((screen_width, screen_height))
intro.preview()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)
