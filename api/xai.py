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
    "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


@api_handler(max_retries=0, retry_delay=10.0, timeout=30)
def get_xai_news():
    """ Get XAI news """

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

    response = requests.post(URL_DEEPSEARCH, headers=HEADERS, data=json.dumps(payload), timeout=30)
    return response.json()
