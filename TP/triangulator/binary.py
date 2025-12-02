import struct
from TP.pointset import PointSet

# Binary format (as specified in the project):
# - 4 bytes unsigned int (big-endian) = number of points (N)
# - then for each point: 4 bytes float X, 4 bytes float Y (big-endian)
# For Triangles:
# - first the PointSet blob as above
# - then 4 bytes unsigned int (big-endian) = number of triangles (M)
# - then for each triangle: 3 x 4 bytes unsigned int indices (big-endian)


def encode_pointset(pointset: PointSet) -> bytes:
    count = len(pointset)
    data = struct.pack(">I", count)
    for x, y in pointset.points:
        data += struct.pack(">f", float(x))
        data += struct.pack(">f", float(y))
    return data


def decode_pointset(buffer: bytes) -> PointSet:
    offset = 0
    if len(buffer) < 4:
        raise ValueError("buffer too short for pointset count")
    (count,) = struct.unpack_from(">I", buffer, offset)
    offset += 4
    points = []
    for _ in range(count):
        if offset + 8 > len(buffer):
            raise ValueError("buffer too short for points")
        x = struct.unpack_from(">f", buffer, offset)[0]
        y = struct.unpack_from(">f", buffer, offset + 4)[0]
        offset += 8
        points.append((x, y))
    return PointSet(points)


def encode_triangles(pointset: PointSet, triangles: list) -> bytes:
    data = encode_pointset(pointset)
    count = len(triangles)
    data += struct.pack(">I", count)
    for a, b, c in triangles:
        # each index stored as unsigned int
        data += struct.pack(">I", int(a))
        data += struct.pack(">I", int(b))
        data += struct.pack(">I", int(c))
    return data


def decode_triangles(buffer: bytes):
    """
    Returns tuple (PointSet, triangles_list)
    triangles_list is list of (a,b,c) indices
    """
    # decode pointset first
    offset = 0
    if len(buffer) < 4:
        raise ValueError("buffer too short")
    (count,) = struct.unpack_from(">I", buffer, offset)
    offset += 4
    points = []
    for _ in range(count):
        if offset + 8 > len(buffer):
            raise ValueError("buffer too short for points")
        x = struct.unpack_from(">f", buffer, offset)[0]
        y = struct.unpack_from(">f", buffer, offset + 4)[0]
        offset += 8
        points.append((x, y))
    pointset = PointSet(points)

    if offset + 4 > len(buffer):
        # no triangles section: return empty
        return pointset, []

    (tcount,) = struct.unpack_from(">I", buffer, offset)
    offset += 4
    triangles = []
    for _ in range(tcount):
        if offset + 12 > len(buffer):
            raise ValueError("buffer too short for triangles")
        a = struct.unpack_from(">I", buffer, offset)[0]
        b = struct.unpack_from(">I", buffer, offset + 4)[0]
        c = struct.unpack_from(">I", buffer, offset + 8)[0]
        offset += 12
        triangles.append((a, b, c))
    return pointset, triangles
