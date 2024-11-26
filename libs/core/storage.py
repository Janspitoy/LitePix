
import os
from kivy import platform


def get_base_directory():
    """Return the base directory based on platform."""
    if platform == "android":
        from main import get_android_base_directory
        return get_android_base_directory()
    else:
        return os.path.expanduser('~')  # Default home directory for non-Android platforms
