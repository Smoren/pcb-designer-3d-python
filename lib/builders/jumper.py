import math

import numpy as np
import trimesh
from trimeshtools.combine import union_meshes, concatenate_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_x, create_rotation_matrix_for_z

from lib.base import BaseMeshBuilder, PositionSide, Rotation, FloatPosition3d
from lib.constants import CYLINDER_SECTIONS


class JumperBuilder(BaseMeshBuilder):
    _x_count: int
    _y_count: int
    _step: float
    _step_delta: float
    _radius: float
    _contact_radius: float
    _offset_z: float
    _color: np.ndarray
    _contact_color: np.ndarray

    def __init__(
        self,
        x_count: int,
        y_count: int,
        step: float,
        step_delta: float,
        radius: float,
        contact_radius: float,
        contact_height: float,
        offset_z: float,
        color: np.ndarray,
        contact_color: np.ndarray
    ):
        assert x_count > 0 and y_count > 0
        assert x_count > 1 or y_count > 1

        self._x_count = x_count
        self._y_count = y_count
        self._step = step
        self._step_delta = step_delta
        self._radius = radius
        self._contact_radius = contact_radius
        self._contact_height = contact_height
        self._offset_z = offset_z
        self._color = color
        self._contact_color = contact_color

    def build(self) -> trimesh.Trimesh:
        length = ((self._x_count-1)**2 + (self._y_count-1)**2)**(1/2) * self._step - self._step_delta*2
        angle = -math.atan2(self._y_count-1, self._x_count-1)

        sphere_mesh = trimesh.creation.icosphere(radius=self._contact_radius)
        cylinder_mesh = trimesh.creation.cylinder(radius=self._contact_radius, height=length, sections=CYLINDER_SECTIONS)
        cylinder_mesh.apply_transform(create_rotation_matrix_for_x(math.pi / 2))
        cylinder_mesh.apply_transform(create_rotation_matrix_for_z(math.pi / 2))

        move_to_bound(sphere_mesh, 0, 0, 0)
        move_to_bound(cylinder_mesh, 1, 0, 0)
        wire_mesh = union_meshes(cylinder_mesh, sphere_mesh)

        move_to_bound(wire_mesh, -1, 0, 0)
        wire_mesh = union_meshes(wire_mesh, sphere_mesh)

        left_contact_mesh = trimesh.creation.cylinder(radius=self._contact_radius, height=self._contact_height, sections=CYLINDER_SECTIONS)
        move_to_bound(left_contact_mesh, 1, 0, -1)
        right_contact_mesh = left_contact_mesh.copy().apply_translation([length, 0, 0])
        contacts_mesh = union_meshes(left_contact_mesh, right_contact_mesh)

        move_to_bound(contacts_mesh, 0, 0, -1)
        move_to_bound(wire_mesh, 0, 0, 0)
        wire_mesh = union_meshes(wire_mesh, contacts_mesh)
        wire_mesh.visual.face_colors = self._contact_color

        cylinder_mesh = trimesh.creation.cylinder(radius=self._radius, height=length-self._contact_radius*2)
        cylinder_mesh.apply_transform(create_rotation_matrix_for_x(math.pi / 2))
        cylinder_mesh.apply_transform(create_rotation_matrix_for_z(math.pi / 2))
        cylinder_mesh.visual.face_colors = self._color

        move_to_bound(wire_mesh, 0, 0, -1)
        wire_mesh.apply_translation([0, 0, -(self._radius - self._contact_radius)])
        move_to_bound(cylinder_mesh, 0, 0, -1)
        final_mesh = concatenate_meshes(wire_mesh, cylinder_mesh)

        final_mesh.apply_transform(create_rotation_matrix_for_z(angle))

        return final_mesh

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        is_horizontal = self._x_count == 1 and rotation.is_horizontal or self._y_count == 1 and rotation.is_vertical
        is_vertical = self._y_count == 1 and rotation.is_horizontal or self._x_count == 1 and rotation.is_vertical

        if is_horizontal:
            return -self._radius, -self._contact_radius + self._step_delta, self._offset_z

        if is_vertical:
            return -self._contact_radius + self._step_delta, -self._radius, self._offset_z

        return 0, 0, self._offset_z  # FIXME
