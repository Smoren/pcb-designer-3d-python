import math
import hashlib
import trimesh
import numpy as np
from typing import Dict, Optional

from trimeshtools.combine import union_meshes, concatenate_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_z

from lib.base import BaseMeshBuilder, FloatPosition3d, Rotation, PositionSide
from lib.constants import CYLINDER_SECTIONS
from lib.pattern.structs import BoardPattern, Pin, Track, Side


class PrototypingBoardBuilder(BaseMeshBuilder):
    _x_count: int
    _y_count: int
    _step: float
    _pad_radius: float
    _contact_pad_radius: float
    _contact_pad_thickness: float
    _thickness: float
    _x_indent: float
    _y_indent: float
    _color: np.ndarray
    _contact_pad_color: np.ndarray

    def __init__(
        self,
        x_count: int,
        y_count: int,
        step: float,
        pad_radius: float,
        contact_pad_radius: float,
        contact_pad_thickness: float,
        thickness: float,
        x_indent: float,
        y_indent: float,
        color: np.ndarray,
        contact_pad_color: np.ndarray,
    ):
        self._x_count = x_count
        self._y_count = y_count
        self._step = step
        self._pad_radius = pad_radius
        self._contact_pad_radius = contact_pad_radius
        self._contact_pad_thickness = contact_pad_thickness
        self._thickness = thickness
        self._x_indent = x_indent
        self._y_indent = y_indent
        self._color = color
        self._contact_pad_color = contact_pad_color

    def build(self) -> trimesh.Trimesh:
        board_mesh = trimesh.creation.box([self._step*self._x_count + self._x_indent*2, self._step*self._y_count + self._y_indent*2, self._thickness-self._contact_pad_thickness*2])

        move_to_bound(board_mesh, 1, 1, 0)
        diff_mesh = trimesh.creation.cylinder(radius=self._pad_radius, height=self._thickness*2, sections=CYLINDER_SECTIONS)
        union_mesh = trimesh.creation.cylinder(radius=self._contact_pad_radius, height=self._thickness, sections=CYLINDER_SECTIONS)
        union_mesh = union_mesh.difference(diff_mesh)

        diff_mesh = trimesh.creation.cylinder(radius=(self._pad_radius + self._contact_pad_radius)/2, height=self._thickness*2, sections=CYLINDER_SECTIONS)

        for i in range(self._x_count):
            for j in range(self._y_count):
                board_mesh = board_mesh.difference(diff_mesh.copy().apply_translation([
                    self._x_indent + self._step / 2 + i * self._step,
                    self._y_indent + self._step / 2 + j * self._step,
                    0
                ]))

        contact_pads = []
        for i in range(self._x_count):
            for j in range(self._y_count):
                contact_pads.append(union_mesh.copy().apply_translation([
                    self._x_indent + self._step / 2 + i * self._step,
                    self._y_indent + self._step / 2 + j * self._step,
                    0
                ]))
        contact_pads = union_meshes(*contact_pads)

        board_mesh.visual.face_colors = self._color
        contact_pads.visual.face_colors = self._contact_pad_color

        return concatenate_meshes(board_mesh, contact_pads)

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        if rotation.is_horizontal:
            return (
                -self._step/2 - self._x_indent,
                -self._step/2 - self._y_indent,
                -self._thickness/2
            )
        if rotation.is_vertical:
            return (
                -self._step/2 - self._y_indent,
                -self._step/2 - self._x_indent,
                -self._thickness/2
            )
        raise Exception(f"Invalid rotation for {self.__class__.__name__}")  # TODO custom exception


class PrintedBoardBuilder(BaseMeshBuilder):
    _board_pattern: BoardPattern
    _step: float
    _pad_radius: float
    _contact_pad_radius: float
    _contact_pad_thickness: float
    _thickness: float
    _color: np.ndarray
    _contact_pad_color: np.ndarray
    _track_color: np.ndarray

    def __init__(
        self,
        board_pattern: BoardPattern,
        step: float,
        pad_radius: float,
        contact_pad_radius: float,
        contact_pad_thickness: float,
        thickness: float,
        color: np.ndarray,
        contact_pad_color: np.ndarray,
        track_color: np.ndarray,
    ):
        self._board_pattern = board_pattern
        self._step = step
        self._pad_radius = pad_radius
        self._contact_pad_radius = contact_pad_radius
        self._contact_pad_thickness = contact_pad_thickness
        self._thickness = thickness
        self._color = color
        self._contact_pad_color = contact_pad_color
        self._track_color = track_color

    @property
    def cache_key(self) -> str:
        # Базовый cache_key строится из str() всех атрибутов, а repr паттерна
        # слишком длинный для имени файла в файловом кэше, поэтому используем хэш.
        payload = '|'.join([
            repr(self._board_pattern),
            str(self._step),
            str(self._pad_radius),
            str(self._contact_pad_radius),
            str(self._contact_pad_thickness),
            str(self._thickness),
            str(list(self._color)),
            str(list(self._contact_pad_color)),
            str(list(self._track_color)),
        ])
        digest = hashlib.sha1(payload.encode()).hexdigest()
        return f'{self.__class__.__name__}_{digest}'

    def build(self) -> trimesh.Trimesh:
        board_mesh = self._place_board(self._board_pattern)
        front_tracks_mesh = self._place_tracks(Side.FRONT)
        back_tracks_mesh = self._place_tracks(Side.BACK)
        pads_mesh = self._place_pads()

        board_mesh.visual.face_colors = self._color
        pads_mesh.visual.face_colors = self._contact_pad_color

        final_meshes = [board_mesh, pads_mesh]
        for tracks_mesh in (front_tracks_mesh, back_tracks_mesh):
            if tracks_mesh is not None:
                tracks_mesh.visual.face_colors = self._track_color
                final_meshes.append(tracks_mesh)

        return concatenate_meshes(*final_meshes)

    def _place_board(self, board: BoardPattern) -> trimesh.Trimesh:
        width = board.x_indent*2 + board.x_count*self._step
        height = board.y_indent*2 + board.y_count*self._step

        board_mesh = trimesh.creation.box([width, height, self._thickness - self._contact_pad_thickness*2])
        move_to_bound(board_mesh, 1, 1, 0)

        hole_mesh = trimesh.creation.cylinder(
            radius=(self._pad_radius + self._contact_pad_radius)/2,
            height=self._thickness*2,
            sections=CYLINDER_SECTIONS,
        )

        for pin in board.pins:
            center_x = board.x_indent + pin.x*self._step + self._step/2
            center_y = board.y_indent + pin.y*self._step + self._step/2
            board_mesh = board_mesh.difference(hole_mesh.copy().apply_translation([center_x, center_y, 0]))

        return board_mesh

    def _place_tracks(self, side: Side) -> Optional[trimesh.Trimesh]:
        track_meshes = [
            self._create_track_mesh(track, self._get_track_z_center(side))
            for track in self._board_pattern.tracks
            if track.side == side or track.side == Side.BOTH
        ]

        if not track_meshes:
            return None

        tracks_mesh = union_meshes(*track_meshes)

        # Пробиваем отверстия пинов сквозь дорожки, чтобы не перекрывать переходные отверстия
        for pin in self._board_pattern.pins:
            if pin.side != side and pin.side != Side.BOTH:
                continue
            hole_mesh = trimesh.creation.cylinder(radius=self._pad_radius, height=self._thickness*2, sections=CYLINDER_SECTIONS)
            hole_mesh.apply_translation([self._get_pin_center_x(pin), self._get_pin_center_y(pin), 0])
            tracks_mesh = tracks_mesh.difference(hole_mesh)

        return tracks_mesh

    def _place_pads(self) -> trimesh.Trimesh:
        ring_cache: Dict[Side, trimesh.Trimesh] = {}

        pads = []
        for pin in self._board_pattern.pins:
            if pin.side not in ring_cache:
                ring_cache[pin.side] = self._create_pad_ring(pin.side)

            pads.append(ring_cache[pin.side].copy().apply_translation([
                self._get_pin_center_x(pin),
                self._get_pin_center_y(pin),
                0
            ]))

        return union_meshes(*pads)

    def _create_pad_ring(self, side: Side) -> trimesh.Trimesh:
        # Кольцо для одной стороны не должно выступать с противоположной стороны платы
        if side == Side.BOTH:
            ring_height = self._thickness
            z_center = 0
        else:
            ring_height = self._thickness/2 + self._contact_pad_thickness
            z_center = (self._thickness/2 - self._contact_pad_thickness)/2
            if side == Side.BACK:
                z_center = -z_center

        ring = trimesh.creation.cylinder(radius=self._contact_pad_radius, height=ring_height, sections=CYLINDER_SECTIONS)
        hole_mesh = trimesh.creation.cylinder(radius=self._pad_radius, height=self._thickness*2, sections=CYLINDER_SECTIONS)
        ring = ring.difference(hole_mesh)
        ring.apply_translation([0, 0, z_center])

        return ring

    def _create_track_mesh(self, track: Track, z_center: float) -> trimesh.Trimesh:
        start_x = self._board_pattern.x_indent + track.x*self._step + self._step/2
        start_y = self._board_pattern.y_indent + track.y*self._step + self._step/2
        end_x = self._board_pattern.x_indent + (track.x + track.x_count)*self._step + self._step/2
        end_y = self._board_pattern.y_indent + (track.y + track.y_count)*self._step + self._step/2

        dx = end_x - start_x
        dy = end_y - start_y
        length = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)

        cap_mesh = trimesh.creation.cylinder(
            radius=track.width/2,
            height=self._contact_pad_thickness,
            sections=CYLINDER_SECTIONS,
        )

        if length > 0:
            ribbon_mesh = trimesh.creation.box([length, track.width, self._contact_pad_thickness])
            track_mesh = union_meshes(
                ribbon_mesh,
                cap_mesh.copy().apply_translation([length/2, 0, 0]),
                cap_mesh.copy().apply_translation([-length/2, 0, 0]),
            )
            track_mesh.apply_transform(create_rotation_matrix_for_z(angle))
        else:
            track_mesh = cap_mesh

        track_mesh.apply_translation([(start_x + end_x)/2, (start_y + end_y)/2, z_center])

        return track_mesh

    def _get_track_z_center(self, side: Side) -> float:
        z_center = self._thickness/2 - self._contact_pad_thickness/2
        return z_center if side == Side.FRONT else -z_center

    def _get_pin_center_x(self, pin: Pin) -> float:
        return self._board_pattern.x_indent + pin.x*self._step + self._step/2

    def _get_pin_center_y(self, pin: Pin) -> float:
        return self._board_pattern.y_indent + pin.y*self._step + self._step/2

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        if rotation.is_horizontal:
            return (
                -self._step/2 - self._board_pattern.x_indent,
                -self._step/2 - self._board_pattern.y_indent,
                -self._thickness/2
            )
        if rotation.is_vertical:
            return (
                -self._step/2 - self._board_pattern.y_indent,
                -self._step/2 - self._board_pattern.x_indent,
                -self._thickness/2
            )
        raise Exception(f"Invalid rotation for {self.__class__.__name__}")  # TODO custom exception
