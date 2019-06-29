pyinstaller --distpath "." --clean --onefile --specpath "./build" --name "Start Menu Helper" --add-data "../icon.ico;." --noconsole --icon "../icon.ico" --uac-admin "./main.py"
