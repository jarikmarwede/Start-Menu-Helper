import pathlib

PROGRAM_NAME = "Start Menu Helper"
VERSION_NUMBER = "1.0.2"
ICON_FILE_NAME = "icon.ico"
APP_DATA_PATH = pathlib.Path.home().joinpath("AppData")
CONFIGURATION_PATH = APP_DATA_PATH.joinpath("Roaming").joinpath(PROGRAM_NAME)
CONFIGURATION_FILE_PATH = CONFIGURATION_PATH.joinpath("config.ini")
STARTUP_PATH = pathlib.Path.home().drive + "\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
EXECUTABLE_PATH = pathlib.Path.cwd().joinpath(PROGRAM_NAME + ".exe")
START_MENU_PATHS = [
    pathlib.WindowsPath(pathlib.Path.home().drive + "/ProgramData/Microsoft/Windows/Start Menu"),
    APP_DATA_PATH.joinpath("Roaming/Microsoft/Windows/Start Menu")
]
START_MENU_PROGRAMS_PATHS = [
    pathlib.WindowsPath(
        pathlib.Path.home().drive + "/ProgramData/Microsoft/Windows/Start Menu/Programs"),
    APP_DATA_PATH.joinpath("Roaming/Microsoft/Windows/Start Menu/Programs")
]
PROTECTED_FOLDERS = [
    "Startup",
    "Administrative Tools"
]
FLATTEN_FOLDERS_EXCEPTIONS_PATH = CONFIGURATION_PATH.joinpath("flatten_folders_exceptions.txt")
DELETE_FILES_WITH_NAMES_CONTAINING_LIST_PATH = CONFIGURATION_PATH.joinpath(
    "delete_files_with_names_containing.txt")
DELETE_FILES_MATCHING_FILE_TYPES_LIST_PATH = CONFIGURATION_PATH.joinpath(
    "delete_based_on_file_type_list.txt")
