import math

import trimesh
from trimeshtools.combine import union_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_x, create_rotation_matrix_for_z

from lib.base import BaseMeshBuilder, AxisDirection, FloatPosition3d
from lib.constants import CYLINDER_SECTIONS
from lib.utils import create_bounded_pipe


class ResistorBuilder(BaseMeshBuilder):
    _length: float
    _radius: float
    _axis_direction: AxisDirection
    _offset: FloatPosition3d

    def __init__(self, length: float, thickness: float, axis_direction: AxisDirection, offset: FloatPosition3d = (0, 0, 0)):
        self._axis_direction = axis_direction
        self._length = length
        self._radius = thickness
        self._offset = offset

    def build(self):
        left_sphere = trimesh.creation.icosphere(radius=self._radius, subdivisions=4)
        right_sphere = trimesh.creation.icosphere(radius=self._radius, subdivisions=4)

        left_sphere.apply_translation([-self._length/2, 0, 0])
        right_sphere.apply_translation([self._length/2, 0, 0])

        cylinder = trimesh.creation.cylinder(radius=self._radius, height=self._length, sections=CYLINDER_SECTIONS)
        cylinder.apply_transform(create_rotation_matrix_for_x(math.pi/2))
        cylinder.apply_transform(create_rotation_matrix_for_z(math.pi/2))

        final_mesh = union_meshes(left_sphere, cylinder, right_sphere)

        left_wire = create_bounded_pipe(pipe_radius=1, bond_radius=5, vertical_length=10, horizontal_length=10)
        right_wire = left_wire.copy().apply_transform(create_rotation_matrix_for_z(math.pi))

        move_to_bound(final_mesh, 1)
        move_to_bound(left_wire, -1)
        final_mesh = union_meshes(final_mesh, left_wire)

        move_to_bound(final_mesh, -1)
        move_to_bound(right_wire, 1)
        final_mesh = union_meshes(final_mesh, right_wire)

        move_to_bound(final_mesh, 0, 0, 0)

        return final_mesh

    @property
    def offset(self) -> FloatPosition3d:
        return self._offset
