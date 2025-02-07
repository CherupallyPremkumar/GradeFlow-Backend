from datetime import datetime

from fastapi import FastAPI, HTTPException, APIRouter
import requests
from pydantic import BaseModel
from typing import List, Optional

# FastAPI instance
codeforces = APIRouter()


# Codeforces User Info Schema
class UserInfo(BaseModel):
    handle: str
    rating: Optional[int]
    maxRating: Optional[int]
    rank: Optional[str]
    maxRank: Optional[str]
    avatar: Optional[str]


# Fetch user information from Codeforces API
def get_user_info(username: str):
    url = f"https://codeforces.com/api/user.info?handles={username}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching data from Codeforces API")

    data = response.json()

    if data["status"] != "OK":
        raise HTTPException(status_code=404, detail="User not found")

    user_info = data["result"][0]
    # API to get contest rating
    url = f"https://codeforces.com/api/user.rating?handle={username}"

    response = requests.get(url)
    data = response.json()

    # Check if the response was successful
    if data["status"] == "OK":
        print(
            f"{'Contest #':<10}{'Contest':<40}{'Start Time':<20}{'Rank':<10}{'Solved':<10}{'Rating Change':<15}{'New Rating'}")
        print("=" * 100)  # Separator line

        for contest in data["result"]:
            print(contest)
            contest_id = contest.get("contestId", "N/A")
            contest_name = contest.get("contestName", "N/A")
            rank = contest.get("rank", "N/A")
            old_rating = contest.get("oldRating", "N/A")
            new_rating = contest.get("newRating", "N/A")

            # Rating change
            rating_change = new_rating - old_rating if new_rating != "N/A" and old_rating != "N/A" else "N/A"

            # Convert start time (in seconds) to a readable format
            start_time = contest.get("ratingUpdateTimeSeconds", "N/A")
            if start_time != "N/A":
                start_time = datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')

            # Problems Solved - Count the number of problems solved (just an example, modify accordingly)
            problems = contest.get("solved", [])
            solved = sum(
                1 for problem in problems if problem.get("solved", False))  # Assuming problem data has 'solved' key

            # Print contest details in a formatted manner
            print(
                f"{contest_id:<10}{contest_name:<40}{start_time:<20}{rank:<10}{solved:<10}{rating_change:<15}{new_rating}")
    else:
        print("Failed to fetch contest data.")

    return UserInfo(
        handle=user_info['handle'],
        rating=user_info.get('rating'),
        maxRating=user_info.get('maxRating'),
        rank=user_info.get('rank'),
        maxRank=user_info.get('maxRank'),
        avatar=user_info.get('avatar')
    )




# API Endpoint to get user profile
@codeforces.get("/user/{username}", response_model=UserInfo)
async def get_profile(username: str):
    return get_user_info(username)


# API Endpoint to get multiple user profiles
@codeforces.get("/users", response_model=List[UserInfo])
async def get_multiple_profiles(usernames: List[str]):
    user_infos = []
    for username in usernames:
        user_info = get_user_info(username)
        user_infos.append(user_info)
    return user_infos