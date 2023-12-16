import unittest
import pygame
from menu.menu import Menu


def create_overworld(level, max_level):
    pass


def config_parse():
    pass


class TestMenu(unittest.TestCase):
    def setUp(self):
        pygame.init()


        menu = Menu(pygame.display.get_surface(), create_overworld)
        events = pygame.event.get()
        client = None
        menu.input(events, client)

        self.assertIsNotNone(menu.section)
        self.assertIsNotNone(menu.id_current_section)

    def test_setup_bars(self):
        def create_overworld(level, max_level):
            pass

        def config_parse():
            return {}

        menu = Menu(pygame.display.get_surface(), create_overworld)

        with self.assertRaises(AttributeError):
            menu.setup_bars()

        cfg = menu.section.setup_bars()
        self.assertIsNotNone(cfg)
        self.assertGreater(len(cfg), 0)


if __name__ == '__main__':
    unittest.main()
