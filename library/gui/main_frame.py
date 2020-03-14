"""Main frame of the GUI."""
import wx
import wx.adv

from library import configuration, constants, start_menu_helper
from library.gui.exception_list import ExceptionList
from library.gui.task_bar_icon import TaskBarIcon
from library.helpers import pyinstaller_asset, windows_startup


class MainFrame(wx.Frame):
    """Main Frame of the GUI."""

    def __init__(self):
        """Set up Main Frame."""
        super().__init__(parent=None, title=constants.PROGRAM_NAME)
        self.Bind(wx.EVT_CLOSE, lambda _: wx.Exit())

        self.icon = wx.Icon(name=pyinstaller_asset.asset_path(constants.ICON_FILE_NAME),
                            type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        self.task_bar_icon = TaskBarIcon(self.stop_scanning)

        self.config = configuration.Configuration()
        self.start_menu_helper = start_menu_helper.StartMenuHelper()

        # Widgets
        main_panel = wx.Panel(self)

        self.flatten_folder_radiobox = wx.RadioBox(main_panel, label="Flatten folders",
                                                   choices=["All",
                                                            "Only ones with one item in them",
                                                            "None"])
        self.flatten_folder_radiobox.Bind(wx.EVT_RADIOBOX, self.on_flatten_folder_radiobox)
        self.flatten_folder_radiobox.SetStringSelection(
            self.config.get("flatten_folders_str"))

        self.flatten_folder_exceptions_button = wx.Button(main_panel, label="Exceptions")
        self.flatten_folder_exceptions_button.Bind(
            wx.EVT_BUTTON,
            lambda _: self.open_flatten_folders_exception_list()
        )
        if self.config.get("flatten_folders_str") == "None":
            self.flatten_folder_exceptions_button.Disable()

        self.delete_empty_folders_checkbox = wx.CheckBox(main_panel, label="Delete empty folders")
        self.delete_empty_folders_checkbox.SetValue(
            self.config.get("delete_empty_folders_bool"))

        self.delete_links_to_folders_checkbox = wx.CheckBox(main_panel,
                                                            label="Delete links to folders")
        self.delete_links_to_folders_checkbox.SetValue(
            self.config.get("delete_links_to_folders_bool"))

        self.delete_based_on_file_type_radiobox = wx.RadioBox(
            main_panel,
            label="Delete files with file types that are (includes files added by shortcuts)",
            choices=["in the list", "not in the list"]
        )
        self.delete_based_on_file_type_radiobox.SetStringSelection(
            self.config.get("delete_files_based_on_file_type_str")
        )

        delete_based_on_file_type_list_button = wx.Button(main_panel, label="List")
        delete_based_on_file_type_list_button.Bind(
            wx.EVT_BUTTON,
            lambda _: self.open_delete_based_on_file_type_list()
        )

        delete_files_with_names_containing_text = wx.StaticText(
            main_panel,
            label="Delete files based on their name containing"
        )

        delete_files_with_names_containing_button = wx.Button(main_panel, label="List")
        delete_files_with_names_containing_button.Bind(
            wx.EVT_BUTTON,
            lambda _: self.open_delete_files_with_names_containing_list()
        )

        self.delete_duplicates_checkbox = wx.CheckBox(main_panel, label="Delete duplicates")
        self.delete_duplicates_checkbox.SetValue(self.config.get("delete_duplicates_bool"))

        self.delete_broken_links_checkbox = wx.CheckBox(main_panel, label="Delete broken links")
        self.delete_broken_links_checkbox.SetValue(self.config.get("delete_broken_links_bool"))

        start_button = wx.Button(main_panel, label="Start")
        start_button.Bind(wx.EVT_BUTTON, lambda _: self.start_scanning())

        self.switch_startup_button = wx.Button(
            main_panel,
            label="Remove from startup" if windows_startup.is_added() else "Add to startup"
        )
        self.switch_startup_button.Bind(wx.EVT_BUTTON, lambda _: self.switch_startup())
        # Hide because the functionality of the button does not work currently
        self.switch_startup_button.Hide()

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
        folder_sizer.AddSpacer(5)
        folder_sizer.Add(self.flatten_folder_exceptions_button, 0, wx.ALL | wx.ALIGN_CENTER)
        folder_sizer.AddSpacer(20)
        folder_sizer.Add(self.delete_empty_folders_checkbox, 0, wx.ALL | wx.ALIGN_CENTER)
        folder_sizer.AddSpacer(20)
        folder_sizer.Add(self.delete_links_to_folders_checkbox, 0, wx.ALL | wx.ALIGN_CENTER)

        file_sizer.Add(self.delete_based_on_file_type_radiobox, 0, wx.ALL | wx.ALIGN_CENTER)
        file_sizer.AddSpacer(5)
        file_sizer.Add(delete_based_on_file_type_list_button, 0, wx.ALL | wx.ALIGN_CENTER)
        file_sizer.AddSpacer(20)
        file_sizer.Add(delete_files_with_names_containing_text, 0, wx.ALL | wx.ALIGN_CENTER)
        file_sizer.AddSpacer(5)
        file_sizer.Add(delete_files_with_names_containing_button, 0, wx.ALL | wx.ALIGN_CENTER)
        file_sizer.AddSpacer(20)
        file_sizer.Add(self.delete_duplicates_checkbox, 0, wx.ALL | wx.ALIGN_CENTER)
        file_sizer.AddSpacer(20)
        file_sizer.Add(self.delete_broken_links_checkbox, 0, wx.ALL | wx.ALIGN_CENTER)

        buttons_sizer.Add(start_button, 0, wx.ALL | wx.ALIGN_CENTER)
        # Hide the switch_startup_button because the functionality currently does not work
        # This is because the program needs admin privileges
        # which can not be given to programs during startup
        #
        # buttons_sizer.AddSpacer(10)
        # buttons_sizer.Add(self.switch_startup_button, 0, wx.ALL | wx.ALIGN_CENTER)

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
                                        file=constants.FLATTEN_FOLDERS_EXCEPTIONS_PATH)
        exceptions_list.ShowModal()

    def open_delete_based_on_file_type_list(self):
        """Open the list that manages the file types based on which files should be deleted."""
        exceptions_list = ExceptionList(self, title="Delete based on file type list",
                                        file=constants.DELETE_FILES_MATCHING_FILE_TYPES_LIST_PATH)
        exceptions_list.ShowModal()

    def open_delete_files_with_names_containing_list(self):
        """Open the list that manages the strings based on which files
         whose names contain them should be deleted.
         """
        target_list = ExceptionList(self, title="Delete based on file name containing",
                                    file=constants.DELETE_FILES_WITH_NAMES_CONTAINING_LIST_PATH)
        target_list.ShowModal()

    def save_config(self):
        """Saves the current configuration."""
        self.config.set("flatten_folders_str",
                        self.flatten_folder_radiobox.GetStringSelection())
        self.config.set("delete_empty_folders_bool",
                        self.delete_empty_folders_checkbox.IsChecked())
        self.config.set("delete_links_to_folders_bool",
                        self.delete_links_to_folders_checkbox.IsChecked())
        self.config.set("delete_duplicates_bool", self.delete_duplicates_checkbox.IsChecked())
        self.config.set("delete_files_based_on_file_type_str",
                        self.delete_based_on_file_type_radiobox.GetStringSelection())
        self.config.set("Delete_broken_links_bool", self.delete_broken_links_checkbox.IsChecked())
        self.config.save()

    def start_scanning(self):
        """Start scanning and hide GUI except for taskbar icon."""
        self.Hide()
        self.task_bar_icon.show()
        self.save_config()
        self.start_menu_helper.start_cleaning()

    def stop_scanning(self):
        """Stop scanning and show GUI."""
        self.task_bar_icon.hide()
        self.Show()
        self.start_menu_helper.stop_cleaning()

    def switch_startup(self):
        """Switches between adding the program to startup and removing it."""
        if windows_startup.is_added():
            windows_startup.remove()
            self.switch_startup_button.Label = "Add to startup"
            self.switch_startup_button.Fit()
        else:
            windows_startup.add()
            self.switch_startup_button.Label = "Remove from startup"
            self.switch_startup_button.Fit()
