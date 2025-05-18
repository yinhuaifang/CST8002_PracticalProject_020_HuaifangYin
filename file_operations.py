"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project01
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [May 25  2025]
Author: [Huaifang Yin]
Description: This program reads and analyzes nitrogen oxide emissions data from Canadian facilities.
It loads data from a CSV file, creates FacilityRecord objects, and displays the information.
"""

import csv
from facility_record import FacilityRecord

def load_facility_data(filename, max_records=5):
    """
    Load facility data from a CSV file and return a list of FacilityRecord objects.
    
    Args:
        filename (str): Path to the CSV file
        max_records (int): Maximum number of records to load (default: 5)
        
    Returns:
        list: List of FacilityRecord objects
    """
    facilities = []
    
    encoding = 'ansi'
    try:
        with open(filename, mode='r', encoding=encoding) as file:
            reader = csv.DictReader(file)
            
            for i, row in enumerate(reader):
                if i >= max_records:
                    break
                    
                # Handle empty emission values
                emissions = float(row['Emissions']) if row['Emissions'] else 0.0
                
                facility = FacilityRecord(
                    npri_id=row['NPRI ID'],
                    facility_name=row['Facility name'],
                    company_name=row['Company name'],
                    address=row['Address'],
                    city=row['City'],
                    province=row['Province'],
                    postal_code=row['PostalCode'],
                    latitude=float(row['Latitude']) if row['Latitude'] else 0.0,
                    longitude=float(row['Longitude']) if row['Longitude'] else 0.0,
                    emissions=emissions,
                    units=row['Units'],
                    facility_details=row['Facility details'],
                    facility_information=row['Facility information'],
                    report_year=int(row['Report year'])
                )
                
                facilities.append(facility)
        
        # If we get here, the encoding worked
        return facilities
                
    except Exception as e:
        print(f"An error occurred while reading the file with {encoding} encoding: {e}")
        return []