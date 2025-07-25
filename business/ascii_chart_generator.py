"""
Course: CST8002 - Programming Language Research Project
Assignment: Practical Project04
Professor: [Tyler DeLay]
Due Date: [Aug 03 2025]
Author: [Huaifang Yin]
Description: ASCII Chart Generator for creating text-based chart visualizations.
Provides ASCII art versions of charts for console programs and web services.
"""

from typing import List, Dict, Tuple, Any
from collections import defaultdict
import math
from entities.facility_record import FacilityRecord

class ASCIIChartGenerator:
    """
    Generates ASCII art charts for console and web service applications.
    Supports bar charts, line charts, and histogram visualizations.
    """
    
    def __init__(self, max_width: int = 80, max_height: int = 20):
        """
        Initialize the ASCII chart generator.
        
        Args:
            max_width (int): Maximum width of the chart in characters
            max_height (int): Maximum height of the chart in characters
        """
        self.max_width = max_width
        self.max_height = max_height
        self.chart_chars = {
            'bar': '█',
            'bar_alt': '▓',
            'line': '─',
            'line_alt': '━',
            'point': '●',
            'point_alt': '◆',
            'axis': '│',
            'axis_horizontal': '─',
            'corner': '└',
            'corner_top': '┌',
            'corner_bottom': '┘',
            'corner_right': '┐',
            'tick': '├',
            'tick_right': '┤'
        }
    
    def generate_province_chart(self, facilities: List[FacilityRecord], 
                              chart_type: str = 'bar') -> str:
        """
        Generate ASCII chart showing emissions by province.
        
        Args:
            facilities (List[FacilityRecord]): List of facility records
            chart_type (str): Type of chart ('bar', 'line', 'histogram')
            
        Returns:
            str: ASCII art chart
        """
        if not facilities:
            return "No data available for chart generation."
        
        # Aggregate data by province
        province_emissions = defaultdict(float)
        for facility in facilities:
            province_emissions[facility.province] += float(facility.emissions)
        
        # Sort by emissions (descending)
        sorted_provinces = sorted(province_emissions.items(), 
                                key=lambda x: x[1], reverse=True)
        
        labels = [province for province, _ in sorted_provinces]
        values = [emissions for _, emissions in sorted_provinces]
        
        if chart_type == 'bar':
            return self._create_bar_chart(labels, values, "Emissions by Province")
        elif chart_type == 'line':
            return self._create_line_chart(labels, values, "Emissions by Province")
        elif chart_type == 'histogram':
            return self._create_histogram(labels, values, "Emissions by Province")
        else:
            return self._create_bar_chart(labels, values, "Emissions by Province")
    
    def generate_year_chart(self, facilities: List[FacilityRecord], 
                          chart_type: str = 'line') -> str:
        """
        Generate ASCII chart showing emissions by year.
        
        Args:
            facilities (List[FacilityRecord]): List of facility records
            chart_type (str): Type of chart ('bar', 'line', 'histogram')
            
        Returns:
            str: ASCII art chart
        """
        if not facilities:
            return "No data available for chart generation."
        
        # Aggregate data by year
        year_emissions = defaultdict(float)
        for facility in facilities:
            year_emissions[facility.report_year] += float(facility.emissions)
        
        # Sort by year
        sorted_years = sorted(year_emissions.items())
        
        labels = [str(year) for year, _ in sorted_years]
        values = [emissions for _, emissions in sorted_years]
        
        if chart_type == 'bar':
            return self._create_bar_chart(labels, values, "Emissions by Year")
        elif chart_type == 'line':
            return self._create_line_chart(labels, values, "Emissions by Year")
        elif chart_type == 'histogram':
            return self._create_histogram(labels, values, "Emissions by Year")
        else:
            return self._create_line_chart(labels, values, "Emissions by Year")
    
    def generate_top_facilities_chart(self, facilities: List[FacilityRecord], 
                                    top_n: int = 10, chart_type: str = 'bar') -> str:
        """
        Generate ASCII chart showing top facilities by emissions.
        
        Args:
            facilities (List[FacilityRecord]): List of facility records
            top_n (int): Number of top facilities to show
            chart_type (str): Type of chart ('bar', 'line', 'histogram')
            
        Returns:
            str: ASCII art chart
        """
        if not facilities:
            return "No data available for chart generation."
        
        # Sort facilities by emissions (descending)
        sorted_facilities = sorted(facilities, key=lambda x: float(x.emissions), reverse=True)
        top_facilities = sorted_facilities[:top_n]
        
        # Truncate facility names for display
        labels = []
        for facility in top_facilities:
            name = facility.facility_name
            if len(name) > 20:
                name = name[:17] + "..."
            labels.append(name)
        
        values = [float(facility.emissions) for facility in top_facilities]
        
        if chart_type == 'bar':
            return self._create_bar_chart(labels, values, f"Top {top_n} Facilities by Emissions")
        elif chart_type == 'line':
            return self._create_line_chart(labels, values, f"Top {top_n} Facilities by Emissions")
        elif chart_type == 'histogram':
            return self._create_histogram(labels, values, f"Top {top_n} Facilities by Emissions")
        else:
            return self._create_bar_chart(labels, values, f"Top {top_n} Facilities by Emissions")
    
    def _create_bar_chart(self, labels: List[str], values: List[float], title: str) -> str:
        """
        Create a bar chart in ASCII art.
        
        Args:
            labels (List[str]): Labels for each bar
            values (List[float]): Values for each bar
            title (str): Chart title
            
        Returns:
            str: ASCII art bar chart
        """
        if not values:
            return "No data to display."
        
        max_value = max(values)
        min_value = min(values)
        
        # Calculate chart dimensions
        chart_width = min(self.max_width - 20, len(labels) * 8)  # Leave space for labels
        chart_height = self.max_height - 4  # Leave space for title and labels
        
        # Create the chart
        chart_lines = []
        
        # Title
        chart_lines.append(f"\n{title.center(self.max_width)}")
        chart_lines.append("=" * self.max_width)
        
        # Chart area
        for i in range(chart_height):
            line = "│ "  # Left border
            y_value = max_value - (i * max_value / chart_height)
            
            for j, value in enumerate(values):
                if value >= y_value:
                    bar_height = int((value / max_value) * chart_height)
                    if i >= (chart_height - bar_height):
                        line += self.chart_chars['bar'] + " "
                    else:
                        line += "  "
                else:
                    line += "  "
            
            line += "│"  # Right border
            
            # Add y-axis label
            if i % 3 == 0 or i == chart_height - 1:
                label = f"{y_value:.1f}"
                line += f" {label:>8}"
            
            chart_lines.append(line)
        
        # X-axis
        axis_line = "└" + "─" * (chart_width) + "┘"
        chart_lines.append(axis_line)
        
        # X-axis labels
        label_line = "  "
        for i, label in enumerate(labels):
            if i < chart_width // 8:  # Only show labels that fit
                label_line += f"{label[:6]:<8}"
        chart_lines.append(label_line)
        
        # Summary statistics
        chart_lines.append("")
        chart_lines.append(f"Total: {sum(values):.2f} | Max: {max_value:.2f} | Min: {min_value:.2f}")
        
        return "\n".join(chart_lines)
    
    def _create_line_chart(self, labels: List[str], values: List[float], title: str) -> str:
        """
        Create a line chart in ASCII art.
        
        Args:
            labels (List[str]): Labels for each point
            values (List[float]): Values for each point
            title (str): Chart title
            
        Returns:
            str: ASCII art line chart
        """
        if not values:
            return "No data to display."
        
        max_value = max(values)
        min_value = min(values)
        
        # Calculate chart dimensions
        chart_width = min(self.max_width - 20, len(labels) * 8)
        chart_height = self.max_height - 4
        
        # Create the chart
        chart_lines = []
        
        # Title
        chart_lines.append(f"\n{title.center(self.max_width)}")
        chart_lines.append("=" * self.max_width)
        
        # Chart area
        for i in range(chart_height):
            line = "│ "  # Left border
            y_value = max_value - (i * max_value / chart_height)
            
            # Create line by interpolating between points
            for x in range(chart_width):
                x_ratio = x / chart_width
                point_index = x_ratio * (len(values) - 1)
                
                if point_index.is_integer():
                    # Exact point
                    idx = int(point_index)
                    if idx < len(values):
                        if abs(values[idx] - y_value) < (max_value / chart_height / 2):
                            line += self.chart_chars['point']
                        elif values[idx] > y_value:
                            line += self.chart_chars['line']
                        else:
                            line += " "
                    else:
                        line += " "
                else:
                    # Interpolate between points
                    idx1 = int(point_index)
                    idx2 = min(idx1 + 1, len(values) - 1)
                    
                    if idx1 < len(values) and idx2 < len(values):
                        # Linear interpolation
                        ratio = point_index - idx1
                        interpolated_value = values[idx1] * (1 - ratio) + values[idx2] * ratio
                        
                        if abs(interpolated_value - y_value) < (max_value / chart_height / 2):
                            line += self.chart_chars['line']
                        elif interpolated_value > y_value:
                            line += self.chart_chars['line']
                        else:
                            line += " "
                    else:
                        line += " "
            
            line += "│"  # Right border
            
            # Add y-axis label
            if i % 3 == 0 or i == chart_height - 1:
                label = f"{y_value:.1f}"
                line += f" {label:>8}"
            
            chart_lines.append(line)
        
        # X-axis
        axis_line = "└" + "─" * (chart_width) + "┘"
        chart_lines.append(axis_line)
        
        # X-axis labels
        label_line = "  "
        for i, label in enumerate(labels):
            if i < chart_width // 8:
                label_line += f"{label[:6]:<8}"
        chart_lines.append(label_line)
        
        # Summary statistics
        chart_lines.append("")
        chart_lines.append(f"Total: {sum(values):.2f} | Max: {max_value:.2f} | Min: {min_value:.2f}")
        
        return "\n".join(chart_lines)
    
    def _create_histogram(self, labels: List[str], values: List[float], title: str) -> str:
        """
        Create a histogram in ASCII art.
        
        Args:
            labels (List[str]): Labels for each bin
            values (List[float]): Values for each bin
            title (str): Chart title
            
        Returns:
            str: ASCII art histogram
        """
        if not values:
            return "No data to display."
        
        max_value = max(values)
        min_value = min(values)
        
        # Calculate chart dimensions
        chart_width = min(self.max_width - 20, len(labels) * 8)
        chart_height = self.max_height - 4
        
        # Create the chart
        chart_lines = []
        
        # Title
        chart_lines.append(f"\n{title.center(self.max_width)}")
        chart_lines.append("=" * self.max_width)
        
        # Chart area
        for i in range(chart_height):
            line = "│ "  # Left border
            y_value = max_value - (i * max_value / chart_height)
            
            for j, value in enumerate(values):
                if value >= y_value:
                    bar_height = int((value / max_value) * chart_height)
                    if i >= (chart_height - bar_height):
                        # Use different characters for histogram effect
                        if i == chart_height - bar_height:
                            line += self.chart_chars['bar']
                        else:
                            line += self.chart_chars['bar_alt']
                    else:
                        line += " "
                else:
                    line += " "
            
            line += "│"  # Right border
            
            # Add y-axis label
            if i % 3 == 0 or i == chart_height - 1:
                label = f"{y_value:.1f}"
                line += f" {label:>8}"
            
            chart_lines.append(line)
        
        # X-axis
        axis_line = "└" + "─" * (chart_width) + "┘"
        chart_lines.append(axis_line)
        
        # X-axis labels
        label_line = "  "
        for i, label in enumerate(labels):
            if i < chart_width // 8:
                label_line += f"{label[:6]:<8}"
        chart_lines.append(label_line)
        
        # Summary statistics
        chart_lines.append("")
        chart_lines.append(f"Total: {sum(values):.2f} | Max: {max_value:.2f} | Min: {min_value:.2f}")
        
        return "\n".join(chart_lines)
    
    def get_available_chart_types(self) -> List[str]:
        """
        Get list of available chart types.
        
        Returns:
            List[str]: List of available chart types
        """
        return ['bar', 'line', 'histogram']
    
    def generate_chart(self, chart_type: str, facilities: List[FacilityRecord], **kwargs) -> str:
        """
        Generate a chart based on the specified type.
        
        Args:
            chart_type (str): Type of chart to generate ('province', 'year', 'top_facilities')
            facilities (List[FacilityRecord]): List of facility records
            **kwargs: Additional arguments (e.g., top_n for top_facilities)
            
        Returns:
            str: Generated ASCII art chart
        """
        if chart_type == 'province':
            return self.generate_province_chart(facilities, kwargs.get('style', 'bar'))
        elif chart_type == 'year':
            return self.generate_year_chart(facilities, kwargs.get('style', 'line'))
        elif chart_type == 'top_facilities':
            top_n = kwargs.get('top_n', 10)
            return self.generate_top_facilities_chart(facilities, top_n, kwargs.get('style', 'bar'))
        else:
            return f"Unknown chart type: {chart_type}. Available types: {self.get_available_chart_types()}" 