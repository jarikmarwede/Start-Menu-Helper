import configparser
import typing


class Configuration:

    def __init__(self):
        self._config = configparser.ConfigParser()

        self.reload()

        if not self._config.sections():
            self._create_new_config()

    def _create_new_config(self):
        """Create a default configuration file."""
        self._config["options"] = {
            "flatten_folders_str": "None",
            "delete_empty_folders_bool": False,
            "delete_duplicates_bool": False,
            "delete_files_based_on_file_type_str": "in the list"
        }
        self.save()

    def reload(self):
        """Reload the configuration from the configuration file."""
        self._config.read("config.ini")

    def save(self):
        """Save the configuration to the configuration file."""
        with open("config.ini", "w") as configfile:
            self._config.write(configfile)

    def get_value(self, value: str) -> typing.Union[bool, int, float, str]:
        """Get a value from the configuration in its correct type."""
        if value.endswith("_bool"):
            return self._config["options"].getboolean(value)
        elif value.endswith("_int"):
            return self._config["options"].getint(value)
        elif value.endswith("_float"):
            return self._config["options"].getfloat(value)
        else:
            return self._config["options"][value]
