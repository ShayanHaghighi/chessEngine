# Chess Engine with GUI in Pygame

This project is a chess engine implemented in Python using the `python-chess` library for the chess logic and `pygame` for the graphical user interface (GUI). The engine supports features like iterative deepening, transposition tables, and move ordering.

## Features

- Complete chess game implementation with GUI built with Pygame 
- Chess engine using minimax algorithm with alpha-beta pruning
- Iterative deepening for time management
- Transposition tables to avoid redundant calculations
- Move ordering to improve search efficiency

## Installation

To get started with the project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/ShayanHaghighi/chessEngine.git
cd chessEngine
pip install -r requirements.txt
```
### Requirements
```
    Python 3.7+
    Pygame
    python-chess
```
### Usage

To run the chess engine with the GUI, simply execute the chessMain.py file:

```bash
python chessMain.py
```

You can change which players are controlled by the chess engine by changing the `IS_WHITE_AI` and `IS_BLACK_AI` variables on line 15-16 of the `chessMain.py` file.
(Alternatively running `python chessGame.py` will run the game with 2 human players)


## How It Works

### Minimax Algorithm with Alpha-Beta Pruning

The engine uses the minimax algorithm to evaluate the best move. Alpha-beta pruning is implemented to optimize the search by eliminating branches that don't need to be explored.
### Iterative Deepening

Iterative deepening is used to progressively deepen the search, ensuring that the engine can return a move even if the allocated time runs out.

### Transposition Tables

Transposition tables store evaluations of previously encountered positions, reducing redundant calculations and speeding up the search.

### Move Ordering

Moves are ordered to improve the efficiency of alpha-beta pruning. Captures and checks are prioritized to be evaluated first.

## License

This project is licensed under the MIT License. See the [LICENSE file](https://github.com/ShayanHaghighi/chessEngine/blob/main/LICENSE) for details.

## Contact

For any questions or suggestions, feel free to [open an issue](https://github.com/ShayanHaghighi/chessEngine/issues/new) (keep in mind this project is not yet finished).

Happy coding