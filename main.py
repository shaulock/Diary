"""Main GUI Generator module for this app"""
import tkinter as tk
from pathlib import Path
from random import randint
from datetime import datetime
from tkcalendar import DateEntry
from tkinter.ttk import Style
from tkfontchooser import askfont
from tkinter.scrolledtext import ScrolledText
from json import loads, dumps
from tklinenums import TkLineNumbers

PATH = f'{str(Path.home())}/.diary'

cache = f'{PATH}/.cache'

class letter:
    def __init__(self, c:str, p:int):
        self.char = c
        self.pos = p
    def __str__(self):
        return f"{self.char} is at {self.pos}"

def increment(lst: list, key: int):
    l = len(lst)
    temp = [i.char for i in lst]
    for i in range(l):
        lst[(i+key)%l].char = temp[i]
    return lst

def decrement(lst: list, key: int):
    l = len(lst)
    temp = [i.char for i in lst]
    for i in range(l):
        lst[i].char = temp[(i+key)%l]
    return lst

def sort(lst: list):
    return sorted(lst, key=lambda x: x.pos)

def generateKey():
    return randint(100000, 999999)

def encrypter(string: str):
    alpha = []
    number = []
    other = []
    alphabets = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
    'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
    ]
    for i in range(len(string)):
        if string[i].upper() in alphabets:
            alpha.append(letter(string[i], i))
        elif string[i] in numbers:
            number.append(letter(string[i], i))
        else:
            other.append(letter(string[i], i))
    key = generateKey()
    key_alpha = int(str(key)[:2])
    key_num = int(str(key)[2:4])
    key_oth = int(str(key)[4:])
    alpha = sort(alpha)
    number = sort(number)
    other = sort(other)
    alpha = increment(alpha, key_alpha)
    number = increment(number, key_num)
    other = increment(other, key_oth)
    alpha = sort(alpha)
    number = sort(number)
    other = sort(other)
    temp = alpha + number + other
    temp = sort(temp)
    if len(str(key_alpha)) == 1:
        key_alpha = f"{0}{key_alpha}"
    else:
        key_alpha = str(key_alpha)
    if len(str(key_num)) == 1:
        key_num = f"{0}{key_num}"
    else:
        key_num = str(key_num)
    if len(str(key_oth)) == 1:
        key_oth = f"{0}{key_oth}"
    else:
        key_oth = str(key_oth)
    new_string = "".join([i.char for i in temp])
    return f"{key_alpha} {key_num} {key_oth} {new_string}"

def decrypter(string: str):
    key = string[:9].split()
    key_alpha = int(key[0])
    key_num = int(key[1])
    key_oth = int(key[2])
    string = string[9:]
    alpha=[]
    number=[]
    other=[]
    alphabets = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
    'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
    ]
    for i in range(len(string)):
        if string[i].upper() in alphabets:
            alpha.append(letter(string[i], i))
        elif string[i] in numbers:
            number.append(letter(string[i], i))
        else:
            other.append(letter(string[i], i))
    alpha = sort(alpha)
    number = sort(number)
    other = sort(other)
    alpha = decrement(alpha, key_alpha)
    number = decrement(number, key_num)
    other = decrement(other, key_oth)
    alpha = sort(alpha)
    number = sort(number)
    other = sort(other)
    temp = alpha + number + other
    temp = sort(temp)
    new_string = "".join([i.char for i in temp])
    return new_string

def change_font():
    global home, editor
    font = askfont(home)
    if font:
        font['family'] = font['family'].replace(' ', '\\ ')
        font_str = f"{font['family']} {font['size']} {font['weight']} {font['slant']}{' underline' if font['underline'] else ''}{' overstrike' if font['overstrike'] else ''}"
        editor.configure(font=font_str)

def save_page():
    """This function will save the contents of the current page"""
    file_name = f"{PATH}/.Page-{current_page.strftime('%Y-%m-%d')}"
    text_to_save = editor.get(1.0, tk.END).strip('\n')+'\n'
    with open(file_name, 'w', encoding='utf8') as file:
        file.write(encrypter(text_to_save))

def on_close():
    save_page()
    settings = {
        'font': editor.cget('font'),
        'wrap': wrap_on.get()
    }
    settings = dumps(settings)
    with open(cache, 'w') as c:
        c.write(settings)
    home.destroy()

def open_page():
    """This function will open the page for a given date
    And return the text from it"""
    global home, current_page
    contents = ''
    try:
        with open(f'{PATH}/.Page-{current_page.strftime('%Y-%m-%d')}', 'r', encoding='utf8') as file:
            contents = file.read()
            try:
                contents = decrypter(contents)
            except ValueError:
                pass
    except FileNotFoundError:
        with open(f'{PATH}/.Page-{current_page.strftime('%Y-%m-%d')}', 'w', encoding='utf8'):
            pass
    finally:
        home.title(f"Diary Page - {current_page.strftime('%A, %d %B, %Y')}")
        editor.delete(1.0, tk.END)
        editor.insert(1.0, contents)

def wrap_text():
    global editor, wrap_on, home
    if wrap_on.get() == 1:
        editor.configure(wrap=tk.WORD)
    else:
        editor.configure(wrap="none")

def main() -> None:
    """The main body of the diary app"""
    global home, editor, calendar, wrap_on, linenumbers, y_scroll
    font = 'Consolas 18'
    wrap = True
    try:
        with open(cache, 'r', encoding='utf8') as c:
            _ = loads(c.read())
            font = _['font']
            wrap = True if _['wrap'] else False
    except FileNotFoundError:
        pass
    except KeyError:
        pass
    home = tk.Tk()
    home.geometry('1000x700')
    home.title(f"Diary Page - {current_page.strftime('%A, %d %B, %Y')}")
    frame = tk.Frame(home, relief=tk.RAISED, bd=2, padx=5, pady=5)
    frame.pack(side=tk.TOP, fill=tk.BOTH)
    label = tk.Label(frame, text='Select the date here', padx=5, pady=5)
    label.grid(row=0, column = 0, sticky="ns")
    font_button = tk.Button(frame, text="Change Font", command=change_font, padx=5, pady=5)
    font_button.grid(row=0, column=3, sticky="ns")
    editor_frame = tk.Frame(home, relief=tk.RIDGE, bd=2)
    editor_frame.pack(fill=tk.BOTH, expand=True)
    wrap_on = tk.IntVar()
    word_wrap = tk.Checkbutton(frame, text="Word Wrap", command=wrap_text, variable=wrap_on, padx=5, pady=5)
    word_wrap.grid(row=0, column=4, sticky="ns")
    calendar = DateEntry(
        master=frame,
        firstweekday="sunday",
        weekenddays=[],
        maxdate=datetime.today(),
        showothermonthdays=True,
        date_pattern='dd / mm / y',
        weekendbackground='white',
        normalbackground='white',
        padx=5,
        pady=5
        )
    calendar.grid(row=0, column=1, sticky="ns")
    calendar.bind('<<DateEntrySelected>>', when_open)
    editor = tk.Text(editor_frame, font=font, undo=True, padx=5, pady=5)
    x_scroll = tk.Scrollbar(editor_frame,orient='horizontal', command=editor.xview, cursor="arrow", width=15)
    x_scroll.pack(side=tk.TOP, fill='x')
    linenumbers = TkLineNumbers(editor_frame, editor, justify='right')
    linenumbers.pack(side=tk.LEFT, fill='y')
    editor.bind('<<Modified>>', on_modified, add=True)
    y_scroll = tk.Scrollbar(editor_frame, orient='vertical', command=editor.yview, cursor="arrow", width=15)
    y_scroll.pack(side=tk.RIGHT, fill='y')
    editor.pack(fill=tk.BOTH, expand=True)
    editor.config(yscrollcommand=on_scroll)
    if wrap:
        editor.configure(wrap=tk.WORD)
        word_wrap.select()
    else:
        editor.configure(wrap="none")
        word_wrap.deselect()
    editor.configure(xscrollcommand=x_scroll.set)
    # home.bind('<Configure>', update_size)
    open_page()
    home.protocol("WM_DELETE_WINDOW", on_close)
    home.mainloop()

def on_scroll(*args):
    y_scroll.set(*args)
    home.after_idle(linenumbers.redraw)

def on_modified(event):
    editor.edit_modified(False) # reset the internal modified flag
    home.after_idle(linenumbers.redraw) # update line numbers

def when_open(_):
    save_page()
    global current_page, calendar
    current_page = calendar.get_date()
    open_page()

if __name__ == "__main__":
    Path(PATH).mkdir(exist_ok=True)
    style: Style
    home: tk.Tk
    editor: tk.Text
    current_page: datetime = datetime.today()
    calender: DateEntry
    wrap_on: tk.IntVar
    linenumbers: TkLineNumbers
    y_scroll: tk.Scrollbar
    main()