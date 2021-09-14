# Minesweeper

This project implements a minesweeper game using artificial intelligence , python and pygame. In this game there are 4 features -

1) User can use the left click to unreveal a cell.
2) User can use the right click to mark a cell as a mine.
3) User can use the reset button to reset the game.
4) User can use the AI button to allow the AI to make the move on his / her behalf.

The game ends when either the user clicks on a mine ( game is lost ) or he / she is able to find out all the safe cells ( game is won ).

To make an intelligent guess the AI uses prepositional logic, inference rules and its knowledge base ( made up of sentences ) to find out a safe cell for a move. If it is not able to find out such a cell then it makes a random move.

To implement this project I have used classes and pygame. The project is divided in 2 main files - runner.py and minesweeper.py. The runner.py implements
the user interface of the game and the minesweeper.py implements the logic behind the game.
