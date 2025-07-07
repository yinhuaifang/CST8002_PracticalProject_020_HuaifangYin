"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Database layer for handling MySQL database operations with Django-style patterns.
"""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import List, Optional
from entities.facility_record import FacilityRecord, StandardFormatFacility

# Try to import MySQL connector
try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    print("Note: MySQL connector not available. Install mysql-connector-python to enable database features.")

class DatabaseManager:
    """
    Database manager class for handling MySQL database operations.
    This demonstrates database connectivity as an advanced language feature.
    Implements Django-style database operations and migrations.
    """
    
    def __init__(self, host="localhost", user="root", password="1101", database="project03"):
        """
        Initialize the database manager.
        
        Args:
            host (str): Database host
            user (str): Database user
            password (str): Database password
            database (str): Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self) -> bool:
        """
        Connect to the MySQL database.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        if not MYSQL_AVAILABLE:
            print("MySQL connector not available.")
            return False
            
        try:
            # Debug: Print connection parameters
            print(f"Attempting to connect with: host={self.host}, user={self.user}, database={self.database}")
            # Use the specific connection code provided by the user
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print(f"Connected to MySQL database: {self.database}")
                return True
            else:
                print("Failed to connect to MySQL database.")
                return False
                
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the MySQL database."""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Disconnected from MySQL database.")
    
    def create_table(self) -> bool:
        """
        Create the facilities table if it doesn't exist using Django-style migrations.
        
        Returns:
            bool: True if table creation successful, False otherwise
        """
        if not self.connection or not self.connection.is_connected():
            print("Not connected to database.")
            return False
            
        try:
            # Use Django-style model migration [1.3]
            return StandardFormatFacility.create_table(self.connection)
            
        except Error as e:
            print(f"Error creating table: {e}")
            return False 