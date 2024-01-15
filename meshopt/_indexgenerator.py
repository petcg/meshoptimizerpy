"""meshoptimzer APIs: indexgenerator

This module provides "raw" bindings to MESHOPTIMIZER_API and MESHOPTIMIZER_EXPERIMENTAL.
"""

from ctypes import c_uint, c_size_t, c_void_p
from ctypes import POINTER

from ._dll import meshoptdll


__all__ = [
    'generateVertexRemap',
    'remapVertexBuffer',
    'remapIndexBuffer',
]

# Common pointer types

c_uint_p = POINTER(c_uint)

# Foreign functions and public APIs

generateVertexRemap = meshoptdll.meshopt_generateVertexRemap
generateVertexRemap.restype = c_size_t
generateVertexRemap.argtypes = (
    c_uint_p,  # destination
    c_uint_p,  # indices
    c_size_t,  # index_count
    c_void_p,  # vertices
    c_size_t,  # vertex_count
    c_size_t,  # vertex_size
)

remapVertexBuffer = meshoptdll.meshopt_remapVertexBuffer
remapVertexBuffer.restype = None
remapVertexBuffer.argtypes = (
    c_void_p,  # destination
    c_void_p,  # vertices
    c_size_t,  # vertex_count
    c_size_t,  # vertex_size
    c_uint_p,  # remap
)

remapIndexBuffer = meshoptdll.meshopt_remapIndexBuffer
remapIndexBuffer.restype = None
remapIndexBuffer.argtypes = (
    c_uint_p,  # destination
    c_uint_p,  # indices
    c_size_t,  # index_count
    c_uint_p,  # remap
)
