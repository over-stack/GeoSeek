import random
import math


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

    return distance
