#!/usr/bin/env python3
import argparse
import logging
import os

import wx

from library import constants, gui

if __name__ == "__main__":
    if not os.path.exists(constants.CONFIGURATION_PATH):
        os.mkdir(constants.CONFIGURATION_PATH)

    logging.basicConfig(level=logging.INFO,
                        filename=constants.LOG_FILE_PATH,
                        filemode="a",
                        format="%(asctime)s - %(levelname)s - %(message)s")

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-b", "--start-in-background", action="store_true",
                                 help="Start the program in the background with the previous configuration")
    arguments = argument_parser.parse_args()

    app = wx.App()
    main_frame = gui.MainFrame()
    if arguments.start_in_background:
        main_frame.start_scanning()
    else:
        main_frame.Show()
    app.MainLoop()
