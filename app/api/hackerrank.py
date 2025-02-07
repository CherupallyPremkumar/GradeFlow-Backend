from fastapi import APIRouter, HTTPException
import requests
from bs4 import BeautifulSoup

hackerrank = APIRouter()
HACKERRANK_API = "https://www.hackerrank.com/rest/hackers/{}/badges"

def get_hackerrank_data(username):
    """Fetch user details from HackerRank."""
    try:
        response = requests.get(HACKERRANK_API.format(username))
        data = response.json()
        if not data.get("status"):
            raise ValueError("Invalid HackerRank username")

        problem_solving = next((badge for badge in data["models"] if badge["badge_type"] == "problem-solving"), {})
        return {
            "platform": "HackerRank",
            "username": username,
            "hacker_rank": problem_solving.get("hacker_rank", "Unknown"),
            "stars": problem_solving.get("stars", 0),
            "problems_solved": problem_solving.get("solved", 0),
            "total_challenges": problem_solving.get("total_challenges", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@hackerrank.get("/hackerrank/{username}")
async def get_hackerrank_profile(username: str):
    url = f"https://www.hackerrank.com/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found on HackerRank")

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract username
    profile_name = soup.find("h1", class_="profile-heading")
    user_display_name = profile_name.text.strip() if profile_name else username

    # Extract stars (rating)
    stars_section = soup.find("span", class_="hacker-badge")
    stars = stars_section.text.strip() if stars_section else "N/A"

    # Extract badges
    badges_section = soup.find_all("div", class_="hacker-badge")
    badges = [badge.text.strip() for badge in badges_section] if badges_section else []

    # Extract solved problems (approximate from the skills section)
    solved_section = soup.find("div", class_="profile-scores")
    solved_problems = solved_section.text.strip().split()[0] if solved_section else "N/A"

    return {
        "username": user_display_name,
        "stars": stars,
        "badges": badges,
        "solved_problems": solved_problems
    }
@hackerrank.get("/hackerrank/{username}/badges")
async def get_hackerrank_badges(username: str):
    hackerrank_data = get_hackerrank_data(username)


