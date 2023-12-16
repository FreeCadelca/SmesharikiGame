import platform


def create_path_on_platform(path: str):
    """
    Creates a modified path based on the platform's system.

    Args:
        path (str): A string representing the original path.

    Returns:
        str: The modified path (replacing '/' with '\\' on Windows).

    Raises:
        None.
    """
    if platform.system() != 'Windows' or '\\' in path:
        return path
    else:
        return path.replace('/', '\\')
