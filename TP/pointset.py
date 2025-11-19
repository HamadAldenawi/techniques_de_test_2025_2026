class PointSet:
    """
    Simple container for a list of 2D points.
    points = [(x1, y1), (x2, y2), ...]
    """

    def __init__(self, points):
        if not isinstance(points, list):
            raise TypeError("points must be a list")

        for p in points:
            if (
                not isinstance(p, tuple)
                or len(p) != 2
                or not isinstance(p[0], (int, float))
                or not isinstance(p[1], (int, float))
            ):
                raise ValueError("each point must be a tuple (x, y)")

        self.points = points

    def __len__(self):
        return len(self.points)

    def __getitem__(self, idx):
        return self.points[idx]

    # Convenience / serialization helpers
    def to_list(self):
        return list(self.points)

    @classmethod
    def from_list(cls, lst):
        return cls(lst)

    def as_dict(self):
        return {"points": self.to_list()}

    @classmethod
    def from_dict(cls, d):
        if "points" not in d:
            raise KeyError("missing 'points' field")
        return cls.from_list(d["points"])

    def __repr__(self):
        return f"PointSet({self.points})"
