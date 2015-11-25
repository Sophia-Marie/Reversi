import unittest
import pygame
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


def draw_Field(window, player, allPositionsRect, positionArrow, stoneSet, clicked):
    
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
            if only_analyse_for_all_directions(stoneSet, nextPlayer, i):
                return True
    return False
    
def available_Moves_horizontal(stoneSet, player, p, direction, foundOpponent = False):
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
                return available_Moves_horizontal(stoneSet, player, p, direction, foundOpponent)
            
        if direction==-1 or direction==1:
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
                return available_Moves_horizontal(stoneSet, player, p, direction, foundOpponent)
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
                return available_Moves_horizontal(stoneSet, player, p, direction, foundOpponent)
    else:
        None

def available_Moves_horizontal_flip(stoneSet, player, p, direction, foundOpponent = False):
    if 0<=p<=63:
        p += direction
        if stoneSet[p] == (2 if player == 2 else 1):
            if DEBUG:    print "[FLIP] end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
            return
        else:
            if DEBUG:    print "[FLIP] coloring and recursive call p={}, foundOpponent={}".format(p, foundOpponent)
            stoneSet[p] = 2 if player == 2 else 1
            return available_Moves_horizontal_flip(stoneSet, player, p, direction, foundOpponent)
    else:
        None
    
def analyse(stoneSet, direction, player, positionArrow, doFlip):
    if DEBUG:    print "--- analysis start --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")
        if not doFlip:
            print "analyse only"
        else:
            print "analyse and flip"
    flipOk = available_Moves_horizontal(stoneSet, player, positionArrow, direction)

    if flipOk and doFlip:
        if DEBUG:    print "--- flip start --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")
        available_Moves_horizontal_flip(stoneSet, player, positionArrow, direction)
        if DEBUG:    print "--- flip end --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")        

    if DEBUG:    print "--- analysis end --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")
    if DEBUG:    print
    return flipOk

def for_all_directions(stoneSet, currentPlayer, positionArrow, doFlip):
    rightFlipOk = analyse(stoneSet, 1, currentPlayer, positionArrow, doFlip)
    leftFlipOk = analyse(stoneSet, -1, currentPlayer, positionArrow, doFlip)
    upFlipOk = analyse(stoneSet, 8, currentPlayer, positionArrow, doFlip)
    downFlipOk = analyse(stoneSet, -8, currentPlayer, positionArrow, doFlip)
    sevenFlipOk = analyse(stoneSet, 7, currentPlayer, positionArrow, doFlip)
    sevendownFlipOk = analyse(stoneSet, -7, currentPlayer, positionArrow, doFlip)
    nineFlipOk= analyse(stoneSet, 9, currentPlayer, positionArrow, doFlip)
    ninedownFlipOk= analyse(stoneSet, -9, currentPlayer, positionArrow, doFlip)
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

def draw_buttons(window, mouseX, mouseY, clicked, gameIsOver):
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
        pygame.draw.rect(window, DARKGREEN, (250,8,100,20))
        playerVsPlayerClicked = True
    else:
        pygame.draw.rect(window, GREEN, (250,8,100,20))
        
    playerKiText=font.render("Player vs Player", 1, BLACK)
    window.blit(playerKiText, (250,10,80,20))

    #player vs Ki button
    if 475 > mouseX > 400 and 28 > mouseY > 8 and clicked==1:
        pygame.draw.rect(window, DARKGREEN, (400,8,75,20))
        playerVsKiClicked=True
    else:
        pygame.draw.rect(window, GREEN, (400,8,75,20))
    playerKiText=font.render("Player vs Ki", 1, BLACK)
    window.blit(playerKiText, (400,10,80,20))

    # New Game button
    resetText= font.render("New Game", 1, BLACK)
    window.blit(resetText, (60,55,50,50))
    
    return newGameButtonClicked #, playerVsPlayerClicked, playerVsKiClicked

def ki_on_or_off(mouseX, mouseY, clicked):
    kiOn="Off"
    if 350 > mouseX > 250 and 28 > mouseY > 8 and clicked==1:
        kiOn = "Off"
    elif 475 > mouseX > 400 and 28 > mouseY > 8 and clicked==1:
        kiOn="On"

        
    return kiOn

def ki_move_set(kiTurn):
    if kiTurn:
        pass
        

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

def player_vs_player(stoneSet, currentPlayer, positionArrow, clicked):
    if positionArrow != None and clicked and stoneSet[positionArrow]==0:
        flipOk = flip(stoneSet, currentPlayer, positionArrow)
        if flipOk:
            availableMove = any_available_move_for_next_player(stoneSet, currentPlayer)
            if currentPlayer == 1:
                if not availableMove:
                    currentPlayer = 1
                else:
                    currentPlayer = 2
                if DEBUG: print "current Player: {}".format("BLACK" if currentPlayer == 1 else "WHITE") 
            else:
                if not availableMove:
                    currentPlayer = 2
                else:
                    currentPlayer = 1
                if DEBUG: print "current Player: {}".format("BLACK" if currentPlayer == 1 else "WHITE")
                
def player_vs_ki(stoneSet, currentPlayer, positionArrow, clicked):
    if currentPlayer==1:
        if positionArrow != None and clicked and stoneSet[positionArrow]==0 and not kiTurn:
            flipOk = flip(stoneSet, currentPlayer, positionArrow)
            if flipOk:
                availableMove = any_available_move_for_next_player(stoneSet, currentPlayer)
                if currentPlayer == 1:
                    if not availableMove:
                        currentPlayer = 1
                    else:
                        currentPlayer=2
                        kiTurn=True
    else:
        kiTurn=True
        #kiMove= #funktion die den gewaehlten Stein zurueck gibt
        flipOk=flip(stoneSet,currentplayer, kiMove)
        if flipOk:
            availableMove = any_available_move_for_next_player(stoneSet, currentPlayer)
            if currentPlayer==2:
                if not availableMove:
                    currentPlayer = 2
                    kiTurn=True
                else:
                    currentPlayer = 1


def show_winner(window, occupiedWhite, occupiedBlack):
    window.fill((64,64,64,128), special_flags=pygame.BLEND_MULT)


    if occupiedWhite>occupiedBlack:
        winnerFont=pygame.font.Font(None, 48)
        winnerText=winnerFont.render("Player White wins, congratulations!", 1, ORANGE)
        window.blit(winnerText, (100,350,200,200))
    elif occupiedBlack>occupiedWhite:
        winnerFont=pygame.font.Font(None, 48)
        winnerText=winnerFont.render("Player Black wins, congratulations!", 1, ORANGE)
        window.blit(winnerText, (100,350,200,200)) 
    else:
        winnerFont=pygame.font.Font(None, 48)
        winnerText=winnerFont.render("No Player wins, it is a tie!", 1, ORANGE)
        window.blit(winnerText, (100,350,200,200))
        
# ---------------------------------------------------------------------

def main():
    pygame.init()

    window = pygame.display.set_mode((800,700))

    pygame.display.set_caption("Reversi")

    currentPlayer = 1

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
        kiON =ki_on_or_off(mouseX, mouseY, clicked)

    ##    if not init and not clicked:
    ##        sleep(0.01)
    ##        continue

        window.fill(BROWN)

        positionArrow = check_mouse_position(allPositionsRect, mouseX, mouseY)
        
##        if not kiON=="Off":
##            pass
##            player_vs_ki(stoneSet, currentPlayer, positionArrow, clicked)
##            
##        else:
        player_vs_player(stoneSet, currentPlayer, positionArrow, clicked)
             

        draw_Field(window, currentPlayer, allPositionsRect, positionArrow, stoneSet, clicked)

        occupiedBlack,occupiedWhite = calc_occupied_stones(stoneSet)

        show_text(window, currentPlayer, occupiedBlack, occupiedWhite)

        gameIsOver = occupiedBlack + occupiedWhite == 64

        if gameIsOver:
            show_winner(window, occupiedWhite, occupiedBlack)

        newGameButtonClicked = draw_buttons(window, mouseX, mouseY, clicked, gameIsOver)

        if newGameButtonClicked:
            stoneSet = stones_set()
            stoneSet = basic_lineup(stoneSet)
            currentPlayer = 1
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
        currentPlayer=1
        player_vs_player(self.stoneSet, currentPlayer, 29, 1)
        self.assertTrue(currentPlayer==2)

    def test_any_available_move(self):
        availableMove = any_available_move_for_next_player(self.stoneSet, 1)
        self.assertFalse(availableMove)

        self.stoneSet = basic_lineup(self.stoneSet)
        availableMove = any_available_move_for_next_player(self.stoneSet, 1)
        self.assertTrue(availableMove)
        
    def test_kiOn(self):
        kiOn=ki_on_or_off(300, 20, 0)
        self.assertTrue(kiOn=="Off")

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
    #TESTING = False
    TESTING = True

    if TESTING:
        unittest.main()
    else:
        main()
