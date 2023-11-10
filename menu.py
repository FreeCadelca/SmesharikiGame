import pygame


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('../graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos


class Bar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.selected = 0


class BarInMain(Bar):
    def __init__(self):
        super().__init__()


class BarInSettings(Bar):
    def __init__(self):
        super().__init__()


# class BarInMainMenu(Bar):


class Menu:
    def __init__(self):
        self.current_bar = 0
        self.max_bar = 4
        self.current_section = 0

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            self.current_bar = (self.current_bar + 1) % self.max_bar
        elif keys[pygame.K_UP]:
            self.current_bar = (self.current_bar - 1) % self.max_bar

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    # def run(self):
