import numpy as np

from lib.builders.track import TrackBuilder
from lib.constants import BOARD_GRID_STEP, BOARD_THICKNESS, BOARD_CONTACT_PAD_THICKNESS, TRACK_COLOR, TRACK_WIDTH


def create_track_builder(x_count: int, y_count: int, color: np.ndarray = TRACK_COLOR):
    return TrackBuilder(
        x_count=x_count,
        y_count=y_count,
        step=BOARD_GRID_STEP,
        radius=TRACK_WIDTH/2,
        offset_z=BOARD_THICKNESS / 2 - BOARD_CONTACT_PAD_THICKNESS,
        color=color,
    )
