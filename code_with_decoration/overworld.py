import pygame
from game_data import levels
from support import import_folder
from decoration import Sky
from create_path_on_platform import *


class Node(pygame.sprite.Sprite):
    """
    Represents a node on the Overworld map.

    Attributes:
    - frames (list): A list of images for animation.
    - frame_index (float): Index representing the current frame in the animation.
    - image (pygame.Surface): The current image of the node.
    - status (str): The status of the node ('available' or 'locked').
    - rect (pygame.Rect): The rectangular area occupied by the node on the screen.
    - detection_zone (pygame.Rect): The collision detection zone around the node.

    Methods:
    - __init__(self, pos, status, icon_speed, path): Initializes a new Node instance.
    - animate(self): Animates the node by updating the frame index and image.
    - update(self): Updates the node, applying animations and handling locked status tinting.
    """
    def __init__(self, pos, status, icon_speed, path):
        """
        Initializes a new Node instance.

        Parameters:
        - pos (tuple): The position (x, y) of the node on the Overworld map.
        - status (str): The status of the node ('available' or 'locked').
        - icon_speed (float): The speed of the player's icon on the Overworld map.
        - path (str): The path to the folder containing images for the node's animation.
        """
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
        """
        Animates the node by updating the frame index and image.
        """
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        """
        Updates the node, applying animations and handling locked status tinting.
        """
        # анимация только доступных лвл
        if self.status == 'available':
            self.animate()
        else:
            tint_surf = self.image.copy()
            tint_surf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0, 0))


class Icon(pygame.sprite.Sprite):
    """
    Represents the icon on the Overworld map.

    Attributes:
    - pos (tuple): The position of the icon.
    - image (pygame.Surface): The image of the icon.
    - rect (pygame.Rect): The rectangular area occupied by the icon on the screen.

    Methods:
    - __init__(self, pos): Initializes a new Icon instance.
    - update(self): Updates the position of the icon on the Overworld map.
    """
    def __init__(self, pos):
        """
        Initializes a new Icon instance.

        Parameters:
        - pos (tuple): The position (x, y) of the icon on the Overworld map.
        """
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load(create_path_on_platform('./graphics/overworld/hat.png'))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        """
        Updates the position of the icon on the Overworld map.
        """
        self.rect.center = self.pos


class Overworld:
    """
    Manages the Overworld map, nodes, and player icon.

    Attributes:
    - display_surface (pygame.Surface): The display surface where the Overworld is rendered.
    - max_level (int): The maximum level reached by the player.
    - current_level (int): The current level selected by the player.
    - create_level (function): A function to create a specific game level.
    - moving (bool): Indicates whether the icon is currently moving.
    - move_direction (pygame.math.Vector2): The direction of the icon's movement.
    - speed (int): The speed of the icon's movement.
    - nodes (pygame.sprite.Group): Sprite group containing nodes on the Overworld map.
    - icon (pygame.sprite.GroupSingle): Sprite group containing the player's icon on the Overworld.
    - sky (Sky): Instance of the Sky class for background decoration.
    - start_time (int): The time at which the input timer started.
    - allow_input (bool): Indicates whether input is currently allowed.
    - timer_length (int): The duration of the input timer (in milliseconds).

    Methods:
    - __init__(self, start_level, max_level, surface, create_level): Initializes a new Overworld instance.
    - setup_nodes(self): Initializes and sets up the nodes on the Overworld map based on the maximum level reached.
    - draw_paths(self): Draws paths between available nodes on the Overworld map.
    - setup_icon(self): Initializes and sets up the player's icon on the Overworld map.
    - input(self): Handles player input for navigating the Overworld map and creating game levels.
    - get_movement_data(self, target): Calculates the movement data for the player's icon.
    - update_icon_pos(self): Updates the position of the player's icon on the Overworld map during movement.
    - input_timer(self): Manages the input timer to control when player input is allowed.
    - run(self): Executes the main logic for updating the Overworld map, handling input, and rendering.
    """
    def __init__(self, start_level, max_level, surface, create_level):
        """
        Initializes a new Overworld instance.

        Parameters:
        - start_level (int): The initial level selected by the player.
        - max_level (int): The maximum level reached by the player.
        - surface (pygame.Surface): The display surface where the Overworld is rendered.
        - create_level (function): A function to create a specific game level.
        """
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

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
        """
        Initializes and sets up the nodes on the Overworld map based on the maximum level reached.
        """
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
        """
        Draws paths between available levels on the Overworld map.
        """
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
        # surface color fillcolor pounts line_width
        pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)

    def setup_icon(self):
        """
        Initializes and sets up the player's icon on the Overworld map.
        """
        self.icon = pygame.sprite.GroupSingle()
        # иконка будет отображается на позиции текущего уровня
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        """
        Handles player input for navigating the Overworld map and creating game levels.
        """
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

    def get_movement_data(self, target):
        """
        Calculates the movement data for the player's icon.

        Parameters:
        - target (str): The target direction ('next' or 'previous').

        Returns:
        - pygame.math.Vector2: The normalized vector representing the movement direction.
        """
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
        return (end - start).normalize()

    def update_icon_pos(self):
        """
        Updates the position of the player's icon on the Overworld map during movement.
        """
        # позиция иконки - определяется текущим уровнем
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def input_timer(self):
        """
        Manages the input timer to control when player input is allowed.
        """
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_lengh:
                self.allow_input = True

    def run(self):
        """
        Executes the main logic for updating the Overworld map, handling input, and rendering.
        """
        self.input_timer()
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()

        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
