from win32 import win32gui
import win32ui, win32con, win32api, win32clipboard
import time, datetime, sqlite3, pyautogui

w = win32gui

conn = sqlite3.connect('activity_log.db')
c = conn.cursor()


class Active:
    def __init__(self, name, url, app, time):
        self.name = name
        self.url = url
        self.app = app
        self.time = time

    def read_active(self):
        self.name = w.GetWindowText(w.GetForegroundWindow())
        # self.url = w.GetWindowText(w.GetForegroundWindow()).split('-')[-2] raczej źle ale zostawiam na wszelki wypadek
        self.app = w.GetWindowText(w.GetForegroundWindow()).split('-')[-1]


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS log(unix REAL, date TEXT, application TEXT, url TEXT, name TEXT,'
              ' timespend REAL)')


def enter_data(app, url, name, timespend):
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%Y %H:%M:%S'))
    c.execute("INSERT INTO log (unix, date, application, url, name, timespend) VALUES(?,?,?,?,?,?)",
              (unix, date, app, url, name, timespend))
    conn.commit()


def copy_url():
    win32clipboard.OpenClipboard()
    clpboard = win32clipboard.GetClipboardData()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    time.sleep(0.25)
    pyautogui.hotkey('ctrl', 'l')
    # pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.25)
    win32clipboard.OpenClipboard()
    time.sleep(0.25)
    data = win32clipboard.GetClipboardData()
    time.sleep(0.25)
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, clpboard)
    win32clipboard.CloseClipboard()
    return data



active_window = Active("", "", "", "")
new_window = Active("", "", "", "")
active_window.time = time.time()

create_table()

while True:

    new_window.read_active()
    new_window.time = time.time()

    if active_window.name != new_window.name:
        time_passed = new_window.time - active_window.time
        enter_data(active_window.app, active_window.url, active_window.name, time_passed)
        if time_passed > 1.5:
            print(time_passed)
        active_window.time = time.time()
        active_window.name = new_window.name
        active_window.app = new_window.app
        active_window.url = new_window.url
        print(active_window.app)
        if active_window.app == ' Google Chrome':
            active_window.url = copy_url()
            print(active_window.url)

    time.sleep(1)

c.close()
conn.close()
