import json


def config_parse():
    """
    Parses the config file and returns it as a dictionary.

    Returns:
        dict: The parsed content of the config file.
    """
    with open('config.json') as cfg:
        return json.loads(cfg.read())


def config_edit(field: list, value):
    """
    Edits the value in the specified field in the config file.

    Args:
        field (list): The list representing the field hierarchy in the config file.
        value: The new value to be written into the specified field.

    Example:
        >>> config_edit(["controls", "Left"], "K_LEFT")
        # Writes "K_LEFT" into field cfg["controls"]["Left"]
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
    Replaces the entire content of the config file with the new configuration.

    Args:
        new_config (dict): The new configuration to replace the existing content of the config file.
    """
    with open('config.json', mode="w") as cfg:
        cfg.write(json.dumps(new_config, indent=4))
