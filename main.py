""" Main """
from api.xai import get_xai_news
from tools.handler import APIError

def main():
    """ Main function """
    print("Getting XAI news...")
    try:
        response = get_xai_news()
        if response:
            print("Successfully retrieved XAI news")
        else:
            print("No data received from XAI")
    except APIError as e:
        print(f"Failed to get XAI news: {e.message}")
        if e.status_code:
            print(f"Status code: {e.status_code}")

if __name__ == "__main__":
    main()
