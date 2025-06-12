from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import re
import httpx

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 가짜 유저 DB
users = {
    "test": {"password": "Test!1234", "email": "test@example.com"},
    "a": {"password": "a", "email": "testa@example.com"},
    "b": {"password": "b", "email": "testa@example.com"}
}

GPT_API_URL = "https://dev.wenivops.co.kr/services/openai-api"

# -------------------------------
# 페이지 라우팅
# -------------------------------

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request, username: str = Cookie(default=None)):
    if not username:
        return RedirectResponse("/login")
    return templates.TemplateResponse("index.html", {"request": request, "username": username})

# -------------------------------
# 로그인 처리
# -------------------------------

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(data: LoginData):
    user = users.get(data.username)
    if user and user["password"] == data.password:
        response = JSONResponse({"success": True})
        response.set_cookie(key="username", value=data.username)
        return response
    return JSONResponse({"success": False})

# -------------------------------
# 회원가입 처리
# -------------------------------

class SignupData(BaseModel):
    username: str
    password: str
    email: str

@app.post("/signup")
def signup(data: SignupData):
    if data.username in users:
        return JSONResponse({"success": False, "reason": "이미 존재하는 아이디입니다."})

    if len(data.username) < 4:
        return JSONResponse({"success": False, "reason": "아이디는 최소 4자 이상이어야 합니다."})

    if len(data.password) < 8:
        return JSONResponse({"success": False, "reason": "비밀번호는 최소 8자 이상이어야 합니다."})

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", data.password):
        return JSONResponse({"success": False, "reason": "비밀번호에 특수문자가 최소 하나 포함되어야 합니다."})

    if not re.search(r"[A-Za-z]", data.password):
        return JSONResponse({"success": False, "reason": "비밀번호에 영문자가 포함되어야 합니다."})

    users[data.username] = {"password": data.password, "email": data.email}
    return JSONResponse({"success": True})

# -------------------------------
# GPT 질문 처리
# -------------------------------

class QuestionData(BaseModel):
    question: str

@app.post("/ask")
async def ask_gpt(request: Request):
    data = await request.json()  # 클라이언트에서 온 JSON 데이터 읽기
    question = data.get("question")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
    ]

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(GPT_API_URL, json=messages, timeout=10.0)
            response.raise_for_status()
            response_data = response.json()
            answer = response_data["choices"][0]["message"]["content"]

            return JSONResponse({"answer": answer})

        except httpx.HTTPError as e:
            return JSONResponse({"answer": f"❌ 오류 발생: {str(e)}"})
