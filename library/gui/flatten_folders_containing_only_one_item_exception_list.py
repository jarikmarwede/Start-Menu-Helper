"""Edit the exceptions for the flatten folders containing only one item functionality."""
from wx import Window

from library.configuration import Configuration
from library.gui.exception_list import ExceptionList


class FlattenFoldersContainingOnlyOneItemExceptionList(ExceptionList):
    """List widget for editing exceptions for the flatten folders that only contain on item functionality."""
    def __init__(self, parent: Window, title: str, configuration: Configuration):
        super().__init__(parent, title)
        self._configuration = configuration

        self.load()

    def load(self) -> None:
        self.exceptions_list.SetStrings(self._configuration.flatten_folders_containing_one_file_exceptions)

    def save(self) -> None:
        self._configuration.flatten_folders_containing_one_file_exceptions = self.exceptions_list.GetStrings()
        self.close()
