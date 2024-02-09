# Conway's Game Of Life

## Description

This is a simple implementation of the Game of Life in Python. The Game of Life is a cellular automaton devised by the British mathematician John Horton Conway in 1970. It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves.

It is played on a 2D square grid. Each square (or "cell") on the grid can be either alive or dead, and they evolve according to the following rules:

- Any live cell with fewer than two live neighbours dies (referred to as underpopulation).
- Any live cell with more than three live neighbours dies (referred to as overpopulation).
- Any live cell with two or three live neighbours lives, unchanged, to the next generation.
- Any dead cell with exactly three live neighbours comes to life.

## Requirements

To run this simulation, you'll need:

- Python 3.x
- Pygame library

You can install Pygame using pip:

```bash
pip install pygame
```

## How to Run

1. Ensure Python and Pygame are installed on your system.
2. Save the script in a file, for example, `game_of_life.py`.
3. Run the script from your terminal or command prompt:

```bash
python game_of_life.py
```

## Controls

- **Left Click**: Make a cell alive.
- **Right Click**: Clear a cell (make it dead).
- **Enter**: Play the simulation.
- **P**: Pause the simulation.
- **Space**: Toggle Play/Pause.
- **C**: Clear the grid and pause the simulation.
- **G**: Generate random cells.

## References

- [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
- [ConwayLife.com](https://conwaylife.com/)

## Acknowledgements

Thanks to [TechWithTim](https://www.youtube.com/@TechWithTim) for the inspiration and the tutorial on which this project is based.
