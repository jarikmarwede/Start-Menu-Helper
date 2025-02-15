"""Loads, edits and saves the configuration."""
import configparser
import pathlib
from typing import Optional, Union, List

from library import constants


class Configuration:
    """Interact with the configuration files."""
    def __init__(self, configuration_directory: pathlib.Path) -> None:
        self._config: configparser.ConfigParser = configparser.ConfigParser()
        self._configuration_directory = configuration_directory
        self._configuration_file = configuration_directory.joinpath("config.ini")
        self._flatten_folders_exception_path = configuration_directory.joinpath(
            "flatten_folders_exceptions.txt"
        )
        self._flatten_folders_with_one_item_exception_path = configuration_directory.joinpath(
            "flatten_folders_with_one_item_exceptions.txt"
        )
        self._delete_files_with_names_containing_list_path = configuration_directory.joinpath(
            "delete_files_with_names_containing.txt"
        )
        self._delete_files_matching_file_types_list_path = configuration_directory.joinpath(
            "delete_based_on_file_type_list.txt"
        )

        self.reload()

        if self._empty:
            self._create_new_config()
        elif self._config["app_info"]["version"] != constants.VERSION_NUMBER:
            self._migrate_config()

    def _create_new_config(self, options: Optional[dict] = None) -> None:
        """Create a new configuration file."""
        self._config["app_info"] = {
            "version": constants.VERSION_NUMBER
        }
        self._config["options"] = {
            "flatten_folders_containing_only_one_item_bool": "False",
            "flatten_folders_list_type_str": "whitelist",
            "delete_empty_folders_bool": "False",
            "delete_links_to_folders_bool": "False",
            "delete_duplicates_bool": "False",
            "delete_files_based_on_file_type_str": "in the list",
            "delete_broken_links_bool": "False",
        }

        if options:
            for key, value in options.items():
                self._config["options"][key] = value

        self.save()

    def _migrate_config(self) -> None:
        """Migrates the configuration of an old version to a new configuration file."""
        old_options = dict(self._config["options"])
        self._create_new_config(old_options)

    def reload(self) -> None:
        """Reload the configuration from the configuration file."""
        self._config.read(self._configuration_file)

    def save(self) -> None:
        """Save the configuration to the configuration file."""
        if not self._configuration_directory.exists():
            self._configuration_directory.mkdir()
        with open(self._configuration_file, "w", encoding="utf-8") as configfile:
            self._config.write(configfile)

    def get(self, key: str) -> Union[bool, int, float, str]:
        """Get a value from the configuration in its correct type."""
        option: Union[bool, int, float, str, None]
        if key.endswith("_bool"):
            option = self._config["options"].getboolean(key)
        elif key.endswith("_int"):
            option = self._config["options"].getint(key)
        elif key.endswith("_float"):
            option = self._config["options"].getfloat(key)
        else:
            option = self._config["options"][key]
        assert option is not None
        return option

    def set(self, key: str, value: Union[bool, int, float, str]) -> None:
        """Set a value in the configuration."""
        self._config["options"][key] = str(value)

    @property
    def _empty(self) -> bool:
        return not self._config.sections()

    @staticmethod
    def _get_list_from_file(file_path: pathlib.Path) -> List[str]:
        """Read a newline separated list of strings from a file."""
        strings = []
        if file_path.exists():
            with open(file_path, encoding="utf-8") as file:
                strings = file.read().splitlines()

        return strings

    @staticmethod
    def _save_list_to_file(file_path: pathlib.Path, strings: List[str]) -> None:
        """Write a newline separated list of strings to a file."""
        with open(file_path, "w", encoding="utf-8") as file:
            for string in strings:
                file.write(string + "\n")

    @property
    def flatten_folders_exceptions(self) -> List[str]:
        """Get list of exceptions for flattening folders."""
        return self._get_list_from_file(self._flatten_folders_exception_path)

    @flatten_folders_exceptions.setter
    def flatten_folders_exceptions(self, exceptions: List[str]) -> None:
        """Set list of exceptions for flattening folders."""
        self._save_list_to_file(self._flatten_folders_exception_path, exceptions)

    @property
    def flatten_folders_containing_one_file_exceptions(self) -> List[str]:
        """Get list of exceptions for flattening folders only containing one file."""
        return self._get_list_from_file(self._flatten_folders_with_one_item_exception_path)

    @flatten_folders_containing_one_file_exceptions.setter
    def flatten_folders_containing_one_file_exceptions(self, exceptions: List[str]) -> None:
        """Set list of exceptions for flattening folders only containing one file."""
        self._save_list_to_file(self._flatten_folders_with_one_item_exception_path, exceptions)

    @property
    def delete_files_with_names_containing_list(self) -> List[str]:
        """Get list of phrases to delete files by."""
        return self._get_list_from_file(self._delete_files_with_names_containing_list_path)

    @delete_files_with_names_containing_list.setter
    def delete_files_with_names_containing_list(self, phrases: List[str]) -> None:
        """Set list of phrases to delete files by."""
        self._save_list_to_file(self._delete_files_with_names_containing_list_path, phrases)

    @property
    def delete_matching_file_types_exceptions(self) -> List[str]:
        """Get list of exceptions for deleting files (not) matching certain file types."""
        return self._get_list_from_file(self._delete_files_matching_file_types_list_path)

    @delete_matching_file_types_exceptions.setter
    def delete_matching_file_types_exceptions(self, exceptions: List[str]) -> None:
        """Set list of exceptions for deleting files (not) matching certain file types."""
        self._save_list_to_file(self._delete_files_matching_file_types_list_path, exceptions)
