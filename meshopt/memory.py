"""Utilities?"""

from ctypes import Array, c_uint, c_uint8
from ._types import *


__all__ = ('make_meshlets', 'make_meshlet_vertices', 'make_meshlet_triangles')


def make_meshlets(max_meshlets: int) -> Array[Meshlet]:
    """_summary_

    Args:
        max_meshlets (int): _description_

    Returns:
        Array[Meshlet]: _description_
    """

    MeshletArray = Meshlet * max_meshlets
    meshlets = MeshletArray()
    return meshlets


def make_meshlet_vertices(
    max_meshlets: int, max_vertices: int
) -> Array[c_uint]:
    """_summary_

    Args:
        max_meshlets (int): _description_
        max_vertices (int): _description_

    Returns:
        Array[c_uint]: _description_
    """

    MeshletVertexArray = c_uint * (max_meshlets * max_vertices)
    meshlet_vertices = MeshletVertexArray()
    return meshlet_vertices


def make_meshlet_triangles(
    max_meshlets: int, max_triangles: int
) -> Array[c_uint8]:
    """_summary_

    Args:
        max_meshlets (int): _description_
        max_triangles (int): _description_

    Returns:
        Array[c_uint8]: _description_
    """
    MeshletTriangleArray = c_uint8 * (3 * max_meshlets * max_triangles)
    meshlet_triangles = MeshletTriangleArray()
    return meshlet_triangles
