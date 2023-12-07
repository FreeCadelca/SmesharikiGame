import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import StaticTile, Coin, Tile
from enemy import Enemy
from decoration import Sky, Lava, Clouds
from player import Player
from game_data import levels


class Level:
    def __init__(self, current_level, surface, create_overworld):
        # общая настройка
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # связь с overworld
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        self.player_on_ground = False

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
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'ground':
                        groud_tile_list = import_cut_graphics('../graphics/tiles/cracked_ground.png')
                        tile_surface = groud_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'flying_rocks':
                        flying_rocks_tile_list = import_cut_graphics('../graphics/tiles/flying_rocks.png')
                        tile_surface = flying_rocks_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'coins':
                        if val == '0': sprite = Coin(tile_size, x, y, '../graphics/coins/gold')
                        if val == '1': sprite = Coin(tile_size, x, y, '../graphics/coins/silver')
                    if type == 'enemy':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraint':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)
        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface)
                    self.player.add(sprite)

                if val == '1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def horizontal_movement_collision(self):
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
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def check_death(self):
        # игрок упал с платформы и ушёл под экран
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def run(self):
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

        # lava
        self.lava.draw(self.display_surface, self.world_shift)
