# ======= imports ======= #
from customtkinter import *
import os
from sqlite3 import connect
from sys import path
from _tkinter import TclError
# ======= ------- ======= #

# ======= constants ======= #
USER = os.getlogin()
DIRECTORY = f"C:\\Users\\{USER}\\AppData\\Local\\"+"the2048game\\"
COLORS = [None, "#eee4da", "#ebd8b6", "#f3b178", "#f69562", "#f88165", "#f76644", "#f0d26c", "#edcc61", "#edc850", "#edc53f", "#edc22e", "#3c3a32"]
TEXT_COLORS = ["#756452", "#ffffff"]
# ======= --------- ======= #

# ======= directory and database creation ======= #
if not os.path.exists(DIRECTORY): os.makedirs(DIRECTORY)

conn = connect(f"{DIRECTORY}\\2048.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Scores (Time TEXT, Name TEXT, Score INTEGER, Block INTEGER)")
# ======= --------- --- -------- -------- ======= #

# ======= window ======= #
class App(CTk):

    def __init__(root):
        # ======= window setup ======= #
        super().__init__(fg_color="#faf8f0")
        root.geometry("600x600+50+50")
        root.minsize(600, 600)
        # ======= ------ ----- ======= #

        # ======= empty title bar ======= #
        try:
            from ctypes import windll, byref, sizeof, c_int
            windll.dwmapi.DwmSetWindowAttribute(windll.user32.GetParent(root.winfo_id()), 35, byref(c_int(0x00f0f8fa)), sizeof(c_int))
            root.title("")
            root.iconbitmap(f"{path[0]}\\empty.ico")
        except ImportError:
            root.title("the2048game")
            root.iconbitmap(f"{path[0]}\\favicon.ico")
        except TclError: pass 
        # ======= ----- ----- --- ======= #

        # ======= globals ======= # 
        global scoreVar, highVar
        scoreVar = IntVar(value=0)
        highVar = IntVar(value=cursor.execute(f'''SELECT MAX(Score) FROM Scores''').fetchone()[0])
        # ======= ------- ======= # 

        # ======= mainloop ======= #
        root.mainloop()
        # ======= -------- ======= #
# ======= ------ ======= #

App()