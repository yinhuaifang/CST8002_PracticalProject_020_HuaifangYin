"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Tyler DeLay]
Due Date: [Aug 03 2025]
Author: [Huaifang Yin]
Description: Test suite for Flask app (app.py).
Tests all routes, chart data generation, and template rendering.

References:
[1] Python Documentation. "unittest - Unit testing framework."
    https://docs.python.org/3/library/unittest.html
[2] Flask Documentation. "Testing Flask Applications."
    https://flask.palletsprojects.com/en/2.3.x/testing/
"""

import unittest
import sys
import os
import json
from unittest.mock import Mock, patch, MagicMock
from typing import List

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Flask app and related modules
from presentation.app import app, facility_manager
from entities.facility_record import FacilityRecord


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask app routes and functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create sample facility records for testing
        self.sample_facilities = [
            FacilityRecord(
                facility_name="Test Facility 1",
                company_name="Test Company 1",
                province="Ontario",
                city="Toronto",
                report_year=2020,
                emissions="1000.5"
            ),
            FacilityRecord(
                facility_name="Test Facility 2",
                company_name="Test Company 2",
                province="Alberta",
                city="Calgary",
                report_year=2020,
                emissions="2000.0"
            ),
            FacilityRecord(
                facility_name="Test Facility 3",
                company_name="Test Company 3",
                province="Ontario",
                city="Ottawa",
                report_year=2021,
                emissions="1500.0"
            ),
            FacilityRecord(
                facility_name="Test Facility 4",
                company_name="Test Company 4",
                province="British Columbia",
                city="Vancouver",
                report_year=2021,
                emissions="3000.0"
            ),
            FacilityRecord(
                facility_name="Test Facility 5",
                company_name="Test Company 5",
                province="Alberta",
                city="Edmonton",
                report_year=2022,
                emissions="2500.0"
            )
        ]
    
    def test_index_route_redirect(self):
        """Test that the index route redirects to province charts."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertIn('/charts/province', response.location)
    
    def test_province_chart_route_with_data(self):
        """Test province chart route with sample data."""
        # Mock the helper function to return sample data
        from presentation.app import get_province_chart_data
        with patch('presentation.app.get_province_chart_data', return_value=(['Ontario', 'Alberta'], [2500.5, 4500.0])):
            response = self.app.get('/charts/province')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Interactive Charts: Emissions by Province', response.data)
            self.assertIn(b'Province Charts', response.data)
            self.assertIn(b'Horizontal Bar Chart', response.data)
            self.assertIn(b'Vertical Bar Chart', response.data)
            self.assertIn(b'Pie Chart', response.data)
    
    def test_province_chart_route_no_data(self):
        """Test province chart route with no data."""
        # Mock the helper function to return empty data
        from presentation.app import get_province_chart_data
        with patch('presentation.app.get_province_chart_data', return_value=([], [])):
            response = self.app.get('/charts/province')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Error: No data available for chart generation', response.data)
    
    def test_year_chart_route_with_data(self):
        """Test year chart route with sample data."""
        # Mock the helper function to return sample data
        from presentation.app import get_year_chart_data
        with patch('presentation.app.get_year_chart_data', return_value=(['2020', '2021'], [3000.5, 4500.0])):
            response = self.app.get('/charts/year')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Interactive Charts: Emissions by Year', response.data)
            self.assertIn(b'Year Charts', response.data)
            self.assertIn(b'Horizontal Bar Chart', response.data)
            self.assertIn(b'Vertical Bar Chart', response.data)
            self.assertIn(b'Pie Chart', response.data)
    
    def test_year_chart_route_no_data(self):
        """Test year chart route with no data."""
        # Mock the helper function to return empty data
        from presentation.app import get_year_chart_data
        with patch('presentation.app.get_year_chart_data', return_value=([], [])):
            response = self.app.get('/charts/year')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Error: No data available for chart generation', response.data)
    
    def test_top_facilities_chart_route_default(self):
        """Test top facilities chart route with default top_n."""
        # Mock the helper function to return sample data
        from presentation.app import get_top_facilities_chart_data
        with patch('presentation.app.get_top_facilities_chart_data', return_value=(['Facility 1', 'Facility 2'], [3000.0, 2000.0])):
            response = self.app.get('/charts/top-facilities')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Interactive Charts: Top 10 Facilities by Emissions', response.data)
            self.assertIn(b'Top Facilities Charts', response.data)
            self.assertIn(b'Horizontal Bar Chart', response.data)
            self.assertIn(b'Vertical Bar Chart', response.data)
            self.assertIn(b'Pie Chart', response.data)
    
    def test_top_facilities_chart_route_custom_top_n(self):
        """Test top facilities chart route with custom top_n parameter."""
        # Mock the helper function to return sample data
        from presentation.app import get_top_facilities_chart_data
        with patch('presentation.app.get_top_facilities_chart_data', return_value=(['Facility 1', 'Facility 2', 'Facility 3'], [3000.0, 2000.0, 1500.0])):
            response = self.app.get('/charts/top-facilities?top_n=3')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Interactive Charts: Top 3 Facilities by Emissions', response.data)
    
    def test_top_facilities_chart_route_no_data(self):
        """Test top facilities chart route with no data."""
        # Mock the helper function to return empty data
        from presentation.app import get_top_facilities_chart_data
        with patch('presentation.app.get_top_facilities_chart_data', return_value=([], [])):
            response = self.app.get('/charts/top-facilities')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Error: No data available for chart generation', response.data)
    
    def test_navigation_links_present(self):
        """Test that navigation links are present on all chart pages."""
        # Mock the helper functions to return sample data
        from presentation.app import get_province_chart_data, get_year_chart_data, get_top_facilities_chart_data
        
        with patch('presentation.app.get_province_chart_data', return_value=(['Ontario'], [2500.5])):
            # Test province chart
            response = self.app.get('/charts/province')
            self.assertIn(b'href="/charts/province"', response.data)
            self.assertIn(b'href="/charts/year"', response.data)
            self.assertIn(b'href="/charts/top-facilities"', response.data)
        
        with patch('presentation.app.get_year_chart_data', return_value=(['2020'], [3000.5])):
            # Test year chart
            response = self.app.get('/charts/year')
            self.assertIn(b'href="/charts/province"', response.data)
            self.assertIn(b'href="/charts/year"', response.data)
            self.assertIn(b'href="/charts/top-facilities"', response.data)
        
        with patch('presentation.app.get_top_facilities_chart_data', return_value=(['Facility 1'], [3000.0])):
            # Test top facilities chart
            response = self.app.get('/charts/top-facilities')
            self.assertIn(b'href="/charts/province"', response.data)
            self.assertIn(b'href="/charts/year"', response.data)
            self.assertIn(b'href="/charts/top-facilities"', response.data)
    
    def test_chart_js_included(self):
        """Test that Chart.js is included in all chart pages."""
        # Mock the helper functions to return sample data
        from presentation.app import get_province_chart_data, get_year_chart_data, get_top_facilities_chart_data
        
        with patch('presentation.app.get_province_chart_data', return_value=(['Ontario'], [2500.5])):
            # Test province chart
            response = self.app.get('/charts/province')
            self.assertIn(b'chart.js', response.data)
        
        with patch('presentation.app.get_year_chart_data', return_value=(['2020'], [3000.5])):
            # Test year chart
            response = self.app.get('/charts/year')
            self.assertIn(b'chart.js', response.data)
        
        with patch('presentation.app.get_top_facilities_chart_data', return_value=(['Facility 1'], [3000.0])):
            # Test top facilities chart
            response = self.app.get('/charts/top-facilities')
            self.assertIn(b'chart.js', response.data)
    
    def test_template_inheritance(self):
        """Test that templates properly extend the base template."""
        # Mock the helper functions to return sample data
        from presentation.app import get_province_chart_data, get_year_chart_data, get_top_facilities_chart_data
        
        with patch('presentation.app.get_province_chart_data', return_value=(['Ontario'], [2500.5])):
            # Test that all pages have the common base template elements
            response = self.app.get('/charts/province')
            self.assertIn(b'Author:', response.data)
            self.assertIn(b'Huaifang Yin', response.data)
            self.assertIn(b'Interactive Charts', response.data)
        
        with patch('presentation.app.get_year_chart_data', return_value=(['2020'], [3000.5])):
            response = self.app.get('/charts/year')
            self.assertIn(b'Author:', response.data)
            self.assertIn(b'Huaifang Yin', response.data)
            self.assertIn(b'Interactive Charts', response.data)
        
        with patch('presentation.app.get_top_facilities_chart_data', return_value=(['Facility 1'], [3000.0])):
            response = self.app.get('/charts/top-facilities')
            self.assertIn(b'Author:', response.data)
            self.assertIn(b'Huaifang Yin', response.data)
            self.assertIn(b'Interactive Charts', response.data)





class TestAppIntegration(unittest.TestCase):
    """Integration tests for the Flask app."""
    
    def setUp(self):
        """Set up test fixtures for integration tests."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create realistic facility data
        self.realistic_facilities = [
            FacilityRecord("Alberta Oil Refinery", "Alberta Energy Corp", "Alberta", "Calgary", 2020, "50000.0"),
            FacilityRecord("Ontario Power Plant", "Ontario Power Inc", "Ontario", "Toronto", 2020, "30000.0"),
            FacilityRecord("BC Mining Facility", "BC Resources Ltd", "British Columbia", "Vancouver", 2020, "25000.0"),
            FacilityRecord("Quebec Steel Mill", "Quebec Steel Co", "Quebec", "Montreal", 2020, "40000.0"),
            FacilityRecord("Saskatchewan Factory", "Sask Manufacturing", "Saskatchewan", "Regina", 2020, "15000.0"),
            FacilityRecord("Alberta Oil Refinery", "Alberta Energy Corp", "Alberta", "Calgary", 2021, "52000.0"),
            FacilityRecord("Ontario Power Plant", "Ontario Power Inc", "Ontario", "Toronto", 2021, "28000.0"),
            FacilityRecord("BC Mining Facility", "BC Resources Ltd", "British Columbia", "Vancouver", 2021, "27000.0"),
            FacilityRecord("Quebec Steel Mill", "Quebec Steel Co", "Quebec", "Montreal", 2021, "42000.0"),
            FacilityRecord("Saskatchewan Factory", "Sask Manufacturing", "Saskatchewan", "Regina", 2021, "16000.0"),
        ]
    
    def test_full_workflow_province_chart(self):
        """Test complete workflow for province chart generation."""
        from presentation.app import get_province_chart_data
        with patch('presentation.app.get_province_chart_data', return_value=(['Alberta', 'Ontario', 'British Columbia', 'Quebec', 'Saskatchewan'], [102000.0, 58000.0, 52000.0, 82000.0, 31000.0])):
            response = self.app.get('/charts/province')
            self.assertEqual(response.status_code, 200)
            
            # Check that the page contains expected content
            self.assertIn(b'Alberta', response.data)
            self.assertIn(b'Ontario', response.data)
            self.assertIn(b'British Columbia', response.data)
            self.assertIn(b'Quebec', response.data)
            self.assertIn(b'Saskatchewan', response.data)
            
            # Check that Chart.js is included
            self.assertIn(b'chart.js', response.data)
            
            # Check that all three chart types are present
            self.assertIn(b'Horizontal Bar Chart', response.data)
            self.assertIn(b'Vertical Bar Chart', response.data)
            self.assertIn(b'Pie Chart', response.data)
    
    def test_full_workflow_year_chart(self):
        """Test complete workflow for year chart generation."""
        from presentation.app import get_year_chart_data
        with patch('presentation.app.get_year_chart_data', return_value=(['2020', '2021'], [160000.0, 165000.0])):
            response = self.app.get('/charts/year')
            self.assertEqual(response.status_code, 200)
            
            # Check that the page contains expected content
            self.assertIn(b'2020', response.data)
            self.assertIn(b'2021', response.data)
            
            # Check that Chart.js is included
            self.assertIn(b'chart.js', response.data)
            
            # Check that all three chart types are present
            self.assertIn(b'Horizontal Bar Chart', response.data)
            self.assertIn(b'Vertical Bar Chart', response.data)
            self.assertIn(b'Pie Chart', response.data)
    
    def test_full_workflow_top_facilities_chart(self):
        """Test complete workflow for top facilities chart generation."""
        from presentation.app import get_top_facilities_chart_data
        with patch('presentation.app.get_top_facilities_chart_data', return_value=(['Alberta Oil Refinery', 'Quebec Steel Mill', 'Ontario Power Plant', 'BC Mining Facility', 'Saskatchewan Factory'], [52000.0, 42000.0, 28000.0, 27000.0, 16000.0])):
            response = self.app.get('/charts/top-facilities?top_n=5')
            self.assertEqual(response.status_code, 200)
            
            # Check that the page contains expected content
            self.assertIn(b'Top 5 Facilities by Emissions', response.data)
            self.assertIn(b'Alberta Oil Refinery', response.data)
            self.assertIn(b'Quebec Steel Mill', response.data)
            
            # Check that Chart.js is included
            self.assertIn(b'chart.js', response.data)
            
            # Check that all three chart types are present
            self.assertIn(b'Horizontal Bar Chart', response.data)
            self.assertIn(b'Vertical Bar Chart', response.data)
            self.assertIn(b'Pie Chart', response.data)
    
    def test_navigation_between_pages(self):
        """Test navigation between different chart pages."""
        from presentation.app import get_province_chart_data, get_year_chart_data, get_top_facilities_chart_data
        
        # Test that all navigation links work
        with patch('presentation.app.get_province_chart_data', return_value=(['Alberta'], [102000.0])):
            response = self.app.get('/charts/province')
            self.assertIn(b'href="/charts/province"', response.data)
            self.assertIn(b'href="/charts/year"', response.data)
            self.assertIn(b'href="/charts/top-facilities"', response.data)
        
        with patch('presentation.app.get_year_chart_data', return_value=(['2020'], [160000.0])):
            response = self.app.get('/charts/year')
            self.assertIn(b'href="/charts/province"', response.data)
            self.assertIn(b'href="/charts/year"', response.data)
            self.assertIn(b'href="/charts/top-facilities"', response.data)
        
        with patch('presentation.app.get_top_facilities_chart_data', return_value=(['Alberta Oil Refinery'], [52000.0])):
            response = self.app.get('/charts/top-facilities')
            self.assertIn(b'href="/charts/province"', response.data)
            self.assertIn(b'href="/charts/year"', response.data)
            self.assertIn(b'href="/charts/top-facilities"', response.data)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2) 