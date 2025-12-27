from trimeshtools.combine import concatenate_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.show import show_mesh

from app.box import create_middle_box_mesh
from app.elements import create_or_mesh
from app.test import create_test
from lib.constants import BOARD_PAD_RADIUS, BOARD_CONTACT_PAD_RADIUS, TRACK_WIDTH, BOARD_GRID_STEP
from lib.pattern.builders import BoardImageBuilder
from lib.pattern.structs import Board, Pin, Track, MultiTrack


def run_build_mesh():
    file_name = 'test'

    # final_mesh = create_test()
    final_mesh = create_or_mesh()
    move_to_bound(final_mesh, 0, 0)

    middle_box_mesh = create_middle_box_mesh()

    final_mesh = concatenate_meshes(final_mesh, middle_box_mesh)
    # final_mesh = middle_box_mesh

    print('is_watertight =', final_mesh.is_watertight)
    print('is_volume =', final_mesh.is_volume)

    final_mesh.export(f'output/{file_name}.obj')
    print(f'Saved: output/{file_name}.obj')

    show_mesh(final_mesh, with_axis=False)


def run_build_pattern():
    board = Board(x_count=9, y_count=14, x_indent=1.2, y_indent=1.2)
    pin_radius = BOARD_CONTACT_PAD_RADIUS
    track_width = TRACK_WIDTH/1.5

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

    builder = BoardImageBuilder(step=BOARD_GRID_STEP, board=board, pins=pins, tracks=tracks, dpi=300)
    image = builder.build()

    # Сохраняем изображение
    image.save("output/pattern.png", dpi=(300, 300))
    image.show()


if __name__ == '__main__':
    # run_build_mesh()
    run_build_pattern()
