from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import logging

# Initialize FastAPI app
app = FastAPI()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the API key from the environment variable
genai.configure(api_key="AIzaSyCW6IjnbUl7UxuWjQGsbgI_WgKUFsuSW2k")

# Initialize the GenerativeModel object
model = genai.GenerativeModel("gemini-1.5-flash")

extra = (
    "You are a highly knowledgeable AI tutor. "
    "You provide detailed, accurate, and concise answers to questions, explaining concepts as if you were teaching a student. "
    "Please use a friendly and engaging tone to ensure the student understands the explanation. "
    "If you encounter a question that you cannot answer or are not allowed to answer, "
    "please respond with a polite and understandable apology, explaining that you are unable to provide the information."
)


class Question(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    question: str
    answer: str


def generate_answer(question: str) -> str:
    """Sends the user question to the Gemini API and returns the answer."""
    try:
        response = model.generate_content(extra + " " + question)
        return response.text  # Assuming the response object has a 'text' attribute
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        raise HTTPException(status_code=500, detail="Error generating answer")


@app.post("/waseem-answer/", response_model=AnswerResponse)
async def generate_answer_view(question: Question):
    answer = generate_answer(question.question)
    return {"question": question.question, "answer": answer}


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI app!"}
