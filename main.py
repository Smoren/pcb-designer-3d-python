import math

import numpy as np
import trimesh
from trimeshtools.combine import concatenate_meshes
from trimeshtools.show import show_mesh

from lib.base import GridPlacer, PositionSide, Rotation, CachedBuilderManager, TransparentBuildManager
from lib.factories.board import create_board_builder
from lib.factories.chip import create_chip_builder
from lib.constants import BOARD_GRID_STEP, COLOR_BLUE, COLOR_ORANGE, COLOR_BLACK, COLOR_RED
from lib.factories.jumper import create_jumper_builder
from lib.factories.led import create_led_builder
from lib.factories.resistor import create_resistor_builder
from lib.factories.socket import create_socket_builder
from lib.factories.track import create_track_builder


def create_test() -> trimesh.Trimesh:
    build_manager = TransparentBuildManager()
    # build_manager = CachedBuilderManager()

    placer = GridPlacer(build_manager, BOARD_GRID_STEP, (0, 0, 0))

    board_builder = create_board_builder(7, 5, x_indent=1.2, y_indent=1.2)
    jumper_builder = create_jumper_builder(5, 2, offset_z=1)

    board_mesh = placer.place(board_builder, (0, 0), PositionSide.TOP, Rotation.NO_ROTATION)
    jumper_mesh = placer.place(jumper_builder, (0, 0), PositionSide.TOP, Rotation.NO_ROTATION)

    final_mesh = concatenate_meshes(board_mesh, jumper_mesh)

    # fix_all(final_mesh)
    return final_mesh


def create_my() -> trimesh.Trimesh:
    # build_manager = TransparentBuildManager()
    build_manager = CachedBuilderManager()

    placer = GridPlacer(build_manager, BOARD_GRID_STEP, (0, 0, 0))

    board_builder = create_board_builder(14, 9, x_indent=1.2, y_indent=1.2)
    resistor_220om_builder = create_resistor_builder('220 Om', np.array([0, 0, 100, 255]))
    resistor_10kom_builder = create_resistor_builder('10 kOm', np.array([0, 0, 0, 255]))
    blue_led_builder = create_led_builder(COLOR_BLUE)
    orange_led_builder = create_led_builder(COLOR_ORANGE)
    chip_builder = create_chip_builder(x_count=7, y_count=2, text="74HC32")
    socket_builder = create_socket_builder(4.5, 2, pin_positions=[(2, 1, math.pi/2), (1, 2, 0.0)], color=np.array([50, 50, 50, 255]))

    track_builder_1x4 = create_track_builder(1, 4)
    track_builder_1x1 = create_track_builder(1, 1)
    track_builder_2x1 = create_track_builder(2, 1)
    track_builder_1x3 = create_track_builder(1, 3)
    track_builder_1x5 = create_track_builder(1, 5)
    track_builder_1x8 = create_track_builder(1, 8)

    jumper_builder_black_1x5 = create_jumper_builder(1, 5, offset_z=1, color=COLOR_BLACK)
    jumper_builder_orange_6x1 = create_jumper_builder(6, 1, offset_z=1, color=COLOR_ORANGE)
    jumper_builder_blue_6x1 = create_jumper_builder(6, 1, offset_z=1, color=COLOR_BLUE)

    meshes = []
    meshes.append(placer.place(board_builder, (0, 0), PositionSide.TOP, Rotation.NO_ROTATION))

    meshes.append(placer.place(resistor_10kom_builder, (2, 5), PositionSide.TOP, Rotation.NO_ROTATION))
    meshes.append(placer.place(resistor_10kom_builder, (2, 6), PositionSide.TOP, Rotation.NO_ROTATION))
    meshes.append(placer.place(resistor_10kom_builder, (2, 7), PositionSide.TOP, Rotation.NO_ROTATION))
    meshes.append(placer.place(resistor_220om_builder, (3, 8), PositionSide.TOP, Rotation.NO_ROTATION))
    meshes.append(placer.place(resistor_220om_builder, (3, 0), PositionSide.TOP, Rotation.ROTATE_COUNTER_CLOCKWISE_90))
    meshes.append(placer.place(resistor_220om_builder, (9, 0), PositionSide.TOP, Rotation.NO_ROTATION))

    meshes.append(placer.place(orange_led_builder, (2, 0), PositionSide.TOP, Rotation.ROTATE_180))
    meshes.append(placer.place(orange_led_builder, (2, 8), PositionSide.TOP, Rotation.ROTATE_180))
    meshes.append(placer.place(blue_led_builder, (13, 2), PositionSide.TOP, Rotation.ROTATE_CLOCKWISE_90))

    meshes.append(placer.place(chip_builder, (7, 1), PositionSide.TOP, Rotation.ROTATE_COUNTER_CLOCKWISE_90))

    meshes.append(placer.place(socket_builder, (-2, 0), PositionSide.TOP, Rotation.ROTATE_180))
    meshes.append(placer.place(socket_builder, (-2, 6), PositionSide.TOP, Rotation.ROTATE_180))
    meshes.append(placer.place(socket_builder, (11, 3), PositionSide.TOP, Rotation.NO_ROTATION))

    meshes.append(placer.place(track_builder_1x4, (2, 5), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_1x3, (1, 0), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_1x3, (1, 2), PositionSide.BOTTOM, Rotation.ROTATE_CLOCKWISE_90))
    meshes.append(placer.place(track_builder_2x1, (0, 1), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_2x1, (1, 6), PositionSide.BOTTOM, Rotation.ROTATE_CLOCKWISE_90))
    meshes.append(placer.place(track_builder_2x1, (0, 7), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_1x5, (3, 2), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_2x1, (12, 5), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_1x3, (13, 3), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_1x3, (13, 0), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_1x1, (3, 0), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_1x1, (3, 8), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_2x1, (6, 5), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_1x5, (3, 6), PositionSide.BOTTOM, Rotation.ROTATE_CLOCKWISE_90))
    meshes.append(placer.place(track_builder_2x1, (6, 7), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_2x1, (7, 7), PositionSide.BOTTOM, Rotation.ROTATE_CLOCKWISE_90))
    meshes.append(placer.place(track_builder_1x1, (7, 1), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_1x1, (10, 7), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(track_builder_1x8, (2, 1), PositionSide.BOTTOM, Rotation.ROTATE_CLOCKWISE_90))
    meshes.append(placer.place(track_builder_2x1, (2, 0), PositionSide.BOTTOM, Rotation.ROTATE_CLOCKWISE_90))
    meshes.append(placer.place(track_builder_2x1, (9, 0), PositionSide.BOTTOM, Rotation.ROTATE_CLOCKWISE_90))

    meshes.append(placer.place(jumper_builder_black_1x5, (2, 1), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(jumper_builder_orange_6x1, (1, 7), PositionSide.BOTTOM, Rotation.NO_ROTATION))
    meshes.append(placer.place(jumper_builder_blue_6x1, (7, 5), PositionSide.BOTTOM, Rotation.NO_ROTATION))

    final_mesh = concatenate_meshes(*meshes)

    # fix_all(final_mesh)
    return final_mesh


if __name__ == '__main__':
    file_name = 'test'

    # final_mesh = create_test()
    final_mesh = create_my()

    print('is_watertight =', final_mesh.is_watertight)
    print('is_volume =', final_mesh.is_volume)

    final_mesh.export(f'output/{file_name}.obj')
    print(f'Saved: output/{file_name}.obj')

    show_mesh(final_mesh, with_axis=False)
