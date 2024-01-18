"""OpenAi API for sentiment analysis."""

# import openai

# openai.api_key = "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"
# # from openai import OpenAI
# # client = OpenAI(api_key='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')
# # ENDPOINT = 'https://api.openai.com//v1/chat/completions'


# def get_sentiment(text):
#     """Analyze and score the comment measurement value.

#     Args:
#         text: comment type value.

#     Returns:
#         sentiment score of given comment.
#     """
#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         temperature=0.5,
#         max_tokens=1,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#         stop=["\n"],
#         messages=[
#             {
#                 "role": "system",
#                 "content": f"Sentiment analysis of the following text:\n\n{text}",
#             },
#             # {"role": "user", "content": f"Analyze the sentiment of the text
#             # ,provide a sentiment score from 0 to 10, where 0 is extremely negative,
#             #  10 is extremely positive, and 5 is neutral:\n\n{text}"},
#             # {"role": "user", "content": f"{text}"}
#         ],
#     )
#     sentiment = response.choices[0].message.content
#     return sentiment


# if __name__ == "__main__":
#     sample_text = "I love my mobile phone, it has a great camera."
#     # , it has a great camera.

#     sentiment = get_sentiment(sample_text)
#     print(f"The sentiment of the text is {sentiment}")

import json

import httpx


async def get_sentiment(text: str) -> str:
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
                "content": f"Sentiment analysis of the following text:\n\n{text}",
            }
        ],
    }

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(data),
        )
        response.raise_for_status()  # raise an exception for HTTP error responses

    sentiment = response.json()["choices"][0]["message"]["content"]
    return sentiment
