# the2048game
This is the Python version for 2048 by Gabriele Cirulli.

## Status
> [!NOTE]
> This project is in development. Do not try to run it.

## [2048](https://github.com/gabrielecirulli/2048 "2048 on GitHub")
The original 2048 was made by [Gabriele Cirulli](https://github.com/gabrielecirulli "Gabriele Cirulli's GitHub") in JavaScript and CSS. If you want to play the actual game: [`play2048.co`](https://play2048.co/ "2048 website"). 

I am attempting to make the same game in Python.

## How To Play
If you have never played 2048 before here is the rules of 2048:

> You have a 4x4 grid, in which there 2 blocks in the start, you have 90% chance of haing an 2, while 10% chance of having an 4 in the start.

> You can either play UP (⬆️), DOWN (⬇️), LEFT (⬅️), or RIGHT (➡️). Each of them will result all the blocks sliding in that direction. And the blocks having the same numbers will merge, making a block that is the sum of the merged blocks.

> You win when you reach 2048.

> The game ends when you have no empty spaces left and also no moves left.

## Installation

### Source Code (recommended)
This requires `Python 3.10+`, atleast that's what I think.

This also requires all the [needed modules](requirements.txt requirements), for which you need to do 
> `pip install -r requirements.txt`

This will install all needed modules and libraries.

> [!TIP]
> You might even need to edit some things in the code to change the working flow of the code. Like the directory where the database is saved, or the color of the background, etc.

### Executable
On Windows you can install the executable from releases. The executable is only compatible with Windows currently, and is quite slow because it is made with `PyInstaller`. If you have any suggestions, put them in [this discussion](https://github.com/aahan0511/the2048game/discussions/2 "Ideas Discussion").

## High Score
Your score is locally saved along with the time and the highest number you reached.

## Font
The font used is from [JetBrainsMono](https://github.com/JetBrains/JetBrainsMono "JetBrainsMono on GitHub"). I have peronally used [JetBrains Mono Medium](requirements/JetBrainsMono-Medium.ttf), which is available in the repository. You can change the font in the `constants` section.

## Notes
> [!WARNING]
> If you are not on Windows, or get an error related to the `DIRECTORY`, you might need to redirect the `DIRECTORY`.
> In [`__main__.py`](__main__.py "__main__") go to the `constants` section and change the first part of `DIRECTORY`.

## License
This project has the [MIT License](https://en.wikipedia.org/wiki/MIT_License), as [LICENSE](LICENSE.txt "LICENSE file")

## Credit and Thanks

### [Clear Code](https://github.com/clear-code-projects "Clear Code's GitHub")
I took his course [`Learn Python by creating 10 apps with tkinter`](https://www.udemy.com/course/learn-python-by-creating-10-apps/), and it was super helpful in making this project.

### [Aarav-S2005](https://github.com/Aarav-S2005 "Aarav-S2005's GitHub")
He was the one who gave me the idea to do a competition who makes a better 2048 clone. Here is his [repository](https://github.com/Aarav-S2005/The2048Game "The2048Game by Aarav-S2005").
