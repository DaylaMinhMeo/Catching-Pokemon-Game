Catching Pokemon Game
Welcome to the Catching Pokemon game project

Overview
    -Catching pokemon game is a type of game, where the player's objective is to catch pokemon in a virtual environment.
    -The goal is catch all pokemon in a pokemon ball

Installation
1. Installation dependencies
To get the Pacman game up and running on your local machine, make sure you have the following installed:
    - Python3
    - Pillow
    - Opencv
    - Mediapipe
    - Pyaudio
    - Numpy
    - Pygame
    - Sounddevice

Usage
1. How to play
    - Move the hand around the screen: Move pokemon ball to catch pokemon.
    - Objective: catch all pokemon in a pokemon ball.
    - Game over: The game ends when time runs out.

2. Gameplay Mechanic
Control
    - Hand movement: Move your hand around the screen to move the pokemon ball to catch the pokemon, close
    4 fingers outside the thumb to close the pokemon ball to catch the pokemon, touch thumb with index 
    finger to go to next button

Game elements
    - Pokemon ball: Move along the hand and close the pokemon ball to catch pokemon
    - Pokemon:pokemon will appear on screen for a period of time, it is divided by region, type and rarity

Scoring:
    - Vaporeon
    + rarity: 2
    + type: Water
    + points: 20
- Pikachu
    + rarity: 4
    + type: Land
    + points: 30
- Lighting 
    +rarity: 3
    + type: Land
    + points: 40
-Whitedragon
    + rarity: 3
    + type: Flying
    + points: 30
-Ghost
    + rarity: 1
    + type: Flying
    + points: 10

Project Structure
The project is organized into following directories and files:
    - Font: Black Ops One

Game Logic
- Pokemon ball:
    The Pokemon ball recognizes the hand through the camera and moves according to the hand.
    Move and check for collision with pokemon.
- Pokemon:
    Pokemon appear randomly depending on score and rarity and region.
    The rarer the pokemon, the faster it will disappear.

Game Elements:
- Pokemon ball
    x, y: Current position of the ball.
    x velocity, y velocity: Velocity in both directions.
    radius: Radius of the ball.
    Close.png: Image of the ball when it is closed.
    Open.png: Imange of the ball when it opens .
- Pokemon
    x, y: Current position of the ball.
    width, height: Dimensions of the Pokemon.
    radius: Bán kính của bóng.
    Vapoleon.png: Image of a pokemon in area "Water".
    Pikachu.png: Image of a pokemon in area "Land".
    Lighting.png: Image of a pokemon in area "LandLand".
    Whitedragon.png: Image of a pokemon in area "Flying".
    Ghost.png: Image of a pokemon in area "Flying".
- Scores: Current score.

Contact Information
- Trần Quang Minh - Minh.tq233971@sis.hust.edu.vnvn
- Trần Sơn Tùng - Tung.ts233986@sis.hust.edu.vn

