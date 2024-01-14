"""meshoptimzer APIs: clusterizer

This module provides "raw" bindings to MESHOPTIMIZER_API and MESHOPTIMIZER_EXPERIMENTAL.
"""

from ctypes import c_float, c_uint, c_uint8, c_size_t
from ctypes import POINTER

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

# Common pointer types

c_float_p = POINTER(c_float)
c_uint_p = POINTER(c_uint)
c_uint8_p = POINTER(c_uint8)
Meshlet_p = POINTER(Meshlet)

# Foreign functions and public APIs

buildMeshlets = meshoptdll.meshopt_buildMeshlets
buildMeshlets.restype = c_size_t
buildMeshlets.argtypes = (
    Meshlet_p,  # meshlets
    c_uint_p,  # meshlet_vertices
    c_uint8_p,  # meshlet_triangles
    c_uint_p,  # indices
    c_size_t,  # index_count
    c_float_p,  # vertex_positions
    c_size_t,  # vertex_count
    c_size_t,  # vertex_positions_stride
    c_size_t,  # max_vertices
    c_size_t,  # max_triangles
    c_float,  # cone_weight
)

buildMeshletsScan = meshoptdll.meshopt_buildMeshletsScan
buildMeshletsScan.restype = c_size_t
buildMeshletsScan.argtypes = (
    Meshlet_p,  # meshlets
    c_uint_p,  # meshlet_vertices
    c_uint8_p,  # meshlet_triangles
    c_uint_p,  # indices
    c_size_t,  # index_count
    c_size_t,  # vertex_count
    c_size_t,  # max_vertices
    c_size_t,  # max_triangles
)

buildMeshletsBound = meshoptdll.meshopt_buildMeshletsBound
buildMeshletsBound.restype = c_size_t
buildMeshletsBound.argtypes = (
    c_size_t,  # index_count
    c_size_t,  # max_vertices
    c_size_t,  # max_triangles
)

computeClusterBounds = meshoptdll.meshopt_computeClusterBounds
computeClusterBounds.restype = Bounds
computeClusterBounds.argtypes = (
    c_uint_p,  # indices
    c_size_t,  # index_count
    c_float_p,  # vertex_positions
    c_size_t,  # vertex_count
    c_size_t,  # vertex_positions_stride
)

computeMeshletBounds = meshoptdll.meshopt_computeMeshletBounds
computeMeshletBounds.restype = Bounds
computeMeshletBounds.argtypes = (
    c_uint_p,  # meshlet_vertices
    c_uint8_p,  # meshlet_triangles
    c_size_t,  # triangle_count
    c_float_p,  # vertex_positions
    c_size_t,  # vertex_count
    c_size_t,  # vertex_positions_stride
)
