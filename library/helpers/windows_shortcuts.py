"""Work with windows shortcuts."""
import pathlib
from typing import Optional

import pythoncom
import win32com.client


def is_shortcut(file: pathlib.Path) -> bool:
    """Determines whether a file is a windows shortcut."""
    return file.name.endswith(".lnk")


def read_shortcut(link: pathlib.Path) -> pathlib.Path:
    """Read the destination of a windows shortcut file."""
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(link))
    return pathlib.Path(shortcut.Targetpath)


def create_shortcut(link_path: pathlib.Path, item_to_link_to: pathlib.Path,
                    arguments: Optional[str] = ""):
    """Create a windows shortcut file."""
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(str(link_path))
    shortcut.Targetpath = str(item_to_link_to)
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = str(item_to_link_to.parent)
    shortcut.IconLocation = "icon.png"
    shortcut.save()
