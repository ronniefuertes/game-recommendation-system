# Steam Data Analysis API

This repository contains the code for building and deploying an API for Steam data analysis. The API is designed to provide insights and information based on Steam gaming platform data. It offers various endpoints to query and retrieve data related to user activity, game reviews, sentiment analysis, and more.

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Data Preparation](#data-preparation)
- [API Endpoints](#api-endpoints)
- [Machine Learning Model](#machine-learning-model)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Steam Data Analysis API is built using the FastAPI framework and provides the following functionalities:

1. **User Data**: Get information about a user, including money spent, recommendation percentage, and the number of items owned.

2. **Review Count by Date**: Retrieve the number of user reviews posted between two specified dates and their recommendation percentages.

3. **Genre Ranking**: Find the ranking of a genre based on playtime forever.

4. **Top Users by Genre**: Get the top 5 users who have spent the most hours playing games in a specific genre, along with their URLs and user IDs.

5. **Developer Insights**: Obtain information about game items and the percentage of free content by year, categorized by the developer.

6. **Sentiment Analysis**: Retrieve sentiment analysis statistics for user reviews based on the release year of the games.

7. **Machine Learning Recommendation**: Implement machine learning-based recommendation system.


## Requirements

To run the API and perform data analysis, you'll need the following:

- Python 3.7 or higher
- FastAPI
- Pandas
- spaCy (for sentiment analysis)
- WordCloud (for word cloud generation)
- Steam dataset (provided separately)

## Data Preparation

Before running the API, its necessary to ensure that the Steam dataset is properly formatted and loaded into the system. You can perform necessary data preprocessing and feature engineering as outlined in the requirements.

## API Endpoints

The API offers the following endpoints, including those for machine learning-based recommendations.

- `/userdata/{user_id}`: Get user data including money spent, recommendation percentage, and the number of items owned.

- `/countreviews/{start_date}/{end_date}`: Retrieve the number of user reviews posted between two specified dates and their recommendation percentages.

- `/genre/{genre}`: Find the ranking of a genre based on playtime forever.

- `/userforgenre/{genre}`: Get the top 5 users who have spent the most hours playing games in a specific genre, along with their URLs and user IDs.

- `/developer/{developer}`: Obtain information about game items and the percentage of free content by year, categorized by the developer.

- `/sentimentanalysis/{year}`: Retrieve sentiment analysis statistics for user reviews based on the release year of the games.

- `/recomendacion_juego/{product_id}`: Get a list of 5 recommended games similar to the one specified by the product ID.

## Machine Learning Models

Once the data is prepared and consumable by the API, it is ready for consumption by the Analytics and Machine Learning departments. The proposed approach for building a recommendation system is:

**Item-Item Recommendation System:**
   - Input: Game ID
   - Output: List of 5 recommended games similar to the input game using cosine similarity.

## Usage

To use the API, you can send GET requests to the specified endpoints, passing the required parameters as needed. The API will return the requested data in a JSON format.

## Deployment

Deployment of the API can be done using a cloud hosting service or a platform like Render. The API is accessible via the "https://gamesenseapi.onrender.com/docs" endpoint to be consumed by other applications.

## Contributing

Contributions to this project are welcome. Feel free to submit issues, feature requests, or pull requests as needed.

