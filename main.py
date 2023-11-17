import sys
import pygame
import moviepy.editor
from screen_data import *
from menu.menu import Menu


class Game:
    def __init__(self, status='menu'):
        self.status = status
        self.menu = Menu(screen)

    def run(self, events):
        if self.status == 'menu':
            self.menu.run(events)
        # else:
        #     self.level.run()
        #     self.ui.show_health(self.cur_health, self.max_health)
        #     self.ui.show_coins(self.coins)
        #     self.check_game_over()


pygame.init()
# video = moviepy.editor.VideoFileClip("source\\preview.mp4")
# video.preview()
# pygame.quit()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    game.run(events)
    
    pygame.display.update()
    clock.tick(60)
