from trimeshtools.combine import concatenate_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.show import show_mesh

from app.box import create_middle_box_mesh
from app.elements import create_or_mesh, create_or_board_pattern
from app.test import create_test
from lib.constants import BOARD_PAD_RADIUS, BOARD_CONTACT_PAD_RADIUS, TRACK_WIDTH, BOARD_GRID_STEP
from lib.pattern.builders import BoardPatternImageBuilder, BoardPatternMeshBuilder
from lib.pattern.structs import BoardPattern, Pin, Track, MultiTrack


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
    file_name = 'pattern'

    board_pattern = create_or_board_pattern()

    mesh_builder = BoardPatternMeshBuilder(step=BOARD_GRID_STEP, board_pattern=board_pattern, thickness=0.5)
    final_mesh = mesh_builder.build()

    print('is_watertight =', final_mesh.is_watertight)
    print('is_volume =', final_mesh.is_volume)

    final_mesh.export(f'output/{file_name}.stl')
    print(f'Saved: output/{file_name}.stl')

    show_mesh(final_mesh, with_axis=True)

    img_builder = BoardPatternImageBuilder(step=BOARD_GRID_STEP, board_pattern=board_pattern, dpi=300)
    image = img_builder.build()

    image.save("output/pattern.png", dpi=(300, 300))
    image.show()


if __name__ == '__main__':
    # run_build_mesh()
    run_build_pattern()
