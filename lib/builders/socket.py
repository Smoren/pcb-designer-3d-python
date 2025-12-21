import math
from typing import Tuple, List

import numpy as np
import trimesh
from trimeshtools.combine import union_meshes, concatenate_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_x, create_rotation_matrix_for_z

from lib.base import BaseMeshBuilder, PositionSide, Rotation, FloatPosition3d
from lib.constants import CYLINDER_SECTIONS


class SocketBuilder(BaseMeshBuilder):
    _x_count: float
    _y_count: float
    _step: float
    _thickness: float
    _pin_positions: List[Tuple[float, float, float]]
    _socket_radius: float
    _socket_pin_radius: float
    _pin_width: float
    _pin_thickness: float
    _pin_height: float
    _offset_z: float
    _color: np.ndarray
    _contacts_color: np.ndarray

    def __init__(
        self,
        x_count: float,
        y_count: float,
        step: float,
        thickness: float,
        pin_positions: List[Tuple[float, float, float]],
        socket_radius: float,
        socket_pin_radius: float,
        pin_width: float,
        pin_thickness: float,
        pin_height: float,
        offset_z: float,
        color: np.ndarray,
        contacts_color: np.ndarray
    ):
        self._x_count = x_count
        self._x_count = x_count
        self._y_count = y_count
        self._step = step
        self._thickness = thickness
        self._pin_positions = pin_positions
        self._socket_radius = socket_radius
        self._socket_pin_radius = socket_pin_radius
        self._pin_width = pin_width
        self._pin_thickness = pin_thickness
        self._pin_height = pin_height
        self._offset_z = offset_z
        self._color = color
        self._contacts_color = contacts_color

    def build(self) -> trimesh.Trimesh:
        socket_depth = (self._x_count/2)*self._step

        box_mesh = trimesh.creation.box([self._x_count*self._step, self._y_count*self._step, self._thickness])
        box_diff = trimesh.creation.cylinder(radius=self._socket_radius, height=socket_depth, sections=CYLINDER_SECTIONS)
        box_diff.apply_transform(create_rotation_matrix_for_x(math.pi/2))
        box_diff.apply_transform(create_rotation_matrix_for_z(math.pi/2))
        move_to_bound(box_mesh, -1, 0, 0)
        move_to_bound(box_diff, -1, 0, 0)
        box_mesh = box_mesh.difference(box_diff)
        box_mesh.visual.face_colors = self._color

        socket_pin_mesh = trimesh.creation.cylinder(radius=self._socket_pin_radius, height=socket_depth, sections=CYLINDER_SECTIONS)
        socket_pin_mesh.apply_transform(create_rotation_matrix_for_x(math.pi/2))
        socket_pin_mesh.apply_transform(create_rotation_matrix_for_z(math.pi/2))
        socket_pin_mesh.visual.face_colors = self._contacts_color
        move_to_bound(box_mesh, -1, 0, 0)
        move_to_bound(socket_pin_mesh, -1, 0, 0)
        final_mesh = concatenate_meshes(box_mesh, socket_pin_mesh)

        pins = []
        for x, y, angle in self._pin_positions:
            pin_mesh = trimesh.creation.box([self._pin_width, self._pin_thickness, self._pin_height])
            if angle > 0:
                pin_mesh.apply_transform(create_rotation_matrix_for_z(angle))

            x_dir = 0
            if x == 0:
                x_dir = 1
            elif x == self._x_count - 1:
                x_dir = -1

            y_dir = 0
            if y == 0:
                y_dir = 1
            elif x == self._x_count - 1:
                y_dir = -1

            move_to_bound(pin_mesh, x_dir, y_dir, 1)

            pin_mesh.apply_translation([x*self._step, y*self._step, 0])
            pins.append(pin_mesh)

        pins_mesh = union_meshes(*pins)
        pins_mesh.visual.face_colors = self._contacts_color

        move_to_bound(final_mesh, 1, 1, 1)
        move_to_bound(pins_mesh, z=-1)

        final_mesh = concatenate_meshes(final_mesh, pins_mesh)

        return final_mesh

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        x_delta = (self._x_count - int(self._x_count))*self._step
        y_delta = (self._y_count - int(self._y_count))*self._step

        offset_x = 0
        offset_y = 0

        if rotation == Rotation.ROTATE_180:
            offset_x = -x_delta
            offset_y = -y_delta

        if rotation == Rotation.ROTATE_CLOCKWISE_90:
            offset_y = -y_delta

        if rotation == Rotation.ROTATE_COUNTER_CLOCKWISE_90:
            offset_x = -x_delta
        # offset_x = -x_delta*self._step if rotation == Rotation.ROTATE_180 else 0
        # offset_y = y_delta*self._step if rotation == Rotation.ROTATE_CLOCKWISE_90 else 0
        return offset_x, offset_y, self._offset_z
