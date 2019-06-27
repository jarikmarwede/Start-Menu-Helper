import pathlib

import pythoncom
import win32com.client


def is_shortcut(file: pathlib.WindowsPath) -> bool:
    return file.name.endswith(".lnk")


def read_shortcut(link: pathlib.WindowsPath) -> pathlib.WindowsPath:
    pythoncom.CoInitialize()
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(link))
    return pathlib.WindowsPath(shortcut.Targetpath)
