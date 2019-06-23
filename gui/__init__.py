import wx
import wx.adv

import configuration
from gui.exception_list import ExceptionList
from gui.task_bar_icon import TaskBarIcon


class MainFrame(wx.Frame):
    """Main Frame of the GUI."""

    def __init__(self):
        """Set up Main Frame."""
        super().__init__(parent=None, title="Windows Start-menu helper")
        self.icon = wx.Icon(name="icon.png", type=wx.BITMAP_TYPE_PNG)
        self.SetIcon(self.icon)

        self.task_bar_icon = TaskBarIcon(self.stop_scanning)

        self.config = configuration.Configuration()

        # Widgets
        main_panel = wx.Panel(self)

        self.flatten_folder_radiobox = wx.RadioBox(main_panel, label="Flatten folders",
                                                   choices=["All",
                                                            "Only ones with one item in them",
                                                            "None"])
        self.flatten_folder_radiobox.Bind(wx.EVT_RADIOBOX, self.on_flatten_folder_radiobox)
        self.flatten_folder_radiobox.SetStringSelection(
            self.config.get_value("flatten_folders_str"))

        self.flatten_folder_exceptions_button = wx.Button(main_panel, label="Exceptions")
        self.flatten_folder_exceptions_button.Bind(wx.EVT_BUTTON, lambda
            _: self.open_flatten_folders_exception_list())
        if self.config.get_value("flatten_folders_str") == "None":
            self.flatten_folder_exceptions_button.Disable()

        self.delete_empty_folders_checkbox = wx.CheckBox(main_panel, label="Delete empty folders")
        self.delete_empty_folders_checkbox.SetValue(
            self.config.get_value("delete_empty_folders_bool"))

        self.delete_based_on_file_type_radiobox = wx.RadioBox(main_panel,
                                                              label="Delete files with file types that are",
                                                              choices=["in the list",
                                                                       "not in the list"])
        self.delete_based_on_file_type_radiobox.SetStringSelection(
            self.config.get_value("delete_files_based_on_file_type_str"))

        self.delete_based_on_file_type_list_button = wx.Button(main_panel, label="List")
        self.delete_based_on_file_type_list_button.Bind(wx.EVT_BUTTON, lambda
            _: self.open_delete_based_on_file_type_list())

        self.delete_duplicates_checkbox = wx.CheckBox(main_panel, label="Delete duplicates")
        self.delete_duplicates_checkbox.SetValue(self.config.get_value("delete_duplicates_bool"))

        self.start_button = wx.Button(main_panel, label="Start")
        self.start_button.Bind(wx.EVT_BUTTON, lambda _: self.start_scanning())

        # Sizers
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        folder_sizer = wx.StaticBoxSizer(wx.VERTICAL, main_panel, label="Folders")
        file_sizer = wx.StaticBoxSizer(wx.VERTICAL, main_panel, label="Files")
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        frame_sizer.Add(main_panel)

        main_sizer.Add(folder_sizer, 1, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(file_sizer, 1, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(buttons_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 10)

        folder_sizer.Add(self.flatten_folder_radiobox, 0, wx.ALL | wx.ALIGN_CENTER)
        folder_sizer.Add(self.flatten_folder_exceptions_button, 0, wx.ALL | wx.ALIGN_CENTER)
        folder_sizer.AddSpacer(20)
        folder_sizer.Add(self.delete_empty_folders_checkbox, 0, wx.ALL | wx.ALIGN_CENTER)

        file_sizer.Add(self.delete_based_on_file_type_radiobox, 0, wx.ALL | wx.ALIGN_CENTER)
        file_sizer.Add(self.delete_based_on_file_type_list_button, 0, wx.ALL | wx.ALIGN_CENTER)
        file_sizer.AddSpacer(20)
        file_sizer.Add(self.delete_duplicates_checkbox, 0, wx.ALL | wx.ALIGN_CENTER)

        buttons_sizer.Add(self.start_button, 0, wx.ALL | wx.ALIGN_CENTER)

        main_panel.SetSizer(main_sizer)

        self.SetSizerAndFit(frame_sizer)
        self.Center()

    def on_flatten_folder_radiobox(self, event):
        """Enable/disable exceptions button for flatten folder setting based on selection."""
        if event.GetString() == "None":
            self.flatten_folder_exceptions_button.Disable()
        else:
            self.flatten_folder_exceptions_button.Enable()

    def open_flatten_folders_exception_list(self):
        """Open the list that manages exceptions to the flatten folders option."""
        exceptions_list = ExceptionList(self, title="Flatten folders exceptions",
                                        file="flatten_folders_exceptions.txt")
        exceptions_list.ShowModal()

    def open_delete_based_on_file_type_list(self):
        """Open the list that manages the file types based on which files should be deleted."""
        exceptions_list = ExceptionList(self, title="Delete based on file type list",
                                        file="delete_based_on_file_type_list.txt")
        exceptions_list.ShowModal()

    def save_config(self):
        """Saves the current configuration."""
        self.config.set_value("flatten_folders_str",
                              self.flatten_folder_radiobox.GetStringSelection())
        self.config.set_value("delete_empty_folders_bool",
                              self.delete_empty_folders_checkbox.IsChecked())
        self.config.set_value("delete_duplicates_bool", self.delete_duplicates_checkbox.IsChecked())
        self.config.set_value("delete_files_based_on_file_type_str",
                              self.delete_based_on_file_type_radiobox.GetStringSelection())
        self.config.save()

    def start_scanning(self):
        """Start scanning and hide GUI except for taskbar icon."""
        self.Hide()
        self.task_bar_icon.show()
        self.save_config()

    def stop_scanning(self):
        """Stop scanning and show GUI."""
        self.task_bar_icon.hide()
        self.Show()
