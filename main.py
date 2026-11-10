from dataclasses import dataclass
import numpy as np
from typing import List, Tuple, Union


@dataclass(frozen=True)
class SpatialBounds:
    """Represents bounding box boundaries for spatial validation."""
    x_min: float
    x_max: float
    y_min: float
    y_max: float


class PolarToCartesianMapper:
    """Engine for batch converting polar coordinates (r, theta) to Cartesian (x, y)."""

    def __init__(self, degrees: bool = True) -> None:
        self.degrees = degrees

    def convert_batch(self, polar_data: Union[np.ndarray, List, Tuple]) -> np.ndarray:
        """Converts an (N, 2) array of polar points [r, theta] into an (N, 2) Cartesian array [x, y]."""
        data = np.asarray(polar_data, dtype=np.float64)

        if data.ndim != 2 or data.shape[1] != 2:
            raise ValueError(f"Expected input array of shape (N, 2), got {data.shape}")

        r = data[:, 0]
        theta = data[:, 1]

        if np.any(r < 0):
            raise ValueError("Radial distance 'r' must be non-negative.")

        theta_rad = np.radians(theta) if self.degrees else theta

        x = r * np.cos(theta_rad)
        y = r * np.sin(theta_rad)

        return np.column_stack((x, y))

    @staticmethod
    def validate_spatial_bounds(cartesian_points: np.ndarray, bounds: SpatialBounds) -> np.ndarray:
        """Filters Cartesian coordinates to find points falling within spatial boundaries."""
        x = cartesian_points[:, 0]
        y = cartesian_points[:, 1]

        in_x = (x >= bounds.x_min) & (x <= bounds.x_max)
        in_y = (y >= bounds.y_min) & (y <= bounds.y_max)

        return in_x & in_y


def get_terminal_inputs() -> List[List[float]]:
    """Collects polar coordinate pairs interactively from user terminal input."""
    coords: List[List[float]] = []
    print("--- Polar Coordinate Entry ---")
    print("Enter coordinates as 'radius, theta' (e.g., 10, 45). Type 'done' when finished.\n")

    while True:
        user_input = input("Enter (r, theta): ").strip()
        if user_input.lower() == "done":
            break
        if not user_input:
            continue

        try:
            parts = user_input.split(",")
            if len(parts) != 2:
                print(" Invalid input format. Please enter two comma-separated numbers (e.g. 10, 90).")
                continue

            r, theta = float(parts[0].strip()), float(parts[1].strip())
            if r < 0:
                print(" Radius 'r' cannot be negative. Try again.")
                continue

            coords.append([r, theta])
        except ValueError:
            print(" Invalid numeric values. Please enter valid numbers.")

    return coords


def main() -> None:
    # Collect coordinates interactively
    user_coords = get_terminal_inputs()

    if not user_coords:
        print("No valid coordinates entered. Exiting program.")
        return

    mapper = PolarToCartesianMapper(degrees=True)

    try:
        # Convert user inputs
        cartesian_coords = mapper.convert_batch(user_coords)

        print("\n--- Transformed Cartesian Coordinates ---")
        for polar, cart in zip(user_coords, cartesian_coords):
            print(f"Polar (r={polar[0]:>5.1f}, θ={polar[1]:>6.1f}°) -> Cartesian (x={cart[0]:>7.2f}, y={cart[1]:>7.2f})")

        # Boundary validation check
        bounds = SpatialBounds(x_min=-10.0, x_max=10.0, y_min=0.0, y_max=10.0)
        valid_mask = mapper.validate_spatial_bounds(cartesian_coords, bounds)

        print("\n--- Spatial Boundary Check ---")
        print(f"Bounds: X [{bounds.x_min}, {bounds.x_max}], Y [{bounds.y_min}, {bounds.y_max}]")
        print(f"Valid points count: {np.sum(valid_mask)} / {len(cartesian_coords)}")
        print("Valid Points Vector Array:\n", cartesian_coords[valid_mask])

    except ValueError as e:
        print(f"Transformation Error: {e}")


if __name__ == "__main__":
    main()