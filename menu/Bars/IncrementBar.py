import pygame


class IncrementBar(pygame.sprite.Sprite):
    BAR_HEIGHT = 75
    BAR_WIDTH = 500

    def __init__(self, name, pos, path, value=50):
        super().__init__()
        self.name = name
        self.pos = pos
        self.value = value
        self.max_value = 100
        self.image = pygame.image.load('source\\' + path)
        self.primary_image = pygame.image.load('source\\' + path)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.image = self.primary_image.copy()  # resetting the image to a state without rendering a number
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 50)
        text_surface = my_font.render(str(self.value), False, (0, 0, 0))
        self.image.blit(text_surface, (IncrementBar.BAR_WIDTH * 3 // 4, 0))
        # method.blit changes the current image,
        # so I store the original image as primary_image and reset it to it before each rendering
        self.rect.center = self.pos

    def increment_value(self, delta):
        self.value += delta
        if self.value > self.max_value:  # I can't write cyclic incrementing via % max_value
            self.value = 0  # so I should write this crutch(
        elif self.value < 0:
            self.value = 100
