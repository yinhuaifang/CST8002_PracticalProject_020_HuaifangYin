"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project02
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [May 25  2025]
Author: [Huaifang Yin]
Description: Unit tests for the business layer.
"""

import unittest
from business_layer import FacilityManager
from facility_record import FacilityRecord

class TestFacilityManager(unittest.TestCase):
    """Test cases for the FacilityManager class."""
    
    def setUp(self):
        """Set up before each test method."""
        self.manager = FacilityManager()
        self.test_facility = FacilityRecord(
            npri_id="12345",
            facility_name="Test Facility",
            company_name="Test Company",
            address="123 Test St",
            city="Test City",
            province="ON",
            postal_code="A1A 1A1",
            latitude=45.0,
            longitude=-75.0,
            emissions=100.0,
            units="tonnes",
            facility_details="http://test.com",
            facility_information="http://test.com/info",
            report_year=2023
        )
    
    def test_add_facility(self):
        """Test adding a facility."""
        self.manager.add_facility(self.test_facility)
        self.assertEqual(self.manager.get_facility_count(), 1)
        self.assertEqual(self.manager.get_facility(0), self.test_facility)
    
    def test_remove_facility(self):
        """Test removing a facility."""
        self.manager.add_facility(self.test_facility)
        self.assertTrue(self.manager.remove_facility(0))
        self.assertEqual(self.manager.get_facility_count(), 0)
    
    def test_update_facility(self):
        """Test updating a facility."""
        self.manager.add_facility(self.test_facility)
        updated_facility = FacilityRecord(
            npri_id="12345",
            facility_name="Updated Facility",
            company_name="Test Company",
            address="123 Test St",
            city="Test City",
            province="ON",
            postal_code="A1A 1A1",
            latitude=45.0,
            longitude=-75.0,
            emissions=100.0,
            units="tonnes",
            facility_details="http://test.com",
            facility_information="http://test.com/info",
            report_year=2023
        )
        self.assertTrue(self.manager.update_facility(0, updated_facility))
        self.assertEqual(self.manager.get_facility(0).facility_name, "Updated Facility")
    
    def test_invalid_index_operations(self):
        """Test operations with invalid indices."""
        self.assertFalse(self.manager.remove_facility(0))
        self.assertFalse(self.manager.update_facility(0, self.test_facility))
        self.assertIsNone(self.manager.get_facility(0))
    
    def test_clear_facilities(self):
        """Test clearing all facilities."""
        self.manager.add_facility(self.test_facility)
        self.manager.add_facility(self.test_facility)
        self.manager.clear_facilities()
        self.assertEqual(self.manager.get_facility_count(), 0)

if __name__ == '__main__':
    unittest.main() 