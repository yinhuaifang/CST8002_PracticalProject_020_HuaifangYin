"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project01
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [May 25  2025]
Author: [Huaifang Yin]
Description: This program reads and analyzes nitrogen oxide emissions data from Canadian facilities.
It loads data from a CSV file, creates FacilityRecord objects, and displays the information.
"""

from file_operations import load_facility_data

def display_facilities(facilities):
    """
    Display information about facilities in the console.
    
    Args:
        facilities (list): List of FacilityRecord objects to display
    """    
    for facility in facilities:
        print("-" * 80)
        print(facility)

def main():
    """Main program function."""
    # Display author name
    version = "1.0"
    print("Nitrogen Oxide Emissions Analyzer")
    print("Created by: Huaifang Yin")
    print(f"Version: {version}")
    
    # Load data from CSV file
    filename = "Nitrogen oxide emissions by facility.csv"
    facilities = load_facility_data(filename, 5)
    
    if facilities:
        print(f"\nLoaded {len(facilities)} facility records:\n")
        display_facilities(facilities)
    else:
        print("No facility data was loaded. Please check the input file.")
if __name__ == "__main__":
    main()
