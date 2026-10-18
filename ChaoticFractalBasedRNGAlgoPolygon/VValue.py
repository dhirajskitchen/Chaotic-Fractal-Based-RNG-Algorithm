import math


class Generate_V:
    """Base class to generate V values."""

    def __init__(self, x, y, V):
        """Initialize with x, y, and V values."""
        self.x = round(x, 8)
        self.y = round(y, 8)
        self.V = round(V, 8)
        self.V_x = None
        self.V_y = None
        self.V_next = None

    def Generate_V_next(self):
        """Placeholder method for generating V_next (to be implemented in subclass)."""
        pass

    def get_V_next(self):
        """Return the computed V_next value."""
        return self.V_next


class V_next(Generate_V):
    """Class to compute V_next value."""

    def __init__(self, x, y, V):
        """Initialize and compute V_x, V_y, and V_next."""
        super().__init__(x, y, V)
        self.V_next = self.Generate_V_next()

    def Generate_V_next(self):
        """Calculate V_next as a fraction number between 0.1 and 0.999 using a mathematical
formula."""
        scaled_x = self.x * 3.1415  # Introduce variation using pi multiplier
        scaled_y = self.y * 2.7182  # Introduce variation using e multiplier
        mod_component = (math.sin(scaled_x) + math.cos(scaled_y) + self.V) % 1  # Modulo for fraction
        V_next = 0.1 + (0.899 * abs(mod_component))  # Ensure within range [0.1, 0.999]
        return round(V_next, 8)

# Example usage
if __name__ == "__main__":
    x = 2.5
    y = 1.5
    V = 0.3

    v_next_obj = V_next(x, y, V)
    print(f"Computed V_next: {v_next_obj.get_V_next()}")