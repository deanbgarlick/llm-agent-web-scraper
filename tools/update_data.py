"""
Factory function for creating data update tools bound to a data manager.

This module provides the factory pattern for creating update_data tools
that are bound to specific data manager instances.
"""

def create_update_data_tool(data_manager):
    """
    Create an update_data tool function bound to a specific data manager.
    
    Args:
        data_manager (DataPointsManager): The data manager instance to bind to
        
    Returns:
        callable: A function that can be used as the update_data tool
    """
    def update_data(datas_update):
        """
        Update the state with new data points found.
        
        Args:
            datas_update (List[dict]): The new data points found, containing data_point, value, and reference
        
        Returns:
            str: Message confirming data update
        """
        for data in datas_update:
            data_manager.update_data_point(
                data["data_point"], 
                data["value"], 
                data["reference"]
            )
        
        return f"data updated: {data_manager.get_current_state()}"
    
    return update_data 