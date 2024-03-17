"""A sample using ply."""

from ctypes import c_float, c_uint, c_uint8
from ctypes import Array, sizeof, cast, POINTER
import os

import numpy
import plyfile  # type: ignore

import meshopt
from meshopt.memory import (
    make_meshlets,
    make_meshlet_vertices,
    make_meshlet_triangles,
)


def main():
    source = os.path.join(os.path.dirname(__file__), 'bun_zipper.ply')

    print('Reading PLY file...')

    # read data
    vertex_positions, indices = read_ply(source)

    # cast positions to one dimensional array
    vertex_count = len(vertex_positions)
    vertex_positions_stride = sizeof(c_float) * 3

    # indices
    index_count = len(indices)

    # parameters for meshlet
    max_vertices = 64
    max_triangles = 124
    cone_weight = 0.0

    # compute meshlets' bound
    max_meshlets = meshopt.buildMeshletsBound(
        index_count, max_vertices, max_triangles
    )

    # create buffers
    meshlets = make_meshlets(max_meshlets)
    meshlet_vertices = make_meshlet_vertices(max_meshlets, max_vertices)
    meshlet_triangles = make_meshlet_triangles(max_meshlets, max_triangles)

    print('Building meshlets...')

    # build
    meshlet_count = meshopt.buildMeshlets(
        meshlets,
        meshlet_vertices,
        meshlet_triangles,
        indices,
        index_count,
        cast(vertex_positions, POINTER(c_float)),
        vertex_count,
        vertex_positions_stride,
        max_vertices,
        max_triangles,
        cone_weight,
    )

    print(f'{meshlet_count} meshlets')

    target = os.path.join(
        os.path.dirname(__file__),
        '../build/examples/bun_zipper_meshlets.ply',
    )
    os.makedirs(os.path.dirname(target), exist_ok=True)

    print('Writing PLY file...')

    # meshlets to PLY file
    meshlets_to_ply(
        target,
        meshlets,
        meshlet_count,
        meshlet_vertices,
        meshlet_triangles,
        vertex_positions,
    )


def read_ply(
    path: str,
) -> tuple[Array[Array[c_float]], Array[c_uint]]:
    """Read PLY file and return vertices and triangle indices.

    Args:
        path (str): Path to PLY file.

    Returns:
        tuple[Array[Array[c_float]], Array[c_uint]]: Vertices as float[][3] and indices of triangles as uint[].
    """

    plydata = plyfile.PlyData.read(
        path, known_list_len={'face': {'vertex_indices': 3}}
    )

    vertices: numpy.ndarray = plydata['vertex'].data
    faces: numpy.ndarray = plydata['face'].data

    VertexArrayType = c_float * 3 * vertices.size  # [x, y, z] * vertex_count
    vertex_positions = VertexArrayType()

    for i, vertex in enumerate(vertices):
        vertex_positions[i] = (vertex['x'], vertex['y'], vertex['z'])  # type: ignore

    TriangleArrayType = c_uint * (3 * faces.size)
    indices = TriangleArrayType()

    for i, face in enumerate(faces):
        end = (begin := i * 3) + 3
        indices[begin:end] = face[0]

    return vertex_positions, indices


def meshlets_to_ply(
    path: str,
    meshlets: Array[meshopt.Meshlet],
    meshlet_count: int,
    meshlet_vertices: Array[c_uint],
    meshlet_triangles: Array[c_uint8],
    vertex_positions: Array[Array[c_float]],
):
    """Write coloured meshlets to PLY file.

    This just marks meshlets with colours, not for a practical use.
    This does not use "plyfile" for the speed and the simplicity.

    Args:
        path (str): Path to PLY file.
    """

    # colour table to use for marking meshlets
    colors = (
        (0xFF, 0xFF, 0xFF),
        (0xC0, 0xC0, 0xC0),
        (0x80, 0x80, 0x80),
        (0x00, 0x00, 0x00),
        (0xFF, 0x00, 0x00),
        (0x80, 0x00, 0x00),
        (0xFF, 0xFF, 0x00),
        (0x80, 0x80, 0x00),
        (0x00, 0xFF, 0x00),
        (0x00, 0x80, 0x00),
        (0x00, 0xFF, 0xFF),
        (0x00, 0x80, 0x80),
        (0x00, 0x00, 0xFF),
        (0x00, 0x00, 0x80),
        (0xFF, 0x00, 0xFF),
        (0x80, 0x00, 0x80),
    )
    color_count = len(colors)

    # calculate total vertex count, which is usually greater than
    # the original vertex_count due to duplicate vertices of borders.
    total_vertex_count = sum(
        meshlets[m].vertex_count for m in range(meshlet_count)
    )

    # calculate total index count, which should be the same as the original indices.
    total_triangle_count = sum(
        meshlets[m].triangle_count for m in range(meshlet_count)
    )

    # store strings to write to PLY file.
    index_offset = 0
    vertices = list()
    indices = list()

    for m in range(meshlet_count):
        meshlet: meshopt.Meshlet = meshlets[m]

        vertex_offset = int(meshlet.vertex_offset)
        vertex_count = int(meshlet.vertex_count)

        for i in range(vertex_offset, vertex_offset + vertex_count):
            # position
            position = vertex_positions[meshlet_vertices[i]]
            vertices.append(f'{" ".join(str(p) for p in position)}')

            # colour
            color = colors[m % color_count]
            vertices.append(f' {" ".join(str(c) for c in color)}\n')

        triangle_offset = int(meshlet.triangle_offset)
        triangle_count = int(meshlet.triangle_count)

        for i in range(triangle_count):
            end = (begin := triangle_offset + i * 3) + 3

            indices.append('3')
            for index in meshlet_triangles[begin:end]:
                indices.append(f' {vertex_offset + index}')
            indices.append('\n')

        index_offset += triangle_count

    # write stored strings to PLY file.
    with open(path, 'w', newline='\n') as file:
        file.write( 'ply\n'
                    'format ascii 1.0\n'
                   f'element vertex {total_vertex_count}\n'
                    'property float x\n'
                    'property float y\n'
                    'property float z\n'
                    'property uchar red\n'
                    'property uchar green\n'
                    'property uchar blue\n'
                   f'element face {total_triangle_count}\n'
                    'property list uchar uint vertex_indices\n'
                    'end_header\n')  # fmt: skip

        file.writelines(vertices)
        file.writelines(indices)


if __name__ == '__main__':
    main()
