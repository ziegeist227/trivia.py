# trivia.py

A simple trivia game written in Python using the Open Trivia DB API.

## How to Play

1. Run the game by executing `python trivia.py` in your terminal.
2. Select an option from the main menu:
	* Play: Start a new game.
	* Settings: Change the question category and difficulty.
	* Exit: Quit the game.
3. Follow the instructions in the game to answer questions and keep track of your score.

## Settings

The game saves your settings in a file called `settings.json`. This file is edited in the settings menu to change the default category and difficulty.

## API

The game uses the Open Trivia DB API to fetch questions. You can find more information about the API at <https://opentdb.com/api_config.php>.