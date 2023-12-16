import unittest
import pygame
# from main import Game
from code_with_decoration.player import Player

global health


def change_health(value):
    global health
    health += value


class TestYourCharacterClass(unittest.TestCase):
    def setUp(self):
        # Initialize the character for testing
        pygame.init()
        surface = pygame.display.set_mode((100, 100))
        clock = pygame.time.Clock()
        self.character = Player((50, 50), surface, change_health)

    def test_apply_gravity(self):
        initial_y_position = self.character.rect.y
        self.character.apply_gravity()
        self.assertNotEqual(initial_y_position, self.character.rect.y)

    def test_jump(self):
        initial_y_direction = self.character.direction.y
        self.character.jump()
        self.assertEqual(self.character.direction.y, initial_y_direction + self.character.jump_speed)

    def test_get_damage(self):
        global health
        health = 80
        initial_health = health
        self.character.get_damage()
        self.assertEqual(health, initial_health - 10)
        self.assertTrue(self.character.invincible)
        self.assertIsNotNone(self.character.hurt_time)  # Ensure hurt_time is set

    def test_invincibility_timer(self):
        self.character.invincible = True
        self.character.hurt_time = 0  # Force invincibility
        self.character.invincibility_timer()
        self.assertTrue(self.character.invincible)  # Invincibility should still be active

    def test_wave_value(self):
        value = self.character.wave_value()
        self.assertIn(value, [0, 255])


if __name__ == '__main__':
    unittest.main()
