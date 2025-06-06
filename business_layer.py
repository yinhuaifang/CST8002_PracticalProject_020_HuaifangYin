"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project02
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [May 25  2025]
Author: [Huaifang Yin]
Description: Business layer for managing facility records and operations.
"""

from typing import List, Optional
from facility_record import FacilityRecord

class FacilityManager:
    """
    Business layer class that manages facility records and operations.
    """
    
    def __init__(self):
        """Initialize the facility manager with an empty list of facilities."""
        self._facilities: List[FacilityRecord] = []
    
    @property
    def facilities(self) -> List[FacilityRecord]:
        """Get the list of facilities."""
        return self._facilities
    
    def add_facility(self, facility: FacilityRecord) -> None:
        """
        Add a new facility to the list.
        
        Args:
            facility (FacilityRecord): The facility record to add
        """
        self._facilities.append(facility)
    
    def remove_facility(self, index: int) -> bool:
        """
        Remove a facility at the specified index.
        
        Args:
            index (int): Index of the facility to remove
            
        Returns:
            bool: True if removal was successful, False otherwise
        """
        try:
            self._facilities.pop(index)
            return True
        except IndexError:
            return False
    
    def update_facility(self, index: int, facility: FacilityRecord) -> bool:
        """
        Update a facility at the specified index.
        
        Args:
            index (int): Index of the facility to update
            facility (FacilityRecord): New facility data
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            self._facilities[index] = facility
            return True
        except IndexError:
            return False
    
    def get_facility(self, index: int) -> Optional[FacilityRecord]:
        """
        Get a facility at the specified index.
        
        Args:
            index (int): Index of the facility to get
            
        Returns:
            Optional[FacilityRecord]: The facility record if found, None otherwise
        """
        try:
            return self._facilities[index]
        except IndexError:
            return None
    
    def clear_facilities(self) -> None:
        """Clear all facilities from the list."""
        self._facilities.clear()
    
    def get_facility_count(self) -> int:
        """
        Get the total number of facilities.
        
        Returns:
            int: Number of facilities
        """
        return len(self._facilities) 