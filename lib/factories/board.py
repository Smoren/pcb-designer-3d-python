import numpy as np

from lib.base import BaseMeshBuilder
from lib.builders.board import PrototypingBoardBuilder, PrintedBoardBuilder
from lib.constants import BOARD_GRID_STEP, BOARD_PAD_RADIUS, BOARD_THICKNESS, BOARD_CONTACT_PAD_RADIUS, \
    BOARD_CONTACT_PAD_THICKNESS, BOARD_COLOR, BOARD_CONTACT_PAD_COLOR, TRACK_COLOR, BOARD_CONTACT_TRACK_COLOR
from lib.pattern.structs import BoardPattern


def create_prototyping_board_builder(x_count: int, y_count: int, x_indent: float = 0, y_indent: float = 0) -> BaseMeshBuilder:
    return PrototypingBoardBuilder(
        x_count=x_count,
        y_count=y_count,
        step=BOARD_GRID_STEP,
        pad_radius=BOARD_PAD_RADIUS,
        contact_pad_radius=BOARD_CONTACT_PAD_RADIUS,
        contact_pad_thickness=BOARD_CONTACT_PAD_THICKNESS,
        thickness=BOARD_THICKNESS,
        x_indent=x_indent,
        y_indent=y_indent,
        color=BOARD_COLOR,
        contact_pad_color=BOARD_CONTACT_PAD_COLOR,
    )


def create_printed_board_builder(board_pattern: BoardPattern) -> BaseMeshBuilder:
    return PrintedBoardBuilder(
        board_pattern=board_pattern,
        step=BOARD_GRID_STEP,
        pad_radius=BOARD_PAD_RADIUS,
        contact_pad_radius=BOARD_CONTACT_PAD_RADIUS,
        contact_pad_thickness=BOARD_CONTACT_PAD_THICKNESS,
        thickness=BOARD_THICKNESS,
        color=BOARD_COLOR,
        contact_pad_color=BOARD_CONTACT_PAD_COLOR,
        track_color=BOARD_CONTACT_TRACK_COLOR,
    )
