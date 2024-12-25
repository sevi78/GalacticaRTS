import pygame


def init(H, W, Title):
    pygame.init()
    win = pygame.display.set_mode((900, 900))
    pygame.display.set_caption(Title)
    pygame.font.init()
    return win


class Axis:
    vel = 2
    pxWidth = 1
    refRad = 3
    refZoom = 2
    refSpace = 50

    def __init__(self, center, color):
        self.center = (int(center[0]), int(center[1]))
        self.color = color

    def ref2T(self, tuple2):
        return (self.refX(tuple2[0]), self.refY(tuple2[1]))

    def refX(self, n: float):
        return int(n * self.refSpace + self.center[0])

    def refY(self, n: float):
        return int(-n * self.refSpace + self.center[1])

    def centerAdx(self, dx):
        self.center = (self.center[0] + int(dx), self.center[1])

    def centerAdy(self, dy):
        self.center = (self.center[0], self.center[1] + int(dy))

    def draw(self, win: pygame.Surface):
        pygame.draw.line(win, self.color, (self.center[0], 0),
                (self.center[0], h), self.pxWidth)
        pygame.draw.line(win, self.color, (0, self.center[1]),
                (w, self.center[1]), self.pxWidth)
        self.drawReferences(win)

    def drawReferences(self, win: pygame.Surface):
        for i in range(win.get_width() // (self.refSpace) + 1):
            pygame.draw.circle(win, self.color, (i * self.refSpace +
                                                 (self.center[0] % self.refSpace), self.center[1]), self.refRad)
        for i in range(win.get_height() // (self.refSpace) + 1):
            pygame.draw.circle(win, self.color, (self.center[0],
                                                 (self.center[1] % self.refSpace) + i * self.refSpace), self.refRad)


class Line:
    width = 2

    def __init__(self, startX, startY, endX, endY):
        self.start = (startX, startY)
        self.end = (endX, endY)

    def drawInAxis(self, axis, win):
        pygame.draw.line(win, (255, 255, 0), (axis.refX(self.start.x), axis.refY(
                self.start.y)), (axis.refX(self.end.x), axis.refY(self.end.y)), self.width)


class LineSet:
    width = 2

    def __init__(self, startX, startY, endX, endY):
        self.start = (startX, startY)
        self.end = (endX, endY)

    def drawInAxis(self, axis, win):
        pygame.draw.line(win, (255, 255, 0), (axis.refX(self.start.x), axis.refY(
                self.start.y)), (axis.refX(self.end.x), axis.refY(self.end.y)), self.width)


class Polygon:
    width = 2

    def __init__(self, points):
        self.points = points

    def drawInAxis(self, axis: Axis, win):
        truePoints = map(axis.ref2T, self.points)
        pygame.draw.polygon(win, (255, 0, 50), list(truePoints), self.width)


def checkActions(keys, axis, win):
    if keys[pygame.K_LEFT]:
        axis[0].centerAdx(-axis[0].vel)
    if keys[pygame.K_RIGHT]:
        axis[0].centerAdx(axis[0].vel)
    if keys[pygame.K_UP]:
        axis[0].centerAdy(-axis[0].vel)
    if keys[pygame.K_DOWN]:
        axis[0].centerAdy(axis[0].vel)
    if keys[pygame.K_u] and axis[0].refSpace <= win.get_width() / 2:

        for ax in axis:
            ax.refSpace += ax.refZoom

    #        axis[0].center[0] = axis[1].refX(((axis[0].center[0] - axis[1].center[0])/axis[1].refSpace))
    #       axis[0].center[1] = axis[1].refY(((axis[0].center[1] - axis[1].center[1])/axis[1].refSpace))

    if keys[pygame.K_y] and axis[0].refSpace > axis[0].refZoom:
        for ax in axis:
            ax.refSpace -= ax.refZoom


def drawMouseCursor(win):
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        pygame.draw.circle(win, (0, 0, 255), pygame.mouse.get_pos(), 5)


def printMousePosWin(win, font, axis):
    x, y = pygame.mouse.get_pos()
    x = round((x - axis.center[0]) / axis.refSpace, 2)
    y = -round((y - axis.center[1]) / axis.refSpace, 2)
    textsurface = font.render(str(x) + " " + str(y), False, (255, 0, 0))
    win.blit(textsurface, dest=(0, 0))


def renderInAxis(axis: Axis, win, list):
    axis.draw(win)
    for drawable in list:
        drawable.drawInAxis(axis, win)


def keepOpen():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


if __name__ == "__main__":

    win = init(500, 600, "2D graphs and transformations")
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    w, h = pygame.display.get_surface().get_size()

    axis = Axis((w / 2, h / 2), (255, 255, 0))
    axisBase = Axis((w / 2, h / 2), (100, 0, 0))
    axises = [axis, axisBase]
    triangle = Polygon([(-0.5, 0.5),
                        (4.5, 1.5),
                        (1.5, 3.5)])

    quadrilateral = Polygon([
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
        ])
    run = True

    while keepOpen():
        pygame.time.delay(1000 // 30)

        checkActions(pygame.key.get_pressed(), axises, win)

        win.fill((0, 0, 0))
        renderInAxis(axisBase, win, [])
        renderInAxis(axis, win, [triangle, quadrilateral])

        drawMouseCursor(win)
        printMousePosWin(win, font, axis)
        pygame.display.update()