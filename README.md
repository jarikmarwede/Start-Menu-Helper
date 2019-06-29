# Start Menu Helper
A tool to clean up your Windows Start Menu

## Introduction
This program can help you clean your Start Menu in Windows. You set some options of how your Start Menu should be organized once and it helps you apply these rules.

## Development
### Setup
To set the program up for development on your computer:
1. Clone this program to your computer using `git clone https://github.com/jarikmarwede/Start-Menu-Helper.git`
2. Set up a virtual environment or make sure you have [Python](https://www.python.org/downloads/windows/) version 3.7.3+ installed
3. Install the required libraries using `pip install -r requirements.txt`

### Build executable
To build the program run `.\generate_executable.cmd`

### Generate setup
To generate the setup:
1. Install [Inno Setup](http://www.jrsoftware.org/isdl.php) to "C:\Program Files (x86)"
2. Run `.\generate_setup.cmd`

Alternatively if you do not want to install it to "C:\Program Files (x86)":
1. Install [Inno Setup](http://www.jrsoftware.org/isdl.php) anywhere
2. Open "setup_script.iss" in Inno Setup
3. Click "Compile"
