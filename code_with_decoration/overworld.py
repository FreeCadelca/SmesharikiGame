import pygame
from code_with_decoration.game_data import levels
from code_with_decoration.support import import_folder
from code_with_decoration.decoration import Sky
from create_path_on_platform import *


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed, path):
        path = create_path_on_platform(path)
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == 'available':
            self.status = 'available'
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center=pos)

        # зона обнаружения столкновения
        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed / 2), self.rect.centery - (icon_speed / 2),
                                          icon_speed, icon_speed)

    def animate(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        # анимация только доступных лвл
        if self.status == 'available':
            self.animate()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0, 0))


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load(create_path_on_platform('./graphics/overworld/hat.png'))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos


class Overworld:
    def __init__(self, start_level, max_level, surface, create_level, create_menu):
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level
        self.create_menu = create_menu

        # movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8

        # sprites
        self.setup_nodes()
        self.setup_icon()
        self.sky = Sky(8)

        # time
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_lengh = 1000

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        # доступ к кортежу из словарей
        for index, node_data in enumerate(levels.values()):
            # убираю недоступные уровни, оставляю только доступные в соответствии с максимально достигнутым уровнем
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])
            self.nodes.add(node_sprite)

    # рисунок путей к уровням
    def draw_paths(self):
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
        # surface color fillcolor pounts line_width
        pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        # иконка будет отображается на позиции текущего уровня
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            # метод игрового класса вызываем из overworld
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)
            elif keys[pygame.K_ESCAPE]:
                self.create_menu()

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
        return (end - start).normalize()

    def update_icon_pos(self):
        # позиция иконки - определяется текущим уровнем
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_lengh:
                self.allow_input = True

    def run(self):
        self.input_timer()
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()

        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
