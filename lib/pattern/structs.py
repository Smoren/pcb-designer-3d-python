class Board:
    x_count: int
    y_count: int
    x_indent: float
    y_indent: float

    def __init__(self, x_count: int, y_count: int, x_indent: float, y_indent: float):
        self.x_count = x_count
        self.y_count = y_count
        self.x_indent = x_indent
        self.y_indent = y_indent


class Pin:
    radius: float
    x: int
    y: int

    def __init__(self, radius: float, x: int, y: int):
        self.radius = radius
        self.x = x
        self.y = y


class Track:
    x: int
    y: int
    x_count: int
    y_count: int
    width: float

    def __init__(self, x: int, y: int, x_count: int, y_count: int, width: float):
        self.x = x
        self.y = y
        self.x_count = x_count
        self.y_count = y_count
        self.width = width