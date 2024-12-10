# the2048game
This is the Python clone for 2048.

## Table Of Contents
- [Status](#status)
    - [Bugs](#bugs)
    - [Not Ready Features](#not-ready-features)
- [Inspiration](#inspiration)
- [How To Play](#how-to-play)
- [Installation](#installation)
    - [Source Code](#source-code-recommended)
    - [ZIP File](#zip-file)
- [Security](#security)
- [Requirements](#requirements)
    - [Font](#font)
    - [Modules](#modules)
- [Rate](#rate)
- [Commit History](#commit-history)
- [License](#license)

## Status
> [!NOTE]
> The project is not production ready, but is functional. Some functions are not yet ready. See [v0.2.0-alpha](https://github.com/aahan0511/the2048game/releases/tag/v0.2.0-alpha) for the current release.

> [!IMPORTANT]
> **the2048game** is currently only for windows, it may work for other operating systems after some changes, but it may not work as intended.

### Bugs

> [!IMPORTANT]
> If you get an error related to tables in sqlite3, or related to assets, run the [`setup.py`](setup.py) again, this will refresh your database and assets.
> This ussually happens due to version change.

> [!TIP]
> If you find a bug, you may create an issue.

### Not Ready Features

#### Help ❔
> The help button [❔], is not ready. It should show How To Play instructions.

#### Undo 🔙
> The undo button [🔙], is not ready. It will go back one move.

#### Hint 💡
> The hint button [💡], is not ready. It will show a suggested move.

#### Settings ⚙️
> The settings button [⚙️], is not ready. It will show a settings page.

#### Slide Animation
> The sliding animation, is not ready.

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

Run [`setup.py`](setup.py), or get latest [`setup.exe`](binary/setup.exe) (from the release, or in the binary folder).

Running it will give you the options to install the app, or source code.
This way is the most recommended as it installs the assets, fonts, etc.

## Security
Your score is locally saved along with the time and the highest number you reached. You may even enter your name, which is optional.

See [SECURITY.md](SECURITY.md) for more information.

## Requirements

Installing the app using setup will install all nessecary requirements.

### Font
The font used is from [JetBrainsMono](https://github.com/JetBrains/JetBrainsMono "JetBrainsMono on GitHub"). I have peronally used [JetBrains Mono Medium](requirements/JetBrainsMono-Medium.ttf), which is available in the repository. You can change the font in the [`constants`](https://github.com/aahan0511/the2048game/blob/d62a9709354e9c1dd00bc62e517f4d0a6e2a3fc8/__main__.py#L14-L26 "constants section") section.

### Modules
> `pip install -r requirements.txt`

[customtkinter](https://github.com/TomSchimansky/CustomTkinter) - `pip install customtkinter`

[pillow (PIL)](https://github.com/python-pillow/Pillow) - `pip install pillow`

[CTkTable](https://github.com/Akascape/CTkTable) - `pip install CTkTable`

[pywinstyles](https://github.com/Akascape/py-window-styles) - `pip install pywinstyles`

[pyglet](https://github.com/pyglet/pyglet) - `pip install pyglet`

## Rate
How would you rate this game?
[Rate Here](https://github.com/aahan0511/the2048game/discussions/5 "Rating Discussion")

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
