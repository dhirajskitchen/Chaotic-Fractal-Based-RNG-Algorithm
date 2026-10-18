class BinaryRepresentation:
    """Class to convert (x, y) coordinates into a processed binary representation."""

    def __init__(self, x_coordinate, y_coordinate):
        """Initialize with x and y coordinates and compute a transformed binary value."""
        self.x_coordinate = round(x_coordinate, 8)
        self.y_coordinate = round(y_coordinate, 8)
        self.binary_value = self._convert_to_binary()

    def _convert_to_binary(self):
        """Convert x and y coordinates into an 8-bit binary representation using bitwise
        operations."""
        x_scaled = int(self.x_coordinate * 1000)
        y_scaled = int(self.y_coordinate * 1000)

        bitwise_xor = x_scaled ^ y_scaled  # Introduce randomness
        shifted_value = ((bitwise_xor << 3) & 0xFFFF) ^ (bitwise_xor >> 2)  # Shift and mask

        return bin(shifted_value)[2:].zfill(8)[-8:]


    def get_binary_value(self):
        """Return the computed binary representation."""
        return self.binary_value


class XDirection(BinaryRepresentation):
    """Class to determine movement degree based on transformed binary representation."""

    def __init__(self, x_coordinate, y_coordinate):
        """Initialize with x and y coordinates, compute binary representation, and determine
movement degree."""
        super().__init__(x_coordinate, y_coordinate)
        self.degree = self._determine_direction()

    def _determine_direction(self):
        """Determine the movement degree based on transformed value."""
        x_scaled = int(self.x_coordinate * 1000)
        y_scaled = int(self.y_coordinate * 1000)

        bitwise_xor = x_scaled ^ y_scaled
        shifted_value = ((bitwise_xor << 3) & 0xFFFF) ^ (bitwise_xor >> 2)
        degree = shifted_value % 360  # Normalize within 0°–360°

        return "null", degree

    def get_direction(self):
        """Return the determined degree."""
        return self.degree

    # Example usage


if __name__ == "__main__":
    test_cases = [(2.5, 2.349), (1.795, 1.644), (2.414, 2.263), (1.735, 1.584)]

    for x, y in test_cases:
        direction_obj = XDirection(x, y)
        print(f"Binary representation of ({x}, {y}): {direction_obj.get_binary_value()}")
        print(f"Move in the direction: {direction_obj.get_direction()}°\n")