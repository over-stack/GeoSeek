import random
import math
from shapely.geometry import LineString


def generate_random_point(lat, lon, radius):
    # Convert radius from meters to degrees
    radius_in_degrees = radius / 111320

    # Generate two random numbers
    u = random.random()
    v = random.random()

    # Calculate random point within the radius
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    delta_lat = w * math.cos(t)
    delta_lon = w * math.sin(t) / math.cos(math.radians(lat))

    # Calculate new latitude and longitude
    new_lat = lat + delta_lat
    new_lon = lon + delta_lon

    return new_lat, new_lon


def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Compute differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c

    return distance * 1000


def kalman_filter(
    lat: list[float],
    lon: list[float],
) -> tuple[list[float], list[float]]:
    return lat, lon


def optimize_path(
    lat: list[float], lon: list[float], epsilon: float = 0.0001
) -> tuple[list[float], list[float]]:
    """Optimize the path using the Ramer-Douglas-Peucker algorithm from shapely."""
    line = LineString(zip(lat, lon))
    simplified_line = line.simplify(epsilon, preserve_topology=False)

    optimized_lat, optimized_lon = zip(*simplified_line.coords)
    return list(optimized_lat), list(optimized_lon)


def split_lat_lon(coordinates: list[str]) -> tuple[list[float], list[float]]:
    """Splits a list of 'lat:lon' strings into separate latitude and longitude lists."""
    lat, lon = zip(*(map(float, coord.split(":")) for coord in coordinates))
    return list(lat), list(lon)


def calc_path_distance(lat: list[float], lon: list[float]) -> float:
    """Calculate the total distance of a path."""
    distance = 0
    for i in range(1, len(lat)):
        distance += haversine_distance(lat[i - 1], lon[i - 1], lat[i], lon[i])
    return distance
