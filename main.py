import pygame


def check_mouse_position(allPositionsRect, mouseX, mouseY):
    for i, positionList, in enumerate(allPositionsRect):
        if positionList[0] < mouseX < positionList[0]+positionList[2] and positionList[1] < mouseY < positionList[1]+positionList[3]:
            return i
        
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


def draw_Field(window, allPositionsRect, positionArrow, stoneSet, clicked):
    
    global PLAYER
    
    for i, positionList in enumerate(allPositionsRect):
        
        if positionArrow==i:
            pygame.draw.rect(window, PINK, positionList)
            
            if clicked==1 and stoneSet[i]==0:
                
                pygame.draw.circle(window, PLAYER, (positionList[0]+35, positionList[1]+35), 25)
                
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

    window.fill(BROWN)
    mouseX, mouseY = get_mouse_position()
    clicked = check_mouse_pressed()
    draw_buttons(mouseX, mouseY, clicked)
    positionArrow=check_mouse_position(allPositionsRect, mouseX, mouseY)
    draw_Field(window, allPositionsRect, positionArrow, stoneSet,clicked)

    #wenn alle aus stoneset nicht 0, dann der der am meisten Steine hat gewinnt.
    
    pygame.display.flip()
    
pygame.quit()
