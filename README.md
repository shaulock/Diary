# Diary
A python based GUI Diary app

# To Run
Open commandline in the directory and do "pip install -r requirements.txt"
Then simply run "python main.py"

# To Build
Open commandline in the directory and do "pip install -r requirements.txt"
Then run "pip install PyInstaller"
Finally run "pyinstaller --distpath ./release --onedir --name Diary --contents-directory Files --noconsole main.py --hidden-import babel.numbers"
The Diary.exe file will be stored in the ./realease/Diary directory, you can run it now