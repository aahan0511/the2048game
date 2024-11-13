# ======= imports ======= #
from customtkinter import *
import os
from sqlite3 import connect
from sys import path
from _tkinter import TclError
from PIL import Image, ImageTk
# ======= ------- ======= #

# ======= constants ======= #
USER = os.getlogin()
DIRECTORY = f"C:\\Users\\{USER}\\AppData\\Local\\"+"the2048game\\"
COLORS = [None, "#eee4da", "#ebd8b6", "#f3b178", "#f69562", "#f88165", "#f76644", "#f0d26c", "#edcc61", "#edc850", "#edc53f", "#edc22e", "#3c3a32"]
TEXT_COLORS = ["#756452", "#ffffff"]
PATHS = {
    "empty" : f"{path[0]}\\images\\empty.ico",
    "favicon" : f"{path[0]}\\images\\favicon.ico",
    "icon" : f"{path[0]}\\images\\icon.png"
}
FONT = "JetBrains Mono Medium"
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
        super().__init__("#faf8f0")
        root.geometry("600x600+50+50")
        root.resizable(False, False)
        # ======= ------ ----- ======= #

        # ======= empty title bar ======= #
        try:
            from ctypes import windll, byref, sizeof, c_int
            windll.dwmapi.DwmSetWindowAttribute(
                windll.user32.GetParent(root.winfo_id()), 
                35, 
                byref(c_int(0x00f0f8fa)), 
                sizeof(c_int)
            )
            root.title("")
            root.iconbitmap(PATHS["empty"])
        except ImportError:
            root.title("the2048game")
            root.iconbitmap(PATHS["favicon"])
        except TclError: pass 
        # ======= ----- ----- --- ======= #

        # ======= variables ======= # 
        root.scoreVar = IntVar(master=root, value=0)
        root.highVar = IntVar(master=root, value=cursor.execute(f'''SELECT MAX(Score) FROM Scores''').fetchone()[0])
        # ======= --------- ======= # 

        # ======= gui ======= #
        root.icon = ImageTk.PhotoImage(
            Image.open(PATHS["icon"]).resize((80, 80))
        )

        root.header = Header(root, root.scoreVar, root.highVar, root.icon)
        # ======= --- ======= #

        # ======= mainloop ======= #
        root.mainloop()
        # ======= -------- ======= #
# ======= ------ ======= #

# ======= header ======= #
class Header(CTkFrame):

    def __init__(header, master, scoreVar, highVar, icon):
        # ======= setup ======= #
        super().__init__(
            master,
            fg_color="#bdac97",
            border_color="#9c8978",
            border_width=5,
            corner_radius=35,
            width=555, 
            height=100, 
        )
        # ======= ----- ======= #

        # ======= grid setup ======= #
        header.rowconfigure(0, weight=1, uniform="a")
        header.columnconfigure(0, weight=2, uniform="a")
        header.columnconfigure((1, 2), weight=1, uniform="a")
        header.grid_propagate(False)
        # ======= ---- ----- ======= #

        # ======= gui ======= #
        header.namePlate = NamePlate(header, icon)

        header.curScore = Score(
            header, 
            "#eae7d9", 
            1, 
            "SCORE", 
            scoreVar
        )

        header.highScore = Score(
            header, 
            "#faf8f0", 
            2, 
            "BEST", 
            highVar
        )
        # ======= --- ======= #

        # ======= place ======= #
        header.place(x=300, y=60, anchor="center")
        # ======= ----- ======= #
# ======= ------ ======= #

# ======= name plate box ======= #
class NamePlate(CTkFrame):

    def __init__(nameplate, master, icon):
        # ======= setup ======= #
        super().__init__(master, fg_color="transparent")
        # ======= ----- ======= #

        # ======= gui ======= #
        nameplate.logo = CTkCanvas(
            nameplate,
            bd=0, 
            highlightthickness=0, 
            relief="ridge",
            background="#bdac97",
            width=80, 
            height=80
        )
        nameplate.logo.create_image(40, 40, image=icon, anchor="center")
        nameplate.logo.place(relx=0.2, rely=0.5, anchor="center")

        nameplate.name = CTkLabel(
            nameplate,
            text_color="#756452",
            text="2048",
            font=(FONT, 50)
        )
        nameplate.name.place(relx=0.6, rely=0.5, anchor="center")
        # ======= --- ======= #

        # ======= place ======= #
        nameplate.grid(row=0, column=0, sticky="nsew", padx=10, pady=19)
        # ======= ----- ======= #

# ======= ---- ----- --- ======= #

# ======= score box ======= #
class Score(CTkFrame):

    def __init__(score, master, color, pos, description, var):
        # ======= setup ======= #
        super().__init__(
            master,
            corner_radius=25,
            fg_color=color,
            border_color="#eae7d9",
            border_width=3,
        )
        # ======= ----- ======= #

        # ======= gui ======= #
        score.label = CTkLabel(score, text=description, font=(FONT, 10), text_color="#988a86")
        score.label.place(relx=0.5, rely=0, anchor="n")

        score.number = CTkLabel(score, textvariable=var, text_color="#988a86", font=(FONT, 20))
        score.number.place(relx=0.5, rely=0.6, anchor="center")
        # ======= --- ======= #

        # ======= place ======= #
        score.grid(row=0, column=pos, sticky="nsew", padx=15, pady=19)
        # ======= ----- ======= #
# ======= ----- --- ======= #

# ======= main code ======= #
if __name__ == "__main__":
    App()
# ======= ---- ---- ======= #