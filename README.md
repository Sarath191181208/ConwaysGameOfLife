# Conways Game Of life

A game with simple rules founded by **Jhon Horton Conway**. Altough a simple game it is discussed that has a possibilty to solve every existing problem.

Read more on Wikipedia : https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

# Description

It has namely four rules:

- Any live cell with **fewer than two live neighbours dies**, as if by underpopulation.
- Any live cell with **two or three live neighbours lives** on to the next generation.
- Any live cell with **more than three live neighbours dies**, as if by overpopulation.
- Any **dead cell with exactly three live neighbours becomes a live cell**, as if by reproduction.

It is a simple yet a complex simulation representing life itself. Intruged by it's properties I tried a simple simulation.

## Demo

![Image](https://github.com/Sarath191181208/ConwaysGameOfLife/blob/master/images/Screenshot.png)

## Features

- A **Create button** to creates a random board.
- A **Clear button** to totally clear the board.
- A **Start button** to start the visualization.
- **Save/Load** Features.

## Run Locally

Clone the project

```bash
  git clone https://github.com/Sarath191181208/ConwaysGameOfLife.git
```

Go to the project directory

```bash
  cd ./ConwaysGameOfLife
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Run the project Locally

```bash
  python main.py
```

## References

Wikipedia : https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

Coding Train : https://www.youtube.com/watch?v=FWSR_7kZuYg

## Usage

- **Right click to delete the block.**
- Left click to insert.
- All the buttons are explained in features section.

## Hot keys

- SPACE : Start visualization
- C : Clear
- S : Save
- O : Load
- R : Random Board

## Requirements

- python `Make sure to add to path`
- pygame `pip install pygame`
- pygame_gui `pip install pygame_gui`
