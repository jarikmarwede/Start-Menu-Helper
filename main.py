#!/usr/bin/env python3
import argparse

import wx

import gui

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-b", "--start-in-background", action="store_true",
                                 help="Start the program in the background with the previous configuration")
    arguments = argument_parser.parse_args()

    app = wx.App()
    main_frame = gui.MainFrame()
    if arguments.start_in_background:
        main_frame.start_scanning()
    else:
        main_frame.stop_scanning()
    app.MainLoop()
