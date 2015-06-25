import pygame

def draw_Field(colour):
    colour= colour
    positionList = [100, 100, 70, 70]
    for position in range(1,65):
        pygame.draw.rect(window, colour, positionList)
        if position !=0 and position %8==0:
            positionList[1] +=72
            positionList[0] = 100
        else :
            positionList[0] +=72


def statusColour():
    statusRect= pygame.mouse.get_pressed()
    statusColour=(0,0,0)
    
    if statusRect==True:
        statusColour= PINK
        
    else :
        statusColour= GREEN

    return statusColour

pygame.init()

window = pygame.display.set_mode((800,700))

pygame.display.set_caption("Reversi")

#Colours
PINK  =  (102, 0, 51)
GREEN = (51,102,0)
BROWN = (80,26,26)
BLACK = (0,0,0)
WHITE = (255,255,255)

gameLoop=True
while gameLoop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop=False

    window.fill(BROWN)

    colour= statusColour()
    draw_Field(colour)

    pygame.display.flip()
pygame.quit()
