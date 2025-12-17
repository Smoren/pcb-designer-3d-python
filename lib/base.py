import abc
import inspect
import os
import re
from enum import Enum
from typing import Tuple

import trimesh
from trimeshtools.move import move_to_bound

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


class AxisDirection(Enum):
    ALONG_X = 0
    ALONG_Y = 1


class BaseMeshBuilder(abc.ABC):
    @abc.abstractmethod
    def build(self):
        raise NotImplementedError()

    @property
    def cache_key(self) -> str:
        return '_'.join([
            self.__class__.__name__,
            *[str(getattr(self, attr)) for attr in self.__dict__.keys()],
        ])

    @property
    def offset(self) -> FloatPosition3d:
        return 0, 0, 0


class CachedMeshBuilder(BaseMeshBuilder):
    _mesh_builder: BaseMeshBuilder
    _dir_path: str

    def __init__(self, mesh_builder: BaseMeshBuilder, dir_path: str = CACHE_DIR):
        self._mesh_builder = mesh_builder
        self._dir_path = dir_path
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

    def build(self):
        file_path = os.path.join(self._dir_path, f'{self.cache_key}.obj')
        if os.path.exists(file_path):
            return trimesh.load(file_path)

        mesh = self._mesh_builder.build()
        mesh.export(file_path)
        return mesh

    @property
    def offset(self) -> FloatPosition3d:
        return self._mesh_builder.offset

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

    def place(self, mesh_builder: BaseMeshBuilder, position: IntPosition2d, side: PositionSide) -> trimesh.Trimesh:
        mesh = mesh_builder.build()

        if side == PositionSide.BOTTOM:
            mesh.vertices[:, 2] *= -1

        move_to_bound(mesh, 1, 1, side.direction)

        offset_x = self._offset[0] + position[0]*self._step + mesh_builder.offset[0]
        offset_y = self._offset[1] + position[1]*self._step + mesh_builder.offset[1]
        offset_z = self._offset[2] + side.direction*mesh_builder.offset[2]

        mesh.apply_translation([offset_x, offset_y, offset_z])

        return mesh
