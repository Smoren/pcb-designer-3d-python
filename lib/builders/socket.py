import math

import numpy as np
import trimesh
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_x, create_rotation_matrix_for_z

from lib.base import BaseMeshBuilder, PositionSide, Rotation, FloatPosition3d
from lib.constants import BOARD_GRID_STEP, CYLINDER_SECTIONS, BOARD_THICKNESS, BOARD_CONTACT_PAD_THICKNESS


class SocketBuilder(BaseMeshBuilder):
    def build(self) -> trimesh.Trimesh:
        x_count = 4.5
        y_count = 2
        step = BOARD_GRID_STEP
        thickness = 5.0
        pins = [(2, 0.5, math.pi/2), (4, 0, 0.0)]
        socket_radius = 1.5
        socket_depth = 5.0
        pin_thickness = 0.3
        pin_height = 3.0
        offset_z = BOARD_THICKNESS/2
        color = np.array([50, 50, 50, 255])

        box_mesh = trimesh.creation.box([x_count*step, y_count*step, thickness])
        box_diff = trimesh.creation.cylinder(radius=socket_radius, height=socket_depth, sections=CYLINDER_SECTIONS)
        box_diff.apply_transform(create_rotation_matrix_for_x(math.pi/2))
        box_diff.apply_transform(create_rotation_matrix_for_z(math.pi/2))
        move_to_bound(box_mesh, -1, 0, 0)
        move_to_bound(box_diff, -1, 0, 0)
        box_mesh = box_mesh.difference(box_diff)
        box_mesh.visual.face_colors = color

        return box_mesh

    def get_offset(self, side: PositionSide, rotation: Rotation) -> FloatPosition3d:
        offset_z = BOARD_THICKNESS/2 + BOARD_CONTACT_PAD_THICKNESS + 0.1
        return 0, 0, offset_z
