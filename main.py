from trimeshtools.combine import concatenate_meshes
from trimeshtools.show import show_mesh
from trimeshtools.utils import fix_all

from lib.base import GridPlacer, PositionSide, Rotation
from lib.factories.board import create_board_builder
from lib.factories.chip import create_chip_builder
from lib.factories.constants import BOARD_GRID_STEP, LED_COLOR_BLUE, LED_COLOR_RED
from lib.factories.led import create_led_builder
from lib.factories.resistor import create_resistor_builder

if __name__ == '__main__':
    file_name = 'test'

    placer = GridPlacer(BOARD_GRID_STEP, (0, 0, 0))

    board_builder = create_board_builder(14, 9, x_indent=1.2, y_indent=1.2)
    resistor_builder = create_resistor_builder()
    chip_builder = create_chip_builder(x_count=7, y_count=2)
    blue_led_builder = create_led_builder(LED_COLOR_BLUE)
    red_led_builder = create_led_builder(LED_COLOR_RED)

    board_mesh = placer.place(board_builder, (0, 0), PositionSide.TOP, Rotation.NO_ROTATION)
    resistor_mesh1 = placer.place(resistor_builder, (1, 2), PositionSide.TOP, Rotation.NO_ROTATION)
    resistor_mesh2 = placer.place(resistor_builder, (13, 3), PositionSide.TOP, Rotation.ROTATE_CLOCKWISE_90)
    resistor_mesh3 = placer.place(resistor_builder, (13, 4), PositionSide.BOTTOM, Rotation.ROTATE_CLOCKWISE_90)
    chip_mesh = placer.place(chip_builder, (2, 3), PositionSide.TOP, Rotation.NO_ROTATION)
    led_blue_mesh = placer.place(blue_led_builder, (0, 0), PositionSide.TOP, Rotation.NO_ROTATION)
    led_red_mesh = placer.place(red_led_builder, (2, 0), PositionSide.TOP, Rotation.ROTATE_CLOCKWISE_90)

    # final_mesh = concatenate_meshes(board_mesh, resistor_mesh1, resistor_mesh2, resistor_mesh3)
    final_mesh = concatenate_meshes(board_mesh, resistor_mesh1, resistor_mesh2, resistor_mesh3, led_blue_mesh, led_red_mesh)
    fix_all(final_mesh)

    print('is_watertight =', final_mesh.is_watertight)
    print('is_volume =', final_mesh.is_volume)

    final_mesh.export(f'output/{file_name}.stl')
    print(f'Saved: output/{file_name}.stl')

    show_mesh(final_mesh, with_axis=False)
