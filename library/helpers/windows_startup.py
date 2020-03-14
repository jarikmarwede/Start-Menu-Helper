"""Configure behaviour of program on system start."""
import pathlib

from library import constants
from library.helpers import windows_shortcuts

_STARTUP_PATH = pathlib.WindowsPath(constants.STARTUP_PATH)
_EXECUTABLE_PATH = pathlib.WindowsPath(constants.EXECUTABLE_PATH)


def add():
    """Add the program to windows startup."""
    windows_shortcuts.create_shortcut(_STARTUP_PATH.joinpath(constants.PROGRAM_NAME + ".lnk"),
                                      _EXECUTABLE_PATH,
                                      arguments="-b")


def remove():
    """Remove the program from windows startup."""
    _STARTUP_PATH.joinpath(constants.PROGRAM_NAME + ".lnk").unlink()


def is_added() -> bool:
    """Return whether program is added to windows startup."""
    for item in _STARTUP_PATH.iterdir():
        if windows_shortcuts.is_shortcut(item) and windows_shortcuts.read_shortcut(
                item).name == constants.PROGRAM_NAME + ".exe":
            return True
    return False
