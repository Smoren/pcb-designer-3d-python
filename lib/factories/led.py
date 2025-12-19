import numpy as np

from lib.base import BaseMeshBuilder
from lib.builders.led import LedBuilder
from lib.utils.constants import LED_RADIUS, LED_HEIGHT, LED_ANODE_LENGTH, LED_CATHODE_LENGTH, BOARD_GRID_STEP, \
    WIRE_CONTACT_RADIUS, BOARD_THICKNESS, WIRE_CONTACT_TOLERANCE, WIRE_CONTACT_COLOR, BOARD_CONTACT_PAD_RADIUS


def create_led_builder(color: np.ndarray) -> BaseMeshBuilder:
    return LedBuilder(
        radius=LED_RADIUS,
        height=LED_HEIGHT,
        anode_length=LED_ANODE_LENGTH,
        cathode_length=LED_CATHODE_LENGTH,
        anode_cathode_distance=BOARD_GRID_STEP - BOARD_CONTACT_PAD_RADIUS/2,
        contact_radius=WIRE_CONTACT_RADIUS,
        offset_z=-BOARD_THICKNESS/2 - WIRE_CONTACT_TOLERANCE - (LED_ANODE_LENGTH-LED_CATHODE_LENGTH),
        color=color,
        color_contact=WIRE_CONTACT_COLOR,
    )
