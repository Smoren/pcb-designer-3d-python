import numpy as np

from lib.builders.wire import WireBuilder
from lib.constants import WIRE_CONTACT_COLOR, WIRE_CONTACT_RADIUS, WIRE_CONTACT_HEIGHT, WIRE_ISOLATION_RADIUS


def create_wire_builder(length: float, color: np.ndarray):
    return WireBuilder(
        length=length,
        contact_length=WIRE_CONTACT_HEIGHT,
        radius=WIRE_ISOLATION_RADIUS,
        contact_radius=WIRE_CONTACT_RADIUS,
        offset_z=0,
        color=color,
        contact_color=WIRE_CONTACT_COLOR
    )
