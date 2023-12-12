import platform


def create_path_on_platform(path: str):
    if platform.system() != 'Windows' or '\\' in path:
        return path
    else:
        if len(path) and path[0] == '.':
            path = path.replace('.', '..', 1)
        return path.replace('/', '\\')
