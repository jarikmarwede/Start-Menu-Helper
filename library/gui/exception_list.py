"""Edit the exceptions for different cleaning functions."""
import os

import wx
import wx.adv


class ExceptionList(wx.Dialog):
    """A list widget that allows users to edit the exception files."""
    def __init__(self, parent, title, file):
        super().__init__(parent=parent, title=title)

        self.file = file

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

        self.load()

        self.SetSizerAndFit(frame_sizer)
        self.Center()

    def load(self):
        """Load the list from its file."""
        if os.path.exists(self.file):
            with open(self.file) as file:
                self.exceptions_list.SetStrings(file.read().splitlines())

    def save(self):
        """Save the list and close the dialog."""
        with open(self.file, "w") as file:
            for string in self.exceptions_list.GetStrings():
                file.write(string + "\n")
        self.close()

    def close(self):
        """Close the dialog."""
        self.EndModal(0)
