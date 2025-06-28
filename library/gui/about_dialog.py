import wx

from library import constants


class AboutDialog(wx.Dialog):
    def __init__(self, parent: wx.Window):
        super().__init__(parent=parent, title=f"About {constants.PROGRAM_NAME}")

        main_panel = wx.Panel(self)

        heading_text = wx.StaticText(
            main_panel,
            label=constants.PROGRAM_NAME
        )
        text_font = heading_text.GetFont()
        text_font.SetPointSize(20)
        heading_text.SetFont(text_font)

        about_text = wx.StaticText(
            main_panel,
            label=f"Version: {constants.VERSION_NUMBER}"
        )

        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(heading_text, flag=wx.ALL, border=5)
        main_sizer.Add(about_text, flag=wx.ALL, border=5)

        frame_sizer.Add(main_panel, flag=wx.ALL | wx.EXPAND, border=10)

        main_panel.SetSizer(main_sizer)

        self.SetSizerAndFit(frame_sizer)
        self.Center()
