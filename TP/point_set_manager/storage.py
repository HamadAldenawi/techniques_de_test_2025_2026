from TP.pointset import PointSet

class Storage:
    def __init__(self):
        self.db = {}
        self.counter = 1

    def add_pointset(self, points):
        fixed = []
        for p in points:
            if not (isinstance(p, (list, tuple)) and len(p) == 2):
                raise ValueError("each point must be a list [x,y] or tuple (x,y)")
            fixed.append((float(p[0]), float(p[1])))

        ps = PointSet(fixed)
        pid = self.counter
        self.db[pid] = ps
        self.counter += 1

        return pid

    def get_pointset(self, pid):
        return self.db.get(pid)