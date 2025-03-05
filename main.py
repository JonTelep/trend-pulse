""" Main """
from api.xai import get_xai_news
from tools.handler import APIError
import os
from datetime import datetime, timedelta
import json
import pathlib
import pytz

def main():
    """ Main function """
    print("Getting XAI news...")
    est = pytz.timezone('America/New_York')
    end_time = datetime.now(est)
    start_time = end_time - timedelta(hours=24)
    try:
        response = get_xai_news()
        print(response)
        
        # Create data and raw_responses directories if they don't exist
        data_dir = pathlib.Path("data")
        raw_dir = data_dir / "raw_responses"
        data_dir.mkdir(exist_ok=True)
        raw_dir.mkdir(exist_ok=True)
        
        # Format filenames with current timestamp
        timestamp = end_time.strftime('%Y%m%d_%H%M%S')
        filename = f"top_10_news_{timestamp}.json"
        raw_filename = f"raw_response_{timestamp}.json"
        
        filepath = data_dir / filename
        raw_filepath = raw_dir / raw_filename
        
        # Always save the raw response
        with open(raw_filepath, 'w', encoding='utf-8') as f:
            json.dump(response, f, indent=2)
        
        if "choices" in response and len(response["choices"]) > 0:
            # Extract the content from the response
            raw_content = response["choices"][0]["message"]["content"]
            try:
                # Try to parse the content as JSON
                news_data = json.loads(raw_content)
                print(news_data)
                
                # Write the parsed news data to file
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(news_data, f, indent=2)
                print("Successfully retrieved and saved XAI news")
            except json.JSONDecodeError:
                # If content is not valid JSON, save the raw response
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(response, f, indent=2)
                print("Retrieved XAI news but content was not in JSON format")
        else:
            # Save the raw response if it doesn't have the expected structure
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(response, f, indent=2)
            print("Retrieved XAI news but response format was unexpected")
    except APIError as e:
        print(f"Failed to get XAI news: {e.message}")
        if e.status_code:
            print(f"Status code: {e.status_code}")

if __name__ == "__main__":
    main()
