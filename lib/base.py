import abc
import math
import os
import re
from enum import Enum
from typing import Tuple, Dict

import trimesh
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_x, create_rotation_matrix_for_z

from lib.constants import CACHE_DIR

FloatPosition3d = Tuple[float, float, float]
IntPosition3d = Tuple[int, int, int]
IntPosition2d = Tuple[int, int]


class PositionSide(Enum):
    TOP = 1
    BOTTOM = -1

    @property
    def direction(self) -> float:
        return float(self.value)


class Rotation(Enum):
    NO_ROTATION = 0
    ROTATE_CLOCKWISE_90 = 0.5
    ROTATE_COUNTER_CLOCKWISE_90 = -0.5
    ROTATE_180 = 1

    @property
    def angle(self):
        return float(self.value * math.pi)

    @property
    def is_horizontal(self):
        return self == Rotation.NO_ROTATION or self == Rotation.ROTATE_180

    @property
    def is_vertical(self):
        return self == Rotation.ROTATE_CLOCKWISE_90 or self == Rotation.ROTATE_COUNTER_CLOCKWISE_90


class BaseMeshBuilder(abc.ABC):
    @abc.abstractmethod
    def build(self) -> trimesh.Trimesh:
        raise NotImplementedError()

    @property
    def cache_key(self) -> str:
        return '_'.join([
            self.__class__.__name__,
            *[str(getattr(self, attr)) for attr in self.__dict__.keys()],
        ])

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        return 0, 0, 0


class CachedMeshBuilder(BaseMeshBuilder):
    _map: Dict[str, trimesh.Trimesh] = {}
    _mesh_builder: BaseMeshBuilder
    _dir_path: str

    def __init__(self, mesh_builder: BaseMeshBuilder, dir_path: str = CACHE_DIR):
        self._mesh_builder = mesh_builder
        self._dir_path = dir_path
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def build(self) -> trimesh.Trimesh:
        if self.cache_key in CachedMeshBuilder._map:
            return CachedMeshBuilder._map[self.cache_key].copy()

        file_path = os.path.join(self._dir_path, f'{self.cache_key}.obj')
        if os.path.exists(file_path):
            result = trimesh.load(file_path)
            assert isinstance(result, trimesh.Trimesh)
            CachedMeshBuilder._map[self.cache_key] = result
            return result

        mesh = self._mesh_builder.build()
        mesh.export(file_path)
        CachedMeshBuilder._map[self.cache_key] = mesh
        return mesh

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        return self._mesh_builder.get_offset(side, rotation)

    @property
    def cache_key(self) -> str:
        return self._format_cache_key(self._mesh_builder.cache_key)

    @staticmethod
    def _format_cache_key(key: str) -> str:
        result = re.sub(r'[^a-zA-Z0-9._]', '_', key)
        result = re.sub(r'[_]{2,}', '_', result)
        result = result.strip('_')
        return result


class GridPlacer:
    _step: float
    _offset: FloatPosition3d

    def __init__(self, step: float, offset: FloatPosition3d):
        self._step = step
        self._offset = offset

    def place(self, mesh_builder: BaseMeshBuilder, position: IntPosition2d, side: PositionSide, rotation: Rotation) -> trimesh.Trimesh:
        mesh = mesh_builder.build()

        if rotation != rotation.NO_ROTATION:
            mesh.apply_transform(create_rotation_matrix_for_z(-rotation.angle))

        if side == PositionSide.BOTTOM:
            mesh.apply_transform(create_rotation_matrix_for_x(math.pi))

        move_to_bound(mesh, 1, 1, side.direction)

        mesh_offset = mesh_builder.get_offset(side, rotation)
        offset_x = self._offset[0] + position[0]*self._step + mesh_offset[0]
        offset_y = self._offset[1] + position[1]*self._step + mesh_offset[1]
        offset_z = self._offset[2] + side.direction*mesh_offset[2]

        mesh.apply_translation([offset_x, offset_y, offset_z])

        return mesh
