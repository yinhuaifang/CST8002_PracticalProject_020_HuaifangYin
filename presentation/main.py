"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Presentation layer for the facility management system with multithreading support.
"""

import os
import sys
import time
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import Optional
from business.business_layer import FacilityManager
from persistence.persistence_layer import FileManager
from entities.facility_record import (
    FacilityRecord, ShortFormatFacility, DetailedFormatFacility, StandardFormatFacility
)

# Try to import database functionality (optional)
try:
    from persistence.database_layer import DatabaseManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("Note: Database functionality not available. Install mysql-connector-python to enable database features.")

class FacilityManagementSystem:
    """
    Presentation layer class that handles user interaction and display with multithreading support.
    """
    
    def __init__(self):
        """Initialize the facility management system."""
        self.manager = FacilityManager()
        self.file_manager = FileManager()
        # Use absolute path to ensure the CSV file can be found regardless of working directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.data_file = os.path.join(project_root, "data", "Nitrogen oxide emissions by facility.csv")
        
        # Set up database manager if available
        if DATABASE_AVAILABLE:
            try:
                self.database_manager = DatabaseManager()
                self.manager.set_database_manager(self.database_manager)
                # Connect to database on startup but don't load data automatically
                if self.manager.enable_database_mode():
                    print("Successfully connected to database!")
                    # Create table if it doesn't exist
                    if self.database_manager.create_table():
                        print("Database table ready!")
                        print("Use option 2 or 10 to load data from database.")
                    else:
                        print("Failed to create database table.")
                else:
                    print("Failed to connect to database. Please check your MySQL settings.")
            except Exception as e:
                print(f"Error during database initialization: {e}")
                print("Continuing without database functionality...")
                self.database_manager = None
        else:
            self.database_manager = None

    #self.data_file = "Nitrogen oxide emissions by facility.csv"
    
    def display_header(self):
        """Show the program header and author info."""
        print("\n" + "=" * 80)
        print("Facility Management System")
        print("Created by: Huaifang Yin")
        print("Current Display Format: " + self.manager.get_current_format_name())
        if DATABASE_AVAILABLE and self.manager.use_database:
            print("Storage Mode: Database")
        else:
            print("Storage Mode: File")
        print("=" * 80 + "\n")
    
    def display_menu(self):
        """Show the main menu options."""
        print("\n==================== Main Menu ====================")
        print("1. Initial import data from CSV file (Async)")
        print("2. Load data from database (Async)")
        print("3. Display single facility by index")
        print("4. Add new facility")
        print("5. Edit facility")
        print("6. Delete facility")
        print("7. Sort facilities")
        print("8. Change display format")
        print("9. Exit")
        print("====================================================")
    
    def display_sort_menu(self):
        """Show the sorting menu options."""
        print("\nSort Options:")
        print("1. Sort by facility name (A-Z)")
        print("2. Sort by facility name (Z-A)")
        print("3. Sort by emissions (low to high)")
        print("4. Sort by emissions (high to low)")
        print("5. Back to main menu")
    
    def display_format_menu(self):
        """Show the display format menu options."""
        print("\nDisplay Format Options:")
        print("1. Short format")
        print("2. Detailed format")
        print("3. Standard format")
        print("4. Back to main menu")
    
    def get_facility_input(self) -> Optional[FacilityRecord]:
        """
        Get facility information from user input and create facility with current format.
        Returns:
            Optional[FacilityRecord]: New facility record if input is valid, None otherwise
        """
        try:
            print("\nEnter facility details:")
            npri_id = input("NPRI ID: ")
            facility_name = input("Facility name: ")
            company_name = input("Company name: ")
            address = input("Address: ")
            city = input("City: ")
            province = input("Province: ")
            postal_code = input("Postal code: ")
            latitude = float(input("Latitude: "))
            longitude = float(input("Longitude: "))
            emissions = float(input("Emissions: "))
            units = input("Units: ")
            facility_details = input("Facility details URL: ")
            facility_information = input("Facility information URL: ")
            report_year = int(input("Report year: "))
            
            # Create facility using the current format class (polymorphic object creation)
            return self.manager.create_facility_with_format(
                npri_id=npri_id,
                facility_name=facility_name,
                company_name=company_name,
                address=address,
                city=city,
                province=province,
                postal_code=postal_code,
                latitude=latitude,
                longitude=longitude,
                emissions=emissions,
                units=units,
                facility_details=facility_details,
                facility_information=facility_information,
                report_year=report_year
            )
        except ValueError:
            print("Invalid input. Please enter valid numbers for numeric fields.")
            return None
    
    def handle_sorting(self):
        """Handle the sorting menu and operations."""
        while True:
            self.display_sort_menu()
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                self.manager.sort_facilities_by_name(reverse=False)
                print("\nFacilities sorted by name (A-Z)")
            elif choice == "2":
                self.manager.sort_facilities_by_name(reverse=True)
                print("\nFacilities sorted by name (Z-A)")
            elif choice == "3":
                self.manager.sort_facilities_by_emissions(reverse=False)
                print("\nFacilities sorted by emissions (low to high)")
            elif choice == "4":
                self.manager.sort_facilities_by_emissions(reverse=True)
                print("\nFacilities sorted by emissions (high to low)")
            elif choice == "5":
                break
            else:
                print("\nInvalid choice. Please try again.")
            
            self.display_top_n_facilities(3)

            input("\nPress Enter to continue...")
    
    def display_top_n_facilities(self, n: int):
        """Display the top 3 facilities after sorting."""
        if self.manager.get_facility_count() == 0:
            print("No facilities to display.")
            return
        
        print(f"\n--- Top {n} Facilities ---")
        for i in range(min(n, self.manager.get_facility_count())):
            facility = self.manager.get_facility(i)
            if facility:
                print(f"\n--- Record {i + 1} ---")
                print(facility.display())
        print(f"--- End of Top {n} ---")
    
    def handle_display_format_change(self):
        """Handle the display format change menu."""
        while True:
            self.display_format_menu()
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                new_format = self.manager.change_display_format("short")
                print(f"\nDisplay format changed to: {new_format}")
            elif choice == "2":
                new_format = self.manager.change_display_format("detailed")
                print(f"\nDisplay format changed to: {new_format}")
            elif choice == "3":
                new_format = self.manager.change_display_format("standard")
                print(f"\nDisplay format changed to: {new_format}")
            elif choice == "4":
                break
            else:
                print("\nInvalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    
    def load_csv_data_async(self):
        """Load CSV data using background thread."""
        print(f"\nInitial import from CSV file...")
        
        def load_worker():
            """Worker thread function for loading CSV data."""
            try:
                # Drop and recreate the table if using the database
                if DATABASE_AVAILABLE and self.manager.use_database and self.database_manager and self.database_manager.connection:
                    cursor = self.database_manager.connection.cursor()
                    
                    # Drop the table if it exists
                    cursor.execute("DROP TABLE IF EXISTS facilities")
                    self.database_manager.connection.commit()
                    print("Database table dropped.")
                    
                    # Recreate the table
                    if self.database_manager.create_table():
                        print("Database table recreated.")
                    else:
                        print("Failed to recreate database table.")
                        return
                
                facilities = self.file_manager.load_facility_data(self.data_file, max_records=100)
                
                if facilities:
                    # Populate database with loaded facilities
                    if DATABASE_AVAILABLE and self.manager.use_database:
                        success = self.manager.populate_database_from_csv_async(
                            facilities,
                            completion_callback=lambda success: print(f"\n✓ Imported {len(facilities)} facilities to database!")
                        )
                    else:
                        # Add to in-memory storage
                        for facility in facilities:
                            self.manager.add_facility(facility)
                        print(f"\n✓ Imported {len(facilities)} facilities to memory!")
                else:
                    print("\n✗ Failed to import facilities from CSV file.")
                    
            except Exception as e:
                print(f"\n✗ Error importing CSV data: {e}")
        
        # Start the loading thread
        loading_thread = threading.Thread(target=load_worker, daemon=True)
        loading_thread.start()
        
        print("Initial import started in background. You can continue using the menu...")
    
    def load_database_data_async(self):
        """Load database data using background thread."""
        if not DATABASE_AVAILABLE:
            print("\nDatabase functionality is not available.")
            return
        
        print("\nLoading data from database in background thread...")
        
        def on_completion(facilities):
            print(f"\n✓ Successfully loaded {len(facilities)} facilities from database in background!")
        
        # Start async loading
        if self.manager.load_facilities_from_database_async(completion_callback=on_completion):
            print("Loading started in background thread. You can continue using the menu...")
            
            # Monitor loading progress
            while True:
                is_processing, count, error = self.manager.get_processing_status()
                
                if not is_processing:
                    if count is not None:
                        print(f"\n✓ Successfully loaded {count} facilities from database!")
                    elif error:
                        print(f"\n✗ Loading failed: {error}")
                    break
                
                time.sleep(0.5)  # Check status every 500ms
        else:
            print("Failed to start loading. Another operation may be in progress.")
    
    def run(self):
        """Run the main loop of the facility management system."""
        while True:
            self.display_header()
            self.display_menu()
            choice = input("\nEnter your choice (1-9): ")
            
            if choice == "1":
                # Import data from CSV file (Async)
                self.load_csv_data_async()
            
            elif choice == "2":
                # Load data from database (Async)
                self.load_database_data_async()
            
            elif choice == "3":
                # Display single facility by index
                if self.manager.get_facility_count() > 0:
                    try:
                        index = int(input("\nEnter facility index (0-{}): ".format(
                            self.manager.get_facility_count() - 1)))
                        facility = self.manager.get_facility(index)
                        if facility:
                            print("\n" + "-" * 80)
                            print(facility.display())  # Polymorphic call                          
                        else:
                            print("\nInvalid facility index.")
                    except ValueError:
                        print("\nPlease enter a valid number.")
                else:
                    print("\nNo facilities to display.")
            
            elif choice == "4":
                # Add new facility
                facility = self.get_facility_input()
                if facility:
                    self.manager.add_facility(facility)
                    print("\nFacility added successfully to database.")
            
            elif choice == "5":
                # Edit facility
                if self.manager.get_facility_count() > 0:
                    try:
                        index = int(input("\nEnter facility index to edit (0-{}): ".format(
                            self.manager.get_facility_count() - 1)))
                        facility = self.get_facility_input()
                        if facility and self.manager.update_facility(index, facility):
                            print("\nFacility updated successfully in database.")
                        else:
                            print("\nFailed to update facility.")
                    except ValueError:
                        print("\nPlease enter a valid number.")
                else:
                    print("\nNo facilities to edit.")
            
            elif choice == "6":
                # Delete facility
                if self.manager.get_facility_count() > 0:
                    try:
                        index = int(input("\nEnter facility index to delete (0-{}): ".format(
                            self.manager.get_facility_count() - 1)))
                        if self.manager.remove_facility(index):
                            print("\nFacility deleted successfully from database.")
                        else:
                            print("\nFailed to delete facility.")
                    except ValueError:
                        print("\nPlease enter a valid number.")
                else:
                    print("\nNo facilities to delete.")
            
            elif choice == "7":
                # Sort facilities
                if self.manager.get_facility_count() > 0:
                    self.handle_sorting()
                else:
                    print("\nNo facilities to sort.")
            
            elif choice == "8":
                # Change display format
                self.handle_display_format_change()
            
            elif choice == "9":
                # Exit
                print("\nThank you for using the Facility Management System!")
                print("Program by Huaifang Yin")
                # Disconnect from database if connected
                if DATABASE_AVAILABLE and self.manager.use_database:
                    self.manager.disable_database_mode()
                break
            
            else:
                print("\nInvalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    system = FacilityManagementSystem()
    system.run()
