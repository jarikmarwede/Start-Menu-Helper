"""Main menu bar widget."""
import os
import pathlib
import webbrowser

import wx

from library.constants import DOCUMENTATION_URL, ISSUE_TRACKER_URL, LOG_FILE_NAME
from library.gui.about_dialog import AboutDialog

ID_OPEN_CONFIG_DIRECTORY = wx.NewId()
ID_OPEN_LOG_FILE = wx.NewId()
ID_OPEN_DOCUMENTATION = wx.NewId()
ID_OPEN_ISSUE_TRACKER = wx.NewId()
ID_OPEN_ABOUT_DIALOG = wx.NewId()


class MainMenu(wx.MenuBar):
    """Main menu bar widget."""
    def __init__(self, frame: wx.Frame, config_directory: pathlib.Path) -> None:
        """Initialize main menu bar."""
        super().__init__()

        self._frame = frame
        self._config_directory = config_directory

        self.add_help_menu()

        self.Bind(wx.EVT_MENU, self.handle_menu_click)

    def add_help_menu(self) -> None:
        """Append the help menu to the menu bar."""
        help_menu = wx.Menu()
        help_menu.Append(
            ID_OPEN_CONFIG_DIRECTORY,
            "Open configuration directory",
            "Open the configuration directory in Windows File Explorer"
        )
        help_menu.Append(
            ID_OPEN_LOG_FILE,
            "Open log file",
            "Open the log file"
        )
        help_menu.AppendSeparator()
        help_menu.Append(ID_OPEN_DOCUMENTATION, "Documentation", "Open the online documentation")
        help_menu.Append(ID_OPEN_ISSUE_TRACKER, "Report issue", "Open the issue tracker")
        help_menu.AppendSeparator()
        help_menu.Append(ID_OPEN_ABOUT_DIALOG, "About", "Open the about dialog")

        self.Append(help_menu, "Help")

    def handle_menu_click(self, event: wx.MenuEvent) -> None:
        """Handle menu item selection."""
        event_id = event.GetId()
        if event_id == ID_OPEN_DOCUMENTATION:
            webbrowser.open_new_tab(DOCUMENTATION_URL)
        elif event_id == ID_OPEN_ISSUE_TRACKER:
            webbrowser.open_new_tab(ISSUE_TRACKER_URL)
        elif event_id == ID_OPEN_CONFIG_DIRECTORY:
            os.startfile(self._config_directory, "explore") # nosec B606
        elif event_id == ID_OPEN_LOG_FILE:
            os.startfile(self._config_directory.joinpath(LOG_FILE_NAME), "open") # nosec B606
        elif event_id == ID_OPEN_ABOUT_DIALOG:
            about_dialog = AboutDialog(self._frame)
            about_dialog.ShowModal()
