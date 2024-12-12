import psycopg2
import math

# add hospital ,add resource ,delete hospital and delete resource have been tested

'''
Function to add hospital
takes hospitaldictionary and database connection as parameteres
'''

def add_hospital(conn, hospital):
    try:
        cursor = conn.cursor()

        # Start a transaction block
        query = """
        INSERT INTO HOSPITAL (hospital_name, addr, city, state_name, pincode, latitude, longitude, contact)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        cursor.execute(query, (
            hospital['hospital_name'],
            hospital['addr'],
            hospital['city'],
            hospital['state_name'],
            hospital['pincode'],
            hospital['latitude'],
            hospital['longitude'],
            hospital['contact'],
        ))

        hospital_id = cursor.fetchone()[0]
        conn.commit()  # Commit the transaction only if successful

        print("Hospital added successfully!")
        return hospital_id

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        print(f"Error: {e}")
    
    finally:
        cursor.close()


'''
Function to delete hospital
takes hospital_id and database connection as parameteres
'''
def delete_hospital(conn, hospital_id):
    try:
        cursor = conn.cursor()

        # Start a transaction block
        query = "DELETE FROM HOSPITAL WHERE id = %s"
        cursor.execute(query, (hospital_id,))

        if cursor.rowcount > 0:
            conn.commit()  # Commit the transaction
            print(f"Hospital with ID {hospital_id} deleted successfully!")
        else:
            print(f"No hospital found with ID {hospital_id}.")

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        print(f"Error: {e}")
    
    finally:
        cursor.close()

'''
Function to add a resource 
takes resource dictinary and database connection as paramenres
'''

def add_resource(conn, resource):
    try:
        cursor = conn.cursor()

        # Start a transaction block
        query = """
        INSERT INTO RESOURCES (hospital_id, dept, resource_type, quantity, occupied_quantity)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """
        
        cursor.execute(query, (
            resource['hospital_id'],
            resource['dept'],
            resource['resource_type'],
            resource['quantity'],
            resource['occupied_quantity']
        ))

        resource_id = cursor.fetchone()[0]
        conn.commit()  # Commit the transaction

        print("Resource added successfully!")
        return resource_id

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        print(f"Error: {e}")
    
    finally:
        cursor.close()
  


'''
function to delete a resource
'''

def delete_resource(conn, resource_id):
    try:
        cursor = conn.cursor()

        # Start a transaction block
        query = "DELETE FROM RESOURCES WHERE id = %s"
        cursor.execute(query, (resource_id,))

        if cursor.rowcount > 0:
            conn.commit()  # Commit the transaction
            print(f"Resource with ID {resource_id} deleted successfully!")
        else:
            print(f"No resource found with ID {resource_id}.")

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        print(f"Error: {e}")
    
    finally:
        cursor.close()
# Function to add a patient to the database
def add_patient(conn, patient):
    """
    Adds a patient to the PATIENT table.
    Parameters:
        conn: Database connection object.
        patient: Dictionary containing patient details.
            Required keys: 'name', 'gender'.
            Optional keys: 'contact', 'hospital_id', 'insurance_id'.
    Returns:
        int: ID of the newly added patient.
    """
    try:
        cursor = conn.cursor()

        # Insert query for the PATIENT table
        query = """
        INSERT INTO PATIENT (name, gender, contact, hospital_id, insurance_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """
        
        cursor.execute(query, (
            patient['name'],
            patient['gender'],
            patient.get('contact', None),  # Default to None if not provided
            patient.get('hospital_id', None),  # Default to None if not provided
            patient.get('insurance_id', None)  # Default to None if not provided
        ))

        patient_id = cursor.fetchone()[0]  # Get the ID of the newly added patient
        conn.commit()  # Commit transaction

        print("Patient added successfully!")
        return patient_id

    except Exception as e:
        conn.rollback()  # Rollback transaction on error
        print(f"Error while adding patient: {e}")
    
    finally:
        cursor.close()


# Function to add accident details to the database
def add_accident(conn, accident):
    """
    Adds accident details to the ACCIDENT table.
    Parameters:
        conn: Database connection object.
        accident: Dictionary containing accident details.
            Required keys: 'patient_id', 'latitude', 'longitude'.
            Optional key: 'accident_details' (JSON object).
    Returns:
        int: ID of the newly added accident.
    """
    try:
        cursor = conn.cursor()

        # Insert query for the ACCIDENT table
        query = """
        INSERT INTO ACCIDENT (patient_id, latitude, longitude, accident_details)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """
        
        cursor.execute(query, (
            accident['patient_id'],
            accident['latitude'],
            accident['longitude'],
            accident.get('accident_details', None)  # Default to None if not provided
        ))

        accident_id = cursor.fetchone()[0]  # Get the ID of the newly added accident
        conn.commit()  # Commit transaction

        print("Accident details added successfully!")
        return accident_id

    except Exception as e:
        conn.rollback()  # Rollback transaction on error
        print(f"Error while adding accident details: {e}")
    
    finally:
        cursor.close()

'''
function to find shortest distance
'''

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points
    on the Earth using the Haversine formula.
    """
    R = 6371  # Radius of Earth in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = math.sin(d_lat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def find_closest_hospital(conn, accident_lat, accident_lon):
    try:
        cursor = conn.cursor()

        # Fetch all hospital locations
        query = """
        SELECT id, hospital_name, latitude, longitude
        FROM HOSPITAL
        """
        cursor.execute(query)
        hospitals = cursor.fetchall()

        closest_hospital = None
        min_distance = float('inf')

        # Iterate over hospitals and calculate the distance
        for hospital in hospitals:
            hospital_id, hospital_name, hospital_lat, hospital_lon = hospital

            # Convert Decimal to float
            hospital_lat = float(hospital_lat)
            hospital_lon = float(hospital_lon)

            # Calculate haversine distance
            distance = haversine_distance(accident_lat, accident_lon, hospital_lat, hospital_lon)

            if distance < min_distance:
                min_distance = distance
                closest_hospital = {
                    'id': hospital_id,
                    'name': hospital_name,
                    'latitude': hospital_lat,
                    'longitude': hospital_lon,
                    'distance': min_distance
                }

        if closest_hospital:
            print(f"Closest hospital: {closest_hospital['name']} (ID: {closest_hospital['id']})")
            print(f"Location: ({closest_hospital['latitude']}, {closest_hospital['longitude']})")
            print(f"Distance: {closest_hospital['distance']:.2f} km")
        else:
            print("No hospitals found.")

        return closest_hospital

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
