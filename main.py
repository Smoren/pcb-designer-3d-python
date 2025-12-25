from trimeshtools.combine import concatenate_meshes
from trimeshtools.move import move_to_bound
from trimeshtools.show import show_mesh

from app.box import create_middle_box_mesh
from app.elements import create_or_mesh
from app.test import create_test

if __name__ == '__main__':
    file_name = 'test'

    # final_mesh = create_test()
    final_mesh = create_or_mesh()
    move_to_bound(final_mesh, 0, 0)

    middle_box_mesh = create_middle_box_mesh()

    final_mesh = concatenate_meshes(final_mesh, middle_box_mesh)
    # final_mesh = middle_box_mesh

    print('is_watertight =', final_mesh.is_watertight)
    print('is_volume =', final_mesh.is_volume)

    final_mesh.export(f'output/{file_name}.obj')
    print(f'Saved: output/{file_name}.obj')

    show_mesh(final_mesh, with_axis=False)
