import requests
from fastapi import APIRouter, HTTPException

github = APIRouter()

GITHUB_API_URL = "https://api.github.com"

# Function to fetch public repositories for a given username
def get_github_repositories(username: str):
    url = f"{GITHUB_API_URL}/users/{username}"
    response = requests.get(url)
    print(response.json())

    if response.status_code == 200:
        return response.json()  # Returns a list of repositories
    else:
        return None

@github.get("/github/repositories/{username}")
async def get_github_repos(username: str):
    repos = get_github_repositories(username)
    if repos:
        return repos
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch repositories")