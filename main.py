#!/usr/bin/env python3
import argparse
import logging
import os
import pathlib

import wx

from library import constants, gui

if __name__ == "__main__":
    if not os.path.exists(constants.DEFAULT_CONFIGURATION_PATH):
        os.mkdir(constants.DEFAULT_CONFIGURATION_PATH)

    logging.basicConfig(level=logging.INFO,
                        filename=constants.LOG_FILE_PATH,
                        filemode="a",
                        format="%(asctime)s - %(levelname)s - %(message)s")

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-b", "--start-in-background", action="store_true",
                                 help="Start the program in the background with the previous configuration")
    argument_parser.add_argument("-c",
                                 "--config-directory",
                                 action="store",
                                 help=f"Specify an alternative directory where the configuration files are located (Default is \"{constants.DEFAULT_CONFIGURATION_PATH}\")")
    arguments = argument_parser.parse_args()

    app = wx.App()
    configuration_directory = constants.DEFAULT_CONFIGURATION_PATH
    if arguments.config_directory:
        configuration_directory = arguments.config_directory
    main_frame = gui.MainFrame(pathlib.Path(configuration_directory))
    if arguments.start_in_background:
        main_frame.start_scanning()
    else:
        main_frame.Show()
    app.MainLoop()
