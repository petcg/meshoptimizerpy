"""meshoptimizer types."""

from ctypes import c_float, c_int8, c_size_t, c_uint, c_void_p, Structure
from enum import IntEnum


__all__ = [
    'Stream',
    'EncodeExp',
    'Simplify',
    'VertexCacheStatistics',
    'OverdrawStatistics',
    'VertexFetchStatistics',
    'Meshlet',
    'Bounds',
]


class Stream(Structure):
    """struct meshopt_Stream"""

    _fields_ = (
        ('data', c_void_p),
        ('size', c_size_t),
        ('stride', c_size_t),
    )


class EncodeExp(IntEnum):
    """Encoding exponents options"""

    Separate = 0
    SharedVector = 1
    SharedComponent = 2


class Simplify(IntEnum):
    """Simplification options"""

    LockBorder = 1 << 0


class VertexCacheStatistics(Structure):
    """struct meshopt_VertexCacheStatistics"""

    _fields_ = (
        ('vertices_transformed', c_uint),
        ('warps_executed', c_uint),
        ('acmr', c_float),
        ('atvr', c_float),
    )


class OverdrawStatistics(Structure):
    """struct meshopt_OverdrawStatistics"""

    _fields_ = (
        ('pixels_covered', c_uint),
        ('pixels_shaded', c_uint),
        ('overdraw', c_float),
    )


class VertexFetchStatistics(Structure):
    """struct meshopt_VertexFetchStatistics"""

    _fields_ = (
        ('bytes_fetched', c_uint),
        ('overfetch', c_float),
    )


class Meshlet(Structure):
    """struct meshopt_Meshlet"""

    _fields_ = (
        ('vertex_offset', c_uint),
        ('triangle_offset', c_uint),
        ('vertex_count', c_uint),
        ('triangle_count', c_uint),
    )


class Bounds(Structure):
    """struct meshopt_Bounds"""

    _fields_ = (
        ('center', c_float * 3),
        ('radius', c_float),
        ('cone_apex', c_float * 3),
        ('cone_axis', c_float * 3),
        ('cone_cutoff', c_float),
        ('cone_axis_s8', c_int8 * 3),
        ('cone_cutoff_s8', c_int8),
    )
