from typing import List
from PIL import Image, ImageDraw

from lib.pattern.structs import Board, Pin, Track


class BoardImageBuilder:
    _step: float
    _board: Board
    _pins: List[Pin]
    _tracks: List[Track]

    def __init__(self, step: float, board: Board, pins: List[Pin], tracks: List[Track]):
        self._step = step
        self._board = board
        self._pins = pins
        self._tracks = tracks

    def build(self):
        width = int((self._board.x_indent*2 + self._board.x_count-1)*self._step)
        height = int((self._board.y_indent*2 + self._board.y_count-1)*self._step)

        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)

        draw = self._place_board(self._board, draw)

        for track in self._tracks:
            draw = self._place_track(track, draw)

        for pin in self._pins:
            draw = self._place_pin(pin, draw)

        return image

    def _place_board(self, board: Board, draw: ImageDraw.ImageDraw) -> ImageDraw.ImageDraw:
        left = board.x_indent
        top = board.y_indent
        right = left + (board.x_count - 1)*self._step
        bottom = top + (board.y_count - 1)*self._step

        draw.rectangle([left, top, right, bottom], outline='black', width=2)

        for x in range(board.x_count):
            x_pos = left + x*self._step
            draw.line([(x_pos, top), (x_pos, bottom)], fill='lightgray', width=1)

        for y in range(board.y_count):
            y_pos = top + y*self._step
            draw.line([(left, y_pos), (right, y_pos)], fill='lightgray', width=1)

        return draw

    def _place_pin(self, pin: Pin, draw: ImageDraw.ImageDraw) -> ImageDraw.ImageDraw:
        center_x = self._board.x_indent + pin.x*self._step
        center_y = self._board.y_indent + pin.y*self._step

        outer_bbox = [
            center_x - pin.outer_radius,
            center_y - pin.outer_radius,
            center_x + pin.outer_radius,
            center_y + pin.outer_radius
        ]
        draw.ellipse(outer_bbox, fill='black')

        if pin.inner_radius > 0:
            inner_bbox = [
                center_x - pin.inner_radius,
                center_y - pin.inner_radius,
                center_x + pin.inner_radius,
                center_y + pin.inner_radius
            ]
            draw.ellipse(inner_bbox, fill='white')

        return draw

    def _place_track(self, track: Track, draw: ImageDraw.ImageDraw) -> ImageDraw.ImageDraw:
        start_x = self._board.x_indent + track.x*self._step
        start_y = self._board.y_indent + track.y*self._step

        end_x = self._board.x_indent + (track.x + track.x_count)*self._step
        end_y = self._board.y_indent + (track.y + track.y_count)*self._step

        draw.line([(start_x, start_y), (end_x, end_y)], fill='black', width=round(track.width))
        draw.ellipse([start_x-track.width, start_y-track.width, start_x+track.width, start_y+track.width], fill='black')
        draw.ellipse([end_x-track.width, end_y-track.width, end_x+track.width, end_y+track.width], fill='black')

        return draw
