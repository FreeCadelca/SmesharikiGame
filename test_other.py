import unittest

import pygame
from code_with_decoration.enemy import Enemy
from code_with_decoration.decoration import Sky, Lava
from code_with_decoration.tiles import AnimatedTiles
from code_with_decoration.screen_settings import screen_width, tile_size, screen_height
from code_with_decoration.level import Level
from code_with_decoration.particles import ParticEffect
from code_with_decoration.support import import_folder, import_csv_layout, import_cut_graphics, create_path_on_platform
from menu.Bars.DefaultBar import DefaultBar
from menu.Bars.IncrementBar import IncrementBar
from menu.Bars.LabelBar import LabelBar


class TestEnemy(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.NOFRAME)
        size = 30
        x = 100
        y = 200

        self.enemy = Enemy(size, x, y)

    def test_move(self):
        initial_x = self.enemy.rect.x

        self.enemy.move()

        # Check if the enemy has moved horizontally
        self.assertNotEqual(initial_x, self.enemy.rect.x)

    def test_reverse_image(self):
        initial_image = self.enemy.image

        self.enemy.reverse_image()

        # Check if the image is reversed
        flipped_image = pygame.transform.flip(initial_image, True, False)
        self.assertEqual(self.enemy.image.get_size(), flipped_image.get_size())

    def test_reverse(self):
        initial_speed = self.enemy.speed

        self.enemy.reverse()

        # Check if the speed is reversed
        self.assertEqual(self.enemy.speed, -initial_speed)

    def tearDown(self):
        pygame.quit()


class TestSky(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))  # Set an invisible window
        self.horizon_level = 200  # Set the horizon level as needed
        self.sky = Sky(self.horizon_level)

    def test_sky_initialization(self):
        # Check if the horizon is set correctly
        self.assertEqual(self.sky.horizon, self.horizon_level)

        # Check if the top image is loaded and scaled correctly
        self.assertIsInstance(self.sky.top, pygame.Surface)
        self.assertEqual(self.sky.top.get_width(), screen_width)
        self.assertEqual(self.sky.top.get_height(), tile_size * 11)

    def tearDown(self):
        pygame.quit()


class TestLava(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))  # Set an invisible window
        self.top_position = 300  # Set the top position as needed
        self.level_width = 1000  # Set the level width as needed

        self.lava = Lava(self.top_position, self.level_width)

    def test_lava_initialization(self):
        # Check if lava_sprites is a pygame.sprite.Group
        self.assertIsInstance(self.lava.lava_sprites, pygame.sprite.Group)

        # Check if lava_sprites contains AnimatedTiles instances
        for sprite in self.lava.lava_sprites.sprites():
            self.assertIsInstance(sprite, AnimatedTiles)

        # Check if the number of lava tiles is correct based on level_width and tile width
        lava_tile_width = 180
        expected_tile_amount = int((self.level_width + screen_width * 2) / lava_tile_width)
        self.assertEqual(len(self.lava.lava_sprites), expected_tile_amount)

    def tearDown(self):
        pygame.quit()


class TestLevel(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))  # Set an invisible window
        current_level = 1  # Set the current level as needed
        surface = pygame.Surface((screen_width, screen_height))
        self.create_overworld = lambda *args: None
        self.change_coins = lambda *args: None
        self.change_health = lambda *args: None
        self.game_over_func = lambda: None
        self.send_coins_to_database = lambda: None

        self.level = Level(current_level, surface, self.create_overworld, self.change_coins, self.change_health,
                           self.game_over_func, self.send_coins_to_database)

    def test_level_initialization(self):
        # Check if key attributes are initialized correctly
        self.assertIsInstance(self.level.display_surface, pygame.Surface)
        self.assertEqual(self.level.world_shift, 0)
        self.assertIsNone(self.level.current_x)
        self.assertIsInstance(self.level.player, pygame.sprite.GroupSingle)
        self.assertIsInstance(self.level.goal, pygame.sprite.GroupSingle)
        self.assertIsInstance(self.level.coins_sprites, pygame.sprite.Group)
        self.assertIsInstance(self.level.enemy_sprites, pygame.sprite.Group)
        self.assertIsInstance(self.level.sky, Sky)
        self.assertIsInstance(self.level.lava, Lava)

    # Add more test methods for other functionalities as needed

    def tearDown(self):
        pygame.quit()


class TestParticEffect(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))

        pos = (100, 200)  # Set the initial position as needed
        particle_type = 'explosion'

        self.partic_effect = ParticEffect(pos, particle_type)

    def test_partic_effect_initialization(self):
        # Check if key attributes are initialized correctly
        self.assertEqual(self.partic_effect.frame_index, 0)
        self.assertEqual(self.partic_effect.animation_speed, 0.5)
        self.assertIsInstance(self.partic_effect.frames, list)
        self.assertIsInstance(self.partic_effect.image, pygame.Surface)
        self.assertIsInstance(self.partic_effect.rect, pygame.Rect)

    def test_animate_method(self):
        # Call the animate method multiple times to simulate animation
        for _ in range(10):
            self.partic_effect.animate()

        # Check if the frame index increases and the image updates accordingly
        self.assertEqual(self.partic_effect.frame_index, 5)  # Adjust based on the animation speed
        self.assertIsInstance(self.partic_effect.image, pygame.Surface)

    def test_update_method(self):
        initial_x = self.partic_effect.rect.x

        # Call the update method with a shift
        self.partic_effect.update(5)

        # Check if the position and animation are updated with the given shift
        self.assertEqual(self.partic_effect.rect.x, initial_x + 5)
        self.assertIsInstance(self.partic_effect.image, pygame.Surface)

    def tearDown(self):
        pygame.quit()


class TestImportFunctions(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1))

    def test_import_folder(self):
        path = create_path_on_platform("./graphics/enemy/explosion")
        result = import_folder(path)
        self.assertIsInstance(result, list)
        for surface in result:
            self.assertIsInstance(surface, pygame.Surface)

    def test_import_csv_layout(self):
        path = create_path_on_platform("./levels/1/1_lvl_coins.csv")
        result = import_csv_layout(path)
        self.assertIsInstance(result, list)
        for row in result:
            self.assertIsInstance(row, list)

    def test_import_cut_graphics(self):
        path = create_path_on_platform("./graphics/enemy/setup_tile.png")
        result = import_cut_graphics(path)
        self.assertIsInstance(result, list)
        for cut_tile in result:
            self.assertIsInstance(cut_tile, pygame.Surface)

    def tearDown(self):
        pygame.quit()


class TestDefaultBar(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def test_init(self):
        bar = DefaultBar(
            'image',
            (screen_width // 2, screen_height // 2),
            "AboutUs.png"
        )
        self.assertIsInstance(bar.image, pygame.Surface)
        self.assertIsInstance(bar.rect, pygame.Rect)

    def test_update(self):
        bar = DefaultBar(
            'image',
            (screen_width // 2, screen_height // 2),
            "AboutUs.png"
        )

        new_pos = (200, 200)
        bar.pos = new_pos
        bar.update()

        self.assertEqual(bar.rect.center, new_pos)

    def tearDown(self):
        pygame.quit()


class TestIncrementBar(unittest.TestCase):

    def setUp(self):
        pygame.init()

    def test_initialization(self):
        # Test the initialization of IncrementBar
        bar = IncrementBar("TestBar", (0, 0), "Test", value=75, text_offset_x=10)

        self.assertEqual(bar.name, "TestBar")
        self.assertEqual(bar.text, "Test")
        self.assertEqual(bar.value, 75)
        self.assertEqual(bar.text_offset_x, 10)
        self.assertEqual(bar.max_value, 100)
        self.assertEqual(bar.rect.center, (0, 0))



class TestLabelBar(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_label_bar_creation(self):
        label = LabelBar("TestLabel", (100, 100), "Hello, Test!")

        self.assertEqual(label.name, "TestLabel")
        self.assertEqual(label.pos, (100, 100))
        self.assertEqual(label.text, "Hello, Test!")
        self.assertEqual(label.text_offset_x, 0)
        self.assertEqual(label.text_color, (255, 240, 0))
        self.assertEqual(label.font_size, 26)


if __name__ == '__main__':
    unittest.main()
