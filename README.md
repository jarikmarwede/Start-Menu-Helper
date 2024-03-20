# Start Menu Helper
A tool to clean up your Windows Start Menu

## Table of contents
* [Introduction](#introduction)
* [Installation](#installation)
* [How to use](#how-to-use)
  * [Warning](#exclamation-warning)
  * [Backup](#floppy_disk-backup)
  * [Cleaning](#cleaning)
  * [Run on startup](#run-on-startup)
  * [Options](#gear-options)
* [Development](#wrench-development)
  * [Setup](#setup)
  * [Generate executable](#generate-executable)
  * [Generate setup](#generate-setup)

## Introduction
This program can help you clean your Start Menu in Windows. You set some options of how your Start Menu should be organized once and it helps you apply these rules.

## Installation
To install the program download the setup for the [latest version](https://github.com/jarikmarwede/Start-Menu-Helper/releases/latest) and run the setup after it is finished downloading.

## How to use
### :exclamation: Warning
This program can delete or destroy your start menu if you configure it the wrong way. So be careful and __do not switch on an option without knowing what it does__. It is advised that you make a [backup](#floppy_disk-backup) of the start menu folders before you use this program.

### :floppy_disk: Backup
To backup your Start menu you just have to copy two folders to a save place on your computer.
1. "__Drive letter of the drive you installed windows on__:\Users\\__your username__\AppData\Roaming\Microsoft\Windows\Start Menu"
2. "__Drive letter of the drive you installed windows on__:\ProgramData\Microsoft\Windows\Start Menu"

If something goes wrong with your start menu you can copy your backup into these folders again.

### Cleaning
Once you have configured all of the [options](#gear-options) you can start the cleaning by pressing the "Start" button. Once you have clicked it the cleaning begins and the program will continually clean the start menu every few minutes. You can reopen the options window by clicking on the icon of the program in the windows taskbar. If you want to close it you can also right-click on it to open a menu where you can select "Close".

### Run on startup
If you want the program to automatically start cleaning in the background when you start your computer follow these steps:
1. Open the "Task Scheduler" program by Microsoft
2. Click on "Action" in the top menu
3. Click on "Create task"
4. Give the task a name, for example "Start Menu Cleaning"
5. Click the "Run with highest privileges" checkbox
6. In the "Triggers" section click on "New..."
7. Select "At log on" in the "Begin the task" dropdown" and click "Ok"
8. In the "Actions" section click on "New..."
9. Click on "Browse" and select the "Start Menu Helper.exe" executable (you specified where it should be installed during the setup, probably in one of the "Program Files" folders)
10. Write "--start-in-background" in the "Add arguments" field and click Ok
11. Finally click on "Ok"

### :gear: Options
#### Folders
##### Flatten folders whose names:
This option specifies whether folders within the start menu should be deleted and their files moved to the normal start menu folder if they match a word in the list or if they don't match any of the words in the list. You can edit the list by clicking on the "List" button. If you don't want to flatten any folders set the option to "contain one of the words in the list" and leave the list empty.

Options: contain one of the words in the list, do not contain any of the words in the list
##### Flatten folders only containing one item
This option specifies whether folders with only one item in them should be flattened. You can specify folders that should not be flattened even if they only contain one item by clicking on the "Exception" button.

Options: On, Off
##### Delete empty folders:
This option specifies whether to delete folders that do not contain any files or other folders.

Options: On, Off
##### Delete links to folders:
This option specifies whether to delete windows shortcuts that point to a folder.

Options: On, Off

#### Files
##### Delete files with file types that are
This option specifies whether to delete all files that have one of the file types in the List or delete all files that __do not__. This also includes the files linked to by windows shortcuts, but instead of the actual files only the shortcut is deleted. If you do not want to delete any files based on their file types, do not put any in the list.

Options: in the list, not in the list
##### Delete files based on their name containing
This list specifies words or combinations of words based on which files that contain them in their name should be deleted.

##### Delete duplicates
This option specifies whether to delete files that have the same name in multiple different folders until there is only one file left.

Options: On, Off
##### Delete broken links
This option specifies whether to delete windows shortcuts that point to a file or a folder that does not exist.

Options: On, Off

## :wrench: Development
### Setup
To set the program up for development on your computer:
1. Clone this program to your computer using `git clone https://github.com/jarikmarwede/Start-Menu-Helper.git`
2. Set up a virtual environment or make sure you have [Python](https://www.python.org/downloads/windows/) version 3.7.3+ installed
3. Install the required libraries using `pip install -r requirements.txt`

### Generate executable
To just generate the executable for the program:
1. Install [PyInstaller](https://www.pyinstaller.org) using `pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz`
2. Run `.\scripts\generate_executable.cmd`

### Generate setup
To generate the setup:
1. Install [Inno Setup](http://www.jrsoftware.org/isdl.php) to "C:\Program Files (x86)"
2. Run `.\scripts\build.cmd`

Alternatively if you do not want to install it to "C:\Program Files (x86)":
1. Install [Inno Setup](http://www.jrsoftware.org/isdl.php) anywhere
2. Open ".\scripts\setup_script.iss" in Inno Setup
3. Click "Compile"
