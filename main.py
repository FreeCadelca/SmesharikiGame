import pygame, sys
from settings import *
import cv2
import moviepy.editor

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([screen_width, screen_height])

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()
video = moviepy.editor.VideoFileClip("../SmesharikiGame/source/preview.mp4")
intro = video.resize((screen_width, screen_height))
intro.preview()
