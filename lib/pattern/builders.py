from typing import List
from PIL import Image, ImageDraw

from lib.pattern.structs import Board, Pin, Track


class BoardImageBuilder:
    _step: float  # в мм
    _board: Board
    _pins: List[Pin]
    _tracks: List[Track]
    _dpi: int

    def __init__(self, step: float, board: Board, pins: List[Pin], tracks: List[Track], dpi: int = 300):
        self._step = step
        self._board = board
        self._pins = pins
        self._tracks = tracks
        self._dpi = dpi

    def _mm_to_pixels(self, mm: float) -> int:
        # 1 inch = 25.4 mm
        return int(mm * self._dpi / 25.4)

    def build(self):
        width_mm = (self._board.x_indent * 2 + (self._board.x_count - 1) * self._step)
        height_mm = (self._board.y_indent * 2 + (self._board.y_count - 1) * self._step)

        width_px = self._mm_to_pixels(width_mm)
        height_px = self._mm_to_pixels(height_mm)

        image = Image.new('RGB', (width_px, height_px), color='white')
        draw = ImageDraw.Draw(image)

        draw = self._place_board(self._board, draw)

        for track in self._tracks:
            draw = self._place_track(track, draw)

        for pin in self._pins:
            draw = self._place_pin(pin, draw)

        return image

    def _place_board(self, board: Board, draw: ImageDraw.ImageDraw) -> ImageDraw.ImageDraw:
        left = self._mm_to_pixels(board.x_indent)
        top = self._mm_to_pixels(board.y_indent)
        right = self._mm_to_pixels(board.x_indent + (board.x_count - 1) * self._step)
        bottom = self._mm_to_pixels(board.y_indent + (board.y_count - 1) * self._step)

        draw.rectangle([left, top, right, bottom], outline='black', width=1)

        for x in range(board.x_count):
            x_pos_mm = board.x_indent + x * self._step
            x_pos = self._mm_to_pixels(x_pos_mm)
            draw.line([(x_pos, top), (x_pos, bottom)], fill='lightgray', width=1)

        for y in range(board.y_count):
            y_pos_mm = board.y_indent + y * self._step
            y_pos = self._mm_to_pixels(y_pos_mm)
            draw.line([(left, y_pos), (right, y_pos)], fill='lightgray', width=1)

        return draw

    def _place_pin(self, pin: Pin, draw: ImageDraw.ImageDraw) -> ImageDraw.ImageDraw:
        center_x_mm = self._board.x_indent + pin.x * self._step
        center_y_mm = self._board.y_indent + pin.y * self._step

        center_x = self._mm_to_pixels(center_x_mm)
        center_y = self._mm_to_pixels(center_y_mm)

        outer_radius_px = self._mm_to_pixels(pin.outer_radius)
        inner_radius_px = self._mm_to_pixels(pin.inner_radius) if pin.inner_radius > 0 else 0

        outer_bbox = [
            center_x - outer_radius_px,
            center_y - outer_radius_px,
            center_x + outer_radius_px,
            center_y + outer_radius_px
        ]
        draw.ellipse(outer_bbox, fill='black')

        if inner_radius_px > 0:
            inner_bbox = [
                center_x - inner_radius_px,
                center_y - inner_radius_px,
                center_x + inner_radius_px,
                center_y + inner_radius_px
            ]
            draw.ellipse(inner_bbox, fill='white')

        return draw

    def _place_track(self, track: Track, draw: ImageDraw.ImageDraw) -> ImageDraw.ImageDraw:
        start_x_mm = self._board.x_indent + track.x * self._step
        start_y_mm = self._board.y_indent + track.y * self._step

        end_x_mm = self._board.x_indent + (track.x + track.x_count) * self._step
        end_y_mm = self._board.y_indent + (track.y + track.y_count) * self._step

        start_x = self._mm_to_pixels(start_x_mm)
        start_y = self._mm_to_pixels(start_y_mm)
        end_x = self._mm_to_pixels(end_x_mm)
        end_y = self._mm_to_pixels(end_y_mm)

        width_px = max(1, self._mm_to_pixels(track.width))
        draw.line([(start_x, start_y), (end_x, end_y)], fill='black', width=width_px)

        radius_px = max(1, width_px)
        draw.ellipse([
            start_x-radius_px, start_y-radius_px,
            start_x+radius_px, start_y+radius_px
        ], fill='black')
        draw.ellipse([
            end_x-radius_px, end_y-radius_px,
            end_x+radius_px, end_y+radius_px
        ], fill='black')

        return draw
