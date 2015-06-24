import pygame

pygame.init()

window = pygame.display.set_mode((800,700))

pygame.display.set_caption("Reversi")

GREEN = (51,102,0)
BROWN = (80,26,26)
gameLoop=True
while gameLoop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop=False

    window.fill(BROWN)

    positionList = [100, 100, 70, 70]
    for position in range(1,65):
        pygame.draw.rect(window, GREEN, positionList)
        if position !=0 and position %8==0:
            positionList[1] +=72
            positionList[0] = 100
        else :
            positionList[0] +=72

    pygame.display.flip()
pygame.quit()
