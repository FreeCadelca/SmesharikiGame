import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height
from tiles import StaticTile, Coin, Tile
from enemy import Enemy
from decoration import Sky, Lava, Clouds


class Level:
    def __init__(self, level_data, surface):
        # общая настройка
        self.display_surface = surface
        self.world_shift = -6

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

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
        self.lava = Lava(screen_height - 30, level_width)
        self.clouds = Clouds(400, level_width, 20)

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
                    print('player goes here')
                if val == '1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

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
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # lava
        self.lava.draw(self.display_surface, self.world_shift)
