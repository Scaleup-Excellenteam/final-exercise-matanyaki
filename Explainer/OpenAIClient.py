import openai
from tenacity import retry, stop_after_attempt, wait_random_exponential
from openai import AsyncOpenAI

class OpenAIClient:
    def __init__(self, api_key):
        self.client = AsyncOpenAI(api_key=api_key)

    #Using to manage information in required pace
    @retry(
        stop=stop_after_attempt(3),  # Maximum number of retry attempts
        wait=wait_random_exponential(min=1, max=60),  # Exponential backoff with jitter
    )
    async def get_explanation(self, text: str) -> str:
        #Description for the api
        prompt = f"Explain the following slide content in concise language:\n\n{text}\n\nLimit the explanation to the key points and ensure it's shorter than the slide itself."

        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except openai.OpenAIError as e:
            return f"OpenAI API error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

