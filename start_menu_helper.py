import getpass
import pathlib
import threading
import time
from typing import List

import configuration
import windows_shortcuts


class StartMenuHelper:

    def __init__(self):
        self.start_menu_paths = [
            pathlib.WindowsPath(
                pathlib.Path.home().drive + "/ProgramData/Microsoft/Windows/Start Menu"),
            pathlib.WindowsPath(
                pathlib.Path.home().drive + "/Users/" + getpass.getuser() + "/AppData/Roaming/Microsoft/Windows/Start Menu")
        ]
        self.start_menu_programs_path = [
            pathlib.WindowsPath(
                pathlib.Path.home().drive + "/ProgramData/Microsoft/Windows/Start Menu/Programs"),
            pathlib.WindowsPath(
                pathlib.Path.home().drive + "/Users/" + getpass.getuser() + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs")
        ]

        self.protected_folders = [
            "Startup",
            "Administrative Tools"
        ]

        self._config = configuration.Configuration()
        self._cleaner_thread = StoppableThread()

    def start_cleaning(self):
        """Starts the cleaning based on the configuration."""
        self._cleaner_thread = StoppableThread(target=self._clean, daemon=True)
        self._cleaner_thread.start()

    def stop_cleaning(self):
        """Stops the cleaning."""
        self._cleaner_thread.stop()
        self._cleaner_thread.join()

    def _clean(self):
        """Cleans based on configuration.

        This method is supposed to be run by the _cleaner_thread.
        """
        self._config.reload()
        while not self._cleaner_thread.stopped():
            self.move_files_to_programs_directory()

            self.delete_files_with_names_containing()
            if self._config.get("delete_files_based_on_file_type_str") == "in the list":
                self.delete_files_matching_file_types()
            else:
                self.delete_files_not_matching_file_types()
            if self._config.get("delete_broken_links_bool"):
                self.delete_broken_links()
            if self._config.get("delete_duplicates_bool"):
                self.delete_duplicates()
            if self._config.get("flatten_folders_str") == "All":
                self.flatten_all_folders()
            elif self._config.get("flatten_folders_str") == "Only ones with one item in them":
                self.flatten_folders_containing_one_file()
            if self._config.get("delete_empty_folders_bool"):
                self.delete_empty_folders()
            time.sleep(5)

    def move_files_to_programs_directory(self):
        """Move all files to the programs directory."""
        for path in self.start_menu_paths:
            for item in path.iterdir():
                if item.name != "Programs":
                    item.replace(path.joinpath("Programs").joinpath(item.name))

    def delete_duplicates(self):
        """Delete duplicates of files."""
        found_files = []
        for path in self.start_menu_programs_path:
            files = [item for item in path.iterdir() if item.is_file()]
            for file in files:
                if file.name in found_files:
                    file.unlink()
                else:
                    found_files.append(file.name)

    def flatten_folders_containing_one_file(self):
        """Flatten folders that are only containing one file."""
        whitelist = []
        if pathlib.WindowsPath("flatten_folders_exceptions.txt").exists():
            with open("flatten_folders_exceptions.txt") as file:
                whitelist = file.read().splitlines()

        for path in self.start_menu_programs_path:
            for directory in get_nested_directories(path):
                if directory.exists() and len(list(
                        directory.iterdir())) <= 1 and directory.name not in whitelist and directory.name not in self.protected_folders:
                    for item in directory.iterdir():
                        item.replace(item.parents[1].joinpath(item.name))

    def flatten_all_folders(self):
        """Flatten all folders."""
        whitelist = []
        if pathlib.WindowsPath("flatten_folders_exceptions.txt").exists():
            with open("flatten_folders_exceptions.txt") as file:
                whitelist = file.read().splitlines()

        for path in self.start_menu_programs_path:
            for directory in get_nested_directories(path):
                if directory.name not in whitelist and directory.name not in self.protected_folders:
                    for item in directory.iterdir():
                        item.replace(path.joinpath(item.name))

    def delete_empty_folders(self):
        """Delete empty folders."""
        for path in self.start_menu_programs_path:
            for directory in get_nested_directories(path):
                if len(list(
                        directory.iterdir())) == 0 and directory.name not in self.protected_folders:
                    directory.rmdir()

    def delete_broken_links(self):
        """Delete links that point to a non existing file."""
        for path in self.start_menu_programs_path:
            for link in get_nested_links(path):
                if not link.exists() or not windows_shortcuts.read_shortcut(link).exists():
                    link.unlink()

    def delete_files_with_names_containing(self):
        """Deletes files whose names contain the strings from the list."""
        match_strings = []
        if pathlib.WindowsPath("delete_files_with_names_containing.txt").exists():
            with open("delete_files_with_names_containing.txt") as file:
                match_strings = file.read().splitlines()

        for path in self.start_menu_programs_path:
            for file in get_nested_files(path):
                for match_string in match_strings:
                    if match_string in file.name:
                        file.unlink()

    def delete_files_matching_file_types(self):
        """Delete files that match the file types."""
        file_types = []
        if pathlib.WindowsPath("delete_based_on_file_type_list.txt").exists():
            with open("delete_based_on_file_type_list.txt") as file:
                file_types = file.read().splitlines()

        for path in self.start_menu_programs_path:
            for file_type in file_types:
                files = get_nested_files(path)
                for file, resolved_file in zip(files, resolve_files(files)):
                    if resolved_file.name.endswith(file_type) and resolved_file.is_file():
                        file.unlink()

    def delete_files_not_matching_file_types(self):
        """Delete files that do not match the file types."""
        file_types = []
        if pathlib.WindowsPath("delete_based_on_file_type_list.txt").exists():
            with open("delete_based_on_file_type_list.txt") as file:
                file_types = file.read().splitlines()

        for path in self.start_menu_programs_path:
            for file_type in file_types:
                for file in get_nested_files(path):
                    if not file.name.endswith(file_type) and file.is_file():
                        file.unlink()


def get_nested_directories(directory: pathlib.WindowsPath) -> List[pathlib.WindowsPath]:
    """Return all directories inside directory and its child directories."""
    directories = []
    for item in directory.iterdir():
        if item.is_dir():
            directories.append(item)
    for directory in directories:
        for item in directory.iterdir():
            if item.is_dir():
                directories.append(item)
    return directories


def get_nested_files(directory: pathlib.WindowsPath) -> List[pathlib.WindowsPath]:
    """Return all files inside directory and its child directories."""
    files = []
    for current_directory in get_nested_directories(directory):
        for item in current_directory.iterdir():
            if item.is_file():
                files.append(item)
    return files


def get_nested_links(directory: pathlib.WindowsPath) -> List[pathlib.WindowsPath]:
    """Return all links inside directory and its child directories."""
    links = []
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


class StoppableThread(threading.Thread):
    """Thread class with a stop() method.

    The thread itself has to check regularly for the stopped() condition.

    Copied from: https://stackoverflow.com/a/325528
    """

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        """Signals to the thread that it should stop."""
        self._stop_event.set()

    def stopped(self) -> bool:
        """Return whether the thread is supposed to be stopped."""
        return self._stop_event.is_set()
