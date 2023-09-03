"""API to extract the information of steam games and user's reviews and items"""

from fastapi import FastAPI
from api.api_utils import money_spent


app_description = """
        API to extract the information of steam games and user's reviews and items.
        """

app = FastAPI(title="steam games and users data",description=app_description)


@app.get('/userdata/{user_id}')
def userdata(user_id:str):
    """
    Insert a user ID to see the amount of money spent and the percentage of recommendation.

    The user id is case sensitive.
    
    Resulting values are rounded.
    """
    money_info = money_spent(user_id)[0]
    percentage = money_spent(user_id)[1]
    
    return {'User ID:':money_info, 'recommendation_percentage':percentage}