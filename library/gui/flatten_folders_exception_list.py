"""Edit the exceptions for the flatten folders functionality."""
from wx import Window

from library.configuration import Configuration
from library.gui.exception_list import ExceptionList


class FlattenFoldersExceptionList(ExceptionList):
    """A list widget that allows users to edit the exceptions for the flatten folders functionality."""
    def __init__(self, parent: Window, title: str, configuration: Configuration):
        super().__init__(parent, title)
        self._configuration = configuration

        self.load()

    def load(self) -> None:
        self.exceptions_list.SetStrings(self._configuration.flatten_folders_exceptions)

    def save(self) -> None:
        self._configuration.flatten_folders_exceptions = self.exceptions_list.GetStrings()
        self.close()
