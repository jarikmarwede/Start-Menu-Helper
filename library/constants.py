"""Constants used in the whole project."""
import pathlib

PROGRAM_NAME = "Start Menu Helper"
VERSION_NUMBER = "1.2.0"
ICON_FILE_NAME = "icon.ico"
TIME_BETWEEN_SCANS_IN_MINUTES = 5
APP_DATA_PATH = pathlib.WindowsPath.home().joinpath("AppData")
DEFAULT_CONFIGURATION_PATH = APP_DATA_PATH.joinpath("Roaming").joinpath(PROGRAM_NAME)
LOG_FILE_PATH = DEFAULT_CONFIGURATION_PATH.joinpath("log.txt")
STARTUP_PATH = pathlib.WindowsPath.home().drive + \
               "\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
EXECUTABLE_PATH = pathlib.WindowsPath.cwd().joinpath(PROGRAM_NAME + ".exe")
START_MENU_PATHS = [
    pathlib.WindowsPath(
        pathlib.WindowsPath.home().drive + "/ProgramData/Microsoft/Windows/Start Menu"
    ),
    APP_DATA_PATH.joinpath("Roaming/Microsoft/Windows/Start Menu")
]
START_MENU_PROGRAMS_PATHS = [
    pathlib.WindowsPath(
        pathlib.WindowsPath.home().drive + "/ProgramData/Microsoft/Windows/Start Menu/Programs"),
    APP_DATA_PATH.joinpath("Roaming/Microsoft/Windows/Start Menu/Programs")
]
PROTECTED_FOLDERS = [
    "StartUp",
    "Startup",
    "Accessibility",
    "Accessories",
    "Administrative Tools",
    "System Tools",
    "Windows PowerShell"
]
