"""
This module provides functions for the API.

Available functions:
- safe_literal_eval: Safely evaluates a string containing a Python literal using ast.literal_eval.
"""


import ast
import os
from datetime import datetime
import pandas as pd


# Get the current working directory
current_directory = os.getcwd()

# Construct an absolute file path
path_1u = os.path.join(current_directory, 'api', 'datasets', 'user_data_1.csv')
path_1g = os.path.join(current_directory, 'api', 'datasets', 'games_data_1.csv')
path_2u = os.path.join(current_directory, 'api', 'datasets', 'user_data_2.csv')


# path_1u = r"api\datasets\user_data_1.csv"
# path_1g = r"api\datasets\games_data_1.csv"

   
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
    

def money_spent(user_id: str) -> int:
    """Check for the money spent by the user and the percentage of recommendation."""
    
    # Calling dataframes from files
    users_dataframe = pd.read_csv(path_1u)
    games_dataframe = pd.read_csv(path_1g)

    # Filter the DataFrame for the specific user ID
    user_data = users_dataframe.loc[users_dataframe['user_id'] == str(user_id)]

    # Check if any rows match the user ID
    if not user_data.empty:
        # Extract values with error handling for NaN
        id_item = user_data['item_id'].values[0] if not user_data['item_id'].isna().any() else 0
        id_item = safe_literal_eval(id_item)
        id_recommend = user_data['recommend'].values[0] if not user_data['recommend'].isna().any() else 0
        id_recommend = safe_literal_eval(id_recommend)
        id_items_count = user_data['items_count'].values[0] if not user_data['items_count'].isna().any() else 0
    else:
        # Handle the case where no matching rows were found for the user ID
        id_item = 0
        id_recommend = 0
        id_items_count = 0
    
    # Calculating total money spent
    total_price = 0

    if type(id_item) == list and len(id_item) != 0:
        for id_value in id_item:
            matching_rows = games_dataframe[games_dataframe['id'] == id_value]
            if not matching_rows.empty:
                total_price += matching_rows['price'].sum()

    # Calculating percentage
    num_rcmnd = 0

    if type(id_recommend) == list and len(id_recommend) != 0:
        for id_rcmnd in id_recommend:
            if id_rcmnd:
                num_rcmnd += 1

    if id_items_count != 0:
        percentage = 100*(num_rcmnd / id_items_count)
    else:
        percentage = 0

    # rounding values
    total_price = round(total_price, 2)
    percentage = round(percentage, 2)

    return total_price, percentage


def valid_date_string(date_str):
    """Check for valid "yyyy-mm-dd" date pattern"""
    date_str = date_str.strip()  # Remove leading and trailing spaces
    
    try:
        # Attempt to parse the date string
        datetime.strptime(date_str, "%Y-%m-%d")
        return True  # It's a valid date in the "yyyy-mm-dd" format
    except ValueError:
        return False  # It's not a valid date in the expected format
    

def date_in_range(dates_list, start_date, end_date):
    """Check for dates within a range of dates."""
    # Initialize a list to store the valid dates
    idx_valid_dates = []
    v_in_list = False

    for indx_date, date_str in enumerate(dates_list):
        try:
            # Convert the date string to a datetime object
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            # Check if the date is in range
            if start_date <= date_obj <= end_date:
                idx_valid_dates.append(indx_date)
                v_in_list = True
        except ValueError:
            # Handle invalid date strings here if needed
            pass

    return v_in_list, idx_valid_dates


def num_user_review(dates: str) -> int:
    """Check for the number of users that made a review and the percentage of recommendations."""

    # Load data from a CSV file into a DataFrame (adjust path_2u to your file path)
    recommendations_df = pd.read_csv(path_2u)

    # Converting into their respective data types
    recommendations_df = recommendations_df.applymap(safe_literal_eval)

    # Split the date range into start and end dates
    start_date, end_date = dates.split()

    try:
        # Convert start_date and end_date to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format in date_range. Use 'yyyy-mm-dd' format.")
    
    # Initialize counters
    count = 0
    positive = 0
    negative = 0

    # Iterating over rows of the DataFrame
    for idx_row, row in recommendations_df.iterrows():
        list_verf, idx_dates = date_in_range(row['posted'], start_date, end_date)
        
        # Calculating the number of users with valid dates
        if list_verf:
            count += 1
        
        # Calculating recommendations
        for idx in idx_dates:
            if idx < len(row["recommend"]):
                if row["recommend"][idx]:
                    positive += 1
                else:
                    negative += 1
    
    # Calculating percentage based on total recommendations made within the range of dates
    if positive + negative != 0:
        total_recommendations = positive + negative
        percentage = (positive / total_recommendations) * 100
    else: 
        percentage = 0

    return count, round(percentage, 2)