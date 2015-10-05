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

def available_Moves_horizontal_right(p):
    p=p+1
    modulo_offset=1
    rightBoarder= (p+modulo_offset)%8
    if PLAYER==BLACK:
        if stoneSet[p]==2:
            availableMove=True
        else:
            availableMove=False
    else:
        if stoneSet[p]==1:
            availableMove=True
        else:
            availableMove=False
            
    if rightBoarder!=0:
        available_Moves_horizontal_right(p)
    else:
        None
    return availableMove

##def available_moves_horizontal_left():
##    p=p-1
##    leftBoarder= p%8
##    if PLAYER==BLACK:
##        if stoneSet[p]==2:
##            availableMove=True
##        else:
##            availableMove=False
##    else:
##        if stoneSet[p]==1:
##            availableMove=True
##        else:
##            availableMove=False 
##
##    if leftBoarder!=0:
##        available_moves_horizontal_left(p)
##    else:
##        None
##
##    return availableMove
##
##def available_moves_vertikal_up():
##    
##    p=p+8
##    if PLAYER==BLACK:
##        if stoneSet[p]==2:
##            availableMove=True
##        else:
##            availableMove=False
##    else:
##        if stoneSet[p]==1:
##            availableMove=True
##        else:
##            availableMove=False
##    #if boarder at top reached
##    if p>=1:
##        available_moves_vertikal_up(p):
##    else:
##        None
##
##    return availableMove
##
##def available_moves_vertikal_down():
##    
##    p=p+8
##    if PLAYER==BLACK:
##        if stoneSet[p]==2:
##            availableMove=True
##        else:
##            availableMove=False
##    else:
##        if stoneSet[p]==1:
##            availableMove=True
##        else:
##            availableMove=False
##    #if boarder at top reached
##    if p<=62:
##        available_moves_vertikal_down(p):
##    else:
##        None
##
##    return availableMove
    
        
       
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


gameLoop=True
while gameLoop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop=False
            
    mouseX, mouseY = get_mouse_position()
    clicked = check_mouse_pressed()
    draw_buttons(mouseX, mouseY, clicked)
    positionArrow=check_mouse_position(allPositionsRect, mouseX, mouseY)
    p=0
    if clicked==1:
        p=positionArrow
    availableMove=available_Moves_horizontal_right(p)
    draw_Field(window, allPositionsRect, positionArrow, stoneSet,clicked, availableMove)
    #wenn alle aus stoneset nicht 0, dann der der am meisten Steine hat gewinnt.
    
    pygame.display.flip()
    
pygame.quit()
