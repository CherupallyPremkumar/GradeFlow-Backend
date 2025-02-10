from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth_routes import auth_router
from app.api.codechef import codechef
from app.api.codeforces import codeforces
from app.api.hackerrank import hackerrank
from app.api.leetcode import leetcode
from app.api.routes import router

app = FastAPI(title="ATS Resume Checker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)  # Existing routes
app.include_router(leetcode)
app.include_router(codeforces)
app.include_router(codechef)
app.include_router(hackerrank)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Welcome to the ATS System"}
