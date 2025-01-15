import sqlite3
import uuid
from datetime import datetime
import geocoder
from geopy.geocoders import Nominatim
import logging
import requests
import pytz

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Fallback location (can be replaced with a default location of your choice)
FALLBACK_LOCATION = {
    'latitude': 0.0,
    'longitude': 0.0,
    'city': 'Unknown',
    'state': 'Unknown',
    'pincode': 'Unknown'
}

def get_current_time():
    """
    Get the current time in UTC to ensure consistency across deployments
    """
    return datetime.utcnow()

def get_location_with_fallback():
    """
    Attempt to get location with multiple fallback strategies
    """
    # Strategy 1: Use ipinfo.io (more reliable for cloud deployments)
    try:
        response = requests.get('https://ipinfo.io/json', timeout=5)
        data = response.json()
        loc = data.get('loc', '').split(',')
        city = data.get('city', 'Unknown')
        region = data.get('region', 'Unknown')
        
        if len(loc) == 2:
            return float(loc[0]), float(loc[1]), city, region
    except Exception as e:
        logger.warning(f"IPInfo location retrieval failed: {e}")

    # Strategy 2: Use geocoder
    try:
        g = geocoder.ip('me')
        if g.latlng:
            latitude, longitude = g.latlng
            return latitude, longitude, 'Unknown', 'Unknown'
    except Exception as e:
        logger.warning(f"Geocoder IP location failed: {e}")

    # Strategy 3: Return fallback location
    logger.error("All location retrieval methods failed. Using fallback location.")
    return (FALLBACK_LOCATION['latitude'], 
            FALLBACK_LOCATION['longitude'], 
            FALLBACK_LOCATION['city'], 
            FALLBACK_LOCATION['state'])

def get_location_details(latitude, longitude):
    """
    Attempt to get location details with multiple fallback strategies
    """
    city = state = pincode = "Unknown"

    # Strategy 1: Use Nominatim
    try:
        geolocator = Nominatim(user_agent="resume_analyzer")
        location = geolocator.reverse(f"{latitude},{longitude}", language="en", timeout=5)
        
        if location:
            address_details = location.raw.get("address", {})
            city = address_details.get("city", address_details.get("town", address_details.get("village", city)))
            state = address_details.get("state", state)
            pincode = address_details.get("postcode", pincode)
    except Exception as geo_error:
        logger.warning(f"Geocoding failed: {geo_error}")

    return city, state, pincode

# Initialize the database
def init_db():
    conn = sqlite3.connect("session_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            latitude REAL,
            longitude REAL,
            city TEXT,
            state TEXT,
            pincode TEXT       
        )
    ''')
    conn.commit()
    conn.close()

# Generate a new session ID and save it to the database
def create_and_save_session():
    session_id = str(uuid.uuid4())
    
    # Use UTC time
    timestamp = get_current_time()

    # Get location with fallback
    latitude, longitude, fallback_city, fallback_state = get_location_with_fallback()
    
    # Get location details with fallback
    city, state, pincode = get_location_details(latitude, longitude)
    
    # Use fallback city and state if retrieved details are unknown
    if city == "Unknown":
        city = fallback_city
    if state == "Unknown":
        state = fallback_state

    # Save the session data to the database
    try:
        conn = sqlite3.connect("session_data.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sessions (session_id, timestamp, latitude, longitude, city, state, pincode)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, timestamp, latitude, longitude, city, state, pincode))
        conn.commit()
    except sqlite3.Error as db_error:
        logger.error(f"Database error: {db_error}")
    finally:
        if 'conn' in locals():
            conn.close()

    return session_id, latitude, longitude, city, state, pincode
