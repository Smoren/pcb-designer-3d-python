from trimeshtools.show import show_mesh

from app.elements import create_or_mesh
from app.test import create_test

if __name__ == '__main__':
    file_name = 'test'

    # final_mesh = create_test()
    final_mesh = create_or_mesh()

    print('is_watertight =', final_mesh.is_watertight)
    print('is_volume =', final_mesh.is_volume)

    final_mesh.export(f'output/{file_name}.obj')
    print(f'Saved: output/{file_name}.obj')

    show_mesh(final_mesh, with_axis=False)
