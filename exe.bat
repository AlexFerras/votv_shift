python write_version_file.py
pyinstaller votv_shift.py --noconsole -y --version-file version_file.txt
robocopy mingit dist/votv_shift/mingit /s /e
robocopy CS dist/votv_shift/CS
robocopy git_fuckery dist/votv_shift/git_fuckery
copy version.txt dist\votv_shift\version.txt /y
copy secrets.json dist\votv_shift\secrets.json /y
copy forceupdate.bat dist\votv_shift\forceupdate.bat /y
pyinstaller updater.py --onefile -y
copy dist\updater.exe dist\votv_shift /y
set /p Version=<version.txt
python -m zipfile -c votv_shift.zip dist/votv_shift