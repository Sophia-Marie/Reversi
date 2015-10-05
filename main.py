import pygame


# to do: Regeln und 2 Spieler sollen spielen können.

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
                
                if PLAYER==BLACK:
                    stoneSet[i]=1
                    PLAYER= WHITE
                    
                else :
                    stoneSet[i]=2
                    PLAYER=BLACK
                    
        else:
            pygame.draw.rect(window, GREEN, positionList)
    
        if stoneSet[i]==1:
            pygame.draw.circle(window, BLACK, (positionList[0]+35, positionList[1]+35), 25)
        elif stoneSet[i]==2:
            pygame.draw.circle(window, WHITE,(positionList[0]+35, positionList[1]+35), 25)
        else:
            pass
#Klasse draw_field:

def available_Moves_horizontal(p, direction, foundOpponent = False):
    p += direction

    print "stoneSet[p]:", stoneSet[p]

    if not foundOpponent:
        if PLAYER==BLACK:
            foundOpponent = stoneSet[p] == 2
        else:
            foundOpponent = stoneSet[p] == 1
            
    MODULO_OFFSET=1 # Because modulo works best with even numbers
    LEFT_BORDER_OFFSET=7 # Modulo checks right border, this offset simulates a right border when it is actually the left border

    if (p+MODULO_OFFSET)%8 == 0 or (p+MODULO_OFFSET+LEFT_BORDER_OFFSET)%8 == 0:
        print "end of recursion (border) p={}, foundOpponent={}".format(p, foundOpponent)
        return False
    elif stoneSet[p] == 0:
        print "end of recursion (empty field) p={}, foundOpponent={}".format(p, foundOpponent)
        return False        
    elif stoneSet[p] == (2 if PLAYER == WHITE else 1):
        print "end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
        return foundOpponent
    else:
        print "recursive call p={}, foundOpponent={}".format(p, foundOpponent)
        return available_Moves_horizontal(p, direction, foundOpponent)

def available_Moves_horizontal_flip(p, direction, foundOpponent = False):
    p += direction
    if stoneSet[p] == (2 if PLAYER == WHITE else 1):
        print "[FLIP] end of recursion (own stone) p={}, foundOpponent={}".format(p, foundOpponent)
        return
    else:
        print "[FLIP] coloring and recursive call p={}, foundOpponent={}".format(p, foundOpponent)
        stoneSet[p] = 2 if PLAYER == WHITE else 1
        return available_Moves_horizontal_flip(p, direction, foundOpponent)    


           
    #circle(Surface, color, pos, radius, width=0)
def draw_buttons(mouseX, mouseY, clicked):
    mousePosition= pygame.mouse.get_pos()
    # New Game Button
    if 100 > mouseX > 50 and 70 > mouseY > 50 and clicked==1:
        pygame.draw.rect(window, GREY, (50,50,50,20))
        
    else:
        pygame.draw.rect(window, WHITE, (50, 50, 50, 20))



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

PLAYER = BLACK

# first call of functions
allPositionsRect = calculate_position()
stoneSet= stones_set()

#Klasse:
window.fill(BROWN)

#Grundaufstellung
stoneSet[27] = 1
stoneSet[28] = 2
stoneSet[35] = 2
stoneSet[36] = 1

# Test
stoneSet[9] = 1
stoneSet[10] = 2
stoneSet[12] = 2
stoneSet[13] = 1


def analyseAndFlip(direction):
    print "--- analysis start --- PLAYER: {}".format("BLACK" if PLAYER == BLACK else "WHITE")
    flipOk = available_Moves_horizontal(positionArrow, direction)

    if flipOk:
        print "--- flip start --- PLAYER: {}".format("BLACK" if PLAYER == BLACK else "WHITE")
        available_Moves_horizontal_flip(positionArrow, direction)
        print "--- flip end --- PLAYER: {}".format("BLACK" if PLAYER == BLACK else "WHITE")        

    print "--- analysis end --- PLAYER: {}".format("BLACK" if PLAYER == BLACK else "WHITE")
    print
    return flipOk

gameLoop=True
while gameLoop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop=False
            
    mouseX, mouseY = get_mouse_position()
    clicked = check_mouse_pressed()
    draw_buttons(mouseX, mouseY, clicked)
    positionArrow = check_mouse_position(allPositionsRect, mouseX, mouseY)

    #flipOk = analyseAndFlip(1) if positionArrow and clicked else False

    if positionArrow and clicked:
        rightFlipOk = analyseAndFlip(1)
        leftFlipOk = analyseAndFlip(-1)
        flipOk = leftFlipOk or rightFlipOk
    else:
        flipOk = False

    draw_Field(window, allPositionsRect, positionArrow, stoneSet, clicked, flipOk)
    #wenn alle aus stoneset nicht 0, dann der der am meisten Steine hat gewinnt.
    
    pygame.display.flip()
    
pygame.quit()
