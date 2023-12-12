import pygame, sys
from screen_settings import *
from create_path_on_platform import *
from level import Level
from overworld import Overworld
from ui import UI
import moviepy.editor


class Game:
    def __init__(self):
        # game attributes
        self.max_level = 2
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # audio
        self.level_music = pygame.mixer.Sound(create_path_on_platform('./audio/level_music.wav'))
        self.overworld_music = pygame.mixer.Sound(create_path_on_platform('./audio/overworld_music.wav'))

        # метод запуска overworld creation
        self.overworld = Overworld(1, self.max_level, screen, self.create_level)
        # для переключения между двумя различными состояниями игры: overworld or level
        self.status = 'overworld'
        self.overworld_music.play(loops=-1)
        self.overworld_music.set_volume(-0.5)

        # user interface
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_music.stop()
        self.level_music.play(loops=-1)
        self.level_music.set_volume(0.25)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.level_music.stop()
        self.overworld_music.play(-1)
        self.overworld_music.set_volume(-0.5)

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'

    def run(self):
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
