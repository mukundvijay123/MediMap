import psycopg2

# This has to be tested and matched to the db schema

'''
Function to add hospital
takes hospitaldictionary and database connection as parameteres
'''

def add_hospital(conn, hospital):
    try:
        cursor = conn.cursor()
        
        # Start a transaction block
        query = """
        INSERT INTO hospital_details (name, address, city, state, pin_code, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING ID
        """
        
        cursor.execute(query, (
            hospital['name'],
            hospital['address'],
            hospital['city'],
            hospital['state'],
            hospital['pin_code'],
            hospital['latitude'],
            hospital['longitude']
        ))

        hospital_id=cursor.fetchone()[0]
        # Commit the transaction only if everything is successful
        conn.commit()
        print("Hospital added successfully!")
        return hospital_id

    except Exception as e:
        # Rollback the transaction in case of error
        conn.rollback()
        print(f"Error: {e}")
    
    finally:
        cursor.close()


'''
Function to delete hospital
takes hospitaldictionary and database connection as parameteres
'''
def delete_hospital(conn, hospital):
    try:
        cursor = conn.cursor()

        # Extract the hospital ID from the dictionary
        hospital_id = hospital.get("id")
        if not hospital_id:
            raise ValueError("Hospital ID must be provided in the dictionary.")

        # Query to delete the hospital by ID
        query = "DELETE FROM hospital_details WHERE id = %s"
        cursor.execute(query, (hospital_id,))

        # Commit the transaction
        conn.commit()

        # Check if any row was deleted
        if cursor.rowcount > 0:
            print(f"Hospital with ID {hospital_id} deleted successfully!")
        else:
            print(f"No hospital found with ID {hospital_id}.")

    except Exception as e:
        # Rollback the transaction in case of error
        conn.rollback()
        print(f"Error: {e}")
    
    finally:
        cursor.close()




