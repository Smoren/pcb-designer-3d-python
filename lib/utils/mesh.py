import math

import trimesh
from trimeshtools.combine import union_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_x, create_rotation_matrix_for_z

from lib.constants import CYLINDER_SECTIONS


def create_bounded_pipe_mesh(pipe_radius: float, bond_radius: float, horizontal_length: float, vertical_length: float):
    vertical_cylinder = trimesh.creation.cylinder(radius=pipe_radius, height=vertical_length - bond_radius, sections=CYLINDER_SECTIONS)
    horizontal_cylinder = trimesh.creation.cylinder(radius=pipe_radius, height=horizontal_length - bond_radius, sections=CYLINDER_SECTIONS)
    horizontal_cylinder.apply_transform(create_rotation_matrix_for_x(math.pi / 2))
    horizontal_cylinder.apply_transform(create_rotation_matrix_for_z(math.pi / 2))

    torus = trimesh.creation.torus(major_radius=bond_radius, minor_radius=pipe_radius, major_sections=CYLINDER_SECTIONS, minor_sections=CYLINDER_SECTIONS)
    torus.apply_transform(create_rotation_matrix_for_x(math.pi / 2))
    diff_box = trimesh.creation.box([(bond_radius + pipe_radius) * 2, (bond_radius + pipe_radius) * 2, (bond_radius + pipe_radius) * 2])
    torus = torus.difference(move_to_bound(diff_box, 1, 0, 0))
    torus = torus.difference(move_to_bound(diff_box, 0, 0, -1))

    move_to_bound(torus, 1, 0, 1)
    move_to_bound(vertical_cylinder, 1, 0, -1)
    final_mesh = union_meshes(vertical_cylinder, torus)

    move_to_bound(final_mesh, -1, 0, -1)
    move_to_bound(horizontal_cylinder, 1, 0, -1)
    final_mesh = union_meshes(horizontal_cylinder, final_mesh)

    final_mesh.apply_translation([0, 0, pipe_radius])

    return final_mesh
