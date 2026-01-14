#Import the necessary libraries
import requests
import json
import pandas as pd

from main import ACCESS_TOKEN

def user_info():
    # Set the headers for the request
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }


    #Get the user profile
    response = requests.get("https://api.spotify.com/v1/me", headers= headers)

    #Get data in json format
    data = response.json()
    
    # Print the data
    # data=json.dumps(data, indent=3)
    # print(data)

    user_profile=[]

    user_profile.append({
            "user_id":data["id"],
            "user_display_name":data["display_name"],
            "follower_count":data["followers"]["total"],       
            })

    #Convert this data to a pandas dataframe for better readability and ease of ingestion
    df_user_profile=pd.DataFrame(user_profile)
    return df_user_profile
