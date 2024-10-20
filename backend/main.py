from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import openai
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from rag import (analyze_data, compare_data, get_sustainability_insights, get_christmas_insights,
    get_dataset_stats, retrieve_entries, compare_demographics, related_topics,
    custom_query, sentiment_analysis
)

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
app = FastAPI()

# Mount the frontend/static directory to serve static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

# Set up Jinja2 to serve HTML templates from the frontend directory
templates = Jinja2Templates(directory="../frontend")


class Query(BaseModel):
    text: str

class CustomQuery(BaseModel):
    text: str
    dataset: str = "sustainability"

# Set up OpenAI key (use environment variables in production)
openai.api_key = OPENAI_API_KEY


# @app.get("/")
# async def index():
#     return "Hello World, Welcome to my OpenAI powered R.A.G"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    data = get_dataset_stats()
    return templates.TemplateResponse("index.html", {"request": request,  "data": data})


@app.post("/submit/")
async def handle_form(query: str = Form(...)):
    print("Recieved Query", query)
    response = analyze_data(query)
    return {"message": response}
@app.post("/analyze/")
async def analyze(query: Query):
    response = analyze_data(query.text)
    return {"response": response}

@app.post("/compare/")
async def compare(query: Query):
    response = compare_data(query.text)
    return {"response": response}

@app.get("/sustainability_insights/")
async def sustainability_insights(query: Query):
    response = get_sustainability_insights(query.text)
    return {"response": response}

@app.get("/christmas_insights/")
async def christmas_insights(query: Query):
    response = get_christmas_insights(query.text)
    return {"response": response}


@app.get("/get_dataset_stats/")
async def dataset_stats():
    stats = get_dataset_stats()
    return {"dataset_stats": stats}

@app.post("/retrieve_entries/")
async def retrieve(query: CustomQuery):
    entries = retrieve_entries(query.text, query.dataset)
    return {"top_entries": entries}

@app.post("/compare_demographics/")
async def demographics(query: Query):
    response = compare_demographics(query.text)
    return {"demographic_comparison": response}

@app.get("/related_topics/")
async def topics():
    topics_list = related_topics()
    return {"related_topics": topics_list}

@app.post("/custom_query/")
async def custom(query: CustomQuery):
    response = custom_query(query.text, query.dataset)
    return {"custom_response": response}

@app.post("/sentiment_analysis/")
async def sentiment(query: CustomQuery):
    response = sentiment_analysis(query.text, query.dataset)
    return {"sentiment_analysis": response}