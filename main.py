from trimeshtools.show import show_mesh

from lib.base import GridPlacer, PositionSide, AxisDirection
from lib.builders.board import BoardBuilder
from lib.builders.resistor import ResistorBuilder
from lib.factories.board import create_board_builder

if __name__ == '__main__':
    file_name = 'test'

    # builder = ResistorBuilder(30, 5, AxisDirection.ALONG_X)
    builder = create_board_builder(10, 5, x_indent=1.2, y_indent=1.2)
    placer = GridPlacer(10, (0, 0, 0))

    final_mesh = placer.place(builder, (0, 0), PositionSide.TOP)
    # fix_all(final_mesh)

    print('is_watertight =', final_mesh.is_watertight)
    print('is_volume =', final_mesh.is_volume)

    final_mesh.export(f'output/{file_name}.stl')
    print(f'Saved: output/{file_name}.stl')

    show_mesh(final_mesh, with_axis=True)
