from fastapi import APIRouter

github = APIRouter()


def fetch_github_details(username :str):
    pass


@github.get("/github/{username}")
async def get_leetcode_profile(username: str):
    """ API endpoint to fetch LeetCode profile details """
    return fetch_github_details(username)