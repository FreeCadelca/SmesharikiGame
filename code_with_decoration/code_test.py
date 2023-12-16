from code_with_decoration.overworld import Icon
from code_with_decoration.overworld import Overworld
from code_with_decoration.tiles import AnimatedTiles
import os
from code_with_decoration.tiles import Tile
import unittest
from code_with_decoration.overworld import Node
import pygame
from create_path_on_platform import *


class TestTile(unittest.TestCase):
    def test_init(self):
        size = 30
        x = 100
        y = 200
        tile = Tile(size, x, y)
        tile.__init__(size, x, y)
        self.assertEqual(tile.rect.topleft, (x, y))
        self.assertEqual(tile.rect.size, (size, size))

    def test_update(self):
        shift = 5
        x = 100
        y = 200
        size = 30
        tile = Tile(size, x, y)
        tile.__init__(size, x, y)
        initial_x = tile.rect.x
        tile.update(shift)
        self.assertEqual(tile.rect.x, initial_x + shift)


if __name__ == '__main__':
    pygame.init()
    unittest.main()


class TestAnimatedTiles(unittest.TestCase):
    def test_init(self):
        pygame.display.init()
        pygame.display.set_mode((1, 1))
        size = 30
        x = 100
        y = 200
        path = create_path_on_platform('./graphics/tiles/lava')  # Замените на путь к вашей папке с анимацией
        animated_tile = AnimatedTiles(size, x, y, path)
        animated_tile.__init__(size, x, y, path)
        self.assertEqual(len(animated_tile.frames),  # Проверяем, что список кадров не пустой
                         len(os.listdir(path)))
        self.assertEqual(animated_tile.frame_index, 0)  # Проверяем, что начальный индекс кадра равен 0
        self.assertEqual(animated_tile.image,
                         animated_tile.frames[0])  # Проверяем, что изображение соответствует начальному кадру

    def test_update(self):
        size = 30
        x = 100
        y = 200
        shift = 5
        path = create_path_on_platform('./graphics/tiles/lava')  # Замените на путь к вашей папке с анимацией
        animated_tile = AnimatedTiles(size, x, y, path)
        animated_tile.__init__(size, x, y, path)
        initial_x = animated_tile.rect.x
        initial_frame_index = animated_tile.frame_index
        animated_tile.update(shift)
        self.assertEqual(animated_tile.rect.x, initial_x + shift)  # Проверяем, что позиция обновилась с учетом сдвига
        self.assertEqual(animated_tile.frame_index,
                         initial_frame_index + 0.15)  # Проверяем, что индекс анимации обновился на 0.15


if __name__ == '__main__':
    pygame.init()  # инициализируем pygame для запуска тестов
    unittest.main()

import unittest

from code_with_decoration.tiles import Coin


class TestCoin(unittest.TestCase):
    def setUp(self):
        # Здесь вы можете создать начальные объекты или переменные, необходимые для вашего теста
        self.size = 20
        self.x = 100
        self.y = 100
        self.path = create_path_on_platform('./graphics/coins/gold')
        self.value = 10

    def test_coin_initialization(self):
        # Проверка инициализации монеты
        coin = Coin(self.size, self.x, self.y, self.path, self.value)

        # Проверяем, что координаты монеты и её значение устанавливаются правильно
        self.assertEqual(coin.rect.center, (self.x + int(self.size / 2), self.y + int(self.size / 2)),
                         "Неправильные координаты монеты")
        self.assertEqual(coin.value, self.value, "Неправильное значение монеты")

    def test_animate_method(self):
        # Проверка метода animate
        coin = Coin(self.size, self.x, self.y, self.path, self.value)


if __name__ == '__main__':
    unittest.main()


class TestNode(unittest.TestCase):
    def test_init(self):
        pygame.init()
        test_pos = (100, 100)
        test_status = 'available'
        test_icon_speed = 5.0
        test_path = create_path_on_platform('./graphics/overworld/0')
        node = Node(test_pos, test_status, test_icon_speed, test_path)
        node.__init__(test_pos, test_status, test_icon_speed, test_path)
        self.assertIsInstance(node.frames, list)
        self.assertEqual(node.frame_index, 0)
        self.assertIsInstance(node.image, pygame.Surface)
        self.assertEqual(node.status, 'available')
        self.assertEqual(node.rect.center, test_pos)
        self.assertIsInstance(node.detection_zone, pygame.Rect)

    def test_animate(self):
        test_pos = (100, 100)
        test_status = 'available'
        test_icon_speed = 5.0
        test_path = create_path_on_platform('./graphics/overworld/0')
        node = Node(test_pos, test_status, test_icon_speed, test_path)
        node.__init__(test_pos, test_status, test_icon_speed, test_path)
        old_frame_index = node.frame_index
        node.animate()
        self.assertNotEqual(node.frame_index, old_frame_index)
        self.assertIn(node.image, node.frames)

    def test_update(self):
        test_pos = (100, 100)
        test_status = 'available'
        test_icon_speed = 5.0
        test_path = create_path_on_platform('./graphics/overworld/0')
        node = Node(test_pos, test_status, test_icon_speed, test_path)
        node.__init__(test_pos, test_status, test_icon_speed, test_path)
        node.update()
        self.assertIn(node.image.get_at((0, 0)),
                      [(0, 0, 0, 0)])  # test if the image is tinted black for a locked status


if __name__ == '__main__':
    unittest.main()


class TestIcon(unittest.TestCase):

    def test_update(self):
        test_pos = (1, 5)
        icon = Icon(test_pos)
        icon.pos = (200, 200)
        icon.update()
        self.assertEqual(icon.rect.center, (200, 200))


if __name__ == '__main__':
    unittest.main()


class TestOverworld(unittest.TestCase):

    def setUp(self):
        pygame.init()
        max_level = 1
        start_level = 1
        surface = pygame.surface.Surface
        create_level = lambda *args: None
        create_menu = lambda *args: None

        self.window = pygame.display.set_mode((800, 600))
        self.overworld = Overworld(start_level, max_level, surface, create_level, create_menu)

    def test_setup_icon(self):
        self.overworld.setup_nodes()  # First, set up nodes for the icon to use
        self.overworld.setup_icon()  # Call the method

        icon_pos = self.overworld.icon.sprite.pos
        self.assertEqual(icon_pos, self.overworld.nodes.sprites()[self.overworld.current_level].rect.center)
        # Add more specific tests for the icon setup logic as needed

    # Add additional test cases for other methods in the Overworld class as needed

    def tearDown(self):
        pygame.quit()
