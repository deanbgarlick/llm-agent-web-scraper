from data_point_manager import get_data_point_manager

def update_data(datas_update):
    """
    Update the state with new data points found
    
    Args:
        datas_update (List[dict]): The new data points found, containing data_point, value, and reference
    
    Returns:
        str: Message confirming data update
    """

    for data in datas_update:
        get_data_point_manager().update_data_point(data["data_point"], data["value"], data["reference"])
    
    return f"data updated: {get_data_point_manager().get_current_state()}" 