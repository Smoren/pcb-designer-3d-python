import numpy as np

from lib.builders.jumper import JumperBuilder
from lib.constants import BOARD_GRID_STEP, BOARD_THICKNESS, BOARD_CONTACT_PAD_THICKNESS, COLOR_RED, \
    WIRE_CONTACT_RADIUS, WIRE_CONTACT_COLOR, BOARD_PAD_RADIUS, JUMPER_CONTACT_HEIGHT


def create_jumper_builder(x_count: int, y_count: int, offset_z: int = 0, color: np.ndarray = COLOR_RED):
    radius = WIRE_CONTACT_RADIUS*1.5
    return JumperBuilder(
        x_count=x_count,
        y_count=y_count,
        step=BOARD_GRID_STEP,
        step_delta=BOARD_PAD_RADIUS/2,
        radius=radius,
        contact_radius=WIRE_CONTACT_RADIUS,
        contact_height=(offset_z*2+1)*radius + WIRE_CONTACT_RADIUS/2 + JUMPER_CONTACT_HEIGHT,
        offset_z=BOARD_THICKNESS/2 - JUMPER_CONTACT_HEIGHT,
        color=color,
        contact_color=WIRE_CONTACT_COLOR,
    )
