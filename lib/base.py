import abc
from enum import Enum
from typing import Tuple

import trimesh
from trimeshtools.move import move_to_bound

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


class MeshBuilderInterface(abc.ABC):
    @abc.abstractmethod
    def build(self):
        raise NotImplementedError()

    @property
    def offset(self) -> FloatPosition3d:
        return 0, 0, 0


class GridPlacer:
    _step: float
    _offset: FloatPosition3d

    def __init__(self, step: float, offset: FloatPosition3d):
        self._step = step
        self._offset = offset

    def place(self, mesh_builder: MeshBuilderInterface, position: IntPosition2d, side: PositionSide) -> trimesh.Trimesh:
        mesh = mesh_builder.build()

        if side == PositionSide.BOTTOM:
            mesh.vertices[:, 2] *= -1

        move_to_bound(mesh, 1, 1, side.direction)

        offset_x = self._offset[0] + position[0]*self._step + mesh_builder.offset[0]
        offset_y = self._offset[1] + position[1]*self._step + mesh_builder.offset[1]
        offset_z = self._offset[2] + side.direction*mesh_builder.offset[2]

        mesh.apply_translation([offset_x, offset_y, offset_z])

        return mesh
