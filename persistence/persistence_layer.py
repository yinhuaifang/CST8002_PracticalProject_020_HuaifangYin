"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project02
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Persistence layer for handling file I/O operations.
"""
import os
import csv
import uuid
from typing import List, Optional
from entities.facility_record import FacilityRecord

class FileManager:
    """
    Persistence layer class for handling file read/write operations.
    """
    
    @staticmethod
    def load_facility_data(filename: str, max_records: int = 100) -> List[FacilityRecord]:
        """
        Load facility data from a CSV file.
        Args:
            filename (str): Path to the CSV file
            max_records (int): Maximum number of records to load (default 100)
        Returns:
            List[FacilityRecord]: List of loaded facility records
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
            
            return facilities
                    
        except Exception as e:
            print(f"An error occurred while reading the file with {encoding} encoding: {e}")
            return []
    
    @staticmethod
    def save_facility_data(facilities: List[FacilityRecord]) -> Optional[str]:
        """
        Save facility data to a new CSV file with a UUID filename.
        Args:
            facilities (List[FacilityRecord]): List of facilities to save
        Returns:
            Optional[str]: The generated filename if successful, None otherwise
        """
        if not facilities:
            return None
            
        # Generate a unique filename using UUID
        filename = f"facilities_{uuid.uuid4()}.csv"
        
        filename = os.path.join("..", "data", filename)

        #filename = f"facilities_updated.csv"
        
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Write header
                writer.writerow([
                    'NPRI ID', 'Facility name', 'Company name', 'Address',
                    'City', 'Province', 'PostalCode', 'Latitude', 'Longitude',
                    'Emissions', 'Units', 'Facility details', 'Facility information',
                    'Report year'
                ])
                
                # Write data
                for facility in facilities:
                    writer.writerow([
                        facility.npri_id,
                        facility.facility_name,
                        facility.company_name,
                        facility.address,
                        facility.city,
                        facility.province,
                        facility.postal_code,
                        facility.latitude,
                        facility.longitude,
                        facility.emissions,
                        facility.units,
                        facility.facility_details,
                        facility.facility_information,
                        facility.report_year
                    ])
            
            return filename
            
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")
            return None 