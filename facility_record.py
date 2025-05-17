"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project01
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [May 25  2025]
Author: [Huaifang Yin]
Description: This program reads and analyzes nitrogen oxide emissions data from Canadian facilities.
It loads data from a CSV file, creates FacilityRecord objects, and displays the information.
"""


class FacilityRecord:
    """
    A class to represent a single facility's nitrogen oxide emissions record.
    
    Attributes:
        npri_id (str): NPRI ID of the facility
        facility_name (str): Name of the facility
        company_name (str): Name of the company
        address (str): Street address
        city (str): City name
        province (str): Province/territory
        postal_code (str): Postal code
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
        emissions (float): Emissions in tonnes
        units (str): Units of measurement
        facility_details (str): URL with facility details
        facility_information (str): URL with facility information
        report_year (int): Year of report
    """
    
    def __init__(self, npri_id="", facility_name="", company_name="", address="", 
                 city="", province="", postal_code="", latitude=0.0, longitude=0.0, 
                 emissions=0.0, units="", facility_details="", facility_information="", 
                 report_year=0):
        """
        Initialize a FacilityRecord with all attributes.
        
        Args:
            npri_id (str): NPRI ID
            facility_name (str): Facility name
            company_name (str): Company name
            address (str): Street address
            city (str): City
            province (str): Province
            postal_code (str): Postal code
            latitude (float): Latitude
            longitude (float): Longitude
            emissions (float): Emissions amount
            units (str): Units
            facility_details (str): Details URL
            facility_information (str): Info URL
            report_year (int): Report year
        """
        self.npri_id = npri_id
        self.facility_name = facility_name
        self.company_name = company_name
        self.address = address
        self.city = city
        self.province = province
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude
        self.emissions = emissions
        self.units = units
        self.facility_details = facility_details
        self.facility_information = facility_information
        self.report_year = report_year
    
    def __str__(self):
        """Return a formatted string representation of the facility record."""
        return (f"Facility: {self.facility_name}\n"
                f"Company: {self.company_name}\n"
                f"Location: {self.address}, {self.city}, {self.province} {self.postal_code}\n"
                f"Coordinates: {self.latitude}, {self.longitude}\n"
                f"Emissions: {self.emissions} {self.units} ({self.report_year})\n"
                f"Details: {self.facility_details}\n")