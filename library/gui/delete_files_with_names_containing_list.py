"""Edit the list for deleting files that match a phrase in their name functionality."""
from wx import Window

from library.configuration import Configuration
from library.gui.exception_list import ExceptionList


class DeleteFilesWithNamesContainingList(ExceptionList):
    """List widget for editing list of phrases for deleting files containing them in their file name."""
    def __init__(self, parent: Window, title: str, configuration: Configuration):
        super().__init__(parent, title)
        self._configuration = configuration

        self.load()

    def load(self) -> None:
        self.exceptions_list.SetStrings(self._configuration.delete_files_with_names_containing_list)

    def save(self) -> None:
        self._configuration.delete_files_with_names_containing_list = self.exceptions_list.GetStrings()
        self.close()
