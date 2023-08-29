"""
This module provides functions to transform and standardize data.

Available Functions:
- column_data_types_summary: Generate a summary of data types present in a specified column.
- check_duplicates_summary: Check for duplicated values in a specific column.
- remove_duplicates: Remove duplicate rows from a DataFrame based on a specified column.
- check_none_values: Check for None values in a specific column.
- remove_none_values: Remove rows with None values in a specific column of a DataFrame.
- transform_to_numeric: Transform the values of a column to numeric type based on specific rules.
"""

import pandas as pd
import numpy as np


def column_data_types_summary(dataframe, column_name):
    """
    Generate a summary of data types present in a specified column of a DataFrame.
    
    Args:
        dataframe (pd.DataFrame): The DataFrame to analyze.
        column_name (str): The name of the column to analyze.
        
    Returns:
        dict: A summary dictionary containing information about data types in the column.
    """
    # Check if the specified column exists in the DataFrame
    if column_name not in dataframe.columns:
        return {"error": f"Column '{column_name}' not found in the DataFrame"}
    
    # Get the Series of data types in the specified column
    data_types = dataframe[column_name].apply(type)
    
    # Count the occurrences of each data type
    data_type_counts = data_types.value_counts().to_dict()
    
    # Convert the types to their string representations for better readability
    data_type_counts_str = {str(data_type): count for data_type, count in data_type_counts.items()}
    
    # Create a summary dictionary
    summary = {
        "column_name": column_name,
        "data_type_counts": data_type_counts_str,
    }
    
    return summary


def check_duplicates_summary(dataframe, column_name):
    """
    Check for duplicated values in a specific column of a DataFrame and return a summary.
    
    Parameters:
        dataframe (pd.DataFrame): The DataFrame to check for duplicates.
        column_name (str): The name of the column to check for duplicates.
        
    Returns:
        pd.DataFrame: A summary DataFrame with information about duplicated values.
    """
    # Check if the specified column exists in the DataFrame
    if column_name not in dataframe.columns:
        return {"error": f"Column '{column_name}' not found in the DataFrame"}
    
    # Get the duplicated rows based on the specified column
    duplicated_rows = dataframe[dataframe.duplicated(subset=[column_name], keep=False)]
    
    # Count the occurrences of each duplicated value
    duplicated_counts = duplicated_rows[column_name].value_counts()
    
    # Create a summary DataFrame
    summary = pd.DataFrame({
        'Duplicated Value': duplicated_counts.index,
        'Occurrences': duplicated_counts.values
    })
    
    # Sort the summary by the number of occurrences
    summary = summary.sort_values(by='Occurrences', ascending=False)
    
    return summary


def remove_duplicates(dataframe, column_name):
    """
    Remove duplicate rows from a DataFrame based on a specified column.

    Args:
        dataframe (pd.DataFrame): Input DataFrame.
        column_name (str): Name of the column to check for duplicates.

    Returns:
        pd.DataFrame: DataFrame with duplicate rows removed.
    """
    # Check if the column exists in the DataFrame
    if column_name not in dataframe.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Determine the number of rows before removing duplicates
    initial_rows = dataframe.shape[0]

    # Remove duplicates based on the specified column
    df_cleaned = dataframe.drop_duplicates(subset=column_name, keep='first')

    # Determine the number of rows after removing duplicates
    cleaned_rows = df_cleaned.shape[0]

    # Calculate the number of duplicate rows removed
    duplicates_removed = initial_rows - cleaned_rows

    # Print a summary of the operation
    print(f"Removed {duplicates_removed} duplicate rows based on '{column_name}' column.")

    return df_cleaned


# def check_none_values(dataframe, column_name):
#     """
#     Check for None values in a specific column of a DataFrame and return a summary.
    
#     Args:
#         dataframe (pd.DataFrame): The DataFrame to check.
#         column_name (str): The name of the column to check for None values.
        
#     Returns:
#         dict: A summary dictionary containing information about None values.
#     """
#     # Check if the specified column exists in the DataFrame
#     if column_name not in dataframe.columns:
#         return {"error": f"Column '{column_name}' not found in the DataFrame"}
    
#     # Count the number of None values in the specified column
#     num_none_values = dataframe[column_name].isnull().sum()
    
#     # Get the total number of rows in the DataFrame
#     total_rows = len(dataframe)
    
#     # Create a summary dictionary
#     summary = {
#         "column_name": column_name,
#         "total_rows": total_rows,
#         "num_none_values": num_none_values,
#     }
    
#     return summary


def check_none_values(dataframe, column_name, check_other_columns=False, min_none_null_values=4):
    """
    Check for None values in a specific column of a DataFrame and optionally check for rows with too few non-null values.
    
    Args:
        dataframe (pd.DataFrame): The DataFrame to check.
        column_name (str): The name of the column to check for None values.
        check_other_columns (bool, optional): Whether to check for non-null values in other columns as well.
        min_none_null_values (int, optional): The minimum number of non-null values a row must have to be kept.
        
    Returns:
        dict: A summary dictionary containing information about None values and optional row counts.
    """
    # Check if the specified column exists in the DataFrame
    if column_name not in dataframe.columns:
        return {"error": f"Column '{column_name}' not found in the DataFrame"}
    
    # Count the number of None values in the specified column
    num_none_values = dataframe[column_name].isnull().sum()
    
    # Initialize variables for optional checks
    rows_below_threshold = 0
    
    # Check for rows with too few non-null values (if requested)
    if check_other_columns:
        num_columns = len(dataframe.columns)
        min_non_null_required = num_columns - min_none_null_values
        rows_below_threshold = (dataframe.notnull().sum(axis=1) < min_non_null_required).sum()
    
    # Get the total number of rows in the DataFrame
    total_rows = len(dataframe)
    
    # Create a summary dictionary
    summary = {
        "column_name": column_name,
        "total_rows": total_rows,
        "num_none_values": num_none_values,
        "rows_below_threshold": rows_below_threshold if check_other_columns else None,
    }
    
    return summary


# def remove_none_values(dataframe, column_name):
#     """
#     Remove rows with None values in a specific column of a DataFrame.
    
#     Args:
#         dataframe (pd.DataFrame): The DataFrame to remove rows from.
#         column_name (str): The name of the column to check for None values.
        
#     Returns:
#         pd.DataFrame: A new DataFrame with rows containing None values removed.
#     """
#     # Check if the specified column exists in the DataFrame
#     if column_name not in dataframe.columns:
#         raise ValueError(f"Column '{column_name}' not found in the DataFrame")
    
#     # Create a new DataFrame by filtering out rows with None values in the specified column
#     cleaned_dataframe = dataframe[dataframe[column_name].notnull()]
    
#     return cleaned_dataframe


def remove_none_values(dataframe, column_name, remove_none_rows=False, min_none_values=4):
    """
    Remove rows with None values in a specific column of a DataFrame, optionally remove rows with too few None values.
    
    Args:
        dataframe (pd.DataFrame): The DataFrame to remove rows from.
        column_name (str): The name of the column to check for None values.
        remove_none_rows (bool): Whether to remove rows with None values in the entire DataFrame. Default is False.
        min_none_values (int): The minimum number of None values that a row must have to be kept. Default is 4.
        
    Returns:
        pd.DataFrame: A new DataFrame with specified rows containing None values removed.
    """
    # Check if the specified column exists in the DataFrame
    if column_name not in dataframe.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame")
    
    # Remove None values in the specified column
    dataframe = dataframe.copy()
    dataframe[column_name] = dataframe[column_name].dropna()
    
    # Remove None rows if specified
    if remove_none_rows:
        num_none_values = dataframe.isnull().sum(axis=1)
        dataframe = dataframe[num_none_values <= min_none_values]
    
    return dataframe


def transform_to_numeric(dataframe, column_name):
    """
    Transform the values of a column to numeric type, with special handling for "free to play".
    
    Args:
        dataframe (pd.DataFrame): The DataFrame containing the column to transform.
        column_name (str): The name of the column to transform.
        
    Returns:
        dict: A summary containing information about the transformation.
    """
    # Check if the specified column exists in the DataFrame
    if column_name not in dataframe.columns:
        return {"error": f"Column '{column_name}' not found in the DataFrame"}
    
    numeric_count = 0
    non_numeric_count = 0
    stored_info = []
    
    # Convert "free to play" and "free" to numeric
    free_list = ["free to play", "free", "Free Demo", "Free to Use", "Free Mod", "Free to try", "Install Theme", "Play the Demo", "Play for Free!", "Install Now", "Play WARMACHINE: Tactics Demo", "Third-party", "play now", "Free HITMAN™ Holiday Pack"]
    dataframe[column_name] = np.where(
        dataframe[column_name].str.lower().isin(free_list), 0, dataframe[column_name]
    )
    
    # Convert values to numeric using pd.to_numeric
    numeric_values = pd.to_numeric(dataframe[column_name], errors="coerce")
    numeric_mask = numeric_values.notnull()
    
    # Update the original column with numeric values
    dataframe.loc[numeric_mask, column_name] = numeric_values[numeric_mask]
    
    non_numeric_mask = ~numeric_mask
    non_numeric_count = non_numeric_mask.sum()
    
    # Store non-numeric values information
    stored_info = [
        {"index": index, "value": value}
        for index, value in dataframe[column_name][non_numeric_mask].items()
    ]
    
    total_values = len(dataframe)
    numeric_count = numeric_mask.sum()
    
    # Create a summary dictionary
    summary = {
        "total_values": total_values,
        "numeric_count": numeric_count,
        "non_numeric_count": non_numeric_count,
        "stored_info": stored_info
    }
    
    return summary