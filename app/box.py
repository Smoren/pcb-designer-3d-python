import numpy as np
import trimesh
from trimeshtools.combine import union_meshes
from trimeshtools.move import move_to_bound

THICKNESS = 4

SUPPORT_OFFSET = 2.25
SUPPORT_RADIUS = 7
SUPPORT_THICKNESS = 5
SUPPORT_THICKNESS_OFFSET = 1.7

SOCKET_WIDTH = 5.5
SOCKET_HEIGHT = 7.5
SOCKET_LEFT_OFFSET = -7.75
SOCKET_RIGHT_OFFSET = 7.5

OUTER_WIDTH = 31
OUTER_HEIGHT = 44
MIDDLE_OUTER_THICKNESS = 10
MIDDLE_TOLERANCE = 0.07

BOTTOM_OUTER_THICKNESS = 6
BOTTOM_BED_THICKNESS = 2
BOTTOM_HOLE_RADIUS = 3.90

TOP_DIODE_HOLE_RADIUS = 3
TOP_OUTER_THICKNESS = 5
TOP_ROOF_THICKNESS = 3
TOP_STEMS_THICKNESS = 12
TOP_STEM_DIAMETER = 3

TOP_BUTTON_OUTER_THICKNESS = 10
TOP_BUTTON_STEMS_THICKNESS = 16
TOP_BUTTON_HOLE_RADIUS = 10

def create_middle_box_mesh() -> trimesh.Trimesh:
    box_mesh = trimesh.creation.box((OUTER_WIDTH, OUTER_HEIGHT, MIDDLE_OUTER_THICKNESS))

    diff_mesh = trimesh.creation.box((OUTER_WIDTH - THICKNESS, OUTER_HEIGHT - THICKNESS, MIDDLE_OUTER_THICKNESS))
    box_mesh = box_mesh.difference(diff_mesh)

    support_mesh = trimesh.creation.box((OUTER_WIDTH - SUPPORT_OFFSET, OUTER_HEIGHT - SUPPORT_OFFSET, SUPPORT_THICKNESS))
    support_diff_mesh = trimesh.creation.box((OUTER_WIDTH - SUPPORT_RADIUS, OUTER_HEIGHT - SUPPORT_RADIUS, SUPPORT_THICKNESS * 2))
    support_mesh = support_mesh.difference(support_diff_mesh)
    move_to_bound(box_mesh, 0, 0, 1)
    move_to_bound(support_mesh, 0, 0, -1)
    support_mesh.apply_translation([0, 0, SUPPORT_THICKNESS_OFFSET])
    box_mesh = box_mesh.union(support_mesh)

    diff_mesh = trimesh.creation.box((SOCKET_WIDTH, SOCKET_WIDTH, SOCKET_HEIGHT))
    move_to_bound(box_mesh, 0, -1, -1)
    move_to_bound(diff_mesh, 0, 0, -1)
    box_mesh = box_mesh.difference(diff_mesh)

    move_to_bound(box_mesh, 0, 1, -1)
    move_to_bound(diff_mesh, 0, 1, -1)
    diff_mesh.apply_translation([SOCKET_LEFT_OFFSET, 0, 0])
    box_mesh = box_mesh.difference(diff_mesh)

    move_to_bound(diff_mesh, 0, 1, -1)
    diff_mesh.apply_translation([SOCKET_RIGHT_OFFSET, 0, 0])
    box_mesh = box_mesh.difference(diff_mesh)

    final_mesh = box_mesh

    move_to_bound(final_mesh, 0, 0, -1)
    final_mesh.visual.face_colors = np.array([0.7, 0.7, 0, 0.85])
    final_mesh.apply_translation([0, 0, 7.75])

    return final_mesh


def create_bottom_box_mesh() -> trimesh.Trimesh:
    walls_mesh = trimesh.creation.box((OUTER_WIDTH, OUTER_HEIGHT, BOTTOM_OUTER_THICKNESS))
    diff_mesh = trimesh.creation.box((OUTER_WIDTH - SUPPORT_OFFSET - MIDDLE_TOLERANCE, OUTER_HEIGHT - SUPPORT_OFFSET - MIDDLE_TOLERANCE, BOTTOM_OUTER_THICKNESS * 2))
    walls_mesh = walls_mesh.difference(diff_mesh)
    move_to_bound(walls_mesh, 0, 0, 1)

    bed_mesh = trimesh.creation.box((OUTER_WIDTH, OUTER_HEIGHT, BOTTOM_BED_THICKNESS))
    move_to_bound(bed_mesh, 0, 0, 1)

    final_mesh = union_meshes(walls_mesh, bed_mesh)

    hole_diff_mesh = trimesh.creation.cylinder(radius=BOTTOM_HOLE_RADIUS, height=BOTTOM_OUTER_THICKNESS*2)
    final_mesh = final_mesh.difference(hole_diff_mesh)

    move_to_bound(final_mesh, 0, 0, 0)
    final_mesh.visual.face_colors = np.array([0.7, 0, 0.7, 0.85])

    final_mesh.apply_translation([0, 0, -5.5])

    return final_mesh


def create_top_box_mesh() -> trimesh.Trimesh:
    walls_mesh = trimesh.creation.box((OUTER_WIDTH, OUTER_HEIGHT, TOP_OUTER_THICKNESS))
    diff_mesh = trimesh.creation.box((OUTER_WIDTH - THICKNESS, OUTER_HEIGHT - THICKNESS, TOP_OUTER_THICKNESS * 2))
    walls_mesh = walls_mesh.difference(diff_mesh)
    move_to_bound(walls_mesh, 0, 0, -1)

    roof_mesh = trimesh.creation.box((OUTER_WIDTH, OUTER_HEIGHT, TOP_ROOF_THICKNESS))
    diode_hole_diff_mesh = trimesh.creation.cylinder(radius=TOP_DIODE_HOLE_RADIUS, height=TOP_OUTER_THICKNESS*2)

    move_to_bound(diode_hole_diff_mesh, 0, 0, 0)
    diode_hole_diff_mesh.apply_translation([-10, -9, 0])
    roof_mesh = roof_mesh.difference(diode_hole_diff_mesh)

    move_to_bound(diode_hole_diff_mesh, 0, 0, 0)
    diode_hole_diff_mesh.apply_translation([10, -9, 0])
    roof_mesh = roof_mesh.difference(diode_hole_diff_mesh)

    move_to_bound(diode_hole_diff_mesh, 0, 0, 0)
    diode_hole_diff_mesh.apply_translation([5, 17, 0])
    roof_mesh = roof_mesh.difference(diode_hole_diff_mesh)

    move_to_bound(roof_mesh, 0, 0, -1)

    final_mesh = union_meshes(walls_mesh, roof_mesh)
    stem_mesh = trimesh.creation.box((TOP_STEM_DIAMETER, TOP_STEM_DIAMETER, TOP_STEMS_THICKNESS))

    move_to_bound(final_mesh, -1, -1, -1)
    move_to_bound(stem_mesh, -1, -1, -1)
    stem_mesh.apply_translation([-THICKNESS/2, -THICKNESS/2, 0])
    final_mesh = union_meshes(final_mesh, stem_mesh)

    move_to_bound(final_mesh, 1, -1, -1)
    move_to_bound(stem_mesh, 1, -1, -1)
    stem_mesh.apply_translation([THICKNESS/2, -THICKNESS/2, 0])
    final_mesh = union_meshes(final_mesh, stem_mesh)

    move_to_bound(final_mesh, -1, 1, -1)
    move_to_bound(stem_mesh, -1, 1, -1)
    stem_mesh.apply_translation([-THICKNESS/2, THICKNESS/2, 0])
    final_mesh = union_meshes(final_mesh, stem_mesh)

    move_to_bound(final_mesh, 1, 1, -1)
    move_to_bound(stem_mesh, 1, 1, -1)
    stem_mesh.apply_translation([THICKNESS/2, THICKNESS/2, 0])
    final_mesh = union_meshes(final_mesh, stem_mesh)

    move_to_bound(final_mesh, 0, 0, 0)
    final_mesh.visual.face_colors = np.array([0.7, 0, 0.7, 0.85])
    final_mesh.apply_translation([0, 0, 7])

    return final_mesh


def create_top_button_box_mesh() -> trimesh.Trimesh:
    walls_mesh = trimesh.creation.box((OUTER_WIDTH, OUTER_HEIGHT, TOP_BUTTON_OUTER_THICKNESS))
    diff_mesh = trimesh.creation.box((OUTER_WIDTH - THICKNESS, OUTER_HEIGHT - THICKNESS, TOP_BUTTON_OUTER_THICKNESS * 2))
    walls_mesh = walls_mesh.difference(diff_mesh)
    move_to_bound(walls_mesh, 0, 0, -1)

    roof_mesh = trimesh.creation.box((OUTER_WIDTH, OUTER_HEIGHT, TOP_ROOF_THICKNESS))
    hole_diff_mesh = trimesh.creation.cylinder(radius=TOP_BUTTON_HOLE_RADIUS, height=TOP_BUTTON_OUTER_THICKNESS*2)

    move_to_bound(hole_diff_mesh, 0, 0, 0)
    move_to_bound(roof_mesh, 0, 0, 0)
    roof_mesh = roof_mesh.difference(hole_diff_mesh)

    move_to_bound(roof_mesh, 0, 0, -1)

    final_mesh = union_meshes(walls_mesh, roof_mesh)
    stem_mesh = trimesh.creation.box((TOP_STEM_DIAMETER, TOP_STEM_DIAMETER, TOP_BUTTON_STEMS_THICKNESS))

    move_to_bound(final_mesh, -1, -1, -1)
    move_to_bound(stem_mesh, -1, -1, -1)
    stem_mesh.apply_translation([-THICKNESS/2, -THICKNESS/2, 0])
    final_mesh = union_meshes(final_mesh, stem_mesh)

    move_to_bound(final_mesh, 1, -1, -1)
    move_to_bound(stem_mesh, 1, -1, -1)
    stem_mesh.apply_translation([THICKNESS/2, -THICKNESS/2, 0])
    final_mesh = union_meshes(final_mesh, stem_mesh)

    move_to_bound(final_mesh, -1, 1, -1)
    move_to_bound(stem_mesh, -1, 1, -1)
    stem_mesh.apply_translation([-THICKNESS/2, THICKNESS/2, 0])
    final_mesh = union_meshes(final_mesh, stem_mesh)

    move_to_bound(final_mesh, 1, 1, -1)
    move_to_bound(stem_mesh, 1, 1, -1)
    stem_mesh.apply_translation([THICKNESS/2, THICKNESS/2, 0])
    final_mesh = union_meshes(final_mesh, stem_mesh)

    move_to_bound(final_mesh, 0, 0, 0)
    final_mesh.visual.face_colors = np.array([0.7, 0, 0.7, 0.85])
    final_mesh.apply_translation([0, 0, 7])

    return final_mesh
