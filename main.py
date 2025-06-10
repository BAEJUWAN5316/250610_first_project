from fastapi import FastAPI,Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()
templates = Jinja2Templates(directory="templates")