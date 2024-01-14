"""Type information for shared types like struct and enum.

Notes:
- Python types are used rather than C types whenever possible, e.g. c_size_t -> int.
- C types are used for element's type in Array since it affects data's layout and size.
"""

from ctypes import c_float, c_int8, c_void_p, Array, Structure

class Stream(Structure):
    data: c_void_p
    size: int
    stride: int

class EncodeExp:
    Separate: int
    SharedVector: int
    SharedComponent: int

class Simplify:
    LockBorder: int

class VertexCacheStatistics(Structure):
    vertices_transformed: int
    warps_executed: int
    acmr: float
    atvr: float

class OverdrawStatistics(Structure):
    pixels_covered: int
    pixels_shaded: int
    overdraw: float

class VertexFetchStatistics(Structure):
    bytes_fetched: int
    overfetch: float

class Meshlet(Structure):
    vertex_offset: int
    triangle_offset: int
    vertex_count: int
    triangle_count: int

class Bounds(Structure):
    center: Array[c_float]
    radius: float
    cone_apex: Array[c_float]
    cone_axis: Array[c_float]
    cone_cutoff: float
    cone_axis_s8: Array[c_int8]
    cone_cutoff_s8: int
