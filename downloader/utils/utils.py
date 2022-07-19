import os


def get_resource_path(resource: str):
    dir_name = os.getcwd()
    file_path = os.path.normpath(os.path.join(dir_name, resource))

    return file_path
