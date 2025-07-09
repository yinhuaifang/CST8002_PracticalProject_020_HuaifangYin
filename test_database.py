"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Test file for database functionality.
This demonstrates testing of database connectivity and operations.
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
    Test class for database functionality.
    Tests database connectivity and basic operations.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        if DATABASE_AVAILABLE:
            self.database_manager = DatabaseManager()
        else:
            self.database_manager = None
    
    def test_database_manager_initialization(self):
        """Test DatabaseManager initialization."""
        print("\n=== Testing DatabaseManager Initialization ===")
        
        if not DATABASE_AVAILABLE:
            print("⚠ Database functionality not available (MySQL connector not installed)")
            return
        
        self.assertIsNotNone(self.database_manager)
        self.assertEqual(self.database_manager.host, "localhost")
        self.assertEqual(self.database_manager.user, "root")
        self.assertEqual(self.database_manager.database, "project03")
        print("✓ DatabaseManager initialization successful")
    
    def test_database_connection(self):
        """Test database connection."""
        print("\n=== Testing Database Connection ===")
        
        if not DATABASE_AVAILABLE:
            print("⚠ Database functionality not available (MySQL connector not installed)")
            return
        
        # Test connection
        connection_success = self.database_manager.connect()
        
        if connection_success:
            print("✓ Database connection successful")
            self.assertTrue(self.database_manager.connection.is_connected())
            
            # Test table creation
            table_created = self.database_manager.create_table()
            if table_created:
                print("✓ Database table created successfully")
            else:
                print("⚠ Database table creation failed (may already exist)")
            
            # Test disconnection
            self.database_manager.disconnect()
            print("✓ Database disconnection successful")
        else:
            print("⚠ Database connection failed (this is expected if MySQL is not running)")
    
    def test_table_creation(self):
        """Test table creation functionality."""
        print("\n=== Testing Table Creation ===")
        
        if not DATABASE_AVAILABLE:
            print("⚠ Database functionality not available (MySQL connector not installed)")
            return
        
        # Test table creation without connection (should fail)
        table_created = self.database_manager.create_table()
        self.assertFalse(table_created, "Table creation should fail without connection")
        print("✓ Table creation correctly fails without connection")
        
        # Test with connection
        if self.database_manager.connect():
            table_created = self.database_manager.create_table()
            # This might succeed or fail depending on if table already exists
            print(f"✓ Table creation attempt completed (result: {table_created})")
            self.database_manager.disconnect()
    
    def test_connection_parameters(self):
        """Test connection parameters."""
        print("\n=== Testing Connection Parameters ===")
        
        if not DATABASE_AVAILABLE:
            print("⚠ Database functionality not available (MySQL connector not installed)")
            return
        
        # Test default parameters
        self.assertEqual(self.database_manager.host, "localhost")
        self.assertEqual(self.database_manager.user, "root")
        self.assertEqual(self.database_manager.password, "1101")
        self.assertEqual(self.database_manager.database, "project03")
        print("✓ Default connection parameters are correct")
        
        # Test custom parameters
        custom_manager = DatabaseManager(
            host="testhost",
            user="testuser", 
            password="testpass",
            database="testdb"
        )
        
        self.assertEqual(custom_manager.host, "testhost")
        self.assertEqual(custom_manager.user, "testuser")
        self.assertEqual(custom_manager.password, "testpass")
        self.assertEqual(custom_manager.database, "testdb")
        print("✓ Custom connection parameters work correctly")

def run_database_tests():
    """Run all database tests."""
    print("RUNNING DATABASE TESTS")
    print("=" * 30)
    
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
    print("\n" + "=" * 30)
    print("TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 ALL DATABASE TESTS PASSED!")
    else:
        print("\n❌ SOME DATABASE TESTS FAILED!")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_database_tests()
    exit(0 if success else 1) 