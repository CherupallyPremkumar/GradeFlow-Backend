import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

leetcode = APIRouter()

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

QUERY = """
query userProfileUserQuestionProgressV2($userSlug: String!) {
  userProfileUserQuestionProgressV2(userSlug: $userSlug) {
    numAcceptedQuestions {
      count
      difficulty
    }
    numFailedQuestions {
      count
      difficulty
    }
    numUntouchedQuestions {
      count
      difficulty
    }
    userSessionBeatsPercentage {
      difficulty
      percentage
    }
    totalQuestionBeatsPercentage
  }
}
"""


# Response model for the problem count by difficulty
class ProblemCountResponse(BaseModel):
    easy: int
    medium: int
    hard: int


# Fetch problem count by difficulty
def get_problem_count(user_slug: str):
    variables = {
        "userSlug": user_slug
    }

    # You need to provide the Authorization token here
    headers = {
        "Authorization": "Bearer YOUR_LEETCODE_TOKEN"
    }

    # Make the request to the GraphQL endpoint
    response = requests.post(LEETCODE_GRAPHQL_URL, json={'query': QUERY, 'variables': variables}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        user_profile = data.get("data", {}).get("userProfileUserQuestionProgressV2", {})

        # Extracting problem counts by difficulty
        num_accepted = user_profile.get("numAcceptedQuestions", [])
        problem_count = {"easy": 0, "medium": 0, "hard": 0}

        for entry in num_accepted:
            difficulty = entry.get("difficulty", "").lower()
            count = entry.get("count", 0)
            if difficulty in problem_count:
                problem_count[difficulty] = count

        return problem_count
    else:
        return None


# API endpoint to fetch problem count by difficulty
@leetcode.get("/get_problem_count/{user_slug}", response_model=ProblemCountResponse)
async def get_problem_count_api(user_slug: str):
    count = get_problem_count(user_slug)
    if count is not None:
        return ProblemCountResponse(**count)
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch problem count")

# Fetch user profile and other details from LeetCode
def fetch_leetcode_details(username: str):
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
    if response.status_code == 200:
        data = response.json()
        if "errors" in data:
            return {"error": "User not found on LeetCode"}
        return data["data"]
    else:
        return {"error": "Failed to fetch data from LeetCode API", "status_code": response.status_code}

# API endpoint to fetch LeetCode profile details
@leetcode.get("/leetcode/{username}")
async def get_leetcode_profile(username: str):
    data = fetch_leetcode_details(username)
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return data

