"""
This module provides functions for the API.

Available functions:
- safe_literal_eval: Safely evaluates a string containing a Python literal using ast.literal_eval.
"""


import ast
import pandas as pd


path_1u = r"api\datasets\user_data_1.csv"
path_1g = r"api\datasets\games_data_1.csv"

   
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

    # Converting to its corresponding data types
    #users_dataframe['item_id'] = users_dataframe['item_id'].apply(safe_literal_eval)
    games_dataframe = games_dataframe.applymap(safe_literal_eval)

    # converting value to list type if possible
    id_item = users_dataframe.loc[users_dataframe['user_id'] == str(user_id), 'item_id'].values[0]
    id_item = safe_literal_eval(id_item)
    
    # Calculating total money spent
    total_price = 0

    for id_value in id_item:
        matching_rows = games_dataframe[games_dataframe['id'] == id_value]
        if not matching_rows.empty:
            total_price += matching_rows['price'].sum()

    # Calculating percentage
    # converting value to list type if possible
    id_recommend = users_dataframe.loc[users_dataframe['user_id'] == str(user_id), 'recommend'].values[0]
    id_recommend = safe_literal_eval(id_item)

    id_items_count = users_dataframe.loc[users_dataframe['user_id'] == str(user_id), 'items_count'].values[0]

    num_rcmnd = 0

    for id_rcmnd in id_recommend:
        if isinstance(id_recommend, list) and len(id_recommend) != 0:
            if id_rcmnd:
                num_rcmnd += 1

    percentage = num_rcmnd / id_items_count

    # rounding values
    total_price = round(total_price, 2)
    percentage = round(percentage, 2)

    return total_price, percentage