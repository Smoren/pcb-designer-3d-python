import numpy as np
import trimesh

from lib.base import BaseMeshBuilder, FloatPosition3d, AxisDirection


class ChipBuilder(BaseMeshBuilder):
    _x_count: int
    _y_count: int
    _thickness: float
    _axis_direction: AxisDirection
    _step: float
    _color: np.ndarray
    _contacts_color: np.ndarray

    def __init__(
        self,
        x_count: int,
        y_count: int,
        thickness: float,
        axis_direction: AxisDirection,
        step: float,
        color: np.ndarray,
        contacts_color: np.ndarray
    ):
        self._x_count = x_count
        self._y_count = y_count
        self._axis_direction = axis_direction
        self._thickness = thickness
        self._step = step
        self._color = color
        self._contacts_color = contacts_color

    def build(self) -> trimesh.Trimesh:
        box_mesh = trimesh.creation.box([self._x_count*self._step, self._y_count*self._step, self._thickness])
        return box_mesh

    @property
    def offset(self) -> FloatPosition3d:
        return 0, 0, 0
