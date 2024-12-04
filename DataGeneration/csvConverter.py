import json
import csv

# Load the downloaded JSON data
with open('data.json', 'r') as f:
    data = json.load(f)

# Prepare data for CSV
hospital_data = []
for element in data['elements']:
    if element['type'] == 'node':  # Only process points (nodes)
        name = element.get('tags', {}).get('name', 'Unnamed Hospital')
        latitude = element['lat']
        longitude = element['lon']
        hospital_data.append([name, latitude, longitude])

# Write data to CSV file
with open('hospitals_bangalore.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Name', 'Latitude', 'Longitude'])  # Header row
    for hospital in hospital_data:
        if (hospital[0]!="Unnamed Hospital"):
            csvwriter.writerow(hospital) 

print("CSV file 'hospitals_bangalore.csv' created successfully.")
