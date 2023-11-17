import pygame


class DefaultBar(pygame.sprite.Sprite):
    BAR_HEIGHT = 75
    BAR_WIDTH = 500

    def __init__(self, name, pos, path):
        super().__init__()
        self.name = name
        self.pos = pos
        self.image = pygame.image.load('source\\' + path)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos
        # print("hello")
