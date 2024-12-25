import math
import pygame


class FlailPiece:
    def __init__(self, distance, color, rad):
        self.distance = distance
        self.color = color
        self.rad = rad
        self.mpointX = 0
        self.mpointY = 0

    def calculatePos(self, xPos, centerY, xAxis, yAxis):
        self.mpointX = (int(xPos) + (math.cos(xAxis) * self.distance))
        self.mpointY = (centerY + (math.sin(yAxis) * self.distance))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.mpointX), int(self.mpointY)), int(self.rad))


def checkCollision(mX, mY, flail, bRad):
    if math.sqrt((mX - flail.mpointX) ** 2 + (mY - flail.mpointY) ** 2) <= bRad:
        flail.color = (0, 255, 0)
    else:
        flail.color = (255, 0, 0)


pygame.display.init()

winx, winy = 600, 600
screen = pygame.display.set_mode((winx, winy))
pygame.display.set_caption("Flail")

flailSpeed = 0.0005

done = False
xAxis = 0
xCoefficient = flailSpeed

yAxis = 0
yCoefficient = flailSpeed

centerX = int(winx / 2)
centerY = int(winy / 2)

bRad = 20

xPos = centerX

cCol = (255, 0, 0)
pointRad = 5

flailPieces = []
totalFlailDistance = centerY
flailPieceDistance = bRad * 2

curD = flailPieceDistance
for i in range(int(totalFlailDistance / flailPieceDistance)):
    f = FlailPiece(curD, cCol, bRad)
    flailPieces.append(f)
    curD += flailPieceDistance

clockwise = False
while not done:
    mX, mY = pygame.mouse.get_pos()

    if clockwise:
        xAxis += xCoefficient
        yAxis += yCoefficient
    else:
        xAxis -= xCoefficient
        yAxis -= yCoefficient

    if xCoefficient >= 1.0:
        xCoefficient *= -1

    if xCoefficient <= -1.0:
        xCoefficient *= -1

    if yCoefficient >= 1.0:
        yCoefficient *= -1

    if yCoefficient <= -1.0:
        yCoefficient *= -1

    for f in flailPieces:
        f.calculatePos(xPos, centerY, xAxis, yAxis)
        checkCollision(mX, mY, f, bRad)

    events = pygame.event.get()

    for e in events:
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                done = True
        if e.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))

    for f in flailPieces:
        f.draw(screen)

    pygame.draw.circle(screen, cCol, (int(xPos), centerY), pointRad)
    pygame.display.flip()

pygame.display.quit()