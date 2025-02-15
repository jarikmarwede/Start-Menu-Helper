"""Helper functions for file system operations."""
import ctypes
import pathlib
from typing import List

from library.helpers import windows_shortcuts


def get_nested_directories(directory: pathlib.WindowsPath) -> List[pathlib.WindowsPath]:
    """Return all directories inside directory recursively."""
    nested_directories: List[pathlib.WindowsPath] = []
    for item in directory.iterdir():
        if item.is_dir():
            nested_directories.append(item)
            nested_directories.extend(get_nested_directories(item))
    return nested_directories


def get_nested_files(directory: pathlib.WindowsPath) -> List[pathlib.WindowsPath]:
    """Return all files inside directory and its child directories."""
    files = [item for item in directory.iterdir() if item.is_file()]

    for current_directory in get_nested_directories(directory):
        for item in current_directory.iterdir():
            if item.is_file():
                files.append(item)
    return files


def get_nested_links(directory: pathlib.WindowsPath) -> List[pathlib.WindowsPath]:
    """Return all links inside directory and its child directories."""
    links = [item for item in directory.iterdir() if
             item.is_symlink() or windows_shortcuts.is_shortcut(item)]

    for current_directory in get_nested_directories(directory):
        for item in current_directory.iterdir():
            if item.is_symlink() or windows_shortcuts.is_shortcut(item):
                links.append(item)
    return links


def resolve_files(files: List[pathlib.WindowsPath]) -> List[pathlib.WindowsPath]:
    """Resolve multiple files."""
    resolved_files = []
    for file in files:
        if windows_shortcuts.is_shortcut(file):
            resolved_files.append(windows_shortcuts.read_shortcut(file))
        else:
            resolved_files.append(file.resolve())
    return resolved_files

def file_is_writable(file: pathlib.WindowsPath) -> bool:
    """Return whether the file is writable."""
    file_attributes = ctypes.windll.kernel32.GetFileAttributesW(str(file))
    return not file_attributes & 0x01
