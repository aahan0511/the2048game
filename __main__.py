# ======= imports ======= #
from customtkinter import CTkFrame, CTk, IntVar, CTkCanvas, CTkLabel, CTkButton, CTkTabview, CTkInputDialog, CTkSegmentedButton, StringVar, CTkComboBox
from os import path as osPath, makedirs, getlogin, system
from sqlite3 import connect
from sys import path
from _tkinter import TclError
from tkinter import Event
from CTkTable import CTkTable
from PIL import Image, ImageTk
from random import randint, choice
from webbrowser import open as openWeb
from datetime import datetime
# ======= ------- ======= #

# ======= constants ======= #
USER = getlogin()
DIRECTORY = f"C:\\Users\\{USER}\\AppData\\Local\\"+"the2048game\\"
COLORS = [None, "#eee4da", "#ebd8b6", "#f3b178", "#f69562", "#f88165", "#f76644", "#f0d26c", "#edcc61", "#edc850", "#edc53f", "#edc22e", "#393931"]
PATHS = {
    "empty" : f"{path[0]}\\images\\empty.ico",
    "favicon" : f"{path[0]}\\images\\favicon.ico",
    "icon" : f"{path[0]}\\images\\icon.png"
}
FONT = "JetBrains Mono Medium"
SPEED = 5
GROW_SPEED = 3.6
TABLE_LEN = 20
# ======= --------- ======= #

# ======= global variables ======= #
grid = [None]*16
matrix = [0]*16
ongoing = False
showingWin = False
showingLoss = False
pause = False
# ======= ------ --------- ======= #

# ======= directory and database creation ======= #
if not osPath.exists(DIRECTORY): 
    makedirs(DIRECTORY)

conn = connect(f"{DIRECTORY}\\2048.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Scores (Time TEXT, Score INTEGER, Block INTEGER, NAME TEXT)")
# ======= --------- --- -------- -------- ======= #

# ======= window ======= #
class App(CTk):

    # ======= init ======= #
    def __init__(root) -> None:
        # ======= window setup ======= #
        super().__init__("#faf8f0")
        root.geometry("715x700+50+50")
        root.resizable(False, False)

        root.bind("<Any-KeyPress>", root.keyPress)
        root.bind("<space>", root.play)
        root.bind("<Escape>", root.end)
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
        root.scoreVar = IntVar(value=0)
        root.highVar = IntVar(value=cursor.execute(f'''SELECT MAX(Score) FROM Scores''').fetchone()[0])
        icon = ImageTk.PhotoImage(Image.open(PATHS["icon"]).resize((80, 80)))
        # ======= --------- ======= # 

        # ======= gui ======= #
        root.more = More(master=root)
        root.header = Header(
            master=root, 
            scoreVar=root.scoreVar,
            highVar=root.highVar,
            icon=icon
        )
        root.game = GameScreen(master=root)
        root.side = Side(master=root, more=root.more)
        # ======= --- ======= #

        # ======= mainloop ======= #
        root.mainloop()
        # ======= -------- ======= #
    # ======= ---- ======= #

    # ======= key press ======= #
    def keyPress(root, event: Event) -> None:
        # ======= declarations ======= #
        global movement
        movement = False
        key = event.keysym
        # ======= ------------ ======= #

        # ======= exceptions and restart ======= #
        if showingWin or showingLoss: return

        for cell in grid:
            if cell != None:
                cell.mix = True
        # ======= --------- --- ------- ======= #

        # ======= movement switchcase ======= #
        if key == "Left" or key == "a":
            for cell in grid:
                if cell != None:
                    cell.merge(direction="left")
        if key == "Right" or key == "d":
            for cell in grid[::-1]:
                if cell != None:
                    cell.merge(direction="right")
        if key == "Up" or key == "w":
            tempGrid = grid[::4]+grid[1::4]+grid[2::4]+grid[3::4]
            for cell in tempGrid:
                if cell != None:
                    cell.merge(direction="up")
        if key == "Down" or key == "s":
            tempGrid = (grid[::4]+grid[1::4]+grid[2::4]+grid[3::4])[::-1]
            for cell in tempGrid:
                if cell != None:
                    cell.merge(direction="down")
        # ======= -------- ---------- ======= #

        # ======= game checks ======= #
        if movement:
            Block(master=root.game).place()
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
        # ======= ---- ------ ======= #
    # ======= --- ----- ======= #

    # ======= end ======= #
    def end(root, _: Event = None) -> None:
        # ======= end ======= #
        if not pause:
            global ongoing
            if ongoing:
                ongoing = False
                if root.scoreVar.get() != 0:
                    name = CTkInputDialog(
                        text="Your game has ended; what name should we save your score with?",
                        title="the2048game: NAME REQUEST",
                        fg_color="#bdac97",
                        button_fg_color="#faf8f0",
                        button_hover_color="#eae7d9",
                        button_text_color="#988a86",
                        entry_border_color="#9b8878",
                        entry_fg_color="#bdac97",
                        entry_text_color="#ffffff"
                    )

                    try:
                        from ctypes import windll, byref, sizeof, c_int
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
                    except ImportError:
                        name.title("NAME REQUEST")

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
        # ======= --- ======= #

        # ======= open folder ======= #
        else:
            try: system(f'start %windir%\\explorer.exe "{DIRECTORY}"')
            except: pass #TODO: add open folder for non-windows
        # ======= ---- ------ ======= #
    # ======= --- ======= #
    
    # ======= play ======= #
    def play(root, _: Event = None) -> None:
        # ======= play ======= #
        if not pause:
            global ongoing
            if not ongoing and not showingWin and not showingLoss:
                Block(master=root.game).place()
                Block(master=root.game).place()
                ongoing = True
        # ======= ---- ======= #

        # ======= settings ======= #
        else:
            pass #TODO: add settings function
        # ======= ---- ----------- ======= #
    # ======= ---- ======= #

    # ======= score increaser ======= #
    def increase(root, increament: int) -> None:
        root.scoreVar.set(root.scoreVar.get()+increament)
    # ======= ----- --------- ======= #

    # ======= undo ======= #
    def undo(screen) -> None:
        # ======= undo ======= #
        if not pause:
            pass #TODO: add undo function
        # ======= ---- ======= #

        # ======= open website ======= #
        else:
            openWeb("https://github.com/aahan0511/the2048game")
        # ======= ---- ------- ======= #
    # ======= ---- ======= #
# ======= ------ ======= #

# ======= more box ======= #
class More(CTkFrame):

    # ======= init ======= #
    def __init__(more, master: App) -> None:
        # ======= setup ======= #
        super().__init__(
            master,
            border_color="#9c8978",
            border_width=5,
            fg_color="#bdac97",
            height=670,
            width=555,
            corner_radius=35
        )
        more.grid_propagate(False)

        more.rowconfigure(0, uniform="a", weight=10)
        more.rowconfigure(1, uniform="a", weight=33)
        more.rowconfigure(2, uniform="a", weight=606)
        more.rowconfigure(3, uniform="a", weight=19)
        more.columnconfigure((0, 1), weight=1, uniform="a")
        # ======= ----- ======= #

        # ======= leaderboard ======= #
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
        # ======= ----------- ======= #
    # ======= ---- ======= #

    # ======= help ======= #
    def help(more) -> None:
        # ======= help ======= #
        if pause:
            pass #TODO: add help function
        # ======= ---- ======= #

        # ======= star ======= #
        else:
            openWeb("https://github.com/aahan0511/the2048game/discussions/5")
        # ======= ---- ======= #
    # ======= ---- ======= #

    # ======= show leaderboard ======= #
    def showLeaderboard(more) -> None:
        if not more.showingLeader: 
            more.leaderFilter.grid(row=1, column=0, sticky="e", padx=5)
            more.leaderSize.grid(row=1, column=1, sticky="w", padx=5)
            more.leaderboard.show()
        else: 
            more.leaderFilter.grid_forget()
            more.leaderSize.grid_forget()
            more.leaderboard.hide()
        more.showingLeader = not more.showingLeader
    # ======= ---- ----------- ======= #

    # ======= show ======= #
    def show(more) -> None:
        more.place(x=415, y=342, anchor="center")
        more.lift()
    # ======= ---- ======= #

    # ======= hide ======= #
    def hide(more) -> None:
        more.place_forget()

        more.leaderFilter.grid_forget()
        more.leaderSize.grid_forget()
        more.leaderboard.hide()
        more.showingLeader = False
    # ======= ---- ======= #
# ======= ---- --- ======= #

# ======= leaderboard ======= #
class Leaderboard(CTkTabview):

    # ======= init ======= #
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
    # ======= ---- ======= #

    # ======= refresh ======= #
    def refresh(board, need=False, *_) -> None:
        match board.filter.get():
            case "time": filtr = 0
            case "score": filtr = 1
            case "block": filtr = 2
            case "name": filtr = 3
        if filtr == 0:
            def toDate(total: str) -> None:
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

        if (board.values != values or board.values == None or need) and board.size.get() != "":
            try:
                if board.values != None:
                    for tab in range(1, board.length+1):
                        board.delete(str(tab))
            except ValueError: pass

            size = int(board.size.get())
            if size < 10: size = 10
            if size > 25: size = 30
            board.length = len(values)//size + (1 if len(values)%size != 0 else 0)

            # ======= table creation ======= #
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
            # ======= ----- -------- ======= #

            board.values = values
    # ======= ------- ======= #

    # ======= show ======= #
    def show(board) -> None:
        board.grid(row=2, column=0, sticky="nsew", padx=19, columnspan=2)
        board.filter.trace("w", board.refresh)
        board.size.trace("w", lambda *_: board.refresh(True))
        board.refresh()
    # ======= ---- ======= #

    # ======= hide ======= #
    def hide(board) -> None:
        board.grid_forget()
    # ======= ---- ======= #
# ======= ----------- ======= #

# ======= header ======= #
class Header(CTkFrame):

    # ======= init ======= #
    def __init__(header, master: App, scoreVar: IntVar, highVar: IntVar, icon: ImageTk.PhotoImage) -> None:
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
        # ======= --- ======= #

        # ======= place ======= #
        header.place(x=415, y=60, anchor="center")
        # ======= ----- ======= #
    # ======= ---- ======= #
# ======= ------ ======= #

# ======= name plate box ======= #
class NamePlate(CTkFrame):

    # ======= init ======= #
    def __init__(nameplate, master: Header, icon: ImageTk.PhotoImage) -> None:
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
    def __init__(score, master: Header, color: str, pos: int, description: str, var: IntVar) -> None:
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

        try:
            import pywinstyles
            pywinstyles.set_opacity(score.label, color=color)
        except ImportError: pass

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
    def __init__(side, master: App, more: More) -> None:
        # ======= setup ======= #
        super().__init__(
            master,
            fg_color="#bdac97",
            border_color="#9c8978",
            border_width=5,
            corner_radius=35,
            width=100, 
            height=670, 
        )
        # ======= ----- ======= #

        # ======= grid setup ======= #
        side.columnconfigure(0, weight=1, uniform="a")
        side.rowconfigure((0, 1, 3, 4, 5, 6), weight=100, uniform="a")
        side.rowconfigure((2), weight=70, uniform="a")
        side.grid_propagate(False)
        # ======= ---- ----- ======= #

        # ======= gui ======= #
        side.moreButton = CTkButton(
            side, 
            text="✨", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=(FONT, 28),
            command=side.click
        )
        side.moreButton.grid(column=0, row=0, sticky="nsew", padx=19, pady=19)
        side.more = more

        side.help = CTkButton(
            side, 
            text="⭐", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=(FONT, 28),
            command=more.help
        )
        side.help.grid(column=0, row=1, sticky="nsew", padx=19, pady=19)

        side.play = CTkButton(
            side, 
            text="🎮", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=(FONT, 28),
            command=master.play
        )
        side.play.grid(column=0, row=3, sticky="nsew", padx=19, pady=19)

        side.undo = CTkButton(
            side, 
            text="🔙", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=(FONT, 28),
            command=master.undo
        )
        side.undo.grid(column=0, row=4, sticky="nsew", padx=19, pady=19)

        side.hint = CTkButton(
            side, 
            text="💡", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=(FONT, 28),
            command=master.game.hint
        )
        side.hint.grid(column=0, row=5, sticky="nsew", padx=19, pady=19)
        
        side.end = CTkButton(
            side, 
            text="❌", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=(FONT, 28),
            command=master.end
        )
        side.end.grid(column=0, row=6, sticky="nsew", padx=19, pady=19)
        # ======= --- ======= #

        # ======= place ======= #
        side.place(x=72.5, y=342, anchor="center")
        # ======= ----- ======= #
    # ======= ---- ======= #

    # ======= click ======= #
    def click(side) -> None:
        global pause
        if not pause:
            side.more.show()
            side.help.configure(text="❔")
            side.play.configure(text="⚙️")
            side.undo.configure(text="🌐")
            side.hint.configure(text="🏅")
            side.end.configure(text="📂")
            side.moreButton.configure(text="🎲")
        else:
            side.more.hide()
            side.help.configure(text="⭐")
            side.play.configure(text="🎮")
            side.undo.configure(text="🔙")
            side.hint.configure(text="💡")
            side.end.configure(text="❌")
            side.moreButton.configure(text="✨")
        pause = not pause
    # ======= ----- ======= #
# ======= ---- --- ======= #

# ======= game screen ======= #
class GameScreen(CTkFrame):

    # ======= init ======= #
    def __init__(screen, master: App) -> None:
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

        # ======= variable ======= #
        screen.parent = master
        # ======= -------- ======= #

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
        screen.place(x=415, y=400, anchor="center")
        # ======= ----- ======= #
    # ======= ---- ======= #

    # ======= win ======= #
    def win(screen) -> None:
        if not showingLoss:
            global showingWin
            showingWin = True
            screen.winNotifier = Notification(screen, True)
    # ======= --- ======= #

    # ======= loss ======= #
    def loss(screen) -> None:
        if not showingWin:
            global showingLoss
            showingLoss = True
            screen.loseNotifier = Notification(screen, False)
    # ======= --- ======= #

    # ======= hint ======= #
    def hint(screen) -> None:
        # ======= hint ======= #
        if not pause:
            pass #TODO: add hint function
        # ======= ---- ======= #

        # ======= show leaderboard ======= #
        else:
            screen.parent.more.showLeaderboard()
        # ======= ---- ======= #
    # ======= ---- ======= #
# ======= ---- ------ ======= #

# ======= notification ======= #
class Notification(CTkFrame):

    # ======= init ======= #
    def __init__(notifier, master: GameScreen, version: bool) -> None:
        # ======= win ======= #
        if version:
            # ======= setup ======= #
            super().__init__(
                master, 
                fg_color="#ffd700", 
                corner_radius=35
            )
            notifier.grid(row=0, column=0, columnspan=4, rowspan=4, sticky="nsew")
            # ======= ----- ======= #

            # ======= gui ======= #
            text = CTkLabel(
                notifier,
                font=(FONT, 100),
                text="You Win!",
                text_color="#888888"
            )
            text.place(relx=0.5, rely=0.5, anchor="center")

            subtext = CTkLabel(
                notifier,
                font=(FONT, 20),
                text="Click to Continue",
                text_color="#888888"
            )
            subtext.place(relx=0.5, rely=0.6, anchor="center")
            
            try:
                import pywinstyles
                pywinstyles.set_opacity(notifier, value=0.5, color="#9b8878")
            except ImportError: pass
            # ======= --- ======= #

            # ======= exit ======= #
            notifier.bind("<Button>", notifier.clear)        
            text.bind("<Button>", notifier.clear)        
            subtext.bind("<Button>", notifier.clear)        
            # ======= ---- ======= #
        # ======= --- ======= #

        # ======= loss ======= #
        else:
            # ======= setup ======= #
            super().__init__(
                master, 
                fg_color="#888888", 
                corner_radius=35
            )
            notifier.grid(row=0, column=0, columnspan=4, rowspan=4, sticky="nsew")
            notifier.lift()
            # ======= ----- ======= #

            # ======= gui ======= #
            text = CTkLabel(
                notifier,
                font=(FONT, 100),
                text="You Lose!",
                text_color="#ffffff"
            )
            text.place(relx=0.5, rely=0.5, anchor="center")

            subtext = CTkLabel(
                notifier,
                font=(FONT, 20),
                text="Press ❌ to Continue",
                text_color="#ffffff"
            )
            subtext.place(relx=0.5, rely=0.6, anchor="center")

            try:
                import pywinstyles
                pywinstyles.set_opacity(notifier, value=0.5, color="#9b8878")
            except ImportError: pass
            # ======= --- ======= #
        # ======= ---- ======= #
    # ======= ---- ======= #

    # ======= clear ======= #
    def clear(notifier, _: Event = None) -> None:
        global showingWin, showingLoss
        notifier.grid_forget()
        showingWin = False
        showingLoss = False
    # ======= ----- ======= #
# ======= ------------ ======= #

# ======= block ======= #
class Block:

    # ======= init ======= #
    def __init__(block, master: GameScreen) -> None:
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
            font=(FONT, 28 if block.power <= 13 else 24),
            justify="center", 
            anchor="center",
            width=1,
            height=1,
            corner_radius=35,
            bg_color="transparent",
        )
        block.master = master
        block.mix = True
        # ======= ----- ======= #

        # ======= position chooser ======= #
        block.pos = randint(0, 15)
        while matrix[block.pos] != 0: 
            block.pos = randint(0, 15)
        block.x = (block.pos%4)*136.25+73.125
        block.y = (block.pos//4)*136.25+73.125
        # ======= -------- ------- ======= #
    # ======= ---- ======= #

    # ======= place ======= #
    def place(block) -> None:
        block.cell.place(
            x=block.x, 
            y=block.y,
            anchor="center"
        )
        def grow(side):
            block.cell.configure(width=116.25-side, height=116.25-side, justify="center", anchor="center", corner_radius=35)
            if side > 0:
                block.cell.after(1, lambda: grow(side-GROW_SPEED if side>=GROW_SPEED else 0))
                block.cell.lift()
                if showingLoss:
                    block.cell.after(1, block.master.loseNotifier.lift)
                if showingWin:
                    block.cell.after(1, block.master.winNotifier.lift)
        grow(116.25)
        matrix[block.pos] = block.power
        grid[block.pos] = block 
    # ======= ----- ======= #

    # ======= destroy ======= #
    def destroy(block) -> None:
        grid[block.pos] = None
        matrix[block.pos] = 0
        block.cell.destroy()
        del block
    # ======= ------- ======= #

    # ======= set ======= #
    def set(block) -> None:
        block.var.set(2**block.power)
        block.cell.configure(
            fg_color=COLORS[block.power] if block.power <= 11 else COLORS[-1], 
            text_color="#ffffff" if block.power > 2 else "#756452", 
            font=(FONT, 28 if block.power <= 13 else 24)
        )
        grid[block.pos] = block
        matrix[block.pos] = block.power
    # ======= --- ======= #

    # ======= slide ======= #
    def slide(block, pos: int) -> None:
        block.cell.place(
            x=(pos%4)*136.25+73.125,
            y=(pos//4)*136.25+73.125,
            anchor="center"
        ) #TODO: add slide function
    # ======= ----- ======= #

    # ======= merge ======= #           
    def merge(block, direction: str) -> None:
        # ======= global variable ======= #
        global movement
        # ======= ------ -------- ======= #

        # ======= direction switch case ======= #
        match direction:
            # ======= left ======= #
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
            # ======= ---- ======= #

            # ======= right ======= #
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
            # ======= ----- ======= #

            # ======= up ======= #
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
            # ======= -- ======= #

            # ======= down ======= #
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
            # ======= ---- ======= #
        # ======= --------- ------ ---- ======= #
    # ======= ----- ======= #
# ======= ----- ======= #

# ======= execution ======= #
app = App()

# ======= database closure ======= #
if app.scoreVar.get() != 0:
    name = CTkInputDialog(
        text="Your game has ended; what name should we save your score with?",
        title="the2048game: NAME REQUEST",
        fg_color="#bdac97",
        button_fg_color="#faf8f0",
        button_hover_color="#eae7d9",
        button_text_color="#988a86",
        entry_border_color="#9b8878",
        entry_fg_color="#bdac97",
        entry_text_color="#ffffff"
    )

    try:
        from ctypes import windll, byref, sizeof, c_int
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
    except ImportError: pass
    
    cursor.execute(f"INSERT INTO Scores VALUES ('{datetime.now().date()} {datetime.now().hour}:{datetime.now().minute}.{datetime.now().second}', {app.scoreVar.get()}, {2**max(matrix)}, '{name.get_input()}')") 
    conn.commit()
conn.close()
# ======= -------- ------- ======= #
# ======= --------- ======= #