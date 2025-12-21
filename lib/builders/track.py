import math

import numpy as np
import trimesh
from trimeshtools.combine import union_meshes, concatenate_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_x, create_rotation_matrix_for_z

from lib.base import BaseMeshBuilder, PositionSide, Rotation, FloatPosition3d


class TrackBuilder(BaseMeshBuilder):
    _x_count: int
    _y_count: int
    _step: float
    _radius: float
    _offset_z: float
    _color: np.ndarray

    def __init__(
        self,
        x_count: int,
        y_count: int,
        step: float,
        radius: float,
        offset_z: float,
        color: np.ndarray
    ):
        assert x_count > 0 and y_count > 0

        self._x_count = x_count
        self._y_count = y_count
        self._step = step
        self._radius = radius
        self._offset_z = offset_z
        self._color = color

    def build(self) -> trimesh.Trimesh:
        length = ((self._x_count-1)**2 + (self._y_count-1)**2)**(1/2) * self._step
        angle = -math.atan2(self._y_count-1, self._x_count-1)

        if self._x_count != 1 or self._y_count != 1:
            sphere_mesh = trimesh.creation.icosphere(radius=self._radius)
            cylinder_mesh = trimesh.creation.cylinder(radius=self._radius, height=length)
            cylinder_mesh.apply_transform(create_rotation_matrix_for_x(math.pi/2))
            cylinder_mesh.apply_transform(create_rotation_matrix_for_z(math.pi/2))

            move_to_bound(sphere_mesh, 0, 0, 0)
            move_to_bound(cylinder_mesh, 1, 0, 0)
            final_mesh = union_meshes(cylinder_mesh, sphere_mesh)

            move_to_bound(final_mesh, -1, 0, 0)
            final_mesh = union_meshes(final_mesh, sphere_mesh)
        else:
            final_mesh = trimesh.creation.icosphere(radius=self._radius)

        diff_mesh = trimesh.creation.box([(length+1)*2, (length+1)*2, (length+1)*2])
        move_to_bound(final_mesh, 0, 0, 0)
        move_to_bound(diff_mesh, 0, 0, -1)
        final_mesh = final_mesh.difference(diff_mesh)

        final_mesh.apply_transform(create_rotation_matrix_for_z(angle))
        final_mesh.visual.face_colors = self._color

        return final_mesh

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        return -self._radius, -self._radius, self._offset_z
