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
departments = [
    "Cardiac", "Orthopedic", "Neurology", "General Medicine",
    "Pediatrics", "Dermatology", "Ophthalmology", "ENT", 
    "Gastroenterology", "Oncology", "Pulmonology", "Urology",
    "Psychiatry", "Endocrinology", "Gynecology", "Nephrology",
    "Infectious Diseases", "Traumatology", "Hematology", "Rheumatology"
]


insert_query = sql.SQL("""
            INSERT INTO api_resource (dept,resource_type)
            VALUES (%s, %s)
        """)
for dept in departments:
    cursor.execute(insert_query,(dept,"bed"))



connection.commit()
cursor.close()
connection.close()
print("Done!!")