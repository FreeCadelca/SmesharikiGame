import json


def config_parse():
    # returns dict of parsed config
    with open('config.json') as cfg:
        return json.loads(cfg.read())


def config_edit(field: list, value):
    # edits value in field in config.json
    # ex: config_edit(["controls", "Left"], "K_LEFT") -> writes "K_LEFT" into field cfg["controls"]["Left"]
    cfg_dict = config_parse()
    if len(field) == 1:
        cfg_dict[field[0]] = value
    elif len(field) == 2:
        cfg_dict[field[0]][field[1]] = value

    with open('config.json', mode="w") as cfg:
        cfg.write(json.dumps(cfg_dict, indent=4))


def replace_config(new_config: dict):
    #  replaces config at new
    with open('config.json', mode="w") as cfg:
        cfg.write(json.dumps(new_config, indent=4))
