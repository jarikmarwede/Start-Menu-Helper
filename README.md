# Start Menu Helper
A tool to clean up your Windows Start Menu

## Introduction
This program can help you clean your Start Menu in Windows. You set some options of how your Start Menu should be organized once and it helps you apply these rules.

## How to use
### :exclamation: Warning
This program can delete or destroy your start menu if you configure it the wrong way. So be careful and __do not switch on an option without knowing what it does__. It is advised that you make a backup of the start menu folders before you use this program.

### :floppy_disk: Backup
To backup your Start menu you just have to copy two folders to a save place on your computer.
1. "__Drive letter of the drive you installed windows on__:\Users\\__your username__\AppData\Roaming\Microsoft\Windows\Start Menu"
2. "__Drive letter of the drive you installed windows on__:\ProgramData\Microsoft\Windows\Start Menu"
If something goes wrong with your start menu you can copy your backup into these folders again.

### Cleaning
Once you have configured all of the options you can start the cleaning by pressing the "Start" button. Once you have clicked it the cleaning begins and the program will continually clean the start menu every few minutes. You can reopen the options window by clicking on the icon of the program in the windows taskbar. If you want to close it you can also right-click on it to open a menu where you can select "Close".

### :gear: Options
#### Folders
##### Flatten folders:
This option specifies whether folders within the start menu should be deleted and their files moved to the normal start menu folder. You can specify folders that should not be flattened by clicking on the "Exceptions" button and entering their names.

Options: All, Only ones with one item in them, None
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

### Build executable
To build the program:
1. Install [PyInstaller](https://www.pyinstaller.org/index.html) using `pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz`
2. Run `.\generate_executable.cmd`

### Generate setup
To generate the setup:
1. [Build executable](#build-executable)
2. Install [Inno Setup](http://www.jrsoftware.org/isdl.php) to "C:\Program Files (x86)"
3. Run `.\generate_setup.cmd`

Alternatively if you do not want to install it to "C:\Program Files (x86)":
1. [Build executable](#build-executable)
2. Install [Inno Setup](http://www.jrsoftware.org/isdl.php) anywhere
3. Open "setup_script.iss" in Inno Setup
4. Click "Compile"
