"""Windows task bar icon."""
import typing

import wx
import wx.adv

from library import constants
from library.helpers import pyinstaller_asset


class TaskBarIcon(wx.adv.TaskBarIcon):
    """Icon that appears in the windows taskbar when cleaning in background."""
    def __init__(self, open_callback: typing.Callable):
        super().__init__()

        self._open_callback = open_callback

        self._icon = wx.Icon(name=pyinstaller_asset.asset_path(constants.ICON_FILE_NAME),
                             type=wx.BITMAP_TYPE_ICO)

        self._task_bar_menu = wx.Menu()
        self._task_bar_menu.Append(wx.ID_OPEN, "Open")
        self._task_bar_menu.Append(wx.ID_CLOSE, "Close")
        self._task_bar_menu.Bind(wx.EVT_MENU, self._on_menu_select)

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, lambda _: open_callback())

    def CreatePopupMenu(self) -> wx.Menu:  # pylint: disable=C0103
        """Overwrites wx.adv.TaskBarIcon.CreatePopupMenu
        to set self._task_bar_menu as standard menu."""
        return self._task_bar_menu

    def _on_menu_select(self, event: wx.MenuEvent) -> None:
        """Do actions of menu items."""
        event_id = event.GetId()
        if event_id == wx.ID_OPEN:
            self._open_callback()
        elif event_id == wx.ID_CLOSE:
            wx.Exit()

    def show(self) -> None:
        """Show the icon in the taskbar."""
        self.SetIcon(self._icon, "Start-menu helper")

    def hide(self) -> None:
        """Hide the icon from the taskbar."""
        self.RemoveIcon()
