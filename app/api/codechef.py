from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup

codechef = APIRouter()


@codechef.get("/codechef/{username}")
async def get_codechef_profile(username: str):
    url = f"https://www.codechef.com/users/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found on CodeChef")

    soup = BeautifulSoup(response.text, "html.parser")


    # Extract current rating
    rating_section = soup.find("div", class_="rating-number")
    rating = rating_section.text.strip() if rating_section else "N/A"

    # Extract highest rating
    highest_rating_section = soup.find("small")
    highest_rating = highest_rating_section.text.split()[-1] if highest_rating_section else "N/A"

    # Extract total problems solved
    problems_solved = soup.find("section", class_="rating-data-section problems-solved")
    solved_count = "0"
    if problems_solved:
        solved_text = problems_solved.find("h5")
        if solved_text:
            solved_count = solved_text.text.split()[-1]

    return {
        "username": username,
        "current_rating": rating,
        "highest_rating": highest_rating,
        "total_problems_solved": solved_count
    }