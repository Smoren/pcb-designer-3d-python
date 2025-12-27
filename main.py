from trimeshtools.combine import concatenate_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.show import show_mesh

from app.box import create_middle_box_mesh
from app.elements import create_or_mesh
from app.test import create_test
from lib.constants import BOARD_PAD_RADIUS, BOARD_CONTACT_PAD_RADIUS, TRACK_WIDTH, BOARD_GRID_STEP
from lib.pattern.builders import BoardImageBuilder
from lib.pattern.structs import Board, Pin, Track


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

    pins = [
        # Pin(radius=BOARD_CONTACT_PAD_RADIUS, x=2, y=3),
        # Pin(outer_radius=BOARD_CONTACT_PAD_RADIUS, x=5, y=5),
        # Pin(outer_radius=BOARD_CONTACT_PAD_RADIUS, x=8, y=2)
    ]

    tracks = [
        Track(x=1, y=3, x_count=3, y_count=0, width=TRACK_WIDTH),
        # Track(x=4, y=3, x_count=0, y_count=2, width=TRACK_WIDTH),
        # Track(x=3, y=4, x_count=2, y_count=2, width=TRACK_WIDTH)
    ]

    builder = BoardImageBuilder(step=BOARD_GRID_STEP, board=board, pins=pins, tracks=tracks, dpi=300)
    image = builder.build()

    # Сохраняем изображение
    image.save("output/pattern.png", dpi=(300, 300))
    image.show()


if __name__ == '__main__':
    # run_build_mesh()
    run_build_pattern()
