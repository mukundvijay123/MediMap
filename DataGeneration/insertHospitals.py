import psycopg2
import csv
from psycopg2 import sql

HOST = 'localhost'  # Change to your database host if it's not localhost
DATABASE = 'medimap'  # Your database name
USER = 'postgres'  # Your PostgreSQL username
PASSWORD = '123456789'  # Your PostgreSQL password

# Connect to PostgreSQL
connection = psycopg2.connect(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASSWORD
)

cursor = connection.cursor()

csv_file_path="DataGeneration\enriched_hospitals_data.csv"

with open(csv_file_path, mode='r') as file:
    csv_reader=csv.DictReader(file)
    for row in csv_reader:
        hospital_name = row['Hospital Name']
        address = row['Address']
        city = row['City']
        state = row['State']
        pin_code = row['Pin Code']
        latitude = row['Latitude']
        longitude = row['Longitude']


        insert_query = sql.SQL("""
            INSERT INTO api_hospital (hospital_name, addr, city, state_name, pincode, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)
     
        cursor.execute(insert_query, (hospital_name, address, city, state, pin_code, latitude, longitude))


connection.commit()
cursor.close()
connection.close()
print("Done!!")
