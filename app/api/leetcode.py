import requests
from fastapi import APIRouter

leetcode = APIRouter()

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"


def fetch_leetcode_details(username: str):
    """ Fetches user profile details, recent submissions, and contest ranking from LeetCode. """

    query = f"""
        {{
            matchedUser(username: "{username}") {{
                username
                profile {{
                    ranking
                    realName
                    userAvatar
                    countryName
                    reputation
                }}
                submissionCalendar
            }}
            recentAcSubmissionList(username: "{username}", limit: 5) {{
                title
                titleSlug
                timestamp
                statusDisplay
            }}
            userContestRanking(username: "{username}") {{
                rating
                globalRanking
                totalParticipants
            }}
        }}
        """

    response = requests.post(LEETCODE_GRAPHQL_URL, json={"query": query})
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        if "errors" in data:
            return {"error": "User not found on LeetCode"}
        return data["data"]
    else:
        return {"error": "Failed to fetch data from LeetCode API", "status_code": response.status_code}


@leetcode.get("/leetcode/{username}")
async def get_leetcode_profile(username: str):
    """ API endpoint to fetch LeetCode profile details """
    return fetch_leetcode_details(username)