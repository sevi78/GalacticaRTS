from pygame import Rect


class Point:
    def __init__(self, x: int, y: int, width:int, height:int, layer:int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.layer = layer
        self.rect = Rect(0, 0, 0, 0)
        self.selected = False

    def __str__(self):
        return f"Point(x={self.x}, y={self.y}, width={self.width}, height={self.height})"
