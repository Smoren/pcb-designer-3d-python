import trimesh
from trimeshtools.move import move_to_bound


def create_middle_box_mesh() -> trimesh.Trimesh:
    OUTER_WIDTH = 31
    OUTER_HEIGHT = 44
    THICKNESS = 4
    SUPPORT_OFFSET = 2.25
    SUPPORT_RADIUS = 7
    SUPPORT_THICKNESS = 4
    SUPPORT_THICKNESS_OFFSET = 1.5
    SOCKET_WIDTH = 5.5
    SOCKET_HEIGHT = 5.25
    SOCKET_LEFT_OFFSET = -7.75
    SOCKET_RIGHT_OFFSET = 7.5

    box_mesh = trimesh.creation.box((OUTER_WIDTH, OUTER_HEIGHT, 10))

    diff_mesh = trimesh.creation.box((OUTER_WIDTH-THICKNESS, OUTER_HEIGHT-THICKNESS, 10))
    box_mesh = box_mesh.difference(diff_mesh)

    support_mesh = trimesh.creation.box((OUTER_WIDTH-SUPPORT_OFFSET, OUTER_HEIGHT-SUPPORT_OFFSET, SUPPORT_THICKNESS))
    support_diff_mesh = trimesh.creation.box((OUTER_WIDTH-SUPPORT_RADIUS, OUTER_HEIGHT-SUPPORT_RADIUS, SUPPORT_THICKNESS*2))
    support_mesh = support_mesh.difference(support_diff_mesh)
    move_to_bound(box_mesh, 0, 0, 1)
    move_to_bound(support_mesh, 0, 0, 1)
    support_mesh.apply_translation([0, 0, -SUPPORT_THICKNESS_OFFSET])
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

    move_to_bound(final_mesh, 0, 0, 0)
    final_mesh.apply_translation([0, 0, -0.25])
    return final_mesh
