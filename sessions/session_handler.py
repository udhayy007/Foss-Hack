import sqlite3
import uuid
from datetime import datetime
import geocoder
from geopy.geocoders import Nominatim

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

    # Get the user's location
    g = geocoder.ip('me')
    latlong = g.latlng

    # initialize default values
    latitude = None
    longitude = None
    city = "Unknown City"
    state = "Unknown State"
    pincode = "Unknown Pincode"

    if latlong:
        latitude, longitude = latlong
        # use geopy to get the address
        geolocator = Nominatim(user_agent="http")
        location = geolocator.reverse(latlong, language="en")
        
        if location:
            address_details = location.raw.get("address", {})
            city = address_details.get("city", address_details.get("town", address_details.get("village", "Unknown City")))
            state = address_details.get("state", "Unknown State")
            pincode = address_details.get("postcode", "Unknown Pincode")

    # Save the session data to the database
    conn = sqlite3.connect("session_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sessions (session_id, timestamp, latitude, longitude, city, state, pincode)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (session_id, timestamp, latitude, longitude, city, state, pincode))
    conn.commit()
    conn.close()

    return session_id, latitude, longitude, city, state, pincode
