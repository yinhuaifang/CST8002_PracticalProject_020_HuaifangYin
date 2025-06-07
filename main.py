"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project02
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [May 25  2025]
Author: [Huaifang Yin]
Description: Presentation layer for the facility management system.
"""

import os
from typing import Optional
from business_layer import FacilityManager
from persistence_layer import FileManager
from facility_record import FacilityRecord

class FacilityManagementSystem:
    """
    Presentation layer class that handles user interaction and display.
    """
    
    def __init__(self):
        """Initialize the facility management system."""
        self.manager = FacilityManager()
        self.file_manager = FileManager()
        self.data_file = "Nitrogen oxide emissions by facility.csv"
    
    def display_header(self):
        """Show the program header and author info."""
        print("\n" + "=" * 80)
        print("Facility Management System")
        print("Created by: Huaifang Yin")
        print("=" * 80 + "\n")
    
    def display_menu(self):
        """Show the main menu options."""
        print("\nMain Menu:")
        print("1. Load data from file")
        print("2. Save data to file")
        print("3. Display all facilities")
        print("4. Display single facility")
        print("5. Add new facility")
        print("6. Edit facility")
        print("7. Delete facility")
        print("8. Exit")
    
    def display_facilities(self, facilities: list[FacilityRecord], start: int = 0, count: int = 10):
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
                    self.display_facilities(self.manager.facilities)
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
