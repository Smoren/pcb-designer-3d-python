from trimeshtools.show import show_mesh
from trimeshtools.utils import fix_all

from lib.base import GridPlacer, PositionSide, AxisDirection
from lib.factories.board import create_board_builder
from lib.factories.constants import BOARD_GRID_STEP

if __name__ == '__main__':
    file_name = 'test'

    # builder = ResistorBuilder(30, 5, AxisDirection.ALONG_X)
    builder = create_board_builder(14, 9, x_indent=1.2, y_indent=1.2)
    placer = GridPlacer(BOARD_GRID_STEP, (0, 0, 0))

    final_mesh = placer.place(builder, (0, 0), PositionSide.TOP)
    fix_all(final_mesh)

    print('is_watertight =', final_mesh.is_watertight)
    print('is_volume =', final_mesh.is_volume)

    final_mesh.export(f'output/{file_name}.stl')
    print(f'Saved: output/{file_name}.stl')

    show_mesh(final_mesh, with_axis=True)
