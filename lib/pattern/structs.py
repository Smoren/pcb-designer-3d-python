from typing import List


class Pin:
    x: int
    y: int
    radius: float

    def __init__(self, x: int, y: int, radius: float):
        self.x = x
        self.y = y
        self.radius = radius


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


class MultiTrack:
    _x_start: int
    _y_start: int
    _width: float
    _tracks: List[Track]

    def __init__(self, x_start: int, y_start: int, width: float):
        self._x_start = x_start
        self._y_start = y_start
        self._width = width
        self._tracks = []

    def move(self, x_offset: int, y_offset: int) -> "MultiTrack":
        self._tracks.append(Track(
            x=self._x_start,
            y=self._y_start,
            x_count=x_offset,
            y_count=y_offset,
            width=self._width,
        ))

        self._x_start += x_offset
        self._y_start += y_offset

        return self

    @property
    def tracks(self) -> List[Track]:
        return list(self._tracks)


class BoardPattern:
    x_count: int
    y_count: int
    x_indent: float
    y_indent: float

    pins: List[Pin]
    tracks: List[Track]

    def __init__(self, x_count: int, y_count: int, x_indent: float, y_indent: float, pins: List[Pin], tracks: List[Track]):
        self.x_count = x_count
        self.y_count = y_count
        self.x_indent = x_indent
        self.y_indent = y_indent

        self.pins = pins
        self.tracks = tracks
