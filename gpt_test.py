# gpt_test.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = {"김김":"123abc", "나나":"ab12"}

GPT_API_URL = "https://dev.wenivops.co.kr/services/openai-api"

@app.get("/question_gpt", response_class=HTMLResponse)
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

@app.get("/signup", response_class=HTMLResponse)
def show_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
def signup(id_signup: str = Form(...), pw_signup: str = Form(...)):
    if id_signup in users:
        return "이미 존재하는 사용자입니다."
    users[id_signup] = pw_signup
    return RedirectResponse(url="/", status_code=303)

@app.get("/", response_class=HTMLResponse)
def get_login(request : Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/")
def login(request : Request, id_login: str = Form(...), pw_login: str = Form(...)):
    if users.get(id_login) == pw_login:
        return templates.TemplateResponse("index.html", {"request": request})
    return "로그인 실패! 아이디 또는 비밀번호 확인"

