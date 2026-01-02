from typing import List

import shapely
import trimesh
from PIL import Image, ImageDraw
from trimeshtools.move import move_to_bound
from trimeshtools.show import show_mesh

from lib.constants import CYLINDER_SECTIONS
from lib.pattern.structs import Board, Pin, Track


class BoardImageBuilder:
    _step: float  # в мм
    _board: Board
    _pins: List[Pin]
    _tracks: List[Track]
    _dpi: int
    _antialias_factor: int  # Коэффициент антиалиасинга

    def __init__(self, step: float, board: Board, pins: List[Pin], tracks: List[Track], dpi: int = 300, antialias_factor: int = 4):
        self._step = step
        self._board = board
        self._pins = pins
        self._tracks = tracks
        self._dpi = dpi
        self._antialias_factor = antialias_factor

    def _mm_to_pixels(self, mm: float) -> int:
        # 1 inch = 25.4 mm
        return int(mm * self._dpi / 25.4)

    def _mm_to_scaled_pixels(self, mm: float) -> int:
        return int(mm * self._dpi / 25.4 * self._antialias_factor)

    def build(self):
        width_mm = self._board.x_indent * 2 + self._board.x_count * self._step
        height_mm = self._board.y_indent * 2 + self._board.y_count * self._step

        scaled_width_px = self._mm_to_scaled_pixels(width_mm)
        scaled_height_px = self._mm_to_scaled_pixels(height_mm)

        image = Image.new('RGBA', (scaled_width_px, scaled_height_px), color=(255, 255, 255, 255))
        draw = ImageDraw.Draw(image)

        draw = self._place_board(self._board, draw)

        for track in self._tracks:
            draw = self._place_track(track, draw)

        for pin in self._pins:
            draw = self._place_pin(pin, draw)

        final_width = scaled_width_px // self._antialias_factor
        final_height = scaled_height_px // self._antialias_factor

        image = image.resize((final_width, final_height), Image.Resampling.LANCZOS)

        image = image.convert('RGB')

        return image

    def _place_board(self, board: Board, draw: ImageDraw.ImageDraw) -> ImageDraw.ImageDraw:
        left = self._mm_to_scaled_pixels(board.x_indent)
        top = self._mm_to_scaled_pixels(board.y_indent)
        right = self._mm_to_scaled_pixels(board.x_indent + board.x_count * self._step)
        bottom = self._mm_to_scaled_pixels(board.y_indent + board.y_count * self._step)

        left_outer = 0
        top_outer = 0
        right_outer = right + self._mm_to_scaled_pixels(board.x_indent)
        bottom_outer = bottom + self._mm_to_scaled_pixels(board.y_indent)

        draw.rectangle([left_outer, top_outer, right_outer, bottom_outer], outline='gray', width=2 * self._antialias_factor)

        for x in range(board.x_count + 1):
            x_pos_mm = board.x_indent + x * self._step
            x_pos = self._mm_to_scaled_pixels(x_pos_mm)
            draw.line([(x_pos, top), (x_pos, bottom)], fill='lightgray', width=1 * self._antialias_factor)

        for y in range(board.y_count + 1):
            y_pos_mm = board.y_indent + y * self._step
            y_pos = self._mm_to_scaled_pixels(y_pos_mm)
            draw.line([(left, y_pos), (right, y_pos)], fill='lightgray', width=1 * self._antialias_factor)

        return draw

    def _place_pin(self, pin: Pin, draw: ImageDraw.ImageDraw) -> ImageDraw.ImageDraw:
        center_x_mm = self._board.x_indent + pin.x * self._step + self._step / 2
        center_y_mm = self._board.y_indent + pin.y * self._step + self._step / 2

        center_x = self._mm_to_scaled_pixels(center_x_mm)
        center_y = self._mm_to_scaled_pixels(center_y_mm)

        radius_px = self._mm_to_scaled_pixels(pin.radius)

        outer_bbox = [
            center_x - radius_px,
            center_y - radius_px,
            center_x + radius_px,
            center_y + radius_px
        ]

        draw.ellipse(outer_bbox, fill='black')

        return draw

    def _place_track(self, track: Track, draw: ImageDraw.ImageDraw) -> ImageDraw.ImageDraw:
        start_x_mm = self._board.x_indent + track.x * self._step + self._step / 2
        start_y_mm = self._board.y_indent + track.y * self._step + self._step / 2

        end_x_mm = self._board.x_indent + (track.x + track.x_count) * self._step + self._step / 2
        end_y_mm = self._board.y_indent + (track.y + track.y_count) * self._step + self._step / 2

        start_x = self._mm_to_scaled_pixels(start_x_mm)
        start_y = self._mm_to_scaled_pixels(start_y_mm)
        end_x = self._mm_to_scaled_pixels(end_x_mm)
        end_y = self._mm_to_scaled_pixels(end_y_mm)

        width_px = max(self._antialias_factor, self._mm_to_scaled_pixels(track.width))

        draw.line([(start_x, start_y), (end_x, end_y)], fill='black', width=width_px)

        radius_px = max(self._antialias_factor, width_px // 2)

        draw.ellipse([
            start_x - radius_px, start_y - radius_px,
            start_x + radius_px, start_y + radius_px
        ], fill='black')

        draw.ellipse([
            end_x - radius_px, end_y - radius_px,
            end_x + radius_px, end_y + radius_px
        ], fill='black')

        return draw


class BoardMeshBuilder:
    _step: float  # в мм
    _board: Board
    _pins: List[Pin]
    _tracks: List[Track]
    _thickness: float

    def __init__(self, step: float, board: Board, pins: List[Pin], tracks: List[Track], thickness: float = 1.0):
        self._step = step
        self._board = board
        self._pins = pins
        self._tracks = tracks
        self._thickness = thickness

    def build(self) -> trimesh.Trimesh:
        final_mesh = self._place_board(self._board)

        for track in self._tracks:
            final_mesh = self._place_track(track, final_mesh)

        for pin in self._pins:
            final_mesh = self._place_pin(pin, final_mesh)

        return final_mesh

    def _place_board(self, board: Board) -> trimesh.Trimesh:
        width = board.x_indent*2 + board.x_count*self._step
        height = board.y_indent*2 + board.y_count*self._step

        final_mesh = trimesh.creation.box([width, height, self._thickness])
        move_to_bound(final_mesh, 1, 1, 1)
        final_mesh.apply_translation([-board.x_indent, -board.y_indent, 0])

        return final_mesh

    def _place_pin(self, pin: Pin, final_mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        center_x = pin.x*self._step + self._step/2
        center_y = pin.y*self._step + self._step/2

        pin = trimesh.creation.cylinder(radius=pin.radius, height=self._thickness*2, sections=CYLINDER_SECTIONS)
        pin.apply_translation([center_x, center_y, 0])

        final_mesh = final_mesh.difference(pin)
        return final_mesh

    def _place_track(self, track: Track, final_mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        start_x = track.x*self._step + self._step/2
        start_y = track.y*self._step + self._step/2

        end_x = (track.x + track.x_count)*self._step + self._step/2
        end_y = (track.y + track.y_count)*self._step + self._step/2

        # Create a line segment for the track path
        track_line = trimesh.load_path([
            [start_x, start_y, 0],
            [end_x, end_y, 0]
        ])

        # Create a rectangle polygon for the track cross-section
        width = track.width
        half_width = width / 2

        # Define rectangle vertices (square with width = track.width)
        polygon = shapely.geometry.Polygon([
            [-half_width, -self._thickness*2],
            [half_width, -self._thickness*2],
            [half_width, self._thickness*2],
            [-half_width, self._thickness*2],
        ])

        # Sweep the rectangle along the line to create a 3D track
        track_mesh = trimesh.creation.sweep_polygon(
            polygon=polygon,
            path=track_line.vertices
        )

        # Subtract the track from the board
        final_mesh = final_mesh.difference(track_mesh)

        cylinder_mesh = trimesh.creation.cylinder(radius=track.width/2, height=self._thickness*2, sections=CYLINDER_SECTIONS)
        cylinder_mesh.apply_translation([start_x, start_y, 0])
        final_mesh = final_mesh.difference(cylinder_mesh)

        return final_mesh
