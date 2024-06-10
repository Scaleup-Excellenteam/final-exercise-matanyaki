import aiohttp
import openai
from aiohttp import ClientSession


class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key

    async def get_explanation(self, session : ClientSession, text : str) -> str:
        prompt = f"Explain the following slide content in detail:\n\n{text}"
        try:
            async with session.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    'max_tokens': 500
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['choices'][0]['message']['content'].strip()
                else:
                    return f"Error: {response.status} - {response.reason}"
        except aiohttp.ClientError as e:
            return f"HTTP error: {str(e)}"
        except openai.OpenAIError as e:
            return f"OpenAI API error: {str(e)}"
