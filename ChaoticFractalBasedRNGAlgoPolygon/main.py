import turtle
from Polygon import Polygon, PointChecker
from GenerateNextPoint import GenerateNextPoint

# Initialize screen
def draw_polygon(vertices):
    """Draw the polygon using Turtle."""
    turtle.penup()
    turtle.goto(vertices[0])
    turtle.pendown()

    for vertex in vertices[1:] + [vertices[0]]:  # Loop back to the first vertex
        turtle.goto(vertex)


def mark_point(point, label, color="red"):
    """Mark a point on the Turtle canvas and label it."""
    turtle.penup()
    turtle.goto(point)
    turtle.dot(5, color)
    turtle.goto(point[0] + 5, point[1] + 5)  # Offset text
    turtle.write(label, font=("Arial", 10, "bold"))


class PointInput:
    """Class to handle user input for point P."""

    def __init__(self, polygon):
        self.vertices = polygon.get_vertices()
        self.polygon = polygon

    def get_P_point(self):
        while True:
            try:
                print("\nVertices of the polygon:")
                for i in range(len(vertices)):
                    print(chr(65+i)+":",vertices[i])

                x = float(input("Enter x-coordinate for P: "))
                y = float(input("Enter y-coordinate for P: "))

                checker = PointChecker(self.vertices, (x, y))

                if checker.is_point_inside():
                    print(f"\nPoint P ({x:.3f}, {y:.3f}) accepted.")
                    return (x, y)
                else:
                    print("\nPoint P is not strictly inside the polygon. Please try again.")
            except ValueError:
                print("\nInvalid input. Please enter numeric values.")

class ValueInput:
    """Class to handle user input for value V."""

    def __init__(self, lower_limit=0.1, higher_limit=0.9):
        self.lower_limit = lower_limit
        self.higher_limit = higher_limit

    def get_V_value(self):
        while True:
            try:
                V = float(input(f"Enter value V (between {self.lower_limit} and {self.higher_limit}): "))
                if self.lower_limit <= V <= self.higher_limit:
                    print(f"\nValue V ({V:.1f}) accepted.")
                    return round(V, 8)
                else:
                    print(f"\nValue V must be between {self.lower_limit} and {self.higher_limit}. Please try again.")
            except ValueError:
                print("\nInvalid input. Please enter numeric values.")


class UserInput(PointInput, ValueInput):
    """Single point of operation for user input."""

    def __init__(self, polygon):
        PointInput.__init__(self, polygon)
        ValueInput.__init__(self)


if __name__ == "__main__":
    # Create polygon instance
    polygon = Polygon(degree=7)
    vertices= polygon.get_vertices()

    # Get user input
    user_input = UserInput(polygon)
    P = user_input.get_P_point()
    V = user_input.get_V_value()

    # Print final values
    print("Final Values:")
    for i in range(len(vertices)):
        print("\n"+chr(65+i)+":",vertices[i])
    print(f"\nP: {P}\nV: {V}")

    # Turtle visualization
    turtle.speed(0)
    scale_factor = 5
    # A = (A[0] * scale_factor, A[1] * scale_factor)
    scaled_vertices=[]
    for vertice in vertices:
        scaled_vertices.append((vertice[0]*scale_factor,vertice[1]*scale_factor))
    draw_polygon(scaled_vertices)

    P = (P[0] * scale_factor, P[1] * scale_factor)
    mark_point(P, "P", color="blue")
    
    # Set number of points
    number_of_points=500
    
    for i in range(number_of_points):
        print(f"\nIteration {i + 1}:")

        generate_next_point = GenerateNextPoint(P[0] / scale_factor, P[1] / scale_factor, polygon, V)
        next_point, V_next = generate_next_point.get_next_point_and_V_next()

        print(f"P {i + 1}: {next_point}")
        print(f"V next : {V_next}")

        x_int = next_point[0] * 10000
        y_int = next_point[1] * 10000
        sum_int = int(x_int * y_int)
        binary_representation = bin(sum_int)[2:]  # Remove the '0b' prefix

        # sum_bin_32 = f"{sum_int:032b}"[:32] # Ensures the binary string is exactly 32 bits

        print(f"Single value generated using x and y coordinate of P{i + 1}", sum_int)
        print("Binary representation: ", binary_representation)

        next_point = (next_point[0] * scale_factor, next_point[1] * scale_factor)
        mark_point(next_point, "")
        P = next_point
        V = V_next

    turtle.done()