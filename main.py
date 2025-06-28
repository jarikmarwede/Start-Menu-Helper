#!/usr/bin/env python3
"""Start up script for the Start-Menu-Helper program."""
import argparse
import logging
import os
import pathlib

import wx

from library import constants, gui

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "-b",
        "--start-in-background",
        action="store_true",
        help="Start the program in the background with the previous configuration"
    )
    argument_parser.add_argument(
        "-c",
        "--config-directory",
        action="store",
        help="Specify an alternative directory where the configuration files are located "
             f"(Default is \"{constants.DEFAULT_CONFIGURATION_PATH}\")"
    )
    arguments = argument_parser.parse_args()

    configuration_directory = constants.DEFAULT_CONFIGURATION_PATH
    if arguments.config_directory:
        configuration_directory = pathlib.WindowsPath(arguments.config_directory)

    if not os.path.exists(configuration_directory):
        os.mkdir(configuration_directory)

    logging.basicConfig(
        level=logging.INFO,
        filename=configuration_directory.joinpath(constants.LOG_FILE_NAME),
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    app = wx.App()
    main_frame = gui.MainFrame(configuration_directory)
    if arguments.start_in_background:
        main_frame.start_scanning()
    else:
        main_frame.Show()
    app.MainLoop()
