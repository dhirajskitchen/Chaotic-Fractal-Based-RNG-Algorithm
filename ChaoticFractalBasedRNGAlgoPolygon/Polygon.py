import math
class Polygon:
    """Class to represent a polygon and calculate its vertices."""

    def __init__(self, edge_length=60.0,degree=4):
        """Initialize the polygon with a given edge length and calculate vertices."""
        self.edge_length = round(edge_length, 8)
        self.n=degree;
        self.vertices = self._calculate_vertices()

    def _calculate_vertices(self):
        """Calculate and return the eight vertices of the polygon."""

        # Step 1: Circumradius
        R = self.edge_length / (2 * math.sin(math.pi / self.n))

       # Step 2: Center coordinates (for one vertex at (0, 0) and next at (a, 0))
        x_c = self.edge_length / (2 * math.tan(math.pi / self.n))
        y_c = self.edge_length / 2

        # Step 3: Initial angle (from center to first vertex)
        theta0 = math.atan2(-y_c, -x_c)  # since first vertex is at (0,0)

        # Step 4: Generate n vertices by rotating 2*pie/n each time
        vertices = []
        for k in range(self.n):
            theta = theta0 + k * (2*math.pi / self.n)
            x = x_c + R * math.cos(theta)
            y = y_c + R * math.sin(theta)
            vertices.append((round(x, 8), round(y, 8)))

        return vertices
    
    def get_vertices(self):
        """Return the vertices of the polygon."""
        return tuple(self.vertices)


class PointChecker:
    """Class to check whether a given point lies inside a polygon."""

    def __init__(self, vertices, point):
        """Initialize with the polygon vertices and the point to check."""
        self.vertices = vertices
        self.point = point

    def is_point_inside(self):
        """Check if the point is inside the polygon using bounding conditions."""
        vertices=self.vertices
        n = len(vertices)
        inside = False
        x,y=self.point
        px, py = x, y
        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]

            # Check if the point is within the y-bounds of the edge
            if ((y1 > py) != (y2 > py)):
                # Compute x coordinate of intersection of polygon edge with ray
                x_intersect = (x2 - x1) * (py - y1) / (y2 - y1) + x1
                if px < x_intersect:
                    inside = not inside

        return inside

# Example usage
if __name__ == "__main__":
    soctagon = Polygon()
    vertices = Polygon.get_vertices()
    print("Vertices of the Polygon:", vertices)

    test_point = (3.0, 2.0)
    checker = PointChecker(vertices, test_point)
    print(f"Is point {test_point} inside the Polygon?", checker.is_point_inside())