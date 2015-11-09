import pygame
from time import sleep

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


def draw_Field(window, allPositionsRect, positionArrow, stoneSet, clicked, availableMove):
    global PLAYER
    
    for i, positionList in enumerate(allPositionsRect):
        
        if positionArrow==i:

            pygame.draw.rect(window, PINK, positionList)

            if clicked==1 and stoneSet[i]==0 and availableMove==True:
                
              #  pygame.draw.circle(window, PLAYER, (positionList[0]+35, positionList[1]+35), 25)
                
                if PLAYER==1:
                    stoneSet[i]=1
                    PLAYER= 2
                    
                else :
                    stoneSet[i]=2
                    PLAYER=1
                    
        else:
            pygame.draw.rect(window, GREEN, positionList)
    
        if stoneSet[i]==1:
            pygame.draw.circle(window, BLACK, (positionList[0]+35, positionList[1]+35), 25)
        elif stoneSet[i]==2:
            pygame.draw.circle(window, WHITE,(positionList[0]+35, positionList[1]+35), 25)
        else:
            pass

def available_Moves_horizontal(p, direction, foundOpponent = False):
    p += direction
    if 0<=p<=63:
        print "stoneSet[p]:", stoneSet[p]

        if not foundOpponent:
            if PLAYER==1:
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
            elif stoneSet[p] == (2 if PLAYER == 2 else 1):
                print "end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
                return foundOpponent
            else:
                print "recursive call p={}, foundOpponent={}".format(p, foundOpponent)
                return available_Moves_horizontal(p, direction, foundOpponent)
            
        if direction==-1 or direction==1:
            
            if (p+MODULO_OFFSET)%8 == 0 or (p+MODULO_OFFSET+LEFT_BORDER_OFFSET)%8 == 0:
                print "end of recursion (border) p={}, foundOpponent={}".format(p, foundOpponent)
                return False
            elif stoneSet[p] == 0:
                print "end of recursion (empty field) p={}, foundOpponent={}".format(p, foundOpponent)
                return False        
            elif stoneSet[p] == (2 if PLAYER == 2 else 1):
                print "end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
                return foundOpponent
            else:
                print "recursive call p={}, foundOpponent={}".format(p, foundOpponent)
                return available_Moves_horizontal(p, direction, foundOpponent)
        else:
            
            if (p+MODULO_OFFSET)%8 == 0 or (p+MODULO_OFFSET+LEFT_BORDER_OFFSET)%8 == 0 or (p>BOTTOM_BORDER_OFFSET) or (p<TOP_BORDER_OFFSET):
                print "end of recursion (border) p={}, foundOpponent={}".format(p, foundOpponent)
                return False
            elif stoneSet[p] == 0:
                print "end of recursion (empty field) p={}, foundOpponent={}".format(p, foundOpponent)
                return False        
            elif stoneSet[p] == (2 if PLAYER == 2 else 1):
                print "end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
                return foundOpponent
            else:
                print "recursive call p={}, foundOpponent={}".format(p, foundOpponent)
                return available_Moves_horizontal(p, direction, foundOpponent)
    else:
        None

def available_Moves_horizontal_flip(p, direction, foundOpponent = False):
    if 0<=p<=63:
        p += direction
        if stoneSet[p] == (2 if PLAYER == 2 else 1):
            print "[FLIP] end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
            return
        else:
            print "[FLIP] coloring and recursive call p={}, foundOpponent={}".format(p, foundOpponent)
            stoneSet[p] = 2 if PLAYER == 2 else 1
            return available_Moves_horizontal_flip(p, direction, foundOpponent)
    else:
        None
    
def analyseAndFlip(direction):
    print "--- analysis start --- PLAYER: {}".format("BLACK" if PLAYER == 1 else "WHITE")
    flipOk = available_Moves_horizontal(positionArrow, direction)

    if flipOk:
        print "--- flip start --- PLAYER: {}".format("BLACK" if PLAYER == 1 else "WHITE")
        available_Moves_horizontal_flip(positionArrow, direction)
        print "--- flip end --- PLAYER: {}".format("BLACK" if PLAYER == 1 else "WHITE")        

    print "--- analysis end --- PLAYER: {}".format("BLACK" if PLAYER == 1 else "WHITE")
    print
    return flipOk
           
    #circle(Surface, color, pos, radius, width=0)

def calc_occupied_stones():
    occupiedBlack=0
    occupiedWhite=0
    for i in stoneSet:
        if i == 1:
            occupiedBlack+=1
        elif i == 2:
            occupiedWhite+=1

    return occupiedBlack, occupiedWhite

def draw_buttons(mouseX, mouseY, clicked):
    mousePosition= pygame.mouse.get_pos()
    
    if 100 > mouseX > 50 and 70 > mouseY > 50 and clicked==1:
        pygame.draw.rect(window, GREY, (50,50,80,20))
        global stoneSet
        stoneSet = stones_set()
        #Grundaufstellung wiederherstellen    
        stoneSet[27] = 1
        stoneSet[28] = 2
        stoneSet[35] = 2
        stoneSet[36] = 1
        print "new game"
        
    else:
        pygame.draw.rect(window, WHITE, (50, 50, 80, 20))

    # New Game Button
    
    resetFont= pygame.font.Font(None, 16)
    resetText= resetFont.render("New Game", 1, BLACK)
    window.blit(resetText, (50,50,50,50))

def show_text(occupiedBlack, occupiedWhite):
    blackFont=pygame.font.Font(None, 18)
    blackText=blackFont.render("Player Black: {}".format(occupiedBlack), 1, BLACK)
    window.blit(blackText, (640,50,20,20))
    whiteFont=pygame.font.Font(None, 18)
    whiteText=blackFont.render("Player White: {}".format(occupiedWhite), 1, WHITE)
    window.blit(whiteText, (640,70,20,20))
##    = resetFont.render("{} , {}".format(a,b), 1, BLACK)


pygame.init()

window = pygame.display.set_mode((800,700))


pygame.display.set_caption("Reversi")

#global variables
#Colours

PINK  = (102, 0, 51)
GREEN = (51,102,0)
BROWN = (80,26,26)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY  = (160,160,160)

PLAYER = 1

# first call of functions
allPositionsRect = calculate_position()
stoneSet= stones_set()

#Grundaufstellung
stoneSet[27] = 1
stoneSet[28] = 2
stoneSet[35] = 2
stoneSet[36] = 1

### Test
##stoneSet[9] = 1
##stoneSet[10] = 2
##stoneSet[12] = 2
##stoneSet[13] = 1

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
    
    draw_buttons(mouseX, mouseY, clicked)
    positionArrow = check_mouse_position(allPositionsRect, mouseX, mouseY)

    #flipOk = analyseAndFlip(1) if positionArrow and clicked else False

    if positionArrow and clicked and stoneSet[positionArrow]==0:
        rightFlipOk = analyseAndFlip(1)
        leftFlipOk = analyseAndFlip(-1)
        upFlipOk = analyseAndFlip(8)
        downFlipOk = analyseAndFlip(-8)
        sevenFlipOk = analyseAndFlip(7)
        sevendownFlipOk = analyseAndFlip(-7)
        nineFlipOk= analyseAndFlip(9)
        ninedownFlipOk= analyseAndFlip(-9)
        flipOk = leftFlipOk or rightFlipOk or upFlipOk or downFlipOk or sevenFlipOk or sevendownFlipOk or nineFlipOk or ninedownFlipOk
    else:
        flipOk = False

    draw_Field(window, allPositionsRect, positionArrow, stoneSet, clicked, flipOk)

    occupiedBlack,occupiedWhite = calc_occupied_stones()
    show_text(occupiedBlack,occupiedWhite)
    
    #wenn alle aus stoneset nicht 0, dann der der am meisten Steine hat gewinnt.
    
    pygame.display.flip()

##    init = False
    
pygame.quit()
