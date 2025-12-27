import trimesh
from trimeshtools.combine import concatenate_meshes

from lib.base import GridPlacer, PositionSide, Rotation, CachedBuilderManager, TransparentBuildManager
from lib.factories.board import create_board_builder
from lib.constants import BOARD_GRID_STEP, COLOR_RED
from lib.factories.track import create_track_builder
from lib.factories.wire import create_wire_builder


def create_test() -> trimesh.Trimesh:
    build_manager = TransparentBuildManager()
    # build_manager = CachedBuilderManager()

    placer = GridPlacer(build_manager, BOARD_GRID_STEP, (0, 0, 0))

    board_builder = create_board_builder(7, 5, x_indent=1.2, y_indent=1.2)
    wire_builder = create_wire_builder(15, COLOR_RED)
    track_builder = create_track_builder(3, 1)

    board_mesh = placer.place(board_builder, (0, 0), PositionSide.TOP, Rotation.NO_ROTATION)
    wire_mesh = placer.place(wire_builder, (0, 0), PositionSide.TOP, Rotation.NO_ROTATION)
    track_mesh = placer.place(track_builder, (1, 3), PositionSide.BOTTOM, Rotation.NO_ROTATION)

    final_mesh = concatenate_meshes(board_mesh, wire_mesh, track_mesh)

    # fix_all(final_mesh)
    return final_mesh
