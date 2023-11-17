import pygame


class IncrementBar(pygame.sprite.Sprite):
    BAR_HEIGHT = 75
    BAR_WIDTH = 500

    def __init__(self, name, pos, path, value):
        super().__init__()
        self.name = name
        self.pos = pos
        self.value = value
        self.image = pygame.image.load('source\\' + path)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render('Some Text', False, (0, 0, 0))
        self.image.blit(text_surface, (0, 0))
        self.rect.center = self.pos
