"""Python bindings for meshoptimzer."""

from ctypes import cdll
from ctypes import c_float, c_uint, c_uint8, Array
from ctypes import sizeof
import os
from typing import Any

from ._types import *
from .memory import *

__all__ = [
    'buildMeshletsBound',
    'buildMeshlets',
    'buildMeshletsBound_safe',
    'buildMeshlets_safe',
]


# This must be <= 255 since index 0xff is used internally to indice a vertex
# that doesn't belong to a meshlet
kMeshletMaxVertices = 255  # pylint: disable=invalid-name

# A reasonable limit is around 2*max_vertices or less
kMeshletMaxTriangles = 512  # pylint: disable=invalid-name

_meshopt = cdll.LoadLibrary(
    os.path.join(os.path.dirname(__file__), 'meshoptimizer.dll')
)


def buildMeshletsBound(
    index_count: int, max_vertices: int, max_triangles: int
) -> int:
    """Meshlets must contain enough space for all meshlets, worst case size
    can be computed with buildMeshletsBound.

    Args:
        index_count (int): _description_
        max_vertices (int): _description_
        max_triangles (int): _description_

    Returns:
        int: _description_
    """

    result = _meshopt.meshopt_buildMeshletsBound(
        index_count, max_vertices, max_triangles
    )

    return result


def buildMeshlets(
    meshlets: Array[Meshlet],
    meshlet_vertices: Array[c_uint],
    meshlet_triangles: Array[c_uint8],
    indices: Array[c_uint],
    index_count: int,
    vertex_positions: Array[c_float] | Array[Array[c_float]] | int | Any,
    vertex_count: int,
    vertex_positions_stride: int,
    max_vertices: int,
    max_triangles: int,
    cone_weight: float,
) -> int:
    """A binding to meshopt_buildMeshlets().
    max_meshlets can be computed with buildMeshletsBound().

    Args:
        meshlets (Array[Meshlet]): _description_
        meshlet_vertices (Array[c_uint]): _description_
        meshlet_triangles (Array[c_uint8]): _description_
        indices (Array[c_uint]): _description_
        index_count (int): _description_
        vertex_positions: Array, address, or pointer returned by byref to vertices.
        vertex_count (int): _description_
        vertex_positions_stride (int): _description_
        max_vertices (int): _description_
        max_triangles (int): _description_
        cone_weight (float): _description_

    Returns:
        int: meshlet_count
    """

    meshlet_count: int = _meshopt.meshopt_buildMeshlets(
        meshlets,
        meshlet_vertices,
        meshlet_triangles,
        indices,
        index_count,
        vertex_positions,
        vertex_count,
        vertex_positions_stride,
        max_vertices,
        max_triangles,
        c_float(cone_weight),
    )

    return meshlet_count


def buildMeshlets2(
    max_meshlets: int,
    indices: Array[c_uint],
    index_count: int,
    vertex_positions: Array[c_float],
    vertex_count: int,
    vertex_positions_stride: int,
    max_vertices: int,
    max_triangles: int,
    cone_weight: float,
) -> tuple[int, Array[Meshlet], Array[c_uint], Array[c_uint8]]:
    """A binding to meshopt_buildMeshlets().
    max_meshlets can be computed with buildMeshletsBound().

    Args:
        max_meshlets (int): Worst case size for all meshlets.
        indices (Array[c_uint]): _description_
        index_count (int): _description_
        vertex_positions (Array[c_float]): _description_
        vertex_count (int): _description_
        vertex_positions_stride (int): _description_
        max_vertices (int): _description_
        max_triangles (int): _description_
        cone_weight (float): _description_

    Returns:
        tuple[int, Array[Meshlet], Array[c_uint], Array[c_uint8]]:
            meshlet_count, meshlets, meshlet_vertices, meshlet_triangles
    """

    meshlets = make_meshlets(max_meshlets)
    meshlet_vertices = make_meshlet_vertices(max_meshlets, max_vertices)
    meshlet_triangles = make_meshlet_triangles(max_meshlets, max_triangles)

    meshlet_count: int = _meshopt.meshopt_buildMeshlets(
        meshlets,
        meshlet_vertices,
        meshlet_triangles,
        indices,
        index_count,
        vertex_positions,
        vertex_count,
        vertex_positions_stride,
        max_vertices,
        max_triangles,
        c_float(cone_weight),
    )

    return meshlet_count, meshlets, meshlet_vertices, meshlet_triangles


def buildMeshletsBound_safe(
    index_count: int, max_vertices: int, max_triangles: int
) -> int:
    """Safe version of buildMeshletsBound()."""

    # pylint: disable=line-too-long
    assert (
        index_count >= 0 and index_count % 3 == 0
    ), f'index_count >= 0 and index_count % 3 (index_count: {index_count})'
    assert (
        max_vertices >= 3 and max_vertices <= kMeshletMaxVertices
    ), f'max_vertices >= 3 and max_vertices <= {kMeshletMaxVertices} (max_vertices: {max_vertices})'
    assert (
        max_triangles >= 1 and max_triangles <= kMeshletMaxTriangles
    ), f'max_triangles >= 1 and max_triangles <= {kMeshletMaxTriangles} (max_triangles: {max_triangles})'
    # pylint: enable=line-too-long

    # ensures the caller will compute output space properly as index data is 4b aligned
    assert (
        max_triangles % 4 == 0
    ), f'max_triangles % 4 == 0 (max_triangles: {max_triangles})'

    return buildMeshletsBound(index_count, max_vertices, max_triangles)


def buildMeshlets_safe(
    max_meshlets: int,
    indices: Array[c_uint],
    index_count: int,
    vertex_positions: Array[c_float],
    vertex_count: int,
    vertex_positions_stride: int,
    max_vertices: int,
    max_triangles: int,
    cone_weight: float,
) -> tuple[int, Array[Meshlet], Array[c_uint], Array[c_uint8]]:
    """Safe version of buildMeshlets()."""

    least_max_meshlets = buildMeshletsBound_safe(
        index_count, max_vertices, max_triangles
    )

    # pylint: disable=line-too-long
    assert (
        max_meshlets >= least_max_meshlets
    ), f'max_meshlets >= {least_max_meshlets} (max_meshlets: {max_meshlets})'
    assert (
        vertex_positions_stride >= 12 and vertex_positions_stride <= 256
    ), f'vertex_positions_stride >= 12 and vertex_positions_stride <= 256 (vertex_positions_stride: {vertex_positions_stride})'
    assert (
        vertex_positions_stride % sizeof(c_float) == 0
    ), f'vertex_positions_stride % {sizeof(c_float)} == 0 (vertex_positions_stride: {vertex_positions_stride})'
    # pylint: enable=line-too-long

    return buildMeshlets2(
        max_meshlets,
        indices,
        index_count,
        vertex_positions,
        vertex_count,
        vertex_positions_stride,
        max_vertices,
        max_triangles,
        cone_weight,
    )
