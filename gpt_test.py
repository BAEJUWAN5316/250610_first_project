# gpt_test.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

GPT_API_URL = "https://dev.wenivops.co.kr/services/openai-api"

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask_gpt", response_class=HTMLResponse)
def ask_gpt(request: Request, question: str = Form(...)):
    data = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
    ]

    response = requests.post(GPT_API_URL, json=data)
    answer = response.json()["choices"][0]["message"]["content"]

    return templates.TemplateResponse("answer.html", {
        "request": request,
        "question": question,
        "answer": answer
    })

@app.get("/")