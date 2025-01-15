import sqlite3
import uuid
from datetime import datetime
import geocoder
from geopy.geocoders import Nominatim
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    timestamp = datetime.now()

    # Initialize default values
    latitude = None
    longitude = None
    city = "Unknown City"
    state = "Unknown State"
    pincode = "Unknown Pincode"

    try:
        # Get the user's location
        g = geocoder.ip('me')
        latlong = g.latlng

        if latlong:
            latitude, longitude = latlong
            
            try:
                # Use geopy to get the address with a timeout
                geolocator = Nominatim(user_agent="resume_analyzer")
                location = geolocator.reverse(latlong, language="en", timeout=5)
                
                if location:
                    address_details = location.raw.get("address", {})
                    city = address_details.get("city", address_details.get("town", address_details.get("village", "Unknown City")))
                    state = address_details.get("state", "Unknown State")
                    pincode = address_details.get("postcode", "Unknown Pincode")
            
            except Exception as geo_error:
                logger.warning(f"Geocoding failed: {geo_error}. Using default location details.")
    
    except Exception as location_error:
        logger.error(f"Could not retrieve location: {location_error}")

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
