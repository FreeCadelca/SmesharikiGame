import pprint

from pygame_dicts import *


def config_parse():
    parsed_dict = {}
    with open('config.cfg') as cfg:
        lines = [i.rstrip() for i in cfg.readlines()]
    current_line = 0
    while current_line < len(lines):
        line = [i.strip() for i in lines[current_line].split(':') if len(i)]
        if len(line) == 1:
            if line[0] == 'controls':
                sub_dict_of_params = {}
                current_line += 1
                while lines[current_line] and current_line < len(lines):
                    sub_param = lines[current_line].split(' > ')
                    sub_dict_of_params[sub_param[0]] = STR_TO_PYGAME_CONSTANT[sub_param[1]]
                    current_line += 1
                parsed_dict[line[0]] = sub_dict_of_params
        else:
            parsed_dict[line[0]] = int(line[1]) if line[1].isdigit() else line[1]
        current_line += 1
    return parsed_dict


def config_edit(field: list, value):
    cfg_dict = config_parse()
    if len(field) == 1:
        cfg_dict[field[0]] = value
    elif len(field) == 2:
        cfg_dict[field[0]][field[1]] = value

    new_cfg = ''
    for i in cfg_dict:
        if type(cfg_dict[i]) == str or type(cfg_dict[i]) == int:
            new_cfg += i + ': ' + str(cfg_dict[i]) + '\n'
        else:
            new_cfg += i + ':\n'
            for j in cfg_dict[i]:
                new_cfg += j + ' > ' + PYGAME_CONSTANT_TO_STR[cfg_dict[i][j]] + '\n'
            new_cfg += '\n'
    with open('config.cfg', mode='w') as cfg:
        cfg.write(new_cfg)
