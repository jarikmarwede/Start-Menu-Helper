"""Main menu bar widget."""
import webbrowser

import wx

from library.constants import DOCUMENTATION_URL, ISSUE_TRACKER_URL

ID_OPEN_DOCUMENTATION = wx.NewId()
ID_OPEN_ISSUE_TRACKER = wx.NewId()


class MainMenu(wx.MenuBar):
    """Main menu bar widget."""
    def __init__(self) -> None:
        """Initialize main menu bar."""
        super().__init__()

        self.add_help_menu()

        self.Bind(wx.EVT_MENU, self.handle_menu_click)

    def add_help_menu(self) -> None:
        """Append the help menu to the menu bar."""
        help_menu = wx.Menu()
        help_menu.Append(ID_OPEN_DOCUMENTATION, "Documentation", "Open the online documentation")
        help_menu.Append(ID_OPEN_ISSUE_TRACKER, "Report issue", "Open the issue tracker")

        self.Append(help_menu, "Help")

    def handle_menu_click(self, event: wx.MenuEvent) -> None:
        """Handle menu item selection."""
        event_id = event.GetId()
        if event_id == ID_OPEN_DOCUMENTATION:
            webbrowser.open_new_tab(DOCUMENTATION_URL)
        elif event_id == ID_OPEN_ISSUE_TRACKER:
            webbrowser.open_new_tab(ISSUE_TRACKER_URL)
