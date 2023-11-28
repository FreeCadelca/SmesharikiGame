import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size
from tiles import StaticTile, Coin, Tile


class Level:
    def __init__(self, level_data, surface):
        # общая настройка
        self.display_surface = surface
        self.world_shift = -1

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


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'ground':
                        groud_tile_list = import_cut_graphics('./graphics/tiles/cracked_ground.png')
                        tile_surface = groud_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'flying_rocks':
                        flying_rocks_tile_list = import_cut_graphics('./graphics/tiles/flying_rocks.png')
                        tile_surface = flying_rocks_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                    if type == 'coins':
                        if val =='0': sprite = Coin(tile_size, x, y, './graphics/coins/gold')
                        if val == '1': sprite = Coin(tile_size, x, y, './graphics/coins/silver')
                    sprite_group.add(sprite)
        return sprite_group

    def run(self):
        self.ground_sprites.update(self.world_shift)
        self.ground_sprites.draw(self.display_surface)

        # парящие арки
        self.flying_rocks_sprites.update(self.world_shift)
        self.flying_rocks_sprites.draw(self.display_surface)

        #coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)
