"""
This module provides functions to transform and standardize data.

Available Functions:
- check_duplicates_summary: Check for duplicated values in a specific column.
- check_none_values: Check for None values in a specific column.
- column_data_types_summary: Generate a summary of data types present in a specified column.
- convert_to_numeric: Converts a value to numeric type if possible, otherwise returns original value.
- convert_list_to_numeric: Converts values of a list to numeric type using the convert_to_numeric function.
- convert_column_to_numeric: Converts values of a column to numeric type using convert_list_to_numeric function.
- convert_to_date: Converts a value to datetime type with the pattern 'yyyy-mm-dd'.
- convert_list_to_dates: Converts a list of values to datetime type using the convert_to_date function.
- convert_column_to_dates: Converts values of a column to datetime type using convert_list_to_dates function.
- extract_values: Extract values from nested data.
- remove_duplicates: Remove duplicate rows from a DataFrame based on a specified column.
- remove_none_values: Remove rows with None values in a specific column of a DataFrame.
- convert_special_strings: Converts str values of a column to numeric type based on specific rules.
"""

from datetime import datetime
import pandas as pd


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


def convert_to_numeric(value):
    """
    Converts a value to numeric type if possible, otherwise returns the original value.

    Args:
        value: The value to be converted.

    Returns:
        msj_fail (bool): Indicates True if conversion is successful
        val_numeric: The numeric value if conversion is successful, otherwise the original value.
    """
    msj_fail = False
    if type(value) not in (int, float):
        try:
            # Attempt to convert the value to a numeric type
            val_numeric = pd.to_numeric(value)
            return msj_fail, val_numeric
        except (ValueError, TypeError):
            # If conversion fails, return the original value
            msj_fail = True
            return msj_fail, value
    else:
        return msj_fail, value


def convert_list_to_numeric(lst):
    """
    Recursively converts a list of values to numeric type using the convert_to_numeric function.

    Args:
        lst: The list of values to be converted.

    Returns:
        msj_fail (bool): Indicates True if conversion is successful.
        report_dic (dic): Reports values that couldn't be converted.
        converted_list: The list with converted values or original values.
    """
    msj_fail = False
    converted_list = []
    report_dic = {}

    for idx_list, value in enumerate(lst):

        # Convert the value to numeric using the convert_to_numeric function
        msj_val, analyzed_val = convert_to_numeric(value)

        # Storing value in returning list
        converted_list.append(analyzed_val)
        
        # Report of fail convertion
        if msj_val:
            msj_fail = True
            # Storing report of idx and value
            report_dic[idx_list] = analyzed_val

    return msj_fail, report_dic, converted_list


def convert_column_to_numeric(dataframe, column_name):
    """
    Converts the values of a column in a DataFrame to numeric type.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the column to convert.
        column_name (str): The name of the column to convert.

    Returns:
        dict: A summary containing information about the conversion.
    """
    if column_name not in dataframe.columns:
        return {"error": f"Column '{column_name}' not found in the DataFrame"}

    converted_values = []
    report = {}

    for idx, row in dataframe.iterrows():
        value = row[column_name]
        if isinstance(value, list):
            msj, report_dic, converted_list = convert_list_to_numeric(value)
            if msj:
                report[idx] = report_dic
            converted_values.append(converted_list)
        else:
            msj, converted_value = convert_to_numeric(value)
            if msj:
                report[idx] = value
            converted_values.append(converted_value)

    dataframe[column_name] = converted_values

    summary = {
        "total_rows": len(dataframe),
        "column_name": column_name,
        "num_failed_conversions": len(report),
        "report": report
    }

    return summary


def convert_to_date(value, original_patterns=None):
    """
    Converts a value to datetime type with the pattern 'yyyy-mm-dd'.

    Args:
        value: The value to be converted.
        original_patterns: Optional list of possible original date patterns.

    Returns:
        converted_value: Converted datetime object or original value if conversion fails.
        success: True if conversion was successful, False otherwise.
    """
    if isinstance(value, str):
        if original_patterns is None:
            original_patterns = ["%Y-%m-%d"]
        
        desired_format = "%Y-%m-%d"
        
        for pattern in original_patterns:
            try:
                original_date = datetime.strptime(value, pattern)
                converted_value = original_date.strftime(desired_format)
                return converted_value, True
            except ValueError:
                pass
        
        return value, False
    else:
        return value, False


def convert_list_to_dates(lst, original_patterns=None):
    """
    Converts a list of values to datetime type using the convert_to_date function.

    Args:
        lst: The list of values to be converted.
        original_patterns: Optional list of possible original date patterns.

    Returns:
        success: True if all conversions were successful, False otherwise.
        report: Dictionary containing index-value pairs of values that couldn't be converted.
        converted_list: The list with converted values or original values.
    """
    success = True
    converted_list = []
    report = {}

    for idx, value in enumerate(lst):
        converted_value, conversion_success = convert_to_date(value, original_patterns)
        if not conversion_success:
            success = False
            report[idx] = value
        converted_list.append(converted_value)

    return success, report, converted_list


def convert_column_to_dates(dataframe, column_name, original_patterns=None):
    """
    Converts the values of a column in a DataFrame to datetime type using the convert_list_to_dates function.

    Args:
        dataframe: The DataFrame containing the column to be converted.
        column_name: The name of the column to be converted.
        original_patterns: Optional list of possible original date patterns.

    Returns:
        summary: A summary dictionary containing information about the conversion.
    """
    if column_name not in dataframe.columns:
        return {"error": f"Column '{column_name}' not found in the DataFrame"}

    converted_values = []
    report = {}

    for idx, row in dataframe.iterrows():
        value = row[column_name]
        if isinstance(value, list):
            msj, report_dic, converted_list = convert_list_to_dates(value, original_patterns)
            if not msj:
                report[idx] = report_dic
            converted_values.append(converted_list)
        else:
            converted_value, msj = convert_to_date(value, original_patterns)
            if not msj:
                report[idx] = value
            converted_values.append(converted_value)

    dataframe[column_name] = converted_values

    summary = {
        "total_rows": len(dataframe),
        "column_name": column_name,
        "num_failed_conversions": len(report),
        "report": report
    }

    return summary


def extract_values(dataframe, column_name, keys, new_columns):
    """
    Extract values from nested data.
    
    Parameters:
    - dataframe: DataFrame containing the data.
    - column_name: Name of the column to extract the data.
    - keys: A list with the name of the keys.
    - new_columns: A list with the names of the new columns.

    Returns:
        dataframe: DataFrame containing the data.
    """
    # Evaluating lenght of keys and new_columns lists
    if len(keys) != len(new_columns):
        raise ValueError("keys and new_columns length must be the same")

    # Createing new columns in the dataframe using new_columns
    for column in new_columns:
        dataframe[column] = pd.Series([], dtype='object')

    # Reading each value of the column
    for indx_column_name, value in dataframe[column_name].items():

        extracted_values = {key: [] for key in keys}

        # Extracting items from dictionaries based on a key
        for item in value:
            for key in keys:
                if item.get(key) is not None:
                    extracted_values[key].append(item.get(key))
                else:
                    extracted_values[key].append(None)

        # Going through every new column to store extracted values
        for indx_new_column, column in enumerate(new_columns):
            
            indx_extracted_values = keys[indx_new_column]
            
            if indx_extracted_values in extracted_values:
                # without assigning the values to a variable returns an error
                key_value = extracted_values[indx_extracted_values] 
            
            dataframe.at[indx_column_name, column] = key_value
    
    return dataframe


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

def remove_none_values(dataframe, column_name):
    """
    Remove rows with None values in a specific column of a DataFrame.
    
    Args:
        dataframe (pd.DataFrame): The DataFrame to remove rows from.
        column_name (str): The name of the column to check for None values.
        
    Returns:
        pd.DataFrame: A new DataFrame with rows containing None values removed.
    """
    # Check if the specified column exists in the DataFrame
    if column_name not in dataframe.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame")
    
    # Create a new DataFrame by filtering out rows with None values in the specified column
    cleaned_dataframe = dataframe[dataframe[column_name].notnull()]
    
    return cleaned_dataframe


# def remove_none_values(dataframe, column_name, remove_none_rows=False, min_none_values=4):
#     """
#     Remove rows with None values in a specific column of a DataFrame, optionally remove rows with too few None values.
    
#     Args:
#         dataframe (pd.DataFrame): The DataFrame to remove rows from.
#         column_name (str): The name of the column to check for None values.
#         remove_none_rows (bool): Whether to remove rows with None values in the entire DataFrame. Default is False.
#         min_none_values (int): The minimum number of None values that a row must have to be kept. Default is 4.
        
#     Returns:
#         pd.DataFrame: A new DataFrame with specified rows containing None values removed.
#     """
#     # Check if the specified column exists in the DataFrame
#     if column_name not in dataframe.columns:
#         raise ValueError(f"Column '{column_name}' not found in the DataFrame")
    
#     # Remove None values in the specified column
#     dataframe = dataframe.copy()
#     dataframe[column_name] = dataframe[column_name].dropna()
    
#     # Remove None rows if specified
#     if remove_none_rows:
#         num_none_values = dataframe.isnull().sum(axis=1)
#         dataframe = dataframe[num_none_values <= min_none_values]
    
#     return dataframe


# def convert_special_strings(dataframe, column_name, special_strings, converted_value):
#     """
#     Converts special strings to a numeric value in a specified column of a DataFrame.

#     Args:
#         dataframe (pd.DataFrame): The DataFrame containing the column to convert.
#         column_name (str): The name of the column to convert.
#         special_strings (list): List of special strings to convert.
#         converted_value: The numeric value to convert the special strings to.

#     Returns:
#         dict: A summary containing information about the conversion.
#     """
#     if column_name not in dataframe.columns:
#         return {"error": f"Column '{column_name}' not found in the DataFrame"}

#     total_rows = len(dataframe)
#     num_failed_conversions = 0
#     report = {}

#     # Convert the special strings to lowercase
#     special_strings_lower = [s.lower() for s in special_strings]

#     for idx, value in enumerate(dataframe[column_name]):
#         if type(value) not in (int, float):
#             lowercase_value = value.lower()
#             if lowercase_value in special_strings_lower:
#                 dataframe.at[idx, column_name] = converted_value
#             else:
#                 try:
#                     numeric_value = pd.to_numeric(value, errors="raise")
#                     dataframe.at[idx, column_name] = numeric_value
#                 except (ValueError, TypeError):
#                     num_failed_conversions += 1
#                     report[idx] = value
#         else:
#             dataframe.at[idx, column_name] = value

#     summary = {
#         "total_rows": total_rows,
#         "column_name": column_name,
#         "num_failed_conversions": num_failed_conversions,
#         "report": report
#     }

#     return summary


def convert_special_strings(dataframe, column_name, special_strings, converted_value):
    """
    Converts special strings to a numeric value in a specified column of a DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the column to convert.
        column_name (str): The name of the column to convert.
        special_strings (list): List of special strings to convert.
        converted_value: The numeric value to convert the special strings to.

    Returns:
        dict: A summary containing information about the conversion.
    """
    if column_name not in dataframe.columns:
        return {"error": f"Column '{column_name}' not found in the DataFrame"}

    total_rows = len(dataframe)
    num_failed_conversions = 0
    report = {}

    # Convert the special strings to lowercase
    special_strings_lower = set(map(str.lower, special_strings))

    def convert_value(row):
        value = row[column_name]
        index = row.name
        if pd.isna(value):
            return value
        if isinstance(value, str):
            lowercase_value = value.lower()
            if lowercase_value in special_strings_lower:
                return converted_value
            try:
                numeric_value = pd.to_numeric(value, errors="raise")
                return numeric_value
            except (ValueError, TypeError):
                nonlocal num_failed_conversions
                num_failed_conversions += 1
                report[index] = value
        return value

    dataframe[column_name] = dataframe.apply(convert_value, axis=1)

    summary = {
        "total_rows": total_rows,
        "column_name": column_name,
        "num_failed_conversions": num_failed_conversions,
        "report": report
    }

    return summary