import pygame

def check_mouse_position(allPositionsRect):
    mousex,mousey = pygame.mouse.get_pos()
    for i, positionList in enumerate(allPositionsRect):
        if positionList[0] < mousex < positionList[0]+positionList[2] and positionList[1] < mousey < positionList[1]+positionList[3]:
            return i
        
        

def calculate_position():
    positionList = [100, 100, 70, 70]
    allPositions=[list(positionList)]
    for position in range(1,65):
        if position !=0 and position %8==0:
            positionList[1] +=72
            positionList[0] = 100
        else:
            positionList[0] +=72
        allPositions.append(list(positionList))
    return allPositions


def draw_Field(window, allPositionsRect):
    for positionList in allPositionsRect:
        pygame.draw.rect(window, GREEN, positionList)
    
def draw_buttons():
    mousePosition= pygame.mouse.get_pos()
    clicked= pygame.mouse.get_pressed()[0]
    
    if 100 > mousePosition[0] > 50 and 70 > mousePosition[1] > 50 and clicked==1:
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
    draw_buttons()
    allPositionsRect = calculate_position()
    clicked=check_mouse_position(allPositionsRect)
    print clicked
    draw_Field(window, allPositionsRect)

    pygame.display.flip()
pygame.quit()
