import numpy as np
import trimesh
from trimeshtools.combine import union_meshes, concatenate_meshes
from trimeshtools.move import move_to_bound

from lib.base import BaseMeshBuilder, FloatPosition3d, Rotation, PositionSide
from lib.constants import CYLINDER_SECTIONS


class BoardBuilder(BaseMeshBuilder):
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
