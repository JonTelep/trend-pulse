""" XAI API """
import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pytz


from tools.handler import api_handler

load_dotenv()

URL_DEEPSEARCH = "https://api.x.ai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


@api_handler(max_retries=0, retry_delay=10.0, timeout=30)
def get_xai_news():
    """ Get XAI news """
    
    # Get current time in EST for context
    est = pytz.timezone('America/New_York')
    end_time = datetime.now(est)
    start_time = end_time - timedelta(hours=24)
    
    # Format times for the prompt
    time_context = f"from {start_time.strftime('%I:%M %p EST %B %d, %Y')} to {end_time.strftime('%I:%M %p EST %B %d, %Y')}"

    payload = {
        "model": "grok-2-1212",
        "messages": [
            {
                "role": "system",
                "content": f"You are a news analyst with access to web and X data. Your task is to identify and rank the top 10 news events from the past 24 hours ({time_context}). For each event, provide a title, brief summary, and a verified source (please do not provide fake sources), and timestamp. Return the results as a raw, valid JSON object with an array of events under a 'results' key, each with fields: rank, title, summary, source, verified url, and timestamp. Ensure the response is structured, concise, and contains only valid JSON—no Markdown, no code blocks (e.g., ```json), no extra newlines, and no additional text outside the JSON object."
            },
            {
                "role": "user",
                "content": "Give me the top 10 news events of the past 24 hours in JSON format."
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.5
    }

    response = requests.post(URL_DEEPSEARCH, headers=HEADERS, data=json.dumps(payload), timeout=30)
    return response.json()
