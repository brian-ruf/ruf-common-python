#!/usr/bin/env python3
"""
Timezone Lookup Function

This module provides functionality to lookup IANA Time Zone Identifiers
based on city and country names.
"""

from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from typing import Optional
import time


def lookup_timezone(city: str, country: str, user_agent: str = "timezone_lookup") -> Optional[str]:
    """
    Lookup the IANA Time Zone Identifier for a given city and country.
    
    Args:
        city (str): The city name
        country (str): The country name
        user_agent (str): User agent string for the geocoding service
        
    Returns:
        Optional[str]: The IANA Time Zone Identifier (e.g., 'America/New_York') 
                      or None if not found
                      
    Example:
        >>> lookup_timezone("New York", "United States")
        'America/New_York'
        
        >>> lookup_timezone("London", "United Kingdom")
        'Europe/London'
        
        >>> lookup_timezone("Tokyo", "Japan")
        'Asia/Tokyo'
    """
    try:
        # Initialize geocoder with a user agent
        geolocator = Nominatim(user_agent=user_agent)
        
        # Create the search query
        query = f"{city}, {country}"
        
        # Get location coordinates
        location = geolocator.geocode(query, timeout=10)
        
        if location is None:
            print(f"Could not find coordinates for {query}")
            return None
            
        # Extract latitude and longitude
        latitude = location.latitude
        longitude = location.longitude
        
        print(f"Found coordinates for {query}: {latitude}, {longitude}")
        
        # Initialize timezone finder
        tf = TimezoneFinder()
        
        # Get timezone from coordinates
        timezone_name = tf.timezone_at(lat=latitude, lng=longitude)
        
        if timezone_name:
            print(f"Timezone for {query}: {timezone_name}")
            return timezone_name
        else:
            print(f"Could not determine timezone for coordinates {latitude}, {longitude}")
            return None
            
    except Exception as e:
        print(f"Error looking up timezone for {city}, {country}: {str(e)}")
        return None


def lookup_timezone_batch(locations: list, user_agent: str = "timezone_lookup_batch") -> dict:
    """
    Lookup timezones for multiple city/country pairs.
    
    Args:
        locations (list): List of tuples containing (city, country) pairs
        user_agent (str): User agent string for the geocoding service
        
    Returns:
        dict: Dictionary mapping location strings to timezone identifiers
        
    Example:
        >>> locations = [("New York", "United States"), ("London", "United Kingdom")]
        >>> lookup_timezone_batch(locations)
        {'New York, United States': 'America/New_York', 'London, United Kingdom': 'Europe/London'}
    """
    results = {}
    
    for city, country in locations:
        location_key = f"{city}, {country}"
        timezone = lookup_timezone(city, country, user_agent)
        results[location_key] = timezone
        
        # Add a small delay to be respectful to the geocoding service
        time.sleep(1)
    
    return results


def main():
    """
    Example usage and testing of the timezone lookup functions.
    """
    print("Testing timezone lookup function...")
    print("=" * 50)
    
    # Test cases
    test_locations = [
        ("New York", "United States"),
        ("London", "United Kingdom"),
        ("Tokyo", "Japan"),
        ("Sydney", "Australia"),
        ("Paris", "France"),
        ("Los Angeles", "United States"),
        ("Berlin", "Germany"),
        ("Mumbai", "India")
    ]
    
    print("Single lookups:")
    for city, country in test_locations:
        timezone = lookup_timezone(city, country)
        print(f"{city}, {country} -> {timezone}")
        time.sleep(1)  # Be respectful to the geocoding service
    
    print("\n" + "=" * 50)
    print("Batch lookup:")
    batch_results = lookup_timezone_batch(test_locations[:3])  # Test with first 3 locations
    for location, timezone in batch_results.items():
        print(f"{location} -> {timezone}")


if __name__ == "__main__":
    main()
