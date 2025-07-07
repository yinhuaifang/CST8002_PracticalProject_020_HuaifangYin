"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Business layer for managing facility records and operations with multithreading support.
"""

from typing import List, Optional
from entities.facility_record import FacilityRecord, RecordFormatter, StandardFormatter, CompactFormatter, DetailedFormatter

class FacilityManager:
    """
    Business logic class for managing facility records and operations.
    """
    
    def __init__(self):
        """Initialize the facility manager with an empty list of facilities."""
        self._facilities: List[FacilityRecord] = []
        self._formatters: List[RecordFormatter] = [
            StandardFormatter(),
            CompactFormatter(),
            DetailedFormatter()
        ]
        self._current_formatter_index = 0
        self._database_manager = None
        self._use_database = True  # Default to database mode
        self._current_format_class = StandardFormatFacility  # Default format class
        self._connection = None  # Django-style database connection
    
    @property
    def facilities(self) -> List[FacilityRecord]:
        """Get the list of facilities."""
        return self._facilities
    
    @property
    def current_formatter(self) -> RecordFormatter:
        """Get the current formatter."""
        return self._formatters[self._current_formatter_index]
    
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
    
    def cycle_formatter(self) -> str:
        """
        Cycle to the next formatter and return its name.
        
        Returns:
            str: Name of the current formatter
        """
        self._current_formatter_index = (self._current_formatter_index + 1) % len(self._formatters)
        return self._get_formatter_name(self._formatters[self._current_formatter_index])
    
    def get_current_formatter_name(self) -> str:
        """
        Get the name of the current formatter.
        
        Returns:
            str: Name of the current formatter
        """
        return self._get_formatter_name(self.current_formatter)
    
    def _get_formatter_name(self, formatter: RecordFormatter) -> str:
        """
        Get the name of a formatter.
        
        Args:
            formatter (RecordFormatter): The formatter
            
        Returns:
            str: Name of the formatter
        """
        if isinstance(formatter, StandardFormatter):
            return "Standard"
        elif isinstance(formatter, CompactFormatter):
            return "Compact"
        elif isinstance(formatter, DetailedFormatter):
            return "Detailed"
        else:
            return "Unknown"
    
    def sort_facilities_by_emissions(self, reverse: bool = False) -> None:
        """
        Sort facilities by emissions using the built-in sort method.
        This demonstrates the use of advanced data structures and algorithms.
        
        Args:
            reverse (bool): If True, sort in descending order
        """
        self._facilities.sort(key=lambda x: x.emissions, reverse=reverse)
    
    def sort_facilities_by_name(self, reverse: bool = False) -> None:
        """
        Sort facilities by facility name using the built-in sort method.
        
        Args:
            reverse (bool): If True, sort in descending order
        """
        self._facilities.sort(key=lambda x: x.facility_name.lower(), reverse=reverse)
    
    def sort_facilities_by_province(self, reverse: bool = False) -> None:
        """
        Sort facilities by province using the built-in sort method.
        
        Args:
            reverse (bool): If True, sort in descending order
        """
        self._facilities.sort(key=lambda x: x.province.lower(), reverse=reverse)
    
    def get_formatted_facility(self, index: int) -> Optional[str]:
        """
        Get a formatted string representation of a facility using the current formatter.
        This demonstrates polymorphic method calls.
        
        Args:
            index (int): Index of the facility to format
            
        Returns:
            Optional[str]: Formatted string if facility exists, None otherwise
        """
        facility = self.get_facility(index)
        if facility:
            return self.current_formatter.format_record(facility)
        return None
    
    def get_all_formatted_facilities(self) -> List[str]:
        """
        Get formatted string representations of all facilities using the current formatter.
        This demonstrates polymorphic method calls on a collection.
        
        Returns:
            List[str]: List of formatted facility strings
        """
        return [self.current_formatter.format_record(facility) for facility in self._facilities] 