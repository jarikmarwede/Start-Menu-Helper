:: generate an executable that is required for setup generation
call "%~dp0generate_executable.cmd"
:: generate the setup file
call "%~dp0generate_setup.cmd"
:: delete the executable as it is no longer needed
del "%~dp0..\Start Menu Helper.exe"
