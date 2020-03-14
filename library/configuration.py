"""Loads, edits and saves the configuration."""
import configparser
from typing import Optional, Union

from library import constants


class Configuration:
    """Interact with the configuration file."""
    def __init__(self):
        self._config: configparser.ConfigParser = configparser.ConfigParser()

        self.reload()

        if not self._config.sections():
            self._create_new_config()
        elif self._config["app_info"]["version"] != constants.VERSION_NUMBER:
            self._migrate_config()

    def _create_new_config(self, options: Optional[dict] = None):
        """Create a new configuration file."""
        self._config["app_info"] = {
            "version": constants.VERSION_NUMBER
        }
        self._config["options"] = {
            "flatten_folders_str": "None",
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

    def _migrate_config(self):
        """Migrates the configuration of an old version to a new configuration file."""
        old_options = dict(self._config["options"])
        self._create_new_config(old_options)

    def reload(self):
        """Reload the configuration from the configuration file."""
        self._config.read(constants.CONFIGURATION_FILE_PATH)

    def save(self):
        """Save the configuration to the configuration file."""
        if not constants.CONFIGURATION_PATH.exists():
            constants.CONFIGURATION_PATH.mkdir()
        with open(constants.CONFIGURATION_FILE_PATH, "w") as configfile:
            self._config.write(configfile)

    def get(self, key: str) -> Union[bool, int, float, str]:
        """Get a value from the configuration in its correct type."""
        if key.endswith("_bool"):
            return self._config["options"].getboolean(key)
        if key.endswith("_int"):
            return self._config["options"].getint(key)
        if key.endswith("_float"):
            return self._config["options"].getfloat(key)
        return self._config["options"][key]

    def set(self, key: str, value: Union[bool, int, float, str]):
        """Set a value in the configuration."""
        self._config["options"][key] = str(value)
