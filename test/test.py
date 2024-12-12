import psycopg2
import utils

#this file is to test all the functions


# Database connection details(put your db credetials here
db_config = {
    "dbname": "hospital_resource",
    "user": "postgres",
    "password": "your_password",  # Replace with your actual password
    "host": "localhost",
    "port": "5432"
}

def main():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_config)
        print("Database connection established.")

        # Sample data for hospital and resource
        hospital_data = {
            'hospital_name': 'City Hospital',
            'addr': '123 Main St',
            'city': 'New York',
            'state_name': 'NY',
            'pincode': 10001,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'contact': '1234567890',
        }

        # Call the function to add a hospital
        hospital_id = utils.add_hospital(conn, hospital_data)
        print(f"Added hospital with ID {hospital_id}")

        # Sample data for resource
        resource_data = {
            'hospital_id': hospital_id,
            'dept': 'Cardiology',
            'resource_type': 'ECG Machine',
            'quantity': 5,
            'occupied_quantity': 2
        }

        # Call the function to add a resource
        resource_id = utils.add_resource(conn, resource_data)
        print(f"Added resource with ID {resource_id}")

        # Now, delete the resource
        utils.delete_resource(conn, resource_id)
        print(f"Deleted resource with ID {resource_id}")

        # Finally, delete the hospital
        utils.delete_hospital(conn, hospital_id)
        print(f"Deleted hospital with ID {hospital_id}")

        accident_latitude = 12.890633 # Replace with actual accident latitude
        accident_longitude = 77.594889 # Replace with actual accident longitude
        distance = utils.haversine_distance(
            hospital_data['latitude'],
            hospital_data['longitude'],
            accident_lat,
            accident_lon
        )
        closest_hospital = utils.find_closest_hospital(conn, accident_latitude, accident_longitude)

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
