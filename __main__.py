from customtkinter import *
from os import path as path, makedirs, getlogin, system
from sqlite3 import connect
from tkinter import Event
from CTkTable import CTkTable
from PIL import Image, ImageTk
from random import randint, choice
from webbrowser import open as openWeb
from datetime import datetime
from ctypes import windll, byref, sizeof, c_int
from pywinstyles import *
from pyglet import options, font

USER = getlogin()
DIRECTORY = f"C:\\Users\\{USER}\\AppData\\Local\\the2048game"
COLORS = [None, "#eee4da", "#ebd8b6", "#f3b178", "#f69562", "#f88165", "#f76644", "#f0d26c", "#edcc61", "#edc850", "#edc53f", "#edc22e", "#393931"]
PATHS = {
    "empty" : f"{DIRECTORY}\\assets\\images\\empty.ico",
    "icon" : f"{DIRECTORY}\\assets\\images\\icon.png",
    "JetBrainsMono-Medium.ttf" : DIRECTORY+"\\assets\\fonts\\JetBrainsMono-Medium.ttf",
    "JetBrainsMono-Bold.ttf" : DIRECTORY+"\\assets\\fonts\\JetBrainsMono-Bold.ttf",
    "how to play.png" : DIRECTORY+"\\assets\\images\\how to play.png",
    "info.png" : DIRECTORY+"\\assets\\images\\info.png",
    "license.png" : DIRECTORY+"\\assets\\images\\license.png"
}
SPEED = 5
GROW_SPEED = 3.6
TABLE_LEN = 20

SCREEN_FACTOR = 1 # Recommended 0.75 to 1

grid = [None]*16
matrix = [0]*16
ongoing = False
showingWin = False
showingLoss = False
pause = False

if not path.exists(DIRECTORY): 
    makedirs(DIRECTORY)

conn = connect(f"{DIRECTORY}\\scores.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Scores (Time TEXT, Score INTEGER, Block INTEGER, NAME TEXT)")

options['win32_gdi_font'] = True
font.add_file(PATHS["JetBrainsMono-Medium.ttf"])
font.add_file(PATHS["JetBrainsMono-Bold.ttf"])

class App(CTk):

    def __init__(root) -> None:
        super().__init__("#faf8f0")
        root.geometry(f"{int(715*SCREEN_FACTOR)}x{int(700*SCREEN_FACTOR)}+{int(50*SCREEN_FACTOR)}+{int(50*SCREEN_FACTOR)}")
        root.resizable(False, False)

        root.bind("<Any-KeyPress>", root.keyPress)
        root.bind("<space>", root.play)
        root.bind("<Escape>", root.end)

        windll.dwmapi.DwmSetWindowAttribute(
            windll.user32.GetParent(root.winfo_id()), 
            35, 
            byref(c_int(0x00f0f8fa)), 
            sizeof(c_int)
        )
        root.title("")
        root.iconbitmap(PATHS["empty"])

        root.prevMatrix = None
        root.prevScore = None

        root.scoreVar = IntVar(value=0)
        root.highVar = IntVar(value=cursor.execute(f'''SELECT MAX(Score) FROM Scores''').fetchone()[0])
        icon = ImageTk.PhotoImage(Image.open(PATHS["icon"]).resize((int(80*SCREEN_FACTOR), int(80*SCREEN_FACTOR))))

        root.more = More(master=root)
        root.header = Header(
            master=root, 
            scoreVar=root.scoreVar,
            highVar=root.highVar,
            icon=icon
        )
        root.game = GameScreen(master=root)
        root.side = Side(master=root, more=root.more)

        root.mainloop()

    def keyPress(root, event: Event) -> None:
        global movement
        movement = False
        key = event.keysym

        prevMatrix = matrix.copy()
        prevScore = root.scoreVar.get()

        if showingWin or showingLoss: return

        for cell in grid:
            if cell != None:
                cell.mix = True

        if key == "Left" or key == "a" or key == "A":
            for cell in grid:
                if cell != None:
                    cell.merge(direction="left")
        if key == "Right" or key == "d" or key == "D":
            for cell in grid[::-1]:
                if cell != None:
                    cell.merge(direction="right")
        if key == "Up" or key == "w" or key == "W":
            tempGrid = grid[::4]+grid[1::4]+grid[2::4]+grid[3::4]
            for cell in tempGrid:
                if cell != None:
                    cell.merge(direction="up")
        if key == "Down" or key == "s" or key == "S":
            tempGrid = (grid[::4]+grid[1::4]+grid[2::4]+grid[3::4])[::-1]
            for cell in tempGrid:
                if cell != None:
                    cell.merge(direction="down")

        if movement:
            Block(master=root.game).place()

            root.prevMatrix = prevMatrix
            root.prevScore = prevScore
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
                root.game.loss()
                root.game.loseNotifier.lift()
        if matrix.count(11) == 1:
            root.game.win()
            root.game.winNotifier.lift()

    def end(root, _: Event = None) -> None:
        if not pause:
            global ongoing
            if ongoing:
                ongoing = False
                if root.scoreVar.get() != 0:
                    name = CTkInputDialog(
                        text="Your game has ended; what name should we save your score with?",
                        title="the2048game | NAME REQUEST",
                        fg_color="#bdac97",
                        button_fg_color="#faf8f0",
                        button_hover_color="#eae7d9",
                        button_text_color="#988a86",
                        entry_border_color="#9b8878",
                        entry_fg_color="#bdac97",
                        entry_text_color="#ffffff"
                    )

                    windll.dwmapi.DwmSetWindowAttribute(
                        windll.user32.GetParent(name.winfo_id()), 
                        36, 
                        byref(c_int(0x00f0f8fa)), 
                        sizeof(c_int)
                    )
                    windll.dwmapi.DwmSetWindowAttribute(
                        windll.user32.GetParent(name.winfo_id()), 
                        35, 
                        byref(c_int(0x0097acbd)), 
                        sizeof(c_int)
                    )
                    name.title("")
                    name.after(200, lambda: name.iconbitmap(PATHS["empty"]))

                    cursor.execute(f"INSERT INTO Scores VALUES ('{datetime.now().date()} {datetime.now().hour}:{datetime.now().minute}.{datetime.now().second}', {root.scoreVar.get()}, {2**max(matrix)}, '{name.get_input()}')") 
                    conn.commit()
                for cell in grid: 
                    if cell: 
                        cell.destroy()
                highscore = cursor.execute(f'SELECT MAX(Score) FROM Scores').fetchone()[0]
                root.highVar.set(highscore if highscore != None else 0)
                root.scoreVar.set(0)
            if showingLoss:
                root.game.loseNotifier.clear()
            if showingWin:
                root.game.winNotifier.clear()

        else:
            system(f'start %windir%\\explorer.exe "{DIRECTORY}"')

    def play(root, _: Event = None) -> None:
        if not pause:
            global ongoing
            if not ongoing and not showingWin and not showingLoss:
                Block(master=root.game).place()
                Block(master=root.game).place()
                ongoing = True

        else:
            root.more.license()

    def increase(root, increment: int) -> None:
        root.scoreVar.set(root.scoreVar.get() + increment)

    def undo(root) -> None:
        global grid, matrix

        if not pause:
            if root.prevMatrix:
                for cell in grid:
                    if cell:
                        cell.destroy()
                        
                grid = [None]*16
                matrix = [0]*16

                for idx, cell in enumerate(root.prevMatrix):
                    if cell != 0:
                        temp = Block(root.game)
                        temp.power = cell
                        temp.x = ((idx%4)*136.25+73.125)*SCREEN_FACTOR
                        temp.y = ((idx//4)*136.25+73.125)*SCREEN_FACTOR
                        temp.pos = idx
                        temp.set()
                        temp.place()

                root.scoreVar.set(root.prevScore)

                root.prevMatrix = None
                root.prevScore = None

                if showingWin:
                    root.game.winNotifier.clear()
                if showingLoss:
                    root.game.loseNotifier.clear()

        else:
            openWeb("https://github.com/aahan0511/the2048game")

class More(CTkFrame):

    def __init__(more, master: App) -> None:
        super().__init__(
            master,
            border_color="#9c8978",
            border_width=5*SCREEN_FACTOR,
            fg_color="#bdac97",
            height=670*SCREEN_FACTOR,
            width=555*SCREEN_FACTOR,
            corner_radius=35*SCREEN_FACTOR
        )
        more.grid_propagate(False)

        more.rowconfigure(0, uniform="a", weight=10)
        more.rowconfigure(1, uniform="a", weight=33)
        more.rowconfigure(2, uniform="a", weight=606)
        more.rowconfigure(3, uniform="a", weight=19)
        more.columnconfigure((0, 1), weight=1, uniform="a")

        more.showingLeader = False
        more.leaderboardFilter = StringVar(value="score")
        more.leaderboardSize = StringVar(value=TABLE_LEN)
        more.leaderboard = Leaderboard(more, more.leaderboardFilter, more.leaderboardSize)
        more.leaderFilter = CTkSegmentedButton(
            more,
            values=["time", "score", "block", "name"],
            variable=more.leaderboardFilter,
            fg_color="#9b8878",
            selected_color="#eae7d9",
            selected_hover_color="#9b8878",
            unselected_hover_color="#bdac97",
            unselected_color="#faf8f0",
            text_color="#878787"
        )
        more.leaderSize = CTkComboBox(
            more, 
            values=["10", "15", "20", "25"], 
            variable=more.leaderboardSize,
            border_color="#9b8878",
            fg_color="#eae7d9",
            text_color="#878787",
            dropdown_fg_color="#eae7d9",
            dropdown_text_color="#878787",
            dropdown_hover_color="#faf8f0",
            button_color="#9b8878",
            button_hover_color="#9b8878"
        )

        more.showingHelp = False
        more.helpLabel = CTkLabel(
            more,
            text="",
            image=CTkImage(
                Image.open(PATHS["how to play.png"]),
                Image.open(PATHS["how to play.png"]),
                (535*SCREEN_FACTOR, 630*SCREEN_FACTOR)
            )
        )

        more.showingLicense = False
        more.licenseLabel = CTkLabel(
            more,
            text="",
            image=CTkImage(
                Image.open(PATHS["license.png"]),
                Image.open(PATHS["license.png"]),
                (535*SCREEN_FACTOR, 630*SCREEN_FACTOR)
            )
        )

    def help(more) -> None:
        if pause:
            if not more.showingHelp:
                more.clear()
                
                more.helpLabel.place(relx=0.5, rely=0.5, anchor="center")
            else:
                more.helpLabel.place_forget()
            more.showingHelp = not more.showingHelp

        else:
            openWeb("https://github.com/aahan0511/the2048game/discussions/1")

    def showLeaderboard(more) -> None:
        if not more.showingLeader: 
            more.clear()

            more.leaderFilter.grid(row=1, column=0, sticky="e", padx=5*SCREEN_FACTOR)
            more.leaderSize.grid(row=1, column=1, sticky="w", padx=5*SCREEN_FACTOR)
            more.leaderboard.show()
        else: 
            more.leaderFilter.grid_forget()
            more.leaderSize.grid_forget()
            more.leaderboard.hide()
        more.showingLeader = not more.showingLeader

    def show(more) -> None:
        more.place(x=415*SCREEN_FACTOR, y=342*SCREEN_FACTOR, anchor="center")
        more.lift()

    def hide(more) -> None:
        more.place_forget()
        more.clear()

    def clear(more) -> None:
        more.leaderFilter.grid_forget()
        more.leaderSize.grid_forget()
        more.leaderboard.hide()
        more.showingLeader = False

        more.helpLabel.place_forget()
        more.showingHelp = False

        more.licenseLabel.place_forget()
        more.showingLicense = False

    def license(more) -> None:
        if not more.showingLicense:
            more.clear()
            
            more.licenseLabel.place(relx=0.5, rely=0.5, anchor="center")
        else:
            more.licenseLabel.place_forget()
        more.showingLicense = not more.showingLicense

class Leaderboard(CTkTabview):

    def __init__(board, master: More, boardFilter: StringVar, boardSize: StringVar) -> None:
        super().__init__(
            master,
            fg_color="#9b8878",
            segmented_button_fg_color="#756452",
            segmented_button_selected_color="#eae7d9",
            segmented_button_selected_hover_color="#9b8878",
            segmented_button_unselected_hover_color="#bdac97",
            segmented_button_unselected_color="#faf8f0",
            text_color="#878787",
        )
        board.values = None
        board.filter = boardFilter
        board.size = boardSize

    def refresh(board, need=False, *_) -> None:
        match board.filter.get():
            case "time": filtr = 0
            case "score": filtr = 1
            case "block": filtr = 2
            case "name": filtr = 3
        if filtr == 0:
            def toDate(total: str) -> datetime:
                item = total[0].split(" ")
                date = item[0].split("-")
                time = item[1].split(":")
                hour = time[0]
                time = time[1].split(".")
                return datetime(
                    year=int(date[0]),
                    month=int(date[1]),
                    day=int(date[2]),
                    hour=int(hour),
                    minute=int(time[0]),
                    second=int(time[1]),
                )
            values = sorted(cursor.execute(f'SELECT * FROM Scores').fetchall(), key=lambda item: toDate(item), reverse=(True if filtr in [0, 3] else False))
        else:
            values = sorted(cursor.execute(f'SELECT * FROM Scores').fetchall(), key=lambda item: item[filtr], reverse=(True if filtr != 3 else False))

        if (board.values != values or board.values is None or need) and board.size.get() != "":
            try:
                if board.values is not None:
                    for tab in range(1, board.length+1):
                        board.delete(str(tab))
            except ValueError: pass

            size = int(board.size.get())
            if size < 10: size = 10
            if size > 25: size = 30
            board.length = len(values)//size + (1 if len(values)%size != 0 else 0)

            for tabNum in range(board.length):
                tabName = str(tabNum+1)

                board.add(tabName)

                CTkTable(
                    board.tab(tabName),
                    column=4,
                    values=[("TIME", "SCORE", "BLOCK", "NAME")]+values[size*tabNum:size*(tabNum+1)],
                    corner_radius=35,
                    header_color="#bdac97",
                    text_color="#756452",
                    colors=["#eae7d9", "#faf8f0"],
                    row=size+1
                ).pack(expand=True, fill="both")

            board.values = values

    def show(board) -> None:
        board.grid(row=2, column=0, sticky="nsew", padx=19, columnspan=2)
        board.filter.trace("w", board.refresh)
        board.size.trace("w", lambda *_: board.refresh(True))
        board.refresh()

    def hide(board) -> None:
        board.grid_forget()

class Header(CTkFrame):

    def __init__(header, master: App, scoreVar: IntVar, highVar: IntVar, icon: ImageTk.PhotoImage) -> None:
        super().__init__(
            master,
            fg_color="#bdac97",
            border_color="#9c8978",
            border_width=5,
            corner_radius=35,
            width=555*SCREEN_FACTOR, 
            height=100*SCREEN_FACTOR, 
        )

        header.rowconfigure(0, weight=1, uniform="a")
        header.columnconfigure(0, weight=2, uniform="a")
        header.columnconfigure((1, 2), weight=1, uniform="a")
        header.grid_propagate(False)

        header.namePlate = NamePlate(header, icon)

        header.curScore = Score(
            master=header, 
            color="#eae7d9", 
            pos=1, 
            description="SCORE", 
            var=scoreVar
        )

        header.highScore = Score(
            master=header, 
            color="#faf8f0", 
            pos=2, 
            description="BEST", 
            var=highVar
        )

        header.place(x=415*SCREEN_FACTOR, y=60*SCREEN_FACTOR, anchor="center")

class NamePlate(CTkFrame):

    def __init__(nameplate, master: Header, icon: ImageTk.PhotoImage) -> None:
        super().__init__(master, fg_color="transparent", bg_color="red")
        set_opacity(nameplate, color="red")

        nameplate.logo = CTkCanvas(
            nameplate,
            bd=0, 
            highlightthickness=0, 
            relief="ridge",
            background="#bdac97",
            width=80*SCREEN_FACTOR, 
            height=80*SCREEN_FACTOR
        )
        nameplate.logo.create_image(40*SCREEN_FACTOR, 40*SCREEN_FACTOR, image=icon, anchor="center")
        nameplate.logo.place(relx=0.2, rely=0.5, anchor="center")

        nameplate.name = CTkLabel(
            nameplate,
            text_color="#756452",
            text="2048",
            font=("JetBrains Mono Medium", 50*SCREEN_FACTOR, "bold")
        )
        nameplate.name.place(relx=0.6, rely=0.5, anchor="center")

        nameplate.grid(row=0, column=0, sticky="nsew", padx=10*SCREEN_FACTOR, pady=19*SCREEN_FACTOR)

class Score(CTkFrame):

    def __init__(score, master: Header, color: str, pos: int, description: str, var: IntVar) -> None:
        super().__init__(
            master,
            corner_radius=25,
            fg_color=color,
            border_color="#eae7d9",
            border_width=3*SCREEN_FACTOR,
        )

        score.label = CTkLabel(score, text=description, font=("JetBrains Mono Medium", 13*SCREEN_FACTOR), text_color="#988a86")
        score.label.place(relx=0.5, rely=0, anchor="n")

        set_opacity(score.label, color=color)

        score.number = CTkLabel(score, textvariable=var, text_color="#988a86", font=("JetBrains Mono Medium", 20*SCREEN_FACTOR), fg_color="#988a87")
        score.number.place(relx=0.5, rely=0.6, anchor="center")
        set_opacity(score.number, color="#988a87")

        score.grid(row=0, column=pos, sticky="nsew", padx=15*SCREEN_FACTOR, pady=19*SCREEN_FACTOR)

class Side(CTkFrame):

    def __init__(side, master: App, more: More) -> None:
        super().__init__(
            master,
            fg_color="#bdac97",
            border_color="#9c8978",
            border_width=5*SCREEN_FACTOR,
            corner_radius=35,
            width=100*SCREEN_FACTOR, 
            height=670*SCREEN_FACTOR, 
        )

        side.columnconfigure(0, weight=1, uniform="a")
        side.rowconfigure((0, 1, 3, 4, 5, 6), weight=10, uniform="a")
        side.rowconfigure((2), weight=7, uniform="a")
        side.grid_propagate(False)

        side.moreButton = CTkButton(
            side, 
            text="✨", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3*SCREEN_FACTOR,
            font=("JetBrains Mono Medium", 28*SCREEN_FACTOR*0.9),
            command=side.click
        )
        side.moreButton.grid(column=0, row=0, sticky="nsew", padx=19*SCREEN_FACTOR, pady=19*SCREEN_FACTOR)
        side.more = more

        side.help = CTkButton(
            side, 
            text="⭐", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3*SCREEN_FACTOR,
            font=("JetBrains Mono Medium", 28*SCREEN_FACTOR*0.9),
            command=more.help
        )
        side.help.grid(column=0, row=1, sticky="nsew", padx=19*SCREEN_FACTOR, pady=19*SCREEN_FACTOR)

        side.play = CTkButton(
            side, 
            text="🎮", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3*SCREEN_FACTOR,
            font=("JetBrains Mono Medium", 28*SCREEN_FACTOR*0.9),
            command=master.play
        )
        side.play.grid(column=0, row=3, sticky="nsew", padx=19*SCREEN_FACTOR, pady=19*SCREEN_FACTOR)

        side.undo = CTkButton(
            side, 
            text="🔙", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3*SCREEN_FACTOR,
            font=("JetBrains Mono Medium", 28*SCREEN_FACTOR*0.9),
            command=master.undo
        )
        side.undo.grid(column=0, row=4, sticky="nsew", padx=19*SCREEN_FACTOR, pady=19*SCREEN_FACTOR)

        side.info = CTkButton(
            side, 
            text="🪪", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3*SCREEN_FACTOR,
            font=("JetBrains Mono Medium", 28*SCREEN_FACTOR*0.9),
            command=master.game.info
        )
        side.info.grid(column=0, row=5, sticky="nsew", padx=19*SCREEN_FACTOR, pady=19*SCREEN_FACTOR)

        side.end = CTkButton(
            side, 
            text="❌", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3*SCREEN_FACTOR,
            font=("JetBrains Mono Medium", 28*SCREEN_FACTOR*0.9),
            command=master.end
        )
        side.end.grid(column=0, row=6, sticky="nsew", padx=19*SCREEN_FACTOR, pady=19*SCREEN_FACTOR)

        side.place(x=72.5*SCREEN_FACTOR, y=342*SCREEN_FACTOR, anchor="center")

    def click(side) -> None:
        global pause
        if not pause:
            side.more.show()
            side.help.configure(text="❔")
            side.play.configure(text="ℹ️")
            side.undo.configure(text="🌐")
            side.info.configure(text="🏅")
            side.end.configure(text="📂")
            side.moreButton.configure(text="🎲")
        else:
            side.more.hide()
            side.help.configure(text="⭐")
            side.play.configure(text="🎮")
            side.undo.configure(text="🔙")
            side.info.configure(text="🪪")
            side.end.configure(text="❌")
            side.moreButton.configure(text="✨")
        pause = not pause

class GameScreen(CTkFrame):

    def __init__(screen, master: App) -> None:
        super().__init__(
            master,
            fg_color="#9b8878",
            corner_radius=35,
            width=555*SCREEN_FACTOR, 
            height=555*SCREEN_FACTOR, 
        )

        screen.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")
        screen.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")
        screen.grid_propagate(False)

        screen.parent = master
        screen.information = None

        for row in range(4):
            for column in range(4):
                CTkLabel(
                    screen, 
                    text="",
                    fg_color="#bdac97",
                    corner_radius=35,
                    width=116.25*SCREEN_FACTOR,
                    height=116.25*SCREEN_FACTOR
                ).place(
                    anchor="center", 
                    x=(136.25*column+73.125)*SCREEN_FACTOR,
                    y=(136.25*row+73.125)*SCREEN_FACTOR
                )

        screen.place(x=415*SCREEN_FACTOR, y=400*SCREEN_FACTOR, anchor="center")

    def win(screen) -> None:
        if not showingLoss:
            global showingWin
            showingWin = True
            screen.winNotifier = Notification(screen, True)

    def loss(screen) -> None:
        if not showingWin:
            global showingLoss
            showingLoss = True
            screen.loseNotifier = Notification(screen, False)

    def info(screen) -> None:
        if not pause:
            if screen.information == None or not screen.information.winfo_exists():
                screen.information = Info(screen.parent)
            else:
                screen.information.focus()

        else:
            screen.parent.more.showLeaderboard()

class Info(CTkToplevel):

    def __init__(top, master: App) -> None:
        super().__init__(master, fg_color="#bdac97")
        top.title("the2048game | Info")

        top.geometry(f"{425*SCREEN_FACTOR}x{600*SCREEN_FACTOR}")
        top.resizable(False, False)
        top.after(200, lambda: top.iconbitmap(PATHS["empty"]))
        
        change_border_color(top, "#bdac97")
        change_header_color(top, "#bdac97")
        change_title_color(top, "#bdac97")

        top.image = CTkLabel(
            top,
            text="",
            image=CTkImage(
                Image.open(PATHS["info.png"]),
                Image.open(PATHS["info.png"]),
                (423*SCREEN_FACTOR, 600*SCREEN_FACTOR)
            )
        )
        top.image.pack(expand=True, fill="both")

        top.after(200, top.focus)
        top.after(200, lambda: top.bind("<Button>", lambda _: openWeb("https://github.com/aahan0511")))

class Notification(CTkFrame):

    def __init__(notifier, master: GameScreen, version: bool) -> None:
        if version:
            super().__init__(
                master, 
                fg_color="#ffd700", 
                corner_radius=35
            )
            notifier.grid(row=0, column=0, columnspan=4, rowspan=4, sticky="nsew")

            text = CTkLabel(
                notifier,
                font=("JetBrains Mono Medium", 100*SCREEN_FACTOR),
                text="You Win!",
                text_color="#888888"
            )
            text.place(relx=0.5, rely=0.5, anchor="center")

            subtext = CTkLabel(
                notifier,
                font=("JetBrains Mono Medium", 20*SCREEN_FACTOR),
                text="Click to Continue",
                text_color="#888888"
            )
            subtext.place(relx=0.5, rely=0.6, anchor="center")

            set_opacity(notifier, value=0.5, color="#9b8878")

            notifier.bind("<Button>", notifier.clear)        
            text.bind("<Button>", notifier.clear)        
            subtext.bind("<Button>", notifier.clear)        

        else:
            super().__init__(
                master, 
                fg_color="#888888", 
                corner_radius=35
            )
            notifier.grid(row=0, column=0, columnspan=4, rowspan=4, sticky="nsew")
            notifier.lift()

            text = CTkLabel(
                notifier,
                font=("JetBrains Mono Medium", 100*SCREEN_FACTOR),
                text="You Lose!",
                text_color="#ffffff"
            )
            text.place(relx=0.5, rely=0.5, anchor="center")

            subtext = CTkLabel(
                notifier,
                font=("JetBrains Mono Medium", 20*SCREEN_FACTOR),
                text="Press ❌ to Continue",
                text_color="#ffffff"
            )
            subtext.place(relx=0.5, rely=0.6, anchor="center")

            set_opacity(notifier, value=0.5, color="#9b8878")

    def clear(notifier, _: Event = None) -> None:
        global showingWin, showingLoss
        notifier.grid_forget()
        showingWin = False
        showingLoss = False

class Block:

    def __init__(block, master: GameScreen) -> None:
        if matrix.count(0) == 0:
            del block
            return

        block.power = choice([1]*9+[2])
        block.var = IntVar(value=2**block.power)
        block.cell = CTkLabel(
            master, 
            textvariable=block.var, 
            fg_color=COLORS[block.power] if block.power <= 11 else COLORS[-1], 
            text_color="#ffffff" if block.power > 2 else "#756452", 
            font=("JetBrains Mono Bold", 28*SCREEN_FACTOR if block.power <= 13 else 24*SCREEN_FACTOR),
            justify="center", 
            anchor="center",
            width=1,
            height=1,
            corner_radius=35,
            bg_color="transparent",
        )
        block.master = master
        block.mix = True

        block.pos = randint(0, 15)
        while matrix[block.pos] != 0: 
            block.pos = randint(0, 15)
        block.x = ((block.pos%4)*136.25+73.125)*SCREEN_FACTOR
        block.y = ((block.pos//4)*136.25+73.125)*SCREEN_FACTOR

    def place(block) -> None:
        block.cell.place(
            x=block.x, 
            y=block.y,
            anchor="center"
        )
        def grow(side):
            block.cell.configure(width=116.25*SCREEN_FACTOR-side, height=116.25*SCREEN_FACTOR-side, justify="center", anchor="center", corner_radius=35)
            if side > 0:
                block.cell.after(1, lambda: grow(side-GROW_SPEED if side>=GROW_SPEED else 0))
                block.cell.lift()
                if showingLoss:
                    block.cell.after(1, block.master.loseNotifier.lift)
                if showingWin:
                    block.cell.after(1, block.master.winNotifier.lift)
        grow(116.25*SCREEN_FACTOR)
        matrix[block.pos] = block.power
        grid[block.pos] = block 

    def destroy(block) -> None:
        grid[block.pos] = None
        matrix[block.pos] = 0
        block.cell.destroy()
        del block

    def set(block) -> None:
        block.var.set(2**block.power)
        block.cell.configure(
            fg_color=COLORS[block.power] if block.power <= 11 else COLORS[-1], 
            text_color="#ffffff" if block.power > 2 else "#756452", 
            font=("JetBrains Mono Bold", 28*SCREEN_FACTOR if block.power <= 13 else 24*SCREEN_FACTOR)
        )
        grid[block.pos] = block
        matrix[block.pos] = block.power

    def slide(block, pos: int) -> None:
        block.cell.place(
            x=((pos%4)*136.25+73.125)*SCREEN_FACTOR,
            y=((pos//4)*136.25+73.125)*SCREEN_FACTOR,
            anchor="center"
        ) #TODO: add slide function

    def merge(block, direction: str) -> None:
        global movement

        match direction:
            case "left":
                if block.pos%4 == 0: return
                cell = grid[block.pos-1]
                if cell == None:
                    block.slide(block.pos-1)
                    grid[block.pos] = None
                    matrix[block.pos] = 0
                    grid[block.pos-1] = block
                    matrix[block.pos-1] = block.power
                    block.pos -= 1
                    block.merge("left")
                    movement = True
                elif cell.power == block.power and cell.mix and block.mix:
                    grid[block.pos] = None
                    matrix[block.pos] = 0
                    block.slide(block.pos-1)
                    block.master.parent.increase(2**(cell.power+1))
                    block.destroy()
                    cell.power += 1
                    cell.set()
                    cell.mix = False
                    cell.merge("left")
                    movement = True

            case "right":
                if block.pos%4 == 3: return
                cell = grid[block.pos+1]
                if cell == None:
                    block.slide(block.pos+1)
                    grid[block.pos] = None
                    matrix[block.pos] = 0
                    grid[block.pos+1] = block
                    matrix[block.pos+1] = block.power
                    block.pos += 1
                    block.merge("right")
                    movement = True
                elif cell.power == block.power and cell.mix and block.mix:
                    grid[block.pos] = None
                    matrix[block.pos] = 0
                    block.slide(block.pos+1)
                    block.master.parent.increase(2**(cell.power+1))
                    block.destroy()
                    cell.power += 1
                    cell.set()
                    cell.mix = False
                    cell.merge("right")
                    movement = True

            case "up":
                if block.pos//4 == 0: return
                cell = grid[block.pos-4]
                if cell == None:
                    block.slide(block.pos-4)
                    grid[block.pos] = None
                    matrix[block.pos] = 0
                    grid[block.pos-4] = block
                    matrix[block.pos-4] = block.power
                    block.pos -= 4
                    block.merge("up")
                    movement = True
                elif cell.power == block.power and cell.mix and block.mix:
                    grid[block.pos] = None
                    matrix[block.pos] = 0
                    block.slide(block.pos-4)
                    block.master.parent.increase(2**(cell.power+1))
                    block.destroy()
                    cell.power += 1
                    cell.set()
                    cell.mix = False
                    cell.merge("up")
                    movement = True

            case "down":
                if block.pos//4 == 3: return
                cell = grid[block.pos+4]
                if cell == None:
                    block.slide(block.pos+4)
                    grid[block.pos] = None
                    matrix[block.pos] = 0
                    grid[block.pos+4] = block
                    matrix[block.pos+4] = block.power
                    block.pos += 4
                    block.merge("down")
                    movement = True
                elif cell.power == block.power and cell.mix and block.mix:
                    grid[block.pos] = None
                    matrix[block.pos] = 0
                    block.slide(block.pos+4)
                    block.master.parent.increase(2**(cell.power+1))
                    block.destroy()
                    cell.power += 1
                    cell.set()
                    cell.mix = False
                    cell.merge("down")
                    movement = True

app = App()

if app.scoreVar.get() != 0:
    name = CTkInputDialog(
        text="Your game has ended; what name should we save your score with?",
        title="the2048game | NAME REQUEST",
        fg_color="#bdac97",
        button_fg_color="#faf8f0",
        button_hover_color="#eae7d9",
        button_text_color="#988a86",
        entry_border_color="#9b8878",
        entry_fg_color="#bdac97",
        entry_text_color="#ffffff"
    )
    system("cls")

    name.after(200, lambda: name.iconbitmap(PATHS["empty"]))

    windll.dwmapi.DwmSetWindowAttribute(
        windll.user32.GetParent(name.winfo_id()), 
        36, 
        byref(c_int(0x0097acbd)), 
        sizeof(c_int)
    )
    windll.dwmapi.DwmSetWindowAttribute(
        windll.user32.GetParent(name.winfo_id()), 
        35, 
        byref(c_int(0x0097acbd)), 
        sizeof(c_int)
    )

    cursor.execute(f"INSERT INTO Scores VALUES ('{datetime.now().date()} {datetime.now().hour}:{datetime.now().minute}.{datetime.now().second}', {app.scoreVar.get()}, {2**max(matrix)}, '{name.get_input()}')") 
    conn.commit()

conn.close()