import pygame
from code_with_decoration.support import import_folder
from math import sin
from create_path_on_platform import *
from config import *
from pygame_dicts import *


class Player(pygame.sprite.Sprite):
    """
    The Player class represents the main character in the game.

    Attributes:
    - pos (tuple): The initial position of the player on the screen.
    - surface (pygame.Surface): The display surface where the player is rendered.
    - change_health (function): A function to change the player's health.

    Methods:
    - __init__(self, pos, surface, change_health): Initializes the player with the given position, surface, and health-changing function.
    - import_character_assets(self): Imports character animations from the specified folder.
    - animate(self): Animates the player based on the current status (idle, run, jump, fall).
    - get_input(self): Handles user input for movement and jumping.
    - get_status(self): Determines the current status of the player (idle, run, jump, fall).
    - apply_gravity(self): Applies gravity to the player's vertical movement.
    - jump(self): Initiates a jump, plays jump sound, and adjusts vertical speed.
    - get_damage(self): Inflicts damage on the player and triggers invincibility if not already invincible.
    - invincibility_timer(self): Manages the duration of invincibility after taking damage.
    - wave_value(self): Generates a sine wave value for controlling image alpha during invincibility.
    - update(self): Updates the player's state based on input, status, and animations.
    """

    def __init__(self, pos, surface, change_health):
        """
        Initializes a new Player object.

        Args:
        - pos (tuple): The initial position (x, y) of the player on the screen.
        - surface (pygame.Surface): The display surface where the player is rendered.
        - change_health (function): A function to change the player's health.
        """
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.display_surface = surface

        # движение игрока
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # health management
        self.change_health = change_health
        self.invincible = False
        self.invincibility_duration = 700
        self.hurt_time = 0

        # audio
        self.jump_sound = pygame.mixer.Sound(create_path_on_platform('./audio/effects/jump.wav'))
        self.jump_sound.set_volume(config_parse()["VFX volume"] / 100)
        self.hit_sound = pygame.mixer.Sound(create_path_on_platform('./audio/effects/hit.wav'))
        self.hit_sound.set_volume(config_parse()["VFX volume"] / 100)

    def import_character_assets(self):
        """
        Imports character animations from the specified folder and stores them in a dictionary.
        """
        character_path = create_path_on_platform('./graphics/character/')
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        """
        Animates the player based on the current status, updating the frame index and image accordingly.
        """
        animation = self.animations[self.status]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        # nn (т к не особо вижу разницы)- set the rect - фикчим баги, когда из-за разности между размерами изображений при анимации создаются разные по величине прямоуг-ки и персонаж ведет себя неестетсвенно
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def get_input(self):
        """
        Handles user input for movement and jumping, updating the player's direction and facing direction.
        """
        keys = pygame.key.get_pressed()
        cfg = config_parse()
        if keys[STR_TO_PYGAME_CONSTANT[cfg['controls']['Right']]]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[STR_TO_PYGAME_CONSTANT[cfg['controls']['Left']]]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if keys[STR_TO_PYGAME_CONSTANT[cfg['controls']['Jump']]] and self.on_ground:
            self.jump()

    def get_status(self):
        """
        Determines the current status of the player (idle, run, jump, fall) based on the player's movement.
        """
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    # применение силы тяжести
    def apply_gravity(self):
        """
        Applies gravity to the player's vertical movement.
        """
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        """
        Initiates a jump, plays the jump sound, and adjusts the player's vertical speed.
        """
        self.jump_sound.play()
        self.direction.y = self.jump_speed

    def get_damage(self):
        """
        Inflicts damage on the player, triggers invincibility, and plays the hit sound if the player is not already invincible.
        """
        if not self.invincible:
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            self.hit_sound.play()

    def invincibility_timer(self):
        """
        Manages the duration of invincibility after taking damage.
        """
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        """
        Generates a sine wave value for controlling image alpha during invincibility.
        """
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        """
        Updates the player's state based on input, status, animations, invincibility, and wave value.
        """
        self.get_input()
        self.get_status()
        self.animate()
        self.invincibility_timer()
        self.wave_value()
