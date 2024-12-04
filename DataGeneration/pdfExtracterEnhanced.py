import pdfplumber
import pandas as pd
import re
from fuzzywuzzy import fuzz, process

# Load hospital data with GPS coordinates from CSV
hospital_data = pd.read_csv('hospitals_bangalore.csv')

# Initialize an empty list to store the enriched hospital data
enriched_data = []

# Set a similarity threshold for fuzzy matching (e.g., 80)
similarity_threshold = 86

# Open the PDF file and extract text
pdf_path = "/home/mukund/data/clg/5thsem/HospitalAllocationSystem/Bengaluru PPN List of Hospitals.pdf"
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        # Extract table rows
        table = page.extract_table()
        
        # Skip header and process each row
        for row in table[1:]:  # Assuming the first row is the header
            # Extract hospital details from PDF row
            hospital_name = row[1]
            address = row[2]
            city = row[3]
            state = row[4]
            pin_code = row[5]
            
            # Clean up hospital name for better matching
            clean_name = re.sub(r'[^a-zA-Z0-9 ]', '', hospital_name).strip().lower()
            
            # Find the best match for the hospital name using fuzzy matching
            matches = process.extract(clean_name, hospital_data['Name'].str.lower(), scorer=fuzz.token_sort_ratio)
            best_match = matches[0] if matches else None
            
            # Check if the best match exceeds the similarity threshold
            if best_match and best_match[1] >= similarity_threshold:
                matched_hospital = hospital_data[hospital_data['Name'].str.lower() == best_match[0]]
                
                # If a match is found, get GPS coordinates
                latitude = matched_hospital.iloc[0]['Latitude']
                longitude = matched_hospital.iloc[0]['Longitude']
                
                # Add data to the enriched list
                enriched_data.append({
                    'Hospital Name': hospital_name,
                    'Address': address,
                    'City': city,
                    'State': state,
                    'Pin Code': pin_code,
                    'Latitude': latitude,
                    'Longitude': longitude
                })

# Convert enriched data to a DataFrame and save to CSV
enriched_df = pd.DataFrame(enriched_data)
enriched_df.to_csv('enriched_hospitals_data.csv', index=False)

print("Enriched data saved to 'enriched_hospitals_data.csv'.")
