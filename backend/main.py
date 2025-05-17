from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_utils import get_llm_recommendation
from typing import Dict

app = FastAPI()

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserData(BaseModel):
    education: str
    experience: str
    tech_knowledge: list[str]
    interests: str
    goal: str
    companies: str
    learning_style: str
    time_commitment: int
    other_constraints: str

@app.get("/")
def root() -> Dict[str, str]:
    """Root endpoint with a welcome message."""
    return {"message": "Welcome to the Career & Salary Estimator API!"}

@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/recommend")
def recommend(user_data: UserData) -> Dict[str, str]:
    """Generate a career and salary recommendation report."""
    llm_result = get_llm_recommendation(user_data.dict())
    return llm_result 