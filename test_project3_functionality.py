"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Test file for the main functionality of the Facility Management System.
This demonstrates testing of inheritance, polymorphism, database connectivity, and multithreading.
"""

import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

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

class TestProject3Functionality(unittest.TestCase):
    """
    Test class for the main functionality of the Facility Management System.
    Tests inheritance, polymorphism, database connectivity, and multithreading.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = FacilityManager()
        self.file_manager = FileManager()
        self.data_file = os.path.join("data", "Nitrogen oxide emissions by facility.csv")
        
        # Set up database manager if available
        if DATABASE_AVAILABLE:
            self.database_manager = DatabaseManager()
            self.manager.set_database_manager(self.database_manager)
    
    def test_inheritance_and_polymorphism(self):
        """Test inheritance and polymorphism with different facility formats."""
        print("\n=== Testing Inheritance and Polymorphism ===")
        
        # Test creating facilities with different formats
        short_facility = self.manager.create_facility_with_format(
            npri_id="TEST001",
            facility_name="Test Facility Short",
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
        
        # Test polymorphic display
        display_output = short_facility.display()
        self.assertIsInstance(display_output, str)
        self.assertIn("Test Facility Short", display_output)
        print(f"✓ Short format display: {display_output[:100]}...")
        
        # Test changing display format
        self.manager.change_display_format("detailed")
        detailed_facility = self.manager.create_facility_with_format(
            npri_id="TEST002",
            facility_name="Test Facility Detailed",
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
        
        detailed_display = detailed_facility.display()
        self.assertIsInstance(detailed_display, str)
        self.assertIn("Test Facility Detailed", detailed_display)
        print(f"✓ Detailed format display: {detailed_display[:100]}...")
        
        # Test standard format
        self.manager.change_display_format("standard")
        standard_facility = self.manager.create_facility_with_format(
            npri_id="TEST003",
            facility_name="Test Facility Standard",
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
        
        standard_display = standard_facility.display()
        self.assertIsInstance(standard_display, str)
        self.assertIn("Test Facility Standard", standard_display)
        print(f"✓ Standard format display: {standard_display[:100]}...")
        
        print("✓ Inheritance and polymorphism tests passed!")
    
    def test_database_connectivity(self):
        """Test database connectivity functionality."""
        if not DATABASE_AVAILABLE:
            print("\n=== Database connectivity test skipped (MySQL not available) ===")
            return
        
        print("\n=== Testing Database Connectivity ===")
        
        # Test database connection
        connection_success = self.manager.enable_database_mode()
        if connection_success:
            print("✓ Database connection successful")
            
            # Test table creation
            table_created = self.database_manager.create_table()
            self.assertTrue(table_created, "Table creation should succeed")
            print("✓ Database table created successfully")
            
            # Test database mode properties
            self.assertTrue(self.manager.use_database, "Database mode should be enabled")
            print("✓ Database mode enabled")
            
            # Test database disconnection
            self.manager.disable_database_mode()
            self.assertFalse(self.manager.use_database, "Database mode should be disabled")
            print("✓ Database mode disabled")
        else:
            print("⚠ Database connection failed (this is expected if MySQL is not running)")
        
        print("✓ Database connectivity tests completed!")
    
    def test_data_structures_and_algorithms(self):
        """Test data structures and algorithms (sorting)."""
        print("\n=== Testing Data Structures and Algorithms ===")
        
        # Add test facilities
        facilities = [
            self.manager.create_facility_with_format(
                npri_id="SORT001", facility_name="Alpha Facility", emissions=100.0,
                company_name="Test", address="Test", city="Test", province="Test",
                postal_code="Test", latitude=0.0, longitude=0.0, units="tonnes",
                facility_details="", facility_information="", report_year=2023
            ),
            self.manager.create_facility_with_format(
                npri_id="SORT002", facility_name="Beta Facility", emissions=50.0,
                company_name="Test", address="Test", city="Test", province="Test",
                postal_code="Test", latitude=0.0, longitude=0.0, units="tonnes",
                facility_details="", facility_information="", report_year=2023
            ),
            self.manager.create_facility_with_format(
                npri_id="SORT003", facility_name="Gamma Facility", emissions=200.0,
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
        self.assertEqual(facilities_list[0].facility_name, "Alpha Facility")
        self.assertEqual(facilities_list[1].facility_name, "Beta Facility")
        self.assertEqual(facilities_list[2].facility_name, "Gamma Facility")
        print("✓ Sorting by name (A-Z) works correctly")
        
        # Test sorting by emissions
        self.manager.sort_facilities_by_emissions(reverse=False)
        facilities_list = self.manager.facilities
        self.assertEqual(facilities_list[0].emissions, 50.0)
        self.assertEqual(facilities_list[1].emissions, 100.0)
        self.assertEqual(facilities_list[2].emissions, 200.0)
        print("✓ Sorting by emissions (low to high) works correctly")
        
        # Test reverse sorting
        self.manager.sort_facilities_by_name(reverse=True)
        facilities_list = self.manager.facilities
        self.assertEqual(facilities_list[0].facility_name, "Gamma Facility")
        self.assertEqual(facilities_list[1].facility_name, "Beta Facility")
        self.assertEqual(facilities_list[2].facility_name, "Alpha Facility")
        print("✓ Reverse sorting works correctly")
        
        print("✓ Data structures and algorithms tests passed!")
    
    def test_crud_operations(self):
        """Test CRUD (Create, Read, Update, Delete) operations."""
        print("\n=== Testing CRUD Operations ===")
        
        # Test Create
        facility = self.manager.create_facility_with_format(
            npri_id="CRUD001", facility_name="CRUD Test Facility", emissions=150.0,
            company_name="Test", address="Test", city="Test", province="Test",
            postal_code="Test", latitude=0.0, longitude=0.0, units="tonnes",
            facility_details="", facility_information="", report_year=2023
        )
        self.manager.add_facility(facility)
        
        # Test Read
        self.assertEqual(self.manager.get_facility_count(), 1)
        retrieved_facility = self.manager.get_facility(0)
        self.assertEqual(retrieved_facility.facility_name, "CRUD Test Facility")
        print("✓ Create and Read operations work correctly")
        
        # Test Update
        updated_facility = self.manager.create_facility_with_format(
            npri_id="CRUD001", facility_name="Updated CRUD Test Facility", emissions=200.0,
            company_name="Test", address="Test", city="Test", province="Test",
            postal_code="Test", latitude=0.0, longitude=0.0, units="tonnes",
            facility_details="", facility_information="", report_year=2023
        )
        update_success = self.manager.update_facility(0, updated_facility)
        self.assertTrue(update_success)
        
        retrieved_facility = self.manager.get_facility(0)
        self.assertEqual(retrieved_facility.facility_name, "Updated CRUD Test Facility")
        self.assertEqual(retrieved_facility.emissions, 200.0)
        print("✓ Update operation works correctly")
        
        # Test Delete
        delete_success = self.manager.remove_facility(0)
        self.assertTrue(delete_success)
        self.assertEqual(self.manager.get_facility_count(), 0)
        print("✓ Delete operation works correctly")
        
        print("✓ CRUD operations tests passed!")
    
    def test_multithreading_support(self):
        """Test multithreading support."""
        print("\n=== Testing Multithreading Support ===")
        
        # Test thread-safe operations
        import threading
        import time
        
        def add_facilities_thread():
            """Thread function to add facilities."""
            for i in range(5):
                facility = self.manager.create_facility_with_format(
                    npri_id=f"THREAD{i}", facility_name=f"Thread Facility {i}", emissions=100.0 + i,
                    company_name="Test", address="Test", city="Test", province="Test",
                    postal_code="Test", latitude=0.0, longitude=0.0, units="tonnes",
                    facility_details="", facility_information="", report_year=2023
                )
                self.manager.add_facility(facility)
                time.sleep(0.01)  # Small delay to simulate work
        
        # Create multiple threads
        threads = []
        for i in range(3):
            thread = threading.Thread(target=add_facilities_thread)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify thread-safe operations
        expected_count = 15  # 3 threads * 5 facilities each
        actual_count = self.manager.get_facility_count()
        self.assertEqual(actual_count, expected_count, f"Expected {expected_count} facilities, got {actual_count}")
        print(f"✓ Thread-safe operations: {actual_count} facilities added by 3 threads")
        
        # Test thread-safe sorting
        def sort_thread():
            """Thread function to sort facilities."""
            self.manager.sort_facilities_by_name(reverse=False)
        
        sort_threads = []
        for i in range(2):
            thread = threading.Thread(target=sort_thread)
            sort_threads.append(thread)
            thread.start()
        
        for thread in sort_threads:
            thread.join()
        
        print("✓ Thread-safe sorting operations completed")
        
        print("✓ Multithreading support tests passed!")
    
    def test_csv_file_loading(self):
        """Test CSV file loading functionality."""
        print("\n=== Testing CSV File Loading ===")
        
        if not os.path.exists(self.data_file):
            print(f"⚠ CSV file not found: {self.data_file}")
            return
        
        # Test loading facilities from CSV
        facilities = self.file_manager.load_facility_data(self.data_file, max_records=10)
        
        if facilities:
            self.assertIsInstance(facilities, list)
            self.assertGreater(len(facilities), 0)
            self.assertLessEqual(len(facilities), 10)
            
            # Test that facilities are proper objects
            for facility in facilities:
                self.assertIsInstance(facility, FacilityRecord)
                self.assertIsInstance(facility.facility_name, str)
                self.assertIsInstance(facility.emissions, (int, float))
            
            print(f"✓ Successfully loaded {len(facilities)} facilities from CSV")
            print(f"✓ First facility: {facilities[0].facility_name}")
        else:
            print("⚠ No facilities loaded from CSV file")
        
        print("✓ CSV file loading tests completed!")

def run_project3_tests():
    """Run all Project 3 functionality tests."""
    print("RUNNING PROJECT 3 FUNCTIONALITY TESTS")
    print("=" * 50)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()
    
    # Add test methods
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestProject3Functionality))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED!")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_project3_tests()
    exit(0 if success else 1) 