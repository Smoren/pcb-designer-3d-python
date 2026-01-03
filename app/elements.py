import math

import numpy as np
import trimesh
from trimeshtools.combine import concatenate_meshes
from trimeshtools.rotate import create_rotation_matrix_for_z

from lib.base import GridPlacer, PositionSide, Rotation, CachedBuilderManager
from lib.factories.board import create_board_builder
from lib.factories.chip import create_chip_builder
from lib.constants import BOARD_GRID_STEP, COLOR_BLUE, COLOR_ORANGE, COLOR_BLACK, BOARD_CONTACT_PAD_RADIUS, \
    TRACK_WIDTH
from lib.factories.jumper import create_jumper_builder
from lib.factories.led import create_led_builder
from lib.factories.resistor import create_resistor_builder
from lib.factories.socket import create_socket_builder
from lib.factories.track import create_track_builder
from lib.pattern.structs import BoardPattern, Pin, MultiTrack


def create_or_mesh() -> trimesh.Trimesh:
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
    final_mesh.apply_transform(create_rotation_matrix_for_z(math.pi/2))

    # fix_all(final_mesh)
    return final_mesh


def create_or_board_pattern() -> BoardPattern:
    pin_radius = BOARD_CONTACT_PAD_RADIUS
    track_width = TRACK_WIDTH / 1.5

    pins = [
        Pin(radius=pin_radius, x=1, y=0),
        Pin(radius=pin_radius, x=7, y=0),
        Pin(radius=pin_radius, x=2, y=1),
        Pin(radius=pin_radius, x=8, y=1),
        Pin(radius=pin_radius, x=0, y=2),
        Pin(radius=pin_radius, x=1, y=2),
        Pin(radius=pin_radius, x=2, y=2),
        Pin(radius=pin_radius, x=3, y=2),
        Pin(radius=pin_radius, x=6, y=2),
        Pin(radius=pin_radius, x=8, y=2),
        Pin(radius=pin_radius, x=0, y=3),
        Pin(radius=pin_radius, x=4, y=3),
        Pin(radius=pin_radius, x=8, y=3),
        Pin(radius=pin_radius, x=1, y=6),
        Pin(radius=pin_radius, x=2, y=6),
        Pin(radius=pin_radius, x=3, y=6),
        Pin(radius=pin_radius, x=0, y=7),
        Pin(radius=pin_radius, x=1, y=7),
        Pin(radius=pin_radius, x=2, y=7),
        Pin(radius=pin_radius, x=3, y=7),
        Pin(radius=pin_radius, x=4, y=7),
        Pin(radius=pin_radius, x=5, y=7),
        Pin(radius=pin_radius, x=6, y=7),
        Pin(radius=pin_radius, x=7, y=7),
        Pin(radius=pin_radius, x=1, y=10),
        Pin(radius=pin_radius, x=2, y=10),
        Pin(radius=pin_radius, x=3, y=10),
        Pin(radius=pin_radius, x=4, y=10),
        Pin(radius=pin_radius, x=5, y=10),
        Pin(radius=pin_radius, x=6, y=10),
        Pin(radius=pin_radius, x=7, y=10),
        Pin(radius=pin_radius, x=4, y=11),
        Pin(radius=pin_radius, x=5, y=11),
        Pin(radius=pin_radius, x=3, y=12),
        Pin(radius=pin_radius, x=4, y=13),
        Pin(radius=pin_radius, x=5, y=13),
        Pin(radius=pin_radius, x=6, y=13),
        Pin(radius=pin_radius, x=8, y=13),
    ]

    multi_track1 = MultiTrack(x_start=1, y_start=0, width=track_width) \
        .move(x_offset=1, y_offset=1) \
        .move(x_offset=2, y_offset=0) \
        .move(x_offset=0, y_offset=1) \
        .move(x_offset=-3, y_offset=3) \
        .move(x_offset=0, y_offset=2) \
        .move(x_offset=-1, y_offset=0)

    multi_track2 = MultiTrack(x_start=7, y_start=0, width=track_width) \
        .move(x_offset=0, y_offset=1) \
        .move(x_offset=1, y_offset=0) \
        .move(x_offset=-2, y_offset=0) \
        .move(x_offset=-4, y_offset=4) \
        .move(x_offset=0, y_offset=2) \

    multi_track3 = MultiTrack(x_start=0, y_start=2, width=track_width) \
        .move(x_offset=3, y_offset=0)

    multi_track4 = MultiTrack(x_start=6, y_start=2, width=track_width) \
        .move(x_offset=2, y_offset=0) \
        .move(x_offset=-1, y_offset=0) \
        .move(x_offset=0, y_offset=6) \
        .move(x_offset=1, y_offset=1) \
        .move(x_offset=0, y_offset=1) \
        .move(x_offset=-1, y_offset=1) \
        .move(x_offset=-2, y_offset=0)

    multi_track5 = MultiTrack(x_start=3, y_start=6, width=track_width) \
        .move(x_offset=0, y_offset=1) \
        .move(x_offset=-1, y_offset=1) \
        .move(x_offset=-2, y_offset=0) \
        .move(x_offset=0, y_offset=3) \
        .move(x_offset=1, y_offset=1) \
        .move(x_offset=2, y_offset=0) \
        .move(x_offset=1, y_offset=1) \
        .move(x_offset=1, y_offset=0)

    multi_track6 = MultiTrack(x_start=1, y_start=10, width=track_width) \
        .move(x_offset=1, y_offset=1) \
        .move(x_offset=2, y_offset=0)

    multi_track7 = MultiTrack(x_start=6, y_start=13, width=track_width) \
        .move(x_offset=2, y_offset=0)

    tracks = [
        *multi_track1.tracks,
        *multi_track2.tracks,
        *multi_track3.tracks,
        *multi_track4.tracks,
        *multi_track5.tracks,
        *multi_track6.tracks,
        *multi_track7.tracks,
    ]

    return BoardPattern(x_count=9, y_count=14, x_indent=1.2, y_indent=1.2, pins=pins, tracks=tracks)
