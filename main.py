import pygame, sys
from code_with_decoration.screen_settings import *
from create_path_on_platform import *
from code_with_decoration.level import Level
from code_with_decoration.overworld import Overworld
from code_with_decoration.ui import UI
import moviepy.editor
from Client import Client
from menu.menu import Menu
from config import *


class Game:
    def __init__(self, client: Client, status='menu'):
        """
        Instantiates a new 'Game' object.

        Args:
            client (Client): The client object.
            status (str, optional): The status of the game. Defaults to 'menu'.
        """
        # game attributes
        self.max_level = 2
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0
        self.status = status
        self.client = client

        # audio
        self.level_music = pygame.mixer.Sound(create_path_on_platform('./audio/level_music.wav'))
        self.overworld_music = pygame.mixer.Sound(create_path_on_platform('./audio/overworld_music.wav'))

        # user interface
        self.ui = UI(screen)

        # start menu
        self.create_menu()

    def create_level(self, current_level):
        """
        Create a level in the game.

        Args:
            current_level: The current level of the game.
        """
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health,
                           self.game_over, self.send_coins_to_database)
        self.status = 'level'
        self.overworld_music.stop()
        self.level_music.play(loops=-1)
        self.level_music.set_volume(config_parse()["Music volume"] / 100)

    def create_menu(self):
        """
        Create a menu for the game.
        If previous status was 'overworld', turn off music
        """
        if self.status == 'overworld':
            self.overworld_music.stop()
        self.status = 'menu'
        self.menu = Menu(screen, self.create_overworld, self.max_level)

    def create_overworld(self, current_level, new_max_level):
        """
        Create an overworld for the game.

        Args:
            current_level: The current level of the game.
            new_max_level: The new maximum level of the game.
        """
        self.max_level = max(self.max_level, new_max_level)
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level, self.create_menu)
        self.status = 'overworld'
        self.level_music.stop()
        self.overworld_music.play(loops=-1)
        self.overworld_music.set_volume(config_parse()["Music volume"] / 100)

    def change_coins(self, amount):
        """
        Change the coins in the game.

        Args:
            amount: The number of coins to change to
        """
        self.coins += amount

    def change_health(self, amount):
        """
        Change the health in the game.

        Args:
            amount: The amount of health to change to
        """
        self.cur_health += amount

    def check_game_over(self):
        """
        Check if the game is over.
        """
        if self.cur_health <= 0:
            self.game_over()

    def game_over(self):
        """
        Method for end the game. It updates coins on server and creates overworld
        """
        self.send_coins_to_database()
        self.cur_health = 100
        self.coins = 0
        self.overworld = Overworld(0, self.max_level, screen, self.create_level, self.create_menu)
        self.status = 'overworld'
        self.level_music.stop()
        self.overworld_music.play(-1)
        self.overworld_music.set_volume(config_parse()["Music volume"] / 100)

    def send_coins_to_database(self):
        """
        Update coins in the database.
        """
        config_edit(['coins'], self.coins + config_parse()['coins'])
        response = client.request_to_server(
            json.dumps(
                {
                    'msg': f'UpdateCoins',
                    'cfg': json.dumps(config_parse())
                }
            )
        )

    def run(self, events):
        """
        Run the game.

        Args:
            events: The events being run in the game.
        """
        if self.status == 'menu':
            self.menu.run(events, self.client)
        elif self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, 100)
            self.ui.show_coins(self.coins)
            self.check_game_over()


client = Client('127.0.0.1', 1234)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game(client)

video = moviepy.editor.VideoFileClip(create_path_on_platform("./intro.mp4"))
intro = video.resize((screen_width, screen_height))
intro.preview()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('white')
    game.run(events)

    pygame.display.update()
    clock.tick(60)
