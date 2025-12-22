import numpy as np
import trimesh
from trimeshtools.combine import concatenate_meshes
from trimeshtools.move import move_to_bound

from lib.base import BaseMeshBuilder, PositionSide, Rotation, FloatPosition3d
from lib.constants import CYLINDER_SECTIONS


class WireBuilder(BaseMeshBuilder):
    _length: float
    _contact_length: float
    _radius: float
    _contact_radius: float
    _offset_z: float
    _color: np.ndarray
    _contact_color: np.ndarray

    def __init__(
        self,
        length: float,
        contact_length: float,
        radius: float,
        contact_radius: float,
        offset_z: float,
        color: np.ndarray,
        contact_color: np.ndarray,
    ):
        self._length = length
        self._contact_length = contact_length
        self._radius = radius
        self._contact_radius = contact_radius
        self._offset_z = offset_z
        self._color = color
        self._contact_color = contact_color

    def build(self) -> trimesh.Trimesh:
        contact_cylinder = trimesh.creation.cylinder(radius=self._contact_radius, height=self._length, sections=CYLINDER_SECTIONS)
        contact_cylinder.visual.face_colors = self._contact_color

        wire_cylinder = trimesh.creation.cylinder(radius=self._radius, height=self._length - self._contact_length*2, sections=CYLINDER_SECTIONS)
        wire_cylinder.visual.face_colors = self._color

        move_to_bound(contact_cylinder, 0, 0, 0)
        move_to_bound(wire_cylinder, 0, 0, 0)

        final_mesh = concatenate_meshes(contact_cylinder, wire_cylinder)
        return final_mesh

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        return -self._radius, -self._radius, self._offset_z
