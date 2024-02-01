"""OpenAi API for sentiment analysis."""
import json
import os
import time

import httpx
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

HTTP_TOO_MANY_REQUESTS = 429


async def get_sentiment(text: str) -> int | None:
    """Analyze and score the sentiment of a given comment.

    Args:
        text: The comment to be analyzed.

    Returns:
        An integer representing the sentiment score of the given comment.
    """

    # Function to send request to GPT API
    async def send_request(prompt):
        data = {
            "model": "gpt-3.5-turbo",
            "temperature": 0.5,
            "max_tokens": 1,  # response
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": ["\n"],
            "messages": [{"role": "system", "content": prompt}],
        }
        api_key = os.getenv("CHATGPT_API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        retries = 3  # Number of retries
        backoff_factor = 2  # Backoff factor for exponential backoff
        max_delay = 32  # Maximum delay in seconds

        for attempt in range(retries):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        data=json.dumps(data),
                    )
                    response.raise_for_status()
                    return (
                        response.json()["choices"][0]["message"]["content"]
                        .strip()
                        .lower()
                    )

            except httpx.HTTPStatusError as e:
                if e.response.status_code == HTTP_TOO_MANY_REQUESTS:
                    # API throttling, apply exponential backoff
                    delay = min(backoff_factor**attempt, max_delay)
                    time.sleep(delay)
                else:
                    # If it's not a 429 error, raise the exception
                    raise
        # If all retries fail, raise the last exception
        raise Exception("Max retries reached, unable to make a successful request.")

    # First sentiment analysis to categorize sentiment
    primary_sentiment = await send_request(
        f"Analyze the sentiment of the following text,"
        f"Positive, Negative or Neutral:\n\n{text}"
    )
    print(primary_sentiment)
    # Assign score based on primary sentiment
    if primary_sentiment == "neutral":
        return 5

    elif primary_sentiment in ["positive", "negative"]:
        # Further sentiment analysis for scoring
        detailed_sentiment_prompt = (
            f"Analyze the sentiment of the following text"
            f"and provide a score from 0 to 4, or 6-10,"
            f"where 0 is extremely negative, 10 is extremely positive,"
            f"your output should be a number,"
            f"\n\n"
            f"{text}"
        )
        detailed_sentiment = await send_request(detailed_sentiment_prompt)
        print(detailed_sentiment)
        return detailed_sentiment

    else:
        return None  # In case the response is not one of the expected sentiments
