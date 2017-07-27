#!/usr/bin/env python

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import sys
import random
import enchant
import logging

logging.basicConfig(level=logging.DEBUG)


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


class BoggleGameWindow(qtw.QMainWindow):
    def __init__(self):
        qtw.QWidget.__init__(self)
        self.setup()

    def setup(self):
        # Basic window info
        self.setGeometry(200, 200, 750, 500)
        self.setWindowTitle('Boggle')


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

    def new_game(self):
        logging.debug("Starting new game")
        self.boggle_game.start()

    def save_game(self):
        logging.debug("Saving current game")
        self.boggle_game.save()

    def load_game(self):
        logging.debug("Loading a game")


class BoggleGame(qtw.QWidget):
    def __init__(self, parent):
        qtw.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        # Create the grid
        self.grid = qtw.QGridLayout()
        self.setLayout(self.grid)


        # Create the widgets that go in the grid
        self.input_box = qtw.QLineEdit(self)

        self.typed_words_box = qtw.QTextEdit(self)
        self.typed_words_box.setReadOnly(True)

        self.boggle_letters = BoggleLetters(self)
        

        # Put the widgets in the grid
        self.grid.addWidget(self.boggle_letters, 1, 1, 1, 2)
        self.grid.addWidget(self.typed_words_box, 1, 3, 1, 2)
        self.grid.addWidget(self.input_box, 2, 1, 1, 4)


    def start(self):
        self.boggle_letters.clear()
        self.boggle_letters.draw_dice()

class BoggleLetters(qtw.QWidget):
    def __init__(self, parent):
        qtw.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.setSpacing(0)

    def draw_dice(self):
        self.dice = rollDice()

        logging.debug("Dice rolled are {}".format(self.dice))
        
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

    def kill(self):
        pass


class StartNewGameButton(qtw.QPushButton):
    def __init__(self, parent):
        qtw.QPushButton.__init__(self, parent)
        self.setText("Start New Game")
        self.move(20, 160)


class QuitButton(qtw.QPushButton):
    def __init__(self, parent):
        qtw.QPushButton.__init__(self, parent)
        self.setText("Quit")
        self.move(150, 160)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    main_window = BoggleGameWindow()
    app.exec_()
