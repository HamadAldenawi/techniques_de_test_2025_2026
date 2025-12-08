import struct
from TP.pointset import PointSet


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
    data += struct.pack(">I", len(triangles))

    for a, b, c in triangles:
        data += struct.pack(">III", int(a), int(b), int(c))

    return data


def decode_triangles(buffer: bytes):
    offset = 0

    

    # decode pointset
    (count,) = struct.unpack_from(">I", buffer, offset)
    offset += 4

    points = []
    for _ in range(count):
        x = struct.unpack_from(">f", buffer, offset)[0]
        y = struct.unpack_from(">f", buffer, offset + 4)[0]
        offset += 8
        points.append((x, y))

    pointset = PointSet(points)

    # COVERED NOW — هذا الفرع كان غير مغطى، الآن مغطى لأن tests تستدعيه
    if offset >= len(buffer):
        return pointset, []

    # decode triangles

    (tcount,) = struct.unpack_from(">I", buffer, offset)
    offset += 4

    triangles = []
    for _ in range(tcount):
        if offset + 12 > len(buffer):
            raise ValueError("buffer too short for triangles")

        a, b, c = struct.unpack_from(">III", buffer, offset)
        offset += 12
        triangles.append((a, b, c))

    return pointset, triangles
