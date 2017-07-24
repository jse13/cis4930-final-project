#!/usr/bin/env python
"""
-----------------------------------------------------------------------------------------------------------------------------------
Julian Engel
jse13
-----------------------------------------------------------------------------------------------------------------------------------
"""

from __future__ import print_function #For list comprehension things
import random
import enchant

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


def printGrid(items):
    #Using Python 3 print because it's a function and not a statement
    #Statements aren't allowed in list comprehensions, only functions
    [print("[{}] [{}] [{}] [{}]".format(x[0], x[1], x[2], x[3])) for x in items]


def getWords():
    print("Start typing your words! (press enter after each word and enter \'X\' when done): ")
    buf = []
    while True:
        print("> ", end=''),
        inputWord = raw_input()
        if inputWord == 'X':
            break
        else:
            buf.append(inputWord)

    return buf


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


if __name__ == "__main__":

    #Randomly roll the dice and print the grid to the screen
    currentDiceSet = rollDice()
    printGrid(currentDiceSet)

    #Prompt the user for words
    guessedWords = getWords()

    #Grade the user's words
    score = gradeWords(currentDiceSet, guessedWords)

    #Print the score
    print("Your total score is {} points!".format(score))


#                                                    WW            XkoxX     WXW                                                  
#                                                 Nx;..,dXKo,..';,......;OKd;...cX     W                                          
#                                        Kl...;c:,................................:l:'...k                                        
#                              0;,:lddl;..................................................'d0dco0                                 
#                           Wk,...................................................................c0                              
#                   WXXNNKx:........................................................................'xW                           
#                  d..................................................................................'0                          
#                 x ....................................................................................:N                        
#             Xc;'........................................................................................K                       
#            K.............................................................................................O                      
#           K...............................................................................................0                     
#          N.................................................................................................K                    
#         W,..................................................................................................W                   
#         d ..................................................................................................l                   
#        X.................................................................................................... K                  
#        :...................................,lc;,'',:oc:;;lOOdlcclk0xoodkOd:,,,;cdl;,,;c:,''''................c                  
#       0 ...................'c;,''';lO000O0000000000000000000000000000000000000000000000000000Ol.............. N                 
#       ;..................,d000000000000000000000000000000000000000000000000000000000000000000000kocc, ....... k                 
#      X ................;x000000000000000000000000000000000000000000000000000000000000000000000000000k ........:                 
#      o .............;oO000000000000000000000000000000000000000000000000000000000000000000000000000000: ........                 
#      '...........'O00000000000000000000000000000000000000Oxl:::::::;:x0000000000000000000000000000000O'....... X                
#     N ...........O0000000000000000000000000000000000000c;;cok0000000x:,;o00000000000000000000000000000O'...... k                
#     k ..........k000000000000000000000000000000000000000000000000000000kx000000000000000000000000000000O,......l                
#     c..........x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000l.....,                
#     '.........x000000000000000000000000000000000000000000Okdoc:::::cloxO0000000000000000000000000000000000k.....                
#    W........,O0000000000000000000000000000000000000Oxl:;:::ldxkOOOkkdoc:;;:ok000000000000000000000000000000,... N               
#    X ..... l00000000000000000000000000000000Oxoc::::cdk0000000000000000000ko:;:k000000000000000000000000000;... K               
#    O ..... o00000000000000000000000000000000OcoxO0000000000000000000000000000000000000000000000000000000000: .. O               
#    k ..... o00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c .. x               
#    d ..... d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000l .. d               
#    o ..... d000000000000000000000000000000000000000000000000000000000000000x:clodxkO00000000000000000000000o ...l               
#    l...... x00000000000000000000000000000Okdoc;:O000000000000000000000000000Oxdool:::::::lxO000000000000000x ...c               
#    l...... x000000000000000000000kdl:::::::loxO00000000000000000000000000000000000000000kdc;;:x000000000000k ...:               
#    l...... k0000000000000000Od:;;:ldk00000000000000000000000000000000000Okdoolcc::;;;;;;;;;;;. .;;;;;;::clkO ...:               
#    l...... k00000000Okxdolc,  ',,,,'''''''''',,,,;;::cld00000000000000l.                                   x ...;               
#    o ..... O000000O:                                    :000000000000O.  .',;;::cclllllooooooooooooooooc   c....;               
#    d ..... O000000l   .,,;::cllooddxxxkkkkkkkkkkkkxxx'  .000000000000k   :00000000000000xoO000000000000O   '....;               
#    x ......000000O:   x00000000000000Odk0000000000000:   o:,..   ..,:l   l00000000Ok0000Ol;;c0000000000O        'K              
#    O ......000Oo,.    O00000000000d:;:lk0Oko:'c000000:                   o00000000d.':::::clodk000000000.  ..  .:c,k            
#    K ......Ol'        O0000000000kl::cccllokKx'o00000c    ':lxkOkxoc,.   o000000Oc,xNWNXXXK0Oxlc;lO00000.  l: .O00O.d           
#    N .....     .;dl   O0000000Oc;lkXWWWWWWWWWWX;:0000c  .O000000000000'  o00000O.oWWWWWWWWWK0NWWNd'k0000.  cc k0000x.W          
#   0x ..     'lk000o   O000000d.xWWWWWWWNc.,NWWWW;:000c   O000000000000,  l00000d.WWWWWWWWW:  oNWWWc:0000.  :ll0k,k0O K          
# K,cdxl,.  .O000000o   O00000k.0WWWWWWWWX.  .NWWWk.000c   O000000000000:  c00000O;:XWWWWWWWd..,KWWW;c0000.  ;O0x.d00O X          
#W.o00000Ol..0000000d   O00000k.kWWWWWWWWWN00NWWWX,l000c   k000000000000l  ;0000000d,:xKWWWWWWWWWW0:;O0000.  ,00.l000d.W          
#d.0x:ck000Od0000000x   k000000O:;lkKNWWWWWNX0ko:;d0000c   k000000000000d  .000000000Oo::clodddoc::x000000.  '0O.d000;c           
#,cO.do.x00000000000O   d000000000koc:::c::::loxO000000c   O000000000000O.  O0000000000000Okxxxk0000000000.  .00d.k0k.K           
#.o0000:;000000000000.  l000000000000000000000000000000:   O0000000000000,  d0000000000000000000000000000k   ,000.l0c,            
#,c0000l.000000000000;  ;000000000000000000000000000000;  .00000000000000d  ,0000000000000000000000000Oxl'   l00O.x0.k            
#k.O000l.000000000000x  .xO00000000000000000000000Okxol.  :000000000000000'  ...',;;:::::::::;;;,''...     'd0:d000k.W            
# l,000l.000ld00000000:     .....''''''''''......        'O000000000000000kc,...            ........',;:lxO000:'000l,             
# W,l00o.O00.o000000000kc'.                  ......',;cok000000000000000000000000OOOOOOOO000000000000000000000x O00'd             
#  K.x0O.c00.d00000000000000OkkkkkkkOOOOOOO0000000000000000000000000000000000000000000000000000000000000000000O x0l.N             
#   d'00Ok00.d00000000000000000000000000000000000000000000000000000000000000l:O0000000000000000000000000000000O ,;oW              
#    'o00000.o00000000000000000000000000000000000000000,x0000000000000000000O:'k000000000000000000000000000000k K                 
#    0.k0000'l000000000000000000000000000000000000000x':0000000000000000000000d.o00000000000000000000000000000d.                  
#     d'O000;;0000000000000000000000000000000000000k;,x000000000000000000000000k,;k000000000000000000000000000l'                  
#      k,:od:.O00000000000000000000000000000000000l.d0000000000000000000000000000d'c00000000000000000000000000::                  
#        XOkk'l0000000000000000000000000000000000:'O0000000000000000000000000OO000O.d0000000000000000000000000,l                  
#            O.0000000000000000000000000000000000.l000Ol,';::d00000000000Ol,;''o000cx0000000000000000000000000.x                  
#            W.k000000000000000000000000000000000xc0000Oxk00kc,:dO000Oxl;,oO000000000000000000000000000000000O.0                  
#             'd00000000000000000000000000000000000000000000000kl:::::cdO0000000000000000dx000000000000000000k X                  
#             ;l00000000000000000000000koO00000000000000000000000000000000000000000000000xc;;:clooolccO000000d.                   
#             l;00000000000x;:ldxxxoc;;:oO000000000000000000000000000000000000000000000000000Okddoddxk0000000l'                   
#             d'0000000000000OdlccloxO00000000000000000000000000000000000000000000000000000000000000000000000:c                   
#             O.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,d                   
#             X O00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000.O                   
#             W.d0000000000000000000000000000000000000000000OO000000000000OxdlcccldO000000000000000000000000O.N                   
#              'l0000000000000000000000000000000000000kl::cl,.llcccc:,ccccld;'KKKO;.:;d000000000000000000000x.                    
#              c;0000000000000000000000000000000000Oc. :xkkx,.dxxxxd:.kkxddd'.dxxx',k, .x0000000000000000000l;                    
#              x.000000000000000000000000000000000l. ."Do I look like i know what a   .  x000000000000000000;o 
#              K O0000000000000000000000000000000;  ......boggle is?" .................. .O00000000000000000.O                    
#               .d000000000000000000000000kO0000l  ........               ......    ....  x0000:k0000000000k N                    
#               :c000000000000000000000000'l0000, ......   .',;:::::;;;::::::::::;'.  .. .O0000.d0000000000l,                     
#               x'000000000000000000000000.l0000d.      .',,,,''''.........'''''',,,.   'x00000;x0000000000'x                     
#               N.O00000000000000000000000OO00000Ooc:;:::ccllooddxxxkkkkkxxxdddooooooodO000000000000000000x.W                     
#                :c00000000000000000000000000000000000000000000000000000000000000000000000000000000000000O.x                      
#                K.k0000000000000000000000000000000000000000000000000000000000000000000000000000000000000:;                       
#                 d'O0000000000000000000000000000000000000000000O:::::::::c00000000000000000000000000000o'N                       
#                  o'O000000000000000000000000000000000000000000000000000000000000000000000000000000000o.X                        
#                   x.d0000000000000000000000000000000000000000000000000000000000000000000000000000000o x                         
#                    ,.x00000000000000000000000000000000000000000000000000000000000000000000000000000l .W                         
#                    o,000000000000000000000000000000000000000000000000000000000000000000000000000000x.x                          
#                    K.O00000000000000000000000000000000000000000000000000000000000000000000000000000x.W                          
#                     'o00000000000000000000000000000000000000000000000000000000000000000000000000000,o                           
#                     o,0000000000000000000000000000000000000000000000000000000000000000000000000000k.X                           
#                     N.k000000000000000000000000000000000000000000000000000000000000000000000000000:c                            
#                      c:000000000000000000000000000000000000000000000000000000000000000Oox00000000O.X                            
#                      X.k00000000000000000000000000O000000000000000000000000000000000x:,cO00000000c:                             
#                       c;00000000000000000000000000l;;:oxO0000000000000000000Okxdl:;;:x0000000000O.0                             
#                       N.d0000000000000000000000000000koc::::::::::::::::::::::codk00000000000000c,                              
#                        k.O000000000000000000000000000000000000000000000000000000000000000000000O.O                              
#                         c;000000000000000000000000000000000000000000000000000000000000000000000c,                               
#                         W;;O00000000000000000000000000000000000000000000000000000000000000000x,cN                               
#                           x'o00000000000000000000000000000000000000000000000000000000000000x;:K                                 
#                            Nl,d0000000000000000000000000000000000000000000000000000000000d,:K                                   
#                              No;ck0000000000000000000000000000000000000000000000000000kc;oX                                     
#                                 Ol;cx0000000000000000000000000000000000000000000000xc;l0                                        
#                                    Ko::cxO0000000000000000000000000000000000000kl;:oK                                           
#                                        Kdlc:cokO0000000000000000000000000Oxo::coOW                                              
#                                            WKkolcc::codxkkOO0OOOkxdol::ccldON                                                   
#                                                    NK0kxdollllloodxOKN                                                          
