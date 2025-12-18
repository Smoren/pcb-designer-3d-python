from trimeshtools.combine import concatenate_meshes
from trimeshtools.show import show_mesh
from trimeshtools.utils import fix_all

from lib.base import GridPlacer, PositionSide, AxisDirection
from lib.factories.board import create_board_builder
from lib.factories.constants import BOARD_GRID_STEP
from lib.factories.resistor import create_resistor_builder

if __name__ == '__main__':
    file_name = 'test'

    placer = GridPlacer(BOARD_GRID_STEP, (0, 0, 0))

    board_builder = create_board_builder(14, 9, x_indent=1.2, y_indent=1.2)
    resistor_builder = create_resistor_builder(AxisDirection.ALONG_Y)

    board_mesh = placer.place(board_builder, (0, 0), PositionSide.TOP)
    resistor_mesh = placer.place(resistor_builder, (2, 3), PositionSide.TOP)

    final_mesh = concatenate_meshes(board_mesh, resistor_mesh)
    fix_all(final_mesh)

    print('is_watertight =', final_mesh.is_watertight)
    print('is_volume =', final_mesh.is_volume)

    final_mesh.export(f'output/{file_name}.stl')
    print(f'Saved: output/{file_name}.stl')

    show_mesh(final_mesh, with_axis=True)
