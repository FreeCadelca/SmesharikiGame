import pygame

from create_path_on_platform import *
from ..Bars.DefaultBar import DefaultBar
from .AbstractSection import AbstractSection
from ..Bars.LabelBar import LabelBar

from code_with_decoration.screen_settings import *
from config import *
from hash import *


class SignInSection(AbstractSection):
    BARS_SIGNIN = ['Enter login...', 'Enter password...', 'Repeat password...', 'Confirm', 'Back']

    def __init__(self):
        super().__init__()
        cfg = config_parse()
        self.max_bars = len(SignInSection.BARS_SIGNIN)
        self.single_space = cfg['spacing']
        self.typing_text = ['', '', '']  # text under stars in fields login, password
        self.state_of_entering_text = 0
        self.debug_line = ''
        # the state when the text is entered in the field.
        # 0 - nothing is being entered, 1 - login, 2 - 1st pass, 2 - 2nd pass

        for i in range(3):
            offset = (i - len(SignInSection.BARS_SIGNIN) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(SignInSection.BARS_SIGNIN) // 2)
            # spacing between bars
            new_bar = LabelBar(
                SignInSection.BARS_SIGNIN[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                SignInSection.BARS_SIGNIN[i],
                text_color=(0, 153, 171),
                font_size=20
            )
            self.bars.append(new_bar)
        for i in range(3, len(SignInSection.BARS_SIGNIN)):
            offset = (i - len(SignInSection.BARS_SIGNIN) // 2) * DefaultBar.BAR_HEIGHT
            # offset relative other bars
            spacing = self.single_space * (i - len(SignInSection.BARS_SIGNIN) // 2)
            # spacing between bars
            new_bar = LabelBar(
                SignInSection.BARS_SIGNIN[i],
                (screen_width // 2, screen_height // 2 + (offset + spacing)),
                SignInSection.BARS_SIGNIN[i])
            self.bars.append(new_bar)

    def input(self, keys, last_pressed_keys, id_current_section, events, client):
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
            self.bars[id_field].text = (
                self.typing_text[id_field] if id_field == 0 else '*' * len(self.typing_text[id_field])
            )
        else:
            if keys[pygame.K_RETURN] and not last_pressed_keys[pygame.K_RETURN]:
                if 0 <= self.current_bar < 3:
                    if self.bars[self.current_bar].text == SignInSection.BARS_SIGNIN[self.current_bar]:
                        self.bars[self.current_bar].text = ''
                        self.bars[self.current_bar].text_color = (0, 255, 100)
                        self.bars[self.current_bar].font_size = 28
                    self.state_of_entering_text = self.current_bar + 1
                    last_pressed_keys[pygame.K_RETURN] = True
                elif self.current_bar == 3:  # trying sign in
                    if self.typing_text[0] and self.typing_text[1] and self.typing_text[2]:
                        if self.typing_text[1] != self.typing_text[2]:
                            self.debug_line = 'Passwords are not the same'
                        else:
                            response = client.request_to_server(
                                json.dumps(
                                    {
                                        'msg': f'SignIn {self.typing_text[0]} {my_hash(self.typing_text[1])}',
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
                elif self.current_bar == 4:
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

    def setup_bars(self, bars_sprites, cfg):
        super().setup_bars(bars_sprites, cfg)
        for i in self.bars:
            bars_sprites.add(i)
        offset_of_current_bar = ((self.current_bar - len(SignInSection.BARS_SIGNIN) // 2) * DefaultBar.BAR_HEIGHT +
                                 self.single_space * (self.current_bar - len(SignInSection.BARS_SIGNIN) // 2))
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
