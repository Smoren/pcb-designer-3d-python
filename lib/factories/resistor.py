import numpy as np

from lib.base import CachedMeshBuilder, AxisDirection
from lib.builders.resistor import ResistorBuilder
from lib.factories.constants import BOARD_GRID_STEP, RESISTOR_STEPS_COUNT, RESISTOR_RADIUS, WIRE_CONTACT_RADIUS, \
    RESISTOR_WIRE_BOND_RADIUS, BOARD_PAD_RADIUS, BOARD_THICKNESS, WIRE_CONTACT_TOLERANCE, BOARD_CONTACT_PAD_THICKNESS, \
    RESISTOR_TOLERANCE, RESISTOR_DEFAULT_COLOR, WIRE_COLOR


def create_resistor_builder(axis_direction: AxisDirection, color: np.ndarray = RESISTOR_DEFAULT_COLOR):
    return CachedMeshBuilder(ResistorBuilder(
        length=BOARD_GRID_STEP*RESISTOR_STEPS_COUNT,
        radius=RESISTOR_RADIUS,
        axis_direction=axis_direction,
        wire_contact_radius=WIRE_CONTACT_RADIUS,
        wire_bond_radius=RESISTOR_WIRE_BOND_RADIUS,
        wire_horizontal_length=BOARD_GRID_STEP - BOARD_PAD_RADIUS/2,
        wire_vertical_length=RESISTOR_RADIUS + RESISTOR_TOLERANCE + BOARD_THICKNESS + BOARD_CONTACT_PAD_THICKNESS + WIRE_CONTACT_TOLERANCE,
        offset_z=-BOARD_THICKNESS/2 - WIRE_CONTACT_TOLERANCE,
        color=color,
        color_wire=WIRE_COLOR,
    ))
