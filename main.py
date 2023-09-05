"""API to extract the information of steam games and user's reviews and items"""

from fastapi import FastAPI
from api.api_utils import money_spent, num_user_review, genre_rank, top_users_in_genre


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
    
    return {'Money spent:':money_info, 'Recommendation percentage':percentage}


@app.get('/countreviews/{dates}')
def countreviews(dates:str):
    """
    Insert dates to see the amount of users that made reviews and the percentage of recommendation.

    Dates must be in yyyy-mm-dd format, separated with blank space.
    
    Percentage value is rounded.
    """
    num_users, percentage = num_user_review(dates)
    
    return {'Number of users:':num_users, 'Recommendation percentage':percentage}

@app.get('/genre/{genre_name}')
def genre(genre_name:str):
    """
    Insert the name of a genre to see the position in which a genre is found in the ranking of 
    the genres analyzed under the PlayTimeForever column.

    Name is case sensitive.

    0 will be display if genre is not found.
    """
    rank = genre_rank(genre_name)
    
    return {"rank_number: ": rank}


@app.get('/userforgenre/{genre_name}')
def userforgenre(genre_name:str):
    """
    Insert the name of a genre to see the top 5 users with the most time spended.

    Name is case sensitive.

    If genre not found, a message will appear.
    """
    top_users = top_users_in_genre(genre_name)
    
    return {"Top users: ": top_users}
