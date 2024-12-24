import psycopg2
import csv

# PostgreSQL database connection details
host = 'localhost'         # PostgreSQL server address
database = 'medimap' # Replace with your database name
user = 'postgres'         # Replace with your PostgreSQL username
password = '123456789' # Replace with your PostgreSQL password

# Connect to the PostgreSQL server
conn = psycopg2.connect(host=host, database=database, user=user, password=password)
cursor = conn.cursor()



# Function to insert CSV data into the table
def insert_data_from_csv_for_hospital(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Insert data into the table
            cursor.execute('''
                INSERT INTO api_hospital (hospital_name, addr, city, state_name, pincode, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (row['Hospital Name'], row['Address'], row['City'], row['State'], row['Pin Code'], row['Latitude'], row['Longitude']))
        conn.commit()




# Path to your CSV file
csv_file_path = 'DataGeneration/enriched_hospitals_data.csv'  # Update with the correct path to your CSV file


#insert_data_from_csv_for_hospital(csv_file_path)




# Close the database connection
cursor.close()
conn.close()
