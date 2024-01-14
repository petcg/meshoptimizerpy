"""Type information for clusterizer.

Notes:
- Python types are used rather than C types whenever possible, e.g. c_size_t -> int.
- C types are used for element's type in Array since it affects data's layout and size.
- Docstrings for _FuncPtr are written here for now.
"""

from ctypes import c_float, c_uint, c_uint8, c_size_t
from ctypes import Array, _Pointer

from ._types import *

def buildMeshlets(
    meshlets: _Pointer[Meshlet] | Array[Meshlet],
    meshlet_vertices: _Pointer[c_uint] | Array[c_uint],
    meshlet_triangles: _Pointer[c_uint8] | Array[c_uint8],
    indices: _Pointer[c_uint] | Array[c_uint],
    index_count: int,
    vertex_positions: _Pointer[c_float]
    | Array[c_float]
    | Array[Array[c_float]],
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
    ...

def buildMeshletsScan(
    meshlets: _Pointer[Meshlet] | Array[Meshlet],
    meshlet_vertices: _Pointer[c_uint] | Array[c_uint],
    meshlet_triangles: _Pointer[c_uint8] | Array[c_uint8],
    indices: _Pointer[c_uint] | Array[c_uint],
    index_count: c_size_t | int,
    vertex_count: c_size_t | int,
    max_vertices: c_size_t | int,
    max_triangles: c_size_t | int,
) -> int:
    """For maximum efficiency the index buffer being converted has to be
    optimized for vertex cache first."""
    ...

def buildMeshletsBound(
    index_count: c_size_t | int,
    max_vertices: c_size_t | int,
    max_triangles: c_size_t | int,
) -> int:
    """Compute worst case size of space for all meshlets"""
    ...

def computeClusterBounds(
    indices: _Pointer[c_uint] | Array[c_uint],
    index_count: int,
    vertex_positions: _Pointer[c_float]
    | Array[c_float]
    | Array[Array[c_float]],
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
    ...

def computeMeshletBounds(
    meshlet_vertices: _Pointer[c_uint] | Array[c_uint],
    meshlet_triangles: _Pointer[c_uint8] | Array[c_uint8],
    triangle_count: int,
    vertex_positions: _Pointer[c_float]
    | Array[c_float]
    | Array[Array[c_float]],
    vertex_count: int,
    vertex_positions_stride: int,
) -> Bounds:
    """Cluster bounds generator"""
    ...
