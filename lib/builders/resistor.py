import math

import numpy as np
import trimesh
from trimeshtools.combine import union_meshes, concatenate_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_x, create_rotation_matrix_for_z

from lib.base import BaseMeshBuilder, AxisDirection, FloatPosition3d
from lib.constants import CYLINDER_SECTIONS
from lib.utils import create_bounded_pipe


class ResistorBuilder(BaseMeshBuilder):
    _length: float
    _radius: float
    _axis_direction: AxisDirection
    _wire_contact_radius: float
    _wire_bond_radius: float
    _wire_horizontal_length: float
    _wire_vertical_length: float
    _offset_z: float
    _color: np.ndarray
    _color_wire: np.ndarray

    def __init__(
        self,
        length: float,
        radius: float,
        axis_direction: AxisDirection,
        wire_contact_radius: float,
        wire_bond_radius: float,
        wire_horizontal_length: float,
        wire_vertical_length: float,
        offset_z: float,
        color: np.ndarray,
        color_wire: np.ndarray,
    ):
        self._axis_direction = axis_direction
        self._length = length
        self._radius = radius
        self._wire_contact_radius = wire_contact_radius
        self._wire_bond_radius = wire_bond_radius
        self._wire_horizontal_length = wire_horizontal_length
        self._wire_vertical_length = wire_vertical_length
        self._offset_z = offset_z
        self._color = color
        self._color_wire = color_wire

    def build(self):
        left_sphere = trimesh.creation.icosphere(radius=self._radius)
        right_sphere = trimesh.creation.icosphere(radius=self._radius)

        left_sphere.apply_translation([-self._length/2, 0, 0])
        right_sphere.apply_translation([self._length/2, 0, 0])

        cylinder = trimesh.creation.cylinder(radius=self._radius, height=self._length, sections=CYLINDER_SECTIONS)
        cylinder.apply_transform(create_rotation_matrix_for_x(math.pi/2))
        cylinder.apply_transform(create_rotation_matrix_for_z(math.pi/2))

        final_mesh = union_meshes(left_sphere, cylinder, right_sphere)
        move_to_bound(final_mesh, 0, 0)

        left_wire = create_bounded_pipe(pipe_radius=self._wire_contact_radius, bond_radius=self._wire_bond_radius, horizontal_length=self._wire_horizontal_length, vertical_length=self._wire_vertical_length)
        right_wire = left_wire.copy().apply_transform(create_rotation_matrix_for_z(math.pi))
        center_wire = trimesh.creation.cylinder(radius=self._wire_contact_radius, height=self._length, sections=CYLINDER_SECTIONS)
        center_wire.apply_transform(create_rotation_matrix_for_x(math.pi/2))
        center_wire.apply_transform(create_rotation_matrix_for_z(math.pi/2))

        move_to_bound(center_wire, 1)
        move_to_bound(left_wire, -1)
        wire_mesh = union_meshes(center_wire, left_wire)

        move_to_bound(wire_mesh, -1)
        move_to_bound(right_wire, 1)
        wire_mesh = union_meshes(wire_mesh, right_wire)

        move_to_bound(wire_mesh, 0, 0)

        final_mesh.visual.face_colors = self._color
        wire_mesh.visual.face_colors = self._color_wire

        final_mesh = concatenate_meshes(final_mesh, wire_mesh)
        move_to_bound(final_mesh, 0, 0, 0)

        if self._axis_direction == AxisDirection.ALONG_Y:
            final_mesh.apply_transform(create_rotation_matrix_for_z(math.pi/2))
            move_to_bound(final_mesh, 0, 0, 0)

        return final_mesh

    @property
    def offset(self) -> FloatPosition3d:
        if self._axis_direction == AxisDirection.ALONG_X:
            return 0, -self._radius, self._offset_z

        return -self._radius, 0, self._offset_z
