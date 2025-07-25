"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project04
Professor: [Tyler DeLay]
Due Date: [Aug 03 2025]
Author: [Huaifang Yin]
Description: Console application demonstrating ASCII art chart functionality.
Provides fallback ASCII art versions of charts for console programs.
"""

import sys
import os
from typing import List, Optional

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from business.business_layer import FacilityManager
from entities.facility_record import FacilityRecord

class ConsoleFacilityApp:
    """
    Console application for Facility Management System with ASCII chart capabilities.
    Demonstrates fallback ASCII art versions of charts for console programs.
    """
    
    def __init__(self):
        """Initialize the console application."""
        self.facility_manager = FacilityManager()
        self.csv_file_path = "data/Nitrogen oxide emissions by facility.csv"
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("FACILITY MANAGEMENT SYSTEM - CONSOLE APPLICATION")
        print("="*60)
        print("1. Display facility count")
        print("2. Show ASCII Province Chart")
        print("3. Show ASCII Year Chart")
        print("4. Show ASCII Top Facilities Chart")
        print("5. Search facilities by province")
        print("6. Search facilities by city")
        print("7. Sort facilities by emissions")
        print("8. Show all available chart types")
        print("0. Exit")
        print("="*60)
    
    def load_data(self):
        """Load data from CSV file."""
        try:
            if os.path.exists(self.csv_file_path):
                records_imported = self.facility_manager.reload_from_csv(self.csv_file_path, max_records=100)
                print(f"Successfully loaded {records_imported} records from CSV file.")
            else:
                print(f"CSV file not found: {self.csv_file_path}")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def show_facility_count(self):
        """Display the total number of facilities."""
        count = self.facility_manager.get_facility_count()
        print(f"Total facilities in database: {count}")
    
    def show_province_chart(self):
        """Show ASCII province chart with different styles."""
        print("\n" + "="*60)
        print("ASCII PROVINCE CHART")
        print("="*60)
        
        # Show bar chart
        print("\n--- Bar Chart Style ---")
        ascii_chart = self.facility_manager.generate_province_ascii_chart(style='bar')
        print(ascii_chart)
        
        # Show line chart
        print("\n--- Line Chart Style ---")
        ascii_chart = self.facility_manager.generate_province_ascii_chart(style='line')
        print(ascii_chart)
        
        # Show histogram
        print("\n--- Histogram Style ---")
        ascii_chart = self.facility_manager.generate_province_ascii_chart(style='histogram')
        print(ascii_chart)
    
    def show_year_chart(self):
        """Show ASCII year chart with different styles."""
        print("\n" + "="*60)
        print("ASCII YEAR CHART")
        print("="*60)
        
        # Show line chart (default for year data)
        print("\n--- Line Chart Style ---")
        ascii_chart = self.facility_manager.generate_year_ascii_chart(style='line')
        print(ascii_chart)
        
        # Show bar chart
        print("\n--- Bar Chart Style ---")
        ascii_chart = self.facility_manager.generate_year_ascii_chart(style='bar')
        print(ascii_chart)
        
        # Show histogram
        print("\n--- Histogram Style ---")
        ascii_chart = self.facility_manager.generate_year_ascii_chart(style='histogram')
        print(ascii_chart)
    
    def show_top_facilities_chart(self):
        """Show ASCII top facilities chart with different configurations."""
        print("\n" + "="*60)
        print("ASCII TOP FACILITIES CHART")
        print("="*60)
        
        # Show top 5 facilities
        print("\n--- Top 5 Facilities (Bar Chart) ---")
        ascii_chart = self.facility_manager.generate_top_facilities_ascii_chart(top_n=5, style='bar')
        print(ascii_chart)
        
        # Show top 10 facilities
        print("\n--- Top 10 Facilities (Bar Chart) ---")
        ascii_chart = self.facility_manager.generate_top_facilities_ascii_chart(top_n=10, style='bar')
        print(ascii_chart)
        
        # Show top 10 facilities as line chart
        print("\n--- Top 10 Facilities (Line Chart) ---")
        ascii_chart = self.facility_manager.generate_top_facilities_ascii_chart(top_n=10, style='line')
        print(ascii_chart)
        
        # Show top 10 facilities as histogram
        print("\n--- Top 10 Facilities (Histogram) ---")
        ascii_chart = self.facility_manager.generate_top_facilities_ascii_chart(top_n=10, style='histogram')
        print(ascii_chart)
    
    def search_by_province(self):
        """Search facilities by province."""
        province = input("Enter province name to search: ").strip()
        if province:
            facilities = self.facility_manager.search_facilities_by_province(province)
            print(f"\nFound {len(facilities)} facilities in {province}:")
            for i, facility in enumerate(facilities[:10]):  # Show first 10
                print(f"{i+1}. {facility.facility_name} - {facility.city}, {facility.province} - Emissions: {facility.emissions}")
            if len(facilities) > 10:
                print(f"... and {len(facilities) - 10} more facilities")
        else:
            print("No province name provided.")
    
    def search_by_city(self):
        """Search facilities by city."""
        city = input("Enter city name to search: ").strip()
        if city:
            facilities = self.facility_manager.search_facilities_by_city(city)
            print(f"\nFound {len(facilities)} facilities in {city}:")
            for i, facility in enumerate(facilities[:10]):  # Show first 10
                print(f"{i+1}. {facility.facility_name} - {facility.city}, {facility.province} - Emissions: {facility.emissions}")
            if len(facilities) > 10:
                print(f"... and {len(facilities) - 10} more facilities")
        else:
            print("No city name provided.")
    
    def sort_by_emissions(self):
        """Sort and display facilities by emissions."""
        print("\n--- Top 10 Facilities by Emissions ---")
        sorted_facilities = self.facility_manager.sort_facilities_by_emissions(reverse=True)
        for i, facility in enumerate(sorted_facilities[:10]):
            print(f"{i+1}. {facility.facility_name} - {facility.city}, {facility.province} - Emissions: {facility.emissions}")
    
    def show_available_chart_types(self):
        """Show all available chart types."""
        chart_types = self.facility_manager.get_available_chart_types()
        print(f"\nAvailable chart types: {', '.join(chart_types)}")
        print("\nChart categories:")
        print("- Province charts: Show emissions aggregated by province")
        print("- Year charts: Show emissions aggregated by year")
        print("- Top facilities charts: Show top facilities by emissions")
        print("\nChart styles:")
        print("- Bar: Traditional bar chart representation")
        print("- Line: Line chart with points and connections")
        print("- Histogram: Bar chart with different character styling")
    
    def run(self):
        """Run the console application."""
        print("Welcome to the Facility Management System Console Application!")
        print("This application demonstrates ASCII art chart functionality.")
        print("Author: Huaifang Yin")
        
        while True:
            try:
                self.display_menu()
                choice = input("Enter your choice (0-9): ").strip()
                
                if choice == '0':
                    print("Thank you for using the Facility Management System!")
                    break
                elif choice == '1':
                    self.show_facility_count()
                elif choice == '2':
                    self.show_province_chart()
                elif choice == '3':
                    self.show_year_chart()
                elif choice == '4':
                    self.show_top_facilities_chart()
                elif choice == '5':
                    self.search_by_province()
                elif choice == '6':
                    self.search_by_city()
                elif choice == '7':
                    self.sort_by_emissions()
                elif choice == '8':
                    self.show_available_chart_types()
                else:
                    print("Invalid choice. Please enter a number between 0 and 8.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nApplication interrupted by user.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                input("Press Enter to continue...")
        
        # Clean up
        self.facility_manager.close_database()

def main():
    """Main function to run the console application."""
    app = ConsoleFacilityApp()
    app.run()

if __name__ == "__main__":
    main() 