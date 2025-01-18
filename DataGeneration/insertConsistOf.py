import psycopg2
from psycopg2 import sql
import random


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



resource_query = sql.SQL("""
            SELECT id FROM api_resource
        """)

hospital_query = sql.SQL("""
            SELECT id FROM api_hospital
        """)

insert_query=sql.SQL("""
            INSERT INTO api_consistsof(available,total_quantity,total_available_quantity,hospital_id,resource_id)
            VALUES (%s,%s,%s,%s,%s)
        """)


cursor.execute(resource_query)
resource_ids=cursor.fetchall()
cursor.execute(hospital_query)
hospital_ids=cursor.fetchall()

hospital_ids=[i[0] for i in hospital_ids]
resource_ids=[i[0] for i in resource_ids]

for hid in hospital_ids:
    for rid in resource_ids:
        qty=random.randint(0,50)
        cursor.execute(insert_query,(True,qty,qty,hid,rid))

connection.commit()
cursor.close()
connection.close()
print("Done!!")


