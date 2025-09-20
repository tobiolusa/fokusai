from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


# Load API key from environment
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE Token not set")

MODEL_NAME = "microsoft/DialoGPT-medium"
HF_API_URL = 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium'


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def chat(request : Request):
    return templates.TemplateResponse(
        request=request, name="index.html",
    )
