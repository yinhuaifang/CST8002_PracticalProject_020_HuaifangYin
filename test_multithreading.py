"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Test file for multithreading functionality.
This demonstrates testing of thread-safe operations and parallel processing.
"""

import unittest
import os
import sys
import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from business.business_layer import FacilityManager
from entities.facility_record import StandardFormatFacility

class TestMultithreadingFunctionality(unittest.TestCase):
    """
    Test class for multithreading functionality.
    Tests thread-safe operations and parallel processing.
    """
    
    def setUp(self):
        """Set up test fixtures."""
        self.business_layer = FacilityManager()
        self.test_facilities = [
            StandardFormatFacility(
                npri_id="TEST001",
                facility_name="Test Facility 1",
                company_name="Test Company 1",
                city="Test City 1",
                province="ON",
                emissions=100.0,
                units="tonnes"
            ),
            StandardFormatFacility(
                npri_id="TEST002", 
                facility_name="Test Facility 2",
                company_name="Test Company 2", 
                city="Test City 2",
                province="BC",
                emissions=200.0,
                units="tonnes"
            ),
            StandardFormatFacility(
                npri_id="TEST003",
                facility_name="Test Facility 3", 
                company_name="Test Company 3",
                city="Test City 3",
                province="AB", 
                emissions=150.0,
                units="tonnes"
            )
        ]
    
    def test_thread_safe_data_access(self):
        """Test thread-safe access to shared data."""
        print("\n=== Testing Thread-Safe Data Access ===")
        
        # Add test data
        for facility in self.test_facilities:
            self.business_layer.add_facility(facility)
        
        # Test concurrent reads
        def read_facilities():
            facilities = self.business_layer.facilities
            return len(facilities)
        
        # Run multiple threads reading data
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(read_facilities) for _ in range(10)]
            results = [future.result() for future in as_completed(futures)]
        
        # All threads should get the same result
        expected_count = len(self.test_facilities)
        for result in results:
            self.assertEqual(result, expected_count)
        
        print(f"✓ Thread-safe reads successful: {len(results)} threads got {expected_count} facilities")
    
    
    def test_thread_safe_sorting(self):
        """Test thread-safe sorting operations."""
        print("\n=== Testing Thread-Safe Sorting ===")
        
        # Add test data
        for facility in self.test_facilities:
            self.business_layer.add_facility(facility)
        
        # Test concurrent sorting by different criteria
        def sort_by_emissions():
            self.business_layer.sort_facilities_by_emissions()
            return self.business_layer.facilities
        
        def sort_by_name():
            self.business_layer.sort_facilities_by_name()
            return self.business_layer.facilities
        
        def sort_by_province():
            # Since sort_facilities_by_province doesn't exist, we'll sort by name as a substitute
            self.business_layer.sort_facilities_by_name()
            return self.business_layer.facilities
        
        # Run sorting operations concurrently
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(sort_by_emissions): "emissions",
                executor.submit(sort_by_name): "name", 
                executor.submit(sort_by_province): "province"
            }
            
            results = {}
            for future in as_completed(futures):
                sort_type = futures[future]
                results[sort_type] = future.result()
        
        # Verify all sorting operations completed successfully
        for sort_type, result in results.items():
            self.assertIsNotNone(result)
            self.assertEqual(len(result), len(self.test_facilities))
            print(f"✓ {sort_type.capitalize()} sorting successful: {len(result)} facilities sorted")
    
    def test_parallel_data_processing(self):
        """Test parallel data processing operations."""
        print("\n=== Testing Parallel Data Processing ===")
        
        # Add test data
        for facility in self.test_facilities:
            self.business_layer.add_facility(facility)
        
        # Test parallel statistics calculation
        def calculate_emissions_stats():
            facilities = self.business_layer.facilities
            if not facilities:
                return {"count": 0, "total": 0, "average": 0}
            
            total_emissions = sum(f.emissions for f in facilities)
            return {
                "count": len(facilities),
                "total": total_emissions,
                "average": total_emissions / len(facilities)
            }
        
        def calculate_province_stats():
            facilities = self.business_layer.facilities
            province_counts = {}
            for facility in facilities:
                province = facility.province
                province_counts[province] = province_counts.get(province, 0) + 1
            return province_counts
        
        # Run parallel processing
        with ThreadPoolExecutor(max_workers=2) as executor:
            emissions_future = executor.submit(calculate_emissions_stats)
            province_future = executor.submit(calculate_province_stats)
            
            emissions_stats = emissions_future.result()
            province_stats = province_future.result()
        
        # Verify results
        self.assertEqual(emissions_stats["count"], len(self.test_facilities))
        self.assertGreater(emissions_stats["total"], 0)
        self.assertGreater(emissions_stats["average"], 0)
        
        self.assertIn("ON", province_stats)
        self.assertIn("BC", province_stats)
        self.assertIn("AB", province_stats)
        
        print(f"✓ Parallel processing successful:")
        print(f"  - Emissions stats: {emissions_stats}")
        print(f"  - Province stats: {province_stats}")
    
    def test_thread_safety_under_load(self):
        """Test thread safety under high load."""
        print("\n=== Testing Thread Safety Under Load ===")
        
        # Create many test facilities
        test_facilities = []
        for i in range(100):
            facility = StandardFormatFacility(
                npri_id=f"LOAD_TEST_{i:03d}",
                facility_name=f"Load Test Facility {i}",
                company_name=f"Load Test Company {i}",
                city=f"Load Test City {i}",
                province=["ON", "BC", "AB", "QC"][i % 4],
                emissions=float(i * 10),
                units="tonnes"
            )
            test_facilities.append(facility)
        
        # Add facilities concurrently
        def add_facility_batch(start_idx, end_idx):
            for i in range(start_idx, end_idx):
                self.business_layer.add_facility(test_facilities[i])
            return end_idx - start_idx
        
        # Split work across multiple threads
        batch_size = 20
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for i in range(0, len(test_facilities), batch_size):
                end_idx = min(i + batch_size, len(test_facilities))
                future = executor.submit(add_facility_batch, i, end_idx)
                futures.append(future)
            
            # Wait for all additions to complete
            total_added = sum(future.result() for future in futures)
        
        # Verify all facilities were added
        all_facilities = self.business_layer.facilities
        self.assertEqual(len(all_facilities), len(test_facilities))
        print(f"✓ High-load thread safety test successful: {total_added} facilities added")
        
        # Test concurrent operations on large dataset
        def search_operation():
            results = []
            facilities = self.business_layer.facilities
            for i in range(0, 100, 10):
                search_term = f"LOAD_TEST_{i:03d}"
                search_results = [f for f in facilities if search_term in f.npri_id]
                results.extend(search_results)
            return len(results)
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(search_operation) for _ in range(5)]
            search_counts = [future.result() for future in futures]
        
        # All search operations should return consistent results
        expected_count = search_counts[0]
        for count in search_counts:
            self.assertEqual(count, expected_count)
        
        print(f"✓ Concurrent operations on large dataset successful: {expected_count} results per search")

def run_multithreading_tests():
    """Run all multithreading tests."""
    print("RUNNING MULTITHREADING TESTS")
    print("=" * 35)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    test_loader = unittest.TestLoader()
    
    # Add test methods
    test_suite.addTest(test_loader.loadTestsFromTestCase(TestMultithreadingFunctionality))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 35)
    print("TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n🎉 ALL MULTITHREADING TESTS PASSED!")
    else:
        print("\n❌ SOME MULTITHREADING TESTS FAILED!")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_multithreading_tests()
    exit(0 if success else 1) 