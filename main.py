from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Question(BaseModel):
    message: str

@app.post("/ask_gpt")
def ask_gpt(question: Question):
    url = "https://dev.wenivops.co.kr/services/openai-api"
    response = requests.post(url, json={"message": question.message})
    get_reply = response.json()["message"]
    return {"answer":get_reply}


