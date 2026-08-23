from typing import List, Optional


class Pin:
    x: float
    y: float
    outer_radius: float
    inner_radius: Optional[float]

    def __init__(self, x: float, y: float, outer_radius: float, inner_radius: Optional[float] = None):
        self.x = x
        self.y = y
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius


class Track:
    x: float
    y: float
    x_count: float
    y_count: float
    width: float

    def __init__(self, x: float, y: float, x_count: float, y_count: float, width: float):
        self.x = x
        self.y = y
        self.x_count = x_count
        self.y_count = y_count
        self.width = width


class MultiTrack:
    _x_start: float
    _y_start: float
    _width: float
    _tracks: List[Track]

    def __init__(self, x_start: int, y_start: int, width: float):
        self._x_start = x_start
        self._y_start = y_start
        self._width = width
        self._tracks = []

    def move(self, x_offset: float, y_offset: float) -> "MultiTrack":
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
