"""Allows using assets that were bundled using pyinstaller."""
import os
import sys


def asset_path(relative_path: str) -> str:
    """Returns the path of an asset file."""
    if hasattr(sys, "_MEIPASS"):
        # pylint: disable=E1101,W0212
        return os.path.join(sys._MEIPASS, relative_path)  # type: ignore
    return os.path.join(os.path.abspath("."), relative_path)
