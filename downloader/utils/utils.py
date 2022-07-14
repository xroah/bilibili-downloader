import __main__
import inspect
import os


def get_resource_path(resource: str):
    file = inspect.getfile(__main__)
    dir_name = os.path.dirname(file)
    file_path = os.path.normpath(os.path.join(dir_name, "resources", resource))

    return file_path
