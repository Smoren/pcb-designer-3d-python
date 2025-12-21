import numpy as np

from lib.base import BaseMeshBuilder
from lib.builders.chip import ChipBuilder
from lib.constants import BOARD_GRID_STEP, WIRE_CONTACT_COLOR, CHIP_DEFAULT_COLOR, CHIP_PIN_THICKNESS, \
    CHIP_PIN_TOP_VERTICAL_LENGTH, CHIP_PIN_BOTTOM_VERTICAL_LENGTH, CHIP_PIN_TOP_WIDTH, CHIP_PIN_BOTTOM_WIDTH, \
    CHIP_PIT_RADIUS, CHIP_PIT_HEIGHT, CHIP_THICKNESS, BOARD_THICKNESS


def create_chip_builder(x_count: int, y_count: int, color: np.ndarray = CHIP_DEFAULT_COLOR) -> BaseMeshBuilder:
    return ChipBuilder(
        x_count=x_count,
        y_count=y_count,
        thickness=CHIP_THICKNESS,
        pit_radius=CHIP_PIT_RADIUS,
        pit_height=CHIP_PIT_HEIGHT,
        pin_thickness=CHIP_PIN_THICKNESS,
        pin_top_vertical_length=CHIP_PIN_TOP_VERTICAL_LENGTH,
        pin_bottom_vertical_length=CHIP_PIN_BOTTOM_VERTICAL_LENGTH,
        pin_top_width=CHIP_PIN_TOP_WIDTH,
        pin_bottom_width=CHIP_PIN_BOTTOM_WIDTH,
        step=BOARD_GRID_STEP,
        offset_z=BOARD_THICKNESS/2 - CHIP_PIN_BOTTOM_VERTICAL_LENGTH,
        color=color,
        contacts_color=WIRE_CONTACT_COLOR,
    )
