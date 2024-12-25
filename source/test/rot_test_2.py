"""
https://github.com/Kingcitaldo125/PygamePointRotation
"""
import math
import pygame

pygame.display.init()

winx, winy = 800, 600
screen = pygame.display.set_mode((winx, winy))

done = False
xAxis = 0
xCoefficient = 0.001

yAxis = 0
yCoefficient = 0.001

centerX = int(winx / 2)
centerY = int(winy / 2)

bRad = 50

xPos = 400
xPosCoefficient = 0.01

cCol = (255, 0, 0)
pointRad = 5
flailDistance = 100

clockwise = False
while not done:
    mX, mY = pygame.mouse.get_pos()

    if clockwise:
        xAxis += xCoefficient
        yAxis += yCoefficient
    else:
        xAxis -= xCoefficient
        yAxis -= yCoefficient

    xPos += xPosCoefficient

    if xCoefficient >= 1.0:
        xCoefficient *= -1

    if xCoefficient <= -1.0:
        xCoefficient *= -1

    if yCoefficient >= 1.0:
        yCoefficient *= -1

    if yCoefficient <= -1.0:
        yCoefficient *= -1

    if xPos > winx - (bRad + flailDistance - pointRad):
        xPosCoefficient *= -1

    if xPos < bRad + flailDistance - pointRad:
        xPosCoefficient *= -1

    mpointX = (int(xPos) + (math.cos(xAxis) * flailDistance))
    mpointY = (centerY + (math.sin(yAxis) * flailDistance))

    if math.sqrt((mX - mpointX) ** 2 + (mY - mpointY) ** 2) <= bRad:
        cCol = (0, 255, 0)
    else:
        cCol = (255, 0, 0)

    events = pygame.event.get()

    for e in events:
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                done = True
        if e.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, cCol, (int(mpointX), int(mpointY)), int(bRad))
    pygame.draw.circle(screen, cCol, (int(xPos), centerY), pointRad)
    pygame.draw.line(screen, cCol, (int(mpointX), int(mpointY)), (int(xPos), centerY))
    pygame.display.flip()

pygame.display.quit()