import math
from typing import List, Tuple

import numpy as np

from lib.builders.socket import SocketBuilder
from lib.constants import BOARD_GRID_STEP, BOARD_THICKNESS, WIRE_CONTACT_COLOR, SOCKET_THICKNESS, SOCKET_RADIUS, \
    SOCKET_PIN_RADIUS, SOCKET_PIN_WIDTH, SOCKET_PIN_THICKNESS, SOCKET_PIN_HEIGHT


def create_socket_builder(x_count: float, y_count: float, pin_positions: List[Tuple[float, float, float]], color: np.ndarray):
    return SocketBuilder(
        x_count=x_count,
        y_count=y_count,
        step=BOARD_GRID_STEP,
        thickness=SOCKET_THICKNESS,
        pin_positions=pin_positions,
        socket_radius=SOCKET_RADIUS,
        socket_pin_radius=SOCKET_PIN_RADIUS,
        pin_width=SOCKET_PIN_WIDTH,
        pin_thickness=SOCKET_PIN_THICKNESS,
        pin_height=SOCKET_PIN_HEIGHT,
        offset_z=BOARD_THICKNESS/2 - SOCKET_PIN_HEIGHT,
        color=color,
        contacts_color=WIRE_CONTACT_COLOR,
    )
