"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project04
Professor: [Tyler DeLay]
Due Date: [Aug 03 2025]
Author: [Huaifang Yin]
Description: Test script to verify ASCII chart functionality.
"""

import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from business.business_layer import FacilityManager
from business.ascii_chart_generator import ASCIIChartGenerator

def test_ascii_chart_generator():
    """Test the ASCII chart generator directly."""
    print("Testing ASCII Chart Generator...")
    
    # Create a test facility manager
    facility_manager = FacilityManager()
    
    # Load some test data
    csv_file_path = "data/Nitrogen oxide emissions by facility.csv"
    if os.path.exists(csv_file_path):
        records_imported = facility_manager.reload_from_csv(csv_file_path, max_records=50)
        print(f"Loaded {records_imported} test records")
        
        # Test province chart
        print("\n" + "="*60)
        print("TESTING PROVINCE CHART")
        print("="*60)
        ascii_chart = facility_manager.generate_province_ascii_chart(style='bar')
        print(ascii_chart)
        
        # Test year chart
        print("\n" + "="*60)
        print("TESTING YEAR CHART")
        print("="*60)
        ascii_chart = facility_manager.generate_year_ascii_chart(style='line')
        print(ascii_chart)
        
        # Test top facilities chart
        print("\n" + "="*60)
        print("TESTING TOP FACILITIES CHART")
        print("="*60)
        ascii_chart = facility_manager.generate_top_facilities_ascii_chart(top_n=5, style='bar')
        print(ascii_chart)
        
        print("\n" + "="*60)
        print("ASCII CHART FUNCTIONALITY TEST COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    else:
        print(f"CSV file not found: {csv_file_path}")
        print("Please ensure the data file exists for testing.")
    
    # Clean up
    facility_manager.close_database()

def test_chart_types():
    """Test all available chart types."""
    print("\nTesting all chart types...")
    
    generator = ASCIIChartGenerator()
    chart_types = generator.get_available_chart_types()
    print(f"Available chart types: {chart_types}")
    
    # Test with empty data
    from entities.facility_record import FacilityRecord
    empty_facilities = []
    
    print("\nTesting with empty data:")
    result = generator.generate_province_chart(empty_facilities)
    print(f"Province chart result: {result}")
    
    result = generator.generate_year_chart(empty_facilities)
    print(f"Year chart result: {result}")
    
    result = generator.generate_top_facilities_chart(empty_facilities)
    print(f"Top facilities chart result: {result}")

if __name__ == "__main__":
    print("ASCII Chart Functionality Test")
    print("Author: Huaifang Yin")
    print("="*60)
    
    try:
        test_chart_types()
        test_ascii_chart_generator()
        print("\nAll tests completed successfully!")
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc() 