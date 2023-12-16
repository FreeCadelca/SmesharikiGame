import json


def config_parse():
    """
    Read and parse the 'config.json' file.

    :return: Dictionary containing the parsed contents of the 'config.json' file.
    """
    with open('config.json') as cfg:
        return json.loads(cfg.read())


def config_edit(field: list, value):
    """
    Edit the 'config.json' file by updating the specified field with the given value.

    :param field: List containing the fields to be updated in the 'config.json' file.
    :param value: The value to be assigned to the specified field.

    If the length of the field list is 1, the function updates cfg_dict[field[0]] with the given value.
    If the length of the field list is 2, the function updates cfg_dict[field[0]][field[1]] with the given value.

    The updated contents are then written to the 'config.json' file.

    :return: None
    """
    cfg_dict = config_parse()
    if len(field) == 1:
        cfg_dict[field[0]] = value
    elif len(field) == 2:
        cfg_dict[field[0]][field[1]] = value

    with open('config.json', mode="w") as cfg:
        cfg.write(json.dumps(cfg_dict, indent=4))


def replace_config(new_config: dict):
    """
    Replace the contents of the 'config.json' file with the provided new_config.

    :param new_config: A dictionary containing the new configuration to replace the contents of the 'config.json' file.

    The function opens the 'config.json' file in write mode and writes the new_config to the file in JSON format with
    an indentation of 4.

    :return: None
    """

    with open('config.json', mode="w") as cfg:
        cfg.write(json.dumps(new_config, indent=4))
