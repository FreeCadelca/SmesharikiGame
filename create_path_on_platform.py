import platform


def create_path_on_platform(path: str):
    if platform.system() != 'Windows' or '\\' in path:
        return path
    else:
        return path.replace('/', '\\')
