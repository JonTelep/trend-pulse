""" Perplexity API """
import requests
from dotenv import load_dotenv
import os
from tools.handler import api_handler
load_dotenv()

URL_PERPLEXITY = "https://api.perplexity.ai/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
    "Content-Type": "application/json"
}

@api_handler(max_retries=0, retry_delay=10.0, timeout=30)
def get_perplexity_response(prompt):
    """ Get Perplexity response """
    payload = {
        "model": "sonar",
        "messages": [
            prompt
        ],
        "max_tokens": 123,
        "temperature": 0.2,
        "top_p": 0.9,
        "search_domain_filter": None,
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "<string>",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1,
        "response_format": None
    }


    response = requests.request("POST", URL_PERPLEXITY, json=payload, headers=HEADERS, timeout=30)

    return response.json()
