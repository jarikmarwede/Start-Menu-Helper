"""Reorganize the start menu folder."""
import logging
import re
import time

from library import constants
from library.configuration import Configuration
from library.helpers import windows_shortcuts
from library.helpers.file_system import (
    get_nested_directories,
    get_nested_files,
    get_nested_links,
    resolve_files,
    file_is_writable
)
from library.helpers.stopable_thread import StoppableThread


class StartMenuHelper:
    """Starts and stops cleaning."""
    def __init__(self, config: Configuration) -> None:
        self._config = config
        self._cleaner_thread: StoppableThread = StoppableThread()

    def start_cleaning(self) -> None:
        """Starts the cleaning based on the configuration."""
        self._cleaner_thread = StoppableThread(target=self._clean, daemon=True)
        self._cleaner_thread.start()
        logging.debug("Cleaning started")

    def stop_cleaning(self) -> None:
        """Stops the cleaning."""
        self._cleaner_thread.stop()
        self._cleaner_thread.join()

    def _clean(self) -> None:
        """Cleans based on configuration.

        This method is supposed to be run by the _cleaner_thread.
        """
        self._config.reload()
        while not self._cleaner_thread.stopped():
            self.move_files_to_programs_directory()

            self.delete_files_with_names_containing()
            cleaning_functions = {
                self.delete_files_matching_file_types:
                    self._config.get("delete_files_based_on_file_type_str") == "in the list",
                self.delete_files_not_matching_file_types:
                    self._config.get("delete_files_based_on_file_type_str") == "not in the list",
                self.delete_broken_links:
                    self._config.get("delete_broken_links_bool"),
                self.delete_links_to_folders:
                    self._config.get("delete_links_to_folders_bool"),
                self.delete_duplicates:
                    self._config.get("delete_duplicates_bool"),
                self.flatten_folders_with_whitelist:
                    self._config.get("flatten_folders_list_type_str") == "whitelist",
                self.flatten_folders_with_blacklist:
                    self._config.get("flatten_folders_list_type_str") == "blacklist",
                self.flatten_folders_containing_one_file:
                    self._config.get("flatten_folders_containing_only_one_item_bool"),
                self.delete_empty_folders:
                    self._config.get("delete_empty_folders_bool")
            }

            for function, turned_on in cleaning_functions.items():
                if turned_on:
                    function()

            for _ in range(constants.TIME_BETWEEN_SCANS_IN_MINUTES * 60 * 1000):
                if not self._cleaner_thread.stopped():
                    time.sleep(0.001)

    def move_files_to_programs_directory(self) -> None:
        """Move all files to the programs directory."""
        for path in constants.START_MENU_PATHS:
            for item in path.iterdir():
                if item.name != "Programs" and file_is_writable(item):
                    item.replace(path.joinpath("Programs").joinpath(item.name))

    def delete_duplicates(self) -> None:
        """Delete duplicates of files."""
        found_files = []
        for path in constants.START_MENU_PROGRAMS_PATHS:
            files = [item for item in path.iterdir() if item.is_file()]
            for file in files:
                if file.name in found_files:
                    file.unlink()
                    logging.info("Deleted duplicate: %s", file)
                else:
                    found_files.append(file.name)

    def flatten_folders_containing_one_file(self) -> None:
        """Flatten folders that only contain one file."""
        blacklist = self._config.flatten_folders_containing_one_file_exceptions
        for path in constants.START_MENU_PROGRAMS_PATHS:
            nested_directories = get_nested_directories(path)
            nested_directories.reverse()  # Reverse the list to flatten the deepest folders first
            for directory in nested_directories:
                if (directory.exists() and
                        len(list(directory.iterdir())) <= 1 and
                        directory.name not in blacklist and
                        directory.name not in constants.PROTECTED_FOLDERS):
                    for item in directory.iterdir():
                        item.replace(item.parents[1].joinpath(item.name))
                    logging.info("Flattened folder: %s", directory)

    def flatten_folders_with_whitelist(self) -> None:
        """Flatten folders while respecting exceptions as a whitelist."""
        whitelist = self._config.flatten_folders_exceptions

        for path in constants.START_MENU_PROGRAMS_PATHS:
            nested_directories = get_nested_directories(path)
            nested_directories.reverse()  # Reverse the list to flatten the deepest folders first
            for directory in nested_directories:
                if directory.name in constants.PROTECTED_FOLDERS:
                    continue
                for word in whitelist:
                    if word in directory.name:
                        for item in directory.iterdir():
                            item.replace(path.joinpath(item.name))
                        logging.info("Flattened folder: %s", directory)
                        break

    def flatten_folders_with_blacklist(self) -> None:
        """Flatten folders while respecting exceptions as a blacklist."""
        blacklist = self._config.flatten_folders_exceptions

        for path in constants.START_MENU_PROGRAMS_PATHS:
            nested_directories = get_nested_directories(path)
            nested_directories.reverse()  # Reverse the list to flatten the deepest folders first
            for directory in nested_directories:
                if directory.name in constants.PROTECTED_FOLDERS:
                    continue
                for word in blacklist:
                    if word in directory.name:
                        break
                else:
                    for item in directory.iterdir():
                        item.replace(path.joinpath(item.name))
                    logging.info("Flattened folder: %s", directory)

    def delete_empty_folders(self) -> None:
        """Delete empty folders."""
        for path in constants.START_MENU_PROGRAMS_PATHS:
            for directory in get_nested_directories(path):
                if (len(list(directory.iterdir())) == 0 and
                        directory.name not in constants.PROTECTED_FOLDERS):
                    directory.rmdir()
                    logging.info("Deleted empty folder: %s", directory)

    def delete_broken_links(self) -> None:
        """Delete links that point to a non-existing file."""
        for path in constants.START_MENU_PROGRAMS_PATHS:
            for link in get_nested_links(path):
                if not link.exists() or not windows_shortcuts.read_shortcut(link).exists():
                    link.unlink()
                    logging.info(
                        "Deleted broken link: %s",
                        link
                    )

    def delete_files_with_names_containing(self) -> None:
        """Deletes files whose names contain the strings from the list."""
        match_strings = self._config.delete_files_with_names_containing_list
        for path in constants.START_MENU_PROGRAMS_PATHS:
            for file in get_nested_files(path):
                for match_string in match_strings:
                    if re.search(re.escape(match_string), file.name, flags=re.IGNORECASE):
                        file.unlink()
                        logging.info(
                            "Deleted file \"%s\" "
                            "because the file name contained \"%s\"",
                            file,
                            match_string
                        )

    def delete_files_matching_file_types(self) -> None:
        """Delete files that match the file types."""
        file_types = self._config.delete_matching_file_types_exceptions

        for path in constants.START_MENU_PROGRAMS_PATHS:
            for file_type in file_types:
                files = get_nested_files(path)
                for file, resolved_file in zip(files, resolve_files(files)):
                    if resolved_file.name.endswith(file_type) and resolved_file.is_file():
                        file.unlink()
                        logging.info(
                            "Deleted file \"%s\" "
                            "because it had the extension \"%s\"",
                            file,
                            file_type
                        )

    def delete_files_not_matching_file_types(self) -> None:
        """Delete files that do not match the file types."""
        file_types = self._config.delete_matching_file_types_exceptions

        for path in constants.START_MENU_PROGRAMS_PATHS:
            for file_type in file_types:
                for file in get_nested_files(path):
                    if not file.name.endswith(file_type) and file.is_file():
                        file.unlink()
                        logging.info(
                            "Deleted file \"%s\" because it did not have any of "
                            "the required extensions",
                            file
                        )

    def delete_links_to_folders(self) -> None:
        """Delete links that link to folders."""
        for path in constants.START_MENU_PROGRAMS_PATHS:
            for link in get_nested_links(path):
                if windows_shortcuts.read_shortcut(link).is_dir():
                    link.unlink()
                    logging.info(
                        "Deleted link to folder: %s",
                        link
                    )
