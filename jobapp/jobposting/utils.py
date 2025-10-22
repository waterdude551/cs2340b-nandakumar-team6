from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def geocode_location(location):
    """
    Geocode a location string to latitude and longitude.
    Returns (latitude, longitude) tuple or (None, None) if geocoding fails.
    """
    if not location:
        return None, None
    
    try:
        geolocator = Nominatim(user_agent="jobapp")
        location_data = geolocator.geocode(location, timeout=10)
        
        if location_data:
            return location_data.latitude, location_data.longitude
        return None, None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None, None