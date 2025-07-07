"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Presentation layer for the facility management system.
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import Optional
from business.business_layer import FacilityManager
from persistence.persistence_layer import FileManager
from entities.facility_record import (
    FacilityRecord, StandardFormatFacility
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
    Presentation layer class that handles user interaction and display.
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
    
    def display_facilities(self, facilities: list[FacilityRecord], start: int = 0, count: int = 100):
        """
        Show a list of facilities with pagination.
        Args:
            facilities (list[FacilityRecord]): List of facilities to show
            start (int): Start index
            count (int): Number of facilities to show
        """
        end = min(start + count, len(facilities))
        
        for i in range(start, end):
            print("\n" + "-" * 80)
            print(f"Record {i + 1} of {len(facilities)}")
            print(facilities[i])
            
            # Show author name every 10 records
            if (i + 1) % 10 == 0:
                print("\nProgram by Huaifang Yin")
        
        if end < len(facilities):
            print("\nMore records available. Press Enter to continue...")
            input()
    
    def get_facility_input(self) -> Optional[FacilityRecord]:
        """
        Get facility information from user input.
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
            
            return FacilityRecord(
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
    
    def run(self):
        """Run the main loop of the facility management system."""
      
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-8): ")
            self.display_header()
            if choice == "1":
                # Load data from file
                facilities = self.file_manager.load_facility_data(self.data_file)
                if facilities:
                    self.manager.clear_facilities()
                    for facility in facilities:
                        self.manager.add_facility(facility)
                    print(f"\nLoaded {len(facilities)} facilities successfully.")
                else:
                    print("\nFailed to load facilities. Please check the file.")
            
            elif choice == "2":
                # Save data to file
                if self.manager.get_facility_count() > 0:
                    filename = self.file_manager.save_facility_data(self.manager.facilities)
                    if filename:
                        print(f"\nData saved successfully to {filename}")
                    else:
                        print("\nFailed to save data.")
                else:
                    print("\nNo facilities to save.")
            
            elif choice == "3":
                # Show all facilities
                if self.manager.get_facility_count() > 0:
                    self.display_facilities(self.manager.facilities, start=0, count=3)
                else:
                    print("\nNo facilities to display.")
            
            elif choice == "4":
                # Show a single facility
                if self.manager.get_facility_count() > 0:
                    try:
                        index = int(input("\nEnter facility index (0-{}): ".format(
                            self.manager.get_facility_count() - 1)))
                        facility = self.manager.get_facility(index)
                        if facility:
                            print("\n" + "-" * 80)
                            print(facility)
                        else:
                            print("\nInvalid facility index.")
                    except ValueError:
                        print("\nPlease enter a valid number.")
                else:
                    print("\nNo facilities to display.")
            
            elif choice == "5":
                # Add a new facility
                facility = self.get_facility_input()
                if facility:
                    self.manager.add_facility(facility)
                    print("\nFacility added successfully.")
            
            elif choice == "6":
                # Edit a facility
                if self.manager.get_facility_count() > 0:
                    try:
                        index = int(input("\nEnter facility index to edit (0-{}): ".format(
                            self.manager.get_facility_count() - 1)))
                        facility = self.get_facility_input()
                        if facility and self.manager.update_facility(index, facility):
                            print("\nFacility updated successfully.")
                        else:
                            print("\nFailed to update facility.")
                    except ValueError:
                        print("\nPlease enter a valid number.")
                else:
                    print("\nNo facilities to edit.")
            
            elif choice == "7":
                # Delete a facility
                if self.manager.get_facility_count() > 0:
                    try:
                        index = int(input("\nEnter facility index to delete (0-{}): ".format(
                            self.manager.get_facility_count() - 1)))
                        if self.manager.remove_facility(index):
                            print("\nFacility deleted successfully.")
                        else:
                            print("\nFailed to delete facility.")
                    except ValueError:
                        print("\nPlease enter a valid number.")
                else:
                    print("\nNo facilities to delete.")
            
            elif choice == "8":
                # Exit
                print("\nThank you for using the Facility Management System!")
                break
            
            else:
                print("\nInvalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    system = FacilityManagementSystem()
    system.run()
