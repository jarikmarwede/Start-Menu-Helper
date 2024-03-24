"""Work with windows shortcuts."""
import pathlib
from typing import Optional

import pythoncom
import win32com.client


def is_shortcut(file: pathlib.WindowsPath) -> bool:
    """Determines whether a file is a windows shortcut."""
    return file.name.endswith(".lnk")


def read_shortcut(link: pathlib.WindowsPath) -> pathlib.WindowsPath:
    """Read the destination of a windows shortcut file."""
    pythoncom.CoInitialize()  # pylint: disable=E1101
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(link))
    return pathlib.WindowsPath(shortcut.Targetpath)


def create_shortcut(
        link_path: pathlib.WindowsPath,
        item_to_link_to: pathlib.WindowsPath,
        arguments: Optional[str] = ""
) -> None:
    """Create a windows shortcut file."""
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(str(link_path))
    shortcut.Targetpath = str(item_to_link_to)
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = str(item_to_link_to.parent)
    shortcut.IconLocation = "icon.png"
    shortcut.save()
