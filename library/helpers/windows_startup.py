import pathlib

from library import constants
from library.helpers import windows_shortcuts

_startup_path = pathlib.WindowsPath(constants.STARTUP_PATH)
_executable_path = pathlib.WindowsPath(constants.EXECUTABLE_PATH)


def add():
    """Add the program to windows startup."""
    windows_shortcuts.create_shortcut(_startup_path.joinpath("Start Menu Helper.lnk"),
                                      _executable_path)


def remove():
    """Remove the program from windows startup."""
    _startup_path.joinpath("Start Menu Helper.lnk").unlink()


def is_added() -> bool:
    """Return whether program is added to windows startup."""
    for item in _startup_path.iterdir():
        if windows_shortcuts.is_shortcut(item) and windows_shortcuts.read_shortcut(
                item).name == "Start Menu Helper.exe":
            return True
    else:
        return False
