# the2048game
This is the Python clone for 2048.

## Table Of Contents
- [Status](#status)
- [Inspiration](#inspiration)
- [How To Play](#how-to-play)
- [Installation](#installation)
    - [Source Code](#source-code-recommended)
    - [Executable](#executable-not-ready)
- [Data Stored](#data-stored)
- [Requirements](#requirements)
    - [Font](#font)
    - [Modules](#modules)
        - [Only For Windows](#only-for-windows)
        - [Only For non-Windows](#only-for-non-windows)
- [Notes](#notes)
- [Commit History](#commit-history)
- [License](#license)

## Status
> [!NOTE]
> This project is in development. But the UI is ready, and you may try to run the code, if you find any error, or designing mistake, please provide feedback through a issue.

## [Inspiration](https://github.com/gabrielecirulli/2048 "2048 on GitHub")
The original 2048 was made by [Gabriele Cirulli](https://github.com/gabrielecirulli "Gabriele Cirulli's GitHub") in JavaScript and CSS. If you want to play the actual game: [`play2048.co`](https://play2048.co/ "2048 website"). 

I am attempting to make the same game in Python.

## How To Play
If you have never played 2048 before here is the rules of 2048:

> You start with either pressing `space bar` or the PLAY button.

> You have a 4x4 grid, in which there 2 blocks in the start, you have 90% chance of haing an 2, while 10% chance of having an 4 in the start.

> You can either play UP, DOWN, LEFT, or RIGHT. Each of them will result all the blocks sliding in that direction. And the blocks having the same numbers will merge, making a block that is the sum of the merged blocks.

> You win when you reach 2048.

> The game ends when you have no empty spaces left and also no moves left.

> You may even press the END button, or `esc` to clear the game, and save your score.

## Installation

### Source Code (recommended)
This requires `Python 3.10+`, atleast that's what I think.

This also requires all the [needed modules](requirements.txt requirements), for which you need to do 
> `pip install -r requirements.txt`

This will install all needed modules and libraries.

> [!TIP]
> You might even edit some things in the code to change the working flow of the code. Like the directory where the database is saved, or the color of the background, etc.

> [!WARNING]
> Some things may break when tampered with. Please edit the code with caution.

### Executable (not ready)
On Windows you can install the executable from releases. The executable is only compatible with Windows currently.

> [!CAUTION]
> It is quite slow because it is made with `PyInstaller`. If you have any suggestions, put them in [this discussion](https://github.com/aahan0511/the2048game/discussions/2 "Ideas Discussion").

## Data Stored
Your score is locally saved along with the time and the highest number you reached.
> [!NOTE]
> No other information is used, stored, or sent to us.

## Requirements

### Font
The font used is from [JetBrainsMono](https://github.com/JetBrains/JetBrainsMono "JetBrainsMono on GitHub"). I have peronally used [JetBrains Mono Medium](requirements/JetBrainsMono-Medium.ttf), which is available in the repository. You can change the font in the [`constants`](https://github.com/aahan0511/the2048game/blob/main/__main__.py#L13-L25 "constants section") section.

### Modules
[customtkinter](https://github.com/TomSchimansky/CustomTkinter) - `pip install customtkinter`

[pillow (PIL)](https://github.com/python-pillow/Pillow) - `pip install pillow`

#### Only For Windows:
[pywinstyles](https://github.com/Akascape/py-window-styles) - `pip install pywinstyles`

#### Only for non-Windows:
comment-out [`pywinstyles`](https://github.com/aahan0511/the2048game/blob/main/requirements.txt#L5) in [requirements.txt](requirements.txt), 
> [!NOTE]
> This will result in opaque and broken, winning and losing screen. If you have any suggestion to fix this on non-Windows computers, please suggest in [this discussion](https://github.com/aahan0511/the2048game/discussions/4 "Ideas Discussion").

## Notes
> [!IMPORTANT]
> If you are not on Windows, or get an error related to the `DIRECTORY`, you might need to redirect the `DIRECTORY`.
> In [`__main__.py`](__main__.py "__main__") go to the [`constants`](https://github.com/aahan0511/the2048game/blob/main/__main__.py#L13-L25 "constants section") section and change the first part of `DIRECTORY`.

## Commit History 
The [commit activity](https://github.com/aahan0511/the2048game/graphs/commit-activity) is linked here.

The [commit history](https://github.com/aahan0511/the2048game/activity) is linked here.

## License
This project has the [MIT License](https://en.wikipedia.org/wiki/MIT_License),
> MIT License

> Copyright (c) 2024 Aahan Salecha

> Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

> The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

as [LICENSE](LICENSE.txt "LICENSE file")