import math

import pyvista as pv
import trimesh
from trimeshtools.combine import union_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.rotate import create_rotation_matrix_for_x, create_rotation_matrix_for_z

from lib.constants import CYLINDER_SECTIONS


def create_bounded_pipe_mesh(pipe_radius: float, bond_radius: float, horizontal_length: float, vertical_length: float) -> trimesh.Trimesh:
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


def create_pin_mesh(thickness: float, horizontal_length: float, top_vertical_length: float, bottom_vertical_length: float, top_width: float, bottom_width: float) -> trimesh.Trimesh:
    top_horizontal_mesh = trimesh.creation.box([horizontal_length, top_width, thickness])
    top_vertical_mesh = trimesh.creation.box([thickness, top_width, top_vertical_length])
    move_to_bound(top_horizontal_mesh, -1, 0, -1)
    move_to_bound(top_vertical_mesh, 1, 0, -1)
    top_mesh = union_meshes(top_vertical_mesh, top_horizontal_mesh)

    bottom_mesh = trimesh.creation.box([thickness, bottom_width, bottom_vertical_length])
    move_to_bound(top_mesh, -1, 0, 1)
    move_to_bound(bottom_mesh, -1, 0, -1)

    final_mesh = union_meshes(top_mesh, bottom_mesh)
    return final_mesh


def create_text_mesh(text: str, height: float, scale: float = 1.0) -> trimesh.Trimesh:
    # Создаем текст в PyVista
    text_mesh = pv.Text3D(text, depth=height)

    # Конвертируем в trimesh
    vertices = text_mesh.points
    vertices *= scale
    faces = text_mesh.faces.reshape(-1, 4)[:, 1:4]  # Преобразуем quad в tri

    # Создаем trimesh объект
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    return mesh