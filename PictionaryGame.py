# Name: Arrhat Maharjan
# Student ID: 3091663
# Assignment: HCI & GUI Programming Assignment 2

import csv
import random
import sys

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon, QPainter, QPen, QAction, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QDockWidget, QPushButton, QVBoxLayout, \
    QLabel, QMessageBox, QColorDialog, QSlider, QDialog, QLineEdit, QComboBox


class PictionaryGame(QMainWindow):  # documentation https://doc.qt.io/qt-6/qwidget.html
    '''
    Painting Application class
    '''

    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("Pictionary Game")

        # set the windows dimensions
        top = 200
        left = 200
        width = 800
        height = 600
        self.setGeometry(top, left, width, height)

        # set the icon
        # windows version
        self.setWindowIcon(
            QIcon("./icons/paint-brush.png"))  # documentation: https://doc.qt.io/qt-6/qwidget.html#windowIcon-prop
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap("./icons/paint-brush.png")))

        # image settings (default)
        self.image = QPixmap("./icons/canvas.png")  # documentation: https://doc.qt.io/qt-6/qpixmap.html
        self.image.fill(Qt.GlobalColor.white)  # documentation: https://doc.qt.io/qt-6/qpixmap.html#fill
        mainWidget = QWidget()
        mainWidget.setMaximumWidth(300)

        # default
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black  # documentation: https://doc.qt.io/qt-6/qt.html#GlobalColor-enum
        self.user_guess = ""
        self.gameStarted = False  # initialize to indicate whether the game has started
        self.currentWord = ""
        self.nextIndicator = False
        self.showWordIndicator = True
        self.modeInput = "easy"
        self.roundInput = 5
        self.currentRound = 0

        # reference to last point recorded by mouse
        self.lastPoint = QPoint()  # documentation: https://doc.qt.io/qt-6/qpoint.html

        # set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(
            " File")  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        brushMenu = mainMenu.addMenu("Brush Menu")  # add the "Brush Size" menu to the menu bar
        helpMenu = mainMenu.addMenu("Help")

        # save menu item
        saveAction = QAction(QIcon("./icons/save.png"), "Save",
                             self)  # create a save action with a png as an icon, documentation: https://doc.qt.io/qt-6/qaction.html
        saveAction.setShortcut(
            "Ctrl+S")  # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-6/qaction.html#shortcut-prop
        fileMenu.addAction(
            saveAction)  # add the save action to the file menu, documentation: https://doc.qt.io/qt-6/qwidget.html#addAction
        saveAction.triggered.connect(
            self.save)  # when the menu option is selected or the shortcut is used the save slot is triggered, documentation: https://doc.qt.io/qt-6/qaction.html#triggered

        # clear
        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)  # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")  # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)  # add this action to the file menu
        clearAction.triggered.connect(
            self.clear)  # when the menu option is selected or the shortcut is used the clear slot is triggered

        # open
        openAction = QAction(QIcon("./icons/open.png"), "Open", self)
        openAction.setShortcut("Ctrl+O")
        fileMenu.addAction(openAction)
        openAction.triggered.connect(self.open)

        # exit
        exitAction = QAction(QIcon("./icons/exit.png"), "Exit", self)
        exitAction.setShortcut("Esc")
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exit)

        # about
        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+A")
        helpMenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.about)

        # help
        helpAction = QAction(QIcon("./icons/help.png"), "Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)

        # brush size
        brushSize_subMenu = QAction(QIcon("./icons/brushsize.png"), "Brush Size", self)
        brushSize_subMenu.setShortcut("Alt+S")
        brushMenu.addAction(brushSize_subMenu)
        brushSize_subMenu.triggered.connect(self.showBrushSizeDialog)

        # brush color
        brushColor_subMenu = QAction(QIcon("./icons/brushcolor.png"), "Brush Color", self)
        brushColor_subMenu.setShortcut("Alt+C")
        brushMenu.addAction(brushColor_subMenu)
        brushColor_subMenu.triggered.connect(self.showColorWheel)

        # menu option to show/hide the dock
        viewMenu = mainMenu.addMenu("View")
        self.toggleDockAction = QAction("Dock", self)
        self.toggleDockAction.setShortcut("Ctrl+D")
        self.toggleDockAction.setCheckable(True)
        self.toggleDockAction.setChecked(True)
        self.toggleDockAction.triggered.connect(self.toggleDock)
        viewMenu.addAction(self.toggleDockAction)

        # Add game-related variables
        self.currentPlayer = 1  # 1 or 2 indicating the current player
        self.scores = {'Player 1': 0, 'Player 2': 0}
        self.currentTurnLabel = QLabel(f"Current Turn: Player {self.currentPlayer}")
        self.roundIndicator = QLabel("Round:")
        self.scoresLabel = QLabel("Scores:")
        self.player1ScoreLabel = QLabel("Player 1: 0")
        self.player2ScoreLabel = QLabel("Player 2: 0")

        # Add game controls
        self.startGameButton = QPushButton("Start Game")
        self.startGameButton.setShortcut("Ctrl+G")
        self.startGameButton.clicked.connect(self.startGame)

        self.skipTurnButton = QPushButton("Skip Turn")
        self.skipTurnButton.setShortcut("Ctrl+T")
        self.skipTurnButton.clicked.connect(self.skipTurn)

        self.nextTurnButton = QPushButton("Next Turn")
        self.nextTurnButton.setShortcut("Ctrl+N")
        self.nextTurnButton.clicked.connect(self.nextTurn)
        self.nextTurnButton.setEnabled(False)

        self.showWordButton = QPushButton("Show Word")
        self.showWordButton.setShortcut("Ctrl+W")
        self.showWordButton.clicked.connect(self.showWord)

        self.confirmGuessButton = QPushButton("Guess")
        self.confirmGuessButton.setShortcut("Ctrl+Enter")
        self.confirmGuessButton.clicked.connect(self.confirmGuess)
        self.confirmGuessButton.setEnabled(self.nextIndicator)

        self.modeSelection = QComboBox()
        self.modeSelection.addItems(["Select a mode", "Easy", "Hard"])
        self.modeSelection.setCurrentIndex(0)
        self.modeSelection.activated.connect(self.getMode)
        self.modeSelectionEnabled = True

        self.roundSelection = QComboBox()
        self.roundSelection.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        self.roundSelection.setCurrentIndex(4)
        self.roundSelection.activated.connect(self.getRound)
        self.roundSelectionEnabled = True

        # Add layout for game controls
        gameControlsLayout = QVBoxLayout()
        gameControlsLayout.addWidget(self.startGameButton)
        gameControlsLayout.addWidget(self.skipTurnButton)
        gameControlsLayout.addWidget(self.nextTurnButton)
        gameControlsLayout.addWidget(self.showWordButton)
        gameControlsLayout.addWidget(self.confirmGuessButton)

        # Side Dock
        self.dockInfo = QDockWidget()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockInfo)
        self.dockInfo.visibilityChanged.connect(self.updateDockCheckState)

        # widget inside the Dock
        playerInfo = QWidget()
        self.vbdock = QVBoxLayout()
        playerInfo.setLayout(self.vbdock)
        playerInfo.setMaximumSize(150, self.height())
        # add controls to custom widget
        self.vbdock.addWidget(self.modeSelection)
        self.vbdock.addWidget(self.roundSelection)
        self.vbdock.addWidget(self.currentTurnLabel)
        self.vbdock.addSpacing(10)
        self.vbdock.addWidget(self.roundIndicator)
        self.vbdock.addWidget(self.scoresLabel)
        self.vbdock.addWidget(self.player1ScoreLabel)
        self.vbdock.addWidget(self.player2ScoreLabel)
        self.vbdock.addLayout(gameControlsLayout)

        # Setting colour of dock to gray
        playerInfo.setAutoFillBackground(True)
        p = playerInfo.palette()
        p.setColor(playerInfo.backgroundRole(), Qt.GlobalColor.gray)
        playerInfo.setPalette(p)

        # set widget for dock
        self.dockInfo.setWidget(playerInfo)

    # Get the selected round from the dropdown
    def getRound(self):
        if self.roundSelectionEnabled:
            selectedRound = self.roundSelection.currentText()
            if selectedRound.isnumeric():
                self.roundInput = int(selectedRound)

    # Get the selected mode from the dropdown
    def getMode(self):
        if self.modeSelectionEnabled:
            self.modeInput = self.modeSelection.currentText().lower()
            self.getList(self.modeInput)

    # Toggle the dock
    def toggleDock(self):
        self.dockInfo.setVisible(not self.dockInfo.isVisible())

    # Update the dock check state
    def updateDockCheckState(self):
        self.toggleDockAction.setChecked(self.dockInfo.isVisible())

    # Show the brush size dialog
    def showBrushSizeDialog(self):
        # Create a dialog to display brush size options
        self.brushSizeDialog = QDialog(self)
        self.brushSizeDialog.setWindowTitle("Select Brush Size")

        # Create a slider for brush size
        self.brushSizeSlider = QSlider(Qt.Orientation.Horizontal)
        self.brushSizeSlider.setMinimum(1)
        self.brushSizeSlider.setMaximum(100)
        self.brushSizeSlider.setValue(self.brushSize)  # Set the initial value to the current brush size
        self.brushSizeSlider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.brushSizeSlider.setTickInterval(5)

        # Create a label to display the selected brush size
        self.sizeLabel = QLabel(f"Brush Size: {self.brushSize}")

        # Update the brush size when the slider value changes
        self.brushSizeSlider.valueChanged.connect(self.update_size_label)

        # Create a button to apply the selected brush size
        self.applyButton = QPushButton("Apply")
        self.applyButton.clicked.connect(lambda: self.updateBrushSize(self.brushSizeSlider.value()))

        # Create a layout for the dialog
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.brushSizeSlider)
        self.layout.addWidget(self.sizeLabel)
        self.layout.addWidget(self.applyButton)

        # Set the layout for the dialog
        self.brushSizeDialog.setLayout(self.layout)

        # Show the dialog
        self.brushSizeDialog.exec()

    # Update the brush size label
    def update_size_label(self, value):
        self.sizeLabel.setText(f"Brush Size: {value}")

    # Update the brush size
    def updateBrushSize(self, value):
        self.brushSize = value
        self.brushSizeDialog.accept()

    # Show the color wheel
    def showColorWheel(self):
        color = QColorDialog.getColor(initial=self.brushColor, parent=self)
        if color.isValid():
            self.brushColor = color

    # event handlers
    def mousePressEvent(self,
                        event):  # when the mouse is pressed, documentation: https://doc.qt.io/qt-6/qwidget.html#mousePressEvent
        if self.gameStarted and event.button() == Qt.MouseButton.LeftButton:  # if the pressed button is the left button
            self.drawing = True  # enter drawing mode
            self.lastPoint = event.pos()  # save the location of the mouse press as the lastPoint
            print(self.lastPoint)  # print the lastPoint for debugging purposes

    def mouseMoveEvent(self,
                       event):  # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-6/qwidget.html#mouseMoveEvent
        if self.drawing:
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-6/qpen.html
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                                Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.lastPoint,
                             event.pos())  # draw a line from the point of the orginal press to the point to where the mouse was dragged to
            self.lastPoint = event.pos()  # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
            self.update()  # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(self,
                          event):  # when the mouse is released, documentation: https://doc.qt.io/qt-6/qwidget.html#mouseReleaseEvent
        if event.button() == Qt.MouseButton.LeftButton:  # if the released button is the left button, documentation: https://doc.qt.io/qt-6/qt.html#MouseButton-enum ,
            self.drawing = False  # exit drawing mode

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(
            self)  # create a new QPainter object, documentation: https://doc.qt.io/qt-6/qpainter.html
        canvasPainter.drawPixmap(QPoint(),
                                 self.image)  # draw the image , documentation: https://doc.qt.io/qt-6/qpainter.html#drawImage-1

    # resize event - this function is called
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.image.save(filePath)  # save file image to the file path

    def clear(self):
        self.image.fill(
            Qt.GlobalColor.white)  # fill the image with white, documentation: https://doc.qt.io/qt-6/qimage.html#fill-2
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    # About and Help functions
    def about(self):
        exit_msg = QMessageBox()
        exit_msg.setIcon(QMessageBox.Icon.Information)
        exit_msg.setText(
            "Pictionary Game\n\n"
            "This is a Pictionary Game developed for the HCI & GUI Programming Assignment.\n"
            "It allows players to draw and guess words in a turn-based manner.\n\n"
            "Developed by: Arrhat Maharjan\n"
            "Student ID: 3091663\n"
            "Assignment: HCI & GUI Programming Assignment 2")
        exit_msg.setWindowTitle("About Prompt")
        exit_msg.setWindowIcon(QIcon("./icons/paint-brush.png"))
        exit_msg.setStandardButtons(QMessageBox.StandardButton.Close)
        reply = exit_msg.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

    def help(self):
        exit_msg = QMessageBox()
        exit_msg.setIcon(QMessageBox.Icon.Information)
        exit_msg.setText(
            "Pictionary Game Help\n\n"
            "1. Start the Game: Click 'Start Game' to begin the Pictionary game.\n"
            "2. Drawing: Use the left mouse button to draw on the canvas.\n"
            "3. Brush Size: Adjust the brush size from the 'Brush Menu'.\n"
            "4. Brush Color: Change the brush color from the 'Brush Menu'.\n"
            "5. Save/Load: Use 'Save' and 'Open' from the 'File' menu to save/load your drawing.\n"
            "6. Guessing: Enter your guess and click 'Guess' to confirm.\n"
            "7. Rounds: Select the number of rounds and game mode before starting.\n"
            "8. Help/About: Find more information about the game in the 'Help' and 'About' sections.")
        exit_msg.setWindowTitle("Help Prompt")
        exit_msg.setWindowIcon(QIcon("./icons/paint-brush.png"))
        exit_msg.setStandardButtons(QMessageBox.StandardButton.Close)
        reply = exit_msg.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

    # Get a random word from the list read from file
    def getWord(self):
        randomWord = random.choice(self.wordList)
        print(randomWord)
        return randomWord

    # read word list from file
    def getList(self, mode):
        with open(mode + 'mode.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # print(row)
                self.wordList = row
                line_count += 1
            # print(f'Processed {line_count} lines.')

    # open a file
    def open(self):
        '''
        This is an additional function which is not part of the tutorial. It will allow you to:
         - open a file dialog box,
         - filter the list of files according to file extension
         - set the QImage of your application (self.image) to a scaled version of the file)
         - update the widget
        '''
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if not file is selected exit
            return
        with open(filePath, 'rb') as f:  # open the file in binary mode for reading
            content = f.read()  # read the file
        self.image.loadFromData(content)  # load the data into the file
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)  # scale the image from file and put it in your QImage
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    # exit
    def exit(self):
        # Prompt the user to confirm if they want to exit the application
        exit_msg = QMessageBox()
        exit_msg.setIcon(QMessageBox.Icon.Information)
        exit_msg.setText('Are you sure?')
        exit_msg.setWindowTitle("Exit Prompt")
        exit_msg.setWindowIcon(QIcon("./icons/paint-brush.png"))
        exit_msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        reply = exit_msg.exec()
        if reply == QMessageBox.StandardButton.Yes:
            window.close()
        elif reply == QMessageBox.StandardButton.Cancel:
            pass

    # Start the game
    def startGame(self):
        if self.gameStarted:
            if self.roundInput == 0:
                # Game is already started, end the game
                winner = max(self.scores, key=self.scores.get)  # Get the winner based on scores
                self.showWinnerPrompt(winner)
                self.gameStarted = False
                self.startGameButton.setText("Start Game")
                self.clear()
                self.currentWord = ""
                self.updateGameInfo()
                self.roundSelection.setEnabled(True)
                self.modeSelection.setEnabled(True)
        else:
            # Check if a mode is selected before starting the game
            if self.modeSelection.currentIndex() == 0:
                # Show an alert if no mode is selected
                QMessageBox.warning(self, "Alert", "Please select a game mode before starting the game.")
            else:
                # Start the game
                self.gameStarted = True
                self.startGameButton.setText("End Game")
                self.currentPlayer = 1
                self.scores = {'Player 1': 0, 'Player 2': 0}
                self.currentWord = self.getWord()
                self.showWord()
                self.updateGameInfo()
                self.nextTurnButton.setEnabled(True)
                self.roundSelection.setEnabled(False)
                self.modeSelection.setEnabled(False)

    # Show the winner prompt
    def showWinnerPrompt(self, winner):
        QMessageBox.information(self, "Game Over", f'Player {winner} wins the game!', QMessageBox.StandardButton.Ok)

    # Skip the current turn
    def skipTurn(self):
        self.showWordIndicator = True
        self.confirmGuessButton.setEnabled(self.nextIndicator)
        self.currentPlayer = 3 - self.currentPlayer  # Toggle between player 1 and player 2
        self.currentRound += 1
        self.updateGameInfo()

    # Go to the next turn
    def nextTurn(self):
        self.nextIndicator = True
        self.showWordIndicator = False
        self.confirmGuessButton.setEnabled(self.nextIndicator)
        self.showWordButton.setEnabled(self.showWordIndicator)
        self.currentPlayer = 3 - self.currentPlayer  # Toggle between player 1 and player 2
        self.showWordIndicator = True
        self.updateGameInfo()

    # End the game
    def endGame(self):
        if not self.gameStarted:
            return
        winner = max(self.scores, key=self.scores.get)
        self.showWinnerPrompt(winner)
        self.gameStarted = False
        self.startGameButton.setText("Start Game")
        self.clear()
        self.currentWord = ""
        self.updateGameInfo()
        self.roundSelection.setEnabled(True)
        self.modeSelection.setEnabled(True)

    # Show the word
    def showWord(self):
        wordDialog = QMessageBox(self)
        wordDialog.setIcon(QMessageBox.Icon.Information)
        if self.showWordIndicator:
            wordDialog.setText(f'The word is: {self.currentWord}')
        else:
            wordDialog.setText(f'Player {self.currentPlayer}, it\'s your turn!')
        wordDialog.setWindowTitle("Word Prompt")
        wordDialog.setWindowIcon(QIcon("./icons/paint-brush.png"))
        wordDialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        wordDialog.exec()

    # Confirm the user's guess
    def confirmGuess(self):
        wordDialog = QMessageBox(self)
        wordDialog.setIcon(QMessageBox.Icon.Information)
        wordDialog.setText("Enter your guess.")

        # Add a QLineEdit for the user to input their guess
        guess_input = QLineEdit(wordDialog)
        wordDialog.layout().addWidget(guess_input)

        wordDialog.setWindowTitle("Guess Prompt")
        wordDialog.setWindowIcon(QIcon("./icons/paint-brush.png"))

        wordDialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        result = wordDialog.exec()

        if result == QMessageBox.StandardButton.Ok:
            # Retrieve the user's guess from the QLineEdit
            self.user_guess = guess_input.text()

        if not self.user_guess:
            self.user_guess = "No guess"

        # Check if the user's guess is correct
        if ''.join(self.user_guess.split()).lower() == ''.join(self.currentWord.split()).lower():
            self.scores[f'Player {self.currentPlayer}'] += 1
            self.scores[f'Player {3 - self.currentPlayer}'] += 2

        self.currentRound += 1

        # Check if the game has ended
        if self.currentRound / 2 >= self.roundInput:
            self.endGame()
        else:
            self.currentWord = self.getWord()
            self.showWordIndicator = True
            self.confirmGuessButton.setEnabled(False)
            self.showWordButton.setEnabled(self.showWordIndicator)
            self.updateGameInfo()
            self.showWord()

    # Update the game info
    def updateGameInfo(self):
        self.currentTurnLabel.setText(f"Current Turn: Player {self.currentPlayer}")
        self.roundIndicator.setText(f"Round: {self.currentRound}")
        self.player1ScoreLabel.setText(f"Player 1: {self.scores['Player 1']}")
        self.player2ScoreLabel.setText(f"Player 2: {self.scores['Player 2']}")
        if self.currentRound / 2 >= self.roundInput:
            self.endGame()


# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PictionaryGame()
    window.show()
    app.exec()  # start the event loop running
