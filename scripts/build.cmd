:: Build application into executable that is required for setup generation
call "%~dp0generate_executable.cmd"
:: Generate the setup file
call "%~dp0generate_setup.cmd"
