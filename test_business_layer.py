"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Test file for the business layer functionality.
This demonstrates testing of the FacilityManager class and its methods.
"""

import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from business.business_layer import FacilityManager
from entities.facility_record import FacilityRecord

# Try to import database functionality (optional)
try:
    from persistence.database_layer import DatabaseManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class TestBusinessLayer(unittest.TestCase):
    """
    Test class for the business layer functionality.
    Tests the FacilityManager class and its methods.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = FacilityManager()
        
        # Set up database manager if available
        if DATABASE_AVAILABLE:
            self.database_manager = DatabaseManager()
            self.manager.set_database_manager(self.database_manager)
    
    def test_facility_manager_initialization(self):
        """Test FacilityManager initialization."""
        print("\n=== Testing FacilityManager Initialization ===")
        
        self.assertIsNotNone(self.manager)
        self.assertEqual(self.manager.get_facility_count(), 0)
        self.assertTrue(self.manager.use_database)
        self.assertIsNotNone(self.manager.current_format_class)
        
        print("✓ FacilityManager initialization successful")
    
    def test_facility_creation(self):
        """Test facility creation with different formats."""
        print("\n=== Testing Facility Creation ===")
        
        # Test short format
        self.manager.change_display_format("short")
        short_facility = self.manager.create_facility_with_format(
            npri_id="TEST001",
            facility_name="Test Facility",
            company_name="Test Company",
            address="123 Test St",
            city="Test City",
            province="Test Province",
            postal_code="A1A 1A1",
            latitude=45.0,
            longitude=-75.0,
            emissions=100.0,
            units="tonnes",
            facility_details="http://test.com",
            facility_information="http://test-info.com",
            report_year=2023
        )
        
        self.assertIsInstance(short_facility, FacilityRecord)
        self.assertEqual(short_facility.facility_name, "Test Facility")
        self.assertEqual(short_facility.emissions, 100.0)
        print("✓ Short format facility creation successful")
        
        # Test detailed format
        self.manager.change_display_format("detailed")
        detailed_facility = self.manager.create_facility_with_format(
            npri_id="TEST002",
            facility_name="Test Facility 2",
            company_name="Test Company",
            address="456 Test Ave",
            city="Test City",
            province="Test Province",
            postal_code="B2B 2B2",
            latitude=46.0,
            longitude=-76.0,
            emissions=200.0,
            units="tonnes",
            facility_details="http://test.com",
            facility_information="http://test-info.com",
            report_year=2023
        )
        
        self.assertIsInstance(detailed_facility, FacilityRecord)
        self.assertEqual(detailed_facility.facility_name, "Test Facility 2")
        print("✓ Detailed format facility creation successful")
        
        # Test standard format
        self.manager.change_display_format("standard")
        standard_facility = self.manager.create_facility_with_format(
            npri_id="TEST003",
            facility_name="Test Facility 3",
            company_name="Test Company",
            address="789 Test Blvd",
            city="Test City",
            province="Test Province",
            postal_code="C3C 3C3",
            latitude=47.0,
            longitude=-77.0,
            emissions=300.0,
            units="tonnes",
            facility_details="http://test.com",
            facility_information="http://test-info.com",
            report_year=2023
        )
        
        self.assertIsInstance(standard_facility, FacilityRecord)
        self.assertEqual(standard_facility.facility_name, "Test Facility 3")
        print("✓ Standard format facility creation successful")
    
    def test_crud_operations(self):
        """Test CRUD operations."""
        print("\n=== Testing CRUD Operations ===")
        
        # Create
        facility = self.manager.create_facility_with_format(
            npri_id="CRUD001",
            facility_name="CRUD Test",
            company_name="Test Company",
            address="Test Address",
            city="Test City",
            province="Test Province",
            postal_code="Test",
            latitude=0.0,
            longitude=0.0,
            emissions=100.0,
            units="tonnes",
            facility_details="",
            facility_information="",
            report_year=2023
        )
        self.manager.add_facility(facility)
        
        # Read
        self.assertEqual(self.manager.get_facility_count(), 1)
        retrieved = self.manager.get_facility(0)
        self.assertEqual(retrieved.facility_name, "CRUD Test")
        print("✓ Create and Read operations successful")
        
        # Update
        updated_facility = self.manager.create_facility_with_format(
            npri_id="CRUD001",
            facility_name="Updated CRUD Test",
            company_name="Test Company",
            address="Test Address",
            city="Test City",
            province="Test Province",
            postal_code="Test",
            latitude=0.0,
            longitude=0.0,
            emissions=150.0,
            units="tonnes",
            facility_details="",
            facility_information="",
            report_year=2023
        )
        success = self.manager.update_facility(0, updated_facility)
        self.assertTrue(success)
        
        retrieved = self.manager.get_facility(0)
        self.assertEqual(retrieved.facility_name, "Updated CRUD Test")
        self.assertEqual(retrieved.emissions, 150.0)
        print("✓ Update operation successful")
        
        # Delete
        success = self.manager.remove_facility(0)
        self.assertTrue(success)
        self.assertEqual(self.manager.get_facility_count(), 0)
        print("✓ Delete operation successful")
    
    def test_sorting_operations(self):
        """Test sorting operations."""
        print("\n=== Testing Sorting Operations ===")
        
        # Add test facilities
        facilities = [
            self.manager.create_facility_with_format(
                npri_id="SORT001", facility_name="Alpha", emissions=100.0,
                company_name="Test", address="Test", city="Test", province="Test",
                postal_code="Test", latitude=0.0, longitude=0.0, units="tonnes",
                facility_details="", facility_information="", report_year=2023
            ),
            self.manager.create_facility_with_format(
                npri_id="SORT002", facility_name="Beta", emissions=50.0,
                company_name="Test", address="Test", city="Test", province="Test",
                postal_code="Test", latitude=0.0, longitude=0.0, units="tonnes",
                facility_details="", facility_information="", report_year=2023
            ),
            self.manager.create_facility_with_format(
                npri_id="SORT003", facility_name="Gamma", emissions=200.0,
                company_name="Test", address="Test", city="Test", province="Test",
                postal_code="Test", latitude=0.0, longitude=0.0, units="tonnes",
                facility_details="", facility_information="", report_year=2023
            )
        ]
        
        for facility in facilities:
            self.manager.add_facility(facility)
        
        # Test sorting by name
        self.manager.sort_facilities_by_name(reverse=False)
        facilities_list = self.manager.facilities
        self.assertEqual(facilities_list[0].facility_name, "Alpha")
        self.assertEqual(facilities_list[1].facility_name, "Beta")
        self.assertEqual(facilities_list[2].facility_name, "Gamma")
        print("✓ Sorting by name (A-Z) successful")
        
        # Test sorting by emissions
        self.manager.sort_facilities_by_emissions(reverse=False)
        facilities_list = self.manager.facilities
        self.assertEqual(facilities_list[0].emissions, 50.0)
        self.assertEqual(facilities_list[1].emissions, 100.0)
        self.assertEqual(facilities_list[2].emissions, 200.0)
        print("✓ Sorting by emissions (low to high) successful")
        
        # Test reverse sorting
        self.manager.sort_facilities_by_name(reverse=True)
        facilities_list = self.manager.facilities
        self.assertEqual(facilities_list[0].facility_name, "Gamma")
        self.assertEqual(facilities_list[1].facility_name, "Beta")
        self.assertEqual(facilities_list[2].facility_name, "Alpha")
        print("✓ Reverse sorting successful")
    
    def test_display_format_changes(self):
        """Test display format changes."""
        print("\n=== Testing Display Format Changes ===")
        
        # Test changing to short format
        format_name = self.manager.change_display_format("short")
        self.assertIn("Short", format_name)
        print(f"✓ Changed to {format_name}")
        
        # Test changing to detailed format
        format_name = self.manager.change_display_format("detailed")
        self.assertIn("Detailed", format_name)
        print(f"✓ Changed to {format_name}")
        
        # Test changing to standard format
        format_name = self.manager.change_display_format("standard")
        self.assertIn("Standard", format_name)
        print(f"✓ Changed to {format_name}")
        
        # Test getting current format name
        current_format = self.manager.get_current_format_name()
        self.assertIsInstance(current_format, str)
        print(f"✓ Current format: {current_format}")

def run_business_layer_tests():
    """Run all business layer tests."""
    print("RUNNING BUSINESS LAYER TESTS")
    print("=" * 40)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()
    
    # Add test methods
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestBusinessLayer))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 ALL BUSINESS LAYER TESTS PASSED!")
    else:
        print("\n❌ SOME BUSINESS LAYER TESTS FAILED!")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_business_layer_tests()
    exit(0 if success else 1) 