#!/usr/bin/env python
'''
Julian Engel
jse13
'''

from __future__ import print_function
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import os
import sys
import cPickle as pickle
import random
import enchant
import logging
from datetime import datetime

logging.basicConfig(level=logging.ERROR)


dice = (['A', 'E', 'A', 'N', 'E', 'G'],
        ['A', 'H', 'S', 'P', 'C', 'O'],
        ['A', 'S', 'P', 'F', 'F', 'K'],
        ['O', 'B', 'J', 'O', 'A', 'B'],
        ['I', 'O', 'T', 'M', 'U', 'K'],
        ['R', 'Y', 'V', 'D', 'E', 'L'],
        ['L', 'R', 'E', 'I', 'X', 'D'],
        ['E', 'I', 'U', 'N', 'E', 'S'],
        ['W', 'N', 'G', 'E', 'E', 'H'],
        ['L', 'N', 'H', 'N', 'R', 'Z'],
        ['T', 'S', 'T', 'I', 'Y', 'D'],
        ['O', 'W', 'T', 'O', 'A', 'T'],
        ['E', 'R', 'T', 'T', 'Y', 'L'],
        ['T', 'O', 'E', 'S', 'S', 'I'],
        ['T', 'E', 'R', 'W', 'H', 'V'],
        ['N', 'U', 'I', 'H', 'M', 'Qu'])


def rollDice():
    #Pick a random character from each dice
    rolledDice = [x[random.randint(0, 5)] for x in dice]

    #Shuffle the chosen characters
    random.shuffle(rolledDice)

    #Split into sublists of 4 elements for the grid
    rolledDice = [rolledDice[i:i+4] for i in range(0, 16, 4)]


    return rolledDice


def gradeWords(dice, words):

    score = 0
    wordSet = set() #For detecting duplicate words
    d = enchant.Dict("en_US")
    setinel = True

    for w in words:
        currentWordLength = len(w)
        w = w.upper()
        setinel = True
        print("The word {} ".format(w), end="")

        #(1) The word must not have already been scored
        if w in wordSet:
            print("has already been used.")
            continue
        else:
            wordSet.add(w)

        #(2) The word must be at least three letters long
        if currentWordLength < 3:
            print("is too short.")
            break

        #(3) The word must be in the English language
        if not d.check(w):
            print("is ... not a word.")
            continue

        #(4) The word must be present in the 4x4 grid
        if not findWordInGrid(w, dice):
          print("is not present.")
          continue

        #(5) The word must not use the same letter cube more than once per word
        #This is built into findWordInGrid()

        #Grade the word
        if currentWordLength <= 4:
            score += 1
            print("is worth 1 point.")
        elif currentWordLength == 5:
            score += 2
            print("is worth 2 points.")
        elif currentWordLength == 6:
            score += 3
            print("is worth 3 points.")
        elif currentWordLength == 7:
            score += 5
            print("is worth 5 points.")
        elif currentWordLength >= 8:
            score += 11
            print("is worth 11 points.")


    return score
        

def findWordInGrid(word, dice):
    toReturn = False

    #Search grid for starting character    
    startingPoints = []

    if word[0] == "Q":
      toFind = "Qu"
    else:
      toFind = word[0]


    for rowIdx, row in enumerate(dice):
      for colIdx, col in enumerate(row):
        if col == toFind:
          startingPoints.append([rowIdx, colIdx])

    if len(startingPoints) == 0:
      return False

    #For each occurance of the starting character, try and build the word
    for p in startingPoints:
      toReturn = constructWord(word, p, dice)
      if toReturn:
        break

    return toReturn


def constructWord(word, coord, dice, pos=0, fromCoord = []):
    #Base case
    if pos >= len(word) - 1:
      return True

    #Recursive case
    surroundingChars = [[coord[0] - 1, coord[1] - 1],
                        [coord[0] - 1, coord[1]    ],
                        [coord[0] - 1, coord[1] + 1],
                        [coord[0]    , coord[1] - 1],
                        [coord[0]    , coord[1] + 1],
                        [coord[0] + 1, coord[1] - 1],
                        [coord[0] + 1, coord[1]    ],
                        [coord[0] + 1, coord[1] + 1]]

    #Remove coords that are out of bounds
    surroundingChars = [x for x in surroundingChars 
                        if x[0] != -1 and x[1] != -1 
                       and x[0] != 4  and x[1] != 4
                       ]
    if word[pos] == "Q":
      pos += 2
    else:
      pos += 1

    toReturn = False

    for p in surroundingChars:
      if dice[p[0]][p[1]] == word[pos] and p != fromCoord:
        toReturn = constructWord(word, p, dice, pos, coord)
      elif word[pos:2] == "QU" and dice[p[0]][p[1]] == "qu" and p != fromCoord: 
        toReturn = constructWord(word, p, dice, pos, coord)

    return toReturn


def isCharInGrid(dice, char):
    isIn = False

    for row in dice:
        for c in row:
            c = c.upper()
            if c == char:
                isIn = True
                break
        if isIn:
            break
    
    return isIn

class BoggleGameWindow(qtw.QMainWindow):
    def __init__(self):
        qtw.QWidget.__init__(self)
        self.setup(self.app_start_dialog())

    def setup(self, load_game):
        # Basic window info
        self.setGeometry(200, 200, 750, 500)
        self.setWindowTitle('final.py')


        # Create a menu bar and add options
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        game_menu = menu_bar.addMenu('Game')

        newgame_action = qtw.QAction('New', self)
        newgame_action.triggered.connect(self.new_game)
        game_menu.addAction(newgame_action)

        savegame_action = qtw.QAction('Save', self)
        savegame_action.triggered.connect(self.save_game)
        game_menu.addAction(savegame_action)

        loadgame_action = qtw.QAction('Load', self)
        loadgame_action.triggered.connect(self.load_game)
        game_menu.addAction(loadgame_action)


        # Create the main grid area
        self.boggle_game = BoggleGame(self)
        self.setCentralWidget(self.boggle_game)

        self.show()

        if load_game is True:
            self.load_game()
        else:
            self.new_game()

    def new_game(self):
        logging.debug("Starting new game")
        self.boggle_game.start()

    def save_game(self):
        logging.debug("Saving current game")

        self.boggle_game.pause()

        data_to_save = self.boggle_game.save()

        # Make the save directory if it doesn't exist
        if not os.path.exists("./.saves"):
            os.makedirs("./.saves")

        # Make filename current time and date, and replace invalid chars
        curr_time = "{:%c}".format(datetime.now()).replace(':','-')

        with open("./.saves/" + curr_time, "w") as outfile:
            outfile.write(data_to_save)

        logging.debug("Saved game to .saves/" + curr_time)

        self.boggle_game.resume()

    def load_game(self):
        logging.debug("Loading a game")

        self.boggle_game.pause()

        load_dialog = LoadDialog()
        load_dialog.exec_()

        if load_dialog.selected_item is None:
            logging.error("There was no selection returned by the load dialog")
            exit()
        else:
            self.boggle_game.load(load_dialog.selected_item)

        self.boggle_game.resume()

    def app_start_dialog(self):
        start_msg = qtw.QMessageBox()

        start_msg.setText("Would you like to start a new game or load a saved game?")

        new_game = start_msg.addButton("Start New Game", qtw.QMessageBox.RejectRole)
        load_game = start_msg.addButton("Load Game", qtw.QMessageBox.AcceptRole)

        reply = start_msg.exec_()

        if reply is 1:
            logging.debug("Loading an existing game upon startup...")
            return True
        else:
            logging.debug("Creating a new game upon startup...")
            return False


class LoadDialog(qtw.QDialog):
    def __init__(self):
        qtw.QDialog.__init__(self)
        
        self.selected_item = None

        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

        self.resize(350, 450)


        self.text = qtw.QLabel("Select a game to load:", self)
        self.vbox.addWidget(self.text)


        self.list = qtw.QListWidget(self)
        self.list.itemDoubleClicked.connect(self.return_selection)

        for item in os.listdir("./.saves"):
            item.replace('-', ':')
            logging.debug("Entering item {} in the list".format(item))
            qtw.QListWidgetItem(item, self.list)

        self.vbox.addWidget(self.list)

    def return_selection(self, item):
        logging.debug("Selected to load file {}.".format(item.text()))
        self.selected_item = item.text().replace(":", "-")
        self.close()


class BoggleGame(qtw.QWidget):
    def __init__(self, parent):
        qtw.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        # Track the current time limit, in seconds
        self.time_remaining = 120

        # Create the grid
        self.grid = qtw.QGridLayout()
        self.setLayout(self.grid)


        # Create the widgets that go in the grid
        self.input_box = qtw.QLineEdit(self)
        self.input_box.returnPressed.connect(self.submit_guess)
        self.input_box.setReadOnly(True)

        self.typed_words_box = qtw.QTextEdit(self)
        self.typed_words_box.setReadOnly(True)

        self.boggle_letters = BoggleLetters(self)
        
        self.timer_display = TimerDisplay(self)

        self.timer = qtc.QTimer(self)
        self.timer.timeout.connect(self.update)


        # Put the widgets in the grid
        self.grid.addWidget(self.boggle_letters, 1, 1, 1, 3)
        self.grid.addWidget(self.typed_words_box, 1, 4, 1, 3)
        self.grid.addWidget(self.input_box, 2, 1, 1, 5)
        self.grid.addWidget(self.timer_display, 2, 6, 1, 1)

    def start(self):
        # Clear the text input
        self.input_box.setReadOnly(False)
        self.input_box.clear()
        self.input_box.setFocus()

        # Clear the typed words box
        self.typed_words_box.clear()

        # Roll the dice
        self.boggle_letters.clear()
        self.boggle_letters.roll_dice()

        # Start the timer
        self.time_remaining = 120
        self.timer_display.reset()
        self.timer.start(1000)

    def pause(self):
        self.timer.stop()
        self.input_box.setReadOnly(True)

    def resume(self):
        self.input_box.setReadOnly(False)
        self.timer.start(1000)

    def submit_guess(self):
        guess = self.input_box.text()
        self.input_box.clear()

        logging.debug("Processing guess \"{}\"".format(guess))

        self.typed_words_box.append(guess)

    def update(self):
        self.timer_display.update_timer()

        self.time_remaining -= 1

        if self.time_remaining == 0:
            self.stop()

    def stop(self):
        self.timer.stop()
        
        # Calculate score
        words = self.typed_words_box.toPlainText().split('\n')
        score = gradeWords(self.boggle_letters.get_dice(), words)

        reply = EndgameMessage(score).exec_()

        if reply == qtw.QMessageBox.Yes:
            self.start()
        else:
            app.quit()

    def save(self):
        dice = self.boggle_letters.get_dice()
        guesses = self.typed_words_box.toPlainText()
        # Returns a tuple
        time_left = self.timer_display.get_time()
        
        game_state = (dice, guesses, time_left)

        return pickle.dumps(game_state, 0)

    def load(self, state_to_load):
        # Expects a file to unpickle

        with open("./.saves/" + state_to_load, "r") as f:
            game_state = pickle.Unpickler(f).load()

        dice, guesses, time_left = game_state

        self.boggle_letters.set_dice(dice)

        self.typed_words_box.clear()
        self.typed_words_box.append(guesses)

        self.timer_display.set_time(time_left)


class EndgameMessage(qtw.QMessageBox):
    def __init__(self, score):
        qtw.QMessageBox.__init__(self)
        self.setText("Time's Up!\nScore: {}\nWould you like to play again?".format(score))
        self.addButton(self.No)
        self.addButton(self.Yes)


class TimerDisplay(qtw.QLCDNumber):
    def __init__(self, parent):
        qtw.QLCDNumber.__init__(self, parent)
        self.setup()

    def setup(self):
        # Initial display value is 0
        self.minutes = 3
        self.seconds = 0
        self.display("{}.{}".format(self.minutes, format(self.seconds, '02')))

    def update_timer(self):
        self.seconds -= 1

        if self.seconds < 0:
            self.seconds = 59
            self.minutes -= 1

        self.display("{}.{}".format(self.minutes, format(self.seconds, '02')))

    def reset(self):
        self.minutes = 3
        self.seconds = 0
        self.display("{}.{}".format(self.minutes, format(self.seconds, '02')))

    def get_time(self):
        return (self.minutes, self.seconds)

    def set_time(self, time_tuple):
        self.minutes, self.seconds = time_tuple
        self.update_timer()


class BoggleLetters(qtw.QWidget):
    def __init__(self, parent):
        qtw.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.setSpacing(0)

    def draw_dice(self):
        
        for row in self.dice:
            rowLayout = qtw.QHBoxLayout()
            self.vbox.addLayout(rowLayout)
            for letter in row:
                logging.debug("Drawing box for \"{}\"".format(letter))
                rowLayout.addWidget(LetterBox(self, letter), 0)
        
    def clear(self):
        for row in range(0, self.vbox.count()):
            for column in range(0, self.vbox.itemAt(row).count()):
                self.vbox.itemAt(row).itemAt(column).widget().deleteLater()

    def roll_dice(self):
        self.dice = rollDice()
        logging.debug("Dice rolled are {}".format(self.dice))

        self.draw_dice()

    def get_dice(self):
        return self.dice

    def set_dice(self, dice):
        self.dice = dice
        self.clear()
        self.draw_dice()


class LetterBox(qtw.QWidget):
    def __init__(self, parent, letter):
        qtw.QWidget.__init__(self, parent)
        self.grid = qtw.QGridLayout()
        self.setLayout(self.grid)

        self.letter = letter

    def paintEvent(self, event):
        points_list = [qtc.QPoint(0, 0),
                       qtc.QPoint(74, 0),
                       qtc.QPoint(74, 74),
                       qtc.QPoint(0, 74)]

        square = qtg.QPolygon(points_list)

        qp = qtg.QPainter()
        qp.begin(self)

        font = qp.font()
        font.setBold(True)
        font.setPointSize(font.pointSize() * 2)
        qp.setFont(font)

        # Since Qu is longer than the rest, this makes sure it's still centered
        if self.letter == "Qu":
            letter_pos = qtc.QPoint(15,48)
        else:
            letter_pos = qtc.QPoint(26,48)

        qp.drawText(letter_pos, self.letter)

        qp.drawPolygon(square)

        qp.end()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    main_window = BoggleGameWindow()
    app.exec_()
