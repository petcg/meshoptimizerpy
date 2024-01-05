"""meshoptimzer APIs: clusterizer

This module provides "raw" bindings to MESHOPTIMIZER_API and MESHOPTIMIZER_EXPERIMENTAL.
"""

from ctypes import c_float, c_uint, c_uint8, Array
from typing import Any

from ._dll import meshoptdll
from ._types import *
from ._verification import *


__all__ = [
    'buildMeshlets',
    'buildMeshletsScan',
    'buildMeshletsBound',
    'computeClusterBounds',
    'computeMeshletBounds',
]


def buildMeshlets(
    meshlets: Array[Meshlet],
    meshlet_vertices: Array[c_uint],
    meshlet_triangles: Array[c_uint8],
    indices: Array[c_uint],
    index_count: int,
    vertex_positions: Array[c_float] | Array[Array[c_float]] | Any,
    vertex_count: int,
    vertex_positions_stride: int,
    max_vertices: int,
    max_triangles: int,
    cone_weight: float,
) -> int:
    """Meshlet builder

    Splits the mesh into a set of meshlets where each meshlet has a micro index
    buffer indexing into meshlet vertices that refer to the original vertex buffer

    The resulting data can be used to render meshes using NVidia programmable
    mesh shading pipeline, or in other cluster-based renderers.
    When using buildMeshlets, vertex positions need to be provided to minimize
    the size of the resulting clusters.
    When using buildMeshletsScan, for maximum efficiency the index buffer being
    converted has to be optimized for vertex cache first.

    meshlets must contain enough space for all meshlets, worst case size can be computed with meshopt_buildMeshletsBound
    meshlet_vertices must contain enough space for all meshlets, worst case size is equal to max_meshlets * max_vertices
    meshlet_triangles must contain enough space for all meshlets, worst case size is equal to max_meshlets * max_triangles * 3
    vertex_positions should have float3 position in the first 12 bytes of each vertex
    max_vertices and max_triangles must not exceed implementation limits (max_vertices <= 255 - not 256!, max_triangles <= 512)
    cone_weight should be set to 0 when cone culling is not used, and a value between 0 and 1 otherwise to balance between cluster size and cone culling efficiency
    """

    verify_buildMeshlets_args(
        index_count,
        vertex_count,
        vertex_positions_stride,
        max_vertices,
        max_triangles,
    )

    meshlet_count: int = meshoptdll.meshopt_buildMeshlets(
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


def buildMeshletsScan(
    meshlets: Array[Meshlet],
    meshlet_vertices: Array[c_uint],
    meshlet_triangles: Array[c_uint8],
    indices: Array[c_uint],
    index_count: int,
    vertex_count: int,
    max_vertices: int,
    max_triangles: int,
) -> int:
    """For maximum efficiency the index buffer being converted has to be
    optimized for vertex cache first."""

    verify_buildMeshlets_args(
        index_count, vertex_count, 1, max_vertices, max_triangles
    )

    meshlet_count: int = meshoptdll.meshopt_buildMeshletsScan(
        meshlets,
        meshlet_vertices,
        meshlet_triangles,
        indices,
        index_count,
        vertex_count,
        max_vertices,
        max_triangles,
    )

    return meshlet_count


def buildMeshletsBound(
    index_count: int, max_vertices: int, max_triangles: int
) -> int:
    """Compute worst case size of space for all meshlets"""

    verify_buildMeshlets_args(index_count, 1, 1, max_vertices, max_triangles)

    result = meshoptdll.meshopt_buildMeshletsBound(
        index_count, max_vertices, max_triangles
    )

    return result


def computeClusterBounds(
    indices: Array[c_uint],
    index_count: int,
    vertex_positions: Array[c_float] | Array[Array[c_float]] | Any,
    vertex_count: int,
    vertex_positions_stride: int,
) -> Bounds:
    """Cluster bounds generator

    Creates bounding volumes that can be used for frustum, backface and occlusion
    culling.

    For backface culling with orthographic projection, use the following formula
    to reject backfacing clusters:
      dot(view, cone_axis) >= cone_cutoff

    For perspective projection, you can use the formula that needs cone apex in
    addition to axis & cutoff:
      dot(normalize(cone_apex - camera_position), cone_axis) >= cone_cutoff

    Alternatively, you can use the formula that doesn't need cone apex and uses
    bounding sphere instead:
      dot(normalize(center - camera_position), cone_axis) >= cone_cutoff + radius / length(center - camera_position)
    or an equivalent formula that doesn't have a singularity at center = camera_position:
      dot(center - camera_position, cone_axis) >= cone_cutoff * length(center - camera_position) + radius

    The formula that uses the apex is slightly more accurate but needs the apex;
    if you are already using bounding sphere to do frustum/occlusion culling,
    the formula that doesn't use the apex may be preferable (for derivation see
    Real-Time Rendering 4th Edition, section 19.3).

    vertex_positions should have float3 position in the first 12 bytes of each vertex
    index_count/3 should be less than or equal to 512 (the function assumes clusters of limited size)
    """

    result = meshoptdll.meshopt_computeClusterBounds(
        indices,
        index_count,
        vertex_positions,
        vertex_count,
        vertex_positions_stride,
    )
    return result


def computeMeshletBounds(
    meshlet_vertices: Array[c_uint],
    meshlet_triangles: Array[c_uint8],
    triangle_count: int,
    vertex_positions: Array[c_float] | Array[Array[c_float]] | Any,
    vertex_count: int,
    vertex_positions_stride: int,
) -> Bounds:
    """Cluster bounds generator"""

    result = meshoptdll.meshopt_computeClusterBounds(
        meshlet_vertices,
        meshlet_triangles,
        triangle_count,
        vertex_positions,
        vertex_count,
        vertex_positions_stride,
    )

    return result
