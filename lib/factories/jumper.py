import numpy as np

from lib.builders.jumper import JumperBuilder
from lib.constants import BOARD_GRID_STEP, BOARD_THICKNESS, COLOR_RED, \
    WIRE_CONTACT_RADIUS, WIRE_CONTACT_COLOR, BOARD_PAD_RADIUS, WIRE_CONTACT_HEIGHT, WIRE_ISOLATION_RADIUS


def create_jumper_builder(x_count: int, y_count: int, offset_z: int = 0, color: np.ndarray = COLOR_RED):
    return JumperBuilder(
        x_count=x_count,
        y_count=y_count,
        step=BOARD_GRID_STEP,
        step_delta=BOARD_PAD_RADIUS/2,
        radius=WIRE_ISOLATION_RADIUS,
        contact_radius=WIRE_CONTACT_RADIUS,
        contact_height=(offset_z*2+1) * WIRE_ISOLATION_RADIUS + WIRE_CONTACT_RADIUS / 2 + WIRE_CONTACT_HEIGHT,
        offset_z=BOARD_THICKNESS / 2 - WIRE_CONTACT_HEIGHT,
        color=color,
        contact_color=WIRE_CONTACT_COLOR,
    )
