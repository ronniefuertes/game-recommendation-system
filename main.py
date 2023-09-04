"""API to extract the information of steam games and user's reviews and items"""

from fastapi import FastAPI
from api.api_utils import money_spent, num_user_review


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
    money_info, percentage = money_spent(user_id)
    
    return {'User ID:':money_info, 'recommendation_percentage':percentage}


@app.get('/countreviews/{dates}')
def countreviews(dates:str):
    """
    Insert dates to see the amount of users that made reviews and the percentage of recommendation.

    Dates must be in yyyy-mm-dd format, separated with blank space.
    
    Percentage value is rounded.
    """
    num_users, percentage = num_user_review(dates)
    
    return {'User ID:':num_users, 'recommendation_percentage':percentage}