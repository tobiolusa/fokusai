from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()


# Load API key from environment
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
if not HUGGINGFACE_TOKEN:
    raise ValueError("HUGGINGFACE Token not set")

MODEL_NAME = "microsoft/DialoGPT-medium"
HF_API_URL = 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium'


## Model 

class Question(BaseModel):
    question : str


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def chat(request : Request):
    return templates.TemplateResponse(
        request=request, name="index.html",
    )

@app.post('/')
async def question(q : Question):
    if not q.question:
        raise HTTPException(status_code=400, detail="Question cant be empty")
    payload = {
        "input" : 'q.question',
        "parameters" : {
            "max_length" : 200,
            "num_return_sequences" : 1
        }
    }

    headers = {
        "Authorization" : f"Bearer {HUGGINGFACE_TOKEN}",
        "Conten-Type" : "application/json"
    }
    
    try : 
        response = requests.post(HF_API_URL,headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and result :
            answer = result[0].get("generated_text", "No response genereated")
        else:
            answer = result.get("generated_text", "No response genereated")
        result 
        {"answer" : answer.strip()}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail = f"Error communicating with AI API : {str(e)}")  
    