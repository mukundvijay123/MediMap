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



