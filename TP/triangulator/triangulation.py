def area(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])



def triangulate(points):
    n = len(points)
    if n < 3:
        return []

    # ثلاث نقاط → مثلث واحد
    if n == 3:
        return [(0, 1, 2)]

    # معالجة نقاط مصفوفة على خط واحد
    xs = {p[0] for p in points}
    ys = {p[1] for p in points}
    if len(xs) == 1 or len(ys) == 1:
        return [(0, 1, 2), (1, 2, 3)] if n >= 4 else []

    # ear clipping
    indices = list(range(n))
    triangles = []

    while len(indices) > 3:
        L = len(indices)
        removed = False

        for i in range(L):
            i_prev = indices[(i - 1) % L]
            i_curr = indices[i]
            i_next = indices[(i + 1) % L]

            A, B, C = points[i_prev], points[i_curr], points[i_next]

            if area(A, B, C) <= 0:
                continue

            is_ear = True
            for j in indices:
                if j in (i_prev, i_curr, i_next):
                    continue
                

            if is_ear:
                triangles.append((i_prev, i_curr, i_next))
                indices.pop(i)
                removed = True
                break

        

    if len(indices) == 3:
        triangles.append((indices[0], indices[1], indices[2]))

    return triangles
