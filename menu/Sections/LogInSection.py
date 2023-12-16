import pygame

from create_path_on_platform import *
from ..Bars.DefaultBar import DefaultBar
from .AbstractSection import AbstractSection
from ..Bars.LabelBar import LabelBar

from code_with_decoration.screen_settings import *
from config import *
from hash import *


"""
This class processes the "Log in" section for the application and processes log in request, sending to the server

Attributes:
    BARS_LOGIN (list): list containing names of bars in "Log in" section.
    max_bars (int): maximum number of bars for the account section.
    single_space (int): spacing for the bars.
    typing_text(list): typing text in fields login and password (behind stars)
    state_of_entering_text (int): id of the field in which the user writes
    debug_line (str): error text displayed to the user in the lower left corner
    
Methods:
    input: method to handle user input
    setup_bars: method for drawing sprites
"""


class LogInSection(AbstractSection):
    BARS_LOGIN = ['Enter login...', 'Enter password...', 'Confirm', 'Back']

    def __init__(self):
        """
        The constructor for LogInSection class.
        """
        super().__init__()
        cfg = config_parse()
        self.max_bars = len(LogInSection.BARS_LOGIN)
        self.single_space = cfg['spacing']
        self.typing_text = ['', '']  # text in fields login, password (behind stars)
        self.state_of_entering_text = 0
        self.debug_line = ''
        # the state when the text is entered in the field.
        # 0 - nothing is being entered, 1 - login, 2 - pass

        for i in range(2):
            offset = (i - len(LogInSection.BARS_LOGIN) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(LogInSection.BARS_LOGIN) // 2)
            # spacing between bars
            new_bar = LabelBar(
                LogInSection.BARS_LOGIN[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                LogInSection.BARS_LOGIN[i],
                text_color=(0, 153, 171),
                font_size=20
            )
            self.bars.append(new_bar)
        for i in range(2, len(LogInSection.BARS_LOGIN)):
            offset = (i - len(LogInSection.BARS_LOGIN) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(LogInSection.BARS_LOGIN) // 2)
            # spacing between bars
            new_bar = LabelBar(
                LogInSection.BARS_LOGIN[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                LogInSection.BARS_LOGIN[i])
            self.bars.append(new_bar)

    def input(self, keys, last_pressed_keys, id_current_section, events, client):
        """
        Method to handle user input.
        In case of an authorization attempt, the method sends a "LogIn <Login> <hashed_password>" request
        to the server and changes the game config file depending on the server response.
        Displays errors on the screen in the corner, if any

        Args:
            keys: dictionary representing the pressed keys
            last_pressed_keys: dictionary representing the last pressed keys
            id_current_section (int): the current section id
            events: list of events in Pygame
            client (Client): the client object

        Returns:
            id_current_section (int): the updated current section id
        """
        super().input(keys, last_pressed_keys, id_current_section, events, client)
        if self.state_of_entering_text:  # if we are typing text
            id_field = self.state_of_entering_text - 1
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_UP, pygame.K_DOWN]:
                        self.state_of_entering_text = 0
                    elif event.key == pygame.K_BACKSPACE:
                        self.typing_text[id_field] = self.typing_text[id_field][:-1]
                    else:
                        self.typing_text[id_field] += event.unicode
            self.bars[id_field].text = '*' * len(self.typing_text[id_field]) if id_field else self.typing_text[id_field]
        else:
            if keys[pygame.K_RETURN] and not last_pressed_keys[pygame.K_RETURN]:
                if 0 <= self.current_bar < 2:
                    if self.bars[self.current_bar].text == LogInSection.BARS_LOGIN[self.current_bar]:
                        self.bars[self.current_bar].text = ''
                        self.bars[self.current_bar].text_color = (0, 255, 100)
                        self.bars[self.current_bar].font_size = 28
                    self.state_of_entering_text = self.current_bar + 1
                    last_pressed_keys[pygame.K_RETURN] = True
                elif self.current_bar == 2:  # trying log in
                    if self.typing_text[0] and self.typing_text[1]:
                        response = client.request_to_server(
                            json.dumps(
                                {
                                    'msg': f'LogIn {self.typing_text[0]} {my_hash(self.typing_text[1])}',
                                    'cfg': json.dumps(config_parse())
                                }
                            )
                        )
                        if 'successfully' in response['answer']:
                            replace_config(response['cfg'])
                            id_current_section = 1
                        else:
                            if response['answer']:
                                self.debug_line = response['answer']
                            if response['error']:
                                print(response['error'])
                elif self.current_bar == 3:
                    id_current_section = 1
                    last_pressed_keys[pygame.K_UP] = True
                last_pressed_keys[pygame.K_RETURN] = True
            elif keys[pygame.K_ESCAPE] and not last_pressed_keys[pygame.K_ESCAPE]:
                id_current_section = 0
                last_pressed_keys[pygame.K_ESCAPE] = True
            for i in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RETURN, pygame.K_ESCAPE):
                # refreshing dict of last pressed keys
                if not keys[i]:
                    last_pressed_keys[i] = False
        return id_current_section

    def setup_bars(self, bars_sprites, cfg: dict):
        """
        Method to set up all bars in the 'Log in' section and append these sprites to bars_sprites,
        transmitted from Menu.

        Args:
            bars_sprites: the sprite group for bars from menu
            cfg (dict): dictionary of game configuration for the bars
        """
        super().setup_bars(bars_sprites, cfg)
        for i in self.bars:
            bars_sprites.add(i)
        offset_of_current_bar = ((self.current_bar - len(LogInSection.BARS_LOGIN) // 2) * DefaultBar.BAR_HEIGHT +
                                 self.single_space * (self.current_bar - len(LogInSection.BARS_LOGIN) // 2))
        current_bar_sprite = DefaultBar(
            'selected',
            (screen_width // 2, screen_height // 2 + offset_of_current_bar),
            'Stroke_700px.png'
        )
        bars_sprites.add(current_bar_sprite)

        new_bar = DefaultBar(
            'debug_text',
            (10 + DefaultBar.BAR_WIDTH // 2, 10 + DefaultBar.BAR_HEIGHT),
            'Empty_700px.png'
        )
        pygame.font.init()
        my_font = pygame.font.Font(create_path_on_platform('fonts/' + config_parse()["font"]), 16)
        text_surface = my_font.render(
            self.debug_line,
            False,
            (255, 0, 0))
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        new_bar.image.blit(
            text_surface,
            (0, 0)
        )
        bars_sprites.add(new_bar)