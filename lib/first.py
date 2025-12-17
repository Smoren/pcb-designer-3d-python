import trimesh

from lib.base import MeshBuilderInterface, FloatPosition3d


class CubeBuilder(MeshBuilderInterface):
    def build(self):
        return trimesh.creation.box([1, 1, 1])

    @property
    def offset(self) -> FloatPosition3d:
        return 0, 0, 0


class ConeBuilder(MeshBuilderInterface):
    def build(self):
        return trimesh.creation.cone(10, 20)

    @property
    def offset(self) -> FloatPosition3d:
        return 3, 2, -5
