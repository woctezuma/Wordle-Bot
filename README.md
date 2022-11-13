# Wordle Bot [![Code Quality][codacy-image]][codacy]

This repository contains Python code to solve Wordle puzzles by maximizing entropy.

## Requirements

- Install the latest version of [Python 3.X][python-download-url].
- Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Choose the game by editing `GAME_FOLDER` in `wordle.py`:
- either `wordle/`,
- or `dungleon/`.

Specify a pre-computed first guess by editing `FIRST_GUESS` in `wordle.py`:
- choose `None` to re-compute the first guess,
- or directly use `"tares"` for Wordle,
- and `"EFCBS"` (🟡🐸💰🦇💀) for Dungleon.

Finally, run:

```bash
python wordle.py
```

Alternatively, run [`wordle-bot.ipynb`][colab-notebook]
[![Open In Colab][colab-badge]][colab-notebook]

## References

- 3Blue1Brown, [*Solving Wordle using information theory*][youtube-video], posted on Youtube on February 6, 2022,
- [`3b1b/videos`][youtube-supplementary-code]: supplementary code (in Python) accompanying the aforementioned video,
- [`GillesVandewiele/Wordle-Bot`][wordle-bot-python]: a solver (in Python) inspired by the video,
- [`TylerGlaiel/wordlebot`][wordle-bot-cpp]: a solver (in C++) which uses other approaches,
- [`woctezuma/dungleon-bot`][dungleon-bot]: the application of different solvers to [Dungleon][dungleon-rules].

<!-- Definitions -->

[codacy]: <https://www.codacy.com/gh/woctezuma/Wordle-Bot>
[codacy-image]: <https://api.codacy.com/project/badge/Grade/db464b0064aa4bde8ea084bc80f09dcf>

[python-download-url]: <https://www.python.org/downloads/>
[colab-notebook]: <https://colab.research.google.com/github/woctezuma/Wordle-Bot/blob/colab/wordle-bot.ipynb>
[colab-badge]: <https://colab.research.google.com/assets/colab-badge.svg>

[youtube-video]: <https://www.youtube.com/watch?v=v68zYyaEmEA>
[youtube-supplementary-code]: <https://github.com/3b1b/videos/tree/master/_2022/wordle>
[wordle-bot-python]: <https://github.com/GillesVandewiele/Wordle-Bot>
[wordle-bot-cpp]: <https://github.com/TylerGlaiel/wordlebot>
[dungleon-bot]: <https://github.com/woctezuma/dungleon-bot>
[dungleon-rules]: <https://github.com/woctezuma/dungleon/wiki/Rules>
