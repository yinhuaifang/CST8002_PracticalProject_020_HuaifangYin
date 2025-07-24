"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Database layer for handling MySQL database operations with Django-style patterns.
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import List, Optional
from entities.facility_record import FacilityRecord

# Try to import MySQL connector
try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    print("Note: MySQL connector not available. Install mysql-connector-python to enable database features.")

class DatabaseManager:
    """
    Database manager class for handling MySQL database operations.
    This demonstrates database connectivity as an advanced language feature.
    Implements database operations and migrations.
    """
    
    def __init__(self, host="localhost", user="root", password="1101", database="project03"):
        """
        Initialize the database manager.
        
        Args:
            host (str): Database host
            user (str): Database user
            password (str): Database password
            database (str): Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """
        Connect to the MySQL database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        if not MYSQL_AVAILABLE:
            print("MySQL connector not available.")
            return False
            
        try:
            # Debug: Print connection parameters
            print(f"Attempting to connect with: host={self.host}, user={self.user}, database={self.database}")
            # Use the specific connection code provided by the user
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print(f"Connected to MySQL database: {self.database}")
                return True
            else:
                print("Failed to connect to MySQL database.")
                return False
                
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the MySQL database."""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Disconnected from MySQL database.")
    
    def create_table(self) -> bool:
        """
        Create the facilities table if it doesn't exist.
        
        Returns:
            bool: True if table creation successful, False otherwise
        """
        if not self.connection or not self.connection.is_connected():
            print("Not connected to database.")
            return False
            
        try:
            cursor = self.connection.cursor()
            
            # Create facilities table with all required fields
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS facilities (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    npri_id VARCHAR(255) NOT NULL,
                    facility_name VARCHAR(255) NOT NULL,
                    company_name VARCHAR(255) NOT NULL,
                    address TEXT,
                    city VARCHAR(255),
                    province VARCHAR(255),
                    postal_code VARCHAR(20),
                    latitude DECIMAL(10, 8),
                    longitude DECIMAL(11, 8),
                    emissions DECIMAL(15, 2),
                    units VARCHAR(50),
                    facility_details TEXT,
                    facility_information TEXT,
                    report_year INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            
            self.connection.commit()
            print("Facilities table created successfully.")
            return True
            
        except Error as e:
            print(f"Error creating table: {e}")
            return False
    
    def insert_facility(self, facility: FacilityRecord) -> bool:
        """
        Insert a new facility record into the database.
        
        Args:
            facility (FacilityRecord): The facility record to insert
            
        Returns:
            bool: True if insertion was successful, False otherwise
        """
        if not self.connection or not self.connection.is_connected():
            print("Not connected to database.")
            return False
            
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO facilities (
                    npri_id, facility_name, company_name, address, city, province,
                    postal_code, latitude, longitude, emissions, units,
                    facility_details, facility_information, report_year
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                facility.npri_id, facility.facility_name, facility.company_name,
                facility.address, facility.city, facility.province, facility.postal_code,
                facility.latitude, facility.longitude, facility.emissions, facility.units,
                facility.facility_details, facility.facility_information, facility.report_year
            ))
            
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"Insert error: {e}")
            return False
    
    def get_all_facilities(self) -> List[FacilityRecord]:
        """
        Retrieve all facility records from the database.
        
        Returns:
            List[FacilityRecord]: List of all facility records
        """
        if not self.connection or not self.connection.is_connected():
            print("Not connected to database.")
            return []
            
        facilities = []
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT npri_id, facility_name, company_name, address, city, province,
                       postal_code, latitude, longitude, emissions, units,
                       facility_details, facility_information, report_year
                FROM facilities
                ORDER BY id
            ''')
            
            rows = cursor.fetchall()
            for row in rows:
                facility = FacilityRecord(
                    npri_id=row[0],
                    facility_name=row[1],
                    company_name=row[2],
                    address=row[3],
                    city=row[4],
                    province=row[5],
                    postal_code=row[6],
                    latitude=row[7],
                    longitude=row[8],
                    emissions=row[9],
                    units=row[10],
                    facility_details=row[11],
                    facility_information=row[12],
                    report_year=row[13]
                )
                facilities.append(facility)
            
            return facilities
            
        except Error as e:
            print(f"Select error: {e}")
            return []
    
    def get_facility_by_id(self, facility_id: int) -> Optional[FacilityRecord]:
        """
        Retrieve a facility record by its database ID.
        
        Args:
            facility_id (int): The database ID of the facility
            
        Returns:
            Optional[FacilityRecord]: The facility record if found, None otherwise
        """
        if not self.connection or not self.connection.is_connected():
            print("Not connected to database.")
            return None
            
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT npri_id, facility_name, company_name, address, city, province,
                       postal_code, latitude, longitude, emissions, units,
                       facility_details, facility_information, report_year
                FROM facilities
                WHERE id = %s
            ''', (facility_id,))
            
            row = cursor.fetchone()
            if row:
                return FacilityRecord(
                    npri_id=row[0],
                    facility_name=row[1],
                    company_name=row[2],
                    address=row[3],
                    city=row[4],
                    province=row[5],
                    postal_code=row[6],
                    latitude=row[7],
                    longitude=row[8],
                    emissions=row[9],
                    units=row[10],
                    facility_details=row[11],
                    facility_information=row[12],
                    report_year=row[13]
                )
            return None
            
        except Error as e:
            print(f"Select by ID error: {e}")
            return None
    
    def update_facility(self, facility_id: int, facility: FacilityRecord) -> bool:
        """
        Update a facility record in the database.
        
        Args:
            facility_id (int): The database ID of the facility to update
            facility (FacilityRecord): The updated facility data
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        if not self.connection or not self.connection.is_connected():
            print("Not connected to database.")
            return False
            
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                UPDATE facilities SET
                    npri_id = %s, facility_name = %s, company_name = %s, address = %s,
                    city = %s, province = %s, postal_code = %s, latitude = %s, longitude = %s,
                    emissions = %s, units = %s, facility_details = %s, facility_information = %s,
                    report_year = %s
                WHERE id = %s
            ''', (
                facility.npri_id, facility.facility_name, facility.company_name,
                facility.address, facility.city, facility.province, facility.postal_code,
                facility.latitude, facility.longitude, facility.emissions, facility.units,
                facility.facility_details, facility.facility_information, facility.report_year,
                facility_id
            ))
            
            self.connection.commit()
            return cursor.rowcount > 0
            
        except Error as e:
            print(f"Update error: {e}")
            return False
    
    def delete_facility(self, facility_id: int) -> bool:
        """
        Delete a facility record from the database.
        
        Args:
            facility_id (int): The database ID of the facility to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        if not self.connection or not self.connection.is_connected():
            print("Not connected to database.")
            return False
            
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM facilities WHERE id = %s', (facility_id,))
            
            self.connection.commit()
            return cursor.rowcount > 0
            
        except Error as e:
            print(f"Delete error: {e}")
            return False
    
    def get_facility_count(self) -> int:
        """
        Get the total number of facilities in the database.
        
        Returns:
            int: Number of facilities
        """
        if not self.connection or not self.connection.is_connected():
            print("Not connected to database.")
            return 0
            
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM facilities')
            return cursor.fetchone()[0]
            
        except Error as e:
            print(f"Count error: {e}")
            return 0
    
    def clear_all_facilities(self) -> bool:
        """
        Clear all facilities from the database.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connection or not self.connection.is_connected():
            print("Not connected to database.")
            return False
            
        try:
            cursor = self.connection.cursor()
            cursor.execute('DELETE FROM facilities')
            cursor.execute('ALTER TABLE facilities AUTO_INCREMENT = 1')
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"Clear error: {e}")
            return False
    
    def populate_from_csv(self, csv_file_path: str, max_records: int = 100) -> int:
        """
        Populate the database with data from a CSV file.
        
        Args:
            csv_file_path (str): Path to the CSV file
            max_records (int): Maximum number of records to import
            
        Returns:
            int: Number of records successfully imported
        """
        if not self.connection or not self.connection.is_connected():
            print("Not connected to database.")
            return 0
            
        import csv
        
        try:
            # Clear existing data
            self.clear_all_facilities()
            
            records_imported = 0
            with open(csv_file_path, mode='r', encoding='ansi') as file:
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
                    
                    if self.insert_facility(facility):
                        records_imported += 1
            
            return records_imported
            
        except Exception as e:
            print(f"CSV import error: {e}")
            return 0 