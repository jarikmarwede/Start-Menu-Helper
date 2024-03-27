"""Reorganize the start menu folder."""
import logging
import re
import time

from library import configuration, constants
from library.helpers import windows_shortcuts
from library.helpers.file_system import (
    get_nested_directories,
    get_nested_files,
    get_nested_links,
    resolve_files
)
from library.helpers.stopable_thread import StoppableThread


class StartMenuHelper:
    """Starts and stops cleaning."""
    def __init__(self) -> None:
        self._config: configuration.Configuration = configuration.Configuration()
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
            move_files_to_programs_directory()

            delete_files_with_names_containing()
            cleaning_functions = {
                delete_files_matching_file_types:
                    self._config.get("delete_files_based_on_file_type_str") == "in the list",
                delete_files_not_matching_file_types:
                    self._config.get("delete_files_based_on_file_type_str") == "not in the list",
                delete_broken_links:
                    self._config.get("delete_broken_links_bool"),
                delete_links_to_folders:
                    self._config.get("delete_links_to_folders_bool"),
                delete_duplicates:
                    self._config.get("delete_duplicates_bool"),
                flatten_folders_with_whitelist:
                    self._config.get("flatten_folders_list_type_str") == "whitelist",
                flatten_folders_with_blacklist:
                    self._config.get("flatten_folders_list_type_str") == "blacklist",
                flatten_folders_containing_one_file:
                    self._config.get("flatten_folders_containing_only_one_item_bool"),
                delete_empty_folders:
                    self._config.get("delete_empty_folders_bool")
            }

            for function, turned_on in cleaning_functions.items():
                if turned_on:
                    function()

            for _ in range(constants.TIME_BETWEEN_SCANS_IN_MINUTES * 60 * 1000):
                if not self._cleaner_thread.stopped():
                    time.sleep(0.001)


def move_files_to_programs_directory() -> None:
    """Move all files to the programs directory."""
    for path in constants.START_MENU_PATHS:
        for item in path.iterdir():
            if item.name != "Programs":
                item.replace(path.joinpath("Programs").joinpath(item.name))


def delete_duplicates() -> None:
    """Delete duplicates of files."""
    found_files = []
    for path in constants.START_MENU_PROGRAMS_PATHS:
        files = [item for item in path.iterdir() if item.is_file()]
        for file in files:
            if file.name in found_files:
                file.unlink()
                logging.info(f"Deleted duplicate: {str(file)}")
            else:
                found_files.append(file.name)


def flatten_folders_containing_one_file() -> None:
    """Flatten folders that only contain one file."""
    blacklist = []
    if constants.FLATTEN_FOLDERS_WITH_ONE_ITEM_EXCEPTIONS_PATH.exists():
        with open(constants.FLATTEN_FOLDERS_WITH_ONE_ITEM_EXCEPTIONS_PATH) as file:
            blacklist = file.read().splitlines()

    for path in constants.START_MENU_PROGRAMS_PATHS:
        for directory in get_nested_directories(path):
            if (directory.exists() and
                    len(list(directory.iterdir())) <= 1 and
                    directory.name not in blacklist and
                    directory.name not in constants.PROTECTED_FOLDERS):
                for item in directory.iterdir():
                    item.replace(item.parents[1].joinpath(item.name))
                logging.info(f"Flattened folder: {str(directory)}")


def flatten_folders_with_whitelist() -> None:
    """Flatten folders while respecting exceptions as a whitelist."""
    whitelist = []
    if constants.FLATTEN_FOLDERS_EXCEPTIONS_PATH.exists():
        with open(constants.FLATTEN_FOLDERS_EXCEPTIONS_PATH) as file:
            whitelist = file.read().splitlines()

    for path in constants.START_MENU_PROGRAMS_PATHS:
        for directory in get_nested_directories(path):
            if (directory.name in whitelist and
                    directory.name not in constants.PROTECTED_FOLDERS):
                for item in directory.iterdir():
                    item.replace(path.joinpath(item.name))
                logging.info(f"Flattened folder: {str(directory)}")


def flatten_folders_with_blacklist() -> None:
    """Flatten folders while respecting exceptions as a blacklist."""
    blacklist = []
    if constants.FLATTEN_FOLDERS_EXCEPTIONS_PATH.exists():
        with open(constants.FLATTEN_FOLDERS_EXCEPTIONS_PATH) as file:
            blacklist = file.read().splitlines()

    for path in constants.START_MENU_PROGRAMS_PATHS:
        for directory in get_nested_directories(path):
            if (directory.name not in blacklist and
                    directory.name not in constants.PROTECTED_FOLDERS):
                for item in directory.iterdir():
                    item.replace(path.joinpath(item.name))
                logging.info(f"Flattened folder: {str(directory)}")


def delete_empty_folders() -> None:
    """Delete empty folders."""
    for path in constants.START_MENU_PROGRAMS_PATHS:
        for directory in get_nested_directories(path):
            if (len(list(directory.iterdir())) == 0 and
                    directory.name not in constants.PROTECTED_FOLDERS):
                directory.rmdir()
                logging.info(f"Deleted empty folder: {str(directory)}")


def delete_broken_links() -> None:
    """Delete links that point to a non-existing file."""
    for path in constants.START_MENU_PROGRAMS_PATHS:
        for link in get_nested_links(path):
            if not link.exists() or not windows_shortcuts.read_shortcut(link).exists():
                link.unlink()
                logging.info(f"Deleted broken link: {str(link)}")


def delete_files_with_names_containing() -> None:
    """Deletes files whose names contain the strings from the list."""
    match_strings = []
    if constants.DELETE_FILES_WITH_NAMES_CONTAINING_LIST_PATH.exists():
        with open(constants.DELETE_FILES_WITH_NAMES_CONTAINING_LIST_PATH) as list_file:
            match_strings = list_file.read().splitlines()

    for path in constants.START_MENU_PROGRAMS_PATHS:
        for file in get_nested_files(path):
            for match_string in match_strings:
                if re.search(re.escape(match_string), file.name, flags=re.IGNORECASE):
                    file.unlink()
                    logging.info(
                        f"Deleted file \"{str(file)}\" because the file name contained \"{match_string}\""
                    )


def delete_files_matching_file_types() -> None:
    """Delete files that match the file types."""
    file_types = []
    if constants.DELETE_FILES_MATCHING_FILE_TYPES_LIST_PATH.exists():
        with open(constants.DELETE_FILES_MATCHING_FILE_TYPES_LIST_PATH) as list_file:
            file_types = list_file.read().splitlines()

    for path in constants.START_MENU_PROGRAMS_PATHS:
        for file_type in file_types:
            files = get_nested_files(path)
            for file, resolved_file in zip(files, resolve_files(files)):
                if resolved_file.name.endswith(file_type) and resolved_file.is_file():
                    file.unlink()
                    logging.info(
                        f"Deleted file \"{str(file)}\" because it had the extension \"{file_type}\""
                    )


def delete_files_not_matching_file_types() -> None:
    """Delete files that do not match the file types."""
    file_types = []
    if constants.DELETE_FILES_MATCHING_FILE_TYPES_LIST_PATH.exists():
        with open(constants.DELETE_FILES_MATCHING_FILE_TYPES_LIST_PATH) as list_file:
            file_types = list_file.read().splitlines()

    for path in constants.START_MENU_PROGRAMS_PATHS:
        for file_type in file_types:
            for file in get_nested_files(path):
                if not file.name.endswith(file_type) and file.is_file():
                    file.unlink()
                    logging.info(
                        f"Deleted file \"{str(file)}\" because it did not have any of "
                        "the required extensions"
                    )


def delete_links_to_folders() -> None:
    """Delete links that link to folders."""
    for path in constants.START_MENU_PROGRAMS_PATHS:
        for link in get_nested_links(path):
            if windows_shortcuts.read_shortcut(link).is_dir():
                link.unlink()
                logging.info(f"Deleted link to folder: {str(link)}")
