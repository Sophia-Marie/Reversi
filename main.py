import unittest
import pygame
import math
from time import sleep

# Global variables
# Colours
PINK  = (102, 0, 51)
GREEN = (51,102,0)
BROWN = (80,26,26)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY  = (160,160,160)
ORANGE= (255,128,0)
DARKGREEN= (0,102,51)
DEBUG = False
#DEBUG = True

def asciiPrintGameField(stoneSet):
    for i, s in enumerate(stoneSet):
        if s == 1:
            print u"\u25CF",
        elif s == 2:
            print u"\u25CB",
        else:
            print u"\u25A1",
        if (i+1) % 8 == 0:
            print

def check_mouse_position(allPositionsRect, mouseX, mouseY):
    for i, positionList, in enumerate(allPositionsRect):
        if positionList[0] < mouseX < positionList[0]+positionList[2] and positionList[1] < mouseY < positionList[1]+positionList[3]:
            return i

#Klasse: Maus Eigenschaften: Position, gedrueckt...
        
def get_mouse_position():
    mouseX,mouseY = pygame.mouse.get_pos()
    return mouseX, mouseY

        
def check_mouse_pressed():
    clicked= pygame.mouse.get_pressed()[0] 
    return clicked

def stones_set():
    stonesSet= [ 0 for _ in range(64)]
    return stonesSet

def basic_lineup(stoneSet):
    newStoneSet = list(stoneSet)
    newStoneSet[27] = 1
    newStoneSet[28] = 2
    newStoneSet[35] = 2
    newStoneSet[36] = 1
    return newStoneSet

def calculate_position():
    positionList = [100, 100, 70, 70]
    allPositions=[list(positionList)]
    
    for position in range(1,64):
        if position !=0 and position %8==0:
            positionList[1] +=72
            positionList[0] = 100
        else:
            positionList[0] +=72
        allPositions.append(list(positionList))
        
    return allPositions

def draw_field(window, player, allPositionsRect, positionArrow, stoneSet, clicked):
    
    for i, positionList in enumerate(allPositionsRect):
        if positionArrow==i:
            pygame.draw.rect(window, PINK, positionList)
        else:
            pygame.draw.rect(window, GREEN, positionList)
    
        if stoneSet[i]==1:
            pygame.draw.circle(window, BLACK, (positionList[0]+35, positionList[1]+35), 25)
        elif stoneSet[i]==2:
            pygame.draw.circle(window, WHITE,(positionList[0]+35, positionList[1]+35), 25)
        else:
            pass

def any_available_move_for_next_player(stoneSet, player):
    if player == 1:
        nextPlayer=2
    else:
        nextPlayer=1

    for i, stone in enumerate(stoneSet):
        if stone == 0:
            flipOk = only_analyse_for_all_directions(stoneSet, nextPlayer, i)
            if flipOk:
                return True
    return False
    
def available_moves(stoneSet, player, p, direction, foundOpponent = False):
    p += direction
    if 0<=p<=63:
        if DEBUG:    print "stoneSet[p]:", stoneSet[p]

        if not foundOpponent:
            if player==1:
                foundOpponent = stoneSet[p] == 2
            else:
                foundOpponent = stoneSet[p] == 1
                
        MODULO_OFFSET=1 # Because modulo works best with even numbers
        LEFT_BORDER_OFFSET=7 # Modulo checks right border, this offset simulates a right border when it is actually the left border
        TOP_BORDER_OFFSET=0 # smaller than 0 is the top field border
        BOTTOM_BORDER_OFFSET=63 # bigger than 63 is the bottom field border

        if direction==-8 or direction==8:
            if stoneSet[p] == (2 if player == 2 else 1):
                if DEBUG:    print "end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
                return foundOpponent
            elif (p>BOTTOM_BORDER_OFFSET) or (p<TOP_BORDER_OFFSET):
                if DEBUG:    print "end of recursion (border) p={}, foundOpponent={}".format(p, foundOpponent)
                return False
            elif stoneSet[p] == 0:
                if DEBUG:    print "end of recursion (empty field) p={}, foundOpponent={}".format(p, foundOpponent)
                return False        
            else:
                if DEBUG:    print "recursive call p={}, foundOpponent={}".format(p, foundOpponent)
                return available_moves(stoneSet, player, p, direction, foundOpponent)
            
        elif direction==-1 or direction==1:
            if stoneSet[p] == (2 if player == 2 else 1):
                if DEBUG:    print "end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
                return foundOpponent
            elif (p+MODULO_OFFSET)%8 == 0 or (p+MODULO_OFFSET+LEFT_BORDER_OFFSET)%8 == 0:
                if DEBUG:    print "end of recursion (border) p={}, foundOpponent={}".format(p, foundOpponent)
                return False
            elif stoneSet[p] == 0:
                if DEBUG:    print "end of recursion (empty field) p={}, foundOpponent={}".format(p, foundOpponent)
                return False        
            else:
                if DEBUG:    print "recursive call p={}, foundOpponent={}".format(p, foundOpponent)
                return available_moves(stoneSet, player, p, direction, foundOpponent)
        else:
            if stoneSet[p] == (2 if player == 2 else 1):
                if DEBUG:    print "end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
                return foundOpponent
            elif (p+MODULO_OFFSET)%8 == 0 or (p+MODULO_OFFSET+LEFT_BORDER_OFFSET)%8 == 0 or (p>BOTTOM_BORDER_OFFSET) or (p<TOP_BORDER_OFFSET):
                if DEBUG:    print "end of recursion (border) p={}, foundOpponent={}".format(p, foundOpponent)
                return False
            elif stoneSet[p] == 0:
                if DEBUG:    print "end of recursion (empty field) p={}, foundOpponent={}".format(p, foundOpponent)
                return False        
            else:
                if DEBUG:    print "recursive call p={}, foundOpponent={}".format(p, foundOpponent)
                return available_moves(stoneSet, player, p, direction, foundOpponent)
    else:
        None

def flip_stones_on_game_board(stoneSet, player, p, direction, foundOpponent = False):
    if 0<=p<=63:
        p += direction
        if stoneSet[p] == (2 if player == 2 else 1):
            if DEBUG:    print "[FLIP] end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
            return
        else:
            if DEBUG:    print "[FLIP] coloring and recursive call p={}, foundOpponent={}".format(p, foundOpponent)
            stoneSet[p] = 2 if player == 2 else 1
            return flip_stones_on_game_board(stoneSet, player, p, direction, foundOpponent)
    else:
        None
    
def analyse(stoneSet, direction, player, positionArrow, doFlip):
    if DEBUG:
        print "--- analysis start --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")
        if not doFlip:
            print "analyse only"
        else:
            print "analyse and flip"
    flipOk= available_moves(stoneSet, player, positionArrow, direction)

    if flipOk and doFlip:
        if DEBUG:    print "--- flip start --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")
        flip_stones_on_game_board(stoneSet, player, positionArrow, direction)
        if DEBUG:    print "--- flip end --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")        

    if DEBUG:    print "--- analysis end --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")
    if DEBUG:    print
    return flipOk

def for_all_directions(stoneSet, currentPlayer, positionArrow, doFlip):
    rightFlipOk = analyse(stoneSet, 1, currentPlayer, positionArrow, doFlip)
    leftFlipOk  = analyse(stoneSet, -1, currentPlayer, positionArrow, doFlip)
    upFlipOk    = analyse(stoneSet, 8, currentPlayer, positionArrow, doFlip)
    downFlipOk  = analyse(stoneSet, -8, currentPlayer, positionArrow, doFlip)
    sevenFlipOk = analyse(stoneSet, 7, currentPlayer, positionArrow, doFlip)
    sevendownFlipOk = analyse(stoneSet, -7, currentPlayer, positionArrow, doFlip)
    nineFlipOk = analyse(stoneSet, 9, currentPlayer, positionArrow, doFlip)
    ninedownFlipOk = analyse(stoneSet, -9, currentPlayer, positionArrow, doFlip)
    flipOk = leftFlipOk or rightFlipOk or upFlipOk or downFlipOk or sevenFlipOk or sevendownFlipOk or nineFlipOk or ninedownFlipOk
    return flipOk
    
def flip_for_all_directions(stoneSet, currentPlayer, positionArrow):
    return for_all_directions(stoneSet, currentPlayer, positionArrow, True)

def only_analyse_for_all_directions(stoneSet, currentPlayer, positionArrow):
    return for_all_directions(stoneSet, currentPlayer, positionArrow, False)

def flip(stoneSet, currentPlayer, positionArrow):    
    flipOk = flip_for_all_directions(stoneSet, currentPlayer, positionArrow)
    if flipOk:
        stoneSet[positionArrow] = currentPlayer
        
    return flipOk

def calc_occupied_stones(stoneSet):
    occupiedBlack=0
    occupiedWhite=0
    for i in stoneSet:
        if i == 1:
            occupiedBlack+=1
        elif i == 2:
            occupiedWhite+=1

    return occupiedBlack, occupiedWhite

def draw_buttons(window, mouseX, mouseY, clicked, gameIsOver, kiON, ki1, ki2):
    newGameButtonClicked = False
    font= pygame.font.Font(None, 18)
    
    if 130 > mouseX > 50 and 70 > mouseY > 50 and clicked==1:
        pygame.draw.rect(window, GREY, (50,50,80,20))
        newGameButtonClicked = True
    elif gameIsOver:
        pygame.draw.rect(window, ORANGE, (50,50,80,20))
    else:
        pygame.draw.rect(window, WHITE, (50, 50, 80, 20))
        
    #player vs player button
    if 350 > mouseX > 250 and 28 > mouseY > 8 and clicked==1:
        pygame.draw.rect(window, GREY, (250,8,100,20))
        kiON = "Off"
    else:
        pygame.draw.rect(window, WHITE, (250,8,100,20))
        
    playerKiText=font.render("Player vs Player", 1, BLACK)
    window.blit(playerKiText, (250,10,80,20))

    #player vs Ki button
    if 475 > mouseX > 400 and 28 > mouseY > 8 and clicked==1:
        pygame.draw.rect(window, GREY, (400,8,75,20))
        kiON="On"
        ki1=True
    else:
        pygame.draw.rect(window, WHITE, (400,8,75,20))
    playerKiText=font.render("vs easy Ki", 1, BLACK)
    window.blit(playerKiText, (402,10,80,20))

    if 575 > mouseX > 500 and 28 > mouseY > 8 and clicked==1:
        pygame.draw.rect(window, GREY, (500,8,75,20))
        kiON="On"
        ki2=True
    else:
        pygame.draw.rect(window, WHITE, (500,8,75,20))
    playerBetterKiText=font.render("vs better Ki", 1, BLACK)
    window.blit(playerBetterKiText, (502,10,80,20))

    # New Game button
    resetText= font.render("New Game", 1, BLACK)
    window.blit(resetText, (60,55,50,50))
    
    return newGameButtonClicked , kiON, ki1, ki2

def ki_move_set(stoneSet, currentPlayer, ki1, ki2):
    kiMove=0
    if ki1:
        for i, stone in enumerate(stoneSet):
            if stone == 0:
                flipOk= only_analyse_for_all_directions(stoneSet, currentPlayer, i)
                if flipOk:
                    kiMove=i
                    return kiMove
    elif ki2:
        maxFlip=0
        edgesList=[0, 7, 56, 63]
        for i in edgesList:
            if stoneSet[i]==0:
                flipOk=only_analyse_for_all_directions(stoneSet, currentPlayer, i)
                if flipOk:
                    kiMove=i
                    return kiMove

        for i, stone in enumerate(stoneSet):
            if stone ==0:
                flipOk=only_analyse_for_all_directions(stoneSet, currentPlayer, i)
                if flipOk:
                    stoneSetCopy = list(stoneSet)
                    flip(stoneSetCopy, currentPlayer, i)
                    black,white = calc_occupied_stones(stoneSetCopy)
                    if white>maxFlip:
                        maxFlip=white
                        kiMove=i
        return kiMove
            
def blit_text_with_outline(outerText, innerText, window, position):
    window.blit(outerText, (position[0]-1,position[1],position[2],position[3]))
    window.blit(outerText, (position[0]-1,position[1]-1,position[2],position[3]))
    window.blit(outerText, (position[0]-1,position[1]+1,position[2],position[3]))
    window.blit(outerText, (position[0]+1,position[1],position[2],position[3]))
    window.blit(outerText, (position[0]+1,position[1]-1,position[2],position[3]))
    window.blit(outerText, (position[0]+1,position[1]+1,position[2],position[3]))
    window.blit(outerText, (position[0],position[1]-1,position[2],position[3]))
    window.blit(outerText, (position[0],position[1]+1,position[2],position[3]))
    window.blit(innerText, (position[0],position[1],position[2],position[3]))

def show_text(window, currentPlayer, occupiedBlack, occupiedWhite):
    font=pygame.font.Font(None, 18)

    #occupied stones
    blackTextOutline=font.render("Black Stones: {}".format(occupiedBlack), 1, WHITE)
    blackText=font.render("Black Stones: {}".format(occupiedBlack), 1, BLACK)
    blit_text_with_outline(blackTextOutline, blackText, window, (640,50,20,20))
    

    whiteTextOutline=font.render("White Stones: {}".format(occupiedWhite), 1, BLACK)
    whiteText=font.render("White Stones: {}".format(occupiedWhite), 1, WHITE)
    blit_text_with_outline(whiteTextOutline, whiteText, window, (640,70,20,20))

    #which players turn
    if currentPlayer==1:
        showPlayerText=font.render("BLACK player's turn!", 1, BLACK)
        showPlayerTextOutline=font.render("BLACK player's turn!", 1, WHITE)
    else:
        showPlayerText=font.render("WHITE player's turn!", 1, WHITE)
        showPlayerTextOutline=font.render("WHITE player's turn!", 1, BLACK)
    
    blit_text_with_outline(showPlayerTextOutline, showPlayerText, window, (350,50,200,20))


def player_move(stoneSet, currentPlayer, positionArrow, clicked):
    flipOk=False
    if positionArrow != None and clicked and stoneSet[positionArrow]==0:
        flipOk = flip(stoneSet, currentPlayer, positionArrow)
        if DEBUG: print "current Player: {}".format("BLACK" if currentPlayer == 1 else "WHITE")
    
    return flipOk

def player_change(currentPlayer, kiTurn, kiON, availableMove):
    if currentPlayer == 1:
        if availableMove:
            currentPlayer = 2
            if kiON=="On":
                kiTurn=True
    else:
        if availableMove:
            currentPlayer = 1
            if kiON =="On":
                kiTurn=False
                
    return currentPlayer, kiTurn

def check_if_game_is_over(occupiedBlack, occupiedWhite, stoneSet):
    availableMove1=any_available_move_for_next_player(stoneSet, 1)
    availableMove2=any_available_move_for_next_player(stoneSet, 2)
    if occupiedBlack + occupiedWhite == 64:
        gameIsOver= True
    elif occupiedBlack ==0:
        gameIsOver= True
    elif occupiedWhite==0:
        gameIsOver= True
    elif availableMove1==False and availableMove2==False:
        gameIsOver= True
    else:
        gameIsOver= False
    
    return gameIsOver

def show_winner(window, occupiedWhite, occupiedBlack, ki1, ki2):
    window.fill((64,64,64,128), special_flags=pygame.BLEND_MULT)


    if occupiedWhite>occupiedBlack:
        winnerFont=pygame.font.Font(None, 48)
        if ki1 or ki2:
            winnerText=winnerFont.render("Game Over!", 1, ORANGE)
        else:
            winnerText=winnerFont.render("Player White wins, congratulations!", 1, ORANGE)
        window.blit(winnerText, (100,350,200,200))
    elif occupiedBlack>occupiedWhite:
        winnerFont=pygame.font.Font(None, 48)
        if ki1 or ki2:
            winnerText=winnerFont.render("Congratulations, you won!", 1, ORANGE)
        else:
            winnerText=winnerFont.render("Player Black wins, congratulations!", 1, ORANGE)
        window.blit(winnerText, (100,350,200,200)) 
    else:
        winnerFont=pygame.font.Font(None, 48)
        winnerText=winnerFont.render("No Player wins, it's a tie!", 1, ORANGE)
        window.blit(winnerText, (100,350,200,200))
        
# ---------------------------------------------------------------------

def main():
    pygame.init()

    window = pygame.display.set_mode((800,700))

    pygame.display.set_caption("Reversi")

    #first assign of variables
    currentPlayer = 1
    kiTurn = False
    kiON = "Off"
    ki1 = False
    ki2 = False

    # first call of functions
    allPositionsRect = calculate_position()
    stoneSet = stones_set()

    #basic lineup
    stoneSet = basic_lineup(stoneSet)

    gameLoop=True
    ##init=True
    while gameLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop=False
                
        mouseX, mouseY = get_mouse_position()
        clicked = check_mouse_pressed()

    ##    if not init and not clicked:
    ##        sleep(0.01)
    ##        continue

        window.fill(BROWN)

        positionArrow = check_mouse_position(allPositionsRect, mouseX, mouseY)
        
        if kiTurn:
            positionArrow=ki_move_set(stoneSet, currentPlayer, ki1, ki2)
            clicked=1
        flipOk = player_move(stoneSet, currentPlayer, positionArrow, clicked)
        if flipOk:
            availableMove = any_available_move_for_next_player(stoneSet, currentPlayer)
            currentPlayer, kiTurn = player_change(currentPlayer, kiTurn, kiON, availableMove)
        clicked = check_mouse_pressed()
            
        draw_field(window, currentPlayer, allPositionsRect, positionArrow, stoneSet, clicked)

        occupiedBlack,occupiedWhite = calc_occupied_stones(stoneSet)

        show_text(window, currentPlayer, occupiedBlack, occupiedWhite)

        gameIsOver= check_if_game_is_over(occupiedBlack, occupiedWhite, stoneSet)

        if gameIsOver:
            show_winner(window, occupiedWhite, occupiedBlack, ki1, ki2)

        newGameButtonClicked , kiON, ki1, ki2 = draw_buttons(window, mouseX, mouseY, clicked, gameIsOver, kiON, ki1, ki2)

        if newGameButtonClicked:
            stoneSet = stones_set()
            stoneSet = basic_lineup(stoneSet)
            currentPlayer = 1
            kiTurn = False
            if DEBUG:    print "new game"
       
        pygame.display.flip()

    ##    init = False
        
    pygame.quit()

class TestPlacement(unittest.TestCase):
    def setUp(self):
        self.stoneSet = stones_set()
        
    def test_calc_occupied_stones_empty(self):
        black, white = calc_occupied_stones(self.stoneSet)
        self.assertEqual(black, 0)
        self.assertEqual(white, 0)

    def test_calc_occupied_stones_not_empty(self):
        self.stoneSet = basic_lineup(self.stoneSet)
        self.stoneSet[0] = 1
    
        black, white = calc_occupied_stones(self.stoneSet)
        self.assertEqual(black, 3)
        self.assertEqual(white, 2)

    def test_first_flip(self):
        expectedStoneSet = stones_set()
        expectedStoneSet[27] = 1
        expectedStoneSet[28] = 1
        expectedStoneSet[29] = 1
        expectedStoneSet[35] = 2
        expectedStoneSet[36] = 1
        
        self.stoneSet = basic_lineup(self.stoneSet)
        flip(self.stoneSet, 1, 29)
        self.assertListEqual(expectedStoneSet, self.stoneSet)

    def test_second_flip(self):
        expectedStoneSet = stones_set()
        expectedStoneSet[21] = 2
        expectedStoneSet[27] = 1
        expectedStoneSet[28] = 2
        expectedStoneSet[29] = 1
        expectedStoneSet[35] = 2
        expectedStoneSet[36] = 1
        
        self.stoneSet = basic_lineup(self.stoneSet)
        flip(self.stoneSet, 1, 29)
        flip(self.stoneSet, 2, 21)
        self.assertListEqual(expectedStoneSet, self.stoneSet)

        print
        asciiPrintGameField(self.stoneSet)

    def test_upper_left_corner(self):
        expectedStoneSet = stones_set()
        expectedStoneSet[0] = 1
        expectedStoneSet[1] = 1
        expectedStoneSet[2] = 1

        self.stoneSet[1] = 2
        self.stoneSet[2] = 1

        flip(self.stoneSet, 1, 0)
        self.assertListEqual(expectedStoneSet, self.stoneSet)

    def test_player_change(self):
        self.stoneSet = basic_lineup(self.stoneSet)
        kiON="Off"
        currentPlayer=1
        kiTurn= False
        positionArrow=29
        clicked=1
        flipOk=player_move(self.stoneSet, currentPlayer, positionArrow, clicked)
        if flipOk:
            availableMove= any_available_move_for_next_player(self.stoneSet, currentPlayer)
            currentPlayer, kiTurn=player_change(currentPlayer, kiTurn, kiON, availableMove)
            
        self.assertTrue(currentPlayer==2)

    def test_any_available_move(self):
        availableMove= any_available_move_for_next_player(self.stoneSet, 1)
        self.assertFalse(availableMove)
        self.stoneSet = basic_lineup(self.stoneSet)
        availableMove = any_available_move_for_next_player(self.stoneSet, 1)
        self.assertTrue(availableMove)

    def test_bug_situation_1(self):
        # Up
        self.stoneSet[ 2] = 2
        self.stoneSet[10] = 2
        self.stoneSet[18] = 2
        self.stoneSet[26] = 2
        self.stoneSet[34] = 2
        self.stoneSet[42] = 2
        self.stoneSet[50] = 2

        # To be clicked
        self.stoneSet[58] = 0

        # Up + Right
        self.stoneSet[51] = 2
        self.stoneSet[44] = 2
        self.stoneSet[37] = 2

        # Right
        self.stoneSet[59] = 1
        self.stoneSet[60] = 1
        self.stoneSet[61] = 1

        # Left
        self.stoneSet[57] = 2
        self.stoneSet[56] = 1

        # Up + Left
        self.stoneSet[49] = 2
        self.stoneSet[40] = 1

        print "Before:"
        asciiPrintGameField(self.stoneSet)
        print

        expectedStoneSet = list(self.stoneSet)
        expectedStoneSet[58] = 1
        expectedStoneSet[57] = 1
        expectedStoneSet[49] = 1

        print "Expected:"
        asciiPrintGameField(expectedStoneSet)
        print

        flip(self.stoneSet, 1, 58)

        print "After:"
        asciiPrintGameField(self.stoneSet)
        print

        self.assertListEqual(expectedStoneSet, self.stoneSet)

if __name__ == '__main__':
    TESTING = False
    #TESTING = True

    if TESTING:
        unittest.main()
    else:
        main()
