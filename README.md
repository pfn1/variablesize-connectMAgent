
# ConnectM Game

## Overview
ConnectM is a Python-based implementation of the Connect M game, where two players take turns dropping colored discs into a grid of columns and rows. The objective is to connect M discs of the same color contiguously across the rows, columns, or diagonals. The first player to achieve this goal wins the game. If the grid fills up without either player winning, the game ends in a draw.

This project implements the ConnectM game using adversarial search techniques, specifically min-max with alpha-beta pruning, to enable the computer player to make intelligent moves against the human player.

## Features
- Single-player game: Play against the computer.
- Customizable grid size and number of discs to connect (M).
- Alpha-beta pruning algorithm for efficient decision-making by the computer player.
- Text-based visualization of the game board.
- Input validation to ensure a fair and valid game.

## Getting Started
1. Clone the repository to your local machine.
2. Ensure you have Python installed on your system.
3. Run the ConnectM game with the following command:
    ```

   (LINUX)
   python3 connectM.py N M H  - Tested on WSL

   python connectM.py N M H  - try if above does not work
    
   (MAC)
   python3 connectM.py N M H

   (WINDOWS)
   py .\connectM.py N M H - not tried


    ```
    - `N`: Size of the grid (N x N). Should be at least 3 and no larger than 10.
    - `M`: Number of discs to connect contiguously. Must be higher than one but not higher than N.
    - `H`: Flag indicating if the human (1) or computer (0) makes the first move.

## Gameplay Instructions
1. When prompted, enter the column number where you want to drop your disc.
2. The game alternates between the human and computer players until a winning move is made or the game ends in a draw.
3. Enjoy the game and have fun!

## Sample Command
    python3 connectM.py 5 3 1

NOTE: See Getting Started section above for OS specific commands to try if an issue is encountered.

## This command starts a game on a 5x5 grid, where players need to connect 3 discs in a row, and the human player makes the first move.

## Credits
This project is developed by Paul Negrido and Landon Caraway for Dr. Reichherzer's CAP4601 Intro to AI class.
