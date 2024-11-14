# ======= imports ======= #
from customtkinter import *
from os import path as osPath, makedirs, getlogin
from sqlite3 import connect
from sys import path
from _tkinter import TclError
from PIL import Image, ImageTk
from random import randint, choice
from ttkbootstrap.toast import ToastNotification
# ======= ------- ======= #

# ======= constants ======= #
USER = getlogin()
DIRECTORY = f"C:\\Users\\{USER}\\AppData\\Local\\"+"the2048game\\"
COLORS = [None, "#eee4da", "#ebd8b6", "#f3b178", "#f69562", "#f88165", "#f76644", "#f0d26c", "#edcc61", "#edc850", "#edc53f", "#edc22e", "#3c3a32"]
PATHS = {
    "empty" : f"{path[0]}\\images\\empty.ico",
    "favicon" : f"{path[0]}\\images\\favicon.ico",
    "icon" : f"{path[0]}\\images\\icon.png"
}
FONT = "JetBrains Mono Medium"
SPEED = 5
# ======= --------- ======= #

# ======= variables ======= #
grid = [None]*16
matrix = [0]*16
ongoing = False
# ======= --------- ======= #

# ======= directory and database creation ======= #
if not osPath.exists(DIRECTORY): makedirs(DIRECTORY)

conn = connect(f"{DIRECTORY}\\2048.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Scores (Time TEXT, Score INTEGER, Block INTEGER)")
# ======= --------- --- -------- -------- ======= #

# ======= window ======= #
class App(CTk):

    # ======= init ======= #
    def __init__(root):
        # ======= window setup ======= #
        super().__init__("#faf8f0")
        root.geometry("726x700+50+50")
        root.resizable(False, False)

        root.bind("<Any-KeyPress>", root.keyPress)
        root.bind("<space>", root.start)
        root.bind("<Escape>", root.restart)
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
        icon = ImageTk.PhotoImage(Image.open(PATHS["icon"]).resize((80, 80)))

        root.winToast  = ToastNotification(
            "You Won!!!", 
            "You got 2048.", 
            2000, 
            "success", 
            False, 
            "🥳", 
            "JetBrains Mono Medium", 
            position=(50, 50, "se")
        )
        root.lossToast  = ToastNotification(
            "You Lost...", 
            "You have no possible moves left..", 
            2000, 
            "danger", 
            False, 
            "😔", 
            "JetBrains Mono Medium", 
            position=(50, 50, "se")
        )
        # ======= --------- ======= # 

        # ======= gui ======= #
        root.header = Header(root, root.scoreVar, root.highVar, icon)
        root.side = Side(root)
        root.game = GameScreen(root)
        # ======= --- ======= #

        # ======= mainloop ======= #
        root.mainloop()
        # ======= -------- ======= #
    # ======= ---- ======= #

    # ======= key press ======= #
    def keyPress(root, event):
        global movement
        movement = False
        key = event.keysym
        if key == "Left" or key == "a":
            for cell in grid:
                if cell != None:
                    cell.merge("left")
        if key == "Right" or key == "d":
            for cell in grid[::-1]:
                if cell != None:
                    cell.merge("right")
        if key == "Up" or key == "w":
            tempGrid = grid[::4]+grid[1::4]+grid[2::4]+grid[3::4]
            for cell in tempGrid:
                if cell != None:
                    cell.merge("up")
        if key == "Down" or key == "s":
            tempGrid = grid[::4][::-1]+grid[1::4][::-1]+grid[2::4][::-1]+grid[3::4][::-1]
            for cell in tempGrid:
                if cell != None:
                    cell.merge("down")
        if movement:
            Block(root.game).place()
        if matrix.count(0) == 0:
            matching = False
            for cell in grid:
                if cell.pos%4 != 0:
                    if grid[cell.pos-1].power == cell.power:
                        matching = True
                if cell.pos%4 != 3:
                    if grid[cell.pos+1].power == cell.power:
                        matching = True
                if cell.pos//4 != 0:
                    if grid[cell.pos-4].power == cell.power:
                        matching = True
                if cell.pos//4 != 3:
                    if grid[cell.pos+4].power == cell.power:
                        matching = True
            if not matching:
                root.lossToast.show_toast()
                root.restart()
        elif matrix.count(11) == 1:
            root.winToast.show_toast()
    # ======= --- ----- ======= #

    # ======= restart ======= #
    def restart(root, _=None):
        global ongoing
        if ongoing:
            ongoing = False
            cursor.execute(f"INSERT INTO Scores VALUES (DATETIME('now'), {root.scoreVar.get()}, {2**max(matrix)})") 
            conn.commit()
            for cell in grid: 
                if cell: 
                    cell.destroy()
            root.highVar.set(cursor.execute(f'''SELECT MAX(Score) FROM Scores''').fetchone()[0])
            root.scoreVar.set(0)
    # ======= ------- ======= #
    
    # ======= start ======= #
    def start(root, _=None):
        global ongoing
        if not ongoing:
            Block(root.game).place()
            Block(root.game).place()
            ongoing = True
    # ======= ----- ======= #
# ======= ------ ======= #

# ======= header ======= #
class Header(CTkFrame):

    # ======= init ======= #
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
        header.place(x=426, y=60, anchor="center")
        # ======= ----- ======= #
    # ======= ---- ======= #
# ======= ------ ======= #

# ======= name plate box ======= #
class NamePlate(CTkFrame):

    # ======= init ======= #
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
            font=(FONT, 50, "bold")
        )
        nameplate.name.place(relx=0.6, rely=0.5, anchor="center")
        # ======= --- ======= #

        # ======= place ======= #
        nameplate.grid(row=0, column=0, sticky="nsew", padx=10, pady=19)
        # ======= ----- ======= #
    # ======= ---- ======= #
# ======= ---- ----- --- ======= #

# ======= score box ======= #
class Score(CTkFrame):

    # ======= init ======= #
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
        score.label = CTkLabel(score, text=description, font=(FONT, 13), text_color="#988a86")
        score.label.place(relx=0.5, rely=0, anchor="n")

        score.number = CTkLabel(score, textvariable=var, text_color="#988a86", font=(FONT, 20))
        score.number.place(relx=0.5, rely=0.6, anchor="center")
        # ======= --- ======= #

        # ======= place ======= #
        score.grid(row=0, column=pos, sticky="nsew", padx=15, pady=19)
        # ======= ----- ======= #
    # ======= ---- ======= #
# ======= ----- --- ======= #

# ======= side box ======= #
class Side(CTkFrame):

    # ======= init ======= #
    def __init__(side, master):
        # ======= setup ======= #
        super().__init__(
            master,
            fg_color="#bdac97",
            border_color="#9c8978",
            border_width=5,
            corner_radius=35,
            width=100, 
            height=667, 
        )
        # ======= ----- ======= #

        # ======= grid setup ======= #
        side.columnconfigure(0, weight=1, uniform="a")
        side.rowconfigure((0, 1), weight=1, uniform="a")
        side.grid_propagate(False)
        # ======= ---- ----- ======= #

        # ======= gui ======= #
        side.play = CTkButton(
            side, 
            text="P\nL\nA\nY", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=(FONT, 28),
            command=master.start
        )
        side.play.grid(column=0, row=0, sticky="nsew", padx=19, pady=19)
        
        side.end = CTkButton(
            side, 
            text="E\nN\nD", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=(FONT, 28),
            command=master.restart
        )
        side.end.grid(column=0, row=1, sticky="nsew", padx=19, pady=19)
        # ======= --- ======= #

        # ======= place ======= #
        side.place(x=72.5, y=344, anchor="center")
        # ======= ----- ======= #
    # ======= ---- ======= #
# ======= ---- --- ======= #

# ======= game screen ======= #
class GameScreen(CTkFrame):

    # ======= init ======= #
    def __init__(screen, master):
        # ======= setup ======= #
        super().__init__(
            master,
            fg_color="#9b8878",
            corner_radius=35,
            width=555, 
            height=555, 
        )
        # ======= ----- ======= #

        # ======= grid setup ======= #
        screen.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")
        screen.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        screen.grid_propagate(False)
        # ======= ---- ----- ======= #

        # ======= variables ======= #
        screen.parent = master
        # ======= --------- ======= #

        # ======= base design ======= #
        for row in range(4):
            for column in range(4):
                CTkLabel(
                    screen, 
                    text="",
                    fg_color="#bdac97",
                    corner_radius=35,
                    width=116.25,
                    height=116.25
                ).place(
                    anchor="center", 
                    x=136.25*column+73.125,
                    y=136.25*row+73.125
                )
        # ======= ---- ------ ======= #

        # ======= place ======= #
        screen.place(x=426, y=400, anchor="center")
        # ======= ----- ======= #
    # ======= ---- ======= #
# ======= ---- ------ ======= #

# ======= block ======= #
class Block:

    # ======= init ======= #
    def __init__(block, master):
        # ======= place check ======= #
        if matrix.count(0) == 0:
            del block
            return
        # ======= ----- ----- ======= #

        # ======= setup ======= #
        block.power = choice([1]*9+[2])
        block.var = IntVar(value=2**block.power)
        block.cell = CTkLabel(
            master, 
            textvariable=block.var, 
            fg_color=COLORS[block.power] if block.power <= 11 else COLORS[-1], 
            text_color="#ffffff" if block.power > 2 else "#756452", 
            justify="center", 
            anchor="center",
            font=(FONT, 28),
            width=116.25,
            height=116.25,
            corner_radius=35
        )
        block.master = master
        # ======= ----- ======= #

        # ======= position chooser ======= #
        block.pos = randint(0, 15)
        while matrix[block.pos] != 0: block.pos = randint(0, 15)
        block.x = (block.pos%4)*136.25+73.125
        block.y = (block.pos//4)*136.25+73.125
        # ======= -------- ------- ======= #
    # ======= ---- ======= #

    # ======= place ======= #
    def place(block):
        block.cell.place(
            x=block.x, 
            y=block.y,
            anchor="center"
        )
        matrix[block.pos] = block.power
        grid[block.pos] = block
    # ======= ----- ======= #

    # ======= destroy ======= #
    def destroy(block):
        block.cell.destroy()
        grid[block.pos] = None
        matrix[block.pos] = 0
        del block
    # ======= ------- ======= #

    # ======= set ======= #
    def set(block):
        block.var.set(2**block.power)
        block.cell.configure(fg_color=COLORS[block.power])
        block.cell.configure(text_color="#ffffff" if block.power > 2 else "#756452")
        grid[block.pos] = block
        matrix[block.pos] = block.power
    # ======= --- ======= #

    # ======= slide ======= #
    def slide(block, direction):
        if direction == "left" and block.pos%4 != 0:
            final = block.x - 136.25 
            def left():
                block.x -= 136.25/SPEED
                block.place()
                if block.x != final:
                    left()
            left()
        elif direction == "right" and block.pos%4 != 3:
            final = block.x + 136.25 
            def right():
                block.x += 136.25/SPEED
                block.place()
                if block.x != final:
                    right()
            right()
        elif direction == "up" and block.pos//4 != 0:
            final = block.y + 136.25 
            def up():
                block.y += 136.25/SPEED
                block.place()
                if block.y != final:
                    up()
            up()
        elif direction == "down" and block.pos//4 != 3:
            final = block.y + 136.25 
            def down():
                block.y += 136.25/SPEED
                block.place()
                if block.y != final:
                    down()
            down()
    # ======= ----- ======= #

    # ======= merge ======= #           
    def merge(self):
        pass #TODO: add merge function
    # ======= ----- ======= #
# ======= ----- ======= #

# ======= main code ======= #
if __name__ == "__main__":
    app = App()
    conn.close()
# ======= ---- ---- ======= #