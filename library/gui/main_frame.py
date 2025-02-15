"""Main frame of the GUI."""
import pathlib

import wx
import wx.adv

from library import configuration, constants, start_menu_helper
from library.gui.delete_based_on_file_type_list import DeleteFilesMatchingFileTypesExceptionsList
from library.gui.delete_files_with_names_containing_list import DeleteFilesWithNamesContainingList
from library.gui.flatten_folders_containing_only_one_item_exception_list import \
    FlattenFoldersContainingOnlyOneItemExceptionList
from library.gui.flatten_folders_exception_list import FlattenFoldersExceptionList
from library.gui.task_bar_icon import TaskBarIcon
from library.helpers import pyinstaller_asset, windows_startup


class MainFrame(wx.Frame):
    """Main Frame of the GUI."""

    def __init__(self, configuration_directory: pathlib.Path) -> None:
        """Set up Main Frame."""
        super().__init__(parent=None, title=constants.PROGRAM_NAME)
        self.Bind(wx.EVT_CLOSE, lambda _: wx.Exit())

        self.icon = wx.Icon(name=pyinstaller_asset.asset_path(constants.ICON_FILE_NAME),
                            type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)

        self.task_bar_icon = TaskBarIcon(self.stop_scanning)

        self.config = configuration.Configuration(configuration_directory)
        self.start_menu_helper = start_menu_helper.StartMenuHelper(self.config)

        # Widgets
        main_panel = wx.Panel(self)

        self.flatten_folder_radiobox = wx.RadioBox(
            main_panel,
            label="Flatten folders whose names",
            choices=[
                "contain one of the words in the list",
                "do not contain any of the words in the list"
            ]
        )
        if self.config.get("flatten_folders_list_type_str") == "whitelist":
            self.flatten_folder_radiobox.SetStringSelection("contain one of the words in the list")
        else:
            self.flatten_folder_radiobox.SetStringSelection(
                "do not contain any of the words in the list")

        self.flatten_folder_list_button = wx.Button(main_panel, label="List")
        self.flatten_folder_list_button.Bind(
            wx.EVT_BUTTON,
            lambda _: self.open_flatten_folders_list()
        )

        self.flatten_folder_containing_only_one_item_checkbox = wx.CheckBox(
            main_panel,
            label="Flatten folders only containing one item"
        )
        self.flatten_folder_containing_only_one_item_checkbox.Bind(
            wx.EVT_CHECKBOX,
            self.on_flatten_folder_containing_only_one_item_checkbox
        )
        self.flatten_folder_containing_only_one_item_checkbox.SetValue(
            self.config.get("flatten_folders_containing_only_one_item_bool")
        )

        self.flatten_folder_containing_only_one_item_exceptions_button = wx.Button(
            main_panel,
            label="Exceptions"
        )
        self.flatten_folder_containing_only_one_item_exceptions_button.Bind(
            wx.EVT_BUTTON,
            lambda _: self.open_flatten_folders_containing_only_one_item_exception_list()
        )

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
        folder_sizer.Add(self.flatten_folder_list_button, 0, wx.ALL | wx.ALIGN_CENTER)
        folder_sizer.AddSpacer(20)
        folder_sizer.Add(self.flatten_folder_containing_only_one_item_checkbox, 0,
                         wx.ALL | wx.ALIGN_CENTER)
        folder_sizer.AddSpacer(5)
        folder_sizer.Add(self.flatten_folder_containing_only_one_item_exceptions_button, 0,
                         wx.ALL | wx.ALIGN_CENTER)
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

    def on_flatten_folder_containing_only_one_item_checkbox(self, event: wx.CommandEvent) -> None:
        """Enable/disable exceptions button for flatten folder containing only one item setting."""
        if event.IsChecked():
            self.flatten_folder_containing_only_one_item_exceptions_button.Enable()
        else:
            self.flatten_folder_containing_only_one_item_exceptions_button.Disable()

    def open_flatten_folders_list(self) -> None:
        """Open the whitelist or blacklist for the flatten folders option."""
        list_window = FlattenFoldersExceptionList(
            self,
            "Flatten folders list",
            self.config
        )
        list_window.ShowModal()

    def open_flatten_folders_containing_only_one_item_exception_list(self) -> None:
        """Open the exceptions list for the flatten folders containing only one item option."""
        exceptions_list = FlattenFoldersContainingOnlyOneItemExceptionList(
            self,
            "Flatten folders containing only one item exceptions",
            self.config
        )
        exceptions_list.ShowModal()

    def open_delete_based_on_file_type_list(self) -> None:
        """Open the list that manages the file types based on which files should be deleted."""
        exceptions_list = DeleteFilesMatchingFileTypesExceptionsList(
            self,
            "Delete based on file type list",
            self.config
        )
        exceptions_list.ShowModal()

    def open_delete_files_with_names_containing_list(self) -> None:
        """Open the list that manages the strings based on which files
         whose names contain them should be deleted.
         """
        target_list = DeleteFilesWithNamesContainingList(
            self,
            "Delete based on file name containing",
            self.config
        )
        target_list.ShowModal()

    def save_config(self) -> None:
        """Saves the current configuration."""
        if (self.flatten_folder_radiobox.GetStringSelection()
                == "contain one of the words in the list"):
            self.config.set("flatten_folders_list_type_str", "whitelist")
        else:
            self.config.set("flatten_folders_list_type_str", "blacklist")
        self.config.set(
            "flatten_folders_containing_only_one_item_bool",
            self.flatten_folder_containing_only_one_item_checkbox.IsChecked()
        )
        self.config.set("delete_empty_folders_bool",
                        self.delete_empty_folders_checkbox.IsChecked())
        self.config.set("delete_links_to_folders_bool",
                        self.delete_links_to_folders_checkbox.IsChecked())
        self.config.set("delete_duplicates_bool", self.delete_duplicates_checkbox.IsChecked())
        self.config.set("delete_files_based_on_file_type_str",
                        self.delete_based_on_file_type_radiobox.GetStringSelection())
        self.config.set("Delete_broken_links_bool", self.delete_broken_links_checkbox.IsChecked())
        self.config.save()

    def start_scanning(self) -> None:
        """Start scanning and hide GUI except for taskbar icon."""
        self.Hide()
        self.task_bar_icon.show()
        self.save_config()
        self.start_menu_helper.start_cleaning()

    def stop_scanning(self) -> None:
        """Stop scanning and show GUI."""
        self.task_bar_icon.hide()
        self.Show()
        self.start_menu_helper.stop_cleaning()

    def switch_startup(self) -> None:
        """Switches between adding the program to startup and removing it."""
        if windows_startup.is_added():
            windows_startup.remove()
            self.switch_startup_button.Label = "Add to startup"
            self.switch_startup_button.Fit()
        else:
            windows_startup.add()
            self.switch_startup_button.Label = "Remove from startup"
            self.switch_startup_button.Fit()
