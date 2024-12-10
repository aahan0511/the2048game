# ======= imports ======= #
from os import getlogin, makedirs, path, remove, rename, system

# ===== install modules ===== #
system("pip install customtkinter pillow CTkTable pywinstyles pyglet")
# ===== ------- ------- ===== #

from customtkinter import *
from pywinstyles import change_border_color, change_header_color, change_title_color, set_opacity
from shutil import rmtree
from json import loads
from requests import get
from urllib.request import urlretrieve
from pyglet import options, font
from webbrowser import open as openWeb
from PIL import Image
# ======= ------- ======= #

# ======= dir creation ======= #
USER = getlogin()
DIR = f"C:\\Users\\{USER}\\AppData\\Local\\the2048game"
# ======= --- -------- ======= #

# ======= paths ======= #
PATHS = {
    "assets" : DIR+"\\assets",
    "favicon.ico" : DIR+"\\assets\\images\\favicon.ico",
    "JetBrainsMono-Medium.ttf" : DIR+"\\assets\\fonts\\JetBrainsMono-Medium.ttf",
    "JetBrainsMono-Bold.ttf" : DIR+"\\assets\\fonts\\JetBrainsMono-Bold.ttf",
    "icon.png" : DIR+"\\assets\\images\\icon.png",
    "the2048game.exe" : DIR+"\\binary\\the2048game.exe",
    "Desktop" : f"C:\\Users\\{USER}\\OneDrive\\Desktop",
    "__main__.py" : DIR+"\\__main__.py"
}
# ======= ----- ======= #

# ======= assets download ======= #
# ====== download fucntion ===== #
def download(*keep: str) -> None:
    "CODE INSPIRATION from Fransiscus Emmanuel Bunaren | https://github.com/fbunaren/GitHubFolderDownloader"

    # ===== clear ===== #
    if path.exists(DIR): rmtree(DIR)
    makedirs(DIR)
    # ===== ----- ===== #

    # ===== install ===== #
    for item in [[x['path'],x['url'].replace('https://api.github.com/repos/','https://raw.githubusercontent.com/').split('/git/blobs/')[0]+'/main/'+x['path']] for x in loads(get("https://api.github.com/repos/aahan0511/the2048game/git/trees/main?recursive=1").text)['tree'] if x["type"]=="blob"]:
        if item[0] in keep:
            if not path.isdir(DIR+'/'+path.dirname(item[0])): makedirs(DIR+'/'+path.dirname(item[0]))
            urlretrieve(item[1], DIR + '/' + item[0])
    # ===== ------- ===== #
# ====== -------- -------- ===== #

download(
    "assets/fonts/JetBrainsMono-Bold.ttf",
    "assets/fonts/JetBrainsMono-Medium.ttf",
    "assets/images/empty.ico",
    "assets/images/favicon.ico",
    "assets/images/icon.png",
    "__main__.py",
    "binary/the2048game.exe"
)
# ======= ------ -------- ======= #

# ======= font installation ======= #
options['win32_gdi_font'] = True
font.add_file(PATHS["JetBrainsMono-Medium.ttf"])
font.add_file(PATHS["JetBrainsMono-Bold.ttf"])
# ======= ---- ------------ ======= #

# ======= app ======= #
class App(CTk):

    # ====== init ====== #
    def __init__(root) -> None:
        # ===== setup ===== #
        super().__init__(fg_color="#faf8f0")

        root.title("the2048game | SETUP")
        root.geometry("600x400")
        root.iconbitmap(PATHS["favicon.ico"])
        root.resizable(False, False)
        root.minsize(600, 400)

        root.attributes("-topmost", True)
        root.attributes("-topmost", False)

        change_header_color(root, "#faf8f0")
        change_border_color(root, "#faf8f0")
        change_title_color(root, "#756452")
        # ===== ----- ===== #

        # ===== gui ===== #
        root.columnconfigure(0, weight=1, uniform="a")
        root.columnconfigure(1, weight=2, uniform="a")
        root.rowconfigure((0, 1), weight=1, uniform="a")

        root.binary = Binary(root)
        root.binaryInstallation = CTkButton(
            root, 
            text="Binary\nInstallation", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=("JetBrains Mono Bold", 35),
            command=root.showBinary
        )
        root.binaryInstallation.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        root.source = Source(root)
        root.sourceCode = CTkButton(
            root, 
            text="Source\nCode", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=("JetBrains Mono Bold", 35),
            command=root.showSourceCode
        )
        root.sourceCode.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        root.info = Info(root)
        root.info.grid(row=0, column=0, padx=10, pady=10, rowspan=2)
        # ===== --- ===== #

        # ===== mainloop ===== #
        root.mainloop()
        # ===== -------- ===== #
    # ====== ---- ====== #

    # ====== show binary ====== #
    def showBinary(root) -> None:
        root.binary.grid(row=0, column=1, sticky="nsew", rowspan=2, padx=10, pady=10)
        root.binary.lift()
    # ====== ---- ------ ====== #

    # ====== show sourcecode ====== #
    def showSourceCode(root) -> None:
        root.source.grid(row=0, column=1, sticky="nsew", rowspan=2, padx=10, pady=10)
        root.source.lift()
    # ====== ---- ---------- ====== #
# ======= --- ======= #

# ======= info ======= #
class Info(CTkFrame):
    
    # ====== init ====== #
    def __init__(info, master: App) -> None:
        # ===== setup ===== #
        super().__init__(
            master, 
            fg_color="transparent",
            corner_radius=35,
            height=275
        )
        info.pack_propagate(False)
        # ===== ----- ===== #

        # ===== gui ===== #
        info.name = CTkLabel(
            info, 
            fg_color="transparent",
            text="© 2024 Aahan Salecha",    
            font=("JetBrains Mono Medium", 15),
            text_color="#bdac97"
        )
        info.name.bind("<Button>", lambda _: openWeb("https://github.com/aahan0511/the2048game?tab=MIT-1-ov-file"))
        info.name.bind("<Enter>", lambda _: info.name.configure(text_color="#9b8878"))
        info.name.bind("<Leave>", lambda _: info.name.configure(text_color="#bdac97"))
        info.name.pack(side="bottom")

        info.link = CTkLabel(
            info,
            text_color="#bdac97",
            text="@aahan0511",
            font=("JetBrains Mono Bold", 15)
        )
        info.link.bind("<Button>", lambda _: openWeb("https://github.com/aahan0511"))
        info.link.bind("<Enter>", lambda _: info.link.configure(text_color="#9b8878"))
        info.link.bind("<Leave>", lambda _: info.link.configure(text_color="#bdac97"))
        info.link.pack(side="bottom")

        logo = Image.open(PATHS["icon.png"])
        info.logo = CTkLabel(
            info, 
            image=CTkImage(
                light_image=logo,
                dark_image=logo,
                size=(150, 150)
            ),
            text=""
        )
        info.logo.bind("<Button>", lambda _: openWeb("https://github.com/aahan0511/the2048game"))
        info.logo.bind("<Enter>", lambda _: info.app.configure(text_color="#9b8878"))
        info.logo.bind("<Leave>", lambda _: info.app.configure(text_color="#bdac97"))
        info.logo.pack(side="top")

        info.app = CTkLabel(
            info, 
            fg_color="transparent",
            text="the2048game",
            font=("JetBrains Mono Bold", 20),
            text_color="#bdac97"
        )
        info.app.bind("<Button>", lambda _: openWeb("https://github.com/aahan0511/the2048game"))
        info.app.bind("<Enter>", lambda _: info.app.configure(text_color="#9b8878"))
        info.app.bind("<Leave>", lambda _: info.app.configure(text_color="#bdac97"))
        info.app.pack(side="top")
        # ===== --- ===== #
    # ====== ---- ====== #
# ======= ---- ======= #

# ======= binary ======= #
class Binary(CTkFrame):

    # ====== init ====== #
    def __init__(frame, master: App) -> None:
        # ===== setup ===== #
        super().__init__(
            master,
            fg_color="#bdac97",
            corner_radius=25,
            border_color="#9c8978",
            border_width=5
        )

        frame.pack_propagate(False)

        frame.rowconfigure(0, weight=3, uniform="a")
        frame.rowconfigure(1, weight=5, uniform="a")

        frame.columnconfigure(0, weight=1, uniform="a")
        # ===== ----- ===== #

        # ===== gui ===== #
        frame.installer = BinaryInstaller(frame)

        frame.button = CTkButton(
            frame,
            text="Install", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=("JetBrains Mono Bold", 35),
            command=frame.installer.install
        )
        frame.button.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        frame.license = CTkTextbox(
            frame,
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            border_color="#eae7d9",
            border_width=3,
            font=("JetBrains Mono Medium", 10)
        )
        frame.license.insert(
            0.0,
            "MIT License\n\nCopyright (c) 2024 Aahan Salecha\n\nPermission is hereby granted, free of charge, to any\nperson obtaining a copy of this software and\nassociated documentation files (the \"Software\"), to\ndeal in the Software without restriction, including\nwithout limitation the rights to use, copy, modify,\nmerge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the\nfollowing conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial\nportions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT\nLIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO\nEVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\nFROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."
        )
        frame.license.configure(state="disabled")
        frame.license.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        # ===== --- ===== #
    # ====== ---- ====== #
# ======= ------ ======= #

# ======= binary install frame ======= #
class BinaryInstaller(CTkFrame):

    # ====== init ====== #
    def __init__(installer, master: Binary) -> None:
        # ===== setup ===== #
        super().__init__(
            master,
            fg_color="#bdac96",
            corner_radius=25,
            border_color="#9c8978",
            border_width=5
        )
        installer.grid_propagate(False)
        set_opacity(installer, color="#bdac97")
        # ===== ----- ===== #

        # ===== gui ===== #
        installer.rowconfigure(0, weight=1, uniform="a")
        installer.rowconfigure(1, weight=3, uniform="a")
        installer.columnconfigure(0, weight=1, uniform="a")

        installer.record = CTkTextbox(
            installer,
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            border_color="#eae7d9",
            border_width=3,
            font=("JetBrains Mono Medium", 10)
        )
        installer.record.insert(
            "0.0",
            f"\n#01 Initialize Connection\n#02 Install Assets\n#03 Install Binary\n"
        )
        installer.record.grid(row=1, column=0, sticky="nsew", padx=19, pady=19)

        installer.progress = CTkProgressBar(
            installer,
            border_width=3,
            border_color="#eae7d9",
            fg_color="#bdac96",
            progress_color="#faf8f0",
            height=25
        )
        installer.progress.set(1)
        installer.progress.grid(row=0, column=0, sticky="new", padx=19, pady=30)
        
        installer.percent = CTkLabel(
            installer,
            fg_color="#bdac96",
            text="Progress: 100%",
            text_color="#eae7d9",
            font=("JetBrains Mono Bold", 20)
        )
        installer.percent.grid(row=0, column=0, sticky="sew", padx=19, pady=10)
        # ===== --- ===== #
    # ====== ---- ====== #

    # ====== install ====== #
    def install(installer) -> None:
        installer.grid(row=0, column=0, rowspan=3, sticky="nsew")
        installer.lift()

        # ===== move to desktop ===== #
        if path.exists(PATHS["Desktop"]+"\\the2048game.exe"): remove(PATHS["Desktop"]+"\\the2048game.exe")
        rename(
            PATHS["the2048game.exe"], 
            PATHS["Desktop"]+"\\the2048game.exe"
        )
        # ===== ---- -- ------- ===== #

        installer.record.insert("end", "#04 Add to Desktop\n\nNOTE\nIt may take a few seconds till the app gets to\nDesktop. You may close the app.")
        installer.record.configure(state="disabled")
    # ====== ------- ====== #
# ======= ------ ------- ----- ======= #

# ======= binary ======= #
class Source(CTkFrame):

    # ====== init ====== #
    def __init__(frame, master: App) -> None:
        # ===== setup ===== #
        super().__init__(
            master,
            fg_color="#bdac97",
            corner_radius=25,
            border_color="#9c8978",
            border_width=5
        )

        frame.pack_propagate(False)

        frame.rowconfigure(0, weight=3, uniform="a")
        frame.rowconfigure(1, weight=5, uniform="a")

        frame.columnconfigure(0, weight=1, uniform="a")
        # ===== ----- ===== #

        # ===== gui ===== #
        frame.installer = SourceInstaller(frame)

        frame.button = CTkButton(
            frame,
            text="Clone", 
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            hover_color="#eae7d9",
            border_color="#eae7d9",
            border_width=3,
            font=("JetBrains Mono Bold", 35),
            command=frame.installer.install
        )
        frame.button.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        frame.license = CTkTextbox(
            frame,
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            border_color="#eae7d9",
            border_width=3,
            font=("JetBrains Mono Medium", 10)
        )
        frame.license.insert(
            0.0,
            "MIT License\n\nCopyright (c) 2024 Aahan Salecha\n\nPermission is hereby granted, free of charge, to any\nperson obtaining a copy of this software and\nassociated documentation files (the \"Software\"), to\ndeal in the Software without restriction, including\nwithout limitation the rights to use, copy, modify,\nmerge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the\nfollowing conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial\nportions of the Software.\n\nTHE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT\nLIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO\nEVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\nFROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."
        )
        frame.license.configure(state="disabled")
        frame.license.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        # ===== --- ===== #
    # ====== ---- ====== #
# ======= ------ ======= #

# ======= binary install frame ======= #
class SourceInstaller(CTkFrame):

    # ====== init ====== #
    def __init__(installer, master: Source) -> None:
        # ===== setup ===== #
        super().__init__(
            master,
            fg_color="#bdac96",
            corner_radius=25,
            border_color="#9c8978",
            border_width=5
        )
        installer.grid_propagate(False)
        set_opacity(installer, color="#bdac97")
        # ===== ----- ===== #

        # ===== gui ===== #
        installer.rowconfigure(0, weight=1, uniform="a")
        installer.rowconfigure(1, weight=3, uniform="a")
        installer.columnconfigure(0, weight=1, uniform="a")

        installer.record = CTkTextbox(
            installer,
            fg_color="#faf8f0", 
            text_color="#988a86", 
            corner_radius=25,
            border_color="#eae7d9",
            border_width=3,
            font=("JetBrains Mono Medium", 10)
        )
        installer.record.insert(
            "0.0",
            f"\n#01 Initialize Connection\n#02 Install Assets\n#03 Install Source Code\n"
        )
        installer.record.grid(row=1, column=0, sticky="nsew", padx=19, pady=19)

        installer.progress = CTkProgressBar(
            installer,
            border_width=3,
            border_color="#eae7d9",
            fg_color="#bdac96",
            progress_color="#faf8f0",
            height=25
        )
        installer.progress.set(1)
        installer.progress.grid(row=0, column=0, sticky="new", padx=19, pady=30)
        
        installer.percent = CTkLabel(
            installer,
            fg_color="#bdac96",
            text="Progress: 100%",
            text_color="#eae7d9",
            font=("JetBrains Mono Bold", 20)
        )
        installer.percent.grid(row=0, column=0, sticky="sew", padx=19, pady=10)
        # ===== --- ===== #
    # ====== ---- ====== #

    # ====== install ====== #
    def install(installer) -> None:
        installer.grid(row=0, column=0, rowspan=3, sticky="nsew")
        installer.lift()

        # ===== move to desktop ===== #
        if path.exists(PATHS["Desktop"]+"\\the2048game"): rmtree(PATHS["Desktop"]+"\\the2048game")

        makedirs(PATHS["Desktop"]+"\\the2048game")
        rename(
            PATHS["__main__.py"], 
            PATHS["Desktop"]+"\\the2048game\\__main__.py"
        )
        # ===== ---- -- ------- ===== #

        installer.record.insert("end", "#04 Add to Desktop\n\nNOTE\nIt may take a few seconds till the code gets to\nDesktop. You may close the app.")
        installer.record.configure(state="disabled")
    # ====== ------- ====== #
# ======= ------ ------- ----- ======= #

# ======= execution ======= #
if __name__ == "__main__":
    app = App()
# ======= --------- ======= #