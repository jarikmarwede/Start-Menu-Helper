:: Clean build directory before building into it
rmdir "%~dp0..\build" /s /q
:: Clean dist directory before building into it
rmdir "%~dp0..\dist" /s /q

:: Run PyInstaller to produce an executable
pyinstaller ^
    --distpath "%~dp0..\dist" ^
    --clean ^
    --onedir ^
    --specpath "%~dp0..\build" ^
    --name "Start Menu Helper" ^
    --add-data "../icon.ico;." ^
    --noconsole ^
    --icon "../icon.ico" ^
    --uac-admin ^
    "%~dp0..\main.py"
