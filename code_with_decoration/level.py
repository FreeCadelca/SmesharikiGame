import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from create_path_on_platform import *
from tiles import StaticTile, Coin, Tile
from enemy import Enemy
from decoration import Sky, Lava, Clouds
from player import Player
from game_data import levels
from particles import ParticEffect

class Level:
    """
    The Level class manages individual game levels, handling player setup, tile groups, collisions,
    and various game elements.

    Attributes:
    - display_surface (pygame.Surface): Pygame surface for rendering the level.
    - world_shift (int): Horizontal shift for scrolling the level.
    - current_x (int): Current x-coordinate of the player.
    - coin_sound (pygame.mixer.Sound): Sound object for coin collection.
    - stomp_sound (pygame.mixer.Sound): Sound object for enemy stomping.
    - create_overworld (function): Callback function to create the overworld.
    - current_level (int): Current level number.
    - new_max_level (int): New maximum level unlocked.
    - player (pygame.sprite.GroupSingle): Pygame sprite group for the player.
    - goal (pygame.sprite.GroupSingle): Pygame sprite group for the level goal.
    - player_on_ground (bool): Flag indicating if the player is on the ground.
    - change_coins (function): Callback function to change the coin count.
    - explosion_sprites (pygame.sprite.Group): Pygame sprite group for explosion particles.
    - ground_sprites (pygame.sprite.Group): Pygame sprite group for ground tiles.
    - flying_rocks_sprites (pygame.sprite.Group): Pygame sprite group for floating rocks.
    - coins_sprites (pygame.sprite.Group): Pygame sprite group for coins.
    - enemy_sprites (pygame.sprite.Group): Pygame sprite group for enemies.
    - constraint_sprites (pygame.sprite.Group): Pygame sprite group for constraint tiles.
    - sky (Sky): Instance of the Sky class for sky decoration.
    - lava (Lava): Instance of the Lava class for lava decoration.
    - clouds (Clouds): Instance of the Clouds class for cloud decoration.

    Methods:
    - __init__(self, current_level, surface, create_overworld, change_coins, change_health):
        Initializes the level with the specified parameters.
    - create_tile_group(self, layout, type):
        Creates a Pygame sprite group based on the layout and type.
    - player_setup(self, layout, change_health):
        Sets up the player and the goal based on the layout.
    """
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health):
        """
        Initializes the Level class with the specified parameters.

        Args:
        - current_level (int): The current level number.
        - surface (pygame.Surface): The surface for rendering the level.
        - create_overworld (function): Callback function to create the overworld.
        - change_coins (function): Callback function to change the coin count.
        - change_health (function): Callback function to change the player's health.
        """
        # общая настройка
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # audio
        self.coin_sound = pygame.mixer.Sound(create_path_on_platform('./audio/effects/coin.wav'))
        self.coin_sound.set_volume(0.25)
        self.stomp_sound = pygame.mixer.Sound(create_path_on_platform('./audio/effects/stomp.wav'))
        self.stomp_sound.set_volume(0.25)

        # связь с overworld
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)
        self.player_on_ground = False


        #user interface
        self.change_coins = change_coins

        # explosion particles
        self.explosion_sprites = pygame.sprite.Group()

        # настройка земной поверхности
        ground_layout = import_csv_layout(level_data['ground'])  # планировка местности
        self.ground_sprites = self.create_tile_group(ground_layout, 'ground')
        # т к мы хотим разграничить, какой идентификатор принадлежит какой плитке

        # настройка парящих арок
        flying_rocks_layout = import_csv_layout((level_data['flying_rocks']))
        self.flying_rocks_sprites = self.create_tile_group(flying_rocks_layout, 'flying_rocks')

        # coins
        coins_layout = import_csv_layout((level_data['coins']))
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemy'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemy')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

        # decoration
        self.sky = Sky(8)
        level_width = len(ground_layout[0]) * tile_size
        self.lava = Lava(screen_height - 40, level_width)
        self.clouds = Clouds(400, level_width, 30)

    def create_tile_group(self, layout, type):
        """
        Creates a Pygame sprite group based on the layout and type.

        Args:
        - layout (list): The layout of the tiles.
        - type (str): The type of tiles to create.

        Returns:
        - pygame.sprite.Group: The created sprite group.
        """
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'ground':
                        groud_tile_list = import_cut_graphics(
                            create_path_on_platform('./graphics/tiles/cracked_ground.png')
                        )
                        tile_surface = groud_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'flying_rocks':
                        flying_rocks_tile_list = import_cut_graphics(
                            create_path_on_platform('./graphics/tiles/flying_rocks.png')
                        )
                        tile_surface = flying_rocks_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'coins':
                        if val == '0': sprite = Coin(
                            tile_size, x, y, create_path_on_platform('./graphics/coins/gold'), 5
                        )
                        if val == '1': sprite = Coin(
                            tile_size, x, y, create_path_on_platform('./graphics/coins/silver'), 1
                        )
                    if type == 'enemy':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)
        return sprite_group

    def player_setup(self, layout, change_health):
        """
        Sets up the player and the goal based on the layout.

        Args:
        - layout (list): The layout for player and goal placement.
        - change_health (function): Callback function to change the player's health.
        """
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, change_health)
                    self.player.add(sprite)

                if val == '1':
                    hat_surface = (pygame.image.load(create_path_on_platform('./graphics/character/hat.png'))
                                   .convert_alpha())
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        """
        Reverses the direction of enemies when they collide with constraints.
        """
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def horizontal_movement_collision(self):
        """
        Handles horizontal movement collisions for the player.
        """
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        # спрайты для столкновения
        collidable_sprites = self.ground_sprites.sprites() + self.flying_rocks_sprites.sprites()
        for sprite in collidable_sprites:
            # столкновение игрока и блока
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        # not nessesary (nn) - не вижу разницы
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right < self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        """
        Handles vertical movement collisions for the player.
        """
        player = self.player.sprite
        player.apply_gravity()
        # спрайты для столкновения
        collidable_sprites = self.ground_sprites.sprites() + self.flying_rocks_sprites.sprites()
        for sprite in collidable_sprites:
            # столкновение игрока и блока
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0  # установили, чтобы персонаж не падал вниз в статичном состоянии под силой тяжести
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0  # чтобы персонаж не лип к потолку
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    # камера
    def scroll_x(self):
        """
        Scrolls the screen horizontally based on player movement.
        """
        player = self.player.sprite
        # нахождение игрока по координате Х
        player_x = player.rect.centerx
        # направление движения игрока
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def get_player_on_ground(self):
        """
        Updates the player's on_ground status.
        """
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def check_death(self):
        """
        Checks if the player fell off the platform and went off-screen.
        """
        # игрок упал с платформы и ушёл под экран
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        """
        Checks if the player collides with the goal, triggering a level transition.
        """
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collisions(self):
        """
        Checks for collisions between the player and coins, updating the coin count.
        """
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)


    def check_enemy_collisions(self):
        """
        Checks for collisions between the player and enemies, handling damage or stomping effects.
        """
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    enemy.kill()
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticEffect(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                else:
                    self.player.sprite.get_damage()

    def run(self):
        """
        Runs the main loop for the level, updating and rendering game elements.
        """
        # decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        self.ground_sprites.update(self.world_shift)
        self.ground_sprites.draw(self.display_surface)

        # парящие арки
        self.flying_rocks_sprites.update(self.world_shift)
        self.flying_rocks_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)
        # coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()
        self.check_coin_collisions()
        self.check_enemy_collisions()
        # lava
        self.lava.draw(self.display_surface, self.world_shift)

