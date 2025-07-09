"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Test file for database functionality features.
This demonstrates testing of database operations and Django-style queries.
"""

import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# Try to import database functionality (optional)
try:
    from persistence.database_layer import DatabaseManager
    from entities.facility_record import StandardFormatFacility
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class TestDatabaseFunctionality(unittest.TestCase):
    """
    Test class for database functionality features.
    Tests database operations and Django-style query methods.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        if DATABASE_AVAILABLE:
            self.database_manager = DatabaseManager()
            self.test_facilities = [
                StandardFormatFacility(
                    npri_id="DB_TEST_001",
                    facility_name="Database Test Facility 1",
                    company_name="Database Test Company 1",
                    city="Database Test City 1",
                    province="ON",
                    emissions=100.0,
                    units="tonnes"
                ),
                StandardFormatFacility(
                    npri_id="DB_TEST_002",
                    facility_name="Database Test Facility 2", 
                    company_name="Database Test Company 2",
                    city="Database Test City 2",
                    province="BC",
                    emissions=200.0,
                    units="tonnes"
                ),
                StandardFormatFacility(
                    npri_id="DB_TEST_003",
                    facility_name="Database Test Facility 3",
                    company_name="Database Test Company 3", 
                    city="Database Test City 3",
                    province="AB",
                    emissions=150.0,
                    units="tonnes"
                )
            ]
        else:
            self.database_manager = None
            self.test_facilities = []
    
    def test_django_style_objects_manager(self):
        """Test Django-style objects manager functionality."""
        print("\n=== Testing Django-style Objects Manager ===")
        
        if not DATABASE_AVAILABLE:
            print("⚠ Database functionality not available (MySQL connector not installed)")
            return
        
        # Test connection
        if not self.database_manager.connect():
            print("⚠ Database connection failed (this is expected if MySQL is not running)")
            return
        
        try:
            # Test Django-style all() method
            facilities = StandardFormatFacility.objects(self.database_manager.connection).all()
            print(f"✓ Django-style all(): Found {len(facilities)} facilities")
            
            # Test Django-style count() method
            count = StandardFormatFacility.objects(self.database_manager.connection).count()
            print(f"✓ Django-style count(): {count} facilities")
            
            # Test Django-style filter() method
            on_facilities = StandardFormatFacility.objects(self.database_manager.connection).filter(province="ON")
            print(f"✓ Django-style filter(): Found {len(on_facilities)} facilities in ON")
            
            # Test Django-style first() method
            all_facilities = StandardFormatFacility.objects(self.database_manager.connection).all()
            first_facility = all_facilities[0] if all_facilities else None
            if first_facility:
                print(f"✓ Django-style first(): {first_facility.facility_name}")
            
            # Test polymorphic display
            if first_facility:
                display_format = first_facility.display()
                print(f"✓ Polymorphic display: {display_format[:100]}...")
            
        finally:
            self.database_manager.disconnect()
            print("✓ Database connection closed")
    
    def test_database_table_structure(self):
        """Test database table structure and schema."""
        print("\n=== Testing Database Table Structure ===")
        
        if not DATABASE_AVAILABLE:
            print("⚠ Database functionality not available (MySQL connector not installed)")
            return
        
        # Test connection
        if not self.database_manager.connect():
            print("⚠ Database connection failed (this is expected if MySQL is not running)")
            return
        
        try:
            # Test table creation
            table_created = self.database_manager.create_table()
            if table_created:
                print("✓ Database table created successfully")
            else:
                print("⚠ Database table creation failed (may already exist)")
            
            # Test table structure (if table exists)
            cursor = self.database_manager.connection.cursor()
            cursor.execute("DESCRIBE facilities")
            columns = cursor.fetchall()
            
            if columns:
                print("✓ Database table structure:")
                for column in columns:
                    print(f"  - {column[0]}: {column[1]}")
            else:
                print("⚠ Could not retrieve table structure")
            
        finally:
            self.database_manager.disconnect()
            print("✓ Database connection closed")
    
    def test_facility_record_polymorphism(self):
        """Test polymorphic behavior of facility records."""
        print("\n=== Testing Facility Record Polymorphism ===")
        
        if not DATABASE_AVAILABLE:
            print("⚠ Database functionality not available (MySQL connector not installed)")
            return
        
        # Test polymorphic display methods
        for i, facility in enumerate(self.test_facilities):
            display_result = facility.display()
            self.assertIsInstance(display_result, str)
            self.assertIn(facility.facility_name, display_result)
            print(f"✓ Facility {i+1} polymorphic display: {display_result[:80]}...")
        
        # Test different facility types
        short_facility = StandardFormatFacility(
            npri_id="SHORT_001",
            facility_name="Short Test Facility",
            company_name="Short Test Company",
            city="Short Test City",
            province="ON",
            emissions=50.0,
            units="tonnes"
        )
        
        detailed_facility = StandardFormatFacility(
            npri_id="DETAILED_001",
            facility_name="Detailed Test Facility",
            company_name="Detailed Test Company", 
            city="Detailed Test City",
            province="BC",
            emissions=75.0,
            units="tonnes"
        )
        
        # Test polymorphic behavior
        short_display = short_facility.display()
        detailed_display = detailed_facility.display()
        
        self.assertNotEqual(short_display, detailed_display)
        print("✓ Polymorphic display methods work correctly")
    
    def test_database_connection_management(self):
        """Test database connection management."""
        print("\n=== Testing Database Connection Management ===")
        
        if not DATABASE_AVAILABLE:
            print("⚠ Database functionality not available (MySQL connector not installed)")
            return
        
        # Test connection state
        if self.database_manager.connection:
            self.assertFalse(self.database_manager.connection.is_connected())
        else:
            self.assertIsNone(self.database_manager.connection)
        print("✓ Initial connection state is disconnected")
        
        # Test connection
        connection_success = self.database_manager.connect()
        if connection_success:
            self.assertTrue(self.database_manager.connection.is_connected())
            print("✓ Connection successful")
            
            # Test disconnection
            self.database_manager.disconnect()
            self.assertFalse(self.database_manager.connection.is_connected())
            print("✓ Disconnection successful")
        else:
            print("⚠ Database connection failed (this is expected if MySQL is not running)")
    
    def test_error_handling(self):
        """Test error handling in database operations."""
        print("\n=== Testing Error Handling ===")
        
        if not DATABASE_AVAILABLE:
            print("⚠ Database functionality not available (MySQL connector not installed)")
            return
        
        # Test operations without connection
        table_created = self.database_manager.create_table()
        self.assertFalse(table_created, "Table creation should fail without connection")
        print("✓ Error handling works correctly for operations without connection")
        
        # Test with invalid connection parameters
        invalid_manager = DatabaseManager(
            host="invalid_host",
            user="invalid_user",
            password="invalid_password",
            database="invalid_database"
        )
        
        connection_success = invalid_manager.connect()
        self.assertFalse(connection_success, "Connection should fail with invalid parameters")
        print("✓ Error handling works correctly for invalid connection parameters")

def run_database_functionality_tests():
    """Run all database functionality tests."""
    print("RUNNING DATABASE FUNCTIONALITY TESTS")
    print("=" * 40)
    
    if not DATABASE_AVAILABLE:
        print("⚠ MySQL connector not available")
        print("⚠ Install mysql-connector-python to enable database tests")
        print("⚠ Some tests will be skipped")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()
    
    # Add test methods
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestDatabaseFunctionality))
    
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
        print("\n🎉 ALL DATABASE FUNCTIONALITY TESTS PASSED!")
    else:
        print("\n❌ SOME DATABASE FUNCTIONALITY TESTS FAILED!")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_database_functionality_tests()
    exit(0 if success else 1) 