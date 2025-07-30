"""
Data Points Manager for handling scraping session state.

This module provides centralized management of data points and scraping state
for AI agent sessions.
"""

class DataPointsManager:
    def __init__(self, initial_data_points):
        """
        Initialize the data points manager.
        
        Args:
            initial_data_points (List[dict]): Initial data points structure
        """
        self.data_points = initial_data_points
        self.links_scraped = []
    
    def update_data_point(self, name, value, reference):
        """
        Update a specific data point.
        
        Args:
            name (str): Name of the data point to update
            value (str): Value to set
            reference (str): Reference URL or source
        """
        for obj in self.data_points:
            if obj["name"] == name:
                obj["value"] = value
                obj["reference"] = reference
                break
    
    def get_missing_data_points(self):
        """
        Get list of data point names that still need values.
        
        Returns:
            List[str]: Names of data points with None values
        """
        return [obj["name"] for obj in self.data_points if obj["value"] is None]
    
    def get_current_state(self):
        """
        Get current state of all data points.
        
        Returns:
            List[dict]: Current data points with their values and references
        """
        return self.data_points
    
    def add_scraped_link(self, link):
        """
        Add a link to the scraped links list.
        
        Args:
            link (str): URL that was scraped
        """
        if link not in self.links_scraped:
            self.links_scraped.append(link)
    
    def get_scraped_links(self):
        """
        Get list of already scraped links.
        
        Returns:
            List[str]: URLs that have been scraped
        """
        return self.links_scraped 