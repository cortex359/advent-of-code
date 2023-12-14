# Advent of Code solutions

<!--
![](https://img.shields.io/badge/stars%20⭐-32-yellow) ![](https://img.shields.io/badge/days%20completed-16-red)
-->

:christmas_tree: A somewhat competitive Python :snake: learning experience. :gift:

![](imgs/aoc_2023.png)

Also, check out [Rankail's 2023](https://github.com/Rankail/aoc2023) solution or
(from the previous years) [Rankail's 2022](https://github.com/Rankail/AdventOfCode), [Mickery12's 2022](https://github.com/Mickery12/Advent-of-Code), and [pblan's 2022](https://github.com/pblan/aoc) 
solution. 

For better insights into private leaderboards, see this awesome browser extension: 
[Advent of Code Charts](https://github.com/jeroenheijmans/advent-of-code-charts)

Oh, and you might want to consider [supporting Advent of Code](https://adventofcode.com/support)!

## Usage

Start new day:
```shell
./src/utils/new.zsh
```

Generate a new image with DALL·E 3 by extracting the storyline of the puzzle with GPT-3.5 and generating a visual 
description of a scene to pass along:
```shell
python src/utils/image_generation.py src/2023/day01/puzzle.md  
```


Generate some emojis (GitHub Markdown) to describe the story for use in the commit message:
```shell
cat src/2023/day01/puzzle.md | python ext/emojis.py
```
-> :snowflake: :star2: :1234: :memo: :abacus: :elf:


## Santa Hacking…
![](imgs/santa_hacking_2023.png)

See [here](imgs/README.md) for information on the images.