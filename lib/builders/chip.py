import math

import numpy as np
import trimesh
from trimeshtools.combine import union_meshes, concatenate_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_z, create_mirror_matrix
from trimeshtools.show import show_mesh

from lib.base import BaseMeshBuilder, FloatPosition3d, Rotation, PositionSide
from lib.utils.mesh import create_pin_mesh


class ChipBuilder(BaseMeshBuilder):
    _x_count: int
    _y_count: int
    _thickness: float
    _step: float
    _color: np.ndarray
    _contacts_color: np.ndarray

    def __init__(
        self,
        x_count: int,
        y_count: int,
        thickness: float,
        step: float,
        color: np.ndarray,
        contacts_color: np.ndarray
    ):
        self._x_count = x_count
        self._y_count = y_count
        self._thickness = thickness
        self._step = step
        self._color = color
        self._contacts_color = contacts_color

    def build(self) -> trimesh.Trimesh:
        # TODO to config
        PIN_THICKNESS = 0.3
        HORIZONTAL_LENGTH = 1.0
        TOP_VERTICAL_LENGTH = 4.0
        BOTTOM_VERTICAL_LENGTH = 5.0
        TOP_WIDTH = 2.0
        BOTTOM_WIDTH = 0.5

        box_mesh = trimesh.creation.box([self._x_count*self._step, self._y_count*self._step, self._thickness])
        box_mesh.visual.face_colors = self._color

        move_to_bound(box_mesh, 1, 1, 1)
        pin_mesh = create_pin_mesh(thickness=PIN_THICKNESS, horizontal_length=HORIZONTAL_LENGTH, top_vertical_length=TOP_VERTICAL_LENGTH, bottom_vertical_length=BOTTOM_VERTICAL_LENGTH, top_width=TOP_WIDTH, bottom_width=BOTTOM_WIDTH)
        pin_mesh = pin_mesh.copy().apply_transform(create_rotation_matrix_for_z(-math.pi/2))

        move_to_bound(pin_mesh, 1, -1, -1)

        pins_offset = (box_mesh.extents[0] - ((self._x_count-1)*self._step + TOP_WIDTH))/2

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

        return final_mesh

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        return -self._step/2, 0, 0  # TODO fix
