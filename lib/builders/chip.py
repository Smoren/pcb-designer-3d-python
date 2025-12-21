import math
from typing import Optional

import numpy as np
import trimesh
from trimeshtools.combine import union_meshes, concatenate_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_z, create_mirror_matrix

from lib.base import BaseMeshBuilder, FloatPosition3d, Rotation, PositionSide
from lib.utils.mesh import create_pin_mesh, create_text_mesh


class ChipBuilder(BaseMeshBuilder):
    _x_count: int
    _y_count: int
    _step: float
    _thickness: float
    _pit_radius: float
    _pit_height: float
    _pin_thickness: float
    _pin_top_vertical_length: float
    _pin_bottom_vertical_length: float
    _pin_top_width: float
    _pin_bottom_width: float
    _offset_z: float
    _color: np.ndarray
    _contacts_color: np.ndarray
    _text: Optional[str]

    def __init__(
        self,
        x_count: int,
        y_count: int,
        step: float,
        thickness: float,
        pit_radius: float,
        pit_height: float,
        pin_thickness: float,
        pin_top_vertical_length: float,
        pin_bottom_vertical_length: float,
        pin_top_width: float,
        pin_bottom_width: float,
        offset_z: float,
        color: np.ndarray,
        contacts_color: np.ndarray,
        text: Optional[str] = None
    ):
        self._x_count = x_count
        self._y_count = y_count
        self._step = step
        self._thickness = thickness
        self._pit_radius = pit_radius
        self._pit_height = pit_height
        self._pin_thickness = pin_thickness
        self._pin_top_vertical_length = pin_top_vertical_length
        self._pin_bottom_vertical_length = pin_bottom_vertical_length
        self._pin_top_width = pin_top_width
        self._pin_bottom_width = pin_bottom_width
        self._offset_z = offset_z
        self._color = color
        self._contacts_color = contacts_color
        self._text = text

    def build(self) -> trimesh.Trimesh:
        box_mesh = trimesh.creation.box([self._x_count*self._step, self._y_count*self._step, self._thickness])
        box_diff = trimesh.creation.cylinder(radius=self._pit_radius, height=self._pit_height)
        move_to_bound(box_mesh, -1, 0, -1)
        move_to_bound(box_diff, 0, 0, -1)
        box_mesh = box_mesh.difference(box_diff)
        box_mesh.visual.face_colors = self._color

        pins_offset = (box_mesh.extents[0] - ((self._x_count-1)*self._step + self._pin_top_width))/2
        pin_horizontal_length = self._step/2 - self._pin_thickness

        move_to_bound(box_mesh, 1, 1, 1)
        pin_mesh = create_pin_mesh(thickness=self._pin_thickness, horizontal_length=pin_horizontal_length, top_vertical_length=self._pin_top_vertical_length, bottom_vertical_length=self._pin_bottom_vertical_length, top_width=self._pin_top_width, bottom_width=self._pin_bottom_width)
        pin_mesh = pin_mesh.copy().apply_transform(create_rotation_matrix_for_z(-math.pi/2))

        move_to_bound(pin_mesh, 1, -1, -1)

        left_pins = []
        for i in range(self._x_count):
            left_pins.append(pin_mesh.copy().apply_translation([i*self._step, 0, 0]))
        left_pins_mesh = union_meshes(*left_pins)
        left_pins_mesh.apply_translation([pins_offset, 0, 0])
        left_pins_mesh.visual.face_colors = self._contacts_color

        move_to_bound(box_mesh, 1, 1, 0)
        final_mesh = concatenate_meshes(box_mesh, left_pins_mesh)

        right_pins_mesh = left_pins_mesh.copy().apply_transform(create_mirror_matrix(y=True))
        move_to_bound(final_mesh, y=-1)
        final_mesh = concatenate_meshes(final_mesh, right_pins_mesh)

        if self._text is not None:
            text_mesh = create_text_mesh(self._text, 0.1)
            move_to_bound(final_mesh, 0, 0, -1)
            move_to_bound(text_mesh, 0, 0, 1)
            final_mesh = concatenate_meshes(final_mesh, text_mesh)

        return final_mesh

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        if rotation.is_horizontal:
            return -self._step/2, 0, self._offset_z
        if rotation.is_vertical:
            return 0, -self._step/2, self._offset_z
        raise Exception(f"Invalid rotation for {self.__class__.__name__}")  # TODO custom exception
