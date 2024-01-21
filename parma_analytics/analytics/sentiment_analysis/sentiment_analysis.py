"""OpenAi API for sentiment analysis."""
import json
import os

import httpx
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


async def get_sentiment(text: str) -> str | None:
    """Analyze and score the comment measurement value.

    Args:
        text: comment type value.

    Returns:
        sentiment score of given comment.
    """
    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.5,
        "max_tokens": 1,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": ["\n"],
        "messages": [
            {
                "role": "system",
                "content": (
                    f"Analyze the sentiment of the following text"
                    f"and provide a score from 0 to 10, "
                    f"where 0 is extremely negative, 10 is extremely positive,"
                    f"and 5 is neutral:\n\n"
                    f"{text}"
                ),
            }
        ],
    }
    api_key = os.getenv("OPENAI_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    retries = 0
    sentiment = None
    max_retries = 3
    while retries < max_retries and sentiment is None:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(data),
            )
            response.raise_for_status()  # raise an exception for HTTP error responses

        sentiment = response.json()["choices"][0]["message"]["content"]
        if (
            not sentiment.isdigit()
        ):  # If score is not a digit, set sentiment to None and retry
            sentiment = None
            retries += 1

    return sentiment
