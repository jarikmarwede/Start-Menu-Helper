:: Run pyinstaller to produce an executable
pyinstaller --distpath "%~dp0.." --clean --onefile --specpath "%~dp0..\build" --name "Start Menu Helper" --add-data "../icon.ico;." --noconsole --icon "../icon.ico" --uac-admin "%~dp0..\main.py"
:: Remove folders containing build information created by pyinstaller
rmdir build /s /q
rmdir "%~dp0..\build" /s /q
