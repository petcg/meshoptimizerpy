"""meshoptimizer types."""

from ctypes import c_float, c_int8, c_uint, Structure


__all__ = ('Bounds', 'Meshlet')


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


class Meshlet(Structure):
    """struct meshopt_Meshlet"""

    _fields_ = (
        ('vertex_offset', c_uint),
        ('triangle_offset', c_uint),
        ('vertex_count', c_uint),
        ('triangle_count', c_uint),
    )
