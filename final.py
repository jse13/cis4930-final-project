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
        game_menu.addAction(newgame_action)

        savegame_action = qtw.QAction('Save', self)
        game_menu.addAction(savegame_action)

        loadgame_action = qtw.QAction('Load', self)
        game_menu.addAction(loadgame_action)


        # Create the main grid area
        self.boggle_game = BoggleGame(self)
        self.setCentralWidget(self.boggle_game)

        self.show()


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


class BoggleLetters(qtw.QWidget):
    def __init__(self, parent):
        qtw.QWidget.__init__(self, parent)
        self.setup()

    def setup(self):
        #self.grid = qtw.QGridLayout()
        #self.setLayout(self.grid)

        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.setSpacing(0)

        dice = rollDice()

        logging.debug("Dice rolled are {}".format(dice))
        
        #x = 1
        #y = 1
        for row in dice:
            rowLayout = qtw.QHBoxLayout()
            self.vbox.addLayout(rowLayout)
            #rowLayout.addStretch(0.1)
            for letter in row:
                logging.debug("Drawing box for \"{}\"".format(letter))
                rowLayout.addWidget(LetterBox(self, letter), 0)
            #rowLayout.addStretch(1)

            #for letter in row:
            #    self.grid.addWidget(LetterBox(self), x, y, 1, 1)
            #    y += 1
            #x += 1
            #y = 1



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
        logging.debug("Setting font size to {}".format(font.pointSize()))
        qp.setFont(font)
        qp.drawText(qtc.QPoint(26,48), self.letter)
        qp.drawPolygon(square)
        qp.end()


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
