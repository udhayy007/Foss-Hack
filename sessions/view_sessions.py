# import sqlite3

# def view_sessions():
#     # Connect to the SQLite database
#     conn = sqlite3.connect("session_data.db")
#     cursor = conn.cursor()

#     # Query to get all session data
#     cursor.execute("SELECT * FROM sessions")
#     sessions = cursor.fetchall()

#     # Print session data
#     if sessions:
#         print("Session Data:")
#         for session in sessions:
#             print(f"Session ID: {session[0]}, Timestamp: {session[1]}")
#     else:
#         print("No session data available.")

#     # Close the database connection
#     conn.close()

# if __name__ == "__main__":
#     view_sessions()

import sqlite3

def view_sessions():
    conn = sqlite3.connect("session_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions")
    sessions = cursor.fetchall()
    conn.close()

    if sessions:
        for session in sessions:
            print(f"Session ID: {session[0]}, Timestamp: {session[1]}, "
                  f"Latitude: {session[2]}, Longitude: {session[3]}, "
                  f"City: {session[4]}, State: {session[5]}, Pincode: {session[6]}")
    else:
        print("No session data available.")

if __name__ == "__main__":
    view_sessions()
