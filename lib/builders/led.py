import numpy as np
import trimesh
from trimeshtools.combine import union_meshes, concatenate_meshes
from trimeshtools.move import move_to_bound

from lib.base import BaseMeshBuilder, PositionSide, Rotation, FloatPosition3d
from lib.utils.constants import CYLINDER_SECTIONS


class LedBuilder(BaseMeshBuilder):
    _radius: float
    _height: float
    _anode_length: float
    _cathode_length: float
    _anode_cathode_distance: float
    _contact_radius: float
    _offset_z: float
    _color: np.ndarray
    _color_contact: np.ndarray

    def __init__(
        self,
        radius: float,
        height: float,
        anode_length: float,
        cathode_length: float,
        anode_cathode_distance: float,
        contact_radius: float,
        offset_z: float,
        color: np.ndarray,
        color_contact: np.ndarray
    ):
        self._radius = radius
        self._height = height
        self._anode_length = anode_length
        self._cathode_length = cathode_length
        self._anode_cathode_distance = anode_cathode_distance
        self._contact_radius = contact_radius
        self._offset_z = offset_z
        self._color = color
        self._color_contact = color_contact

    def build(self) -> trimesh.Trimesh:
        sphere = trimesh.creation.icosphere(radius=self._radius)
        cylinder = trimesh.creation.cylinder(radius=self._radius, height=self._height-self._radius, sections=CYLINDER_SECTIONS)
        cylinder_base = trimesh.creation.cylinder(radius=self._radius + self._contact_radius, height=self._contact_radius, sections=CYLINDER_SECTIONS)
        move_to_bound(sphere, 0, 0, 0)
        move_to_bound(cylinder, 0, 0, -1)
        top_mesh = union_meshes(sphere, cylinder)
        move_to_bound(top_mesh, 0, 0, 1)
        move_to_bound(cylinder_base, 0, 0, -1)
        top_mesh = union_meshes(top_mesh, cylinder_base)
        top_mesh.visual.face_colors = self._color

        anode_mesh = trimesh.creation.cylinder(radius=self._contact_radius, height=self._anode_length, sections=CYLINDER_SECTIONS)
        move_to_bound(anode_mesh, 0, 0, 0)
        anode_mesh.apply_translation([-self._anode_cathode_distance/2, 0, 0])

        cathode_mesh = trimesh.creation.cylinder(radius=self._contact_radius, height=self._cathode_length, sections=CYLINDER_SECTIONS)
        move_to_bound(cathode_mesh, 0, 0, 0)
        cathode_mesh.apply_translation([self._anode_cathode_distance/2, 0, 0])

        move_to_bound(anode_mesh, z=-1)
        move_to_bound(cathode_mesh, z=-1)
        contacts_mesh = union_meshes(anode_mesh, cathode_mesh)
        contacts_mesh.visual.face_colors = self._color_contact

        move_to_bound(top_mesh, 0, 0, 1)
        move_to_bound(contacts_mesh, 0, 0, -1)
        final_mesh = concatenate_meshes(top_mesh, contacts_mesh)

        return final_mesh

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        horizontal_offset = -self._contact_radius - self._contact_radius
        vertical_offset = -self._radius - self._contact_radius

        if rotation.is_horizontal:
            return horizontal_offset, vertical_offset, self._offset_z
        if rotation.is_vertical:
            return vertical_offset, horizontal_offset, self._offset_z
        raise Exception(f"Invalid rotation for {self.__class__.__name__}")  # TODO custom exception

