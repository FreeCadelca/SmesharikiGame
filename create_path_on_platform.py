import platform


def create_path_on_platform(path: str):
    """
    Create a platform-specific path by replacing the forward slashes with backslashes for Windows.

    :param path: The input path string.

    If the current platform is not Windows or if the input path already contains backslashes,
    the original path is returned. Otherwise, the function replaces the forward slashes with backslashes in the path
    and returns the modified path.

    :return: The platform-specific path string.
    """
    if platform.system() != 'Windows' or '\\' in path:
        return path
    else:
        return path.replace('/', '\\')
