from XMapping import XDirection
from VValue import V_next
from Polygon import Polygon  # Updated import for Polygon
import math

class Directions:
    def __init__(self, x, y):
        self.xDirection = XDirection(x, y)

    def get_directions(self):
        return self.xDirection


class V_Values:
    def __init__(self, x, y, V):
        self.V_next = self.generate_V_values(x, y, V)

    def generate_V_values(self, x, y, V):
        v_next_obj = V_next(x, y, V)
        return v_next_obj.get_V_next()

    def get_V_next_values(self):
        return self.V_next


class GenerateNextPoint:
    def __init__(self, x, y, polygon, V):
        self.x = x
        self.y = y
        self.V = V
        self.vertices = polygon.get_vertices()  # Polygon has 8 vertices

        self.xDirection = Directions(self.x, self.y).get_directions()

        self.intersectionPoint = self.find_intersections()
        self.farPoint = self.find_longest_distance_point()

        self.P2 = self.find_P2()
        self.V_next = V_Values(x, y, V).get_V_next_values()

    def find_intersections(self):
        radian_angle = math.radians(self.xDirection.get_direction()[1])
        dx1, dy1 = math.cos(radian_angle), math.sin(radian_angle)
        dx2, dy2 = -dx1, -dy1

        edges = [(self.vertices[i], self.vertices[(i + 1) % len(self.vertices)]) for i in range(len(self.vertices))]
        intersections = []

        for dx, dy in [(dx1, dy1), (dx2, dy2)]:
            for edge_start, edge_end in edges:
                x2, y2 = edge_start
                x3, y3 = edge_end

                denominator = (self.x - (self.x + dx)) * (y2 - y3) - (self.y - (self.y + dy)) * (x2 - x3)
                if denominator == 0:
                    continue

                t1 = ((self.x - x2) * (y2 - y3) - (self.y - y2) * (x2 - x3)) / denominator
                t2 = ((self.x - x2) * (self.y - (self.y + dy)) - (self.y - y2) * (self.x - (self.x + dx))) / denominator

                if 0 <= t1 and 0 <= t2 <= 1:
                    intersection_x = self.x + t1 * dx
                    intersection_y = self.y + t1 * dy
                    intersections.append((round(intersection_x, 8), round(intersection_y, 8)))
                    break

        return intersections if len(intersections) == 2 else None

    def find_longest_distance_point(self):
        if not self.intersectionPoint:
            return None

        p1, p2 = self.intersectionPoint
        d1 = math.sqrt((self.x - p1[0]) ** 2 + (self.y - p1[1]) ** 2)
        d2 = math.sqrt((self.x - p2[0]) ** 2 + (self.y - p2[1]) ** 2)

        return p1 if d1 > d2 else p2


    def find_P2(self):
        if not self.farPoint:
            return None

        x1, y1 = self.x, self.y
        x2, y2 = self.farPoint

        P2_x = round(x1 + self.V * (x2 - x1), 8)
        P2_y = round(y1 + self.V * (y2 - y1), 8)

        return (P2_x, P2_y)


    def get_next_point_and_V_next(self):
        return self.P2, self.V_next


# Example usage
if __name__ == "__main__":
    polygon = Polygon(degree=4)
    P1 = (2.5, 1.5)
    V1 = 0.3

    point_generator = GenerateNextPoint(P1[0], P1[1], polygon, V1)

    print(f"Direction angle: {point_generator.xDirection.get_direction()[1]} degrees")
    print(f"Intersection points: {point_generator.intersectionPoint}")
    print(f"Farthest intersection point: {point_generator.farPoint}")
    print(f"Next point (P2): {point_generator.get_next_point_and_V_next()}")