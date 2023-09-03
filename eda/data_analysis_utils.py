""" 
This module provides functions to transform and standardize data.

Available functions:
- calculate_total_price: Calculate the total price for a given list by matching them with a DataFrame.
- check_duplicates_summary: Check for duplicated values in a specific column of a DataFrame and return a summary.
- column_data_types_summary: Generate a summary of data types present in a specified column of a DataFrame.
- merge_values: Merge and update values from two columns of a DataFrame.
- report_summary: Create a summary dictionary containing indices and lists of values from a specified column in a DataFrame.
- safe_literal_eval: Safely evaluates a string containing a Python literal using ast.literal_eval.
"""


import ast
import pandas as pd


def calculate_total_price(id_item, dataframe, column_name_1, column_name_2):
    """
    Calculate the total price for a given list of IDs by matching them with a DataFrame.
    
    Parameters:
    - id_item: List of ID values to be used for calculations.
    - dataframe: The DataFrame containing the data for matching.
    - column_name_1: The name of the column in 'dataframe' used for ID comparisons.
    - column_name_2: The name of the column in 'dataframe' used for price summation.
    
    Returns:
    - total_price: The total sum of prices for matching IDs.
    - non_matching_ids: List of IDs from 'id_item' that did not have a match in 'dataframe'.
    """
    
    total_price = 0        # Initialize the total price to zero
    matching_ids = []      # Initialize an empty list to store matching IDs
    non_matching_ids = []  # Initialize an empty list to store non-matching IDs
    
    # Loop through each ID in the id_item list
    for id_value in id_item:
        # Filter 'dataframe' to get rows where 'column_name_1' matches the current ID
        matching_rows = dataframe[dataframe[column_name_1] == id_value]
        
        # Check if there are matching rows in the DataFrame
        if not matching_rows.empty:
            # Calculate the sum of 'column_name_2' for matching rows and add it to the total_price
            total_price += matching_rows[column_name_2].sum()
            matching_ids.append(id_value)  # Add the matching ID to the list
        else:
            non_matching_ids.append(id_value)  # Add the non-matching ID to the list
    
    return total_price, non_matching_ids


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



def merge_values(dataframe, column_name_1, column_name_2):
    """
    Merge and update values from two columns of a DataFrame, remove duplicates,
    and update the specified column with the merged and deduplicated values.
    
    Parameters:
    - dataframe: The DataFrame to operate on.
    - column_name_1: The name of the first column to merge and update.
    - column_name_2: The name of the second column to merge.
    
    """
    # Iterate over the rows of the dataframe
    for index, row in dataframe.iterrows():
        a_values = row[column_name_1]
        b_values = row[column_name_2]

        if type(a_values) == type(b_values) == list:
            t_values = a_values + b_values  # Merge lists
        elif type(a_values) == list:
            t_values = a_values  # Use only column_name_1
        elif type(b_values) == list:
            t_values = b_values  # Use only column_name_2
        else:
            t_values = []  # Both values are NaN
        
        # Creating a list with unique values
        unique_list = []
        [unique_list.append(x) for x in t_values if x not in unique_list]

        # Storing the list in the corresponding column
        dataframe.at[index, column_name_1] = unique_list  # Update the DataFrame


def report_summary(dataframe, column_name):
    """
    Create a summary dictionary containing indices and lists of values from a specified column in a DataFrame.

    Parameters:
    - dataframe: The DataFrame from which to extract data.
    - column_name: The name of the column in 'dataframe' containing lists of values.

    Returns:
    - summary: A dictionary where each key is the DataFrame index, and the value is a list of values from 'column_name.'
    """

    # Initialize an empty summary dictionary
    summary = {}

    # Iterate through the DataFrame to populate the summary
    for index, row in dataframe.iterrows():
        # Get the list of values from the specified column
        non_matching_values = row[column_name]
        
        # Check if the list is not empty
        if len(non_matching_values) != 0:
            # Add the index as the key and the list of values as the value in the summary dictionary
            summary[index] = non_matching_values

    return summary


def safe_literal_eval(s):
    """
    Safely evaluates a string containing a Python literal using ast.literal_eval.

    Parameters:
    - s: A string to be evaluated.

    Returns:
    - The evaluated Python literal if it's valid.
    - pass if the string is not a valid literal or if it contains NaN.
    """
    try:
        # Attempt to evaluate the string as a Python literal using ast.literal_eval
        return ast.literal_eval(s)
    except (ValueError, SyntaxError):
        # Handle exceptions (e.g., if the string is not a valid literal)
        return s  # Return the original value if it's not a valid literal


# def extract_non_valid_literals(df, column_name):
#     non_valid_literals_summary = {}

#     for index, value in df[column_name].items():
#         result = safe_literal_eval(value)
#         if isinstance(result, str):
#             non_valid_literals_summary[index] = value

#     return non_valid_literals_summary