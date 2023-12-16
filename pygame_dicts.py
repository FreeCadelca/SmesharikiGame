import pygame

SCANCODES = {
    4: 'a',
    5: 'b',
    6: 'c',
    7: 'd',
    8: 'e',
    9: 'f',
    10: 'g',
    11: 'h',
    12: 'i',
    13: 'j',
    14: 'k',
    15: 'l',
    16: 'm',
    17: 'n',
    18: 'o',
    19: 'p',
    20: 'q',
    21: 'r',
    22: 's',
    23: 't',
    24: 'u',
    25: 'v',
    26: 'w',
    27: 'x',
    28: 'y',
    29: 'z',
    30: '1',
    31: '2',
    32: '3',
    33: '4',
    34: '5',
    35: '6',
    36: '7',
    37: '8',
    38: '9',
    39: '0',
    44: 'space',
    45: '-',
    46: '=',
    47: '[',
    48: ']',
    49: '\\',
    51: ';',
    52: '\'',
    53: '`',
    54: ',',
    55: '.',
    56: '/',
    79: 'rightarrow',
    80: 'leftarrow',
    81: 'downarrow',
    82: 'uparrow'
}

STR_TO_KEY_SIGN = {
    'K_SPACE': 'space',
    'K_COMMA': ',',
    'K_PERIOD': '.',
    'K_SLASH': '/',
    'K_0': '0',
    'K_1': '1',
    'K_2': '2',
    'K_3': '3',
    'K_4': '4',
    'K_5': '5',
    'K_6': '6',
    'K_7': '7',
    'K_8': '8',
    'K_9': '9',
    'K_SEMICOLON': ';',
    'K_EQUALS': '=',
    'K_LEFTBRACKET': '[',
    'K_BACKSLASH': '\\',
    'K_RIGHTBRACKET': ']',
    'K_BACKQUOTE': '`',
    'K_QUOTE': '\'',
    'K_MINUS': '-',
    'K_a': 'a',
    'K_b': 'b',
    'K_c': 'c',
    'K_d': 'd',
    'K_e': 'e',
    'K_f': 'f',
    'K_g': 'g',
    'K_h': 'h',
    'K_i': 'i',
    'K_j': 'j',
    'K_k': 'k',
    'K_l': 'l',
    'K_m': 'm',
    'K_n': 'n',
    'K_o': 'o',
    'K_p': 'p',
    'K_q': 'q',
    'K_r': 'r',
    'K_s': 's',
    'K_t': 't',
    'K_u': 'u',
    'K_v': 'v',
    'K_w': 'w',
    'K_x': 'x',
    'K_y': 'y',
    'K_z': 'z',
    'K_UP': 'uparrow',
    'K_DOWN': 'downarrow',
    'K_RIGHT': 'rightarrow',
    'K_LEFT': 'leftarrow'
}

KEY_SIGN_TO_STR = {
    'space': 'K_SPACE',
    ',': 'K_COMMA',
    '.': 'K_PERIOD',
    '/': 'K_SLASH',
    '0': 'K_0',
    '1': 'K_1',
    '2': 'K_2',
    '3': 'K_3',
    '4': 'K_4',
    '5': 'K_5',
    '6': 'K_6',
    '7': 'K_7',
    '8': 'K_8',
    '9': 'K_9',
    ';': 'K_SEMICOLON',
    '=': 'K_EQUALS',
    '[': 'K_LEFTBRACKET',
    '\\': 'K_BACKSLASH',
    ']': 'K_RIGHTBRACKET',
    '`': 'K_BACKQUOTE',
    '\'': 'K_QUOTE',
    '-': 'K_MINUS',
    'a': 'K_a',
    'b': 'K_b',
    'c': 'K_c',
    'd': 'K_d',
    'e': 'K_e',
    'f': 'K_f',
    'g': 'K_g',
    'h': 'K_h',
    'i': 'K_i',
    'j': 'K_j',
    'k': 'K_k',
    'l': 'K_l',
    'm': 'K_m',
    'n': 'K_n',
    'o': 'K_o',
    'p': 'K_p',
    'q': 'K_q',
    'r': 'K_r',
    's': 'K_s',
    't': 'K_t',
    'u': 'K_u',
    'v': 'K_v',
    'w': 'K_w',
    'x': 'K_x',
    'y': 'K_y',
    'z': 'K_z',
    'uparrow': 'K_UP',
    'downarrow': 'K_DOWN',
    'rightarrow': 'K_RIGHT',
    'leftarrow': 'K_LEFT'
}

STR_TO_PYGAME_CONSTANT = {
    'K_BACKSPACE': pygame.K_BACKSPACE,
    'K_TAB': pygame.K_TAB,
    'K_CLEAR': pygame.K_CLEAR,
    'K_RETURN': pygame.K_RETURN,
    'K_PAUSE': pygame.K_PAUSE,
    'K_ESCAPE': pygame.K_ESCAPE,
    'K_SPACE': pygame.K_SPACE,
    'K_EXCLAIM': pygame.K_EXCLAIM,
    'K_QUOTEDBL': pygame.K_QUOTEDBL,
    'K_HASH': pygame.K_HASH,
    'K_DOLLAR': pygame.K_DOLLAR,
    'K_AMPERSAND': pygame.K_AMPERSAND,
    'K_QUOTE': pygame.K_QUOTE,
    'K_LEFTPAREN': pygame.K_LEFTPAREN,
    'K_RIGHTPAREN': pygame.K_RIGHTPAREN,
    'K_ASTERISK': pygame.K_ASTERISK,
    'K_PLUS': pygame.K_PLUS,
    'K_COMMA': pygame.K_COMMA,
    'K_MINUS': pygame.K_MINUS,
    'K_PERIOD': pygame.K_PERIOD,
    'K_SLASH': pygame.K_SLASH,
    'K_0': pygame.K_0,
    'K_1': pygame.K_1,
    'K_2': pygame.K_2,
    'K_3': pygame.K_3,
    'K_4': pygame.K_4,
    'K_5': pygame.K_5,
    'K_6': pygame.K_6,
    'K_7': pygame.K_7,
    'K_8': pygame.K_8,
    'K_9': pygame.K_9,
    'K_COLON': pygame.K_COLON,
    'K_SEMICOLON': pygame.K_SEMICOLON,
    'K_LESS': pygame.K_LESS,
    'K_EQUALS': pygame.K_EQUALS,
    'K_GREATER': pygame.K_GREATER,
    'K_QUESTION': pygame.K_QUESTION,
    'K_AT': pygame.K_AT,
    'K_LEFTBRACKET': pygame.K_LEFTBRACKET,
    'K_BACKSLASH': pygame.K_BACKSLASH,
    'K_RIGHTBRACKET': pygame.K_RIGHTBRACKET,
    'K_CARET': pygame.K_CARET,
    'K_UNDERSCORE': pygame.K_UNDERSCORE,
    'K_BACKQUOTE': pygame.K_BACKQUOTE,
    'K_a': pygame.K_a,
    'K_b': pygame.K_b,
    'K_c': pygame.K_c,
    'K_d': pygame.K_d,
    'K_e': pygame.K_e,
    'K_f': pygame.K_f,
    'K_g': pygame.K_g,
    'K_h': pygame.K_h,
    'K_i': pygame.K_i,
    'K_j': pygame.K_j,
    'K_k': pygame.K_k,
    'K_l': pygame.K_l,
    'K_m': pygame.K_m,
    'K_n': pygame.K_n,
    'K_o': pygame.K_o,
    'K_p': pygame.K_p,
    'K_q': pygame.K_q,
    'K_r': pygame.K_r,
    'K_s': pygame.K_s,
    'K_t': pygame.K_t,
    'K_u': pygame.K_u,
    'K_v': pygame.K_v,
    'K_w': pygame.K_w,
    'K_x': pygame.K_x,
    'K_y': pygame.K_y,
    'K_z': pygame.K_z,
    'K_DELETE': pygame.K_DELETE,
    'K_KP0': pygame.K_KP0,
    'K_KP1': pygame.K_KP1,
    'K_KP2': pygame.K_KP2,
    'K_KP3': pygame.K_KP3,
    'K_KP4': pygame.K_KP4,
    'K_KP5': pygame.K_KP5,
    'K_KP6': pygame.K_KP6,
    'K_KP7': pygame.K_KP7,
    'K_KP8': pygame.K_KP8,
    'K_KP9': pygame.K_KP9,
    'K_KP_PERIOD': pygame.K_KP_PERIOD,
    'K_KP_DIVIDE': pygame.K_KP_DIVIDE,
    'K_KP_MULTIPLY': pygame.K_KP_MULTIPLY,
    'K_KP_MINUS': pygame.K_KP_MINUS,
    'K_KP_PLUS': pygame.K_KP_PLUS,
    'K_KP_ENTER': pygame.K_KP_ENTER,
    'K_KP_EQUALS': pygame.K_KP_EQUALS,
    'K_UP': pygame.K_UP,
    'K_DOWN': pygame.K_DOWN,
    'K_RIGHT': pygame.K_RIGHT,
    'K_LEFT': pygame.K_LEFT,
    'K_INSERT': pygame.K_INSERT,
    'K_HOME': pygame.K_HOME,
    'K_END': pygame.K_END,
    'K_PAGEUP': pygame.K_PAGEUP,
    'K_PAGEDOWN': pygame.K_PAGEDOWN,
    'K_F1': pygame.K_F1,
    'K_F2': pygame.K_F2,
    'K_F3': pygame.K_F3,
    'K_F4': pygame.K_F4,
    'K_F5': pygame.K_F5,
    'K_F6': pygame.K_F6,
    'K_F7': pygame.K_F7,
    'K_F8': pygame.K_F8,
    'K_F9': pygame.K_F9,
    'K_F10': pygame.K_F10,
    'K_F11': pygame.K_F11,
    'K_F12': pygame.K_F12,
    'K_F13': pygame.K_F13,
    'K_F14': pygame.K_F14,
    'K_F15': pygame.K_F15,
    'K_NUMLOCK': pygame.K_NUMLOCK,
    'K_CAPSLOCK': pygame.K_CAPSLOCK,
    'K_SCROLLOCK': pygame.K_SCROLLOCK,
    'K_RSHIFT': pygame.K_RSHIFT,
    'K_LSHIFT': pygame.K_LSHIFT,
    'K_RCTRL': pygame.K_RCTRL,
    'K_LCTRL': pygame.K_LCTRL,
    'K_RALT': pygame.K_RALT,
    'K_LALT': pygame.K_LALT,
    'K_RMETA': pygame.K_RMETA,
    'K_LMETA': pygame.K_LMETA,
    'K_LSUPER': pygame.K_LSUPER,
    'K_RSUPER': pygame.K_RSUPER,
    'K_MODE': pygame.K_MODE,
    'K_HELP': pygame.K_HELP,
    'K_PRINT': pygame.K_PRINT
}

PYGAME_CONSTANT_TO_STR = {
    pygame.K_BACKSPACE: 'K_BACKSPACE',
    pygame.K_TAB: 'K_TAB',
    pygame.K_CLEAR: 'K_CLEAR',
    pygame.K_RETURN: 'K_RETURN',
    pygame.K_PAUSE: 'K_PAUSE',
    pygame.K_ESCAPE: 'K_ESCAPE',
    pygame.K_SPACE: 'K_SPACE',
    pygame.K_EXCLAIM: 'K_EXCLAIM',
    pygame.K_QUOTEDBL: 'K_QUOTEDBL',
    pygame.K_HASH: 'K_HASH',
    pygame.K_DOLLAR: 'K_DOLLAR',
    pygame.K_AMPERSAND: 'K_AMPERSAND',
    pygame.K_QUOTE: 'K_QUOTE',
    pygame.K_LEFTPAREN: 'K_LEFTPAREN',
    pygame.K_RIGHTPAREN: 'K_RIGHTPAREN',
    pygame.K_ASTERISK: 'K_ASTERISK',
    pygame.K_PLUS: 'K_PLUS',
    pygame.K_COMMA: 'K_COMMA',
    pygame.K_MINUS: 'K_MINUS',
    pygame.K_PERIOD: 'K_PERIOD',
    pygame.K_SLASH: 'K_SLASH',
    pygame.K_0: 'K_0',
    pygame.K_1: 'K_1',
    pygame.K_2: 'K_2',
    pygame.K_3: 'K_3',
    pygame.K_4: 'K_4',
    pygame.K_5: 'K_5',
    pygame.K_6: 'K_6',
    pygame.K_7: 'K_7',
    pygame.K_8: 'K_8',
    pygame.K_9: 'K_9',
    pygame.K_COLON: 'K_COLON',
    pygame.K_SEMICOLON: 'K_SEMICOLON',
    pygame.K_LESS: 'K_LESS',
    pygame.K_EQUALS: 'K_EQUALS',
    pygame.K_GREATER: 'K_GREATER',
    pygame.K_QUESTION: 'K_QUESTION',
    pygame.K_AT: 'K_AT',
    pygame.K_LEFTBRACKET: 'K_LEFTBRACKET',
    pygame.K_BACKSLASH: 'K_BACKSLASH',
    pygame.K_RIGHTBRACKET: 'K_RIGHTBRACKET',
    pygame.K_CARET: 'K_CARET',
    pygame.K_UNDERSCORE: 'K_UNDERSCORE',
    pygame.K_BACKQUOTE: 'K_BACKQUOTE',
    pygame.K_a: 'K_a',
    pygame.K_b: 'K_b',
    pygame.K_c: 'K_c',
    pygame.K_d: 'K_d',
    pygame.K_e: 'K_e',
    pygame.K_f: 'K_f',
    pygame.K_g: 'K_g',
    pygame.K_h: 'K_h',
    pygame.K_i: 'K_i',
    pygame.K_j: 'K_j',
    pygame.K_k: 'K_k',
    pygame.K_l: 'K_l',
    pygame.K_m: 'K_m',
    pygame.K_n: 'K_n',
    pygame.K_o: 'K_o',
    pygame.K_p: 'K_p',
    pygame.K_q: 'K_q',
    pygame.K_r: 'K_r',
    pygame.K_s: 'K_s',
    pygame.K_t: 'K_t',
    pygame.K_u: 'K_u',
    pygame.K_v: 'K_v',
    pygame.K_w: 'K_w',
    pygame.K_x: 'K_x',
    pygame.K_y: 'K_y',
    pygame.K_z: 'K_z',
    pygame.K_DELETE: 'K_DELETE',
    pygame.K_KP0: 'K_KP0',
    pygame.K_KP1: 'K_KP1',
    pygame.K_KP2: 'K_KP2',
    pygame.K_KP3: 'K_KP3',
    pygame.K_KP4: 'K_KP4',
    pygame.K_KP5: 'K_KP5',
    pygame.K_KP6: 'K_KP6',
    pygame.K_KP7: 'K_KP7',
    pygame.K_KP8: 'K_KP8',
    pygame.K_KP9: 'K_KP9',
    pygame.K_KP_PERIOD: 'K_KP_PERIOD',
    pygame.K_KP_DIVIDE: 'K_KP_DIVIDE',
    pygame.K_KP_MULTIPLY: 'K_KP_MULTIPLY',
    pygame.K_KP_MINUS: 'K_KP_MINUS',
    pygame.K_KP_PLUS: 'K_KP_PLUS',
    pygame.K_KP_ENTER: 'K_KP_ENTER',
    pygame.K_KP_EQUALS: 'K_KP_EQUALS',
    pygame.K_UP: 'K_UP',
    pygame.K_DOWN: 'K_DOWN',
    pygame.K_RIGHT: 'K_RIGHT',
    pygame.K_LEFT: 'K_LEFT',
    pygame.K_INSERT: 'K_INSERT',
    pygame.K_HOME: 'K_HOME',
    pygame.K_END: 'K_END',
    pygame.K_PAGEUP: 'K_PAGEUP',
    pygame.K_PAGEDOWN: 'K_PAGEDOWN',
    pygame.K_F1: 'K_F1',
    pygame.K_F2: 'K_F2',
    pygame.K_F3: 'K_F3',
    pygame.K_F4: 'K_F4',
    pygame.K_F5: 'K_F5',
    pygame.K_F6: 'K_F6',
    pygame.K_F7: 'K_F7',
    pygame.K_F8: 'K_F8',
    pygame.K_F9: 'K_F9',
    pygame.K_F10: 'K_F10',
    pygame.K_F11: 'K_F11',
    pygame.K_F12: 'K_F12',
    pygame.K_F13: 'K_F13',
    pygame.K_F14: 'K_F14',
    pygame.K_F15: 'K_F15',
    pygame.K_NUMLOCK: 'K_NUMLOCK',
    pygame.K_CAPSLOCK: 'K_CAPSLOCK',
    pygame.K_SCROLLOCK: 'K_SCROLLOCK',
    pygame.K_RSHIFT: 'K_RSHIFT',
    pygame.K_LSHIFT: 'K_LSHIFT',
    pygame.K_RCTRL: 'K_RCTRL',
    pygame.K_LCTRL: 'K_LCTRL',
    pygame.K_RALT: 'K_RALT',
    pygame.K_LALT: 'K_LALT',
    pygame.K_RMETA: 'K_RMETA',
    pygame.K_LMETA: 'K_LMETA',
    pygame.K_LSUPER: 'K_LSUPER',
    pygame.K_RSUPER: 'K_RSUPER',
    pygame.K_MODE: 'K_MODE',
    pygame.K_HELP: 'K_HELP',
    pygame.K_PRINT: 'K_PRINT',
}

"""
There are 5 dictionaries here, which are used for various conversions related to keys and pygame. 
The conversion methods are shown below

                       scancode -----→ to determine the click
                         |
               SCANCODES |
                         ↓
                       key sign -----→ for rendering to the user
                         | ↑
         KEY_SIGN_TO_STR | | STR_TO_KEY_SIGN
                         ↓ |
                         str --------→ in this form, it is read from the config.cfg file
                         | ↑
  STR_TO_PYGAME_CONSTANT | | PYGAME_CONSTANT_TO_STR
                         ↓ |
                    pygame constant -→ to define a key in the code
"""
