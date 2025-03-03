""" XAI API """
import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pytz
import pathlib

from tools.handler import api_handler

load_dotenv()

URL_DEEPSEARCH = "https://api.x.ai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('GROK_API_KEY')}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


@api_handler(max_retries=0, retry_delay=10.0, timeout=30)
def get_xai_news():
    """ Get XAI news """
    # Get current time in EST
    est = pytz.timezone('America/New_York')
    end_time = datetime.now(est)
    start_time = end_time - timedelta(hours=24)

    payload = {
        "model": "grok-2-1212",
        "messages": [
            {
            "role": "system",
            "content": "You are a news analyst with access to web and X data. Your task is to identify and rank the top 10 news events from the past 24 hours (from 11:18 PM EST March 1, 2025, to 11:18 PM EST March 2, 2025). For each event, provide a title, brief summary, source (if available), and timestamp. Return the results in JSON format with fields: rank, title, summary, source, url (if known), and timestamp. Ensure the response is structured and concise."
            },
            {
            "role": "user",
            "content": "Give me the top 10 news events of the past 24 hours in JSON format."
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.5
        }
    print(HEADERS)
    response = requests.post(URL_DEEPSEARCH, headers=HEADERS, data=json.dumps(payload), timeout=30)
    print(response)
    if response.status_code == 200:
        # Create data directory if it doesn't exist
        raw_content = response.json()["choices"][0]["message"]["content"]
        news_data = json.loads(raw_content)
        print(news_data)
        data_dir = pathlib.Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Format filename with current timestamp
        filename = f"top_10_news_{end_time.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = data_dir / filename
        
        # Write response to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=2)
            
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
    