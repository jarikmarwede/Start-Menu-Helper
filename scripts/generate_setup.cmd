:: Clean the output directory before building to it
::rmdir "%~dp0..\setup" /s /q
:: Build the setup wizard using Inno Setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "%~dp0\..\setup.iss"
