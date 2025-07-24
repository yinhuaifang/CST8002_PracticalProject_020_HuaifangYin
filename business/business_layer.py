"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Business layer for managing facility records and MySQL database operations.
Now includes visualization capabilities for data analysis.
"""

from typing import List, Optional
from entities.facility_record import FacilityRecord
from persistence.database_layer import DatabaseManager

class FacilityManager:
    """
    Business logic class for managing facility records and MySQL database operations.
    Implements database connectivity patterns and visualization features.
    """
    
    def __init__(self, host="localhost", user="root", password="1101", database="project03"):
        """
        Initialize the facility manager with MySQL database connection.
        
        Args:
            host (str): MySQL host
            user (str): MySQL user
            password (str): MySQL password
            database (str): MySQL database name
        """
        self.db_manager = DatabaseManager(host, user, password, database)
        self._facilities_cache: List[FacilityRecord] = []
        self._cache_dirty = True
        
        # Connect to database and create table
        if self.db_manager.connect():
            self.db_manager.create_table()
        else:
            print("Warning: Could not connect to MySQL database. Some features may not work.")
    
    @property
    def facilities(self) -> List[FacilityRecord]:
        """
        Get the list of facilities from MySQL database.
        Uses caching for performance.
        
        Returns:
            List[FacilityRecord]: List of all facilities
        """
        if self._cache_dirty:
            self._facilities_cache = self.db_manager.get_all_facilities()
            self._cache_dirty = False
        return self._facilities_cache
    
    def add_facility(self, facility: FacilityRecord) -> bool:
        """
        Add a new facility to the MySQL database.
        
        Args:
            facility (FacilityRecord): The facility record to add
            
        Returns:
            bool: True if addition was successful, False otherwise
        """
        success = self.db_manager.insert_facility(facility)
        if success:
            self._cache_dirty = True
        return success
    
    def remove_facility(self, index: int) -> bool:
        """
        Remove a facility at the specified index from the MySQL database.
        
        Args:
            index (int): Index of the facility to remove
            
        Returns:
            bool: True if removal was successful, False otherwise
        """
        facilities = self.facilities
        if 0 <= index < len(facilities):
            # Get the database ID by finding the facility at the given index
            # Since we don't store database IDs in the cache, we need to find it
            target_facility = facilities[index]
            
            # Find the database ID by matching facility data
            all_facilities = self.db_manager.get_all_facilities()
            for i, fac in enumerate(all_facilities):
                if (fac.npri_id == target_facility.npri_id and 
                    fac.facility_name == target_facility.facility_name and
                    fac.company_name == target_facility.company_name):
                    # This is the facility we want to delete
                    # We need to get the actual database ID
                    # For simplicity, we'll delete by matching criteria
                    success = self._delete_facility_by_criteria(target_facility)
                    if success:
                        self._cache_dirty = True
                    return success
            
        return False
    
    def _delete_facility_by_criteria(self, facility: FacilityRecord) -> bool:
        """
        Delete a facility by matching its criteria in the MySQL database.
        
        Args:
            facility (FacilityRecord): The facility to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute('''
                DELETE FROM facilities 
                WHERE npri_id = %s AND facility_name = %s AND company_name = %s
            ''', (facility.npri_id, facility.facility_name, facility.company_name))
            
            self.db_manager.connection.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Delete by criteria error: {e}")
            return False
    
    def update_facility(self, index: int, facility: FacilityRecord) -> bool:
        """
        Update a facility at the specified index in the MySQL database.
        
        Args:
            index (int): Index of the facility to update
            facility (FacilityRecord): New facility data
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        facilities = self.facilities
        if 0 <= index < len(facilities):
            # Get the original facility to find it in the database
            original_facility = facilities[index]
            
            # Find and update the facility in the database
            success = self._update_facility_by_criteria(original_facility, facility)
            if success:
                self._cache_dirty = True
            return success
        
        return False
    
    def _update_facility_by_criteria(self, original: FacilityRecord, updated: FacilityRecord) -> bool:
        """
        Update a facility by matching original criteria in the MySQL database.
        
        Args:
            original (FacilityRecord): The original facility to find
            updated (FacilityRecord): The updated facility data
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute('''
                UPDATE facilities SET
                    npri_id = %s, facility_name = %s, company_name = %s, address = %s,
                    city = %s, province = %s, postal_code = %s, latitude = %s, longitude = %s,
                    emissions = %s, units = %s, facility_details = %s, facility_information = %s,
                    report_year = %s
                WHERE npri_id = %s AND facility_name = %s AND company_name = %s
            ''', (
                updated.npri_id, updated.facility_name, updated.company_name,
                updated.address, updated.city, updated.province, updated.postal_code,
                updated.latitude, updated.longitude, updated.emissions, updated.units,
                updated.facility_details, updated.facility_information, updated.report_year,
                original.npri_id, original.facility_name, original.company_name
            ))
            
            self.db_manager.connection.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Update by criteria error: {e}")
            return False
    
    def get_facility(self, index: int) -> Optional[FacilityRecord]:
        """
        Get a facility at the specified index from the MySQL database.
        
        Args:
            index (int): Index of the facility to get
            
        Returns:
            Optional[FacilityRecord]: The facility record if found, None otherwise
        """
        facilities = self.facilities
        try:
            return facilities[index]
        except IndexError:
            return None
    
    def clear_facilities(self) -> bool:
        """
        Clear all facilities from the MySQL database.
        
        Returns:
            bool: True if successful, False otherwise
        """
        success = self.db_manager.clear_all_facilities()
        if success:
            self._cache_dirty = True
        return success
    
    def get_facility_count(self) -> int:
        """
        Get the total number of facilities in the MySQL database.
        
        Returns:
            int: Number of facilities
        """
        return self.db_manager.get_facility_count()
    
    def reload_from_csv(self, csv_file_path: str, max_records: int = 100) -> int:
        """
        Reload data from CSV file into the MySQL database.
        
        Args:
            csv_file_path (str): Path to the CSV file
            max_records (int): Maximum number of records to import
            
        Returns:
            int: Number of records successfully imported
        """
        records_imported = self.db_manager.populate_from_csv(csv_file_path, max_records)
        if records_imported > 0:
            self._cache_dirty = True
        return records_imported
    
    # Visualization methods
    def get_available_chart_types(self) -> List[str]:
        """
        Get list of available chart types for visualization.
        
        Returns:
            List[str]: List of available chart types
        """
        return self.chart_generator.get_available_chart_types()
    
    def generate_chart(self, chart_type: str, **kwargs) -> str:
        """
        Generate a chart based on the specified type.
        
        Args:
            chart_type (str): Type of chart to generate
            **kwargs: Additional arguments for specific chart types
            
        Returns:
            str: Generated chart as ASCII art
        """
        facilities = self.facilities
        if not facilities:
            return "No data available for chart generation. Please load data first."
        
        return self.chart_generator.generate_chart(chart_type, facilities, **kwargs)
    
    def search_facilities_by_province(self, province: str) -> List[FacilityRecord]:
        """
        Search for facilities in a specific province.
        
        Args:
            province (str): Province name to search for
            
        Returns:
            List[FacilityRecord]: List of facilities in the specified province
        """
        facilities = self.facilities
        return [facility for facility in facilities 
                if province.lower() in facility.province.lower()]
    
    def search_facilities_by_city(self, city: str) -> List[FacilityRecord]:
        """
        Search for facilities in a specific city.
        
        Args:
            city (str): City name to search for
            
        Returns:
            List[FacilityRecord]: List of facilities in the specified city
        """
        facilities = self.facilities
        return [facility for facility in facilities 
                if city.lower() in facility.city.lower()]
    
    def sort_facilities_by_emissions(self, reverse: bool = True) -> List[FacilityRecord]:
        """
        Sort facilities by emissions.
        
        Args:
            reverse (bool): If True, sort in descending order (highest first)
            
        Returns:
            List[FacilityRecord]: Sorted list of facilities
        """
        facilities = self.facilities.copy()
        return sorted(facilities, key=lambda x: float(x.emissions), reverse=reverse)
    
    def close_database(self) -> None:
        """Close the MySQL database connection."""
        self.db_manager.disconnect() 