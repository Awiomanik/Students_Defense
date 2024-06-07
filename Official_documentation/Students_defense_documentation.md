### Student Defense Game Documentation

#### 1. Game Startup Instructions

##### 1.1 Required Libraries
To run the game, the following libraries need to be installed:
- `pygame`
- `os`
- `typing`


##### 1.2 Running the Prototype
To run the prototype please run the following command in the root directory of the repository:
python PROTOTYPE.py
(Make sure you are in the Students_Defense directory containning PROTOTYPE.py file.)

#### 2. User Guide
The game begins by pressing the "Play" button on the main screen. Then, press the "Buy Tower" button in the bottom right corner to place towers that will defend against enemies. You can do that as long as the button is green(while you are buying towers the amount of gold is decreasing). You can place these towers only on the grass (you can't place it on a tree for example) After placing the towers, press the "Start wave" button to make the first enemies appear and move along the path from the left side of the map. The enemies have a number of lives displayed next to them. A red star briefly appears next to an enemy that has taken damage. When this number of lives reaches 0 as a result of tower attacks, the enemies disappear. At the moment there are only 3 waves of the enemies. Right now the player doesn't lose anything if the enemy comes to an end of the path (but it is going to be changed in the finished product). If you want to come back to the menu you can press the "Exit" botton.

#### 3. UML diagrams are in file named "UML_STUDENTS_DEFENSE"

#### 4. Updated Action Plan for Subsequent Weeks of Work
- Implementing basic game mechanics, including UI drawing, enemy movement, tower attacks, and creating 2 thematic maps.
- Adding advanced features such as 3 different types of enemies with different power variants (student, engineer, master), 2 special enemies (bosses), 3 towers with upgrade options.
- Testing and optimizing code to ensure smooth and error-free gameplay (it contains - among other things - replacing some atributes by static methods, it may cause changes in UML diagrams).

#### 5. Updated Feature Plan for the Completed Application

- **Basic Features:**
  - Adding enemy waves.
  - Adding options such as the player losing live when enemies reach the end of the path
  - Adding the ability to enter the player's nickname
  - Managing towers and attacking enemies.
  - Loading and displaying maps.

- **Advanced Features (as time permits):**
  - Various types of towers and enemies.
  - Special tower abilities.
  - Different difficulty levels and diverse maps.
 
- **User Interface:**
  - Intuitive interface for managing the game.
  - Health, point, and resource indicators.