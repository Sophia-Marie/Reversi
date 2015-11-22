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


def draw_Field(window, player, allPositionsRect, positionArrow, stoneSet, clicked, availableMove):
    
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

def available_Moves_horizontal(stoneSet, player, p, direction, foundOpponent = False):
    p += direction
    if 0<=p<=63:
        print "stoneSet[p]:", stoneSet[p]

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

            if (p>BOTTOM_BORDER_OFFSET) or (p<TOP_BORDER_OFFSET):
                print "end of recursion (border) p={}, foundOpponent={}".format(p, foundOpponent)
                return False
            elif stoneSet[p] == 0:
                print "end of recursion (empty field) p={}, foundOpponent={}".format(p, foundOpponent)
                return False        
            elif stoneSet[p] == (2 if player == 2 else 1):
                print "end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
                return foundOpponent
            else:
                print "recursive call p={}, foundOpponent={}".format(p, foundOpponent)
                return available_Moves_horizontal(stoneSet, player, p, direction, foundOpponent)
            
        if direction==-1 or direction==1:
            
            if (p+MODULO_OFFSET)%8 == 0 or (p+MODULO_OFFSET+LEFT_BORDER_OFFSET)%8 == 0:
                print "end of recursion (border) p={}, foundOpponent={}".format(p, foundOpponent)
                return False
            elif stoneSet[p] == 0:
                print "end of recursion (empty field) p={}, foundOpponent={}".format(p, foundOpponent)
                return False        
            elif stoneSet[p] == (2 if player == 2 else 1):
                print "end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
                return foundOpponent
            else:
                print "recursive call p={}, foundOpponent={}".format(p, foundOpponent)
                return available_Moves_horizontal(stoneSet, player, p, direction, foundOpponent)
        else:
            
            if (p+MODULO_OFFSET)%8 == 0 or (p+MODULO_OFFSET+LEFT_BORDER_OFFSET)%8 == 0 or (p>BOTTOM_BORDER_OFFSET) or (p<TOP_BORDER_OFFSET):
                print "end of recursion (border) p={}, foundOpponent={}".format(p, foundOpponent)
                return False
            elif stoneSet[p] == 0:
                print "end of recursion (empty field) p={}, foundOpponent={}".format(p, foundOpponent)
                return False        
            elif stoneSet[p] == (2 if player == 2 else 1):
                print "end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
                return foundOpponent
            else:
                print "recursive call p={}, foundOpponent={}".format(p, foundOpponent)
                return available_Moves_horizontal(stoneSet, player, p, direction, foundOpponent)
    else:
        None

def available_Moves_horizontal_flip(stoneSet, player, p, direction, foundOpponent = False):
    if 0<=p<=63:
        p += direction
        if stoneSet[p] == (2 if player == 2 else 1):
            print "[FLIP] end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
            return
        else:
            print "[FLIP] coloring and recursive call p={}, foundOpponent={}".format(p, foundOpponent)
            stoneSet[p] = 2 if player == 2 else 1
            return available_Moves_horizontal_flip(stoneSet, player, p, direction, foundOpponent)
    else:
        None
    
def analyseAndFlip(stoneSet, direction, player, positionArrow):
    print "--- analysis start --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")
    flipOk = available_Moves_horizontal(stoneSet, player, positionArrow, direction)

    if flipOk:
        print "--- flip start --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")
        available_Moves_horizontal_flip(stoneSet, player, positionArrow, direction)
        print "--- flip end --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")        

    print "--- analysis end --- PLAYER: {}".format("BLACK" if player == 1 else "WHITE")
    print
    return flipOk
           
    #circle(Surface, color, pos, radius, width=0)

def calc_occupied_stones(stoneSet):
    occupiedBlack=0
    occupiedWhite=0
    for i in stoneSet:
        if i == 1:
            occupiedBlack+=1
        elif i == 2:
            occupiedWhite+=1

    return occupiedBlack, occupiedWhite

def draw_buttons(window, mouseX, mouseY, clicked):
    newGameButtonClicked = False
    mousePosition= pygame.mouse.get_pos()
    
    if 100 > mouseX > 50 and 70 > mouseY > 50 and clicked==1:
        pygame.draw.rect(window, GREY, (50,50,80,20))
        newGameButtonClicked = True
    else:
        pygame.draw.rect(window, WHITE, (50, 50, 80, 20))

    # New Game Button
    
    resetFont= pygame.font.Font(None, 16)
    resetText= resetFont.render("New Game", 1, BLACK)
    window.blit(resetText, (50,50,50,50))
    return newGameButtonClicked

def show_text(window, currentPlayer, occupiedBlack, occupiedWhite):
    blackFont=pygame.font.Font(None, 18)
    blackText=blackFont.render("Player Black: {}".format(occupiedBlack), 1, BLACK)
    window.blit(blackText, (640,50,20,20))
    whiteFont=pygame.font.Font(None, 18)
    whiteText=blackFont.render("Player White: {}".format(occupiedWhite), 1, WHITE)
    window.blit(whiteText, (640,70,20,20))
    showPlayerFont=pygame.font.Font(None, 18)
    if currentPlayer==1:
        showPlayerText=showPlayerFont.render("BLACK player's turn!", 1, BLACK)
    else:
        showPlayerText=showPlayerFont.render("WHITE player's turn!", 1, WHITE)
    window.blit(showPlayerText, (350,50,200,20))
##    = resetFont.render("{} , {}".format(a,b), 1, BLACK)

# ---------------------------------------------------------------------

def main():
    pygame.init()

    window = pygame.display.set_mode((800,700))

    pygame.display.set_caption("Reversi")

    currentPlayer = 1

    # first call of functions
    allPositionsRect = calculate_position()
    stoneSet = stones_set()

    #Grundaufstellung
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
        
        newGameButtonClicked = draw_buttons(window, mouseX, mouseY, clicked)
        if newGameButtonClicked:
            stoneSet = stones_set()
            stoneSet = basic_lineup(stoneSet)
            currentPlayer = 1
            print "new game"

        positionArrow = check_mouse_position(allPositionsRect, mouseX, mouseY)

        #flipOk = analyseAndFlip(1) if positionArrow and clicked else False

        if positionArrow and clicked and stoneSet[positionArrow]==0:
            rightFlipOk = analyseAndFlip(stoneSet, 1, currentPlayer, positionArrow)
            leftFlipOk = analyseAndFlip(stoneSet, -1, currentPlayer, positionArrow)
            upFlipOk = analyseAndFlip(stoneSet, 8, currentPlayer, positionArrow)
            downFlipOk = analyseAndFlip(stoneSet, -8, currentPlayer, positionArrow)
            sevenFlipOk = analyseAndFlip(stoneSet, 7, currentPlayer, positionArrow)
            sevendownFlipOk = analyseAndFlip(stoneSet, -7, currentPlayer, positionArrow)
            nineFlipOk= analyseAndFlip(stoneSet, 9, currentPlayer, positionArrow)
            ninedownFlipOk= analyseAndFlip(stoneSet, -9, currentPlayer, positionArrow)
            flipOk = leftFlipOk or rightFlipOk or upFlipOk or downFlipOk or sevenFlipOk or sevendownFlipOk or nineFlipOk or ninedownFlipOk

            if flipOk:
                stoneSet[positionArrow] = currentPlayer
                if currentPlayer == 1:
                    currentPlayer = 2
                else:
                    currentPlayer = 1
            
        else:
            flipOk = False

        draw_Field(window, currentPlayer, allPositionsRect, positionArrow, stoneSet, clicked, flipOk)

        occupiedBlack,occupiedWhite = calc_occupied_stones(stoneSet)
        show_text(window, currentPlayer, occupiedBlack, occupiedWhite)
        
        #wenn alle aus stoneset nicht 0, dann der der am meisten Steine hat gewinnt.
        
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

if __name__ == '__main__':
    TESTING = False

    if TESTING:
        unittest.main()
    else:
        main()
