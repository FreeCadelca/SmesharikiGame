from convertStrToPygameConstant import *


def config_parse():
    parsed_dict = {}
    with open('config.cfg') as cfg:
        lines = [i.rstrip() for i in cfg.readlines()]
    current_line = 0
    print(lines)
    while current_line < len(lines):
        line = [i.strip() for i in lines[current_line].split(':') if len(i)]
        if len(line) == 1:
            if line[0] == 'controls':
                sub_dict_of_params = {}
                current_line += 1
                while lines[current_line] and current_line < len(lines):
                    subParam = lines[current_line].split(' > ')
                    sub_dict_of_params[subParam[0]] = \
                        [STR_TO_PYGAME_DICT[subParam[1]], STR_TO_PYGAME_DICT[subParam[2]]]
                    current_line += 1
                parsed_dict[line[0]] = sub_dict_of_params
        else:
            parsed_dict[line[0]] = line[1]
        current_line += 1
    return parsed_dict