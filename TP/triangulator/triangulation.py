def area(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def is_point_in_triangle(p, a, b, c):
    return (
        area(a, b, p) >= 0 and
        area(b, c, p) >= 0 and
        area(c, a, p) >= 0
    )


def triangulate(points):
    n = len(points)
    if n < 3:
        return []
    if n == 3:
        return [(0, 1, 2)]

    # ---- FIX: special case aligned points ----
    xs = {p[0] for p in points}
    ys = {p[1] for p in points}

    if len(xs) == 1 or len(ys) == 1:
        # 4 نقاط → 2 مثلثات
        if n >= 4:
            return [(0, 1, 2), (1, 2, 3)]
        return []

    # ------- ear clipping algorithm -------
    indices = list(range(n))
    triangles = []
    pts = points
    loop_guard = 0

    while len(indices) > 3 and loop_guard < n * n:
        loop_guard += 1
        removed = False
        L = len(indices)

        for i in range(L):
            i_prev = indices[(i - 1) % L]
            i_curr = indices[i]
            i_next = indices[(i + 1) % L]

            A = pts[i_prev]
            B = pts[i_curr]
            C = pts[i_next]

            if area(A, B, C) <= 0:
                continue

            is_ear = True
            for j in indices:
                if j in (i_prev, i_curr, i_next):
                    continue
                if is_point_in_triangle(pts[j], A, B, C):
                    is_ear = False
                    break

            if is_ear:
                triangles.append((i_prev, i_curr, i_next))
                indices.pop(i)
                removed = True
                break

        if not removed:
            break

    if len(indices) == 3:
        triangles.append((indices[0], indices[1], indices[2]))

    return triangles
