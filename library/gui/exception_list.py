"""Edit the exceptions for different cleaning rules."""
from abc import abstractmethod

import wx
import wx.adv


class ExceptionList(wx.Dialog):
    """A list widget that allows users to edit the exceptions to cleaning rules."""
    def __init__(self, parent: wx.Window, title: str):
        super().__init__(parent=parent, title=title)

        # widgets
        main_panel = wx.Panel(self)

        self.exceptions_list = wx.adv.EditableListBox(main_panel)

        self.save_button = wx.Button(main_panel, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, lambda _: self.save())

        self.cancel_button = wx.Button(main_panel, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, lambda _: self.close())

        # sizers
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        frame_sizer.Add(main_panel)

        main_sizer.Add(self.exceptions_list, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        main_sizer.Add(buttons_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        buttons_sizer.Add(self.save_button, 0, wx.ALL | wx.ALIGN_CENTER)
        buttons_sizer.AddSpacer(10)
        buttons_sizer.Add(self.cancel_button, 0, wx.ALL | wx.ALIGN_CENTER)

        main_panel.SetSizer(main_sizer)

        self.SetSizerAndFit(frame_sizer)
        self.Center()

    @abstractmethod
    def load(self) -> None:
        """Load the list from its file."""

    @abstractmethod
    def save(self) -> None:
        """Save the list and close the dialog."""

    def close(self) -> None:
        """Close the dialog."""
        self.EndModal(0)
