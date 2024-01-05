"""Verification functions for meshoptimzer APIs"""


__all__ = ['verify_buildMeshlets_args']


def verify_buildMeshlets_args(
    index_count: int,
    vertex_count: int,
    vertex_positions_stride: int,
    max_vertices: int,
    max_triangles: int,
):
    """Verify arguments for meshlet builder

    Note that this verification is tentative and not complete.

    Raises:
        ValueError: Arguments
    """

    if vertex_positions_stride <= 0:
        raise ValueError(
            f'index_count needs to be greater than zero. (index_count == {index_count})'
        )

    if vertex_count <= 0:
        raise ValueError(
            f'vertex_count needs to be greater than zero. (vertex_count == {vertex_count})'
        )

    if vertex_positions_stride <= 0:
        raise ValueError(
            f'vertex_positions_stride needs to be greater than zero. (vertex_positions_stride == {vertex_positions_stride})'
        )

    if max_vertices <= 0:
        raise ValueError(
            f'max_vertices needs to be greater than zero. (max_vertices == {max_vertices})'
        )

    if max_triangles <= 0:
        raise ValueError(
            f'max_triangles needs to be greater than zero. (max_triangles == {max_triangles})'
        )
