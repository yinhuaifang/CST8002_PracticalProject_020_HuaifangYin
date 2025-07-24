"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project03
Professor: [Stanley Pieda,Tyler DeLay]
Due Date: [June 15  2025]
Author: [Huaifang Yin]
Description: Flask web service for Facility Management System.
Provides chart visualization endpoints for data analysis.

References:
[1] Flask Documentation. "Flask - A lightweight WSGI web application framework."
    https://flask.palletsprojects.com/
[2] Python Documentation. "JSON encoder and decoder."
    https://docs.python.org/3/library/json.html
"""

from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
import json
from typing import Dict, List, Any
import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from business.business_layer import FacilityManager
from entities.facility_record import FacilityRecord

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the facility manager and chart generator
facility_manager = FacilityManager()

def get_province_chart_data():
    """Get province chart data using ChartGenerator."""
    facilities = facility_manager.facilities
    if not facilities:
        return [], []
    
    # Use ChartGenerator's logic
    from collections import defaultdict
    province_emissions = defaultdict(float)
    for facility in facilities:
        province_emissions[facility.province] += float(facility.emissions)
    
    # Sort by emissions (descending) - same as ChartGenerator
    sorted_provinces = sorted(province_emissions.items(), 
                            key=lambda x: x[1], reverse=True)
    
    labels = [province for province, _ in sorted_provinces]
    values = [emissions for _, emissions in sorted_provinces]
    return labels, values

def get_year_chart_data():
    """Get year chart data using ChartGenerator."""
    facilities = facility_manager.facilities
    if not facilities:
        return [], []
    
    # Use ChartGenerator's logic
    from collections import defaultdict
    year_emissions = defaultdict(float)
    for facility in facilities:
        year_emissions[facility.report_year] += float(facility.emissions)
    
    # Sort by year - same as ChartGenerator
    sorted_years = sorted(year_emissions.items())
    
    labels = [str(year) for year, _ in sorted_years]
    values = [emissions for _, emissions in sorted_years]
    return labels, values

def get_top_facilities_chart_data(top_n=10):
    """Get top facilities chart data using ChartGenerator."""
    facilities = facility_manager.facilities
    if not facilities:
        return [], []
    
    # Sort facilities by emissions (descending) - same as ChartGenerator
    sorted_facilities = sorted(facilities, key=lambda x: float(x.emissions), reverse=True)
    top_facilities = sorted_facilities[:top_n]
    
    labels = [facility.facility_name[:20] + '...' if len(facility.facility_name) > 20 else facility.facility_name for facility in top_facilities]
    values = [float(facility.emissions) for facility in top_facilities]
    return labels, values

@app.route('/')
def index():
    """Default route - redirect to province charts."""
    return redirect(url_for('show_province_chart'))



@app.route('/charts/province')
def show_province_chart():
    """Show province chart as interactive Chart.js chart with multiple chart types."""
    try:
        # Get chart data using ChartGenerator logic
        labels, values = get_province_chart_data()
        
        if not labels or not values:
            return f"<h2>Error: No data available for chart generation</h2>"
        
        return render_template('province_chart.html', 
                             labels=labels, 
                             values=values,
                             active_page='province')
    except Exception as e:
        return f"<h2>Error loading chart: {e}</h2>"

@app.route('/charts/year')
def show_year_chart():
    """Show year chart as interactive Chart.js chart with multiple chart types."""
    try:
        # Get chart data using ChartGenerator logic
        labels, values = get_year_chart_data()
        
        if not labels or not values:
            return f"<h2>Error: No data available for chart generation</h2>"
        
        return render_template('year_chart.html', 
                             labels=labels, 
                             values=values,
                             active_page='year')
    except Exception as e:
        return f"<h2>Error loading chart: {e}</h2>"

@app.route('/charts/top-facilities')
def show_top_facilities_chart():
    """Show top facilities chart as interactive Chart.js chart with multiple chart types."""
    try:
        top_n = request.args.get('top_n', 10, type=int)
        
        # Get chart data using ChartGenerator logic
        labels, values = get_top_facilities_chart_data(top_n)
        
        if not labels or not values:
            return f"<h2>Error: No data available for chart generation</h2>"
        
        return render_template('top_facilities_chart.html', 
                             labels=labels, 
                             values=values,
                             top_n=top_n,
                             active_page='top-facilities')
    except Exception as e:
        return f"<h2>Error loading chart: {e}</h2>"

if __name__ == '__main__':
    print("Facility Management System")
    print("Author: Huaifang Yin")
    print("Starting Flask server on http://localhost:5000")
    print("Available routes:")
    print("  - http://localhost:5000/ (redirects to /charts/province)")
    print("  - http://localhost:5000/charts/province")
    print("  - http://localhost:5000/charts/year")
    print("  - http://localhost:5000/charts/top-facilities")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        facility_manager.close_database()
    except Exception as e:
        print(f"Error starting server: {e}")
        facility_manager.close_database() 