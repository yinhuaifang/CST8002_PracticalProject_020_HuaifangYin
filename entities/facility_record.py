"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: This program reads and analyzes nitrogen oxide emissions data from Canadian facilities.
It loads data from a CSV file, creates FacilityRecord objects, and displays the information.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Try to import MySQL connector for Django-style operations
try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

class FacilityRecord(ABC):
    """
    Abstract base class for facility records.
    This demonstrates inheritance and polymorphism by providing
    different display formats for facility records.
    Django-style model with database operations.
    """
    
    # Django-style model fields
    _fields = {
        'npri_id': 'VARCHAR(50)',
        'facility_name': 'VARCHAR(255)',
        'company_name': 'VARCHAR(255)',
        'address': 'VARCHAR(255)',
        'city': 'VARCHAR(100)',
        'province': 'VARCHAR(50)',
        'postal_code': 'VARCHAR(20)',
        'latitude': 'DECIMAL(10, 8)',
        'longitude': 'DECIMAL(11, 8)',
        'emissions': 'DECIMAL(15, 2)',
        'units': 'VARCHAR(20)',
        'facility_details': 'TEXT',
        'facility_information': 'TEXT',
        'report_year': 'INT'
    }
    
    # Django-style table name
    _table_name = 'facilities'
    
    def __init__(self, npri_id="", facility_name="", company_name="", address="", 
                 city="", province="", postal_code="", latitude=0.0, longitude=0.0, 
                 emissions=0.0, units="", facility_details="", facility_information="", 
                 report_year=0, id=None):
        """
        Initialize a FacilityRecord with all attributes.
        
        Args:
            npri_id (str): NPRI ID
            facility_name (str): Facility name
            company_name (str): Company name
            address (str): Street address
            city (str): City
            province (str): Province
            postal_code (str): Postal code
            latitude (float): Latitude
            longitude (float): Longitude
            emissions (float): Emissions amount
            units (str): Units
            facility_details (str): Details URL
            facility_information (str): Info URL
            report_year (int): Report year
            id (int): Database ID (Django-style primary key)
        """
        self.id = id  # Django-style primary key
        self.npri_id = npri_id
        self.facility_name = facility_name
        self.company_name = company_name
        self.address = address
        self.city = city
        self.province = province
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude
        self.emissions = emissions
        self.units = units
        self.facility_details = facility_details
        self.facility_information = facility_information
        self.report_year = report_year
    
    @abstractmethod
    def display(self) -> str:
        """
        Abstract method to display facility information.
        This method must be overridden by subclasses.
        
        Returns:
            str: Formatted string representation of the facility
        """
        pass
    
    def __str__(self):
        """Return the display format of the facility."""
        return self.display()
    
    # Django-style model methods
    def save(self, connection=None) -> bool:
        """
        Django-style save method - saves the object to database.
        
        Args:
            connection: Database connection
            
        Returns:
            bool: True if save successful, False otherwise
        """
        if not MYSQL_AVAILABLE or not connection:
            return False
            
        try:
            cursor = connection.cursor()
            
            if self.id is None:
                # Creating new object [1.4.1]
                insert_query = f"""
                INSERT INTO {self._table_name} (
                    npri_id, facility_name, company_name, address, city, province,
                    postal_code, latitude, longitude, emissions, units,
                    facility_details, facility_information, report_year
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                values = (
                    self.npri_id, self.facility_name, self.company_name, self.address,
                    self.city, self.province, self.postal_code, self.latitude,
                    self.longitude, self.emissions, self.units, self.facility_details,
                    self.facility_information, self.report_year
                )
                
                cursor.execute(insert_query, values)
                connection.commit()
                
                # Get the auto-generated ID
                self.id = cursor.lastrowid
                print(f"Created new facility with ID: {self.id}")
                
            else:
                # Saving changes to existing object [1.4.2]
                update_query = f"""
                UPDATE {self._table_name} SET
                    npri_id = %s, facility_name = %s, company_name = %s,
                    address = %s, city = %s, province = %s, postal_code = %s,
                    latitude = %s, longitude = %s, emissions = %s, units = %s,
                    facility_details = %s, facility_information = %s, report_year = %s
                WHERE id = %s
                """
                
                values = (
                    self.npri_id, self.facility_name, self.company_name, self.address,
                    self.city, self.province, self.postal_code, self.latitude,
                    self.longitude, self.emissions, self.units, self.facility_details,
                    self.facility_information, self.report_year, self.id
                )
                
                cursor.execute(update_query, values)
                connection.commit()
                print(f"Updated facility with ID: {self.id}")
            
            return True
            
        except Error as e:
            print(f"Error saving facility: {e}")
            return False
    
    def delete(self, connection=None) -> bool:
        """
        Django-style delete method - deletes the object from database.
        
        Args:
            connection: Database connection
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        if not MYSQL_AVAILABLE or not connection or self.id is None:
            return False
            
        try:
            cursor = connection.cursor()
            delete_query = f"DELETE FROM {self._table_name} WHERE id = %s"
            cursor.execute(delete_query, (self.id,))
            connection.commit()
            print(f"Deleted facility with ID: {self.id}")
            return True
            
        except Error as e:
            print(f"Error deleting facility: {e}")
            return False
    
    @classmethod
    def objects(cls, connection=None):
        """
        Django-style objects manager for database operations.
        
        Args:
            connection: Database connection
            
        Returns:
            FacilityManager: Manager instance for database operations
        """
        return FacilityManager(cls, connection)
    
    @classmethod
    def create_table(cls, connection=None) -> bool:
        """
        Django-style migration - create table for this model.
        
        Args:
            connection: Database connection
            
        Returns:
            bool: True if table creation successful, False otherwise
        """
        if not MYSQL_AVAILABLE or not connection:
            return False
            
        try:
            cursor = connection.cursor()
            
            # Build CREATE TABLE query dynamically from model fields
            field_definitions = []
            for field_name, field_type in cls._fields.items():
                field_definitions.append(f"{field_name} {field_type}")
            
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {cls._table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                {', '.join(field_definitions)},
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_table_query)
            connection.commit()
            print(f"Created table: {cls._table_name}")
            return True
            
        except Error as e:
            print(f"Error creating table: {e}")
            return False

class FacilityManager:
    """
    Django-style objects manager for database operations.
    """
    
    def __init__(self, model_class, connection=None):
        self.model_class = model_class
        self.connection = connection
    
    def all(self) -> List[FacilityRecord]:
        """
        Django-style all() method - retrieve all objects [1.4.3].
        
        Returns:
            List[FacilityRecord]: All facility records
        """
        if not MYSQL_AVAILABLE or not self.connection:
            return []
            
        try:
            cursor = self.connection.cursor()
            select_query = f"SELECT * FROM {self.model_class._table_name} ORDER BY id"
            cursor.execute(select_query)
            records = cursor.fetchall()
            
            facilities = []
            for record in records:
                # Create facility instance with database data
                facility = self.model_class(
                    id=record[0],  # Primary key
                    npri_id=record[1],
                    facility_name=record[2],
                    company_name=record[3],
                    address=record[4],
                    city=record[5],
                    province=record[6],
                    postal_code=record[7],
                    latitude=float(record[8]) if record[8] else 0.0,
                    longitude=float(record[9]) if record[9] else 0.0,
                    emissions=float(record[10]) if record[10] else 0.0,
                    units=record[11],
                    facility_details=record[12],
                    facility_information=record[13],
                    report_year=int(record[14]) if record[14] else 0
                )
                facilities.append(facility)
            
            return facilities
            
        except Error as e:
            print(f"Error retrieving facilities: {e}")
            return []
    
    def filter(self, **kwargs) -> List[FacilityRecord]:
        """
        Django-style filter() method - filter objects by criteria.
        
        Args:
            **kwargs: Filter criteria
            
        Returns:
            List[FacilityRecord]: Filtered facility records
        """
        if not MYSQL_AVAILABLE or not self.connection:
            return []
            
        try:
            cursor = self.connection.cursor()
            
            # Build WHERE clause from kwargs
            conditions = []
            values = []
            for field, value in kwargs.items():
                if field in self.model_class._fields:
                    conditions.append(f"{field} = %s")
                    values.append(value)
            
            if not conditions:
                return self.all()
            
            where_clause = " AND ".join(conditions)
            select_query = f"SELECT * FROM {self.model_class._table_name} WHERE {where_clause} ORDER BY id"
            
            cursor.execute(select_query, values)
            records = cursor.fetchall()
            
            facilities = []
            for record in records:
                facility = self.model_class(
                    id=record[0],
                    npri_id=record[1],
                    facility_name=record[2],
                    company_name=record[3],
                    address=record[4],
                    city=record[5],
                    province=record[6],
                    postal_code=record[7],
                    latitude=float(record[8]) if record[8] else 0.0,
                    longitude=float(record[9]) if record[9] else 0.0,
                    emissions=float(record[10]) if record[10] else 0.0,
                    units=record[11],
                    facility_details=record[12],
                    facility_information=record[13],
                    report_year=int(record[14]) if record[14] else 0
                )
                facilities.append(facility)
            
            return facilities
            
        except Error as e:
            print(f"Error filtering facilities: {e}")
            return []
    
    def get(self, **kwargs) -> Optional[FacilityRecord]:
        """
        Django-style get() method - get single object.
        
        Args:
            **kwargs: Filter criteria
            
        Returns:
            Optional[FacilityRecord]: Single facility record or None
        """
        facilities = self.filter(**kwargs)
        return facilities[0] if facilities else None
    
    def count(self) -> int:
        """
        Django-style count() method - count total objects.
        
        Returns:
            int: Number of facilities
        """
        if not MYSQL_AVAILABLE or not self.connection:
            return 0
            
        try:
            cursor = self.connection.cursor()
            count_query = f"SELECT COUNT(*) FROM {self.model_class._table_name}"
            cursor.execute(count_query)
            count = cursor.fetchone()[0]
            return count
            
        except Error as e:
            print(f"Error counting facilities: {e}")
            return 0

class ShortFormatFacility(FacilityRecord):
    """
    Subclass that displays facility information in a short, compact format.
    """
    
    def display(self) -> str:
        """
        Display facility in short format.
        
        Returns:
            str: Short formatted string
        """
        return (f"{self.facility_name} | {self.company_name} | "
                f"{self.city}, {self.province} | {self.emissions} {self.units}")

class DetailedFormatFacility(FacilityRecord):
    """
    Subclass that displays facility information in a detailed, comprehensive format.
    """
    
    def display(self) -> str:
        """
        Display facility in detailed format.
        
        Returns:
            str: Detailed formatted string
        """
        return (f"=== DETAILED FACILITY REPORT ===\n"
                f"NPRI ID: {self.npri_id}\n"
                f"Facility Name: {self.facility_name}\n"
                f"Company: {self.company_name}\n"
                f"Address: {self.address}\n"
                f"City: {self.city}\n"
                f"Province: {self.province}\n"
                f"Postal Code: {self.postal_code}\n"
                f"Latitude: {self.latitude}\n"
                f"Longitude: {self.longitude}\n"
                f"Emissions: {self.emissions} {self.units}\n"
                f"Report Year: {self.report_year}\n"
                f"Facility Details: {self.facility_details}\n"
                f"Facility Information: {self.facility_information}\n"
                f"=================================")

class StandardFormatFacility(FacilityRecord):
    """
    Subclass that displays facility information in the original standard format.
    """
    
    def display(self) -> str:
        """
        Display facility in standard format.
        
        Returns:
            str: Standard formatted string
        """
        return (f"Facility: {self.facility_name}\n"
                f"Company: {self.company_name}\n"
                f"Location: {self.address}, {self.city}, {self.province} {self.postal_code}\n"
                f"Coordinates: {self.latitude}, {self.longitude}\n"
                f"Emissions: {self.emissions} {self.units} ({self.report_year})\n"
                f"Details: {self.facility_details}")

# Legacy RecordFormatter classes for backward compatibility
class RecordFormatter(ABC):
    """
    Abstract base class for formatting facility records.
    This demonstrates inheritance and polymorphism by providing
    different formatting strategies for displaying records.
    """
    
    @abstractmethod
    def format_record(self, record) -> str:
        """
        Abstract method to format a facility record.
        
        Args:
            record: The facility record to format
            
        Returns:
            str: Formatted string representation of the record
        """
        pass

class StandardFormatter(RecordFormatter):
    """
    Standard formatter that displays records in the original format.
    """
    
    def format_record(self, record) -> str:
        """
        Format record in standard format.
        
        Args:
            record: The facility record to format
            
        Returns:
            str: Standard formatted string
        """
        return (f"Facility: {record.facility_name}\n"
                f"Company: {record.company_name}\n"
                f"Location: {record.address}, {record.city}, {record.province} {record.postal_code}\n"
                f"Coordinates: {record.latitude}, {record.longitude}\n"
                f"Emissions: {record.emissions} {record.units} ({record.report_year})\n"
                f"Details: {record.facility_details}")

class CompactFormatter(RecordFormatter):
    """
    Compact formatter that displays records in a condensed format.
    """
    
    def format_record(self, record) -> str:
        """
        Format record in compact format.
        
        Args:
            record: The facility record to format
            
        Returns:
            str: Compact formatted string
        """
        return (f"{record.facility_name} | {record.company_name} | "
                f"{record.city}, {record.province} | {record.emissions} {record.units}")

class DetailedFormatter(RecordFormatter):
    """
    Detailed formatter that displays records with comprehensive information.
    """
    
    def format_record(self, record) -> str:
        """
        Format record in detailed format.
        
        Args:
            record: The facility record to format
            
        Returns:
            str: Detailed formatted string
        """
        return (f"=== DETAILED FACILITY REPORT ===\n"
                f"NPRI ID: {record.npri_id}\n"
                f"Facility Name: {record.facility_name}\n"
                f"Company: {record.company_name}\n"
                f"Address: {record.address}\n"
                f"City: {record.city}\n"
                f"Province: {record.province}\n"
                f"Postal Code: {record.postal_code}\n"
                f"Latitude: {record.latitude}\n"
                f"Longitude: {record.longitude}\n"
                f"Emissions: {record.emissions} {record.units}\n"
                f"Report Year: {record.report_year}\n"
                f"Facility Details: {record.facility_details}\n"
                f"Facility Information: {record.facility_information}\n"
                f"=================================")