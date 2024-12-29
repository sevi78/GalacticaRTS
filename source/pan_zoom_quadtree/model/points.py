class Point:
    def __init__(self, x: int, y: int, width:int, height:int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return f"Point(x={self.x}, y={self.y}, width={self.width}, height={self.height})"
