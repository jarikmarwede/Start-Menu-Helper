import pathlib
import threading

import configuration


class StartMenuHelper:

    def __init__(self):
        self.start_menu_paths = [
            pathlib.WindowsPath(
                pathlib.Path.home().drive + "/ProgramData/Microsoft/Windows/Start Menu"),
            pathlib.Path.home().joinpath("/AppData/Roaming/Microsoft/Windows/Start Menu")
        ]
        self.start_menu_programs_path = [
            pathlib.WindowsPath(
                pathlib.Path.home().drive + "/ProgramData/Microsoft/Windows/Start Menu/Programs"),
            pathlib.Path.home().joinpath("/AppData/Roaming/Microsoft/Windows/Start Menu/Programs")
        ]

        self._config = configuration.Configuration()
        self._cleaner_thread = StoppableThread()

    def start_cleaning(self):
        """Starts the cleaning based on the configuration."""
        self._cleaner_thread = StoppableThread(target=self._clean, daemon=True)
        self._cleaner_thread.start()

    def stop_cleaning(self):
        """Stops the cleaning."""
        self._cleaner_thread.stop()
        self._cleaner_thread.join()

    def _clean(self):
        """Cleans based on configuration.

        This method is supposed to be run by the _cleaner_thread.
        """
        self._config.reload()
        while not self._cleaner_thread.stopped():
            self.move_files_to_programs_directory()
            if self._config.get("delete_duplicates_bool"):
                self.delete_duplicates()
            if self._config.get("flatten_folders_str") == "All":
                self.flatten_all_folders()
            elif self._config.get("flatten_folders_str") == "Only ones with one item in them":
                self.flatten_folders_containing_one_file()
            if self._config.get("delete_empty_folders_bool"):
                self.delete_empty_folders()
            # TODO: Add delete_broken_links
            if self._config.get("delete_files_based_on_file_type_str") == "in the list":
                self.delete_files_matching_file_types()
            else:
                self.delete_files_not_matching_file_types()

    def move_files_to_programs_directory(self):
        """Move all files to the programs directory."""
        for path in self.start_menu_paths:
            for item in path.iterdir():
                item.replace(path.joinpath("Programs"))

    def delete_duplicates(self):
        """Delete duplicates of files."""
        found_files = []
        for path in self.start_menu_programs_path:
            files = [item for item in path.iterdir() if item.is_file()]
            for file in files:
                if file.name in found_files:
                    file.unlink()
                else:
                    found_files.append(file.name)

    def flatten_folders_containing_one_file(self):
        """Flatten folders that are only containing one file."""
        whitelist = []
        if pathlib.WindowsPath("flatten_folders_exceptions.txt").exists():
            with open("flatten_folders_exceptions.txt") as file:
                whitelist = file.read().splitlines()

        for path in self.start_menu_programs_path:
            directories = [item for item in path.iterdir() if item.is_dir()]
            for directory in directories:
                if len(list(directory.iterdir())) <= 1 and directory.name not in whitelist:
                    for item in directory.iterdir():
                        item.replace(path.joinpath(item.name))

    def flatten_all_folders(self):
        """Flatten all folders."""
        whitelist = []
        if pathlib.WindowsPath("flatten_folders_exceptions.txt").exists():
            with open("flatten_folders_exceptions.txt") as file:
                whitelist = file.read().splitlines()

        for path in self.start_menu_programs_path:
            directories = [item for item in path.iterdir() if item.is_dir()]
            for directory in directories:
                if directory.name not in whitelist:
                    for item in directory.iterdir():
                        item.replace(path.joinpath(item.name))

    def delete_empty_folders(self):
        """Delete empty folders."""
        for path in self.start_menu_programs_path:
            directories = [item for item in path.iterdir() if item.is_dir()]
            for directory in directories:
                if len(list(directory.iterdir())) == 0:
                    directory.rmdir()

    def delete_broken_links(self):
        """Delete links that point to a non existing file."""
        for path in self.start_menu_programs_path:
            links = [item for item in path.iterdir() if item.is_symlink()]
            for link in links:
                if not link.exists():
                    link.unlink()

    def delete_files_matching_file_types(self):
        """Delete files that match the file types."""
        file_types = []
        if pathlib.WindowsPath("delete_based_on_file_type_list.txt").exists():
            with open("delete_based_on_file_type_list.txt") as file:
                file_types = file.read().splitlines()

        for path in self.start_menu_programs_path:
            files = [item for item in path.iterdir() if item.is_file()]
            for file_type in file_types:
                for file in files:
                    if file.name.endswith(file_type) and file.is_file():
                        file.unlink()

    def delete_files_not_matching_file_types(self):
        """Delete files that do not match the file types."""
        file_types = []
        if pathlib.WindowsPath("delete_based_on_file_type_list.txt").exists():
            with open("delete_based_on_file_type_list.txt") as file:
                file_types = file.read().splitlines()

        for path in self.start_menu_programs_path:
            files = [item for item in path.iterdir() if item.is_file()]
            for file_type in file_types:
                for file in files:
                    if not file.name.endswith(file_type) and file.is_file():
                        file.unlink()


class StoppableThread(threading.Thread):
    """Thread class with a stop() method.

    The thread itself has to check regularly for the stopped() condition.

    Copied from: https://stackoverflow.com/a/325528
    """

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        """Signals to the thread that it should stop."""
        self._stop_event.set()

    def stopped(self) -> bool:
        """Return whether the thread is supposed to be stopped."""
        return self._stop_event.is_set()
