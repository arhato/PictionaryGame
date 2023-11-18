# PictionaryGame
A game for Assignment at School using PyQt6

Main Window

The main window serves as the central interface for the Pictionary Game. It includes the following components:
•	Drawing Canvas: The area where players can draw images using the mouse. 
•	Menu Bar: Contains menus for file operations, brush settings, game controls, and view options. 
•	Dock Widget: A dockable side panel that provides information about the game, current turn, scores, and game controls. 
•	Game Controls: Buttons for starting the game, skipping turns, moving to the next turn, showing the word, and confirming guesses.  

![image](https://github.com/arhato/PictionaryGame/assets/104602239/9aca7413-ad54-4123-b0cc-e8a4b630c69c)

The menu bar has four menus:
File, Brush Menu, Help and View.

![image](https://github.com/arhato/PictionaryGame/assets/104602239/37185846-f409-49db-b07a-eb7399dffe5f)

File Menu 

The "File" menu provides options for file-related operations. 
•	Save (Ctrl+S): Save the current drawing to a file. 
•	Clear (Ctrl+C): Clear the drawing canvas. 
•	Open (Ctrl+O): Open a previously saved drawing from a file. 
•	Exit (Esc): Exit the application.

 ![image](https://github.com/arhato/PictionaryGame/assets/104602239/9e118d77-eb88-4e82-97d1-6e3f71a41120)

Brush Menu 

The "Brush Menu" offers options related to the brush used for drawing. 
•	Brush Size (Alt+S): Opens a dialog to select the brush size. 
•	Brush Color (Alt+C): Opens a color wheel dialog to choose the brush color.

 ![image](https://github.com/arhato/PictionaryGame/assets/104602239/64cc2648-dac1-4ff7-a0cc-65da47390c87)


Brush Size Prompt provides the user with a slide to select the desired size for the brush.

![image](https://github.com/arhato/PictionaryGame/assets/104602239/aa7dd1fb-ec70-4f32-9f90-167463e4e893)

Brush color prompts the user with QColorDialog they can choose their brush color.

![image](https://github.com/arhato/PictionaryGame/assets/104602239/cfa661b7-6286-4041-9b7d-f8d504c372af)

Help Menu 

The "Help" menu offers assistance and information about the application. 
•	About (Ctrl+A): Displays information about the application, including the developer details. 
•	Help (Ctrl+H): Provides instructions and tips on using the Pictionary Game. 

View
This only has a menu to toggle the dock.

![image](https://github.com/arhato/PictionaryGame/assets/104602239/db2be7d7-189b-4d16-81e7-f5588d35704e)

Dock Widget 
The dock widget provides essential information and controls related to the game. 

•	Game Mode and Round Selection: Dropdowns for selecting the game mode (easy/hard) and the number of rounds. 
•	Current Turn Label: Indicates the player whose turn it is. Round Indicator: Displays the current round. 
•	Scores: Shows the scores of both players. 
•	Game Controls: Buttons for starting the game, skipping turns, moving to the next turn, showing the word, and confirming guesses.

The current player, round number, and the scores are updated as the game is played.

 ![image](https://github.com/arhato/PictionaryGame/assets/104602239/6e99ddaf-5c70-4ee9-8fd3-9135cf16f07c)


The user can select the mode they want to play on with the ComboBox.

![image](https://github.com/arhato/PictionaryGame/assets/104602239/37e80b52-9efc-48df-9aa3-9d3ab3d8de4e)

The user can also select the number of  rounds they want to play.

 ![image](https://github.com/arhato/PictionaryGame/assets/104602239/2cae3aae-2840-42e0-ba7c-cec906d38ee0)


Game Controls:
The game controls section includes buttons for managing the game. 
•	Start Game (Ctrl+G): Initiates or ends the game. 
•	Skip Turn (Ctrl+T): Skips the current turn. 
•	Next Turn (Ctrl+N): Advances to the next turn. 
•	Show Word (Ctrl+W): Displays the current word to the drawing player. 
•	Confirm Guess (Ctrl+Enter): Confirms the player's guess.

![image](https://github.com/arhato/PictionaryGame/assets/104602239/481bed4e-1e97-4a47-9ef4-32b3095958a6)

 
The Show Word and Guess are enabled and disabled appropriately to the turns.
