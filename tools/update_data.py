def update_data(datas_update):
    """
    Update the state with new data points found
    
    Args:
        datas_update (List[dict]): The new data points found, containing data_point, value, and reference
    
    Returns:
        str: Message confirming data update
    """
    
    # Import data_points from the main module
    from app import data_points
    
    for data in datas_update:
        for obj in data_points:
            if obj["name"] == data["data_point"]:
                obj["value"] = data["value"]
                obj["reference"] = data["reference"]
    
    return f"data updated: {data_points}" 