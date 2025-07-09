"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Business layer for managing facility records and operations with multithreading support.
"""

from typing import List, Optional
import threading
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from entities.facility_record import (
    FacilityRecord, ShortFormatFacility, DetailedFormatFacility, StandardFormatFacility,
    RecordFormatter, StandardFormatter, CompactFormatter, DetailedFormatter
)

class FacilityManager:
    """
    Business logic class for managing facility records and operations with multithreading support.
    """
    
    def __init__(self):
        """Initialize the facility manager with database as primary storage and thread-safe components."""
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
        
        # Thread-safe components
        self._facilities_lock = threading.RLock()  # Reentrant lock for nested operations
        self._database_lock = threading.Lock()
        self._processing_thread = None
        self._processing_queue = queue.Queue()
        self._is_processing = False
        self._thread_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="FacilityManager")
    
    @property
    def facilities(self) -> List[FacilityRecord]:
        """Get the list of facilities (thread-safe)."""
        with self._facilities_lock:
            return self._facilities.copy()  # Return a copy to prevent external modification
    
    @property
    def current_formatter(self) -> RecordFormatter:
        """Get the current formatter."""
        return self._formatters[self._current_formatter_index]
    
    @property
    def use_database(self) -> bool:
        """Check if database mode is enabled."""
        return self._use_database
    
    @property
    def current_format_class(self):
        """Get the current format class for polymorphic display."""
        return self._current_format_class
    
    def set_database_manager(self, database_manager):
        """
        Set the database manager for database operations.
        
        Args:
            database_manager: The database manager instance
        """
        self._database_manager = database_manager
        if database_manager and hasattr(database_manager, 'connection'):
            self._connection = database_manager.connection
    
    def enable_database_mode(self) -> bool:
        """
        Enable database mode and connect to database (thread-safe).
        
        Returns:
            bool: True if database connection successful, False otherwise
        """
        with self._database_lock:
            if self._database_manager:
                try:
                    if self._database_manager.connect():
                        self._use_database = True
                        self._connection = self._database_manager.connection
                        print("Database connection established successfully")
                        # Don't load facilities automatically - let user do it manually
                        # self._facilities = self._load_facilities_from_database()
                        return True
                    else:
                        print("Failed to connect to database")
                        return False
                except Exception as e:
                    print(f"Error in enable_database_mode: {e}")
                    return False
        return False
    
    def disable_database_mode(self):
        """Disable database mode and disconnect from database (thread-safe)."""
        with self._database_lock:
            if self._database_manager:
                self._database_manager.disconnect()
            self._use_database = False
            self._connection = None
            with self._facilities_lock:
                self._facilities.clear()
    
    def _load_facilities_from_database(self) -> List[FacilityRecord]:
        """
        Load facilities from database using Django-style operations (thread-safe).
        
        Returns:
            List[FacilityRecord]: List of facilities loaded from database
        """
        with self._database_lock:
            if not self._connection:
                print("No database connection available")
                return []
            
            try:
                print("Starting to load facilities from database...")
                # Use Django-style objects manager to retrieve all facilities [1.4.3]
                print("Calling objects manager...")
                facilities = self._current_format_class.objects(self._connection).all()
                print(f"Successfully loaded {len(facilities)} facilities from database")
                return facilities
            except Exception as e:
                print(f"Error loading facilities from database: {e}")
                print("Returning empty list and continuing...")
                return []
    
    def load_facilities_from_database_async(self, completion_callback: Optional[callable] = None) -> bool:
        """
        Load facilities from database in a separate thread of execution.
        This demonstrates multithreading for database operations.
        
        Args:
            completion_callback (callable): Callback function when loading completes
            
        Returns:
            bool: True if thread started successfully, False otherwise
        """
        if self._is_processing:
            print("Already processing in background. Please wait...")
            return False
        
        self._is_processing = True
        
        def load_worker():
            """Worker thread function for loading database data."""
            try:
                facilities = self._load_facilities_from_database()
                
                # Update facilities list thread-safely
                with self._facilities_lock:
                    self._facilities = facilities
                
                # Put results in queue for thread-safe access
                self._processing_queue.put(('success', len(facilities)))
                
                if completion_callback:
                    completion_callback(facilities)
                    
            except Exception as e:
                error_msg = f"Error loading facilities from database: {e}"
                print(error_msg)
                self._processing_queue.put(('error', error_msg))
                
            finally:
                self._is_processing = False
        
        # Start the loading thread
        self._processing_thread = threading.Thread(target=load_worker, daemon=True)
        self._processing_thread.start()
        
        print("Started loading facilities from database in background thread...")
        return True
    
    def get_processing_status(self) -> tuple[bool, Optional[int], Optional[str]]:
        """
        Get the current processing status and results (thread-safe).
        
        Returns:
            tuple: (is_processing, result_count, error_message)
        """
        # Check for results in queue
        try:
            status, data = self._processing_queue.get_nowait()
            if status == 'success':
                return False, data, None
            else:
                return False, None, data
        except queue.Empty:
            return self._is_processing, None, None
    
    def change_display_format(self, format_type: str) -> str:
        """
        Change the display format class for polymorphic display (thread-safe).
        
        Args:
            format_type (str): The format type ('short', 'detailed', 'standard')
            
        Returns:
            str: Name of the new format class
        """
        if format_type.lower() == 'short':
            self._current_format_class = ShortFormatFacility
        elif format_type.lower() == 'detailed':
            self._current_format_class = DetailedFormatFacility
        elif format_type.lower() == 'standard':
            self._current_format_class = StandardFormatFacility
        else:
            return "Unknown"
        
        # RELOAD facilities with new format class (thread-safe)
        if self._use_database and self._connection:
            with self._facilities_lock:
                self._facilities = self._load_facilities_from_database()
        
        return self.get_current_format_name()
    
    def get_current_format_name(self) -> str:
        """
        Get the name of the current format class.
        
        Returns:
            str: Name of the current format class
        """
        if self._current_format_class == ShortFormatFacility:
            return "Short"
        elif self._current_format_class == DetailedFormatFacility:
            return "Detailed"
        elif self._current_format_class == StandardFormatFacility:
            return "Standard"
        else:
            return "Unknown"
    
    def create_facility_with_format(self, **kwargs) -> FacilityRecord:
        """
        Create a facility record using the current format class.
        This demonstrates polymorphic object creation.
        
        Args:
            **kwargs: Facility attributes
            
        Returns:
            FacilityRecord: New facility record with current format
        """
        return self._current_format_class(**kwargs)
    
    def add_facility(self, facility: FacilityRecord) -> None:
        """
        Add a new facility to the database using Django-style operations (thread-safe).
        
        Args:
            facility (FacilityRecord): The facility record to add
        """
        with self._facilities_lock:
            if self._use_database and self._connection:
                # Use Django-style save method [1.4.1]
                if facility.save(self._connection):
                    # Refresh the in-memory list from database
                    self._facilities = self._load_facilities_from_database()
            else:
                self._facilities.append(facility)
    
    def remove_facility(self, index: int) -> bool:
        """
        Remove a facility at the specified index using Django-style operations (thread-safe).
        
        Args:
            index (int): Index of the facility to remove
            
        Returns:
            bool: True if removal was successful, False otherwise
        """
        with self._facilities_lock:
            if self._use_database and self._connection:
                # Get the facility to find its database ID
                facility = self.get_facility(index)
                if facility and facility.id is not None:
                    # Use Django-style delete method
                    if facility.delete(self._connection):
                        # Refresh the in-memory list from database
                        self._facilities = self._load_facilities_from_database()
                        return True
                return False
            else:
                try:
                    self._facilities.pop(index)
                    return True
                except IndexError:
                    return False
    
    def update_facility(self, index: int, facility: FacilityRecord) -> bool:
        """
        Update a facility at the specified index using Django-style operations (thread-safe).
        
        Args:
            index (int): Index of the facility to update
            facility (FacilityRecord): New facility data
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        with self._facilities_lock:
            if self._use_database and self._connection:
                # Get the original facility to preserve its ID
                original_facility = self.get_facility(index)
                if original_facility and original_facility.id is not None:
                    # Set the ID for the new facility to update the existing record
                    facility.id = original_facility.id
                    # Use Django-style save method [1.4.2]
                    if facility.save(self._connection):
                        # Refresh the in-memory list from database
                        self._facilities = self._load_facilities_from_database()
                        return True
                return False
            else:
                try:
                    self._facilities[index] = facility
                    return True
                except IndexError:
                    return False
    
    def get_facility(self, index: int) -> Optional[FacilityRecord]:
        """
        Get a facility at the specified index (thread-safe).
        
        Args:
            index (int): Index of the facility to get
            
        Returns:
            Optional[FacilityRecord]: The facility record if found, None otherwise
        """
        with self._facilities_lock:
            try:
                return self._facilities[index]
            except IndexError:
                return None
    
    def get_facility_count(self) -> int:
        """
        Get the total number of facilities using Django-style operations (thread-safe).
        
        Returns:
            int: Number of facilities
        """
        with self._facilities_lock:
            if self._use_database and self._connection:
                return self._current_format_class.objects(self._connection).count()
            else:
                return len(self._facilities)
    
    def populate_database_from_csv_async(self, csv_facilities: List[FacilityRecord],
                                       progress_callback: Optional[callable] = None,
                                       completion_callback: Optional[callable] = None) -> bool:
        """
        Populate database with CSV data in a separate thread of execution.
        This demonstrates multithreading for database operations.
        
        Args:
            csv_facilities (List[FacilityRecord]): Facilities from CSV file
            progress_callback (callable): Callback function for progress updates
            completion_callback (callable): Callback function when operation completes
            
        Returns:
            bool: True if thread started successfully, False otherwise
        """
        if self._is_processing:
            print("Already processing in background. Please wait...")
            return False
        
        self._is_processing = True
        
        def populate_worker():
            """Worker thread function for populating database."""
            try:
                success = False
                with self._facilities_lock:
                    if self._connection:
                        if self._populate_database_from_csv_data(csv_facilities, progress_callback):
                            self._facilities = self._load_facilities_from_database()
                            success = True
                
                self._processing_queue.put(('success', success))
                
                if completion_callback:
                    completion_callback(success)
                    
            except Exception as e:
                error_msg = f"Error populating database: {e}"
                print(error_msg)
                self._processing_queue.put(('error', error_msg))
                
            finally:
                self._is_processing = False
        
        # Start the population thread
        self._processing_thread = threading.Thread(target=populate_worker, daemon=True)
        self._processing_thread.start()
        
        print(f"Started populating database with {len(csv_facilities)} facilities in background thread...")
        return True
    
    def _populate_database_from_csv_data(self, facilities: List[FacilityRecord], 
                                        progress_callback: Optional[callable] = None) -> bool:
        """
        Populate the database with facility data from CSV using Django-style operations.
        
        Args:
            facilities (List[FacilityRecord]): List of facilities to insert
            progress_callback (callable): Callback function for progress updates
            
        Returns:
            bool: True if population successful, False otherwise
        """
        if not self._connection:
            return False
            
        try:
            # Clear existing data
            cursor = self._connection.cursor()
            cursor.execute(f"DELETE FROM {self._current_format_class._table_name}")
            self._connection.commit()
            
            # Insert new data using Django-style save method [1.4.1]
            for i, facility in enumerate(facilities):
                if not facility.save(self._connection):
                    return False
                
                # Report progress every 100 records
                if progress_callback and (i + 1) % 100 == 0:
                    progress = (i + 1) / len(facilities) * 100
                    progress_callback(progress, i + 1, len(facilities))
            
            print(f"Successfully populated database with {len(facilities)} facilities.")
            return True
            
        except Exception as e:
            print(f"Error populating database: {e}")
            return False
    
    def _get_formatter_name(self, formatter: RecordFormatter) -> str:
        """
        Get the name of a formatter.
        
        Args:
            formatter (RecordFormatter): The formatter to get the name for
            
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
        Sort facilities by emissions using the built-in sort method (thread-safe).
        
        Args:
            reverse (bool): If True, sort in descending order
        """
        with self._facilities_lock:
            self._facilities.sort(key=lambda x: x.emissions, reverse=reverse)
    
    def sort_facilities_by_name(self, reverse: bool = False) -> None:
        """
        Sort facilities by name using the built-in sort method (thread-safe).
        
        Args:
            reverse (bool): If True, sort in descending order
        """
        with self._facilities_lock:
            self._facilities.sort(key=lambda x: x.facility_name.lower(), reverse=reverse)
    
    def __del__(self):
        """Cleanup thread pool on destruction."""
        if hasattr(self, '_thread_pool'):
            self._thread_pool.shutdown(wait=True) 