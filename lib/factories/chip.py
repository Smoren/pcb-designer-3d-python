import numpy as np

from lib.base import BaseMeshBuilder, Rotation
from lib.builders.chip import ChipBuilder
from lib.factories.constants import BOARD_GRID_STEP, WIRE_CONTACT_COLOR


def create_chip_builder(x_count: int, y_count: int) -> BaseMeshBuilder:
    return ChipBuilder(
        x_count=x_count,
        y_count=y_count,
        thickness=2,
        step=BOARD_GRID_STEP,
        color=np.array([30, 30, 30, 255]),
        contacts_color=WIRE_CONTACT_COLOR,
    )
