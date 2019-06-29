import pathlib

STARTUP_PATH = pathlib.Path.home().drive + "\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
EXECUTABLE_PATH = pathlib.Path.cwd().joinpath("Start Menu Helper.exe")
