from fastapi import FastAPI, Request
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

# Load env variables from .env (for local testing)
load_dotenv()

# Create the FastAPI app
app = FastAPI()

# Initialize the OpenAI client with your environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/sum-numbers")
async def sum_numbers(request: Request):
    data = await request.json()
    image_b64 = data["image"]

    # Format image for OpenAI API (data URL)
    image_data_url = f"data:image/png;base64,{image_b64}"

    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        { "type": "text", "text": "Sum all numbers visible in this image. Return only the sum." },
                        { "type": "image_url", "image_url": { "url": image_data_url } }
                    ]
                }
            ],
            max_tokens=50
        )

        reply = response.choices[0].message.content.strip()
        return { "sum": reply }

    except Exception as e:
        return { "error": str(e) }
