import pygame

##
##class rectangle():
##    
##    def__init__(self, ):







def check_mouse_position(allPositionsRect, mouseX, mouseY):
    for i, positionList in enumerate(allPositionsRect):
        if positionList[0] < mouseX < positionList[0]+positionList[2] and positionList[1] < mouseY < positionList[1]+positionList[3]:
            return i
        
def get_mouse_position():
    mouseX,mouseY = pygame.mouse.get_pos()
    return mouseX, mouseY

        
def check_mouse_pressed():
    clicked= pygame.mouse.get_pressed()[0] 
    return clicked

def white_circle_list():
    posListCircle= [150,150]
    allPosCircle=[list(posListCircle)]

    for position in range(1,64):
        if position !=0 and position %8==0:
            posListCircle[1] +=72
            posListCircle[0] = 150
        else:
            posListCircle[0] +=72
        allPosCircle.append(list(posListCircle))
        
    whiteStonesList=[]
    for posListCircle in allPosCircle:
        whiteStone= pygame.draw.circle(window, WHITE, allPosCircle, 25)
        whiteStonesList.append(list(whitStone))
        
        
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


def draw_Field(window, allPositionsRect, positionArrow):
    for i, positionList in enumerate(allPositionsRect):
        
        if positionArrow==i:
            pygame.draw.rect(window, PINK, positionList)
        else:
            pygame.draw.rect(window, GREEN, positionList)
        
    #circle(Surface, color, pos, radius, width=0)
    #Grundaufstellung
    pygame.draw.circle(window, BLACK, (350, 350), 25)
    pygame.draw.circle(window, WHITE, (350+72, 350), 25)
    pygame.draw.circle(window, BLACK, (350+72, 350+72), 25)
    pygame.draw.circle(window, WHITE, (350, 350+72), 25)

    
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

#Colours
PINK  = (102, 0, 51)
GREEN = (51,102,0)
BROWN = (80,26,26)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY  = (160,160,160)

gameLoop=True
while gameLoop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop=False

    window.fill(BROWN)
    mouseX, mouseY = get_mouse_position()
    clicked = check_mouse_pressed()
    draw_buttons(mouseX, mouseY, clicked)
    allPositionsRect = calculate_position()
    positionArrow=check_mouse_position(allPositionsRect, mouseX, mouseY)
    print positionArrow
    draw_Field(window, allPositionsRect, positionArrow)
    #white_circle_list()

    pygame.display.flip()
pygame.quit()
