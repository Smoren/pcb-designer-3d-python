import math

import numpy as np
import trimesh
from trimeshtools.combine import concatenate_meshes
from trimeshtools.show import show_mesh

from app.elements import create_or_mesh
from lib.base import GridPlacer, PositionSide, Rotation, CachedBuilderManager, TransparentBuildManager
from lib.factories.board import create_board_builder
from lib.constants import BOARD_GRID_STEP, COLOR_RED
from lib.factories.wire import create_wire_builder


def create_test() -> trimesh.Trimesh:
    build_manager = TransparentBuildManager()
    # build_manager = CachedBuilderManager()

    placer = GridPlacer(build_manager, BOARD_GRID_STEP, (0, 0, 0))

    board_builder = create_board_builder(7, 5, x_indent=1.2, y_indent=1.2)
    wire_builder = create_wire_builder(15, COLOR_RED)

    board_mesh = placer.place(board_builder, (0, 0), PositionSide.TOP, Rotation.NO_ROTATION)
    wire_mesh = placer.place(wire_builder, (0, 0), PositionSide.TOP, Rotation.NO_ROTATION)

    final_mesh = concatenate_meshes(board_mesh, wire_mesh)

    # fix_all(final_mesh)
    return final_mesh


if __name__ == '__main__':
    file_name = 'test'

    # final_mesh = create_test()
    final_mesh = create_or_mesh()

    print('is_watertight =', final_mesh.is_watertight)
    print('is_volume =', final_mesh.is_volume)

    final_mesh.export(f'output/{file_name}.obj')
    print(f'Saved: output/{file_name}.obj')

    show_mesh(final_mesh, with_axis=False)
